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

__all__ = [
    'CertificateProviderInstanceResponse',
    'DestinationResponse',
    'ExprResponse',
    'GoogleCloudNetworksecurityV1CertificateProviderResponse',
    'GoogleCloudNetworksecurityV1GrpcEndpointResponse',
    'GoogleIamV1AuditConfigResponse',
    'GoogleIamV1AuditLogConfigResponse',
    'GoogleIamV1BindingResponse',
    'HttpHeaderMatchResponse',
    'MTLSPolicyResponse',
    'RuleResponse',
    'SourceResponse',
    'ValidationCAResponse',
]

@pulumi.output_type
class CertificateProviderInstanceResponse(dict):
    """
    Specification of a TLS certificate provider instance. Workloads may have one or more CertificateProvider instances (plugins) and one of them is enabled and configured by specifying this message. Workloads use the values from this message to locate and load the CertificateProvider instance configuration.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "pluginInstance":
            suggest = "plugin_instance"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CertificateProviderInstanceResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CertificateProviderInstanceResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        CertificateProviderInstanceResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 plugin_instance: str):
        """
        Specification of a TLS certificate provider instance. Workloads may have one or more CertificateProvider instances (plugins) and one of them is enabled and configured by specifying this message. Workloads use the values from this message to locate and load the CertificateProvider instance configuration.
        :param str plugin_instance: Plugin instance name, used to locate and load CertificateProvider instance configuration. Set to "google_cloud_private_spiffe" to use Certificate Authority Service certificate provider instance.
        """
        pulumi.set(__self__, "plugin_instance", plugin_instance)

    @property
    @pulumi.getter(name="pluginInstance")
    def plugin_instance(self) -> str:
        """
        Plugin instance name, used to locate and load CertificateProvider instance configuration. Set to "google_cloud_private_spiffe" to use Certificate Authority Service certificate provider instance.
        """
        return pulumi.get(self, "plugin_instance")


@pulumi.output_type
class DestinationResponse(dict):
    """
    Specification of traffic destination attributes.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "httpHeaderMatch":
            suggest = "http_header_match"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in DestinationResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        DestinationResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        DestinationResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 hosts: Sequence[str],
                 http_header_match: 'outputs.HttpHeaderMatchResponse',
                 methods: Sequence[str],
                 ports: Sequence[int]):
        """
        Specification of traffic destination attributes.
        :param Sequence[str] hosts: List of host names to match. Matched against the ":authority" header in http requests. At least one host should match. Each host can be an exact match, or a prefix match (example "mydomain.*") or a suffix match (example "*.myorg.com") or a presence (any) match "*".
        :param 'HttpHeaderMatchResponse' http_header_match: Optional. Match against key:value pair in http header. Provides a flexible match based on HTTP headers, for potentially advanced use cases. At least one header should match. Avoid using header matches to make authorization decisions unless there is a strong guarantee that requests arrive through a trusted client or proxy.
        :param Sequence[str] methods: Optional. A list of HTTP methods to match. At least one method should match. Should not be set for gRPC services.
        :param Sequence[int] ports: List of destination ports to match. At least one port should match.
        """
        pulumi.set(__self__, "hosts", hosts)
        pulumi.set(__self__, "http_header_match", http_header_match)
        pulumi.set(__self__, "methods", methods)
        pulumi.set(__self__, "ports", ports)

    @property
    @pulumi.getter
    def hosts(self) -> Sequence[str]:
        """
        List of host names to match. Matched against the ":authority" header in http requests. At least one host should match. Each host can be an exact match, or a prefix match (example "mydomain.*") or a suffix match (example "*.myorg.com") or a presence (any) match "*".
        """
        return pulumi.get(self, "hosts")

    @property
    @pulumi.getter(name="httpHeaderMatch")
    def http_header_match(self) -> 'outputs.HttpHeaderMatchResponse':
        """
        Optional. Match against key:value pair in http header. Provides a flexible match based on HTTP headers, for potentially advanced use cases. At least one header should match. Avoid using header matches to make authorization decisions unless there is a strong guarantee that requests arrive through a trusted client or proxy.
        """
        return pulumi.get(self, "http_header_match")

    @property
    @pulumi.getter
    def methods(self) -> Sequence[str]:
        """
        Optional. A list of HTTP methods to match. At least one method should match. Should not be set for gRPC services.
        """
        return pulumi.get(self, "methods")

    @property
    @pulumi.getter
    def ports(self) -> Sequence[int]:
        """
        List of destination ports to match. At least one port should match.
        """
        return pulumi.get(self, "ports")


