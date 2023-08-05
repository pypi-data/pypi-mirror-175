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

__all__ = [
    'CertificateProviderInstanceArgs',
    'DestinationArgs',
    'ExprArgs',
    'GoogleCloudNetworksecurityV1beta1CertificateProviderArgs',
    'GoogleCloudNetworksecurityV1beta1GrpcEndpointArgs',
    'GoogleIamV1AuditConfigArgs',
    'GoogleIamV1AuditLogConfigArgs',
    'GoogleIamV1BindingArgs',
    'HttpHeaderMatchArgs',
    'MTLSPolicyArgs',
    'RuleArgs',
    'SourceArgs',
    'ValidationCAArgs',
]

@pulumi.input_type
class CertificateProviderInstanceArgs:
    def __init__(__self__, *,
                 plugin_instance: pulumi.Input[str]):
        """
        Specification of a TLS certificate provider instance. Workloads may have one or more CertificateProvider instances (plugins) and one of them is enabled and configured by specifying this message. Workloads use the values from this message to locate and load the CertificateProvider instance configuration.
        :param pulumi.Input[str] plugin_instance: Plugin instance name, used to locate and load CertificateProvider instance configuration. Set to "google_cloud_private_spiffe" to use Certificate Authority Service certificate provider instance.
        """
        pulumi.set(__self__, "plugin_instance", plugin_instance)

    @property
    @pulumi.getter(name="pluginInstance")
    def plugin_instance(self) -> pulumi.Input[str]:
        """
        Plugin instance name, used to locate and load CertificateProvider instance configuration. Set to "google_cloud_private_spiffe" to use Certificate Authority Service certificate provider instance.
        """
        return pulumi.get(self, "plugin_instance")

    @plugin_instance.setter
    def plugin_instance(self, value: pulumi.Input[str]):
        pulumi.set(self, "plugin_instance", value)


