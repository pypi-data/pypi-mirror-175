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
    'GetRestorePlanResult',
    'AwaitableGetRestorePlanResult',
    'get_restore_plan',
    'get_restore_plan_output',
]

@pulumi.output_type
class GetRestorePlanResult:
    def __init__(__self__, backup_plan=None, cluster=None, create_time=None, description=None, etag=None, labels=None, name=None, restore_config=None, uid=None, update_time=None):
        if backup_plan and not isinstance(backup_plan, str):
            raise TypeError("Expected argument 'backup_plan' to be a str")
        pulumi.set(__self__, "backup_plan", backup_plan)
        if cluster and not isinstance(cluster, str):
            raise TypeError("Expected argument 'cluster' to be a str")
        pulumi.set(__self__, "cluster", cluster)
        if create_time and not isinstance(create_time, str):
            raise TypeError("Expected argument 'create_time' to be a str")
        pulumi.set(__self__, "create_time", create_time)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if labels and not isinstance(labels, dict):
            raise TypeError("Expected argument 'labels' to be a dict")
        pulumi.set(__self__, "labels", labels)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if restore_config and not isinstance(restore_config, dict):
            raise TypeError("Expected argument 'restore_config' to be a dict")
        pulumi.set(__self__, "restore_config", restore_config)
        if uid and not isinstance(uid, str):
            raise TypeError("Expected argument 'uid' to be a str")
        pulumi.set(__self__, "uid", uid)
        if update_time and not isinstance(update_time, str):
            raise TypeError("Expected argument 'update_time' to be a str")
        pulumi.set(__self__, "update_time", update_time)

    @property
    @pulumi.getter(name="backupPlan")
    def backup_plan(self) -> str:
        """
        Immutable. A reference to the BackupPlan from which Backups may be used as the source for Restores created via this RestorePlan. Format: `projects/*/locations/*/backupPlans/*`.
        """
        return pulumi.get(self, "backup_plan")

    @property
    @pulumi.getter
    def cluster(self) -> str:
        """
        Immutable. The target cluster into which Restores created via this RestorePlan will restore data. NOTE: the cluster's region must be the same as the RestorePlan. Valid formats: - `projects/*/locations/*/clusters/*` - `projects/*/zones/*/clusters/*`
        """
        return pulumi.get(self, "cluster")

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> str:
        """
        The timestamp when this RestorePlan resource was created.
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        User specified descriptive string for this RestorePlan.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def etag(self) -> str:
        """
        `etag` is used for optimistic concurrency control as a way to help prevent simultaneous updates of a restore from overwriting each other. It is strongly suggested that systems make use of the `etag` in the read-modify-write cycle to perform restore updates in order to avoid race conditions: An `etag` is returned in the response to `GetRestorePlan`, and systems are expected to put that etag in the request to `UpdateRestorePlan` or `DeleteRestorePlan` to ensure that their change will be applied to the same version of the resource.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def labels(self) -> Mapping[str, str]:
        """
        A set of custom labels supplied by user.
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The full name of the RestorePlan resource. Format: `projects/*/locations/*/restorePlans/*`.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="restoreConfig")
    def restore_config(self) -> 'outputs.RestoreConfigResponse':
        """
        Configuration of Restores created via this RestorePlan.
        """
        return pulumi.get(self, "restore_config")

    @property
    @pulumi.getter
    def uid(self) -> str:
        """
        Server generated global unique identifier of [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier) format.
        """
        return pulumi.get(self, "uid")

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> str:
        """
        The timestamp when this RestorePlan resource was last updated.
        """
        return pulumi.get(self, "update_time")


class AwaitableGetRestorePlanResult(GetRestorePlanResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetRestorePlanResult(
            backup_plan=self.backup_plan,
            cluster=self.cluster,
            create_time=self.create_time,
            description=self.description,
            etag=self.etag,
            labels=self.labels,
            name=self.name,
            restore_config=self.restore_config,
            uid=self.uid,
            update_time=self.update_time)


def get_restore_plan(location: Optional[str] = None,
                     project: Optional[str] = None,
                     restore_plan_id: Optional[str] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetRestorePlanResult:
    """
    Retrieve the details of a single RestorePlan.
    """
    __args__ = dict()
    __args__['location'] = location
    __args__['project'] = project
    __args__['restorePlanId'] = restore_plan_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('google-native:gkebackup/v1:getRestorePlan', __args__, opts=opts, typ=GetRestorePlanResult).value

    return AwaitableGetRestorePlanResult(
        backup_plan=__ret__.backup_plan,
        cluster=__ret__.cluster,
        create_time=__ret__.create_time,
        description=__ret__.description,
        etag=__ret__.etag,
        labels=__ret__.labels,
        name=__ret__.name,
        restore_config=__ret__.restore_config,
        uid=__ret__.uid,
        update_time=__ret__.update_time)


@_utilities.lift_output_func(get_restore_plan)
def get_restore_plan_output(location: Optional[pulumi.Input[str]] = None,
                            project: Optional[pulumi.Input[Optional[str]]] = None,
                            restore_plan_id: Optional[pulumi.Input[str]] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetRestorePlanResult]:
    """
    Retrieve the details of a single RestorePlan.
    """
    ...