@pulumi.output_type
class ExprResponse(dict):
    """
    Represents a textual expression in the Common Expression Language (CEL) syntax. CEL is a C-like expression language. The syntax and semantics of CEL are documented at https://github.com/google/cel-spec. Example (Comparison): title: "Summary size limit" description: "Determines if a summary is less than 100 chars" expression: "document.summary.size() < 100" Example (Equality): title: "Requestor is owner" description: "Determines if requestor is the document owner" expression: "document.owner == request.auth.claims.email" Example (Logic): title: "Public documents" description: "Determine whether the document should be publicly visible" expression: "document.type != 'private' && document.type != 'internal'" Example (Data Manipulation): title: "Notification string" description: "Create a notification string with a timestamp." expression: "'New message received at ' + string(document.create_time)" The exact variables and functions that may be referenced within an expression are determined by the service that evaluates it. See the service documentation for additional information.
    """
    def __init__(__self__, *,
                 description: str,
                 expression: str,
                 location: str,
                 title: str):
        """
        Represents a textual expression in the Common Expression Language (CEL) syntax. CEL is a C-like expression language. The syntax and semantics of CEL are documented at https://github.com/google/cel-spec. Example (Comparison): title: "Summary size limit" description: "Determines if a summary is less than 100 chars" expression: "document.summary.size() < 100" Example (Equality): title: "Requestor is owner" description: "Determines if requestor is the document owner" expression: "document.owner == request.auth.claims.email" Example (Logic): title: "Public documents" description: "Determine whether the document should be publicly visible" expression: "document.type != 'private' && document.type != 'internal'" Example (Data Manipulation): title: "Notification string" description: "Create a notification string with a timestamp." expression: "'New message received at ' + string(document.create_time)" The exact variables and functions that may be referenced within an expression are determined by the service that evaluates it. See the service documentation for additional information.
        :param str description: Optional. Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI.
        :param str expression: Textual representation of an expression in Common Expression Language syntax.
        :param str location: Optional. String indicating the location of the expression for error reporting, e.g. a file name and a position in the file.
        :param str title: Optional. Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression.
        """
        pulumi.set(__self__, "description", description)
        pulumi.set(__self__, "expression", expression)
        pulumi.set(__self__, "location", location)
        pulumi.set(__self__, "title", title)

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        Optional. Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def expression(self) -> str:
        """
        Textual representation of an expression in Common Expression Language syntax.
        """
        return pulumi.get(self, "expression")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        Optional. String indicating the location of the expression for error reporting, e.g. a file name and a position in the file.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def title(self) -> str:
        """
        Optional. Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression.
        """
        return pulumi.get(self, "title")