@pulumi.input_type
class DestinationArgs:
    def __init__(__self__, *,
                 hosts: pulumi.Input[Sequence[pulumi.Input[str]]],
                 ports: pulumi.Input[Sequence[pulumi.Input[int]]],
                 http_header_match: Optional[pulumi.Input['HttpHeaderMatchArgs']] = None,
                 methods: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        Specification of traffic destination attributes.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] hosts: List of host names to match. Matched against the ":authority" header in http requests. At least one host should match. Each host can be an exact match, or a prefix match (example "mydomain.*") or a suffix match (example "*.myorg.com") or a presence (any) match "*".
        :param pulumi.Input[Sequence[pulumi.Input[int]]] ports: List of destination ports to match. At least one port should match.
        :param pulumi.Input['HttpHeaderMatchArgs'] http_header_match: Optional. Match against key:value pair in http header. Provides a flexible match based on HTTP headers, for potentially advanced use cases. At least one header should match. Avoid using header matches to make authorization decisions unless there is a strong guarantee that requests arrive through a trusted client or proxy.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] methods: Optional. A list of HTTP methods to match. At least one method should match. Should not be set for gRPC services.
        """
        pulumi.set(__self__, "hosts", hosts)
        pulumi.set(__self__, "ports", ports)
        if http_header_match is not None:
            pulumi.set(__self__, "http_header_match", http_header_match)
        if methods is not None:
            pulumi.set(__self__, "methods", methods)

    @property
    @pulumi.getter
    def hosts(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        List of host names to match. Matched against the ":authority" header in http requests. At least one host should match. Each host can be an exact match, or a prefix match (example "mydomain.*") or a suffix match (example "*.myorg.com") or a presence (any) match "*".
        """
        return pulumi.get(self, "hosts")

    @hosts.setter
    def hosts(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "hosts", value)

    @property
    @pulumi.getter
    def ports(self) -> pulumi.Input[Sequence[pulumi.Input[int]]]:
        """
        List of destination ports to match. At least one port should match.
        """
        return pulumi.get(self, "ports")

    @ports.setter
    def ports(self, value: pulumi.Input[Sequence[pulumi.Input[int]]]):
        pulumi.set(self, "ports", value)

    @property
    @pulumi.getter(name="httpHeaderMatch")
    def http_header_match(self) -> Optional[pulumi.Input['HttpHeaderMatchArgs']]:
        """
        Optional. Match against key:value pair in http header. Provides a flexible match based on HTTP headers, for potentially advanced use cases. At least one header should match. Avoid using header matches to make authorization decisions unless there is a strong guarantee that requests arrive through a trusted client or proxy.
        """
        return pulumi.get(self, "http_header_match")

    @http_header_match.setter
    def http_header_match(self, value: Optional[pulumi.Input['HttpHeaderMatchArgs']]):
        pulumi.set(self, "http_header_match", value)

    @property
    @pulumi.getter
    def methods(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Optional. A list of HTTP methods to match. At least one method should match. Should not be set for gRPC services.
        """
        return pulumi.get(self, "methods")

    @methods.setter
    def methods(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "methods", value)


@pulumi.input_type
class ExprArgs:
    def __init__(__self__, *,
                 description: Optional[pulumi.Input[str]] = None,
                 expression: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 title: Optional[pulumi.Input[str]] = None):
        """
        Represents a textual expression in the Common Expression Language (CEL) syntax. CEL is a C-like expression language. The syntax and semantics of CEL are documented at https://github.com/google/cel-spec. Example (Comparison): title: "Summary size limit" description: "Determines if a summary is less than 100 chars" expression: "document.summary.size() < 100" Example (Equality): title: "Requestor is owner" description: "Determines if requestor is the document owner" expression: "document.owner == request.auth.claims.email" Example (Logic): title: "Public documents" description: "Determine whether the document should be publicly visible" expression: "document.type != 'private' && document.type != 'internal'" Example (Data Manipulation): title: "Notification string" description: "Create a notification string with a timestamp." expression: "'New message received at ' + string(document.create_time)" The exact variables and functions that may be referenced within an expression are determined by the service that evaluates it. See the service documentation for additional information.
        :param pulumi.Input[str] description: Optional. Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI.
        :param pulumi.Input[str] expression: Textual representation of an expression in Common Expression Language syntax.
        :param pulumi.Input[str] location: Optional. String indicating the location of the expression for error reporting, e.g. a file name and a position in the file.
        :param pulumi.Input[str] title: Optional. Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression.
        """
        if description is not None:
            pulumi.set(__self__, "description", description)
        if expression is not None:
            pulumi.set(__self__, "expression", expression)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if title is not None:
            pulumi.set(__self__, "title", title)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def expression(self) -> Optional[pulumi.Input[str]]:
        """
        Textual representation of an expression in Common Expression Language syntax.
        """
        return pulumi.get(self, "expression")

    @expression.setter
    def expression(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "expression", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. String indicating the location of the expression for error reporting, e.g. a file name and a position in the file.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def title(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression.
        """
        return pulumi.get(self, "title")

    @title.setter
    def title(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "title", value)


@pulumi.input_type
class GoogleCloudNetworksecurityV1beta1CertificateProviderArgs:
    def __init__(__self__, *,
                 certificate_provider_instance: Optional[pulumi.Input['CertificateProviderInstanceArgs']] = None,
                 grpc_endpoint: Optional[pulumi.Input['GoogleCloudNetworksecurityV1beta1GrpcEndpointArgs']] = None):
        """
        Specification of certificate provider. Defines the mechanism to obtain the certificate and private key for peer to peer authentication.
        :param pulumi.Input['CertificateProviderInstanceArgs'] certificate_provider_instance: The certificate provider instance specification that will be passed to the data plane, which will be used to load necessary credential information.
        :param pulumi.Input['GoogleCloudNetworksecurityV1beta1GrpcEndpointArgs'] grpc_endpoint: gRPC specific configuration to access the gRPC server to obtain the cert and private key.
        """
        if certificate_provider_instance is not None:
            pulumi.set(__self__, "certificate_provider_instance", certificate_provider_instance)
        if grpc_endpoint is not None:
            pulumi.set(__self__, "grpc_endpoint", grpc_endpoint)

    @property
    @pulumi.getter(name="certificateProviderInstance")
    def certificate_provider_instance(self) -> Optional[pulumi.Input['CertificateProviderInstanceArgs']]:
        """
        The certificate provider instance specification that will be passed to the data plane, which will be used to load necessary credential information.
        """
        return pulumi.get(self, "certificate_provider_instance")

    @certificate_provider_instance.setter
    def certificate_provider_instance(self, value: Optional[pulumi.Input['CertificateProviderInstanceArgs']]):
        pulumi.set(self, "certificate_provider_instance", value)

    @property
    @pulumi.getter(name="grpcEndpoint")
    def grpc_endpoint(self) -> Optional[pulumi.Input['GoogleCloudNetworksecurityV1beta1GrpcEndpointArgs']]:
        """
        gRPC specific configuration to access the gRPC server to obtain the cert and private key.
        """
        return pulumi.get(self, "grpc_endpoint")

    @grpc_endpoint.setter
    def grpc_endpoint(self, value: Optional[pulumi.Input['GoogleCloudNetworksecurityV1beta1GrpcEndpointArgs']]):
        pulumi.set(self, "grpc_endpoint", value)


@pulumi.input_type
class GoogleCloudNetworksecurityV1beta1GrpcEndpointArgs:
    def __init__(__self__, *,
                 target_uri: pulumi.Input[str]):
        """
        Specification of the GRPC Endpoint.
        :param pulumi.Input[str] target_uri: The target URI of the gRPC endpoint. Only UDS path is supported, and should start with "unix:".
        """
        pulumi.set(__self__, "target_uri", target_uri)

    @property
    @pulumi.getter(name="targetUri")
    def target_uri(self) -> pulumi.Input[str]:
        """
        The target URI of the gRPC endpoint. Only UDS path is supported, and should start with "unix:".
        """
        return pulumi.get(self, "target_uri")

    @target_uri.setter
    def target_uri(self, value: pulumi.Input[str]):
        pulumi.set(self, "target_uri", value)


@pulumi.input_type
class GoogleIamV1AuditConfigArgs:
    def __init__(__self__, *,
                 audit_log_configs: Optional[pulumi.Input[Sequence[pulumi.Input['GoogleIamV1AuditLogConfigArgs']]]] = None,
                 service: Optional[pulumi.Input[str]] = None):
        """
        Specifies the audit configuration for a service. The configuration determines which permission types are logged, and what identities, if any, are exempted from logging. An AuditConfig must have one or more AuditLogConfigs. If there are AuditConfigs for both `allServices` and a specific service, the union of the two AuditConfigs is used for that service: the log_types specified in each AuditConfig are enabled, and the exempted_members in each AuditLogConfig are exempted. Example Policy with multiple AuditConfigs: { "audit_configs": [ { "service": "allServices", "audit_log_configs": [ { "log_type": "DATA_READ", "exempted_members": [ "user:jose@example.com" ] }, { "log_type": "DATA_WRITE" }, { "log_type": "ADMIN_READ" } ] }, { "service": "sampleservice.googleapis.com", "audit_log_configs": [ { "log_type": "DATA_READ" }, { "log_type": "DATA_WRITE", "exempted_members": [ "user:aliya@example.com" ] } ] } ] } For sampleservice, this policy enables DATA_READ, DATA_WRITE and ADMIN_READ logging. It also exempts `jose@example.com` from DATA_READ logging, and `aliya@example.com` from DATA_WRITE logging.
        :param pulumi.Input[Sequence[pulumi.Input['GoogleIamV1AuditLogConfigArgs']]] audit_log_configs: The configuration for logging of each type of permission.
        :param pulumi.Input[str] service: Specifies a service that will be enabled for audit logging. For example, `storage.googleapis.com`, `cloudsql.googleapis.com`. `allServices` is a special value that covers all services.
        """
        if audit_log_configs is not None:
            pulumi.set(__self__, "audit_log_configs", audit_log_configs)
        if service is not None:
            pulumi.set(__self__, "service", service)

    @property
    @pulumi.getter(name="auditLogConfigs")
    def audit_log_configs(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['GoogleIamV1AuditLogConfigArgs']]]]:
        """
        The configuration for logging of each type of permission.
        """
        return pulumi.get(self, "audit_log_configs")

    @audit_log_configs.setter
    def audit_log_configs(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['GoogleIamV1AuditLogConfigArgs']]]]):
        pulumi.set(self, "audit_log_configs", value)

    @property
    @pulumi.getter
    def service(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies a service that will be enabled for audit logging. For example, `storage.googleapis.com`, `cloudsql.googleapis.com`. `allServices` is a special value that covers all services.
        """
        return pulumi.get(self, "service")

    @service.setter
    def service(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service", value)


@pulumi.input_type
class GoogleIamV1AuditLogConfigArgs:
    def __init__(__self__, *,
                 exempted_members: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 log_type: Optional[pulumi.Input['GoogleIamV1AuditLogConfigLogType']] = None):
        """
        Provides the configuration for logging a type of permissions. Example: { "audit_log_configs": [ { "log_type": "DATA_READ", "exempted_members": [ "user:jose@example.com" ] }, { "log_type": "DATA_WRITE" } ] } This enables 'DATA_READ' and 'DATA_WRITE' logging, while exempting jose@example.com from DATA_READ logging.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] exempted_members: Specifies the identities that do not cause logging for this type of permission. Follows the same format of Binding.members.
        :param pulumi.Input['GoogleIamV1AuditLogConfigLogType'] log_type: The log type that this config enables.
        """
        if exempted_members is not None:
            pulumi.set(__self__, "exempted_members", exempted_members)
        if log_type is not None:
            pulumi.set(__self__, "log_type", log_type)

    @property
    @pulumi.getter(name="exemptedMembers")
    def exempted_members(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Specifies the identities that do not cause logging for this type of permission. Follows the same format of Binding.members.
        """
        return pulumi.get(self, "exempted_members")

    @exempted_members.setter
    def exempted_members(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "exempted_members", value)

    @property
    @pulumi.getter(name="logType")
    def log_type(self) -> Optional[pulumi.Input['GoogleIamV1AuditLogConfigLogType']]:
        """
        The log type that this config enables.
        """
        return pulumi.get(self, "log_type")

    @log_type.setter
    def log_type(self, value: Optional[pulumi.Input['GoogleIamV1AuditLogConfigLogType']]):
        pulumi.set(self, "log_type", value)


