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

__all__ = ['DocumentArgs', 'Document']

@pulumi.input_type
class DocumentArgs:
    def __init__(__self__, *,
                 display_name: pulumi.Input[str],
                 async_enabled: Optional[pulumi.Input[bool]] = None,
                 cloud_ai_document: Optional[pulumi.Input['GoogleCloudDocumentaiV1DocumentArgs']] = None,
                 cloud_ai_document_option: Optional[pulumi.Input['GoogleCloudContentwarehouseV1CloudAIDocumentOptionArgs']] = None,
                 create_mask: Optional[pulumi.Input[str]] = None,
                 creator: Optional[pulumi.Input[str]] = None,
                 display_uri: Optional[pulumi.Input[str]] = None,
                 document_schema_name: Optional[pulumi.Input[str]] = None,
                 inline_raw_document: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 plain_text: Optional[pulumi.Input[str]] = None,
                 policy: Optional[pulumi.Input['GoogleIamV1PolicyArgs']] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[Sequence[pulumi.Input['GoogleCloudContentwarehouseV1PropertyArgs']]]] = None,
                 raw_document_file_type: Optional[pulumi.Input['DocumentRawDocumentFileType']] = None,
                 raw_document_path: Optional[pulumi.Input[str]] = None,
                 reference_id: Optional[pulumi.Input[str]] = None,
                 request_metadata: Optional[pulumi.Input['GoogleCloudContentwarehouseV1RequestMetadataArgs']] = None,
                 structured_content_uri: Optional[pulumi.Input[str]] = None,
                 text_extraction_disabled: Optional[pulumi.Input[bool]] = None,
                 title: Optional[pulumi.Input[str]] = None,
                 updater: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Document resource.
        :param pulumi.Input[str] display_name: Display name of the document given by the user. This name will be displayed in the UI. Customer can populate this field with the name of the document. This differs from the 'title' field as 'title' is optional and stores the top heading in the document.
        :param pulumi.Input[bool] async_enabled: If true, makes the document visible to asynchronous policies and rules.
        :param pulumi.Input['GoogleCloudDocumentaiV1DocumentArgs'] cloud_ai_document: Document AI format to save the structured content, including OCR.
        :param pulumi.Input['GoogleCloudContentwarehouseV1CloudAIDocumentOptionArgs'] cloud_ai_document_option: Request Option for processing Cloud AI Document in CW Document.
        :param pulumi.Input[str] create_mask: Field mask for creating Document fields. If mask path is empty, it means all fields are masked. For the `FieldMask` definition, see https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#fieldmask
        :param pulumi.Input[str] creator: The user who creates the document.
        :param pulumi.Input[str] display_uri: Uri to display the document, for example, in the UI.
        :param pulumi.Input[str] document_schema_name: The Document schema name. Format: projects/{project_number}/locations/{location}/documentSchemas/{document_schema_id}.
        :param pulumi.Input[str] inline_raw_document: Raw document content.
        :param pulumi.Input[str] name: The resource name of the document. Format: projects/{project_number}/locations/{location}/documents/{document_id}. The name is ignored when creating a document.
        :param pulumi.Input[str] plain_text: Other document format, such as PPTX, XLXS
        :param pulumi.Input['GoogleIamV1PolicyArgs'] policy: Default document policy during creation. Conditions defined in the policy will be ignored.
        :param pulumi.Input[Sequence[pulumi.Input['GoogleCloudContentwarehouseV1PropertyArgs']]] properties: List of values that are user supplied metadata.
        :param pulumi.Input['DocumentRawDocumentFileType'] raw_document_file_type: This is used when DocAI was not used to load the document and parsing/ extracting is needed for the inline_raw_document. For example, if inline_raw_document is the byte representation of a PDF file, then this should be set to: RAW_DOCUMENT_FILE_TYPE_PDF.
        :param pulumi.Input[str] raw_document_path: Raw document file in Cloud Storage path.
        :param pulumi.Input[str] reference_id: The reference ID set by customers. Must be unique per project and location.
        :param pulumi.Input['GoogleCloudContentwarehouseV1RequestMetadataArgs'] request_metadata: The meta information collected about the end user, used to enforce access control for the service.
        :param pulumi.Input[str] structured_content_uri: A path linked to structured content file.
        :param pulumi.Input[bool] text_extraction_disabled: If true, text extraction will not be performed.
        :param pulumi.Input[str] title: Title that describes the document. This is usually present in the top section of the document, and is a mandatory field for the question-answering feature.
        :param pulumi.Input[str] updater: The user who lastly updates the document.
        """
        pulumi.set(__self__, "display_name", display_name)
        if async_enabled is not None:
            pulumi.set(__self__, "async_enabled", async_enabled)
        if cloud_ai_document is not None:
            pulumi.set(__self__, "cloud_ai_document", cloud_ai_document)
        if cloud_ai_document_option is not None:
            pulumi.set(__self__, "cloud_ai_document_option", cloud_ai_document_option)
        if create_mask is not None:
            pulumi.set(__self__, "create_mask", create_mask)
        if creator is not None:
            pulumi.set(__self__, "creator", creator)
        if display_uri is not None:
            pulumi.set(__self__, "display_uri", display_uri)
        if document_schema_name is not None:
            pulumi.set(__self__, "document_schema_name", document_schema_name)
        if inline_raw_document is not None:
            pulumi.set(__self__, "inline_raw_document", inline_raw_document)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if plain_text is not None:
            pulumi.set(__self__, "plain_text", plain_text)
        if policy is not None:
            pulumi.set(__self__, "policy", policy)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if properties is not None:
            pulumi.set(__self__, "properties", properties)
        if raw_document_file_type is not None:
            pulumi.set(__self__, "raw_document_file_type", raw_document_file_type)
        if raw_document_path is not None:
            pulumi.set(__self__, "raw_document_path", raw_document_path)
        if reference_id is not None:
            pulumi.set(__self__, "reference_id", reference_id)
        if request_metadata is not None:
            pulumi.set(__self__, "request_metadata", request_metadata)
        if structured_content_uri is not None:
            pulumi.set(__self__, "structured_content_uri", structured_content_uri)
        if text_extraction_disabled is not None:
            pulumi.set(__self__, "text_extraction_disabled", text_extraction_disabled)
        if title is not None:
            pulumi.set(__self__, "title", title)
        if updater is not None:
            pulumi.set(__self__, "updater", updater)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Input[str]:
        """
        Display name of the document given by the user. This name will be displayed in the UI. Customer can populate this field with the name of the document. This differs from the 'title' field as 'title' is optional and stores the top heading in the document.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter(name="asyncEnabled")
    def async_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        If true, makes the document visible to asynchronous policies and rules.
        """
        return pulumi.get(self, "async_enabled")

    @async_enabled.setter
    def async_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "async_enabled", value)

    @property
    @pulumi.getter(name="cloudAiDocument")
    def cloud_ai_document(self) -> Optional[pulumi.Input['GoogleCloudDocumentaiV1DocumentArgs']]:
        """
        Document AI format to save the structured content, including OCR.
        """
        return pulumi.get(self, "cloud_ai_document")

    @cloud_ai_document.setter
    def cloud_ai_document(self, value: Optional[pulumi.Input['GoogleCloudDocumentaiV1DocumentArgs']]):
        pulumi.set(self, "cloud_ai_document", value)

    @property
    @pulumi.getter(name="cloudAiDocumentOption")
    def cloud_ai_document_option(self) -> Optional[pulumi.Input['GoogleCloudContentwarehouseV1CloudAIDocumentOptionArgs']]:
        """
        Request Option for processing Cloud AI Document in CW Document.
        """
        return pulumi.get(self, "cloud_ai_document_option")

    @cloud_ai_document_option.setter
    def cloud_ai_document_option(self, value: Optional[pulumi.Input['GoogleCloudContentwarehouseV1CloudAIDocumentOptionArgs']]):
        pulumi.set(self, "cloud_ai_document_option", value)

    @property
    @pulumi.getter(name="createMask")
    def create_mask(self) -> Optional[pulumi.Input[str]]:
        """
        Field mask for creating Document fields. If mask path is empty, it means all fields are masked. For the `FieldMask` definition, see https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#fieldmask
        """
        return pulumi.get(self, "create_mask")

    @create_mask.setter
    def create_mask(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "create_mask", value)

    @property
    @pulumi.getter
    def creator(self) -> Optional[pulumi.Input[str]]:
        """
        The user who creates the document.
        """
        return pulumi.get(self, "creator")

    @creator.setter
    def creator(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "creator", value)

    @property
    @pulumi.getter(name="displayUri")
    def display_uri(self) -> Optional[pulumi.Input[str]]:
        """
        Uri to display the document, for example, in the UI.
        """
        return pulumi.get(self, "display_uri")

    @display_uri.setter
    def display_uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "display_uri", value)

    @property
    @pulumi.getter(name="documentSchemaName")
    def document_schema_name(self) -> Optional[pulumi.Input[str]]:
        """
        The Document schema name. Format: projects/{project_number}/locations/{location}/documentSchemas/{document_schema_id}.
        """
        return pulumi.get(self, "document_schema_name")

    @document_schema_name.setter
    def document_schema_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "document_schema_name", value)

    @property
    @pulumi.getter(name="inlineRawDocument")
    def inline_raw_document(self) -> Optional[pulumi.Input[str]]:
        """
        Raw document content.
        """
        return pulumi.get(self, "inline_raw_document")

    @inline_raw_document.setter
    def inline_raw_document(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "inline_raw_document", value)

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
        The resource name of the document. Format: projects/{project_number}/locations/{location}/documents/{document_id}. The name is ignored when creating a document.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="plainText")
    def plain_text(self) -> Optional[pulumi.Input[str]]:
        """
        Other document format, such as PPTX, XLXS
        """
        return pulumi.get(self, "plain_text")

    @plain_text.setter
    def plain_text(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "plain_text", value)

    @property
    @pulumi.getter
    def policy(self) -> Optional[pulumi.Input['GoogleIamV1PolicyArgs']]:
        """
        Default document policy during creation. Conditions defined in the policy will be ignored.
        """
        return pulumi.get(self, "policy")

    @policy.setter
    def policy(self, value: Optional[pulumi.Input['GoogleIamV1PolicyArgs']]):
        pulumi.set(self, "policy", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter
    def properties(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['GoogleCloudContentwarehouseV1PropertyArgs']]]]:
        """
        List of values that are user supplied metadata.
        """
        return pulumi.get(self, "properties")

    @properties.setter
    def properties(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['GoogleCloudContentwarehouseV1PropertyArgs']]]]):
        pulumi.set(self, "properties", value)

    @property
    @pulumi.getter(name="rawDocumentFileType")
    def raw_document_file_type(self) -> Optional[pulumi.Input['DocumentRawDocumentFileType']]:
        """
        This is used when DocAI was not used to load the document and parsing/ extracting is needed for the inline_raw_document. For example, if inline_raw_document is the byte representation of a PDF file, then this should be set to: RAW_DOCUMENT_FILE_TYPE_PDF.
        """
        return pulumi.get(self, "raw_document_file_type")

    @raw_document_file_type.setter
    def raw_document_file_type(self, value: Optional[pulumi.Input['DocumentRawDocumentFileType']]):
        pulumi.set(self, "raw_document_file_type", value)

    @property
    @pulumi.getter(name="rawDocumentPath")
    def raw_document_path(self) -> Optional[pulumi.Input[str]]:
        """
        Raw document file in Cloud Storage path.
        """
        return pulumi.get(self, "raw_document_path")

    @raw_document_path.setter
    def raw_document_path(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "raw_document_path", value)

    @property
    @pulumi.getter(name="referenceId")
    def reference_id(self) -> Optional[pulumi.Input[str]]:
        """
        The reference ID set by customers. Must be unique per project and location.
        """
        return pulumi.get(self, "reference_id")

    @reference_id.setter
    def reference_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "reference_id", value)

    @property
    @pulumi.getter(name="requestMetadata")
    def request_metadata(self) -> Optional[pulumi.Input['GoogleCloudContentwarehouseV1RequestMetadataArgs']]:
        """
        The meta information collected about the end user, used to enforce access control for the service.
        """
        return pulumi.get(self, "request_metadata")

    @request_metadata.setter
    def request_metadata(self, value: Optional[pulumi.Input['GoogleCloudContentwarehouseV1RequestMetadataArgs']]):
        pulumi.set(self, "request_metadata", value)

    @property
    @pulumi.getter(name="structuredContentUri")
    def structured_content_uri(self) -> Optional[pulumi.Input[str]]:
        """
        A path linked to structured content file.
        """
        return pulumi.get(self, "structured_content_uri")

    @structured_content_uri.setter
    def structured_content_uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "structured_content_uri", value)

    @property
    @pulumi.getter(name="textExtractionDisabled")
    def text_extraction_disabled(self) -> Optional[pulumi.Input[bool]]:
        """
        If true, text extraction will not be performed.
        """
        return pulumi.get(self, "text_extraction_disabled")

    @text_extraction_disabled.setter
    def text_extraction_disabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "text_extraction_disabled", value)

    @property
    @pulumi.getter
    def title(self) -> Optional[pulumi.Input[str]]:
        """
        Title that describes the document. This is usually present in the top section of the document, and is a mandatory field for the question-answering feature.
        """
        return pulumi.get(self, "title")

    @title.setter
    def title(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "title", value)

    @property
    @pulumi.getter
    def updater(self) -> Optional[pulumi.Input[str]]:
        """
        The user who lastly updates the document.
        """
        return pulumi.get(self, "updater")

    @updater.setter
    def updater(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "updater", value)


class Document(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 async_enabled: Optional[pulumi.Input[bool]] = None,
                 cloud_ai_document: Optional[pulumi.Input[pulumi.InputType['GoogleCloudDocumentaiV1DocumentArgs']]] = None,
                 cloud_ai_document_option: Optional[pulumi.Input[pulumi.InputType['GoogleCloudContentwarehouseV1CloudAIDocumentOptionArgs']]] = None,
                 create_mask: Optional[pulumi.Input[str]] = None,
                 creator: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 display_uri: Optional[pulumi.Input[str]] = None,
                 document_schema_name: Optional[pulumi.Input[str]] = None,
                 inline_raw_document: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 plain_text: Optional[pulumi.Input[str]] = None,
                 policy: Optional[pulumi.Input[pulumi.InputType['GoogleIamV1PolicyArgs']]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['GoogleCloudContentwarehouseV1PropertyArgs']]]]] = None,
                 raw_document_file_type: Optional[pulumi.Input['DocumentRawDocumentFileType']] = None,
                 raw_document_path: Optional[pulumi.Input[str]] = None,
                 reference_id: Optional[pulumi.Input[str]] = None,
                 request_metadata: Optional[pulumi.Input[pulumi.InputType['GoogleCloudContentwarehouseV1RequestMetadataArgs']]] = None,
                 structured_content_uri: Optional[pulumi.Input[str]] = None,
                 text_extraction_disabled: Optional[pulumi.Input[bool]] = None,
                 title: Optional[pulumi.Input[str]] = None,
                 updater: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Creates a document.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] async_enabled: If true, makes the document visible to asynchronous policies and rules.
        :param pulumi.Input[pulumi.InputType['GoogleCloudDocumentaiV1DocumentArgs']] cloud_ai_document: Document AI format to save the structured content, including OCR.
        :param pulumi.Input[pulumi.InputType['GoogleCloudContentwarehouseV1CloudAIDocumentOptionArgs']] cloud_ai_document_option: Request Option for processing Cloud AI Document in CW Document.
        :param pulumi.Input[str] create_mask: Field mask for creating Document fields. If mask path is empty, it means all fields are masked. For the `FieldMask` definition, see https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#fieldmask
        :param pulumi.Input[str] creator: The user who creates the document.
        :param pulumi.Input[str] display_name: Display name of the document given by the user. This name will be displayed in the UI. Customer can populate this field with the name of the document. This differs from the 'title' field as 'title' is optional and stores the top heading in the document.
        :param pulumi.Input[str] display_uri: Uri to display the document, for example, in the UI.
        :param pulumi.Input[str] document_schema_name: The Document schema name. Format: projects/{project_number}/locations/{location}/documentSchemas/{document_schema_id}.
        :param pulumi.Input[str] inline_raw_document: Raw document content.
        :param pulumi.Input[str] name: The resource name of the document. Format: projects/{project_number}/locations/{location}/documents/{document_id}. The name is ignored when creating a document.
        :param pulumi.Input[str] plain_text: Other document format, such as PPTX, XLXS
        :param pulumi.Input[pulumi.InputType['GoogleIamV1PolicyArgs']] policy: Default document policy during creation. Conditions defined in the policy will be ignored.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['GoogleCloudContentwarehouseV1PropertyArgs']]]] properties: List of values that are user supplied metadata.
        :param pulumi.Input['DocumentRawDocumentFileType'] raw_document_file_type: This is used when DocAI was not used to load the document and parsing/ extracting is needed for the inline_raw_document. For example, if inline_raw_document is the byte representation of a PDF file, then this should be set to: RAW_DOCUMENT_FILE_TYPE_PDF.
        :param pulumi.Input[str] raw_document_path: Raw document file in Cloud Storage path.
        :param pulumi.Input[str] reference_id: The reference ID set by customers. Must be unique per project and location.
        :param pulumi.Input[pulumi.InputType['GoogleCloudContentwarehouseV1RequestMetadataArgs']] request_metadata: The meta information collected about the end user, used to enforce access control for the service.
        :param pulumi.Input[str] structured_content_uri: A path linked to structured content file.
        :param pulumi.Input[bool] text_extraction_disabled: If true, text extraction will not be performed.
        :param pulumi.Input[str] title: Title that describes the document. This is usually present in the top section of the document, and is a mandatory field for the question-answering feature.
        :param pulumi.Input[str] updater: The user who lastly updates the document.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DocumentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Creates a document.

        :param str resource_name: The name of the resource.
        :param DocumentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DocumentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 async_enabled: Optional[pulumi.Input[bool]] = None,
                 cloud_ai_document: Optional[pulumi.Input[pulumi.InputType['GoogleCloudDocumentaiV1DocumentArgs']]] = None,
                 cloud_ai_document_option: Optional[pulumi.Input[pulumi.InputType['GoogleCloudContentwarehouseV1CloudAIDocumentOptionArgs']]] = None,
                 create_mask: Optional[pulumi.Input[str]] = None,
                 creator: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 display_uri: Optional[pulumi.Input[str]] = None,
                 document_schema_name: Optional[pulumi.Input[str]] = None,
                 inline_raw_document: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 plain_text: Optional[pulumi.Input[str]] = None,
                 policy: Optional[pulumi.Input[pulumi.InputType['GoogleIamV1PolicyArgs']]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['GoogleCloudContentwarehouseV1PropertyArgs']]]]] = None,
                 raw_document_file_type: Optional[pulumi.Input['DocumentRawDocumentFileType']] = None,
                 raw_document_path: Optional[pulumi.Input[str]] = None,
                 reference_id: Optional[pulumi.Input[str]] = None,
                 request_metadata: Optional[pulumi.Input[pulumi.InputType['GoogleCloudContentwarehouseV1RequestMetadataArgs']]] = None,
                 structured_content_uri: Optional[pulumi.Input[str]] = None,
                 text_extraction_disabled: Optional[pulumi.Input[bool]] = None,
                 title: Optional[pulumi.Input[str]] = None,
                 updater: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DocumentArgs.__new__(DocumentArgs)

            __props__.__dict__["async_enabled"] = async_enabled
            __props__.__dict__["cloud_ai_document"] = cloud_ai_document
            __props__.__dict__["cloud_ai_document_option"] = cloud_ai_document_option
            __props__.__dict__["create_mask"] = create_mask
            __props__.__dict__["creator"] = creator
            if display_name is None and not opts.urn:
                raise TypeError("Missing required property 'display_name'")
            __props__.__dict__["display_name"] = display_name
            __props__.__dict__["display_uri"] = display_uri
            __props__.__dict__["document_schema_name"] = document_schema_name
            __props__.__dict__["inline_raw_document"] = inline_raw_document
            __props__.__dict__["location"] = location
            __props__.__dict__["name"] = name
            __props__.__dict__["plain_text"] = plain_text
            __props__.__dict__["policy"] = policy
            __props__.__dict__["project"] = project
            __props__.__dict__["properties"] = properties
            __props__.__dict__["raw_document_file_type"] = raw_document_file_type
            __props__.__dict__["raw_document_path"] = raw_document_path
            __props__.__dict__["reference_id"] = reference_id
            __props__.__dict__["request_metadata"] = request_metadata
            __props__.__dict__["structured_content_uri"] = structured_content_uri
            __props__.__dict__["text_extraction_disabled"] = text_extraction_disabled
            __props__.__dict__["title"] = title
            __props__.__dict__["updater"] = updater
            __props__.__dict__["create_time"] = None
            __props__.__dict__["update_time"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["location", "project"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Document, __self__).__init__(
            'google-native:contentwarehouse/v1:Document',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Document':
        """
        Get an existing Document resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = DocumentArgs.__new__(DocumentArgs)

        __props__.__dict__["async_enabled"] = None
        __props__.__dict__["cloud_ai_document"] = None
        __props__.__dict__["create_time"] = None
        __props__.__dict__["creator"] = None
        __props__.__dict__["display_name"] = None
        __props__.__dict__["display_uri"] = None
        __props__.__dict__["document_schema_name"] = None
        __props__.__dict__["inline_raw_document"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["plain_text"] = None
        __props__.__dict__["project"] = None
        __props__.__dict__["properties"] = None
        __props__.__dict__["raw_document_file_type"] = None
        __props__.__dict__["raw_document_path"] = None
        __props__.__dict__["reference_id"] = None
        __props__.__dict__["structured_content_uri"] = None
        __props__.__dict__["text_extraction_disabled"] = None
        __props__.__dict__["title"] = None
        __props__.__dict__["update_time"] = None
        __props__.__dict__["updater"] = None
        return Document(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="asyncEnabled")
    def async_enabled(self) -> pulumi.Output[bool]:
        """
        If true, makes the document visible to asynchronous policies and rules.
        """
        return pulumi.get(self, "async_enabled")

    @property
    @pulumi.getter(name="cloudAiDocument")
    def cloud_ai_document(self) -> pulumi.Output['outputs.GoogleCloudDocumentaiV1DocumentResponse']:
        """
        Document AI format to save the structured content, including OCR.
        """
        return pulumi.get(self, "cloud_ai_document")

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> pulumi.Output[str]:
        """
        The time when the document is created.
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter
    def creator(self) -> pulumi.Output[str]:
        """
        The user who creates the document.
        """
        return pulumi.get(self, "creator")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[str]:
        """
        Display name of the document given by the user. This name will be displayed in the UI. Customer can populate this field with the name of the document. This differs from the 'title' field as 'title' is optional and stores the top heading in the document.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter(name="displayUri")
    def display_uri(self) -> pulumi.Output[str]:
        """
        Uri to display the document, for example, in the UI.
        """
        return pulumi.get(self, "display_uri")

    @property
    @pulumi.getter(name="documentSchemaName")
    def document_schema_name(self) -> pulumi.Output[str]:
        """
        The Document schema name. Format: projects/{project_number}/locations/{location}/documentSchemas/{document_schema_id}.
        """
        return pulumi.get(self, "document_schema_name")

    @property
    @pulumi.getter(name="inlineRawDocument")
    def inline_raw_document(self) -> pulumi.Output[str]:
        """
        Raw document content.
        """
        return pulumi.get(self, "inline_raw_document")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The resource name of the document. Format: projects/{project_number}/locations/{location}/documents/{document_id}. The name is ignored when creating a document.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="plainText")
    def plain_text(self) -> pulumi.Output[str]:
        """
        Other document format, such as PPTX, XLXS
        """
        return pulumi.get(self, "plain_text")

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        return pulumi.get(self, "project")

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Output[Sequence['outputs.GoogleCloudContentwarehouseV1PropertyResponse']]:
        """
        List of values that are user supplied metadata.
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter(name="rawDocumentFileType")
    def raw_document_file_type(self) -> pulumi.Output[str]:
        """
        This is used when DocAI was not used to load the document and parsing/ extracting is needed for the inline_raw_document. For example, if inline_raw_document is the byte representation of a PDF file, then this should be set to: RAW_DOCUMENT_FILE_TYPE_PDF.
        """
        return pulumi.get(self, "raw_document_file_type")

    @property
    @pulumi.getter(name="rawDocumentPath")
    def raw_document_path(self) -> pulumi.Output[str]:
        """
        Raw document file in Cloud Storage path.
        """
        return pulumi.get(self, "raw_document_path")

    @property
    @pulumi.getter(name="referenceId")
    def reference_id(self) -> pulumi.Output[str]:
        """
        The reference ID set by customers. Must be unique per project and location.
        """
        return pulumi.get(self, "reference_id")

    @property
    @pulumi.getter(name="structuredContentUri")
    def structured_content_uri(self) -> pulumi.Output[str]:
        """
        A path linked to structured content file.
        """
        return pulumi.get(self, "structured_content_uri")

    @property
    @pulumi.getter(name="textExtractionDisabled")
    def text_extraction_disabled(self) -> pulumi.Output[bool]:
        """
        If true, text extraction will not be performed.
        """
        return pulumi.get(self, "text_extraction_disabled")

    @property
    @pulumi.getter
    def title(self) -> pulumi.Output[str]:
        """
        Title that describes the document. This is usually present in the top section of the document, and is a mandatory field for the question-answering feature.
        """
        return pulumi.get(self, "title")

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> pulumi.Output[str]:
        """
        The time when the document is last updated.
        """
        return pulumi.get(self, "update_time")

    @property
    @pulumi.getter
    def updater(self) -> pulumi.Output[str]:
        """
        The user who lastly updates the document.
        """
        return pulumi.get(self, "updater")

