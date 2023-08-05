# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = ['ReferenceArgs', 'Reference']

@pulumi.input_type
class ReferenceArgs:
    def __init__(__self__, *,
                 environment_id: pulumi.Input[str],
                 organization_id: pulumi.Input[str],
                 refers: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_type: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Reference resource.
        :param pulumi.Input[str] refers: The id of the resource to which this reference refers. Must be the id of a resource that exists in the parent environment and is of the given resource_type.
        :param pulumi.Input[str] description: Optional. A human-readable description of this reference.
        :param pulumi.Input[str] name: The resource id of this reference. Values must match the regular expression [\\w\\s\\-.]+.
        :param pulumi.Input[str] resource_type: The type of resource referred to by this reference. Valid values are 'KeyStore' or 'TrustStore'.
        """
        pulumi.set(__self__, "environment_id", environment_id)
        pulumi.set(__self__, "organization_id", organization_id)
        pulumi.set(__self__, "refers", refers)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if resource_type is not None:
            pulumi.set(__self__, "resource_type", resource_type)

    @property
    @pulumi.getter(name="environmentId")
    def environment_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "environment_id")

    @environment_id.setter
    def environment_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "environment_id", value)

    @property
    @pulumi.getter(name="organizationId")
    def organization_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "organization_id")

    @organization_id.setter
    def organization_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "organization_id", value)

    @property
    @pulumi.getter
    def refers(self) -> pulumi.Input[str]:
        """
        The id of the resource to which this reference refers. Must be the id of a resource that exists in the parent environment and is of the given resource_type.
        """
        return pulumi.get(self, "refers")

    @refers.setter
    def refers(self, value: pulumi.Input[str]):
        pulumi.set(self, "refers", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. A human-readable description of this reference.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The resource id of this reference. Values must match the regular expression [\\w\\s\\-.]+.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="resourceType")
    def resource_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of resource referred to by this reference. Valid values are 'KeyStore' or 'TrustStore'.
        """
        return pulumi.get(self, "resource_type")

    @resource_type.setter
    def resource_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_type", value)


class Reference(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 environment_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 organization_id: Optional[pulumi.Input[str]] = None,
                 refers: Optional[pulumi.Input[str]] = None,
                 resource_type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Creates a Reference in the specified environment.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: Optional. A human-readable description of this reference.
        :param pulumi.Input[str] name: The resource id of this reference. Values must match the regular expression [\\w\\s\\-.]+.
        :param pulumi.Input[str] refers: The id of the resource to which this reference refers. Must be the id of a resource that exists in the parent environment and is of the given resource_type.
        :param pulumi.Input[str] resource_type: The type of resource referred to by this reference. Valid values are 'KeyStore' or 'TrustStore'.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ReferenceArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Creates a Reference in the specified environment.

        :param str resource_name: The name of the resource.
        :param ReferenceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ReferenceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 environment_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 organization_id: Optional[pulumi.Input[str]] = None,
                 refers: Optional[pulumi.Input[str]] = None,
                 resource_type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ReferenceArgs.__new__(ReferenceArgs)

            __props__.__dict__["description"] = description
            if environment_id is None and not opts.urn:
                raise TypeError("Missing required property 'environment_id'")
            __props__.__dict__["environment_id"] = environment_id
            __props__.__dict__["name"] = name
            if organization_id is None and not opts.urn:
                raise TypeError("Missing required property 'organization_id'")
            __props__.__dict__["organization_id"] = organization_id
            if refers is None and not opts.urn:
                raise TypeError("Missing required property 'refers'")
            __props__.__dict__["refers"] = refers
            __props__.__dict__["resource_type"] = resource_type
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["environment_id", "organization_id"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Reference, __self__).__init__(
            'google-native:apigee/v1:Reference',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Reference':
        """
        Get an existing Reference resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ReferenceArgs.__new__(ReferenceArgs)

        __props__.__dict__["description"] = None
        __props__.__dict__["environment_id"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["organization_id"] = None
        __props__.__dict__["refers"] = None
        __props__.__dict__["resource_type"] = None
        return Reference(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[str]:
        """
        Optional. A human-readable description of this reference.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="environmentId")
    def environment_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "environment_id")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The resource id of this reference. Values must match the regular expression [\\w\\s\\-.]+.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="organizationId")
    def organization_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "organization_id")

    @property
    @pulumi.getter
    def refers(self) -> pulumi.Output[str]:
        """
        The id of the resource to which this reference refers. Must be the id of a resource that exists in the parent environment and is of the given resource_type.
        """
        return pulumi.get(self, "refers")

    @property
    @pulumi.getter(name="resourceType")
    def resource_type(self) -> pulumi.Output[str]:
        """
        The type of resource referred to by this reference. Valid values are 'KeyStore' or 'TrustStore'.
        """
        return pulumi.get(self, "resource_type")

