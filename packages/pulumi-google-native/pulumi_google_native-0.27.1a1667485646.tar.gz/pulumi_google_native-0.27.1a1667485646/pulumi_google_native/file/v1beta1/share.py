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
from ._enums import *
from ._inputs import *

__all__ = ['ShareArgs', 'Share']

@pulumi.input_type
class ShareArgs:
    def __init__(__self__, *,
                 instance_id: pulumi.Input[str],
                 share_id: pulumi.Input[str],
                 capacity_gb: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 mount_name: Optional[pulumi.Input[str]] = None,
                 nfs_export_options: Optional[pulumi.Input[Sequence[pulumi.Input['NfsExportOptionsArgs']]]] = None,
                 project: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Share resource.
        :param pulumi.Input[str] share_id: Required. The ID to use for the share. The ID must be unique within the specified instance. This value must start with a lowercase letter followed by up to 62 lowercase letters, numbers, or hyphens, and cannot end with a hyphen.
        :param pulumi.Input[str] capacity_gb: File share capacity in gigabytes (GB). Filestore defines 1 GB as 1024^3 bytes. Must be greater than 0.
        :param pulumi.Input[str] description: A description of the share with 2048 characters or less. Requests with longer descriptions will be rejected.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Resource labels to represent user provided metadata.
        :param pulumi.Input[str] mount_name: The mount name of the share. Must be 63 characters or less and consist of uppercase or lowercase letters, numbers, and underscores.
        :param pulumi.Input[Sequence[pulumi.Input['NfsExportOptionsArgs']]] nfs_export_options: Nfs Export Options. There is a limit of 10 export options per file share.
        """
        pulumi.set(__self__, "instance_id", instance_id)
        pulumi.set(__self__, "share_id", share_id)
        if capacity_gb is not None:
            pulumi.set(__self__, "capacity_gb", capacity_gb)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if labels is not None:
            pulumi.set(__self__, "labels", labels)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if mount_name is not None:
            pulumi.set(__self__, "mount_name", mount_name)
        if nfs_export_options is not None:
            pulumi.set(__self__, "nfs_export_options", nfs_export_options)
        if project is not None:
            pulumi.set(__self__, "project", project)

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "instance_id")

    @instance_id.setter
    def instance_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "instance_id", value)

    @property
    @pulumi.getter(name="shareId")
    def share_id(self) -> pulumi.Input[str]:
        """
        Required. The ID to use for the share. The ID must be unique within the specified instance. This value must start with a lowercase letter followed by up to 62 lowercase letters, numbers, or hyphens, and cannot end with a hyphen.
        """
        return pulumi.get(self, "share_id")

    @share_id.setter
    def share_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "share_id", value)

    @property
    @pulumi.getter(name="capacityGb")
    def capacity_gb(self) -> Optional[pulumi.Input[str]]:
        """
        File share capacity in gigabytes (GB). Filestore defines 1 GB as 1024^3 bytes. Must be greater than 0.
        """
        return pulumi.get(self, "capacity_gb")

    @capacity_gb.setter
    def capacity_gb(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "capacity_gb", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A description of the share with 2048 characters or less. Requests with longer descriptions will be rejected.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def labels(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource labels to represent user provided metadata.
        """
        return pulumi.get(self, "labels")

    @labels.setter
    def labels(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "labels", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="mountName")
    def mount_name(self) -> Optional[pulumi.Input[str]]:
        """
        The mount name of the share. Must be 63 characters or less and consist of uppercase or lowercase letters, numbers, and underscores.
        """
        return pulumi.get(self, "mount_name")

    @mount_name.setter
    def mount_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "mount_name", value)

    @property
    @pulumi.getter(name="nfsExportOptions")
    def nfs_export_options(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['NfsExportOptionsArgs']]]]:
        """
        Nfs Export Options. There is a limit of 10 export options per file share.
        """
        return pulumi.get(self, "nfs_export_options")

    @nfs_export_options.setter
    def nfs_export_options(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['NfsExportOptionsArgs']]]]):
        pulumi.set(self, "nfs_export_options", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)


