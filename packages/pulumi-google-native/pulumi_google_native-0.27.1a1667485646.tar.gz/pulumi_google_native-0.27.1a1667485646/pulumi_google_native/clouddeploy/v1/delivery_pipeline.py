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

__all__ = ['DeliveryPipelineArgs', 'DeliveryPipeline']

@pulumi.input_type
class DeliveryPipelineArgs:
    def __init__(__self__, *,
                 delivery_pipeline_id: pulumi.Input[str],
                 annotations: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 request_id: Optional[pulumi.Input[str]] = None,
                 serial_pipeline: Optional[pulumi.Input['SerialPipelineArgs']] = None,
                 suspended: Optional[pulumi.Input[bool]] = None,
                 validate_only: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a DeliveryPipeline resource.
        :param pulumi.Input[str] delivery_pipeline_id: Required. ID of the `DeliveryPipeline`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] annotations: User annotations. These attributes can only be set and used by the user, and not by Google Cloud Deploy.
        :param pulumi.Input[str] description: Description of the `DeliveryPipeline`. Max length is 255 characters.
        :param pulumi.Input[str] etag: This checksum is computed by the server based on the value of other fields, and may be sent on update and delete requests to ensure the client has an up-to-date value before proceeding.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Labels are attributes that can be set and used by both the user and by Google Cloud Deploy. Labels must meet the following constraints: * Keys and values can contain only lowercase letters, numeric characters, underscores, and dashes. * All characters must use UTF-8 encoding, and international characters are allowed. * Keys must start with a lowercase letter or international character. * Each resource is limited to a maximum of 64 labels. Both keys and values are additionally constrained to be <= 128 bytes.
        :param pulumi.Input[str] name: Optional. Name of the `DeliveryPipeline`. Format is projects/{project}/ locations/{location}/deliveryPipelines/a-z{0,62}.
        :param pulumi.Input[str] request_id: Optional. A request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. The server will guarantee that for at least 60 minutes since the first request. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported (00000000-0000-0000-0000-000000000000).
        :param pulumi.Input['SerialPipelineArgs'] serial_pipeline: SerialPipeline defines a sequential set of stages for a `DeliveryPipeline`.
        :param pulumi.Input[bool] suspended: When suspended, no new releases or rollouts can be created, but in-progress ones will complete.
        :param pulumi.Input[bool] validate_only: Optional. If set to true, the request is validated and the user is provided with an expected result, but no actual change is made.
        """
        pulumi.set(__self__, "delivery_pipeline_id", delivery_pipeline_id)
        if annotations is not None:
            pulumi.set(__self__, "annotations", annotations)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if etag is not None:
            pulumi.set(__self__, "etag", etag)
        if labels is not None:
            pulumi.set(__self__, "labels", labels)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if request_id is not None:
            pulumi.set(__self__, "request_id", request_id)
        if serial_pipeline is not None:
            pulumi.set(__self__, "serial_pipeline", serial_pipeline)
        if suspended is not None:
            pulumi.set(__self__, "suspended", suspended)
        if validate_only is not None:
            pulumi.set(__self__, "validate_only", validate_only)

    @property
    @pulumi.getter(name="deliveryPipelineId")
    def delivery_pipeline_id(self) -> pulumi.Input[str]:
        """
        Required. ID of the `DeliveryPipeline`.
        """
        return pulumi.get(self, "delivery_pipeline_id")

    @delivery_pipeline_id.setter
    def delivery_pipeline_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "delivery_pipeline_id", value)

    @property
    @pulumi.getter
    def annotations(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        User annotations. These attributes can only be set and used by the user, and not by Google Cloud Deploy.
        """
        return pulumi.get(self, "annotations")

    @annotations.setter
    def annotations(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "annotations", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of the `DeliveryPipeline`. Max length is 255 characters.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def etag(self) -> Optional[pulumi.Input[str]]:
        """
        This checksum is computed by the server based on the value of other fields, and may be sent on update and delete requests to ensure the client has an up-to-date value before proceeding.
        """
        return pulumi.get(self, "etag")

    @etag.setter
    def etag(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "etag", value)

    @property
    @pulumi.getter
    def labels(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Labels are attributes that can be set and used by both the user and by Google Cloud Deploy. Labels must meet the following constraints: * Keys and values can contain only lowercase letters, numeric characters, underscores, and dashes. * All characters must use UTF-8 encoding, and international characters are allowed. * Keys must start with a lowercase letter or international character. * Each resource is limited to a maximum of 64 labels. Both keys and values are additionally constrained to be <= 128 bytes.
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
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. Name of the `DeliveryPipeline`. Format is projects/{project}/ locations/{location}/deliveryPipelines/a-z{0,62}.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

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
        Optional. A request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. The server will guarantee that for at least 60 minutes since the first request. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported (00000000-0000-0000-0000-000000000000).
        """
        return pulumi.get(self, "request_id")

    @request_id.setter
    def request_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "request_id", value)

    @property
    @pulumi.getter(name="serialPipeline")
    def serial_pipeline(self) -> Optional[pulumi.Input['SerialPipelineArgs']]:
        """
        SerialPipeline defines a sequential set of stages for a `DeliveryPipeline`.
        """
        return pulumi.get(self, "serial_pipeline")

    @serial_pipeline.setter
    def serial_pipeline(self, value: Optional[pulumi.Input['SerialPipelineArgs']]):
        pulumi.set(self, "serial_pipeline", value)

    @property
    @pulumi.getter
    def suspended(self) -> Optional[pulumi.Input[bool]]:
        """
        When suspended, no new releases or rollouts can be created, but in-progress ones will complete.
        """
        return pulumi.get(self, "suspended")

    @suspended.setter
    def suspended(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "suspended", value)

    @property
    @pulumi.getter(name="validateOnly")
    def validate_only(self) -> Optional[pulumi.Input[bool]]:
        """
        Optional. If set to true, the request is validated and the user is provided with an expected result, but no actual change is made.
        """
        return pulumi.get(self, "validate_only")

    @validate_only.setter
    def validate_only(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "validate_only", value)


class DeliveryPipeline(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 annotations: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 delivery_pipeline_id: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 request_id: Optional[pulumi.Input[str]] = None,
                 serial_pipeline: Optional[pulumi.Input[pulumi.InputType['SerialPipelineArgs']]] = None,
                 suspended: Optional[pulumi.Input[bool]] = None,
                 validate_only: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        """
        Creates a new DeliveryPipeline in a given project and location.
        Auto-naming is currently not supported for this resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] annotations: User annotations. These attributes can only be set and used by the user, and not by Google Cloud Deploy.
        :param pulumi.Input[str] delivery_pipeline_id: Required. ID of the `DeliveryPipeline`.
        :param pulumi.Input[str] description: Description of the `DeliveryPipeline`. Max length is 255 characters.
        :param pulumi.Input[str] etag: This checksum is computed by the server based on the value of other fields, and may be sent on update and delete requests to ensure the client has an up-to-date value before proceeding.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Labels are attributes that can be set and used by both the user and by Google Cloud Deploy. Labels must meet the following constraints: * Keys and values can contain only lowercase letters, numeric characters, underscores, and dashes. * All characters must use UTF-8 encoding, and international characters are allowed. * Keys must start with a lowercase letter or international character. * Each resource is limited to a maximum of 64 labels. Both keys and values are additionally constrained to be <= 128 bytes.
        :param pulumi.Input[str] name: Optional. Name of the `DeliveryPipeline`. Format is projects/{project}/ locations/{location}/deliveryPipelines/a-z{0,62}.
        :param pulumi.Input[str] request_id: Optional. A request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. The server will guarantee that for at least 60 minutes since the first request. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported (00000000-0000-0000-0000-000000000000).
        :param pulumi.Input[pulumi.InputType['SerialPipelineArgs']] serial_pipeline: SerialPipeline defines a sequential set of stages for a `DeliveryPipeline`.
        :param pulumi.Input[bool] suspended: When suspended, no new releases or rollouts can be created, but in-progress ones will complete.
        :param pulumi.Input[bool] validate_only: Optional. If set to true, the request is validated and the user is provided with an expected result, but no actual change is made.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DeliveryPipelineArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Creates a new DeliveryPipeline in a given project and location.
        Auto-naming is currently not supported for this resource.

        :param str resource_name: The name of the resource.
        :param DeliveryPipelineArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DeliveryPipelineArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 annotations: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 delivery_pipeline_id: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 request_id: Optional[pulumi.Input[str]] = None,
                 serial_pipeline: Optional[pulumi.Input[pulumi.InputType['SerialPipelineArgs']]] = None,
                 suspended: Optional[pulumi.Input[bool]] = None,
                 validate_only: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DeliveryPipelineArgs.__new__(DeliveryPipelineArgs)

            __props__.__dict__["annotations"] = annotations
            if delivery_pipeline_id is None and not opts.urn:
                raise TypeError("Missing required property 'delivery_pipeline_id'")
            __props__.__dict__["delivery_pipeline_id"] = delivery_pipeline_id
            __props__.__dict__["description"] = description
            __props__.__dict__["etag"] = etag
            __props__.__dict__["labels"] = labels
            __props__.__dict__["location"] = location
            __props__.__dict__["name"] = name
            __props__.__dict__["project"] = project
            __props__.__dict__["request_id"] = request_id
            __props__.__dict__["serial_pipeline"] = serial_pipeline
            __props__.__dict__["suspended"] = suspended
            __props__.__dict__["validate_only"] = validate_only
            __props__.__dict__["condition"] = None
            __props__.__dict__["create_time"] = None
            __props__.__dict__["uid"] = None
            __props__.__dict__["update_time"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["delivery_pipeline_id", "location", "project"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(DeliveryPipeline, __self__).__init__(
            'google-native:clouddeploy/v1:DeliveryPipeline',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'DeliveryPipeline':
        """
        Get an existing DeliveryPipeline resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = DeliveryPipelineArgs.__new__(DeliveryPipelineArgs)

        __props__.__dict__["annotations"] = None
        __props__.__dict__["condition"] = None
        __props__.__dict__["create_time"] = None
        __props__.__dict__["delivery_pipeline_id"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["etag"] = None
        __props__.__dict__["labels"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["project"] = None
        __props__.__dict__["request_id"] = None
        __props__.__dict__["serial_pipeline"] = None
        __props__.__dict__["suspended"] = None
        __props__.__dict__["uid"] = None
        __props__.__dict__["update_time"] = None
        __props__.__dict__["validate_only"] = None
        return DeliveryPipeline(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def annotations(self) -> pulumi.Output[Mapping[str, str]]:
        """
        User annotations. These attributes can only be set and used by the user, and not by Google Cloud Deploy.
        """
        return pulumi.get(self, "annotations")

    @property
    @pulumi.getter
    def condition(self) -> pulumi.Output['outputs.PipelineConditionResponse']:
        """
        Information around the state of the Delivery Pipeline.
        """
        return pulumi.get(self, "condition")

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> pulumi.Output[str]:
        """
        Time at which the pipeline was created.
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter(name="deliveryPipelineId")
    def delivery_pipeline_id(self) -> pulumi.Output[str]:
        """
        Required. ID of the `DeliveryPipeline`.
        """
        return pulumi.get(self, "delivery_pipeline_id")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[str]:
        """
        Description of the `DeliveryPipeline`. Max length is 255 characters.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        This checksum is computed by the server based on the value of other fields, and may be sent on update and delete requests to ensure the client has an up-to-date value before proceeding.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def labels(self) -> pulumi.Output[Mapping[str, str]]:
        """
        Labels are attributes that can be set and used by both the user and by Google Cloud Deploy. Labels must meet the following constraints: * Keys and values can contain only lowercase letters, numeric characters, underscores, and dashes. * All characters must use UTF-8 encoding, and international characters are allowed. * Keys must start with a lowercase letter or international character. * Each resource is limited to a maximum of 64 labels. Both keys and values are additionally constrained to be <= 128 bytes.
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Optional. Name of the `DeliveryPipeline`. Format is projects/{project}/ locations/{location}/deliveryPipelines/a-z{0,62}.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        return pulumi.get(self, "project")

    @property
    @pulumi.getter(name="requestId")
    def request_id(self) -> pulumi.Output[Optional[str]]:
        """
        Optional. A request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. The server will guarantee that for at least 60 minutes since the first request. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported (00000000-0000-0000-0000-000000000000).
        """
        return pulumi.get(self, "request_id")

    @property
    @pulumi.getter(name="serialPipeline")
    def serial_pipeline(self) -> pulumi.Output['outputs.SerialPipelineResponse']:
        """
        SerialPipeline defines a sequential set of stages for a `DeliveryPipeline`.
        """
        return pulumi.get(self, "serial_pipeline")

    @property
    @pulumi.getter
    def suspended(self) -> pulumi.Output[bool]:
        """
        When suspended, no new releases or rollouts can be created, but in-progress ones will complete.
        """
        return pulumi.get(self, "suspended")

    @property
    @pulumi.getter
    def uid(self) -> pulumi.Output[str]:
        """
        Unique identifier of the `DeliveryPipeline`.
        """
        return pulumi.get(self, "uid")

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> pulumi.Output[str]:
        """
        Most recent time at which the pipeline was updated.
        """
        return pulumi.get(self, "update_time")

    @property
    @pulumi.getter(name="validateOnly")
    def validate_only(self) -> pulumi.Output[Optional[bool]]:
        """
        Optional. If set to true, the request is validated and the user is provided with an expected result, but no actual change is made.
        """
        return pulumi.get(self, "validate_only")