@pulumi.output_type
class GoogleCloudNetworksecurityV1CertificateProviderResponse(dict):
    """
    Specification of certificate provider. Defines the mechanism to obtain the certificate and private key for peer to peer authentication.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "certificateProviderInstance":
            suggest = "certificate_provider_instance"
        elif key == "grpcEndpoint":
            suggest = "grpc_endpoint"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in GoogleCloudNetworksecurityV1CertificateProviderResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        GoogleCloudNetworksecurityV1CertificateProviderResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        GoogleCloudNetworksecurityV1CertificateProviderResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 certificate_provider_instance: 'outputs.CertificateProviderInstanceResponse',
                 grpc_endpoint: 'outputs.GoogleCloudNetworksecurityV1GrpcEndpointResponse'):
        """
        Specification of certificate provider. Defines the mechanism to obtain the certificate and private key for peer to peer authentication.
        :param 'CertificateProviderInstanceResponse' certificate_provider_instance: The certificate provider instance specification that will be passed to the data plane, which will be used to load necessary credential information.
        :param 'GoogleCloudNetworksecurityV1GrpcEndpointResponse' grpc_endpoint: gRPC specific configuration to access the gRPC server to obtain the cert and private key.
        """
        pulumi.set(__self__, "certificate_provider_instance", certificate_provider_instance)
        pulumi.set(__self__, "grpc_endpoint", grpc_endpoint)

    @property
    @pulumi.getter(name="certificateProviderInstance")
    def certificate_provider_instance(self) -> 'outputs.CertificateProviderInstanceResponse':
        """
        The certificate provider instance specification that will be passed to the data plane, which will be used to load necessary credential information.
        """
        return pulumi.get(self, "certificate_provider_instance")

    @property
    @pulumi.getter(name="grpcEndpoint")
    def grpc_endpoint(self) -> 'outputs.GoogleCloudNetworksecurityV1GrpcEndpointResponse':
        """
        gRPC specific configuration to access the gRPC server to obtain the cert and private key.
        """
        return pulumi.get(self, "grpc_endpoint")


@pulumi.output_type
class GoogleCloudNetworksecurityV1GrpcEndpointResponse(dict):
    """
    Specification of the GRPC Endpoint.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "targetUri":
            suggest = "target_uri"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in GoogleCloudNetworksecurityV1GrpcEndpointResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        GoogleCloudNetworksecurityV1GrpcEndpointResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        GoogleCloudNetworksecurityV1GrpcEndpointResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 target_uri: str):
        """
        Specification of the GRPC Endpoint.
        :param str target_uri: The target URI of the gRPC endpoint. Only UDS path is supported, and should start with "unix:".
        """
        pulumi.set(__self__, "target_uri", target_uri)

    @property
    @pulumi.getter(name="targetUri")
    def target_uri(self) -> str:
        """
        The target URI of the gRPC endpoint. Only UDS path is supported, and should start with "unix:".
        """
        return pulumi.get(self, "target_uri")