@pulumi.input_type
class GoogleIamV1BindingArgs:
    def __init__(__self__, *,
                 condition: Optional[pulumi.Input['ExprArgs']] = None,
                 members: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 role: Optional[pulumi.Input[str]] = None):
        """
        Associates `members`, or principals, with a `role`.
        :param pulumi.Input['ExprArgs'] condition: The condition that is associated with this binding. If the condition evaluates to `true`, then this binding applies to the current request. If the condition evaluates to `false`, then this binding does not apply to the current request. However, a different role binding might grant the same role to one or more of the principals in this binding. To learn which resources support conditions in their IAM policies, see the [IAM documentation](https://cloud.google.com/iam/help/conditions/resource-policies).
        :param pulumi.Input[Sequence[pulumi.Input[str]]] members: Specifies the principals requesting access for a Google Cloud resource. `members` can have the following values: * `allUsers`: A special identifier that represents anyone who is on the internet; with or without a Google account. * `allAuthenticatedUsers`: A special identifier that represents anyone who is authenticated with a Google account or a service account. Does not include identities that come from external identity providers (IdPs) through identity federation. * `user:{emailid}`: An email address that represents a specific Google account. For example, `alice@example.com` . * `serviceAccount:{emailid}`: An email address that represents a Google service account. For example, `my-other-app@appspot.gserviceaccount.com`. * `serviceAccount:{projectid}.svc.id.goog[{namespace}/{kubernetes-sa}]`: An identifier for a [Kubernetes service account](https://cloud.google.com/kubernetes-engine/docs/how-to/kubernetes-service-accounts). For example, `my-project.svc.id.goog[my-namespace/my-kubernetes-sa]`. * `group:{emailid}`: An email address that represents a Google group. For example, `admins@example.com`. * `deleted:user:{emailid}?uid={uniqueid}`: An email address (plus unique identifier) representing a user that has been recently deleted. For example, `alice@example.com?uid=123456789012345678901`. If the user is recovered, this value reverts to `user:{emailid}` and the recovered user retains the role in the binding. * `deleted:serviceAccount:{emailid}?uid={uniqueid}`: An email address (plus unique identifier) representing a service account that has been recently deleted. For example, `my-other-app@appspot.gserviceaccount.com?uid=123456789012345678901`. If the service account is undeleted, this value reverts to `serviceAccount:{emailid}` and the undeleted service account retains the role in the binding. * `deleted:group:{emailid}?uid={uniqueid}`: An email address (plus unique identifier) representing a Google group that has been recently deleted. For example, `admins@example.com?uid=123456789012345678901`. If the group is recovered, this value reverts to `group:{emailid}` and the recovered group retains the role in the binding. * `domain:{domain}`: The G Suite domain (primary) that represents all the users of that domain. For example, `google.com` or `example.com`. 
        :param pulumi.Input[str] role: Role that is assigned to the list of `members`, or principals. For example, `roles/viewer`, `roles/editor`, or `roles/owner`.
        """
        if condition is not None:
            pulumi.set(__self__, "condition", condition)
        if members is not None:
            pulumi.set(__self__, "members", members)
        if role is not None:
            pulumi.set(__self__, "role", role)

    @property
    @pulumi.getter
    def condition(self) -> Optional[pulumi.Input['ExprArgs']]:
        """
        The condition that is associated with this binding. If the condition evaluates to `true`, then this binding applies to the current request. If the condition evaluates to `false`, then this binding does not apply to the current request. However, a different role binding might grant the same role to one or more of the principals in this binding. To learn which resources support conditions in their IAM policies, see the [IAM documentation](https://cloud.google.com/iam/help/conditions/resource-policies).
        """
        return pulumi.get(self, "condition")

    @condition.setter
    def condition(self, value: Optional[pulumi.Input['ExprArgs']]):
        pulumi.set(self, "condition", value)

    @property
    @pulumi.getter
    def members(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Specifies the principals requesting access for a Google Cloud resource. `members` can have the following values: * `allUsers`: A special identifier that represents anyone who is on the internet; with or without a Google account. * `allAuthenticatedUsers`: A special identifier that represents anyone who is authenticated with a Google account or a service account. Does not include identities that come from external identity providers (IdPs) through identity federation. * `user:{emailid}`: An email address that represents a specific Google account. For example, `alice@example.com` . * `serviceAccount:{emailid}`: An email address that represents a Google service account. For example, `my-other-app@appspot.gserviceaccount.com`. * `serviceAccount:{projectid}.svc.id.goog[{namespace}/{kubernetes-sa}]`: An identifier for a [Kubernetes service account](https://cloud.google.com/kubernetes-engine/docs/how-to/kubernetes-service-accounts). For example, `my-project.svc.id.goog[my-namespace/my-kubernetes-sa]`. * `group:{emailid}`: An email address that represents a Google group. For example, `admins@example.com`. * `deleted:user:{emailid}?uid={uniqueid}`: An email address (plus unique identifier) representing a user that has been recently deleted. For example, `alice@example.com?uid=123456789012345678901`. If the user is recovered, this value reverts to `user:{emailid}` and the recovered user retains the role in the binding. * `deleted:serviceAccount:{emailid}?uid={uniqueid}`: An email address (plus unique identifier) representing a service account that has been recently deleted. For example, `my-other-app@appspot.gserviceaccount.com?uid=123456789012345678901`. If the service account is undeleted, this value reverts to `serviceAccount:{emailid}` and the undeleted service account retains the role in the binding. * `deleted:group:{emailid}?uid={uniqueid}`: An email address (plus unique identifier) representing a Google group that has been recently deleted. For example, `admins@example.com?uid=123456789012345678901`. If the group is recovered, this value reverts to `group:{emailid}` and the recovered group retains the role in the binding. * `domain:{domain}`: The G Suite domain (primary) that represents all the users of that domain. For example, `google.com` or `example.com`. 
        """
        return pulumi.get(self, "members")

    @members.setter
    def members(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "members", value)

    @property
    @pulumi.getter
    def role(self) -> Optional[pulumi.Input[str]]:
        """
        Role that is assigned to the list of `members`, or principals. For example, `roles/viewer`, `roles/editor`, or `roles/owner`.
        """
        return pulumi.get(self, "role")

    @role.setter
    def role(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "role", value)


@pulumi.input_type
class HttpHeaderMatchArgs:
    def __init__(__self__, *,
                 header_name: pulumi.Input[str],
                 regex_match: pulumi.Input[str]):
        """
        Specification of HTTP header match attributes.
        :param pulumi.Input[str] header_name: The name of the HTTP header to match. For matching against the HTTP request's authority, use a headerMatch with the header name ":authority". For matching a request's method, use the headerName ":method".
        :param pulumi.Input[str] regex_match: The value of the header must match the regular expression specified in regexMatch. For regular expression grammar, please see: en.cppreference.com/w/cpp/regex/ecmascript For matching against a port specified in the HTTP request, use a headerMatch with headerName set to Host and a regular expression that satisfies the RFC2616 Host header's port specifier.
        """
        pulumi.set(__self__, "header_name", header_name)
        pulumi.set(__self__, "regex_match", regex_match)

    @property
    @pulumi.getter(name="headerName")
    def header_name(self) -> pulumi.Input[str]:
        """
        The name of the HTTP header to match. For matching against the HTTP request's authority, use a headerMatch with the header name ":authority". For matching a request's method, use the headerName ":method".
        """
        return pulumi.get(self, "header_name")

    @header_name.setter
    def header_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "header_name", value)

    @property
    @pulumi.getter(name="regexMatch")
    def regex_match(self) -> pulumi.Input[str]:
        """
        The value of the header must match the regular expression specified in regexMatch. For regular expression grammar, please see: en.cppreference.com/w/cpp/regex/ecmascript For matching against a port specified in the HTTP request, use a headerMatch with headerName set to Host and a regular expression that satisfies the RFC2616 Host header's port specifier.
        """
        return pulumi.get(self, "regex_match")

    @regex_match.setter
    def regex_match(self, value: pulumi.Input[str]):
        pulumi.set(self, "regex_match", value)


@pulumi.input_type
class MTLSPolicyArgs:
    def __init__(__self__, *,
                 client_validation_ca: Optional[pulumi.Input[Sequence[pulumi.Input['ValidationCAArgs']]]] = None):
        """
        Specification of the MTLSPolicy.
        :param pulumi.Input[Sequence[pulumi.Input['ValidationCAArgs']]] client_validation_ca:  Defines the mechanism to obtain the Certificate Authority certificate to validate the client certificate.
        """
        if client_validation_ca is not None:
            pulumi.set(__self__, "client_validation_ca", client_validation_ca)

    @property
    @pulumi.getter(name="clientValidationCa")
    def client_validation_ca(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ValidationCAArgs']]]]:
        """
         Defines the mechanism to obtain the Certificate Authority certificate to validate the client certificate.
        """
        return pulumi.get(self, "client_validation_ca")

    @client_validation_ca.setter
    def client_validation_ca(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ValidationCAArgs']]]]):
        pulumi.set(self, "client_validation_ca", value)


@pulumi.input_type
class RuleArgs:
    def __init__(__self__, *,
                 destinations: Optional[pulumi.Input[Sequence[pulumi.Input['DestinationArgs']]]] = None,
                 sources: Optional[pulumi.Input[Sequence[pulumi.Input['SourceArgs']]]] = None):
        """
        Specification of rules.
        :param pulumi.Input[Sequence[pulumi.Input['DestinationArgs']]] destinations: Optional. List of attributes for the traffic destination. All of the destinations must match. A destination is a match if a request matches all the specified hosts, ports, methods and headers. If not set, the action specified in the 'action' field will be applied without any rule checks for the destination.
        :param pulumi.Input[Sequence[pulumi.Input['SourceArgs']]] sources: Optional. List of attributes for the traffic source. All of the sources must match. A source is a match if both principals and ip_blocks match. If not set, the action specified in the 'action' field will be applied without any rule checks for the source.
        """
        if destinations is not None:
            pulumi.set(__self__, "destinations", destinations)
        if sources is not None:
            pulumi.set(__self__, "sources", sources)

    @property
    @pulumi.getter
    def destinations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['DestinationArgs']]]]:
        """
        Optional. List of attributes for the traffic destination. All of the destinations must match. A destination is a match if a request matches all the specified hosts, ports, methods and headers. If not set, the action specified in the 'action' field will be applied without any rule checks for the destination.
        """
        return pulumi.get(self, "destinations")

    @destinations.setter
    def destinations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['DestinationArgs']]]]):
        pulumi.set(self, "destinations", value)

    @property
    @pulumi.getter
    def sources(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['SourceArgs']]]]:
        """
        Optional. List of attributes for the traffic source. All of the sources must match. A source is a match if both principals and ip_blocks match. If not set, the action specified in the 'action' field will be applied without any rule checks for the source.
        """
        return pulumi.get(self, "sources")

    @sources.setter
    def sources(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['SourceArgs']]]]):
        pulumi.set(self, "sources", value)


@pulumi.input_type
class SourceArgs:
    def __init__(__self__, *,
                 ip_blocks: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 principals: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        Specification of traffic source attributes.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] ip_blocks: Optional. List of CIDR ranges to match based on source IP address. At least one IP block should match. Single IP (e.g., "1.2.3.4") and CIDR (e.g., "1.2.3.0/24") are supported. Authorization based on source IP alone should be avoided. The IP addresses of any load balancers or proxies should be considered untrusted.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] principals: Optional. List of peer identities to match for authorization. At least one principal should match. Each peer can be an exact match, or a prefix match (example, "namespace/*") or a suffix match (example, "*/service-account") or a presence match "*". Authorization based on the principal name without certificate validation (configured by ServerTlsPolicy resource) is considered insecure.
        """
        if ip_blocks is not None:
            pulumi.set(__self__, "ip_blocks", ip_blocks)
        if principals is not None:
            pulumi.set(__self__, "principals", principals)

    @property
    @pulumi.getter(name="ipBlocks")
    def ip_blocks(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Optional. List of CIDR ranges to match based on source IP address. At least one IP block should match. Single IP (e.g., "1.2.3.4") and CIDR (e.g., "1.2.3.0/24") are supported. Authorization based on source IP alone should be avoided. The IP addresses of any load balancers or proxies should be considered untrusted.
        """
        return pulumi.get(self, "ip_blocks")

    @ip_blocks.setter
    def ip_blocks(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "ip_blocks", value)

    @property
    @pulumi.getter
    def principals(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Optional. List of peer identities to match for authorization. At least one principal should match. Each peer can be an exact match, or a prefix match (example, "namespace/*") or a suffix match (example, "*/service-account") or a presence match "*". Authorization based on the principal name without certificate validation (configured by ServerTlsPolicy resource) is considered insecure.
        """
        return pulumi.get(self, "principals")

    @principals.setter
    def principals(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "principals", value)


@pulumi.input_type
class ValidationCAArgs:
    def __init__(__self__, *,
                 certificate_provider_instance: Optional[pulumi.Input['CertificateProviderInstanceArgs']] = None,
                 grpc_endpoint: Optional[pulumi.Input['GoogleCloudNetworksecurityV1beta1GrpcEndpointArgs']] = None):
        """
        Specification of ValidationCA. Defines the mechanism to obtain the Certificate Authority certificate to validate the peer certificate.
        :param pulumi.Input['CertificateProviderInstanceArgs'] certificate_provider_instance: The certificate provider instance specification that will be passed to the data plane, which will be used to load necessary credential information.
        :param pulumi.Input['GoogleCloudNetworksecurityV1beta1GrpcEndpointArgs'] grpc_endpoint: gRPC specific configuration to access the gRPC server to obtain the CA certificate.
        """
        if certificate_provider_instance is not None:
            pulumi.set(__self__, "certificate_provider_instance", certificate_provider_instance)
        if grpc_endpoint is not None:
            pulumi.set(__self__, "grpc_endpoint", grpc_endpoint)

    @property
    @pulumi.getter(name="certificateProviderInstance")
    def certificate_provider_instance(self) -> Optional[pulumi.Input['CertificateProviderInstanceArgs']]:
        """
        The certificate provider instance specification that will be passed to the data plane, which will be used to load necessary credential information.
        """
        return pulumi.get(self, "certificate_provider_instance")

    @certificate_provider_instance.setter
    def certificate_provider_instance(self, value: Optional[pulumi.Input['CertificateProviderInstanceArgs']]):
        pulumi.set(self, "certificate_provider_instance", value)

    @property
    @pulumi.getter(name="grpcEndpoint")
    def grpc_endpoint(self) -> Optional[pulumi.Input['GoogleCloudNetworksecurityV1beta1GrpcEndpointArgs']]:
        """
        gRPC specific configuration to access the gRPC server to obtain the CA certificate.
        """
        return pulumi.get(self, "grpc_endpoint")

    @grpc_endpoint.setter
    def grpc_endpoint(self, value: Optional[pulumi.Input['GoogleCloudNetworksecurityV1beta1GrpcEndpointArgs']]):
        pulumi.set(self, "grpc_endpoint", value)


