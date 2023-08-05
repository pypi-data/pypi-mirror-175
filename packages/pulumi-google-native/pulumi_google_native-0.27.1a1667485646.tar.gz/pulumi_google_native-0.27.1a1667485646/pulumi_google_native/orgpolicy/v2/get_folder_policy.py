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
    'GetFolderPolicyResult',
    'AwaitableGetFolderPolicyResult',
    'get_folder_policy',
    'get_folder_policy_output',
]

@pulumi.output_type
class GetFolderPolicyResult:
    def __init__(__self__, alternate=None, name=None, spec=None):
        if alternate and not isinstance(alternate, dict):
            raise TypeError("Expected argument 'alternate' to be a dict")
        if alternate is not None:
            warnings.warn("""Deprecated.""", DeprecationWarning)
            pulumi.log.warn("""alternate is deprecated: Deprecated.""")

        pulumi.set(__self__, "alternate", alternate)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if spec and not isinstance(spec, dict):
            raise TypeError("Expected argument 'spec' to be a dict")
        pulumi.set(__self__, "spec", spec)

    @property
    @pulumi.getter
    def alternate(self) -> 'outputs.GoogleCloudOrgpolicyV2AlternatePolicySpecResponse':
        """
        Deprecated.
        """
        return pulumi.get(self, "alternate")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Immutable. The resource name of the Policy. Must be one of the following forms, where constraint_name is the name of the constraint which this Policy configures: * `projects/{project_number}/policies/{constraint_name}` * `folders/{folder_id}/policies/{constraint_name}` * `organizations/{organization_id}/policies/{constraint_name}` For example, "projects/123/policies/compute.disableSerialPortAccess". Note: `projects/{project_id}/policies/{constraint_name}` is also an acceptable name for API requests, but responses will return the name using the equivalent project number.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def spec(self) -> 'outputs.GoogleCloudOrgpolicyV2PolicySpecResponse':
        """
        Basic information about the Organization Policy.
        """
        return pulumi.get(self, "spec")


class AwaitableGetFolderPolicyResult(GetFolderPolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetFolderPolicyResult(
            alternate=self.alternate,
            name=self.name,
            spec=self.spec)


def get_folder_policy(folder_id: Optional[str] = None,
                      policy_id: Optional[str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetFolderPolicyResult:
    """
    Gets a `Policy` on a resource. If no `Policy` is set on the resource, NOT_FOUND is returned. The `etag` value can be used with `UpdatePolicy()` to update a `Policy` during read-modify-write.
    """
    __args__ = dict()
    __args__['folderId'] = folder_id
    __args__['policyId'] = policy_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('google-native:orgpolicy/v2:getFolderPolicy', __args__, opts=opts, typ=GetFolderPolicyResult).value

    return AwaitableGetFolderPolicyResult(
        alternate=__ret__.alternate,
        name=__ret__.name,
        spec=__ret__.spec)


@_utilities.lift_output_func(get_folder_policy)
def get_folder_policy_output(folder_id: Optional[pulumi.Input[str]] = None,
                             policy_id: Optional[pulumi.Input[str]] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetFolderPolicyResult]:
    """
    Gets a `Policy` on a resource. If no `Policy` is set on the resource, NOT_FOUND is returned. The `etag` value can be used with `UpdatePolicy()` to update a `Policy` during read-modify-write.
    """
    ...