@pulumi.output_type
class GoogleIamV1AuditConfigResponse(dict):
    """
    Specifies the audit configuration for a service. The configuration determines which permission types are logged, and what identities, if any, are exempted from logging. An AuditConfig must have one or more AuditLogConfigs. If there are AuditConfigs for both `allServices` and a specific service, the union of the two AuditConfigs is used for that service: the log_types specified in each AuditConfig are enabled, and the exempted_members in each AuditLogConfig are exempted. Example Policy with multiple AuditConfigs: { "audit_configs": [ { "service": "allServices", "audit_log_configs": [ { "log_type": "DATA_READ", "exempted_members": [ "user:jose@example.com" ] }, { "log_type": "DATA_WRITE" }, { "log_type": "ADMIN_READ" } ] }, { "service": "sampleservice.googleapis.com", "audit_log_configs": [ { "log_type": "DATA_READ" }, { "log_type": "DATA_WRITE", "exempted_members": [ "user:aliya@example.com" ] } ] } ] } For sampleservice, this policy enables DATA_READ, DATA_WRITE and ADMIN_READ logging. It also exempts `jose@example.com` from DATA_READ logging, and `aliya@example.com` from DATA_WRITE logging.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "auditLogConfigs":
            suggest = "audit_log_configs"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in GoogleIamV1AuditConfigResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        GoogleIamV1AuditConfigResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        GoogleIamV1AuditConfigResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 audit_log_configs: Sequence['outputs.GoogleIamV1AuditLogConfigResponse'],
                 service: str):
        """
        Specifies the audit configuration for a service. The configuration determines which permission types are logged, and what identities, if any, are exempted from logging. An AuditConfig must have one or more AuditLogConfigs. If there are AuditConfigs for both `allServices` and a specific service, the union of the two AuditConfigs is used for that service: the log_types specified in each AuditConfig are enabled, and the exempted_members in each AuditLogConfig are exempted. Example Policy with multiple AuditConfigs: { "audit_configs": [ { "service": "allServices", "audit_log_configs": [ { "log_type": "DATA_READ", "exempted_members": [ "user:jose@example.com" ] }, { "log_type": "DATA_WRITE" }, { "log_type": "ADMIN_READ" } ] }, { "service": "sampleservice.googleapis.com", "audit_log_configs": [ { "log_type": "DATA_READ" }, { "log_type": "DATA_WRITE", "exempted_members": [ "user:aliya@example.com" ] } ] } ] } For sampleservice, this policy enables DATA_READ, DATA_WRITE and ADMIN_READ logging. It also exempts `jose@example.com` from DATA_READ logging, and `aliya@example.com` from DATA_WRITE logging.
        :param Sequence['GoogleIamV1AuditLogConfigResponse'] audit_log_configs: The configuration for logging of each type of permission.
        :param str service: Specifies a service that will be enabled for audit logging. For example, `storage.googleapis.com`, `cloudsql.googleapis.com`. `allServices` is a special value that covers all services.
        """
        pulumi.set(__self__, "audit_log_configs", audit_log_configs)
        pulumi.set(__self__, "service", service)

    @property
    @pulumi.getter(name="auditLogConfigs")
    def audit_log_configs(self) -> Sequence['outputs.GoogleIamV1AuditLogConfigResponse']:
        """
        The configuration for logging of each type of permission.
        """
        return pulumi.get(self, "audit_log_configs")

    @property
    @pulumi.getter
    def service(self) -> str:
        """
        Specifies a service that will be enabled for audit logging. For example, `storage.googleapis.com`, `cloudsql.googleapis.com`. `allServices` is a special value that covers all services.
        """
        return pulumi.get(self, "service")


@pulumi.output_type
class GoogleIamV1AuditLogConfigResponse(dict):
    """
    Provides the configuration for logging a type of permissions. Example: { "audit_log_configs": [ { "log_type": "DATA_READ", "exempted_members": [ "user:jose@example.com" ] }, { "log_type": "DATA_WRITE" } ] } This enables 'DATA_READ' and 'DATA_WRITE' logging, while exempting jose@example.com from DATA_READ logging.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "exemptedMembers":
            suggest = "exempted_members"
        elif key == "logType":
            suggest = "log_type"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in GoogleIamV1AuditLogConfigResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        GoogleIamV1AuditLogConfigResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        GoogleIamV1AuditLogConfigResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 exempted_members: Sequence[str],
                 log_type: str):
        """
        Provides the configuration for logging a type of permissions. Example: { "audit_log_configs": [ { "log_type": "DATA_READ", "exempted_members": [ "user:jose@example.com" ] }, { "log_type": "DATA_WRITE" } ] } This enables 'DATA_READ' and 'DATA_WRITE' logging, while exempting jose@example.com from DATA_READ logging.
        :param Sequence[str] exempted_members: Specifies the identities that do not cause logging for this type of permission. Follows the same format of Binding.members.
        :param str log_type: The log type that this config enables.
        """
        pulumi.set(__self__, "exempted_members", exempted_members)
        pulumi.set(__self__, "log_type", log_type)

    @property
    @pulumi.getter(name="exemptedMembers")
    def exempted_members(self) -> Sequence[str]:
        """
        Specifies the identities that do not cause logging for this type of permission. Follows the same format of Binding.members.
        """
        return pulumi.get(self, "exempted_members")

    @property
    @pulumi.getter(name="logType")
    def log_type(self) -> str:
        """
        The log type that this config enables.
        """
        return pulumi.get(self, "log_type")