class Share(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 capacity_gb: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 mount_name: Optional[pulumi.Input[str]] = None,
                 nfs_export_options: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NfsExportOptionsArgs']]]]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 share_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Creates a share.
        Auto-naming is currently not supported for this resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] capacity_gb: File share capacity in gigabytes (GB). Filestore defines 1 GB as 1024^3 bytes. Must be greater than 0.
        :param pulumi.Input[str] description: A description of the share with 2048 characters or less. Requests with longer descriptions will be rejected.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Resource labels to represent user provided metadata.
        :param pulumi.Input[str] mount_name: The mount name of the share. Must be 63 characters or less and consist of uppercase or lowercase letters, numbers, and underscores.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NfsExportOptionsArgs']]]] nfs_export_options: Nfs Export Options. There is a limit of 10 export options per file share.
        :param pulumi.Input[str] share_id: Required. The ID to use for the share. The ID must be unique within the specified instance. This value must start with a lowercase letter followed by up to 62 lowercase letters, numbers, or hyphens, and cannot end with a hyphen.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ShareArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Creates a share.
        Auto-naming is currently not supported for this resource.

        :param str resource_name: The name of the resource.
        :param ShareArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ShareArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 capacity_gb: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 mount_name: Optional[pulumi.Input[str]] = None,
                 nfs_export_options: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NfsExportOptionsArgs']]]]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 share_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ShareArgs.__new__(ShareArgs)

            __props__.__dict__["capacity_gb"] = capacity_gb
            __props__.__dict__["description"] = description
            if instance_id is None and not opts.urn:
                raise TypeError("Missing required property 'instance_id'")
            __props__.__dict__["instance_id"] = instance_id
            __props__.__dict__["labels"] = labels
            __props__.__dict__["location"] = location
            __props__.__dict__["mount_name"] = mount_name
            __props__.__dict__["nfs_export_options"] = nfs_export_options
            __props__.__dict__["project"] = project
            if share_id is None and not opts.urn:
                raise TypeError("Missing required property 'share_id'")
            __props__.__dict__["share_id"] = share_id
            __props__.__dict__["create_time"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["state"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["instance_id", "location", "project", "share_id"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Share, __self__).__init__(
            'google-native:file/v1beta1:Share',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Share':
        """
        Get an existing Share resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ShareArgs.__new__(ShareArgs)

        __props__.__dict__["capacity_gb"] = None
        __props__.__dict__["create_time"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["instance_id"] = None
        __props__.__dict__["labels"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["mount_name"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["nfs_export_options"] = None
        __props__.__dict__["project"] = None
        __props__.__dict__["share_id"] = None
        __props__.__dict__["state"] = None
        return Share(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="capacityGb")
    def capacity_gb(self) -> pulumi.Output[str]:
        """
        File share capacity in gigabytes (GB). Filestore defines 1 GB as 1024^3 bytes. Must be greater than 0.
        """
        return pulumi.get(self, "capacity_gb")

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> pulumi.Output[str]:
        """
        The time when the share was created.
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[str]:
        """
        A description of the share with 2048 characters or less. Requests with longer descriptions will be rejected.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "instance_id")

    @property
    @pulumi.getter
    def labels(self) -> pulumi.Output[Mapping[str, str]]:
        """
        Resource labels to represent user provided metadata.
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="mountName")
    def mount_name(self) -> pulumi.Output[str]:
        """
        The mount name of the share. Must be 63 characters or less and consist of uppercase or lowercase letters, numbers, and underscores.
        """
        return pulumi.get(self, "mount_name")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The resource name of the share, in the format `projects/{project_id}/locations/{location_id}/instances/{instance_id}/shares/{share_id}`.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="nfsExportOptions")
    def nfs_export_options(self) -> pulumi.Output[Sequence['outputs.NfsExportOptionsResponse']]:
        """
        Nfs Export Options. There is a limit of 10 export options per file share.
        """
        return pulumi.get(self, "nfs_export_options")

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        return pulumi.get(self, "project")

    @property
    @pulumi.getter(name="shareId")
    def share_id(self) -> pulumi.Output[str]:
        """
        Required. The ID to use for the share. The ID must be unique within the specified instance. This value must start with a lowercase letter followed by up to 62 lowercase letters, numbers, or hyphens, and cannot end with a hyphen.
        """
        return pulumi.get(self, "share_id")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        The share state.
        """
        return pulumi.get(self, "state")

