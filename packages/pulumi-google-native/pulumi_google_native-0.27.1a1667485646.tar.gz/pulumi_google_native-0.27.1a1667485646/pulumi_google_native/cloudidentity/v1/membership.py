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
from ._inputs import *

__all__ = ['MembershipArgs', 'Membership']

@pulumi.input_type
class MembershipArgs:
    def __init__(__self__, *,
                 group_id: pulumi.Input[str],
                 preferred_member_key: pulumi.Input['EntityKeyArgs'],
                 roles: Optional[pulumi.Input[Sequence[pulumi.Input['MembershipRoleArgs']]]] = None):
        """
        The set of arguments for constructing a Membership resource.
        :param pulumi.Input['EntityKeyArgs'] preferred_member_key: Immutable. The `EntityKey` of the member.
        :param pulumi.Input[Sequence[pulumi.Input['MembershipRoleArgs']]] roles: The `MembershipRole`s that apply to the `Membership`. If unspecified, defaults to a single `MembershipRole` with `name` `MEMBER`. Must not contain duplicate `MembershipRole`s with the same `name`.
        """
        pulumi.set(__self__, "group_id", group_id)
        pulumi.set(__self__, "preferred_member_key", preferred_member_key)
        if roles is not None:
            pulumi.set(__self__, "roles", roles)

    @property
    @pulumi.getter(name="groupId")
    def group_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "group_id")

    @group_id.setter
    def group_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "group_id", value)

    @property
    @pulumi.getter(name="preferredMemberKey")
    def preferred_member_key(self) -> pulumi.Input['EntityKeyArgs']:
        """
        Immutable. The `EntityKey` of the member.
        """
        return pulumi.get(self, "preferred_member_key")

    @preferred_member_key.setter
    def preferred_member_key(self, value: pulumi.Input['EntityKeyArgs']):
        pulumi.set(self, "preferred_member_key", value)

    @property
    @pulumi.getter
    def roles(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['MembershipRoleArgs']]]]:
        """
        The `MembershipRole`s that apply to the `Membership`. If unspecified, defaults to a single `MembershipRole` with `name` `MEMBER`. Must not contain duplicate `MembershipRole`s with the same `name`.
        """
        return pulumi.get(self, "roles")

    @roles.setter
    def roles(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['MembershipRoleArgs']]]]):
        pulumi.set(self, "roles", value)


class Membership(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 group_id: Optional[pulumi.Input[str]] = None,
                 preferred_member_key: Optional[pulumi.Input[pulumi.InputType['EntityKeyArgs']]] = None,
                 roles: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['MembershipRoleArgs']]]]] = None,
                 __props__=None):
        """
        Creates a `Membership`.
        Auto-naming is currently not supported for this resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['EntityKeyArgs']] preferred_member_key: Immutable. The `EntityKey` of the member.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['MembershipRoleArgs']]]] roles: The `MembershipRole`s that apply to the `Membership`. If unspecified, defaults to a single `MembershipRole` with `name` `MEMBER`. Must not contain duplicate `MembershipRole`s with the same `name`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: MembershipArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Creates a `Membership`.
        Auto-naming is currently not supported for this resource.

        :param str resource_name: The name of the resource.
        :param MembershipArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(MembershipArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 group_id: Optional[pulumi.Input[str]] = None,
                 preferred_member_key: Optional[pulumi.Input[pulumi.InputType['EntityKeyArgs']]] = None,
                 roles: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['MembershipRoleArgs']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = MembershipArgs.__new__(MembershipArgs)

            if group_id is None and not opts.urn:
                raise TypeError("Missing required property 'group_id'")
            __props__.__dict__["group_id"] = group_id
            if preferred_member_key is None and not opts.urn:
                raise TypeError("Missing required property 'preferred_member_key'")
            __props__.__dict__["preferred_member_key"] = preferred_member_key
            __props__.__dict__["roles"] = roles
            __props__.__dict__["create_time"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
            __props__.__dict__["update_time"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["group_id"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Membership, __self__).__init__(
            'google-native:cloudidentity/v1:Membership',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Membership':
        """
        Get an existing Membership resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = MembershipArgs.__new__(MembershipArgs)

        __props__.__dict__["create_time"] = None
        __props__.__dict__["group_id"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["preferred_member_key"] = None
        __props__.__dict__["roles"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["update_time"] = None
        return Membership(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> pulumi.Output[str]:
        """
        The time when the `Membership` was created.
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter(name="groupId")
    def group_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "group_id")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The [resource name](https://cloud.google.com/apis/design/resource_names) of the `Membership`. Shall be of the form `groups/{group}/memberships/{membership}`.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="preferredMemberKey")
    def preferred_member_key(self) -> pulumi.Output['outputs.EntityKeyResponse']:
        """
        Immutable. The `EntityKey` of the member.
        """
        return pulumi.get(self, "preferred_member_key")

    @property
    @pulumi.getter
    def roles(self) -> pulumi.Output[Sequence['outputs.MembershipRoleResponse']]:
        """
        The `MembershipRole`s that apply to the `Membership`. If unspecified, defaults to a single `MembershipRole` with `name` `MEMBER`. Must not contain duplicate `MembershipRole`s with the same `name`.
        """
        return pulumi.get(self, "roles")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the membership.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> pulumi.Output[str]:
        """
        The time when the `Membership` was last updated.
        """
        return pulumi.get(self, "update_time")