@pulumi.output_type
class GoogleIamV1BindingResponse(dict):
    """
    Associates `members`, or principals, with a `role`.
    """
    def __init__(__self__, *,
                 condition: 'outputs.ExprResponse',
                 members: Sequence[str],
                 role: str):
        """
        Associates `members`, or principals, with a `role`.
        :param 'ExprResponse' condition: The condition that is associated with this binding. If the condition evaluates to `true`, then this binding applies to the current request. If the condition evaluates to `false`, then this binding does not apply to the current request. However, a different role binding might grant the same role to one or more of the principals in this binding. To learn which resources support conditions in their IAM policies, see the [IAM documentation](https://cloud.google.com/iam/help/conditions/resource-policies).
        :param Sequence[str] members: Specifies the principals requesting access for a Google Cloud resource. `members` can have the following values: * `allUsers`: A special identifier that represents anyone who is on the internet; with or without a Google account. * `allAuthenticatedUsers`: A special identifier that represents anyone who is authenticated with a Google account or a service account. Does not include identities that come from external identity providers (IdPs) through identity federation. * `user:{emailid}`: An email address that represents a specific Google account. For example, `alice@example.com` . * `serviceAccount:{emailid}`: An email address that represents a Google service account. For example, `my-other-app@appspot.gserviceaccount.com`. * `serviceAccount:{projectid}.svc.id.goog[{namespace}/{kubernetes-sa}]`: An identifier for a [Kubernetes service account](https://cloud.google.com/kubernetes-engine/docs/how-to/kubernetes-service-accounts). For example, `my-project.svc.id.goog[my-namespace/my-kubernetes-sa]`. * `group:{emailid}`: An email address that represents a Google group. For example, `admins@example.com`. * `deleted:user:{emailid}?uid={uniqueid}`: An email address (plus unique identifier) representing a user that has been recently deleted. For example, `alice@example.com?uid=123456789012345678901`. If the user is recovered, this value reverts to `user:{emailid}` and the recovered user retains the role in the binding. * `deleted:serviceAccount:{emailid}?uid={uniqueid}`: An email address (plus unique identifier) representing a service account that has been recently deleted. For example, `my-other-app@appspot.gserviceaccount.com?uid=123456789012345678901`. If the service account is undeleted, this value reverts to `serviceAccount:{emailid}` and the undeleted service account retains the role in the binding. * `deleted:group:{emailid}?uid={uniqueid}`: An email address (plus unique identifier) representing a Google group that has been recently deleted. For example, `admins@example.com?uid=123456789012345678901`. If the group is recovered, this value reverts to `group:{emailid}` and the recovered group retains the role in the binding. * `domain:{domain}`: The G Suite domain (primary) that represents all the users of that domain. For example, `google.com` or `example.com`. 
        :param str role: Role that is assigned to the list of `members`, or principals. For example, `roles/viewer`, `roles/editor`, or `roles/owner`.
        """
        pulumi.set(__self__, "condition", condition)
        pulumi.set(__self__, "members", members)
        pulumi.set(__self__, "role", role)

    @property
    @pulumi.getter
    def condition(self) -> 'outputs.ExprResponse':
        """
        The condition that is associated with this binding. If the condition evaluates to `true`, then this binding applies to the current request. If the condition evaluates to `false`, then this binding does not apply to the current request. However, a different role binding might grant the same role to one or more of the principals in this binding. To learn which resources support conditions in their IAM policies, see the [IAM documentation](https://cloud.google.com/iam/help/conditions/resource-policies).
        """
        return pulumi.get(self, "condition")

    @property
    @pulumi.getter
    def members(self) -> Sequence[str]:
        """
        Specifies the principals requesting access for a Google Cloud resource. `members` can have the following values: * `allUsers`: A special identifier that represents anyone who is on the internet; with or without a Google account. * `allAuthenticatedUsers`: A special identifier that represents anyone who is authenticated with a Google account or a service account. Does not include identities that come from external identity providers (IdPs) through identity federation. * `user:{emailid}`: An email address that represents a specific Google account. For example, `alice@example.com` . * `serviceAccount:{emailid}`: An email address that represents a Google service account. For example, `my-other-app@appspot.gserviceaccount.com`. * `serviceAccount:{projectid}.svc.id.goog[{namespace}/{kubernetes-sa}]`: An identifier for a [Kubernetes service account](https://cloud.google.com/kubernetes-engine/docs/how-to/kubernetes-service-accounts). For example, `my-project.svc.id.goog[my-namespace/my-kubernetes-sa]`. * `group:{emailid}`: An email address that represents a Google group. For example, `admins@example.com`. * `deleted:user:{emailid}?uid={uniqueid}`: An email address (plus unique identifier) representing a user that has been recently deleted. For example, `alice@example.com?uid=123456789012345678901`. If the user is recovered, this value reverts to `user:{emailid}` and the recovered user retains the role in the binding. * `deleted:serviceAccount:{emailid}?uid={uniqueid}`: An email address (plus unique identifier) representing a service account that has been recently deleted. For example, `my-other-app@appspot.gserviceaccount.com?uid=123456789012345678901`. If the service account is undeleted, this value reverts to `serviceAccount:{emailid}` and the undeleted service account retains the role in the binding. * `deleted:group:{emailid}?uid={uniqueid}`: An email address (plus unique identifier) representing a Google group that has been recently deleted. For example, `admins@example.com?uid=123456789012345678901`. If the group is recovered, this value reverts to `group:{emailid}` and the recovered group retains the role in the binding. * `domain:{domain}`: The G Suite domain (primary) that represents all the users of that domain. For example, `google.com` or `example.com`. 
        """
        return pulumi.get(self, "members")

    @property
    @pulumi.getter
    def role(self) -> str:
        """
        Role that is assigned to the list of `members`, or principals. For example, `roles/viewer`, `roles/editor`, or `roles/owner`.
        """
        return pulumi.get(self, "role")


