# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from ._enums import *

__all__ = ['RegionHealthCheckServiceArgs', 'RegionHealthCheckService']

@pulumi.input_type
class RegionHealthCheckServiceArgs:
    def __init__(__self__, *,
                 region: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 health_checks: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 health_status_aggregation_policy: Optional[pulumi.Input['RegionHealthCheckServiceHealthStatusAggregationPolicy']] = None,
                 health_status_aggregation_strategy: Optional[pulumi.Input['RegionHealthCheckServiceHealthStatusAggregationStrategy']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network_endpoint_groups: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 notification_endpoints: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 request_id: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a RegionHealthCheckService resource.
        :param pulumi.Input[str] description: An optional description of this resource. Provide this property when you create the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] health_checks: A list of URLs to the HealthCheck resources. Must have at least one HealthCheck, and not more than 10. HealthCheck resources must have portSpecification=USE_SERVING_PORT or portSpecification=USE_FIXED_PORT. For regional HealthCheckService, the HealthCheck must be regional and in the same region. For global HealthCheckService, HealthCheck must be global. Mix of regional and global HealthChecks is not supported. Multiple regional HealthChecks must belong to the same region. Regional HealthChecks must belong to the same region as zones of NEGs.
        :param pulumi.Input['RegionHealthCheckServiceHealthStatusAggregationPolicy'] health_status_aggregation_policy: Optional. Policy for how the results from multiple health checks for the same endpoint are aggregated. Defaults to NO_AGGREGATION if unspecified. - NO_AGGREGATION. An EndpointHealth message is returned for each pair in the health check service. - AND. If any health check of an endpoint reports UNHEALTHY, then UNHEALTHY is the HealthState of the endpoint. If all health checks report HEALTHY, the HealthState of the endpoint is HEALTHY. .
        :param pulumi.Input['RegionHealthCheckServiceHealthStatusAggregationStrategy'] health_status_aggregation_strategy: This field is deprecated. Use health_status_aggregation_policy instead. Policy for how the results from multiple health checks for the same endpoint are aggregated. - NO_AGGREGATION. An EndpointHealth message is returned for each backend in the health check service. - AND. If any backend's health check reports UNHEALTHY, then UNHEALTHY is the HealthState of the entire health check service. If all backend's are healthy, the HealthState of the health check service is HEALTHY. .
        :param pulumi.Input[str] name: Name of the resource. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression `[a-z]([-a-z0-9]*[a-z0-9])?` which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] network_endpoint_groups: A list of URLs to the NetworkEndpointGroup resources. Must not have more than 100. For regional HealthCheckService, NEGs must be in zones in the region of the HealthCheckService.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] notification_endpoints: A list of URLs to the NotificationEndpoint resources. Must not have more than 10. A list of endpoints for receiving notifications of change in health status. For regional HealthCheckService, NotificationEndpoint must be regional and in the same region. For global HealthCheckService, NotificationEndpoint must be global.
        :param pulumi.Input[str] request_id: An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000).
        """
        pulumi.set(__self__, "region", region)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if health_checks is not None:
            pulumi.set(__self__, "health_checks", health_checks)
        if health_status_aggregation_policy is not None:
            pulumi.set(__self__, "health_status_aggregation_policy", health_status_aggregation_policy)
        if health_status_aggregation_strategy is not None:
            warnings.warn("""This field is deprecated. Use health_status_aggregation_policy instead. Policy for how the results from multiple health checks for the same endpoint are aggregated. - NO_AGGREGATION. An EndpointHealth message is returned for each backend in the health check service. - AND. If any backend's health check reports UNHEALTHY, then UNHEALTHY is the HealthState of the entire health check service. If all backend's are healthy, the HealthState of the health check service is HEALTHY. .""", DeprecationWarning)
            pulumi.log.warn("""health_status_aggregation_strategy is deprecated: This field is deprecated. Use health_status_aggregation_policy instead. Policy for how the results from multiple health checks for the same endpoint are aggregated. - NO_AGGREGATION. An EndpointHealth message is returned for each backend in the health check service. - AND. If any backend's health check reports UNHEALTHY, then UNHEALTHY is the HealthState of the entire health check service. If all backend's are healthy, the HealthState of the health check service is HEALTHY. .""")
        if health_status_aggregation_strategy is not None:
            pulumi.set(__self__, "health_status_aggregation_strategy", health_status_aggregation_strategy)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if network_endpoint_groups is not None:
            pulumi.set(__self__, "network_endpoint_groups", network_endpoint_groups)
        if notification_endpoints is not None:
            pulumi.set(__self__, "notification_endpoints", notification_endpoints)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if request_id is not None:
            pulumi.set(__self__, "request_id", request_id)

    @property
    @pulumi.getter
    def region(self) -> pulumi.Input[str]:
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: pulumi.Input[str]):
        pulumi.set(self, "region", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        An optional description of this resource. Provide this property when you create the resource.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="healthChecks")
    def health_checks(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of URLs to the HealthCheck resources. Must have at least one HealthCheck, and not more than 10. HealthCheck resources must have portSpecification=USE_SERVING_PORT or portSpecification=USE_FIXED_PORT. For regional HealthCheckService, the HealthCheck must be regional and in the same region. For global HealthCheckService, HealthCheck must be global. Mix of regional and global HealthChecks is not supported. Multiple regional HealthChecks must belong to the same region. Regional HealthChecks must belong to the same region as zones of NEGs.
        """
        return pulumi.get(self, "health_checks")

    @health_checks.setter
    def health_checks(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "health_checks", value)

    @property
    @pulumi.getter(name="healthStatusAggregationPolicy")
    def health_status_aggregation_policy(self) -> Optional[pulumi.Input['RegionHealthCheckServiceHealthStatusAggregationPolicy']]:
        """
        Optional. Policy for how the results from multiple health checks for the same endpoint are aggregated. Defaults to NO_AGGREGATION if unspecified. - NO_AGGREGATION. An EndpointHealth message is returned for each pair in the health check service. - AND. If any health check of an endpoint reports UNHEALTHY, then UNHEALTHY is the HealthState of the endpoint. If all health checks report HEALTHY, the HealthState of the endpoint is HEALTHY. .
        """
        return pulumi.get(self, "health_status_aggregation_policy")

    @health_status_aggregation_policy.setter
    def health_status_aggregation_policy(self, value: Optional[pulumi.Input['RegionHealthCheckServiceHealthStatusAggregationPolicy']]):
        pulumi.set(self, "health_status_aggregation_policy", value)

    @property
    @pulumi.getter(name="healthStatusAggregationStrategy")
    def health_status_aggregation_strategy(self) -> Optional[pulumi.Input['RegionHealthCheckServiceHealthStatusAggregationStrategy']]:
        """
        This field is deprecated. Use health_status_aggregation_policy instead. Policy for how the results from multiple health checks for the same endpoint are aggregated. - NO_AGGREGATION. An EndpointHealth message is returned for each backend in the health check service. - AND. If any backend's health check reports UNHEALTHY, then UNHEALTHY is the HealthState of the entire health check service. If all backend's are healthy, the HealthState of the health check service is HEALTHY. .
        """
        return pulumi.get(self, "health_status_aggregation_strategy")

    @health_status_aggregation_strategy.setter
    def health_status_aggregation_strategy(self, value: Optional[pulumi.Input['RegionHealthCheckServiceHealthStatusAggregationStrategy']]):
        pulumi.set(self, "health_status_aggregation_strategy", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the resource. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression `[a-z]([-a-z0-9]*[a-z0-9])?` which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="networkEndpointGroups")
    def network_endpoint_groups(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of URLs to the NetworkEndpointGroup resources. Must not have more than 100. For regional HealthCheckService, NEGs must be in zones in the region of the HealthCheckService.
        """
        return pulumi.get(self, "network_endpoint_groups")

    @network_endpoint_groups.setter
    def network_endpoint_groups(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "network_endpoint_groups", value)

    @property
    @pulumi.getter(name="notificationEndpoints")
    def notification_endpoints(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of URLs to the NotificationEndpoint resources. Must not have more than 10. A list of endpoints for receiving notifications of change in health status. For regional HealthCheckService, NotificationEndpoint must be regional and in the same region. For global HealthCheckService, NotificationEndpoint must be global.
        """
        return pulumi.get(self, "notification_endpoints")

    @notification_endpoints.setter
    def notification_endpoints(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "notification_endpoints", value)

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


class RegionHealthCheckService(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 health_checks: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 health_status_aggregation_policy: Optional[pulumi.Input['RegionHealthCheckServiceHealthStatusAggregationPolicy']] = None,
                 health_status_aggregation_strategy: Optional[pulumi.Input['RegionHealthCheckServiceHealthStatusAggregationStrategy']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network_endpoint_groups: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 notification_endpoints: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 request_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Creates a regional HealthCheckService resource in the specified project and region using the data included in the request.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: An optional description of this resource. Provide this property when you create the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] health_checks: A list of URLs to the HealthCheck resources. Must have at least one HealthCheck, and not more than 10. HealthCheck resources must have portSpecification=USE_SERVING_PORT or portSpecification=USE_FIXED_PORT. For regional HealthCheckService, the HealthCheck must be regional and in the same region. For global HealthCheckService, HealthCheck must be global. Mix of regional and global HealthChecks is not supported. Multiple regional HealthChecks must belong to the same region. Regional HealthChecks must belong to the same region as zones of NEGs.
        :param pulumi.Input['RegionHealthCheckServiceHealthStatusAggregationPolicy'] health_status_aggregation_policy: Optional. Policy for how the results from multiple health checks for the same endpoint are aggregated. Defaults to NO_AGGREGATION if unspecified. - NO_AGGREGATION. An EndpointHealth message is returned for each pair in the health check service. - AND. If any health check of an endpoint reports UNHEALTHY, then UNHEALTHY is the HealthState of the endpoint. If all health checks report HEALTHY, the HealthState of the endpoint is HEALTHY. .
        :param pulumi.Input['RegionHealthCheckServiceHealthStatusAggregationStrategy'] health_status_aggregation_strategy: This field is deprecated. Use health_status_aggregation_policy instead. Policy for how the results from multiple health checks for the same endpoint are aggregated. - NO_AGGREGATION. An EndpointHealth message is returned for each backend in the health check service. - AND. If any backend's health check reports UNHEALTHY, then UNHEALTHY is the HealthState of the entire health check service. If all backend's are healthy, the HealthState of the health check service is HEALTHY. .
        :param pulumi.Input[str] name: Name of the resource. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression `[a-z]([-a-z0-9]*[a-z0-9])?` which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] network_endpoint_groups: A list of URLs to the NetworkEndpointGroup resources. Must not have more than 100. For regional HealthCheckService, NEGs must be in zones in the region of the HealthCheckService.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] notification_endpoints: A list of URLs to the NotificationEndpoint resources. Must not have more than 10. A list of endpoints for receiving notifications of change in health status. For regional HealthCheckService, NotificationEndpoint must be regional and in the same region. For global HealthCheckService, NotificationEndpoint must be global.
        :param pulumi.Input[str] request_id: An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000).
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: RegionHealthCheckServiceArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Creates a regional HealthCheckService resource in the specified project and region using the data included in the request.

        :param str resource_name: The name of the resource.
        :param RegionHealthCheckServiceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(RegionHealthCheckServiceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 health_checks: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 health_status_aggregation_policy: Optional[pulumi.Input['RegionHealthCheckServiceHealthStatusAggregationPolicy']] = None,
                 health_status_aggregation_strategy: Optional[pulumi.Input['RegionHealthCheckServiceHealthStatusAggregationStrategy']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network_endpoint_groups: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 notification_endpoints: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 request_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = RegionHealthCheckServiceArgs.__new__(RegionHealthCheckServiceArgs)

            __props__.__dict__["description"] = description
            __props__.__dict__["health_checks"] = health_checks
            __props__.__dict__["health_status_aggregation_policy"] = health_status_aggregation_policy
            if health_status_aggregation_strategy is not None and not opts.urn:
                warnings.warn("""This field is deprecated. Use health_status_aggregation_policy instead. Policy for how the results from multiple health checks for the same endpoint are aggregated. - NO_AGGREGATION. An EndpointHealth message is returned for each backend in the health check service. - AND. If any backend's health check reports UNHEALTHY, then UNHEALTHY is the HealthState of the entire health check service. If all backend's are healthy, the HealthState of the health check service is HEALTHY. .""", DeprecationWarning)
                pulumi.log.warn("""health_status_aggregation_strategy is deprecated: This field is deprecated. Use health_status_aggregation_policy instead. Policy for how the results from multiple health checks for the same endpoint are aggregated. - NO_AGGREGATION. An EndpointHealth message is returned for each backend in the health check service. - AND. If any backend's health check reports UNHEALTHY, then UNHEALTHY is the HealthState of the entire health check service. If all backend's are healthy, the HealthState of the health check service is HEALTHY. .""")
            __props__.__dict__["health_status_aggregation_strategy"] = health_status_aggregation_strategy
            __props__.__dict__["name"] = name
            __props__.__dict__["network_endpoint_groups"] = network_endpoint_groups
            __props__.__dict__["notification_endpoints"] = notification_endpoints
            __props__.__dict__["project"] = project
            if region is None and not opts.urn:
                raise TypeError("Missing required property 'region'")
            __props__.__dict__["region"] = region
            __props__.__dict__["request_id"] = request_id
            __props__.__dict__["creation_timestamp"] = None
            __props__.__dict__["fingerprint"] = None
            __props__.__dict__["kind"] = None
            __props__.__dict__["self_link"] = None
            __props__.__dict__["self_link_with_id"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["project", "region"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(RegionHealthCheckService, __self__).__init__(
            'google-native:compute/alpha:RegionHealthCheckService',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'RegionHealthCheckService':
        """
        Get an existing RegionHealthCheckService resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = RegionHealthCheckServiceArgs.__new__(RegionHealthCheckServiceArgs)

        __props__.__dict__["creation_timestamp"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["fingerprint"] = None
        __props__.__dict__["health_checks"] = None
        __props__.__dict__["health_status_aggregation_policy"] = None
        __props__.__dict__["health_status_aggregation_strategy"] = None
        __props__.__dict__["kind"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["network_endpoint_groups"] = None
        __props__.__dict__["notification_endpoints"] = None
        __props__.__dict__["project"] = None
        __props__.__dict__["region"] = None
        __props__.__dict__["request_id"] = None
        __props__.__dict__["self_link"] = None
        __props__.__dict__["self_link_with_id"] = None
        return RegionHealthCheckService(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="creationTimestamp")
    def creation_timestamp(self) -> pulumi.Output[str]:
        """
        Creation timestamp in RFC3339 text format.
        """
        return pulumi.get(self, "creation_timestamp")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[str]:
        """
        An optional description of this resource. Provide this property when you create the resource.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def fingerprint(self) -> pulumi.Output[str]:
        """
        Fingerprint of this resource. A hash of the contents stored in this object. This field is used in optimistic locking. This field will be ignored when inserting a HealthCheckService. An up-to-date fingerprint must be provided in order to patch/update the HealthCheckService; Otherwise, the request will fail with error 412 conditionNotMet. To see the latest fingerprint, make a get() request to retrieve the HealthCheckService.
        """
        return pulumi.get(self, "fingerprint")

    @property
    @pulumi.getter(name="healthChecks")
    def health_checks(self) -> pulumi.Output[Sequence[str]]:
        """
        A list of URLs to the HealthCheck resources. Must have at least one HealthCheck, and not more than 10. HealthCheck resources must have portSpecification=USE_SERVING_PORT or portSpecification=USE_FIXED_PORT. For regional HealthCheckService, the HealthCheck must be regional and in the same region. For global HealthCheckService, HealthCheck must be global. Mix of regional and global HealthChecks is not supported. Multiple regional HealthChecks must belong to the same region. Regional HealthChecks must belong to the same region as zones of NEGs.
        """
        return pulumi.get(self, "health_checks")

    @property
    @pulumi.getter(name="healthStatusAggregationPolicy")
    def health_status_aggregation_policy(self) -> pulumi.Output[str]:
        """
        Optional. Policy for how the results from multiple health checks for the same endpoint are aggregated. Defaults to NO_AGGREGATION if unspecified. - NO_AGGREGATION. An EndpointHealth message is returned for each pair in the health check service. - AND. If any health check of an endpoint reports UNHEALTHY, then UNHEALTHY is the HealthState of the endpoint. If all health checks report HEALTHY, the HealthState of the endpoint is HEALTHY. .
        """
        return pulumi.get(self, "health_status_aggregation_policy")

    @property
    @pulumi.getter(name="healthStatusAggregationStrategy")
    def health_status_aggregation_strategy(self) -> pulumi.Output[str]:
        """
        This field is deprecated. Use health_status_aggregation_policy instead. Policy for how the results from multiple health checks for the same endpoint are aggregated. - NO_AGGREGATION. An EndpointHealth message is returned for each backend in the health check service. - AND. If any backend's health check reports UNHEALTHY, then UNHEALTHY is the HealthState of the entire health check service. If all backend's are healthy, the HealthState of the health check service is HEALTHY. .
        """
        return pulumi.get(self, "health_status_aggregation_strategy")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[str]:
        """
        [Output only] Type of the resource. Always compute#healthCheckServicefor health check services.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the resource. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression `[a-z]([-a-z0-9]*[a-z0-9])?` which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="networkEndpointGroups")
    def network_endpoint_groups(self) -> pulumi.Output[Sequence[str]]:
        """
        A list of URLs to the NetworkEndpointGroup resources. Must not have more than 100. For regional HealthCheckService, NEGs must be in zones in the region of the HealthCheckService.
        """
        return pulumi.get(self, "network_endpoint_groups")

    @property
    @pulumi.getter(name="notificationEndpoints")
    def notification_endpoints(self) -> pulumi.Output[Sequence[str]]:
        """
        A list of URLs to the NotificationEndpoint resources. Must not have more than 10. A list of endpoints for receiving notifications of change in health status. For regional HealthCheckService, NotificationEndpoint must be regional and in the same region. For global HealthCheckService, NotificationEndpoint must be global.
        """
        return pulumi.get(self, "notification_endpoints")

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        return pulumi.get(self, "project")

    @property
    @pulumi.getter
    def region(self) -> pulumi.Output[str]:
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
        Server-defined URL for the resource.
        """
        return pulumi.get(self, "self_link")

    @property
    @pulumi.getter(name="selfLinkWithId")
    def self_link_with_id(self) -> pulumi.Output[str]:
        """
        Server-defined URL with id for the resource.
        """
        return pulumi.get(self, "self_link_with_id")

