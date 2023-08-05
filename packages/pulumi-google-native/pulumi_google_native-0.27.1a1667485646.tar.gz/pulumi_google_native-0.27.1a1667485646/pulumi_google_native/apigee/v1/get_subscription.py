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
    'GetSubscriptionResult',
    'AwaitableGetSubscriptionResult',
    'get_subscription',
    'get_subscription_output',
]

@pulumi.output_type
class GetSubscriptionResult:
    def __init__(__self__, apiproduct=None, created_at=None, end_time=None, last_modified_at=None, name=None, start_time=None):
        if apiproduct and not isinstance(apiproduct, str):
            raise TypeError("Expected argument 'apiproduct' to be a str")
        pulumi.set(__self__, "apiproduct", apiproduct)
        if created_at and not isinstance(created_at, str):
            raise TypeError("Expected argument 'created_at' to be a str")
        pulumi.set(__self__, "created_at", created_at)
        if end_time and not isinstance(end_time, str):
            raise TypeError("Expected argument 'end_time' to be a str")
        pulumi.set(__self__, "end_time", end_time)
        if last_modified_at and not isinstance(last_modified_at, str):
            raise TypeError("Expected argument 'last_modified_at' to be a str")
        pulumi.set(__self__, "last_modified_at", last_modified_at)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if start_time and not isinstance(start_time, str):
            raise TypeError("Expected argument 'start_time' to be a str")
        pulumi.set(__self__, "start_time", start_time)

    @property
    @pulumi.getter
    def apiproduct(self) -> str:
        """
        Name of the API product for which the developer is purchasing a subscription.
        """
        return pulumi.get(self, "apiproduct")

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> str:
        """
        Time when the API product subscription was created in milliseconds since epoch.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="endTime")
    def end_time(self) -> str:
        """
        Time when the API product subscription ends in milliseconds since epoch.
        """
        return pulumi.get(self, "end_time")

    @property
    @pulumi.getter(name="lastModifiedAt")
    def last_modified_at(self) -> str:
        """
        Time when the API product subscription was last modified in milliseconds since epoch.
        """
        return pulumi.get(self, "last_modified_at")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the API product subscription.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="startTime")
    def start_time(self) -> str:
        """
        Time when the API product subscription starts in milliseconds since epoch.
        """
        return pulumi.get(self, "start_time")


class AwaitableGetSubscriptionResult(GetSubscriptionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSubscriptionResult(
            apiproduct=self.apiproduct,
            created_at=self.created_at,
            end_time=self.end_time,
            last_modified_at=self.last_modified_at,
            name=self.name,
            start_time=self.start_time)


def get_subscription(developer_id: Optional[str] = None,
                     organization_id: Optional[str] = None,
                     subscription_id: Optional[str] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSubscriptionResult:
    """
    Gets details for an API product subscription.
    """
    __args__ = dict()
    __args__['developerId'] = developer_id
    __args__['organizationId'] = organization_id
    __args__['subscriptionId'] = subscription_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('google-native:apigee/v1:getSubscription', __args__, opts=opts, typ=GetSubscriptionResult).value

    return AwaitableGetSubscriptionResult(
        apiproduct=__ret__.apiproduct,
        created_at=__ret__.created_at,
        end_time=__ret__.end_time,
        last_modified_at=__ret__.last_modified_at,
        name=__ret__.name,
        start_time=__ret__.start_time)


@_utilities.lift_output_func(get_subscription)
def get_subscription_output(developer_id: Optional[pulumi.Input[str]] = None,
                            organization_id: Optional[pulumi.Input[str]] = None,
                            subscription_id: Optional[pulumi.Input[str]] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSubscriptionResult]:
    """
    Gets details for an API product subscription.
    """
    ...
