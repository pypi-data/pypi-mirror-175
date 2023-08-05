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

__all__ = ['InstanceGroupManagerArgs', 'InstanceGroupManager']

@pulumi.input_type
class InstanceGroupManagerArgs:
    def __init__(__self__, *,
                 auto_healing_policies: Optional[pulumi.Input[Sequence[pulumi.Input['InstanceGroupManagerAutoHealingPolicyArgs']]]] = None,
                 base_instance_name: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 distribution_policy: Optional[pulumi.Input['DistributionPolicyArgs']] = None,
                 instance_template: Optional[pulumi.Input[str]] = None,
                 list_managed_instances_results: Optional[pulumi.Input['InstanceGroupManagerListManagedInstancesResults']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 named_ports: Optional[pulumi.Input[Sequence[pulumi.Input['NamedPortArgs']]]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 request_id: Optional[pulumi.Input[str]] = None,
                 stateful_policy: Optional[pulumi.Input['StatefulPolicyArgs']] = None,
                 target_pools: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 target_size: Optional[pulumi.Input[int]] = None,
                 update_policy: Optional[pulumi.Input['InstanceGroupManagerUpdatePolicyArgs']] = None,
                 versions: Optional[pulumi.Input[Sequence[pulumi.Input['InstanceGroupManagerVersionArgs']]]] = None,
                 zone: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a InstanceGroupManager resource.
        :param pulumi.Input[Sequence[pulumi.Input['InstanceGroupManagerAutoHealingPolicyArgs']]] auto_healing_policies: The autohealing policy for this managed instance group. You can specify only one value.
        :param pulumi.Input[str] base_instance_name: The base instance name to use for instances in this group. The value must be 1-58 characters long. Instances are named by appending a hyphen and a random four-character string to the base instance name. The base instance name must comply with RFC1035.
        :param pulumi.Input[str] description: An optional description of this resource.
        :param pulumi.Input['DistributionPolicyArgs'] distribution_policy: Policy specifying the intended distribution of managed instances across zones in a regional managed instance group.
        :param pulumi.Input[str] instance_template: The URL of the instance template that is specified for this managed instance group. The group uses this template to create all new instances in the managed instance group. The templates for existing instances in the group do not change unless you run recreateInstances, run applyUpdatesToInstances, or set the group's updatePolicy.type to PROACTIVE.
        :param pulumi.Input['InstanceGroupManagerListManagedInstancesResults'] list_managed_instances_results: Pagination behavior of the listManagedInstances API method for this managed instance group.
        :param pulumi.Input[str] name: The name of the managed instance group. The name must be 1-63 characters long, and comply with RFC1035.
        :param pulumi.Input[Sequence[pulumi.Input['NamedPortArgs']]] named_ports: Named ports configured for the Instance Groups complementary to this Instance Group Manager.
        :param pulumi.Input[str] request_id: An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000).
        :param pulumi.Input['StatefulPolicyArgs'] stateful_policy: Stateful configuration for this Instanced Group Manager
        :param pulumi.Input[Sequence[pulumi.Input[str]]] target_pools: The URLs for all TargetPool resources to which instances in the instanceGroup field are added. The target pools automatically apply to all of the instances in the managed instance group.
        :param pulumi.Input[int] target_size: The target number of running instances for this managed instance group. You can reduce this number by using the instanceGroupManager deleteInstances or abandonInstances methods. Resizing the group also changes this number.
        :param pulumi.Input['InstanceGroupManagerUpdatePolicyArgs'] update_policy: The update policy for this managed instance group.
        :param pulumi.Input[Sequence[pulumi.Input['InstanceGroupManagerVersionArgs']]] versions: Specifies the instance templates used by this managed instance group to create instances. Each version is defined by an instanceTemplate and a name. Every version can appear at most once per instance group. This field overrides the top-level instanceTemplate field. Read more about the relationships between these fields. Exactly one version must leave the targetSize field unset. That version will be applied to all remaining instances. For more information, read about canary updates.
        """
        if auto_healing_policies is not None:
            pulumi.set(__self__, "auto_healing_policies", auto_healing_policies)
        if base_instance_name is not None:
            pulumi.set(__self__, "base_instance_name", base_instance_name)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if distribution_policy is not None:
            pulumi.set(__self__, "distribution_policy", distribution_policy)
        if instance_template is not None:
            pulumi.set(__self__, "instance_template", instance_template)
        if list_managed_instances_results is not None:
            pulumi.set(__self__, "list_managed_instances_results", list_managed_instances_results)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if named_ports is not None:
            pulumi.set(__self__, "named_ports", named_ports)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if request_id is not None:
            pulumi.set(__self__, "request_id", request_id)
        if stateful_policy is not None:
            pulumi.set(__self__, "stateful_policy", stateful_policy)
        if target_pools is not None:
            pulumi.set(__self__, "target_pools", target_pools)
        if target_size is not None:
            pulumi.set(__self__, "target_size", target_size)
        if update_policy is not None:
            pulumi.set(__self__, "update_policy", update_policy)
        if versions is not None:
            pulumi.set(__self__, "versions", versions)
        if zone is not None:
            pulumi.set(__self__, "zone", zone)

    @property
    @pulumi.getter(name="autoHealingPolicies")
    def auto_healing_policies(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['InstanceGroupManagerAutoHealingPolicyArgs']]]]:
        """
        The autohealing policy for this managed instance group. You can specify only one value.
        """
        return pulumi.get(self, "auto_healing_policies")

    @auto_healing_policies.setter
    def auto_healing_policies(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['InstanceGroupManagerAutoHealingPolicyArgs']]]]):
        pulumi.set(self, "auto_healing_policies", value)

    @property
    @pulumi.getter(name="baseInstanceName")
    def base_instance_name(self) -> Optional[pulumi.Input[str]]:
        """
        The base instance name to use for instances in this group. The value must be 1-58 characters long. Instances are named by appending a hyphen and a random four-character string to the base instance name. The base instance name must comply with RFC1035.
        """
        return pulumi.get(self, "base_instance_name")

    @base_instance_name.setter
    def base_instance_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "base_instance_name", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        An optional description of this resource.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="distributionPolicy")
    def distribution_policy(self) -> Optional[pulumi.Input['DistributionPolicyArgs']]:
        """
        Policy specifying the intended distribution of managed instances across zones in a regional managed instance group.
        """
        return pulumi.get(self, "distribution_policy")

    @distribution_policy.setter
    def distribution_policy(self, value: Optional[pulumi.Input['DistributionPolicyArgs']]):
        pulumi.set(self, "distribution_policy", value)

    @property
    @pulumi.getter(name="instanceTemplate")
    def instance_template(self) -> Optional[pulumi.Input[str]]:
        """
        The URL of the instance template that is specified for this managed instance group. The group uses this template to create all new instances in the managed instance group. The templates for existing instances in the group do not change unless you run recreateInstances, run applyUpdatesToInstances, or set the group's updatePolicy.type to PROACTIVE.
        """
        return pulumi.get(self, "instance_template")

    @instance_template.setter
    def instance_template(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "instance_template", value)

    @property
    @pulumi.getter(name="listManagedInstancesResults")
    def list_managed_instances_results(self) -> Optional[pulumi.Input['InstanceGroupManagerListManagedInstancesResults']]:
        """
        Pagination behavior of the listManagedInstances API method for this managed instance group.
        """
        return pulumi.get(self, "list_managed_instances_results")

    @list_managed_instances_results.setter
    def list_managed_instances_results(self, value: Optional[pulumi.Input['InstanceGroupManagerListManagedInstancesResults']]):
        pulumi.set(self, "list_managed_instances_results", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the managed instance group. The name must be 1-63 characters long, and comply with RFC1035.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="namedPorts")
    def named_ports(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['NamedPortArgs']]]]:
        """
        Named ports configured for the Instance Groups complementary to this Instance Group Manager.
        """
        return pulumi.get(self, "named_ports")

    @named_ports.setter
    def named_ports(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['NamedPortArgs']]]]):
        pulumi.set(self, "named_ports", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter(name="requestId")
    def request_id(self) -> Optional[pulumi.Input[str]]:
        """
        An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000).
        """
        return pulumi.get(self, "request_id")

    @request_id.setter
    def request_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "request_id", value)

    @property
    @pulumi.getter(name="statefulPolicy")
    def stateful_policy(self) -> Optional[pulumi.Input['StatefulPolicyArgs']]:
        """
        Stateful configuration for this Instanced Group Manager
        """
        return pulumi.get(self, "stateful_policy")

    @stateful_policy.setter
    def stateful_policy(self, value: Optional[pulumi.Input['StatefulPolicyArgs']]):
        pulumi.set(self, "stateful_policy", value)

    @property
    @pulumi.getter(name="targetPools")
    def target_pools(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The URLs for all TargetPool resources to which instances in the instanceGroup field are added. The target pools automatically apply to all of the instances in the managed instance group.
        """
        return pulumi.get(self, "target_pools")

    @target_pools.setter
    def target_pools(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "target_pools", value)

    @property
    @pulumi.getter(name="targetSize")
    def target_size(self) -> Optional[pulumi.Input[int]]:
        """
        The target number of running instances for this managed instance group. You can reduce this number by using the instanceGroupManager deleteInstances or abandonInstances methods. Resizing the group also changes this number.
        """
        return pulumi.get(self, "target_size")

    @target_size.setter
    def target_size(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "target_size", value)

    @property
    @pulumi.getter(name="updatePolicy")
    def update_policy(self) -> Optional[pulumi.Input['InstanceGroupManagerUpdatePolicyArgs']]:
        """
        The update policy for this managed instance group.
        """
        return pulumi.get(self, "update_policy")

    @update_policy.setter
    def update_policy(self, value: Optional[pulumi.Input['InstanceGroupManagerUpdatePolicyArgs']]):
        pulumi.set(self, "update_policy", value)

    @property
    @pulumi.getter
    def versions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['InstanceGroupManagerVersionArgs']]]]:
        """
        Specifies the instance templates used by this managed instance group to create instances. Each version is defined by an instanceTemplate and a name. Every version can appear at most once per instance group. This field overrides the top-level instanceTemplate field. Read more about the relationships between these fields. Exactly one version must leave the targetSize field unset. That version will be applied to all remaining instances. For more information, read about canary updates.
        """
        return pulumi.get(self, "versions")

    @versions.setter
    def versions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['InstanceGroupManagerVersionArgs']]]]):
        pulumi.set(self, "versions", value)

    @property
    @pulumi.getter
    def zone(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "zone")

    @zone.setter
    def zone(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "zone", value)


