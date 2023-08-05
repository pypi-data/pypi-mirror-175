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

__all__ = [
    'GetOrganizationInspectTemplateResult',
    'AwaitableGetOrganizationInspectTemplateResult',
    'get_organization_inspect_template',
    'get_organization_inspect_template_output',
]

@pulumi.output_type
class GetOrganizationInspectTemplateResult:
    def __init__(__self__, create_time=None, description=None, display_name=None, inspect_config=None, name=None, update_time=None):
        if create_time and not isinstance(create_time, str):
            raise TypeError("Expected argument 'create_time' to be a str")
        pulumi.set(__self__, "create_time", create_time)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if inspect_config and not isinstance(inspect_config, dict):
            raise TypeError("Expected argument 'inspect_config' to be a dict")
        pulumi.set(__self__, "inspect_config", inspect_config)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if update_time and not isinstance(update_time, str):
            raise TypeError("Expected argument 'update_time' to be a str")
        pulumi.set(__self__, "update_time", update_time)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> str:
        """
        The creation timestamp of an inspectTemplate.
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        Short description (max 256 chars).
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> str:
        """
        Display name (max 256 chars).
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter(name="inspectConfig")
    def inspect_config(self) -> 'outputs.GooglePrivacyDlpV2InspectConfigResponse':
        """
        The core content of the template. Configuration of the scanning process.
        """
        return pulumi.get(self, "inspect_config")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The template name. The template will have one of the following formats: `projects/PROJECT_ID/inspectTemplates/TEMPLATE_ID` OR `organizations/ORGANIZATION_ID/inspectTemplates/TEMPLATE_ID`;
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> str:
        """
        The last update timestamp of an inspectTemplate.
        """
        return pulumi.get(self, "update_time")


class AwaitableGetOrganizationInspectTemplateResult(GetOrganizationInspectTemplateResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetOrganizationInspectTemplateResult(
            create_time=self.create_time,
            description=self.description,
            display_name=self.display_name,
            inspect_config=self.inspect_config,
            name=self.name,
            update_time=self.update_time)


def get_organization_inspect_template(inspect_template_id: Optional[str] = None,
                                      location: Optional[str] = None,
                                      organization_id: Optional[str] = None,
                                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetOrganizationInspectTemplateResult:
    """
    Gets an InspectTemplate. See https://cloud.google.com/dlp/docs/creating-templates to learn more.
    """
    __args__ = dict()
    __args__['inspectTemplateId'] = inspect_template_id
    __args__['location'] = location
    __args__['organizationId'] = organization_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('google-native:dlp/v2:getOrganizationInspectTemplate', __args__, opts=opts, typ=GetOrganizationInspectTemplateResult).value

    return AwaitableGetOrganizationInspectTemplateResult(
        create_time=__ret__.create_time,
        description=__ret__.description,
        display_name=__ret__.display_name,
        inspect_config=__ret__.inspect_config,
        name=__ret__.name,
        update_time=__ret__.update_time)


@_utilities.lift_output_func(get_organization_inspect_template)
def get_organization_inspect_template_output(inspect_template_id: Optional[pulumi.Input[str]] = None,
                                             location: Optional[pulumi.Input[str]] = None,
                                             organization_id: Optional[pulumi.Input[str]] = None,
                                             opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetOrganizationInspectTemplateResult]:
    """
    Gets an InspectTemplate. See https://cloud.google.com/dlp/docs/creating-templates to learn more.
    """
    ...
