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
    'PushConfigArgs',
]

@pulumi.input_type
class PushConfigArgs:
    def __init__(__self__, *,
                 push_endpoint: Optional[pulumi.Input[str]] = None):
        """
        Configuration for a push delivery endpoint.
        :param pulumi.Input[str] push_endpoint: A URL locating the endpoint to which messages should be pushed. For example, a Webhook endpoint might use "https://example.com/push".
        """
        if push_endpoint is not None:
            pulumi.set(__self__, "push_endpoint", push_endpoint)

    @property
    @pulumi.getter(name="pushEndpoint")
    def push_endpoint(self) -> Optional[pulumi.Input[str]]:
        """
        A URL locating the endpoint to which messages should be pushed. For example, a Webhook endpoint might use "https://example.com/push".
        """
        return pulumi.get(self, "push_endpoint")

    @push_endpoint.setter
    def push_endpoint(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "push_endpoint", value)