class InstanceGroupManager(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 auto_healing_policies: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['InstanceGroupManagerAutoHealingPolicyArgs']]]]] = None,
                 base_instance_name: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 distribution_policy: Optional[pulumi.Input[pulumi.InputType['DistributionPolicyArgs']]] = None,
                 instance_template: Optional[pulumi.Input[str]] = None,
                 list_managed_instances_results: Optional[pulumi.Input['InstanceGroupManagerListManagedInstancesResults']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 named_ports: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NamedPortArgs']]]]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 request_id: Optional[pulumi.Input[str]] = None,
                 stateful_policy: Optional[pulumi.Input[pulumi.InputType['StatefulPolicyArgs']]] = None,
                 target_pools: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 target_size: Optional[pulumi.Input[int]] = None,
                 update_policy: Optional[pulumi.Input[pulumi.InputType['InstanceGroupManagerUpdatePolicyArgs']]] = None,
                 versions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['InstanceGroupManagerVersionArgs']]]]] = None,
                 zone: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Creates a managed instance group using the information that you specify in the request. After the group is created, instances in the group are created using the specified instance template. This operation is marked as DONE when the group is created even if the instances in the group have not yet been created. You must separately verify the status of the individual instances with the listmanagedinstances method. A managed instance group can have up to 1000 VM instances per group. Please contact Cloud Support if you need an increase in this limit.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['InstanceGroupManagerAutoHealingPolicyArgs']]]] auto_healing_policies: The autohealing policy for this managed instance group. You can specify only one value.
        :param pulumi.Input[str] base_instance_name: The base instance name to use for instances in this group. The value must be 1-58 characters long. Instances are named by appending a hyphen and a random four-character string to the base instance name. The base instance name must comply with RFC1035.
        :param pulumi.Input[str] description: An optional description of this resource.
        :param pulumi.Input[pulumi.InputType['DistributionPolicyArgs']] distribution_policy: Policy specifying the intended distribution of managed instances across zones in a regional managed instance group.
        :param pulumi.Input[str] instance_template: The URL of the instance template that is specified for this managed instance group. The group uses this template to create all new instances in the managed instance group. The templates for existing instances in the group do not change unless you run recreateInstances, run applyUpdatesToInstances, or set the group's updatePolicy.type to PROACTIVE.
        :param pulumi.Input['InstanceGroupManagerListManagedInstancesResults'] list_managed_instances_results: Pagination behavior of the listManagedInstances API method for this managed instance group.
        :param pulumi.Input[str] name: The name of the managed instance group. The name must be 1-63 characters long, and comply with RFC1035.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NamedPortArgs']]]] named_ports: Named ports configured for the Instance Groups complementary to this Instance Group Manager.
        :param pulumi.Input[str] request_id: An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000).
        :param pulumi.Input[pulumi.InputType['StatefulPolicyArgs']] stateful_policy: Stateful configuration for this Instanced Group Manager
        :param pulumi.Input[Sequence[pulumi.Input[str]]] target_pools: The URLs for all TargetPool resources to which instances in the instanceGroup field are added. The target pools automatically apply to all of the instances in the managed instance group.
        :param pulumi.Input[int] target_size: The target number of running instances for this managed instance group. You can reduce this number by using the instanceGroupManager deleteInstances or abandonInstances methods. Resizing the group also changes this number.
        :param pulumi.Input[pulumi.InputType['InstanceGroupManagerUpdatePolicyArgs']] update_policy: The update policy for this managed instance group.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['InstanceGroupManagerVersionArgs']]]] versions: Specifies the instance templates used by this managed instance group to create instances. Each version is defined by an instanceTemplate and a name. Every version can appear at most once per instance group. This field overrides the top-level instanceTemplate field. Read more about the relationships between these fields. Exactly one version must leave the targetSize field unset. That version will be applied to all remaining instances. For more information, read about canary updates.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[InstanceGroupManagerArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Creates a managed instance group using the information that you specify in the request. After the group is created, instances in the group are created using the specified instance template. This operation is marked as DONE when the group is created even if the instances in the group have not yet been created. You must separately verify the status of the individual instances with the listmanagedinstances method. A managed instance group can have up to 1000 VM instances per group. Please contact Cloud Support if you need an increase in this limit.

        :param str resource_name: The name of the resource.
        :param InstanceGroupManagerArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(InstanceGroupManagerArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 auto_healing_policies: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['InstanceGroupManagerAutoHealingPolicyArgs']]]]] = None,
                 base_instance_name: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 distribution_policy: Optional[pulumi.Input[pulumi.InputType['DistributionPolicyArgs']]] = None,
                 instance_template: Optional[pulumi.Input[str]] = None,
                 list_managed_instances_results: Optional[pulumi.Input['InstanceGroupManagerListManagedInstancesResults']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 named_ports: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NamedPortArgs']]]]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 request_id: Optional[pulumi.Input[str]] = None,
                 stateful_policy: Optional[pulumi.Input[pulumi.InputType['StatefulPolicyArgs']]] = None,
                 target_pools: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 target_size: Optional[pulumi.Input[int]] = None,
                 update_policy: Optional[pulumi.Input[pulumi.InputType['InstanceGroupManagerUpdatePolicyArgs']]] = None,
                 versions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['InstanceGroupManagerVersionArgs']]]]] = None,
                 zone: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = InstanceGroupManagerArgs.__new__(InstanceGroupManagerArgs)

            __props__.__dict__["auto_healing_policies"] = auto_healing_policies
            __props__.__dict__["base_instance_name"] = base_instance_name
            __props__.__dict__["description"] = description
            __props__.__dict__["distribution_policy"] = distribution_policy
            __props__.__dict__["instance_template"] = instance_template
            __props__.__dict__["list_managed_instances_results"] = list_managed_instances_results
            __props__.__dict__["name"] = name
            __props__.__dict__["named_ports"] = named_ports
            __props__.__dict__["project"] = project
            __props__.__dict__["request_id"] = request_id
            __props__.__dict__["stateful_policy"] = stateful_policy
            __props__.__dict__["target_pools"] = target_pools
            __props__.__dict__["target_size"] = target_size
            __props__.__dict__["update_policy"] = update_policy
            __props__.__dict__["versions"] = versions
            __props__.__dict__["zone"] = zone
            __props__.__dict__["creation_timestamp"] = None
            __props__.__dict__["current_actions"] = None
            __props__.__dict__["fingerprint"] = None
            __props__.__dict__["instance_group"] = None
            __props__.__dict__["kind"] = None
            __props__.__dict__["region"] = None
            __props__.__dict__["self_link"] = None
            __props__.__dict__["status"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["project", "zone"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(InstanceGroupManager, __self__).__init__(
            'google-native:compute/v1:InstanceGroupManager',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'InstanceGroupManager':
        """
        Get an existing InstanceGroupManager resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = InstanceGroupManagerArgs.__new__(InstanceGroupManagerArgs)

        __props__.__dict__["auto_healing_policies"] = None
        __props__.__dict__["base_instance_name"] = None
        __props__.__dict__["creation_timestamp"] = None
        __props__.__dict__["current_actions"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["distribution_policy"] = None
        __props__.__dict__["fingerprint"] = None
        __props__.__dict__["instance_group"] = None
        __props__.__dict__["instance_template"] = None
        __props__.__dict__["kind"] = None
        __props__.__dict__["list_managed_instances_results"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["named_ports"] = None
        __props__.__dict__["project"] = None
        __props__.__dict__["region"] = None
        __props__.__dict__["request_id"] = None
        __props__.__dict__["self_link"] = None
        __props__.__dict__["stateful_policy"] = None
        __props__.__dict__["status"] = None
        __props__.__dict__["target_pools"] = None
        __props__.__dict__["target_size"] = None
        __props__.__dict__["update_policy"] = None
        __props__.__dict__["versions"] = None
        __props__.__dict__["zone"] = None
        return InstanceGroupManager(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="autoHealingPolicies")
    def auto_healing_policies(self) -> pulumi.Output[Sequence['outputs.InstanceGroupManagerAutoHealingPolicyResponse']]:
        """
        The autohealing policy for this managed instance group. You can specify only one value.
        """
        return pulumi.get(self, "auto_healing_policies")

    @property
    @pulumi.getter(name="baseInstanceName")
    def base_instance_name(self) -> pulumi.Output[str]:
        """
        The base instance name to use for instances in this group. The value must be 1-58 characters long. Instances are named by appending a hyphen and a random four-character string to the base instance name. The base instance name must comply with RFC1035.
        """
        return pulumi.get(self, "base_instance_name")

    @property
    @pulumi.getter(name="creationTimestamp")
    def creation_timestamp(self) -> pulumi.Output[str]:
        """
        The creation timestamp for this managed instance group in RFC3339 text format.
        """
        return pulumi.get(self, "creation_timestamp")

    @property
    @pulumi.getter(name="currentActions")
    def current_actions(self) -> pulumi.Output['outputs.InstanceGroupManagerActionsSummaryResponse']:
        """
        The list of instance actions and the number of instances in this managed instance group that are scheduled for each of those actions.
        """
        return pulumi.get(self, "current_actions")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[str]:
        """
        An optional description of this resource.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="distributionPolicy")
    def distribution_policy(self) -> pulumi.Output['outputs.DistributionPolicyResponse']:
        """
        Policy specifying the intended distribution of managed instances across zones in a regional managed instance group.
        """
        return pulumi.get(self, "distribution_policy")

    @property
    @pulumi.getter
    def fingerprint(self) -> pulumi.Output[str]:
        """
        Fingerprint of this resource. This field may be used in optimistic locking. It will be ignored when inserting an InstanceGroupManager. An up-to-date fingerprint must be provided in order to update the InstanceGroupManager, otherwise the request will fail with error 412 conditionNotMet. To see the latest fingerprint, make a get() request to retrieve an InstanceGroupManager.
        """
        return pulumi.get(self, "fingerprint")

    @property
    @pulumi.getter(name="instanceGroup")
    def instance_group(self) -> pulumi.Output[str]:
        """
        The URL of the Instance Group resource.
        """
        return pulumi.get(self, "instance_group")

    @property
    @pulumi.getter(name="instanceTemplate")
    def instance_template(self) -> pulumi.Output[str]:
        """
        The URL of the instance template that is specified for this managed instance group. The group uses this template to create all new instances in the managed instance group. The templates for existing instances in the group do not change unless you run recreateInstances, run applyUpdatesToInstances, or set the group's updatePolicy.type to PROACTIVE.
        """
        return pulumi.get(self, "instance_template")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[str]:
        """
        The resource type, which is always compute#instanceGroupManager for managed instance groups.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter(name="listManagedInstancesResults")
    def list_managed_instances_results(self) -> pulumi.Output[str]:
        """
        Pagination behavior of the listManagedInstances API method for this managed instance group.
        """
        return pulumi.get(self, "list_managed_instances_results")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the managed instance group. The name must be 1-63 characters long, and comply with RFC1035.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="namedPorts")
    def named_ports(self) -> pulumi.Output[Sequence['outputs.NamedPortResponse']]:
        """
        Named ports configured for the Instance Groups complementary to this Instance Group Manager.
        """
        return pulumi.get(self, "named_ports")

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        return pulumi.get(self, "project")

    @property
    @pulumi.getter
    def region(self) -> pulumi.Output[str]:
        """
        The URL of the region where the managed instance group resides (for regional resources).
        """
        return pulumi.get(self, "region")

    @property
    @pulumi.getter(name="requestId")
    def request_id(self) -> pulumi.Output[Optional[str]]:
        """
        An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000).
        """
        return pulumi.get(self, "request_id")

    @property
    @pulumi.getter(name="selfLink")
    def self_link(self) -> pulumi.Output[str]:
        """
        The URL for this managed instance group. The server defines this URL.
        """
        return pulumi.get(self, "self_link")

    @property
    @pulumi.getter(name="statefulPolicy")
    def stateful_policy(self) -> pulumi.Output['outputs.StatefulPolicyResponse']:
        """
        Stateful configuration for this Instanced Group Manager
        """
        return pulumi.get(self, "stateful_policy")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output['outputs.InstanceGroupManagerStatusResponse']:
        """
        The status of this managed instance group.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="targetPools")
    def target_pools(self) -> pulumi.Output[Sequence[str]]:
        """
        The URLs for all TargetPool resources to which instances in the instanceGroup field are added. The target pools automatically apply to all of the instances in the managed instance group.
        """
        return pulumi.get(self, "target_pools")

    @property
    @pulumi.getter(name="targetSize")
    def target_size(self) -> pulumi.Output[int]:
        """
        The target number of running instances for this managed instance group. You can reduce this number by using the instanceGroupManager deleteInstances or abandonInstances methods. Resizing the group also changes this number.
        """
        return pulumi.get(self, "target_size")

    @property
    @pulumi.getter(name="updatePolicy")
    def update_policy(self) -> pulumi.Output['outputs.InstanceGroupManagerUpdatePolicyResponse']:
        """
        The update policy for this managed instance group.
        """
        return pulumi.get(self, "update_policy")

    @property
    @pulumi.getter
    def versions(self) -> pulumi.Output[Sequence['outputs.InstanceGroupManagerVersionResponse']]:
        """
        Specifies the instance templates used by this managed instance group to create instances. Each version is defined by an instanceTemplate and a name. Every version can appear at most once per instance group. This field overrides the top-level instanceTemplate field. Read more about the relationships between these fields. Exactly one version must leave the targetSize field unset. That version will be applied to all remaining instances. For more information, read about canary updates.
        """
        return pulumi.get(self, "versions")

    @property
    @pulumi.getter
    def zone(self) -> pulumi.Output[str]:
        return pulumi.get(self, "zone")

