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

__all__ = ['ServiceArgs', 'Service']

@pulumi.input_type
class ServiceArgs:
    def __init__(__self__, *,
                 service_id: pulumi.Input[str],
                 database_type: Optional[pulumi.Input['ServiceDatabaseType']] = None,
                 encryption_config: Optional[pulumi.Input['EncryptionConfigArgs']] = None,
                 hive_metastore_config: Optional[pulumi.Input['HiveMetastoreConfigArgs']] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 maintenance_window: Optional[pulumi.Input['MaintenanceWindowArgs']] = None,
                 metadata_integration: Optional[pulumi.Input['MetadataIntegrationArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network: Optional[pulumi.Input[str]] = None,
                 network_config: Optional[pulumi.Input['NetworkConfigArgs']] = None,
                 port: Optional[pulumi.Input[int]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 release_channel: Optional[pulumi.Input['ServiceReleaseChannel']] = None,
                 request_id: Optional[pulumi.Input[str]] = None,
                 tier: Optional[pulumi.Input['ServiceTier']] = None):
        """
        The set of arguments for constructing a Service resource.
        :param pulumi.Input[str] service_id: Required. The ID of the metastore service, which is used as the final component of the metastore service's name.This value must be between 2 and 63 characters long inclusive, begin with a letter, end with a letter or number, and consist of alpha-numeric ASCII characters or hyphens.
        :param pulumi.Input['ServiceDatabaseType'] database_type: Immutable. The database type that the Metastore service stores its data.
        :param pulumi.Input['EncryptionConfigArgs'] encryption_config: Immutable. Information used to configure the Dataproc Metastore service to encrypt customer data at rest. Cannot be updated.
        :param pulumi.Input['HiveMetastoreConfigArgs'] hive_metastore_config: Configuration information specific to running Hive metastore software as the metastore service.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: User-defined labels for the metastore service.
        :param pulumi.Input['MaintenanceWindowArgs'] maintenance_window: The one hour maintenance window of the metastore service. This specifies when the service can be restarted for maintenance purposes in UTC time. Maintenance window is not needed for services with the SPANNER database type.
        :param pulumi.Input['MetadataIntegrationArgs'] metadata_integration: The setting that defines how metastore metadata should be integrated with external services and systems.
        :param pulumi.Input[str] name: Immutable. The relative resource name of the metastore service, in the following format:projects/{project_number}/locations/{location_id}/services/{service_id}.
        :param pulumi.Input[str] network: Immutable. The relative resource name of the VPC network on which the instance can be accessed. It is specified in the following form:projects/{project_number}/global/networks/{network_id}.
        :param pulumi.Input['NetworkConfigArgs'] network_config: The configuration specifying the network settings for the Dataproc Metastore service.
        :param pulumi.Input[int] port: The TCP port at which the metastore service is reached. Default: 9083.
        :param pulumi.Input['ServiceReleaseChannel'] release_channel: Immutable. The release channel of the service. If unspecified, defaults to STABLE.
        :param pulumi.Input[str] request_id: Optional. A request ID. Specify a unique request ID to allow the server to ignore the request if it has completed. The server will ignore subsequent requests that provide a duplicate request ID for at least 60 minutes after the first request.For example, if an initial request times out, followed by another request with the same request ID, the server ignores the second request to prevent the creation of duplicate commitments.The request ID must be a valid UUID (https://en.wikipedia.org/wiki/Universally_unique_identifier#Format) A zero UUID (00000000-0000-0000-0000-000000000000) is not supported.
        :param pulumi.Input['ServiceTier'] tier: The tier of the service.
        """
        pulumi.set(__self__, "service_id", service_id)
        if database_type is not None:
            pulumi.set(__self__, "database_type", database_type)
        if encryption_config is not None:
            pulumi.set(__self__, "encryption_config", encryption_config)
        if hive_metastore_config is not None:
            pulumi.set(__self__, "hive_metastore_config", hive_metastore_config)
        if labels is not None:
            pulumi.set(__self__, "labels", labels)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if maintenance_window is not None:
            pulumi.set(__self__, "maintenance_window", maintenance_window)
        if metadata_integration is not None:
            pulumi.set(__self__, "metadata_integration", metadata_integration)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if network is not None:
            pulumi.set(__self__, "network", network)
        if network_config is not None:
            pulumi.set(__self__, "network_config", network_config)
        if port is not None:
            pulumi.set(__self__, "port", port)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if release_channel is not None:
            pulumi.set(__self__, "release_channel", release_channel)
        if request_id is not None:
            pulumi.set(__self__, "request_id", request_id)
        if tier is not None:
            pulumi.set(__self__, "tier", tier)

    @property
    @pulumi.getter(name="serviceId")
    def service_id(self) -> pulumi.Input[str]:
        """
        Required. The ID of the metastore service, which is used as the final component of the metastore service's name.This value must be between 2 and 63 characters long inclusive, begin with a letter, end with a letter or number, and consist of alpha-numeric ASCII characters or hyphens.
        """
        return pulumi.get(self, "service_id")

    @service_id.setter
    def service_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "service_id", value)

    @property
    @pulumi.getter(name="databaseType")
    def database_type(self) -> Optional[pulumi.Input['ServiceDatabaseType']]:
        """
        Immutable. The database type that the Metastore service stores its data.
        """
        return pulumi.get(self, "database_type")

    @database_type.setter
    def database_type(self, value: Optional[pulumi.Input['ServiceDatabaseType']]):
        pulumi.set(self, "database_type", value)

    @property
    @pulumi.getter(name="encryptionConfig")
    def encryption_config(self) -> Optional[pulumi.Input['EncryptionConfigArgs']]:
        """
        Immutable. Information used to configure the Dataproc Metastore service to encrypt customer data at rest. Cannot be updated.
        """
        return pulumi.get(self, "encryption_config")

    @encryption_config.setter
    def encryption_config(self, value: Optional[pulumi.Input['EncryptionConfigArgs']]):
        pulumi.set(self, "encryption_config", value)

    @property
    @pulumi.getter(name="hiveMetastoreConfig")
    def hive_metastore_config(self) -> Optional[pulumi.Input['HiveMetastoreConfigArgs']]:
        """
        Configuration information specific to running Hive metastore software as the metastore service.
        """
        return pulumi.get(self, "hive_metastore_config")

    @hive_metastore_config.setter
    def hive_metastore_config(self, value: Optional[pulumi.Input['HiveMetastoreConfigArgs']]):
        pulumi.set(self, "hive_metastore_config", value)

    @property
    @pulumi.getter
    def labels(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        User-defined labels for the metastore service.
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
    @pulumi.getter(name="maintenanceWindow")
    def maintenance_window(self) -> Optional[pulumi.Input['MaintenanceWindowArgs']]:
        """
        The one hour maintenance window of the metastore service. This specifies when the service can be restarted for maintenance purposes in UTC time. Maintenance window is not needed for services with the SPANNER database type.
        """
        return pulumi.get(self, "maintenance_window")

    @maintenance_window.setter
    def maintenance_window(self, value: Optional[pulumi.Input['MaintenanceWindowArgs']]):
        pulumi.set(self, "maintenance_window", value)

    @property
    @pulumi.getter(name="metadataIntegration")
    def metadata_integration(self) -> Optional[pulumi.Input['MetadataIntegrationArgs']]:
        """
        The setting that defines how metastore metadata should be integrated with external services and systems.
        """
        return pulumi.get(self, "metadata_integration")

    @metadata_integration.setter
    def metadata_integration(self, value: Optional[pulumi.Input['MetadataIntegrationArgs']]):
        pulumi.set(self, "metadata_integration", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Immutable. The relative resource name of the metastore service, in the following format:projects/{project_number}/locations/{location_id}/services/{service_id}.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def network(self) -> Optional[pulumi.Input[str]]:
        """
        Immutable. The relative resource name of the VPC network on which the instance can be accessed. It is specified in the following form:projects/{project_number}/global/networks/{network_id}.
        """
        return pulumi.get(self, "network")

    @network.setter
    def network(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "network", value)

    @property
    @pulumi.getter(name="networkConfig")
    def network_config(self) -> Optional[pulumi.Input['NetworkConfigArgs']]:
        """
        The configuration specifying the network settings for the Dataproc Metastore service.
        """
        return pulumi.get(self, "network_config")

    @network_config.setter
    def network_config(self, value: Optional[pulumi.Input['NetworkConfigArgs']]):
        pulumi.set(self, "network_config", value)

    @property
    @pulumi.getter
    def port(self) -> Optional[pulumi.Input[int]]:
        """
        The TCP port at which the metastore service is reached. Default: 9083.
        """
        return pulumi.get(self, "port")

    @port.setter
    def port(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "port", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter(name="releaseChannel")
    def release_channel(self) -> Optional[pulumi.Input['ServiceReleaseChannel']]:
        """
        Immutable. The release channel of the service. If unspecified, defaults to STABLE.
        """
        return pulumi.get(self, "release_channel")

    @release_channel.setter
    def release_channel(self, value: Optional[pulumi.Input['ServiceReleaseChannel']]):
        pulumi.set(self, "release_channel", value)

    @property
    @pulumi.getter(name="requestId")
    def request_id(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. A request ID. Specify a unique request ID to allow the server to ignore the request if it has completed. The server will ignore subsequent requests that provide a duplicate request ID for at least 60 minutes after the first request.For example, if an initial request times out, followed by another request with the same request ID, the server ignores the second request to prevent the creation of duplicate commitments.The request ID must be a valid UUID (https://en.wikipedia.org/wiki/Universally_unique_identifier#Format) A zero UUID (00000000-0000-0000-0000-000000000000) is not supported.
        """
        return pulumi.get(self, "request_id")

    @request_id.setter
    def request_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "request_id", value)

    @property
    @pulumi.getter
    def tier(self) -> Optional[pulumi.Input['ServiceTier']]:
        """
        The tier of the service.
        """
        return pulumi.get(self, "tier")

    @tier.setter
    def tier(self, value: Optional[pulumi.Input['ServiceTier']]):
        pulumi.set(self, "tier", value)


class Service(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 database_type: Optional[pulumi.Input['ServiceDatabaseType']] = None,
                 encryption_config: Optional[pulumi.Input[pulumi.InputType['EncryptionConfigArgs']]] = None,
                 hive_metastore_config: Optional[pulumi.Input[pulumi.InputType['HiveMetastoreConfigArgs']]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 maintenance_window: Optional[pulumi.Input[pulumi.InputType['MaintenanceWindowArgs']]] = None,
                 metadata_integration: Optional[pulumi.Input[pulumi.InputType['MetadataIntegrationArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network: Optional[pulumi.Input[str]] = None,
                 network_config: Optional[pulumi.Input[pulumi.InputType['NetworkConfigArgs']]] = None,
                 port: Optional[pulumi.Input[int]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 release_channel: Optional[pulumi.Input['ServiceReleaseChannel']] = None,
                 request_id: Optional[pulumi.Input[str]] = None,
                 service_id: Optional[pulumi.Input[str]] = None,
                 tier: Optional[pulumi.Input['ServiceTier']] = None,
                 __props__=None):
        """
        Creates a metastore service in a project and location.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input['ServiceDatabaseType'] database_type: Immutable. The database type that the Metastore service stores its data.
        :param pulumi.Input[pulumi.InputType['EncryptionConfigArgs']] encryption_config: Immutable. Information used to configure the Dataproc Metastore service to encrypt customer data at rest. Cannot be updated.
        :param pulumi.Input[pulumi.InputType['HiveMetastoreConfigArgs']] hive_metastore_config: Configuration information specific to running Hive metastore software as the metastore service.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: User-defined labels for the metastore service.
        :param pulumi.Input[pulumi.InputType['MaintenanceWindowArgs']] maintenance_window: The one hour maintenance window of the metastore service. This specifies when the service can be restarted for maintenance purposes in UTC time. Maintenance window is not needed for services with the SPANNER database type.
        :param pulumi.Input[pulumi.InputType['MetadataIntegrationArgs']] metadata_integration: The setting that defines how metastore metadata should be integrated with external services and systems.
        :param pulumi.Input[str] name: Immutable. The relative resource name of the metastore service, in the following format:projects/{project_number}/locations/{location_id}/services/{service_id}.
        :param pulumi.Input[str] network: Immutable. The relative resource name of the VPC network on which the instance can be accessed. It is specified in the following form:projects/{project_number}/global/networks/{network_id}.
        :param pulumi.Input[pulumi.InputType['NetworkConfigArgs']] network_config: The configuration specifying the network settings for the Dataproc Metastore service.
        :param pulumi.Input[int] port: The TCP port at which the metastore service is reached. Default: 9083.
        :param pulumi.Input['ServiceReleaseChannel'] release_channel: Immutable. The release channel of the service. If unspecified, defaults to STABLE.
        :param pulumi.Input[str] request_id: Optional. A request ID. Specify a unique request ID to allow the server to ignore the request if it has completed. The server will ignore subsequent requests that provide a duplicate request ID for at least 60 minutes after the first request.For example, if an initial request times out, followed by another request with the same request ID, the server ignores the second request to prevent the creation of duplicate commitments.The request ID must be a valid UUID (https://en.wikipedia.org/wiki/Universally_unique_identifier#Format) A zero UUID (00000000-0000-0000-0000-000000000000) is not supported.
        :param pulumi.Input[str] service_id: Required. The ID of the metastore service, which is used as the final component of the metastore service's name.This value must be between 2 and 63 characters long inclusive, begin with a letter, end with a letter or number, and consist of alpha-numeric ASCII characters or hyphens.
        :param pulumi.Input['ServiceTier'] tier: The tier of the service.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ServiceArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Creates a metastore service in a project and location.

        :param str resource_name: The name of the resource.
        :param ServiceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ServiceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 database_type: Optional[pulumi.Input['ServiceDatabaseType']] = None,
                 encryption_config: Optional[pulumi.Input[pulumi.InputType['EncryptionConfigArgs']]] = None,
                 hive_metastore_config: Optional[pulumi.Input[pulumi.InputType['HiveMetastoreConfigArgs']]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 maintenance_window: Optional[pulumi.Input[pulumi.InputType['MaintenanceWindowArgs']]] = None,
                 metadata_integration: Optional[pulumi.Input[pulumi.InputType['MetadataIntegrationArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network: Optional[pulumi.Input[str]] = None,
                 network_config: Optional[pulumi.Input[pulumi.InputType['NetworkConfigArgs']]] = None,
                 port: Optional[pulumi.Input[int]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 release_channel: Optional[pulumi.Input['ServiceReleaseChannel']] = None,
                 request_id: Optional[pulumi.Input[str]] = None,
                 service_id: Optional[pulumi.Input[str]] = None,
                 tier: Optional[pulumi.Input['ServiceTier']] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ServiceArgs.__new__(ServiceArgs)

            __props__.__dict__["database_type"] = database_type
            __props__.__dict__["encryption_config"] = encryption_config
            __props__.__dict__["hive_metastore_config"] = hive_metastore_config
            __props__.__dict__["labels"] = labels
            __props__.__dict__["location"] = location
            __props__.__dict__["maintenance_window"] = maintenance_window
            __props__.__dict__["metadata_integration"] = metadata_integration
            __props__.__dict__["name"] = name
            __props__.__dict__["network"] = network
            __props__.__dict__["network_config"] = network_config
            __props__.__dict__["port"] = port
            __props__.__dict__["project"] = project
            __props__.__dict__["release_channel"] = release_channel
            __props__.__dict__["request_id"] = request_id
            if service_id is None and not opts.urn:
                raise TypeError("Missing required property 'service_id'")
            __props__.__dict__["service_id"] = service_id
            __props__.__dict__["tier"] = tier
            __props__.__dict__["artifact_gcs_uri"] = None
            __props__.__dict__["create_time"] = None
            __props__.__dict__["endpoint_uri"] = None
            __props__.__dict__["metadata_management_activity"] = None
            __props__.__dict__["state"] = None
            __props__.__dict__["state_message"] = None
            __props__.__dict__["uid"] = None
            __props__.__dict__["update_time"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["location", "project", "service_id"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Service, __self__).__init__(
            'google-native:metastore/v1alpha:Service',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Service':
        """
        Get an existing Service resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ServiceArgs.__new__(ServiceArgs)

        __props__.__dict__["artifact_gcs_uri"] = None
        __props__.__dict__["create_time"] = None
        __props__.__dict__["database_type"] = None
        __props__.__dict__["encryption_config"] = None
        __props__.__dict__["endpoint_uri"] = None
        __props__.__dict__["hive_metastore_config"] = None
        __props__.__dict__["labels"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["maintenance_window"] = None
        __props__.__dict__["metadata_integration"] = None
        __props__.__dict__["metadata_management_activity"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["network"] = None
        __props__.__dict__["network_config"] = None
        __props__.__dict__["port"] = None
        __props__.__dict__["project"] = None
        __props__.__dict__["release_channel"] = None
        __props__.__dict__["request_id"] = None
        __props__.__dict__["service_id"] = None
        __props__.__dict__["state"] = None
        __props__.__dict__["state_message"] = None
        __props__.__dict__["tier"] = None
        __props__.__dict__["uid"] = None
        __props__.__dict__["update_time"] = None
        return Service(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="artifactGcsUri")
    def artifact_gcs_uri(self) -> pulumi.Output[str]:
        """
        A Cloud Storage URI (starting with gs://) that specifies where artifacts related to the metastore service are stored.
        """
        return pulumi.get(self, "artifact_gcs_uri")

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> pulumi.Output[str]:
        """
        The time when the metastore service was created.
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter(name="databaseType")
    def database_type(self) -> pulumi.Output[str]:
        """
        Immutable. The database type that the Metastore service stores its data.
        """
        return pulumi.get(self, "database_type")

    @property
    @pulumi.getter(name="encryptionConfig")
    def encryption_config(self) -> pulumi.Output['outputs.EncryptionConfigResponse']:
        """
        Immutable. Information used to configure the Dataproc Metastore service to encrypt customer data at rest. Cannot be updated.
        """
        return pulumi.get(self, "encryption_config")

    @property
    @pulumi.getter(name="endpointUri")
    def endpoint_uri(self) -> pulumi.Output[str]:
        """
        The URI of the endpoint used to access the metastore service.
        """
        return pulumi.get(self, "endpoint_uri")

    @property
    @pulumi.getter(name="hiveMetastoreConfig")
    def hive_metastore_config(self) -> pulumi.Output['outputs.HiveMetastoreConfigResponse']:
        """
        Configuration information specific to running Hive metastore software as the metastore service.
        """
        return pulumi.get(self, "hive_metastore_config")

    @property
    @pulumi.getter
    def labels(self) -> pulumi.Output[Mapping[str, str]]:
        """
        User-defined labels for the metastore service.
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="maintenanceWindow")
    def maintenance_window(self) -> pulumi.Output['outputs.MaintenanceWindowResponse']:
        """
        The one hour maintenance window of the metastore service. This specifies when the service can be restarted for maintenance purposes in UTC time. Maintenance window is not needed for services with the SPANNER database type.
        """
        return pulumi.get(self, "maintenance_window")

    @property
    @pulumi.getter(name="metadataIntegration")
    def metadata_integration(self) -> pulumi.Output['outputs.MetadataIntegrationResponse']:
        """
        The setting that defines how metastore metadata should be integrated with external services and systems.
        """
        return pulumi.get(self, "metadata_integration")

    @property
    @pulumi.getter(name="metadataManagementActivity")
    def metadata_management_activity(self) -> pulumi.Output['outputs.MetadataManagementActivityResponse']:
        """
        The metadata management activities of the metastore service.
        """
        return pulumi.get(self, "metadata_management_activity")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Immutable. The relative resource name of the metastore service, in the following format:projects/{project_number}/locations/{location_id}/services/{service_id}.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def network(self) -> pulumi.Output[str]:
        """
        Immutable. The relative resource name of the VPC network on which the instance can be accessed. It is specified in the following form:projects/{project_number}/global/networks/{network_id}.
        """
        return pulumi.get(self, "network")

    @property
    @pulumi.getter(name="networkConfig")
    def network_config(self) -> pulumi.Output['outputs.NetworkConfigResponse']:
        """
        The configuration specifying the network settings for the Dataproc Metastore service.
        """
        return pulumi.get(self, "network_config")

    @property
    @pulumi.getter
    def port(self) -> pulumi.Output[int]:
        """
        The TCP port at which the metastore service is reached. Default: 9083.
        """
        return pulumi.get(self, "port")

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        return pulumi.get(self, "project")

    @property
    @pulumi.getter(name="releaseChannel")
    def release_channel(self) -> pulumi.Output[str]:
        """
        Immutable. The release channel of the service. If unspecified, defaults to STABLE.
        """
        return pulumi.get(self, "release_channel")

    @property
    @pulumi.getter(name="requestId")
    def request_id(self) -> pulumi.Output[Optional[str]]:
        """
        Optional. A request ID. Specify a unique request ID to allow the server to ignore the request if it has completed. The server will ignore subsequent requests that provide a duplicate request ID for at least 60 minutes after the first request.For example, if an initial request times out, followed by another request with the same request ID, the server ignores the second request to prevent the creation of duplicate commitments.The request ID must be a valid UUID (https://en.wikipedia.org/wiki/Universally_unique_identifier#Format) A zero UUID (00000000-0000-0000-0000-000000000000) is not supported.
        """
        return pulumi.get(self, "request_id")

    @property
    @pulumi.getter(name="serviceId")
    def service_id(self) -> pulumi.Output[str]:
        """
        Required. The ID of the metastore service, which is used as the final component of the metastore service's name.This value must be between 2 and 63 characters long inclusive, begin with a letter, end with a letter or number, and consist of alpha-numeric ASCII characters or hyphens.
        """
        return pulumi.get(self, "service_id")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        The current state of the metastore service.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter(name="stateMessage")
    def state_message(self) -> pulumi.Output[str]:
        """
        Additional information about the current state of the metastore service, if available.
        """
        return pulumi.get(self, "state_message")

    @property
    @pulumi.getter
    def tier(self) -> pulumi.Output[str]:
        """
        The tier of the service.
        """
        return pulumi.get(self, "tier")

    @property
    @pulumi.getter
    def uid(self) -> pulumi.Output[str]:
        """
        The globally unique resource identifier of the metastore service.
        """
        return pulumi.get(self, "uid")

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> pulumi.Output[str]:
        """
        The time when the metastore service was last updated.
        """
        return pulumi.get(self, "update_time")

