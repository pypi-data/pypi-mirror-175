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
    'GetLakeResult',
    'AwaitableGetLakeResult',
    'get_lake',
    'get_lake_output',
]

@pulumi.output_type
class GetLakeResult:
    def __init__(__self__, asset_status=None, create_time=None, description=None, display_name=None, labels=None, metastore=None, metastore_status=None, name=None, service_account=None, state=None, uid=None, update_time=None):
        if asset_status and not isinstance(asset_status, dict):
            raise TypeError("Expected argument 'asset_status' to be a dict")
        pulumi.set(__self__, "asset_status", asset_status)
        if create_time and not isinstance(create_time, str):
            raise TypeError("Expected argument 'create_time' to be a str")
        pulumi.set(__self__, "create_time", create_time)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if labels and not isinstance(labels, dict):
            raise TypeError("Expected argument 'labels' to be a dict")
        pulumi.set(__self__, "labels", labels)
        if metastore and not isinstance(metastore, dict):
            raise TypeError("Expected argument 'metastore' to be a dict")
        pulumi.set(__self__, "metastore", metastore)
        if metastore_status and not isinstance(metastore_status, dict):
            raise TypeError("Expected argument 'metastore_status' to be a dict")
        pulumi.set(__self__, "metastore_status", metastore_status)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if service_account and not isinstance(service_account, str):
            raise TypeError("Expected argument 'service_account' to be a str")
        pulumi.set(__self__, "service_account", service_account)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if uid and not isinstance(uid, str):
            raise TypeError("Expected argument 'uid' to be a str")
        pulumi.set(__self__, "uid", uid)
        if update_time and not isinstance(update_time, str):
            raise TypeError("Expected argument 'update_time' to be a str")
        pulumi.set(__self__, "update_time", update_time)

    @property
    @pulumi.getter(name="assetStatus")
    def asset_status(self) -> 'outputs.GoogleCloudDataplexV1AssetStatusResponse':
        """
        Aggregated status of the underlying assets of the lake.
        """
        return pulumi.get(self, "asset_status")

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> str:
        """
        The time when the lake was created.
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        Optional. Description of the lake.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> str:
        """
        Optional. User friendly display name.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def labels(self) -> Mapping[str, str]:
        """
        Optional. User-defined labels for the lake.
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter
    def metastore(self) -> 'outputs.GoogleCloudDataplexV1LakeMetastoreResponse':
        """
        Optional. Settings to manage lake and Dataproc Metastore service instance association.
        """
        return pulumi.get(self, "metastore")

    @property
    @pulumi.getter(name="metastoreStatus")
    def metastore_status(self) -> 'outputs.GoogleCloudDataplexV1LakeMetastoreStatusResponse':
        """
        Metastore status of the lake.
        """
        return pulumi.get(self, "metastore_status")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The relative resource name of the lake, of the form: projects/{project_number}/locations/{location_id}/lakes/{lake_id}.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="serviceAccount")
    def service_account(self) -> str:
        """
        Service account associated with this lake. This service account must be authorized to access or operate on resources managed by the lake.
        """
        return pulumi.get(self, "service_account")

    @property
    @pulumi.getter
    def state(self) -> str:
        """
        Current state of the lake.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def uid(self) -> str:
        """
        System generated globally unique ID for the lake. This ID will be different if the lake is deleted and re-created with the same name.
        """
        return pulumi.get(self, "uid")

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> str:
        """
        The time when the lake was last updated.
        """
        return pulumi.get(self, "update_time")


class AwaitableGetLakeResult(GetLakeResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetLakeResult(
            asset_status=self.asset_status,
            create_time=self.create_time,
            description=self.description,
            display_name=self.display_name,
            labels=self.labels,
            metastore=self.metastore,
            metastore_status=self.metastore_status,
            name=self.name,
            service_account=self.service_account,
            state=self.state,
            uid=self.uid,
            update_time=self.update_time)


def get_lake(lake_id: Optional[str] = None,
             location: Optional[str] = None,
             project: Optional[str] = None,
             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetLakeResult:
    """
    Retrieves a lake resource.
    """
    __args__ = dict()
    __args__['lakeId'] = lake_id
    __args__['location'] = location
    __args__['project'] = project
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('google-native:dataplex/v1:getLake', __args__, opts=opts, typ=GetLakeResult).value

    return AwaitableGetLakeResult(
        asset_status=__ret__.asset_status,
        create_time=__ret__.create_time,
        description=__ret__.description,
        display_name=__ret__.display_name,
        labels=__ret__.labels,
        metastore=__ret__.metastore,
        metastore_status=__ret__.metastore_status,
        name=__ret__.name,
        service_account=__ret__.service_account,
        state=__ret__.state,
        uid=__ret__.uid,
        update_time=__ret__.update_time)


@_utilities.lift_output_func(get_lake)
def get_lake_output(lake_id: Optional[pulumi.Input[str]] = None,
                    location: Optional[pulumi.Input[str]] = None,
                    project: Optional[pulumi.Input[Optional[str]]] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetLakeResult]:
    """
    Retrieves a lake resource.
    """
    ...
