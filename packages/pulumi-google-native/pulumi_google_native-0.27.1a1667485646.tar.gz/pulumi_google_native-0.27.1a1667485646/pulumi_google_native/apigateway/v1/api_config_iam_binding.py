# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from ... import iam as _iam

__all__ = ['ApiConfigIamBindingArgs', 'ApiConfigIamBinding']

@pulumi.input_type
class ApiConfigIamBindingArgs:
    def __init__(__self__, *,
                 members: pulumi.Input[Sequence[pulumi.Input[str]]],
                 name: pulumi.Input[str],
                 role: pulumi.Input[str],
                 condition: Optional[pulumi.Input['_iam.v1.ConditionArgs']] = None):
        """
        The set of arguments for constructing a ApiConfigIamBinding resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] members: Identities that will be granted the privilege in role. Each entry can have one of the following values:
               
                * user:{emailid}: An email address that represents a specific Google account. For example, alice@gmail.com or joe@example.com.
                * serviceAccount:{emailid}: An email address that represents a service account. For example, my-other-app@appspot.gserviceaccount.com.
                * group:{emailid}: An email address that represents a Google group. For example, admins@example.com.
                * domain:{domain}: A G Suite domain (primary, instead of alias) name that represents all the users of that domain. For example, google.com or example.com.
        :param pulumi.Input[str] name: The name of the resource to manage IAM policies for.
        :param pulumi.Input[str] role: The role that should be applied. Only one `IamBinding` can be used per role.
        :param pulumi.Input['_iam.v1.ConditionArgs'] condition: An IAM Condition for a given binding.
        """
        pulumi.set(__self__, "members", members)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "role", role)
        if condition is not None:
            pulumi.set(__self__, "condition", condition)

    @property
    @pulumi.getter
    def members(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        Identities that will be granted the privilege in role. Each entry can have one of the following values:

         * user:{emailid}: An email address that represents a specific Google account. For example, alice@gmail.com or joe@example.com.
         * serviceAccount:{emailid}: An email address that represents a service account. For example, my-other-app@appspot.gserviceaccount.com.
         * group:{emailid}: An email address that represents a Google group. For example, admins@example.com.
         * domain:{domain}: A G Suite domain (primary, instead of alias) name that represents all the users of that domain. For example, google.com or example.com.
        """
        return pulumi.get(self, "members")

    @members.setter
    def members(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "members", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of the resource to manage IAM policies for.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def role(self) -> pulumi.Input[str]:
        """
        The role that should be applied. Only one `IamBinding` can be used per role.
        """
        return pulumi.get(self, "role")

    @role.setter
    def role(self, value: pulumi.Input[str]):
        pulumi.set(self, "role", value)

    @property
    @pulumi.getter
    def condition(self) -> Optional[pulumi.Input['_iam.v1.ConditionArgs']]:
        """
        An IAM Condition for a given binding.
        """
        return pulumi.get(self, "condition")

    @condition.setter
    def condition(self, value: Optional[pulumi.Input['_iam.v1.ConditionArgs']]):
        pulumi.set(self, "condition", value)


class ApiConfigIamBinding(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 condition: Optional[pulumi.Input[pulumi.InputType['_iam.v1.ConditionArgs']]] = None,
                 members: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 role: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Sets the access control policy on the specified resource. Replaces any existing policy. Can return `NOT_FOUND`, `INVALID_ARGUMENT`, and `PERMISSION_DENIED` errors.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['_iam.v1.ConditionArgs']] condition: An IAM Condition for a given binding.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] members: Identities that will be granted the privilege in role. Each entry can have one of the following values:
               
                * user:{emailid}: An email address that represents a specific Google account. For example, alice@gmail.com or joe@example.com.
                * serviceAccount:{emailid}: An email address that represents a service account. For example, my-other-app@appspot.gserviceaccount.com.
                * group:{emailid}: An email address that represents a Google group. For example, admins@example.com.
                * domain:{domain}: A G Suite domain (primary, instead of alias) name that represents all the users of that domain. For example, google.com or example.com.
        :param pulumi.Input[str] name: The name of the resource to manage IAM policies for.
        :param pulumi.Input[str] role: The role that should be applied. Only one `IamBinding` can be used per role.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ApiConfigIamBindingArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Sets the access control policy on the specified resource. Replaces any existing policy. Can return `NOT_FOUND`, `INVALID_ARGUMENT`, and `PERMISSION_DENIED` errors.

        :param str resource_name: The name of the resource.
        :param ApiConfigIamBindingArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ApiConfigIamBindingArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 condition: Optional[pulumi.Input[pulumi.InputType['_iam.v1.ConditionArgs']]] = None,
                 members: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 role: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ApiConfigIamBindingArgs.__new__(ApiConfigIamBindingArgs)

            __props__.__dict__["condition"] = condition
            if members is None and not opts.urn:
                raise TypeError("Missing required property 'members'")
            __props__.__dict__["members"] = members
            if name is None and not opts.urn:
                raise TypeError("Missing required property 'name'")
            __props__.__dict__["name"] = name
            if role is None and not opts.urn:
                raise TypeError("Missing required property 'role'")
            __props__.__dict__["role"] = role
            __props__.__dict__["etag"] = None
            __props__.__dict__["project"] = None
        super(ApiConfigIamBinding, __self__).__init__(
            'google-native:apigateway/v1:ApiConfigIamBinding',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ApiConfigIamBinding':
        """
        Get an existing ApiConfigIamBinding resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ApiConfigIamBindingArgs.__new__(ApiConfigIamBindingArgs)

        __props__.__dict__["condition"] = None
        __props__.__dict__["etag"] = None
        __props__.__dict__["members"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["project"] = None
        __props__.__dict__["role"] = None
        return ApiConfigIamBinding(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def condition(self) -> pulumi.Output[Optional['_iam.v1.outputs.Condition']]:
        """
        An IAM Condition for a given binding. See https://cloud.google.com/iam/docs/conditions-overview for additional details.
        """
        return pulumi.get(self, "condition")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        The etag of the resource's IAM policy.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def members(self) -> pulumi.Output[Sequence[str]]:
        """
        Identities that will be granted the privilege in role. Each entry can have one of the following values:

         * user:{emailid}: An email address that represents a specific Google account. For example, alice@gmail.com or joe@example.com.
         * serviceAccount:{emailid}: An email address that represents a service account. For example, my-other-app@appspot.gserviceaccount.com.
         * group:{emailid}: An email address that represents a Google group. For example, admins@example.com.
         * domain:{domain}: A G Suite domain (primary, instead of alias) name that represents all the users of that domain. For example, google.com or example.com.
        """
        return pulumi.get(self, "members")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource to manage IAM policies for.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        """
        The project in which the resource belongs. If it is not provided, a default will be supplied.
        """
        return pulumi.get(self, "project")

    @property
    @pulumi.getter
    def role(self) -> pulumi.Output[str]:
        """
        The role that should be applied. Only one `IamBinding` can be used per role.
        """
        return pulumi.get(self, "role")

