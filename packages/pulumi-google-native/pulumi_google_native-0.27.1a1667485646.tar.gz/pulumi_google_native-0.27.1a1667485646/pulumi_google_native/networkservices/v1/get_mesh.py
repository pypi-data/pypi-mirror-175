# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = [
    'GetMeshResult',
    'AwaitableGetMeshResult',
    'get_mesh',
    'get_mesh_output',
]

@pulumi.output_type
class GetMeshResult:
    def __init__(__self__, create_time=None, description=None, interception_port=None, labels=None, name=None, self_link=None, update_time=None):
        if create_time and not isinstance(create_time, str):
            raise TypeError("Expected argument 'create_time' to be a str")
        pulumi.set(__self__, "create_time", create_time)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if interception_port and not isinstance(interception_port, int):
            raise TypeError("Expected argument 'interception_port' to be a int")
        pulumi.set(__self__, "interception_port", interception_port)
        if labels and not isinstance(labels, dict):
            raise TypeError("Expected argument 'labels' to be a dict")
        pulumi.set(__self__, "labels", labels)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if self_link and not isinstance(self_link, str):
            raise TypeError("Expected argument 'self_link' to be a str")
        pulumi.set(__self__, "self_link", self_link)
        if update_time and not isinstance(update_time, str):
            raise TypeError("Expected argument 'update_time' to be a str")
        pulumi.set(__self__, "update_time", update_time)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> str:
        """
        The timestamp when the resource was created.
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        Optional. A free-text description of the resource. Max length 1024 characters.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="interceptionPort")
    def interception_port(self) -> int:
        """
        Optional. If set to a valid TCP port (1-65535), instructs the SIDECAR proxy to listen on the specified port of localhost (127.0.0.1) address. The SIDECAR proxy will expect all traffic to be redirected to this port regardless of its actual ip:port destination. If unset, a port '15001' is used as the interception port. This will is applicable only for sidecar proxy deployments.
        """
        return pulumi.get(self, "interception_port")

    @property
    @pulumi.getter
    def labels(self) -> Mapping[str, str]:
        """
        Optional. Set of label tags associated with the Mesh resource.
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the Mesh resource. It matches pattern `projects/*/locations/global/meshes/`.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="selfLink")
    def self_link(self) -> str:
        """
        Server-defined URL of this resource
        """
        return pulumi.get(self, "self_link")

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> str:
        """
        The timestamp when the resource was updated.
        """
        return pulumi.get(self, "update_time")


class AwaitableGetMeshResult(GetMeshResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetMeshResult(
            create_time=self.create_time,
            description=self.description,
            interception_port=self.interception_port,
            labels=self.labels,
            name=self.name,
            self_link=self.self_link,
            update_time=self.update_time)


def get_mesh(location: Optional[str] = None,
             mesh_id: Optional[str] = None,
             project: Optional[str] = None,
             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetMeshResult:
    """
    Gets details of a single Mesh.
    """
    __args__ = dict()
    __args__['location'] = location
    __args__['meshId'] = mesh_id
    __args__['project'] = project
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('google-native:networkservices/v1:getMesh', __args__, opts=opts, typ=GetMeshResult).value

    return AwaitableGetMeshResult(
        create_time=__ret__.create_time,
        description=__ret__.description,
        interception_port=__ret__.interception_port,
        labels=__ret__.labels,
        name=__ret__.name,
        self_link=__ret__.self_link,
        update_time=__ret__.update_time)


@_utilities.lift_output_func(get_mesh)
def get_mesh_output(location: Optional[pulumi.Input[str]] = None,
                    mesh_id: Optional[pulumi.Input[str]] = None,
                    project: Optional[pulumi.Input[Optional[str]]] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetMeshResult]:
    """
    Gets details of a single Mesh.
    """
    ...
