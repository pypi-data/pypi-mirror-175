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
    'GetBackupResult',
    'AwaitableGetBackupResult',
    'get_backup',
    'get_backup_output',
]

@pulumi.output_type
class GetBackupResult:
    def __init__(__self__, encryption_info=None, end_time=None, expire_time=None, name=None, size_bytes=None, source_backup=None, source_table=None, start_time=None, state=None):
        if encryption_info and not isinstance(encryption_info, dict):
            raise TypeError("Expected argument 'encryption_info' to be a dict")
        pulumi.set(__self__, "encryption_info", encryption_info)
        if end_time and not isinstance(end_time, str):
            raise TypeError("Expected argument 'end_time' to be a str")
        pulumi.set(__self__, "end_time", end_time)
        if expire_time and not isinstance(expire_time, str):
            raise TypeError("Expected argument 'expire_time' to be a str")
        pulumi.set(__self__, "expire_time", expire_time)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if size_bytes and not isinstance(size_bytes, str):
            raise TypeError("Expected argument 'size_bytes' to be a str")
        pulumi.set(__self__, "size_bytes", size_bytes)
        if source_backup and not isinstance(source_backup, str):
            raise TypeError("Expected argument 'source_backup' to be a str")
        pulumi.set(__self__, "source_backup", source_backup)
        if source_table and not isinstance(source_table, str):
            raise TypeError("Expected argument 'source_table' to be a str")
        pulumi.set(__self__, "source_table", source_table)
        if start_time and not isinstance(start_time, str):
            raise TypeError("Expected argument 'start_time' to be a str")
        pulumi.set(__self__, "start_time", start_time)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)

    @property
    @pulumi.getter(name="encryptionInfo")
    def encryption_info(self) -> 'outputs.EncryptionInfoResponse':
        """
        The encryption information for the backup.
        """
        return pulumi.get(self, "encryption_info")

    @property
    @pulumi.getter(name="endTime")
    def end_time(self) -> str:
        """
        `end_time` is the time that the backup was finished. The row data in the backup will be no newer than this timestamp.
        """
        return pulumi.get(self, "end_time")

    @property
    @pulumi.getter(name="expireTime")
    def expire_time(self) -> str:
        """
        The expiration time of the backup, with microseconds granularity that must be at least 6 hours and at most 30 days from the time the request is received. Once the `expire_time` has passed, Cloud Bigtable will delete the backup and free the resources used by the backup.
        """
        return pulumi.get(self, "expire_time")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        A globally unique identifier for the backup which cannot be changed. Values are of the form `projects/{project}/instances/{instance}/clusters/{cluster}/ backups/_a-zA-Z0-9*` The final segment of the name must be between 1 and 50 characters in length. The backup is stored in the cluster identified by the prefix of the backup name of the form `projects/{project}/instances/{instance}/clusters/{cluster}`.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="sizeBytes")
    def size_bytes(self) -> str:
        """
        Size of the backup in bytes.
        """
        return pulumi.get(self, "size_bytes")

    @property
    @pulumi.getter(name="sourceBackup")
    def source_backup(self) -> str:
        """
        Name of the backup from which this backup was copied. If a backup is not created by copying a backup, this field will be empty. Values are of the form: projects//instances//backups/.
        """
        return pulumi.get(self, "source_backup")

    @property
    @pulumi.getter(name="sourceTable")
    def source_table(self) -> str:
        """
        Immutable. Name of the table from which this backup was created. This needs to be in the same instance as the backup. Values are of the form `projects/{project}/instances/{instance}/tables/{source_table}`.
        """
        return pulumi.get(self, "source_table")

    @property
    @pulumi.getter(name="startTime")
    def start_time(self) -> str:
        """
        `start_time` is the time that the backup was started (i.e. approximately the time the CreateBackup request is received). The row data in this backup will be no older than this timestamp.
        """
        return pulumi.get(self, "start_time")

    @property
    @pulumi.getter
    def state(self) -> str:
        """
        The current state of the backup.
        """
        return pulumi.get(self, "state")


class AwaitableGetBackupResult(GetBackupResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetBackupResult(
            encryption_info=self.encryption_info,
            end_time=self.end_time,
            expire_time=self.expire_time,
            name=self.name,
            size_bytes=self.size_bytes,
            source_backup=self.source_backup,
            source_table=self.source_table,
            start_time=self.start_time,
            state=self.state)


def get_backup(backup_id: Optional[str] = None,
               cluster_id: Optional[str] = None,
               instance_id: Optional[str] = None,
               project: Optional[str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetBackupResult:
    """
    Gets metadata on a pending or completed Cloud Bigtable Backup.
    """
    __args__ = dict()
    __args__['backupId'] = backup_id
    __args__['clusterId'] = cluster_id
    __args__['instanceId'] = instance_id
    __args__['project'] = project
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('google-native:bigtableadmin/v2:getBackup', __args__, opts=opts, typ=GetBackupResult).value

    return AwaitableGetBackupResult(
        encryption_info=__ret__.encryption_info,
        end_time=__ret__.end_time,
        expire_time=__ret__.expire_time,
        name=__ret__.name,
        size_bytes=__ret__.size_bytes,
        source_backup=__ret__.source_backup,
        source_table=__ret__.source_table,
        start_time=__ret__.start_time,
        state=__ret__.state)


@_utilities.lift_output_func(get_backup)
def get_backup_output(backup_id: Optional[pulumi.Input[str]] = None,
                      cluster_id: Optional[pulumi.Input[str]] = None,
                      instance_id: Optional[pulumi.Input[str]] = None,
                      project: Optional[pulumi.Input[Optional[str]]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetBackupResult]:
    """
    Gets metadata on a pending or completed Cloud Bigtable Backup.
    """
    ...
