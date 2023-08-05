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
    'GetDeploymentResult',
    'AwaitableGetDeploymentResult',
    'get_deployment',
    'get_deployment_output',
]

@pulumi.output_type
class GetDeploymentResult:
    def __init__(__self__, description=None, fingerprint=None, insert_time=None, labels=None, manifest=None, name=None, operation=None, self_link=None, target=None, update=None, update_time=None):
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if fingerprint and not isinstance(fingerprint, str):
            raise TypeError("Expected argument 'fingerprint' to be a str")
        pulumi.set(__self__, "fingerprint", fingerprint)
        if insert_time and not isinstance(insert_time, str):
            raise TypeError("Expected argument 'insert_time' to be a str")
        pulumi.set(__self__, "insert_time", insert_time)
        if labels and not isinstance(labels, list):
            raise TypeError("Expected argument 'labels' to be a list")
        pulumi.set(__self__, "labels", labels)
        if manifest and not isinstance(manifest, str):
            raise TypeError("Expected argument 'manifest' to be a str")
        pulumi.set(__self__, "manifest", manifest)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if operation and not isinstance(operation, dict):
            raise TypeError("Expected argument 'operation' to be a dict")
        pulumi.set(__self__, "operation", operation)
        if self_link and not isinstance(self_link, str):
            raise TypeError("Expected argument 'self_link' to be a str")
        pulumi.set(__self__, "self_link", self_link)
        if target and not isinstance(target, dict):
            raise TypeError("Expected argument 'target' to be a dict")
        pulumi.set(__self__, "target", target)
        if update and not isinstance(update, dict):
            raise TypeError("Expected argument 'update' to be a dict")
        pulumi.set(__self__, "update", update)
        if update_time and not isinstance(update_time, str):
            raise TypeError("Expected argument 'update_time' to be a str")
        pulumi.set(__self__, "update_time", update_time)

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        An optional user-provided description of the deployment.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def fingerprint(self) -> str:
        """
        Provides a fingerprint to use in requests to modify a deployment, such as `update()`, `stop()`, and `cancelPreview()` requests. A fingerprint is a randomly generated value that must be provided with `update()`, `stop()`, and `cancelPreview()` requests to perform optimistic locking. This ensures optimistic concurrency so that only one request happens at a time. The fingerprint is initially generated by Deployment Manager and changes after every request to modify data. To get the latest fingerprint value, perform a `get()` request to a deployment.
        """
        return pulumi.get(self, "fingerprint")

    @property
    @pulumi.getter(name="insertTime")
    def insert_time(self) -> str:
        """
        Creation timestamp in RFC3339 text format.
        """
        return pulumi.get(self, "insert_time")

    @property
    @pulumi.getter
    def labels(self) -> Sequence['outputs.DeploymentLabelEntryResponse']:
        """
        Map of One Platform labels; provided by the client when the resource is created or updated. Specifically: Label keys must be between 1 and 63 characters long and must conform to the following regular expression: `[a-z]([-a-z0-9]*[a-z0-9])?` Label values must be between 0 and 63 characters long and must conform to the regular expression `([a-z]([-a-z0-9]*[a-z0-9])?)?`.
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter
    def manifest(self) -> str:
        """
        URL of the manifest representing the last manifest that was successfully deployed. If no manifest has been successfully deployed, this field will be absent.
        """
        return pulumi.get(self, "manifest")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the resource; provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression `[a-z]([-a-z0-9]*[a-z0-9])?` which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def operation(self) -> 'outputs.OperationResponse':
        """
        The Operation that most recently ran, or is currently running, on this deployment.
        """
        return pulumi.get(self, "operation")

    @property
    @pulumi.getter(name="selfLink")
    def self_link(self) -> str:
        """
        Server defined URL for the resource.
        """
        return pulumi.get(self, "self_link")

    @property
    @pulumi.getter
    def target(self) -> 'outputs.TargetConfigurationResponse':
        """
        [Input Only] The parameters that define your deployment, including the deployment configuration and relevant templates.
        """
        return pulumi.get(self, "target")

    @property
    @pulumi.getter
    def update(self) -> 'outputs.DeploymentUpdateResponse':
        """
        If Deployment Manager is currently updating or previewing an update to this deployment, the updated configuration appears here.
        """
        return pulumi.get(self, "update")

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> str:
        """
        Update timestamp in RFC3339 text format.
        """
        return pulumi.get(self, "update_time")


class AwaitableGetDeploymentResult(GetDeploymentResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDeploymentResult(
            description=self.description,
            fingerprint=self.fingerprint,
            insert_time=self.insert_time,
            labels=self.labels,
            manifest=self.manifest,
            name=self.name,
            operation=self.operation,
            self_link=self.self_link,
            target=self.target,
            update=self.update,
            update_time=self.update_time)


def get_deployment(deployment: Optional[str] = None,
                   project: Optional[str] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDeploymentResult:
    """
    Gets information about a specific deployment.
    """
    __args__ = dict()
    __args__['deployment'] = deployment
    __args__['project'] = project
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('google-native:deploymentmanager/v2:getDeployment', __args__, opts=opts, typ=GetDeploymentResult).value

    return AwaitableGetDeploymentResult(
        description=__ret__.description,
        fingerprint=__ret__.fingerprint,
        insert_time=__ret__.insert_time,
        labels=__ret__.labels,
        manifest=__ret__.manifest,
        name=__ret__.name,
        operation=__ret__.operation,
        self_link=__ret__.self_link,
        target=__ret__.target,
        update=__ret__.update,
        update_time=__ret__.update_time)


@_utilities.lift_output_func(get_deployment)
def get_deployment_output(deployment: Optional[pulumi.Input[str]] = None,
                          project: Optional[pulumi.Input[Optional[str]]] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDeploymentResult]:
    """
    Gets information about a specific deployment.
    """
    ...
