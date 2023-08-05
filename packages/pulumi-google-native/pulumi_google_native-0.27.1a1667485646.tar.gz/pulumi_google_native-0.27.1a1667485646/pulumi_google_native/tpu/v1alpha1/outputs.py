# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from ._enums import *

__all__ = [
    'NetworkEndpointResponse',
    'SchedulingConfigResponse',
    'SymptomResponse',
]

@pulumi.output_type
class NetworkEndpointResponse(dict):
    """
    A network endpoint over which a TPU worker can be reached.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "ipAddress":
            suggest = "ip_address"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in NetworkEndpointResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        NetworkEndpointResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        NetworkEndpointResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 ip_address: str,
                 port: int):
        """
        A network endpoint over which a TPU worker can be reached.
        :param str ip_address: The IP address of this network endpoint.
        :param int port: The port of this network endpoint.
        """
        pulumi.set(__self__, "ip_address", ip_address)
        pulumi.set(__self__, "port", port)

    @property
    @pulumi.getter(name="ipAddress")
    def ip_address(self) -> str:
        """
        The IP address of this network endpoint.
        """
        return pulumi.get(self, "ip_address")

    @property
    @pulumi.getter
    def port(self) -> int:
        """
        The port of this network endpoint.
        """
        return pulumi.get(self, "port")


@pulumi.output_type
class SchedulingConfigResponse(dict):
    """
    Sets the scheduling options for this node.
    """
    def __init__(__self__, *,
                 preemptible: bool,
                 reserved: bool):
        """
        Sets the scheduling options for this node.
        :param bool preemptible: Defines whether the node is preemptible.
        :param bool reserved: Whether the node is created under a reservation.
        """
        pulumi.set(__self__, "preemptible", preemptible)
        pulumi.set(__self__, "reserved", reserved)

    @property
    @pulumi.getter
    def preemptible(self) -> bool:
        """
        Defines whether the node is preemptible.
        """
        return pulumi.get(self, "preemptible")

    @property
    @pulumi.getter
    def reserved(self) -> bool:
        """
        Whether the node is created under a reservation.
        """
        return pulumi.get(self, "reserved")


@pulumi.output_type
class SymptomResponse(dict):
    """
    A Symptom instance.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "createTime":
            suggest = "create_time"
        elif key == "symptomType":
            suggest = "symptom_type"
        elif key == "workerId":
            suggest = "worker_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SymptomResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SymptomResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        SymptomResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 create_time: str,
                 details: str,
                 symptom_type: str,
                 worker_id: str):
        """
        A Symptom instance.
        :param str create_time: Timestamp when the Symptom is created.
        :param str details: Detailed information of the current Symptom.
        :param str symptom_type: Type of the Symptom.
        :param str worker_id: A string used to uniquely distinguish a worker within a TPU node.
        """
        pulumi.set(__self__, "create_time", create_time)
        pulumi.set(__self__, "details", details)
        pulumi.set(__self__, "symptom_type", symptom_type)
        pulumi.set(__self__, "worker_id", worker_id)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> str:
        """
        Timestamp when the Symptom is created.
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter
    def details(self) -> str:
        """
        Detailed information of the current Symptom.
        """
        return pulumi.get(self, "details")

    @property
    @pulumi.getter(name="symptomType")
    def symptom_type(self) -> str:
        """
        Type of the Symptom.
        """
        return pulumi.get(self, "symptom_type")

    @property
    @pulumi.getter(name="workerId")
    def worker_id(self) -> str:
        """
        A string used to uniquely distinguish a worker within a TPU node.
        """
        return pulumi.get(self, "worker_id")


