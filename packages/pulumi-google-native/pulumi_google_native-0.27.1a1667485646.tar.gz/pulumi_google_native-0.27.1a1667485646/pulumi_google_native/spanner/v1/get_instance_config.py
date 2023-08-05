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
    'GetInstanceConfigResult',
    'AwaitableGetInstanceConfigResult',
    'get_instance_config',
    'get_instance_config_output',
]

@pulumi.output_type
class GetInstanceConfigResult:
    def __init__(__self__, base_config=None, config_type=None, display_name=None, etag=None, free_instance_availability=None, labels=None, leader_options=None, name=None, optional_replicas=None, reconciling=None, replicas=None, state=None):
        if base_config and not isinstance(base_config, str):
            raise TypeError("Expected argument 'base_config' to be a str")
        pulumi.set(__self__, "base_config", base_config)
        if config_type and not isinstance(config_type, str):
            raise TypeError("Expected argument 'config_type' to be a str")
        pulumi.set(__self__, "config_type", config_type)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if free_instance_availability and not isinstance(free_instance_availability, str):
            raise TypeError("Expected argument 'free_instance_availability' to be a str")
        pulumi.set(__self__, "free_instance_availability", free_instance_availability)
        if labels and not isinstance(labels, dict):
            raise TypeError("Expected argument 'labels' to be a dict")
        pulumi.set(__self__, "labels", labels)
        if leader_options and not isinstance(leader_options, list):
            raise TypeError("Expected argument 'leader_options' to be a list")
        pulumi.set(__self__, "leader_options", leader_options)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if optional_replicas and not isinstance(optional_replicas, list):
            raise TypeError("Expected argument 'optional_replicas' to be a list")
        pulumi.set(__self__, "optional_replicas", optional_replicas)
        if reconciling and not isinstance(reconciling, bool):
            raise TypeError("Expected argument 'reconciling' to be a bool")
        pulumi.set(__self__, "reconciling", reconciling)
        if replicas and not isinstance(replicas, list):
            raise TypeError("Expected argument 'replicas' to be a list")
        pulumi.set(__self__, "replicas", replicas)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)

    @property
    @pulumi.getter(name="baseConfig")
    def base_config(self) -> str:
        """
        Base configuration name, e.g. projects//instanceConfigs/nam3, based on which this configuration is created. Only set for user managed configurations. `base_config` must refer to a configuration of type GOOGLE_MANAGED in the same project as this configuration.
        """
        return pulumi.get(self, "base_config")

    @property
    @pulumi.getter(name="configType")
    def config_type(self) -> str:
        """
        Whether this instance config is a Google or User Managed Configuration.
        """
        return pulumi.get(self, "config_type")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> str:
        """
        The name of this instance configuration as it appears in UIs.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def etag(self) -> str:
        """
        etag is used for optimistic concurrency control as a way to help prevent simultaneous updates of a instance config from overwriting each other. It is strongly suggested that systems make use of the etag in the read-modify-write cycle to perform instance config updates in order to avoid race conditions: An etag is returned in the response which contains instance configs, and systems are expected to put that etag in the request to update instance config to ensure that their change will be applied to the same version of the instance config. If no etag is provided in the call to update instance config, then the existing instance config is overwritten blindly.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="freeInstanceAvailability")
    def free_instance_availability(self) -> str:
        """
        Describes whether free instances are available to be created in this instance config.
        """
        return pulumi.get(self, "free_instance_availability")

    @property
    @pulumi.getter
    def labels(self) -> Mapping[str, str]:
        """
        Cloud Labels are a flexible and lightweight mechanism for organizing cloud resources into groups that reflect a customer's organizational needs and deployment strategies. Cloud Labels can be used to filter collections of resources. They can be used to control how resource metrics are aggregated. And they can be used as arguments to policy management rules (e.g. route, firewall, load balancing, etc.). * Label keys must be between 1 and 63 characters long and must conform to the following regular expression: `a-z{0,62}`. * Label values must be between 0 and 63 characters long and must conform to the regular expression `[a-z0-9_-]{0,63}`. * No more than 64 labels can be associated with a given resource. See https://goo.gl/xmQnxf for more information on and examples of labels. If you plan to use labels in your own code, please note that additional characters may be allowed in the future. Therefore, you are advised to use an internal label representation, such as JSON, which doesn't rely upon specific characters being disallowed. For example, representing labels as the string: name + "_" + value would prove problematic if we were to allow "_" in a future release.
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter(name="leaderOptions")
    def leader_options(self) -> Sequence[str]:
        """
        Allowed values of the "default_leader" schema option for databases in instances that use this instance configuration.
        """
        return pulumi.get(self, "leader_options")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        A unique identifier for the instance configuration. Values are of the form `projects//instanceConfigs/a-z*`.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="optionalReplicas")
    def optional_replicas(self) -> Sequence['outputs.ReplicaInfoResponse']:
        """
        The available optional replicas to choose from for user managed configurations. Populated for Google managed configurations.
        """
        return pulumi.get(self, "optional_replicas")

    @property
    @pulumi.getter
    def reconciling(self) -> bool:
        """
        If true, the instance config is being created or updated. If false, there are no ongoing operations for the instance config.
        """
        return pulumi.get(self, "reconciling")

    @property
    @pulumi.getter
    def replicas(self) -> Sequence['outputs.ReplicaInfoResponse']:
        """
        The geographic placement of nodes in this instance configuration and their replication properties.
        """
        return pulumi.get(self, "replicas")

    @property
    @pulumi.getter
    def state(self) -> str:
        """
        The current instance config state.
        """
        return pulumi.get(self, "state")


class AwaitableGetInstanceConfigResult(GetInstanceConfigResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetInstanceConfigResult(
            base_config=self.base_config,
            config_type=self.config_type,
            display_name=self.display_name,
            etag=self.etag,
            free_instance_availability=self.free_instance_availability,
            labels=self.labels,
            leader_options=self.leader_options,
            name=self.name,
            optional_replicas=self.optional_replicas,
            reconciling=self.reconciling,
            replicas=self.replicas,
            state=self.state)


def get_instance_config(instance_config_id: Optional[str] = None,
                        project: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetInstanceConfigResult:
    """
    Gets information about a particular instance configuration.
    """
    __args__ = dict()
    __args__['instanceConfigId'] = instance_config_id
    __args__['project'] = project
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('google-native:spanner/v1:getInstanceConfig', __args__, opts=opts, typ=GetInstanceConfigResult).value

    return AwaitableGetInstanceConfigResult(
        base_config=__ret__.base_config,
        config_type=__ret__.config_type,
        display_name=__ret__.display_name,
        etag=__ret__.etag,
        free_instance_availability=__ret__.free_instance_availability,
        labels=__ret__.labels,
        leader_options=__ret__.leader_options,
        name=__ret__.name,
        optional_replicas=__ret__.optional_replicas,
        reconciling=__ret__.reconciling,
        replicas=__ret__.replicas,
        state=__ret__.state)


@_utilities.lift_output_func(get_instance_config)
def get_instance_config_output(instance_config_id: Optional[pulumi.Input[str]] = None,
                               project: Optional[pulumi.Input[Optional[str]]] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetInstanceConfigResult]:
    """
    Gets information about a particular instance configuration.
    """
    ...
