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
    'GetInstanceGroupManagerResizeRequestResult',
    'AwaitableGetInstanceGroupManagerResizeRequestResult',
    'get_instance_group_manager_resize_request',
    'get_instance_group_manager_resize_request_output',
]

@pulumi.output_type
class GetInstanceGroupManagerResizeRequestResult:
    def __init__(__self__, count=None, creation_timestamp=None, description=None, kind=None, name=None, queuing_policy=None, self_link=None, self_link_with_id=None, state=None, status=None, zone=None):
        if count and not isinstance(count, int):
            raise TypeError("Expected argument 'count' to be a int")
        pulumi.set(__self__, "count", count)
        if creation_timestamp and not isinstance(creation_timestamp, str):
            raise TypeError("Expected argument 'creation_timestamp' to be a str")
        pulumi.set(__self__, "creation_timestamp", creation_timestamp)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if queuing_policy and not isinstance(queuing_policy, dict):
            raise TypeError("Expected argument 'queuing_policy' to be a dict")
        pulumi.set(__self__, "queuing_policy", queuing_policy)
        if self_link and not isinstance(self_link, str):
            raise TypeError("Expected argument 'self_link' to be a str")
        pulumi.set(__self__, "self_link", self_link)
        if self_link_with_id and not isinstance(self_link_with_id, str):
            raise TypeError("Expected argument 'self_link_with_id' to be a str")
        pulumi.set(__self__, "self_link_with_id", self_link_with_id)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if status and not isinstance(status, dict):
            raise TypeError("Expected argument 'status' to be a dict")
        pulumi.set(__self__, "status", status)
        if zone and not isinstance(zone, str):
            raise TypeError("Expected argument 'zone' to be a str")
        pulumi.set(__self__, "zone", zone)

    @property
    @pulumi.getter
    def count(self) -> int:
        """
        The count of instances to create as part of this resize request.
        """
        return pulumi.get(self, "count")

    @property
    @pulumi.getter(name="creationTimestamp")
    def creation_timestamp(self) -> str:
        """
        The creation timestamp for this resize request in RFC3339 text format.
        """
        return pulumi.get(self, "creation_timestamp")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        An optional description of this resource.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def kind(self) -> str:
        """
        The resource type, which is always compute#instanceGroupManagerResizeRequest for resize requests.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of this resize request. The name must be 1-63 characters long, and comply with RFC1035.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="queuingPolicy")
    def queuing_policy(self) -> 'outputs.QueuingPolicyResponse':
        """
        When set, defines queing parameters for the requested deferred capacity. When unset, the request starts provisioning immediately, or fails if immediate provisioning is not possible.
        """
        return pulumi.get(self, "queuing_policy")

    @property
    @pulumi.getter(name="selfLink")
    def self_link(self) -> str:
        """
        The URL for this resize request. The server defines this URL.
        """
        return pulumi.get(self, "self_link")

    @property
    @pulumi.getter(name="selfLinkWithId")
    def self_link_with_id(self) -> str:
        """
        Server-defined URL for this resource with the resource id.
        """
        return pulumi.get(self, "self_link_with_id")

    @property
    @pulumi.getter
    def state(self) -> str:
        """
        [Output only] Current state of the request.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def status(self) -> 'outputs.InstanceGroupManagerResizeRequestStatusResponse':
        """
        [Output only] Status of the request. The Status message is aligned with QueuedResource.status. ResizeRequest.queuing_policy contains the queuing policy as provided by the user; it could have either valid_until_time or valid_until_duration. ResizeRequest.status.queuing_policy always contains absolute time as calculated by the server when the request is queued.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def zone(self) -> str:
        """
        The URL of a zone where the resize request is located.
        """
        return pulumi.get(self, "zone")


class AwaitableGetInstanceGroupManagerResizeRequestResult(GetInstanceGroupManagerResizeRequestResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetInstanceGroupManagerResizeRequestResult(
            count=self.count,
            creation_timestamp=self.creation_timestamp,
            description=self.description,
            kind=self.kind,
            name=self.name,
            queuing_policy=self.queuing_policy,
            self_link=self.self_link,
            self_link_with_id=self.self_link_with_id,
            state=self.state,
            status=self.status,
            zone=self.zone)


def get_instance_group_manager_resize_request(instance_group_manager: Optional[str] = None,
                                              project: Optional[str] = None,
                                              resize_request: Optional[str] = None,
                                              zone: Optional[str] = None,
                                              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetInstanceGroupManagerResizeRequestResult:
    """
    Returns all of the details about the specified resize request.
    """
    __args__ = dict()
    __args__['instanceGroupManager'] = instance_group_manager
    __args__['project'] = project
    __args__['resizeRequest'] = resize_request
    __args__['zone'] = zone
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('google-native:compute/alpha:getInstanceGroupManagerResizeRequest', __args__, opts=opts, typ=GetInstanceGroupManagerResizeRequestResult).value

    return AwaitableGetInstanceGroupManagerResizeRequestResult(
        count=__ret__.count,
        creation_timestamp=__ret__.creation_timestamp,
        description=__ret__.description,
        kind=__ret__.kind,
        name=__ret__.name,
        queuing_policy=__ret__.queuing_policy,
        self_link=__ret__.self_link,
        self_link_with_id=__ret__.self_link_with_id,
        state=__ret__.state,
        status=__ret__.status,
        zone=__ret__.zone)


@_utilities.lift_output_func(get_instance_group_manager_resize_request)
def get_instance_group_manager_resize_request_output(instance_group_manager: Optional[pulumi.Input[str]] = None,
                                                     project: Optional[pulumi.Input[Optional[str]]] = None,
                                                     resize_request: Optional[pulumi.Input[str]] = None,
                                                     zone: Optional[pulumi.Input[str]] = None,
                                                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetInstanceGroupManagerResizeRequestResult]:
    """
    Returns all of the details about the specified resize request.
    """
    ...
