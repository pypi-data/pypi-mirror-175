# -*- coding: utf-8 -*-
# Copyright (C) 2012 Matthew Hampton
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301  USA

import copy
import os

from lxml import etree

from .ValidationException import ValidationException
from .TaskParser import TaskParser
from ..workflow import BpmnWorkflow
from .util import first, one, DEFAULT_NSMAP
from ..specs.events import (TimerEventDefinition, MessageEventDefinition,
                            EscalationEventDefinition,SignalEventDefinition,
                            CancelEventDefinition, CycleTimerEventDefinition)
from ...exceptions import WorkflowException
from ...bpmn.specs.events import IntermediateCatchEvent

CAMUNDA_MODEL_NS = 'http://camunda.org/schema/1.0/bpmn'


class UserTaskParser(TaskParser):

    """
    Base class for parsing User Tasks
    """
    pass


class ManualTaskParser(UserTaskParser):

    """
    Base class for parsing Manual Tasks. Currently assumes that Manual Tasks
    should be treated the same way as User Tasks.
    """
    pass


class NoneTaskParser(UserTaskParser):

    """
    Base class for parsing unspecified Tasks. Currently assumes that such Tasks
    should be treated the same way as User Tasks.
    """
    pass


class ExclusiveGatewayParser(TaskParser):
    """
    Parses an Exclusive Gateway, setting up the outgoing conditions
    appropriately.
    """

    def connect_outgoing(self, outgoing_task, outgoing_task_node,
                         sequence_flow_node, is_default):
        if is_default:
            super(ExclusiveGatewayParser, self).connect_outgoing(
                outgoing_task, outgoing_task_node, sequence_flow_node,
                is_default)
        else:
            cond = self.parser.parse_condition(sequence_flow_node)
            if cond is None:
                raise ValidationException(
                    'Non-default exclusive outgoing sequence flow '
                    ' without condition',
                    sequence_flow_node,
                    self.process_parser.filename)
            self.task.connect_outgoing_if(
                cond, outgoing_task,
                sequence_flow_node.get('id'),
                sequence_flow_node.get('name', None),
                self.parser.parse_documentation(sequence_flow_node))

    def handles_multiple_outgoing(self):
        return True


class ParallelGatewayParser(TaskParser):

    """
    Parses a Parallel Gateway.
    """

    def handles_multiple_outgoing(self):
        return True


class InclusiveGatewayParser(TaskParser):

    """
    Parses an Inclusive Gateway.
    """

    def handles_multiple_outgoing(self):
        """
        At the moment I haven't implemented support for diverging inclusive
        gateways
        """
        return False


class SubWorkflowParser(TaskParser):

    """
    Base class for parsing unspecified Tasks. Currently assumes that such Tasks
    should be treated the same way as User Tasks.
    """
    def create_task(self):
        wf_spec = self.get_subprocess_spec()
        return self.spec_class(
            self.spec, self.get_task_spec_name(), bpmn_wf_spec=wf_spec,
            bpmn_wf_class=self.parser.WORKFLOW_CLASS,
            position=self.process_parser.get_coord(self.get_id()),
            lane=self.get_lane(),
            description=self.node.get('name', None))

    def get_subprocess_spec(self):

        workflowStartEvent = self.xpath('./bpmn:startEvent')
        workflowEndEvent =  self.xpath('./bpmn:endEvent')
        if len(workflowStartEvent) != 1:
            raise ValidationException(
                'Multiple Start points are not allowed in SubWorkflow Task',
                node=self.node,
                filename=self.process_parser.filename)
        if len(workflowEndEvent) == 0:
            raise ValidationException(
                'A SubWorkflow Must contain an End event',
                node=self.node,
                filename=self.process_parser.filename)

        nsmap = DEFAULT_NSMAP.copy()
        nsmap['camunda'] = "http://camunda.org/schema/1.0/bpmn"
        nsmap['di'] = "http://www.omg.org/spec/DD/20100524/DI"

        # Create wrapper xml for the subworkflow
        for ns, val in nsmap.items():
            etree.register_namespace(ns, val)

        self.parser.create_parser(
            self.node,
            doc_xpath=self.process_parser.doc_xpath,
            filename=self.process_parser.filename,
            current_lane=self.get_lane()
        )
        wf_spec = self.parser.get_spec(self.node.get('id'))
        wf_spec.file = self.process_parser.filename
        return wf_spec


class TransactionSubprocessParser(SubWorkflowParser):
    """Parses a transaction node"""

    def create_task(self):
        wf_spec = self.get_subprocess_spec()
        return self.spec_class(
            self.spec, self.get_task_spec_name(), bpmn_wf_spec=wf_spec,
            bpmn_wf_class=self.parser.WORKFLOW_CLASS,
            position=self.process_parser.get_coord(self.get_id()),
            description=self.node.get('name', None))


class CallActivityParser(TaskParser):
    """Parses a CallActivity node."""

    def create_task(self):
        wf_spec = self.get_subprocess_spec()
        return self.spec_class(
            self.spec, self.get_task_spec_name(), bpmn_wf_spec=wf_spec,
            bpmn_wf_class=self.parser.WORKFLOW_CLASS,
            position=self.process_parser.get_coord(self.get_id()),
            description=self.node.get('name', None))

    def get_subprocess_spec(self):
        calledElement = self.node.get('calledElement', None)
        if not calledElement:
            raise ValidationException(
                'No "calledElement" attribute for Call Activity.',
                node=self.node,
                filename=self.process_parser.filename)
        parser = self.parser.get_process_parser(calledElement)
        if parser is None:
            raise ValidationException(
                f"The process '{calledElement}' was not found. Did you mean one of the following: "
                f"{', '.join(self.parser.get_process_ids())}?",
                node=self.node,
                filename=self.process_parser.filename)
        return parser.get_spec()


class ScriptTaskParser(TaskParser):
    """
    Parses a script task
    """

    def create_task(self):
        if type(self.get_script()) is not dict:
            script = self.get_script()
            return self.spec_class(self.spec, self.get_task_spec_name(), script,
                                lane=self.get_lane(),
                                position=self.process_parser.get_coord(
                                    self.get_id()),
                                description=self.node.get('name', None))
        else:
            script = self.get_script()['script']
            return self.spec_class(self.spec, self.get_task_spec_name(), script,
                                lane=self.get_lane(),
                                position=self.process_parser.get_coord(
                                    self.get_id()),
                                description=self.node.get('name', None) + '_EXTERNAL')  # Adding _EXTERNAL so we can catch it in bpmn_uploader to change it's class.  # noqa: E501

    def get_script(self):
        """
        Gets the script content from the node. A subclass can override this
        method, if the script needs to be pre-parsed. The result of this call
        will be passed to the Script Engine for execution.
        """
        try:
            try:
                return one(self.xpath('.//bpmn:script')).text
            except:
                external_script = {
                    'script': self.node.attrib['{http://camunda.org/schema/1.0/bpmn}resource']  # Returning a dict so that we can identify it is a external script task.  # noqa: E501
                }
                return external_script
        except AssertionError as ae:
            raise ValidationException(
                f"Invalid Script Task.  No Script Provided. ",
                node=self.node, filename=self.process_parser.filename)
