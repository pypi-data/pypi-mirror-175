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

__all__ = ['TaxonomyArgs', 'Taxonomy']

@pulumi.input_type
class TaxonomyArgs:
    def __init__(__self__, *,
                 display_name: pulumi.Input[str],
                 activated_policy_types: Optional[pulumi.Input[Sequence[pulumi.Input['TaxonomyActivatedPolicyTypesItem']]]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Taxonomy resource.
        :param pulumi.Input[str] display_name: User-defined name of this taxonomy. The name can't start or end with spaces, must contain only Unicode letters, numbers, underscores, dashes, and spaces, and be at most 200 bytes long when encoded in UTF-8. The taxonomy display name must be unique within an organization.
        :param pulumi.Input[Sequence[pulumi.Input['TaxonomyActivatedPolicyTypesItem']]] activated_policy_types: Optional. A list of policy types that are activated for this taxonomy. If not set, defaults to an empty list.
        :param pulumi.Input[str] description: Optional. Description of this taxonomy. If not set, defaults to empty. The description must contain only Unicode characters, tabs, newlines, carriage returns, and page breaks, and be at most 2000 bytes long when encoded in UTF-8.
        """
        pulumi.set(__self__, "display_name", display_name)
        if activated_policy_types is not None:
            pulumi.set(__self__, "activated_policy_types", activated_policy_types)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if project is not None:
            pulumi.set(__self__, "project", project)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Input[str]:
        """
        User-defined name of this taxonomy. The name can't start or end with spaces, must contain only Unicode letters, numbers, underscores, dashes, and spaces, and be at most 200 bytes long when encoded in UTF-8. The taxonomy display name must be unique within an organization.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter(name="activatedPolicyTypes")
    def activated_policy_types(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['TaxonomyActivatedPolicyTypesItem']]]]:
        """
        Optional. A list of policy types that are activated for this taxonomy. If not set, defaults to an empty list.
        """
        return pulumi.get(self, "activated_policy_types")

    @activated_policy_types.setter
    def activated_policy_types(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['TaxonomyActivatedPolicyTypesItem']]]]):
        pulumi.set(self, "activated_policy_types", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. Description of this taxonomy. If not set, defaults to empty. The description must contain only Unicode characters, tabs, newlines, carriage returns, and page breaks, and be at most 2000 bytes long when encoded in UTF-8.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)


class Taxonomy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 activated_policy_types: Optional[pulumi.Input[Sequence[pulumi.Input['TaxonomyActivatedPolicyTypesItem']]]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Creates a taxonomy in a specified project. The taxonomy is initially empty, that is, it doesn't contain policy tags.
        Auto-naming is currently not supported for this resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input['TaxonomyActivatedPolicyTypesItem']]] activated_policy_types: Optional. A list of policy types that are activated for this taxonomy. If not set, defaults to an empty list.
        :param pulumi.Input[str] description: Optional. Description of this taxonomy. If not set, defaults to empty. The description must contain only Unicode characters, tabs, newlines, carriage returns, and page breaks, and be at most 2000 bytes long when encoded in UTF-8.
        :param pulumi.Input[str] display_name: User-defined name of this taxonomy. The name can't start or end with spaces, must contain only Unicode letters, numbers, underscores, dashes, and spaces, and be at most 200 bytes long when encoded in UTF-8. The taxonomy display name must be unique within an organization.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: TaxonomyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Creates a taxonomy in a specified project. The taxonomy is initially empty, that is, it doesn't contain policy tags.
        Auto-naming is currently not supported for this resource.

        :param str resource_name: The name of the resource.
        :param TaxonomyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(TaxonomyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 activated_policy_types: Optional[pulumi.Input[Sequence[pulumi.Input['TaxonomyActivatedPolicyTypesItem']]]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = TaxonomyArgs.__new__(TaxonomyArgs)

            __props__.__dict__["activated_policy_types"] = activated_policy_types
            __props__.__dict__["description"] = description
            if display_name is None and not opts.urn:
                raise TypeError("Missing required property 'display_name'")
            __props__.__dict__["display_name"] = display_name
            __props__.__dict__["location"] = location
            __props__.__dict__["project"] = project
            __props__.__dict__["name"] = None
            __props__.__dict__["policy_tag_count"] = None
            __props__.__dict__["taxonomy_timestamps"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["location", "project"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Taxonomy, __self__).__init__(
            'google-native:datacatalog/v1:Taxonomy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Taxonomy':
        """
        Get an existing Taxonomy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = TaxonomyArgs.__new__(TaxonomyArgs)

        __props__.__dict__["activated_policy_types"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["display_name"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["policy_tag_count"] = None
        __props__.__dict__["project"] = None
        __props__.__dict__["taxonomy_timestamps"] = None
        return Taxonomy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="activatedPolicyTypes")
    def activated_policy_types(self) -> pulumi.Output[Sequence[str]]:
        """
        Optional. A list of policy types that are activated for this taxonomy. If not set, defaults to an empty list.
        """
        return pulumi.get(self, "activated_policy_types")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[str]:
        """
        Optional. Description of this taxonomy. If not set, defaults to empty. The description must contain only Unicode characters, tabs, newlines, carriage returns, and page breaks, and be at most 2000 bytes long when encoded in UTF-8.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[str]:
        """
        User-defined name of this taxonomy. The name can't start or end with spaces, must contain only Unicode letters, numbers, underscores, dashes, and spaces, and be at most 200 bytes long when encoded in UTF-8. The taxonomy display name must be unique within an organization.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name of this taxonomy in URL format. Note: Policy tag manager generates unique taxonomy IDs.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="policyTagCount")
    def policy_tag_count(self) -> pulumi.Output[int]:
        """
        Number of policy tags in this taxonomy.
        """
        return pulumi.get(self, "policy_tag_count")

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        return pulumi.get(self, "project")

    @property
    @pulumi.getter(name="taxonomyTimestamps")
    def taxonomy_timestamps(self) -> pulumi.Output['outputs.GoogleCloudDatacatalogV1SystemTimestampsResponse']:
        """
        Creation and modification timestamps of this taxonomy.
        """
        return pulumi.get(self, "taxonomy_timestamps")

