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
    'GetEndpointResult',
    'AwaitableGetEndpointResult',
    'get_endpoint',
    'get_endpoint_output',
]

@pulumi.output_type
class GetEndpointResult:
    def __init__(__self__, create_time=None, description=None, endpoint_forwarding_rule=None, endpoint_ip=None, labels=None, name=None, network=None, severity=None, state=None, traffic_logs=None, update_time=None):
        if create_time and not isinstance(create_time, str):
            raise TypeError("Expected argument 'create_time' to be a str")
        pulumi.set(__self__, "create_time", create_time)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if endpoint_forwarding_rule and not isinstance(endpoint_forwarding_rule, str):
            raise TypeError("Expected argument 'endpoint_forwarding_rule' to be a str")
        pulumi.set(__self__, "endpoint_forwarding_rule", endpoint_forwarding_rule)
        if endpoint_ip and not isinstance(endpoint_ip, str):
            raise TypeError("Expected argument 'endpoint_ip' to be a str")
        pulumi.set(__self__, "endpoint_ip", endpoint_ip)
        if labels and not isinstance(labels, dict):
            raise TypeError("Expected argument 'labels' to be a dict")
        pulumi.set(__self__, "labels", labels)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if network and not isinstance(network, str):
            raise TypeError("Expected argument 'network' to be a str")
        pulumi.set(__self__, "network", network)
        if severity and not isinstance(severity, str):
            raise TypeError("Expected argument 'severity' to be a str")
        pulumi.set(__self__, "severity", severity)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if traffic_logs and not isinstance(traffic_logs, bool):
            raise TypeError("Expected argument 'traffic_logs' to be a bool")
        pulumi.set(__self__, "traffic_logs", traffic_logs)
        if update_time and not isinstance(update_time, str):
            raise TypeError("Expected argument 'update_time' to be a str")
        pulumi.set(__self__, "update_time", update_time)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> str:
        """
        The create time timestamp.
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        User-provided description of the endpoint
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="endpointForwardingRule")
    def endpoint_forwarding_rule(self) -> str:
        """
        The fully qualified URL of the endpoint's ILB Forwarding Rule.
        """
        return pulumi.get(self, "endpoint_forwarding_rule")

    @property
    @pulumi.getter(name="endpointIp")
    def endpoint_ip(self) -> str:
        """
        The IP address of the IDS Endpoint's ILB.
        """
        return pulumi.get(self, "endpoint_ip")

    @property
    @pulumi.getter
    def labels(self) -> Mapping[str, str]:
        """
        The labels of the endpoint.
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the endpoint.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def network(self) -> str:
        """
        The fully qualified URL of the network to which the IDS Endpoint is attached.
        """
        return pulumi.get(self, "network")

    @property
    @pulumi.getter
    def severity(self) -> str:
        """
        Lowest threat severity that this endpoint will alert on.
        """
        return pulumi.get(self, "severity")

    @property
    @pulumi.getter
    def state(self) -> str:
        """
        Current state of the endpoint.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter(name="trafficLogs")
    def traffic_logs(self) -> bool:
        """
        Whether the endpoint should report traffic logs in addition to threat logs.
        """
        return pulumi.get(self, "traffic_logs")

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> str:
        """
        The update time timestamp.
        """
        return pulumi.get(self, "update_time")


class AwaitableGetEndpointResult(GetEndpointResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetEndpointResult(
            create_time=self.create_time,
            description=self.description,
            endpoint_forwarding_rule=self.endpoint_forwarding_rule,
            endpoint_ip=self.endpoint_ip,
            labels=self.labels,
            name=self.name,
            network=self.network,
            severity=self.severity,
            state=self.state,
            traffic_logs=self.traffic_logs,
            update_time=self.update_time)


def get_endpoint(endpoint_id: Optional[str] = None,
                 location: Optional[str] = None,
                 project: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetEndpointResult:
    """
    Gets details of a single Endpoint.
    """
    __args__ = dict()
    __args__['endpointId'] = endpoint_id
    __args__['location'] = location
    __args__['project'] = project
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('google-native:ids/v1:getEndpoint', __args__, opts=opts, typ=GetEndpointResult).value

    return AwaitableGetEndpointResult(
        create_time=__ret__.create_time,
        description=__ret__.description,
        endpoint_forwarding_rule=__ret__.endpoint_forwarding_rule,
        endpoint_ip=__ret__.endpoint_ip,
        labels=__ret__.labels,
        name=__ret__.name,
        network=__ret__.network,
        severity=__ret__.severity,
        state=__ret__.state,
        traffic_logs=__ret__.traffic_logs,
        update_time=__ret__.update_time)


@_utilities.lift_output_func(get_endpoint)
def get_endpoint_output(endpoint_id: Optional[pulumi.Input[str]] = None,
                        location: Optional[pulumi.Input[str]] = None,
                        project: Optional[pulumi.Input[Optional[str]]] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetEndpointResult]:
    """
    Gets details of a single Endpoint.
    """
    ...