@pulumi.output_type
class HttpHeaderMatchResponse(dict):
    """
    Specification of HTTP header match attributes.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "headerName":
            suggest = "header_name"
        elif key == "regexMatch":
            suggest = "regex_match"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in HttpHeaderMatchResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        HttpHeaderMatchResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        HttpHeaderMatchResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 header_name: str,
                 regex_match: str):
        """
        Specification of HTTP header match attributes.
        :param str header_name: The name of the HTTP header to match. For matching against the HTTP request's authority, use a headerMatch with the header name ":authority". For matching a request's method, use the headerName ":method".
        :param str regex_match: The value of the header must match the regular expression specified in regexMatch. For regular expression grammar, please see: en.cppreference.com/w/cpp/regex/ecmascript For matching against a port specified in the HTTP request, use a headerMatch with headerName set to Host and a regular expression that satisfies the RFC2616 Host header's port specifier.
        """
        pulumi.set(__self__, "header_name", header_name)
        pulumi.set(__self__, "regex_match", regex_match)

    @property
    @pulumi.getter(name="headerName")
    def header_name(self) -> str:
        """
        The name of the HTTP header to match. For matching against the HTTP request's authority, use a headerMatch with the header name ":authority". For matching a request's method, use the headerName ":method".
        """
        return pulumi.get(self, "header_name")

    @property
    @pulumi.getter(name="regexMatch")
    def regex_match(self) -> str:
        """
        The value of the header must match the regular expression specified in regexMatch. For regular expression grammar, please see: en.cppreference.com/w/cpp/regex/ecmascript For matching against a port specified in the HTTP request, use a headerMatch with headerName set to Host and a regular expression that satisfies the RFC2616 Host header's port specifier.
        """
        return pulumi.get(self, "regex_match")


@pulumi.output_type
class MTLSPolicyResponse(dict):
    """
    Specification of the MTLSPolicy.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "clientValidationCa":
            suggest = "client_validation_ca"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in MTLSPolicyResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        MTLSPolicyResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        MTLSPolicyResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 client_validation_ca: Sequence['outputs.ValidationCAResponse']):
        """
        Specification of the MTLSPolicy.
        :param Sequence['ValidationCAResponse'] client_validation_ca:  Defines the mechanism to obtain the Certificate Authority certificate to validate the client certificate.
        """
        pulumi.set(__self__, "client_validation_ca", client_validation_ca)

    @property
    @pulumi.getter(name="clientValidationCa")
    def client_validation_ca(self) -> Sequence['outputs.ValidationCAResponse']:
        """
         Defines the mechanism to obtain the Certificate Authority certificate to validate the client certificate.
        """
        return pulumi.get(self, "client_validation_ca")


@pulumi.output_type
class RuleResponse(dict):
    """
    Specification of rules.
    """
    def __init__(__self__, *,
                 destinations: Sequence['outputs.DestinationResponse'],
                 sources: Sequence['outputs.SourceResponse']):
        """
        Specification of rules.
        :param Sequence['DestinationResponse'] destinations: Optional. List of attributes for the traffic destination. All of the destinations must match. A destination is a match if a request matches all the specified hosts, ports, methods and headers. If not set, the action specified in the 'action' field will be applied without any rule checks for the destination.
        :param Sequence['SourceResponse'] sources: Optional. List of attributes for the traffic source. All of the sources must match. A source is a match if both principals and ip_blocks match. If not set, the action specified in the 'action' field will be applied without any rule checks for the source.
        """
        pulumi.set(__self__, "destinations", destinations)
        pulumi.set(__self__, "sources", sources)

    @property
    @pulumi.getter
    def destinations(self) -> Sequence['outputs.DestinationResponse']:
        """
        Optional. List of attributes for the traffic destination. All of the destinations must match. A destination is a match if a request matches all the specified hosts, ports, methods and headers. If not set, the action specified in the 'action' field will be applied without any rule checks for the destination.
        """
        return pulumi.get(self, "destinations")

    @property
    @pulumi.getter
    def sources(self) -> Sequence['outputs.SourceResponse']:
        """
        Optional. List of attributes for the traffic source. All of the sources must match. A source is a match if both principals and ip_blocks match. If not set, the action specified in the 'action' field will be applied without any rule checks for the source.
        """
        return pulumi.get(self, "sources")


