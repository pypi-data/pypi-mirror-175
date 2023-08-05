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
    'GetUtilizationReportResult',
    'AwaitableGetUtilizationReportResult',
    'get_utilization_report',
    'get_utilization_report_output',
]

@pulumi.output_type
class GetUtilizationReportResult:
    def __init__(__self__, create_time=None, display_name=None, error=None, frame_end_time=None, name=None, state=None, state_time=None, time_frame=None, vm_count=None, vms=None, vms_count=None):
        if create_time and not isinstance(create_time, str):
            raise TypeError("Expected argument 'create_time' to be a str")
        pulumi.set(__self__, "create_time", create_time)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if error and not isinstance(error, dict):
            raise TypeError("Expected argument 'error' to be a dict")
        pulumi.set(__self__, "error", error)
        if frame_end_time and not isinstance(frame_end_time, str):
            raise TypeError("Expected argument 'frame_end_time' to be a str")
        pulumi.set(__self__, "frame_end_time", frame_end_time)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if state_time and not isinstance(state_time, str):
            raise TypeError("Expected argument 'state_time' to be a str")
        pulumi.set(__self__, "state_time", state_time)
        if time_frame and not isinstance(time_frame, str):
            raise TypeError("Expected argument 'time_frame' to be a str")
        pulumi.set(__self__, "time_frame", time_frame)
        if vm_count and not isinstance(vm_count, int):
            raise TypeError("Expected argument 'vm_count' to be a int")
        pulumi.set(__self__, "vm_count", vm_count)
        if vms and not isinstance(vms, list):
            raise TypeError("Expected argument 'vms' to be a list")
        pulumi.set(__self__, "vms", vms)
        if vms_count and not isinstance(vms_count, int):
            raise TypeError("Expected argument 'vms_count' to be a int")
        pulumi.set(__self__, "vms_count", vms_count)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> str:
        """
        The time the report was created (this refers to the time of the request, not the time the report creation completed).
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> str:
        """
        The report display name, as assigned by the user.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def error(self) -> 'outputs.StatusResponse':
        """
        Provides details on the state of the report in case of an error.
        """
        return pulumi.get(self, "error")

    @property
    @pulumi.getter(name="frameEndTime")
    def frame_end_time(self) -> str:
        """
        The point in time when the time frame ends. Notice that the time frame is counted backwards. For instance if the "frame_end_time" value is 2021/01/20 and the time frame is WEEK then the report covers the week between 2021/01/20 and 2021/01/14.
        """
        return pulumi.get(self, "frame_end_time")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The report unique name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def state(self) -> str:
        """
        Current state of the report.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter(name="stateTime")
    def state_time(self) -> str:
        """
        The time the state was last set.
        """
        return pulumi.get(self, "state_time")

    @property
    @pulumi.getter(name="timeFrame")
    def time_frame(self) -> str:
        """
        Time frame of the report.
        """
        return pulumi.get(self, "time_frame")

    @property
    @pulumi.getter(name="vmCount")
    def vm_count(self) -> int:
        """
        Total number of VMs included in the report.
        """
        return pulumi.get(self, "vm_count")

    @property
    @pulumi.getter
    def vms(self) -> Sequence['outputs.VmUtilizationInfoResponse']:
        """
        List of utilization information per VM. When sent as part of the request, the "vm_id" field is used in order to specify which VMs to include in the report. In that case all other fields are ignored.
        """
        return pulumi.get(self, "vms")

    @property
    @pulumi.getter(name="vmsCount")
    def vms_count(self) -> int:
        """
        Total number of VMs included in the report.
        """
        return pulumi.get(self, "vms_count")


class AwaitableGetUtilizationReportResult(GetUtilizationReportResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetUtilizationReportResult(
            create_time=self.create_time,
            display_name=self.display_name,
            error=self.error,
            frame_end_time=self.frame_end_time,
            name=self.name,
            state=self.state,
            state_time=self.state_time,
            time_frame=self.time_frame,
            vm_count=self.vm_count,
            vms=self.vms,
            vms_count=self.vms_count)


def get_utilization_report(location: Optional[str] = None,
                           project: Optional[str] = None,
                           source_id: Optional[str] = None,
                           utilization_report_id: Optional[str] = None,
                           view: Optional[str] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetUtilizationReportResult:
    """
    Gets a single Utilization Report.
    """
    __args__ = dict()
    __args__['location'] = location
    __args__['project'] = project
    __args__['sourceId'] = source_id
    __args__['utilizationReportId'] = utilization_report_id
    __args__['view'] = view
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('google-native:vmmigration/v1alpha1:getUtilizationReport', __args__, opts=opts, typ=GetUtilizationReportResult).value

    return AwaitableGetUtilizationReportResult(
        create_time=__ret__.create_time,
        display_name=__ret__.display_name,
        error=__ret__.error,
        frame_end_time=__ret__.frame_end_time,
        name=__ret__.name,
        state=__ret__.state,
        state_time=__ret__.state_time,
        time_frame=__ret__.time_frame,
        vm_count=__ret__.vm_count,
        vms=__ret__.vms,
        vms_count=__ret__.vms_count)


@_utilities.lift_output_func(get_utilization_report)
def get_utilization_report_output(location: Optional[pulumi.Input[str]] = None,
                                  project: Optional[pulumi.Input[Optional[str]]] = None,
                                  source_id: Optional[pulumi.Input[str]] = None,
                                  utilization_report_id: Optional[pulumi.Input[str]] = None,
                                  view: Optional[pulumi.Input[Optional[str]]] = None,
                                  opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetUtilizationReportResult]:
    """
    Gets a single Utilization Report.
    """
    ...
