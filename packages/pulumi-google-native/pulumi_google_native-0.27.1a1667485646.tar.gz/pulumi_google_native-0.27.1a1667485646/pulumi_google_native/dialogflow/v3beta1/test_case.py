# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
from ._inputs import *

__all__ = ['TestCaseArgs', 'TestCase']

@pulumi.input_type
class TestCaseArgs:
    def __init__(__self__, *,
                 agent_id: pulumi.Input[str],
                 display_name: pulumi.Input[str],
                 last_test_result: Optional[pulumi.Input['GoogleCloudDialogflowCxV3beta1TestCaseResultArgs']] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 notes: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 test_case_conversation_turns: Optional[pulumi.Input[Sequence[pulumi.Input['GoogleCloudDialogflowCxV3beta1ConversationTurnArgs']]]] = None,
                 test_config: Optional[pulumi.Input['GoogleCloudDialogflowCxV3beta1TestConfigArgs']] = None):
        """
        The set of arguments for constructing a TestCase resource.
        :param pulumi.Input[str] display_name: The human-readable name of the test case, unique within the agent. Limit of 200 characters.
        :param pulumi.Input['GoogleCloudDialogflowCxV3beta1TestCaseResultArgs'] last_test_result: The latest test result.
        :param pulumi.Input[str] name: The unique identifier of the test case. TestCases.CreateTestCase will populate the name automatically. Otherwise use format: `projects//locations//agents/ /testCases/`.
        :param pulumi.Input[str] notes: Additional freeform notes about the test case. Limit of 400 characters.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: Tags are short descriptions that users may apply to test cases for organizational and filtering purposes. Each tag should start with "#" and has a limit of 30 characters.
        :param pulumi.Input[Sequence[pulumi.Input['GoogleCloudDialogflowCxV3beta1ConversationTurnArgs']]] test_case_conversation_turns: The conversation turns uttered when the test case was created, in chronological order. These include the canonical set of agent utterances that should occur when the agent is working properly.
        :param pulumi.Input['GoogleCloudDialogflowCxV3beta1TestConfigArgs'] test_config: Config for the test case.
        """
        pulumi.set(__self__, "agent_id", agent_id)
        pulumi.set(__self__, "display_name", display_name)
        if last_test_result is not None:
            pulumi.set(__self__, "last_test_result", last_test_result)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if notes is not None:
            pulumi.set(__self__, "notes", notes)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if test_case_conversation_turns is not None:
            pulumi.set(__self__, "test_case_conversation_turns", test_case_conversation_turns)
        if test_config is not None:
            pulumi.set(__self__, "test_config", test_config)

    @property
    @pulumi.getter(name="agentId")
    def agent_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "agent_id")

    @agent_id.setter
    def agent_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "agent_id", value)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Input[str]:
        """
        The human-readable name of the test case, unique within the agent. Limit of 200 characters.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter(name="lastTestResult")
    def last_test_result(self) -> Optional[pulumi.Input['GoogleCloudDialogflowCxV3beta1TestCaseResultArgs']]:
        """
        The latest test result.
        """
        return pulumi.get(self, "last_test_result")

    @last_test_result.setter
    def last_test_result(self, value: Optional[pulumi.Input['GoogleCloudDialogflowCxV3beta1TestCaseResultArgs']]):
        pulumi.set(self, "last_test_result", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The unique identifier of the test case. TestCases.CreateTestCase will populate the name automatically. Otherwise use format: `projects//locations//agents/ /testCases/`.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def notes(self) -> Optional[pulumi.Input[str]]:
        """
        Additional freeform notes about the test case. Limit of 400 characters.
        """
        return pulumi.get(self, "notes")

    @notes.setter
    def notes(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "notes", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Tags are short descriptions that users may apply to test cases for organizational and filtering purposes. Each tag should start with "#" and has a limit of 30 characters.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="testCaseConversationTurns")
    def test_case_conversation_turns(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['GoogleCloudDialogflowCxV3beta1ConversationTurnArgs']]]]:
        """
        The conversation turns uttered when the test case was created, in chronological order. These include the canonical set of agent utterances that should occur when the agent is working properly.
        """
        return pulumi.get(self, "test_case_conversation_turns")

    @test_case_conversation_turns.setter
    def test_case_conversation_turns(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['GoogleCloudDialogflowCxV3beta1ConversationTurnArgs']]]]):
        pulumi.set(self, "test_case_conversation_turns", value)

    @property
    @pulumi.getter(name="testConfig")
    def test_config(self) -> Optional[pulumi.Input['GoogleCloudDialogflowCxV3beta1TestConfigArgs']]:
        """
        Config for the test case.
        """
        return pulumi.get(self, "test_config")

    @test_config.setter
    def test_config(self, value: Optional[pulumi.Input['GoogleCloudDialogflowCxV3beta1TestConfigArgs']]):
        pulumi.set(self, "test_config", value)


class TestCase(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 agent_id: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 last_test_result: Optional[pulumi.Input[pulumi.InputType['GoogleCloudDialogflowCxV3beta1TestCaseResultArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 notes: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 test_case_conversation_turns: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['GoogleCloudDialogflowCxV3beta1ConversationTurnArgs']]]]] = None,
                 test_config: Optional[pulumi.Input[pulumi.InputType['GoogleCloudDialogflowCxV3beta1TestConfigArgs']]] = None,
                 __props__=None):
        """
        Creates a test case for the given agent.
        Note - this resource's API doesn't support deletion. When deleted, the resource will persist
        on Google Cloud even though it will be deleted from Pulumi state.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] display_name: The human-readable name of the test case, unique within the agent. Limit of 200 characters.
        :param pulumi.Input[pulumi.InputType['GoogleCloudDialogflowCxV3beta1TestCaseResultArgs']] last_test_result: The latest test result.
        :param pulumi.Input[str] name: The unique identifier of the test case. TestCases.CreateTestCase will populate the name automatically. Otherwise use format: `projects//locations//agents/ /testCases/`.
        :param pulumi.Input[str] notes: Additional freeform notes about the test case. Limit of 400 characters.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: Tags are short descriptions that users may apply to test cases for organizational and filtering purposes. Each tag should start with "#" and has a limit of 30 characters.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['GoogleCloudDialogflowCxV3beta1ConversationTurnArgs']]]] test_case_conversation_turns: The conversation turns uttered when the test case was created, in chronological order. These include the canonical set of agent utterances that should occur when the agent is working properly.
        :param pulumi.Input[pulumi.InputType['GoogleCloudDialogflowCxV3beta1TestConfigArgs']] test_config: Config for the test case.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: TestCaseArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Creates a test case for the given agent.
        Note - this resource's API doesn't support deletion. When deleted, the resource will persist
        on Google Cloud even though it will be deleted from Pulumi state.

        :param str resource_name: The name of the resource.
        :param TestCaseArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(TestCaseArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 agent_id: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 last_test_result: Optional[pulumi.Input[pulumi.InputType['GoogleCloudDialogflowCxV3beta1TestCaseResultArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 notes: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 test_case_conversation_turns: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['GoogleCloudDialogflowCxV3beta1ConversationTurnArgs']]]]] = None,
                 test_config: Optional[pulumi.Input[pulumi.InputType['GoogleCloudDialogflowCxV3beta1TestConfigArgs']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = TestCaseArgs.__new__(TestCaseArgs)

            if agent_id is None and not opts.urn:
                raise TypeError("Missing required property 'agent_id'")
            __props__.__dict__["agent_id"] = agent_id
            if display_name is None and not opts.urn:
                raise TypeError("Missing required property 'display_name'")
            __props__.__dict__["display_name"] = display_name
            __props__.__dict__["last_test_result"] = last_test_result
            __props__.__dict__["location"] = location
            __props__.__dict__["name"] = name
            __props__.__dict__["notes"] = notes
            __props__.__dict__["project"] = project
            __props__.__dict__["tags"] = tags
            __props__.__dict__["test_case_conversation_turns"] = test_case_conversation_turns
            __props__.__dict__["test_config"] = test_config
            __props__.__dict__["creation_time"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["agent_id", "location", "project"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(TestCase, __self__).__init__(
            'google-native:dialogflow/v3beta1:TestCase',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'TestCase':
        """
        Get an existing TestCase resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = TestCaseArgs.__new__(TestCaseArgs)

        __props__.__dict__["agent_id"] = None
        __props__.__dict__["creation_time"] = None
        __props__.__dict__["display_name"] = None
        __props__.__dict__["last_test_result"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["notes"] = None
        __props__.__dict__["project"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["test_case_conversation_turns"] = None
        __props__.__dict__["test_config"] = None
        return TestCase(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="agentId")
    def agent_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "agent_id")

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> pulumi.Output[str]:
        """
        When the test was created.
        """
        return pulumi.get(self, "creation_time")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[str]:
        """
        The human-readable name of the test case, unique within the agent. Limit of 200 characters.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter(name="lastTestResult")
    def last_test_result(self) -> pulumi.Output['outputs.GoogleCloudDialogflowCxV3beta1TestCaseResultResponse']:
        """
        The latest test result.
        """
        return pulumi.get(self, "last_test_result")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The unique identifier of the test case. TestCases.CreateTestCase will populate the name automatically. Otherwise use format: `projects//locations//agents/ /testCases/`.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def notes(self) -> pulumi.Output[str]:
        """
        Additional freeform notes about the test case. Limit of 400 characters.
        """
        return pulumi.get(self, "notes")

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        return pulumi.get(self, "project")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Sequence[str]]:
        """
        Tags are short descriptions that users may apply to test cases for organizational and filtering purposes. Each tag should start with "#" and has a limit of 30 characters.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="testCaseConversationTurns")
    def test_case_conversation_turns(self) -> pulumi.Output[Sequence['outputs.GoogleCloudDialogflowCxV3beta1ConversationTurnResponse']]:
        """
        The conversation turns uttered when the test case was created, in chronological order. These include the canonical set of agent utterances that should occur when the agent is working properly.
        """
        return pulumi.get(self, "test_case_conversation_turns")

    @property
    @pulumi.getter(name="testConfig")
    def test_config(self) -> pulumi.Output['outputs.GoogleCloudDialogflowCxV3beta1TestConfigResponse']:
        """
        Config for the test case.
        """
        return pulumi.get(self, "test_config")