@pulumi.output_type
class SourceResponse(dict):
    """
    Specification of traffic source attributes.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "ipBlocks":
            suggest = "ip_blocks"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SourceResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SourceResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        SourceResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 ip_blocks: Sequence[str],
                 principals: Sequence[str]):
        """
        Specification of traffic source attributes.
        :param Sequence[str] ip_blocks: Optional. List of CIDR ranges to match based on source IP address. At least one IP block should match. Single IP (e.g., "1.2.3.4") and CIDR (e.g., "1.2.3.0/24") are supported. Authorization based on source IP alone should be avoided. The IP addresses of any load balancers or proxies should be considered untrusted.
        :param Sequence[str] principals: Optional. List of peer identities to match for authorization. At least one principal should match. Each peer can be an exact match, or a prefix match (example, "namespace/*") or a suffix match (example, "*/service-account") or a presence match "*". Authorization based on the principal name without certificate validation (configured by ServerTlsPolicy resource) is considered insecure.
        """
        pulumi.set(__self__, "ip_blocks", ip_blocks)
        pulumi.set(__self__, "principals", principals)

    @property
    @pulumi.getter(name="ipBlocks")
    def ip_blocks(self) -> Sequence[str]:
        """
        Optional. List of CIDR ranges to match based on source IP address. At least one IP block should match. Single IP (e.g., "1.2.3.4") and CIDR (e.g., "1.2.3.0/24") are supported. Authorization based on source IP alone should be avoided. The IP addresses of any load balancers or proxies should be considered untrusted.
        """
        return pulumi.get(self, "ip_blocks")

    @property
    @pulumi.getter
    def principals(self) -> Sequence[str]:
        """
        Optional. List of peer identities to match for authorization. At least one principal should match. Each peer can be an exact match, or a prefix match (example, "namespace/*") or a suffix match (example, "*/service-account") or a presence match "*". Authorization based on the principal name without certificate validation (configured by ServerTlsPolicy resource) is considered insecure.
        """
        return pulumi.get(self, "principals")


@pulumi.output_type
class ValidationCAResponse(dict):
    """
    Specification of ValidationCA. Defines the mechanism to obtain the Certificate Authority certificate to validate the peer certificate.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "certificateProviderInstance":
            suggest = "certificate_provider_instance"
        elif key == "grpcEndpoint":
            suggest = "grpc_endpoint"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ValidationCAResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ValidationCAResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ValidationCAResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 certificate_provider_instance: 'outputs.CertificateProviderInstanceResponse',
                 grpc_endpoint: 'outputs.GoogleCloudNetworksecurityV1GrpcEndpointResponse'):
        """
        Specification of ValidationCA. Defines the mechanism to obtain the Certificate Authority certificate to validate the peer certificate.
        :param 'CertificateProviderInstanceResponse' certificate_provider_instance: The certificate provider instance specification that will be passed to the data plane, which will be used to load necessary credential information.
        :param 'GoogleCloudNetworksecurityV1GrpcEndpointResponse' grpc_endpoint: gRPC specific configuration to access the gRPC server to obtain the CA certificate.
        """
        pulumi.set(__self__, "certificate_provider_instance", certificate_provider_instance)
        pulumi.set(__self__, "grpc_endpoint", grpc_endpoint)

    @property
    @pulumi.getter(name="certificateProviderInstance")
    def certificate_provider_instance(self) -> 'outputs.CertificateProviderInstanceResponse':
        """
        The certificate provider instance specification that will be passed to the data plane, which will be used to load necessary credential information.
        """
        return pulumi.get(self, "certificate_provider_instance")

    @property
    @pulumi.getter(name="grpcEndpoint")
    def grpc_endpoint(self) -> 'outputs.GoogleCloudNetworksecurityV1GrpcEndpointResponse':
        """
        gRPC specific configuration to access the gRPC server to obtain the CA certificate.
        """
        return pulumi.get(self, "grpc_endpoint")


