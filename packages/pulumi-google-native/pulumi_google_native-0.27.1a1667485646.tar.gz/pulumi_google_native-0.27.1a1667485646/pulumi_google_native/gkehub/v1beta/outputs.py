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
    'AnthosObservabilityFeatureSpecResponse',
    'AnthosObservabilityMembershipSpecResponse',
    'AppDevExperienceFeatureSpecResponse',
    'AppDevExperienceFeatureStateResponse',
    'AuditConfigResponse',
    'AuditLogConfigResponse',
    'BindingResponse',
    'CommonFeatureSpecResponse',
    'CommonFeatureStateResponse',
    'ExprResponse',
    'FeatureResourceStateResponse',
    'FeatureStateResponse',
    'MultiClusterIngressFeatureSpecResponse',
    'StatusResponse',
]

@pulumi.output_type
class AnthosObservabilityFeatureSpecResponse(dict):
    """
    **Anthos Observability**: Spec
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "defaultMembershipSpec":
            suggest = "default_membership_spec"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AnthosObservabilityFeatureSpecResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AnthosObservabilityFeatureSpecResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AnthosObservabilityFeatureSpecResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 default_membership_spec: 'outputs.AnthosObservabilityMembershipSpecResponse'):
        """
        **Anthos Observability**: Spec
        :param 'AnthosObservabilityMembershipSpecResponse' default_membership_spec: Default membership spec for unconfigured memberships
        """
        pulumi.set(__self__, "default_membership_spec", default_membership_spec)

    @property
    @pulumi.getter(name="defaultMembershipSpec")
    def default_membership_spec(self) -> 'outputs.AnthosObservabilityMembershipSpecResponse':
        """
        Default membership spec for unconfigured memberships
        """
        return pulumi.get(self, "default_membership_spec")


@pulumi.output_type
class AnthosObservabilityMembershipSpecResponse(dict):
    """
    **Anthosobservability**: Per-Membership Feature spec.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "doNotOptimizeMetrics":
            suggest = "do_not_optimize_metrics"
        elif key == "enableStackdriverOnApplications":
            suggest = "enable_stackdriver_on_applications"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AnthosObservabilityMembershipSpecResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AnthosObservabilityMembershipSpecResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AnthosObservabilityMembershipSpecResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 do_not_optimize_metrics: bool,
                 enable_stackdriver_on_applications: bool,
                 version: str):
        """
        **Anthosobservability**: Per-Membership Feature spec.
        :param bool do_not_optimize_metrics: Use full of metrics rather than optimized metrics. See https://cloud.google.com/anthos/clusters/docs/on-prem/1.8/concepts/logging-and-monitoring#optimized_metrics_default_metrics
        :param bool enable_stackdriver_on_applications: Enable collecting and reporting metrics and logs from user apps.
        :param str version: the version of stackdriver operator used by this feature
        """
        pulumi.set(__self__, "do_not_optimize_metrics", do_not_optimize_metrics)
        pulumi.set(__self__, "enable_stackdriver_on_applications", enable_stackdriver_on_applications)
        pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter(name="doNotOptimizeMetrics")
    def do_not_optimize_metrics(self) -> bool:
        """
        Use full of metrics rather than optimized metrics. See https://cloud.google.com/anthos/clusters/docs/on-prem/1.8/concepts/logging-and-monitoring#optimized_metrics_default_metrics
        """
        return pulumi.get(self, "do_not_optimize_metrics")

    @property
    @pulumi.getter(name="enableStackdriverOnApplications")
    def enable_stackdriver_on_applications(self) -> bool:
        """
        Enable collecting and reporting metrics and logs from user apps.
        """
        return pulumi.get(self, "enable_stackdriver_on_applications")

    @property
    @pulumi.getter
    def version(self) -> str:
        """
        the version of stackdriver operator used by this feature
        """
        return pulumi.get(self, "version")


@pulumi.output_type
class AppDevExperienceFeatureSpecResponse(dict):
    """
    Spec for App Dev Experience Feature.
    """
    def __init__(__self__):
        """
        Spec for App Dev Experience Feature.
        """
        pass


@pulumi.output_type
class AppDevExperienceFeatureStateResponse(dict):
    """
    State for App Dev Exp Feature.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "networkingInstallSucceeded":
            suggest = "networking_install_succeeded"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AppDevExperienceFeatureStateResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AppDevExperienceFeatureStateResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AppDevExperienceFeatureStateResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 networking_install_succeeded: 'outputs.StatusResponse'):
        """
        State for App Dev Exp Feature.
        :param 'StatusResponse' networking_install_succeeded: Status of subcomponent that detects configured Service Mesh resources.
        """
        pulumi.set(__self__, "networking_install_succeeded", networking_install_succeeded)

    @property
    @pulumi.getter(name="networkingInstallSucceeded")
    def networking_install_succeeded(self) -> 'outputs.StatusResponse':
        """
        Status of subcomponent that detects configured Service Mesh resources.
        """
        return pulumi.get(self, "networking_install_succeeded")


@pulumi.output_type
class AuditConfigResponse(dict):
    """
    Specifies the audit configuration for a service. The configuration determines which permission types are logged, and what identities, if any, are exempted from logging. An AuditConfig must have one or more AuditLogConfigs. If there are AuditConfigs for both `allServices` and a specific service, the union of the two AuditConfigs is used for that service: the log_types specified in each AuditConfig are enabled, and the exempted_members in each AuditLogConfig are exempted. Example Policy with multiple AuditConfigs: { "audit_configs": [ { "service": "allServices", "audit_log_configs": [ { "log_type": "DATA_READ", "exempted_members": [ "user:jose@example.com" ] }, { "log_type": "DATA_WRITE" }, { "log_type": "ADMIN_READ" } ] }, { "service": "sampleservice.googleapis.com", "audit_log_configs": [ { "log_type": "DATA_READ" }, { "log_type": "DATA_WRITE", "exempted_members": [ "user:aliya@example.com" ] } ] } ] } For sampleservice, this policy enables DATA_READ, DATA_WRITE and ADMIN_READ logging. It also exempts `jose@example.com` from DATA_READ logging, and `aliya@example.com` from DATA_WRITE logging.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "auditLogConfigs":
            suggest = "audit_log_configs"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AuditConfigResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AuditConfigResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AuditConfigResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 audit_log_configs: Sequence['outputs.AuditLogConfigResponse'],
                 service: str):
        """
        Specifies the audit configuration for a service. The configuration determines which permission types are logged, and what identities, if any, are exempted from logging. An AuditConfig must have one or more AuditLogConfigs. If there are AuditConfigs for both `allServices` and a specific service, the union of the two AuditConfigs is used for that service: the log_types specified in each AuditConfig are enabled, and the exempted_members in each AuditLogConfig are exempted. Example Policy with multiple AuditConfigs: { "audit_configs": [ { "service": "allServices", "audit_log_configs": [ { "log_type": "DATA_READ", "exempted_members": [ "user:jose@example.com" ] }, { "log_type": "DATA_WRITE" }, { "log_type": "ADMIN_READ" } ] }, { "service": "sampleservice.googleapis.com", "audit_log_configs": [ { "log_type": "DATA_READ" }, { "log_type": "DATA_WRITE", "exempted_members": [ "user:aliya@example.com" ] } ] } ] } For sampleservice, this policy enables DATA_READ, DATA_WRITE and ADMIN_READ logging. It also exempts `jose@example.com` from DATA_READ logging, and `aliya@example.com` from DATA_WRITE logging.
        :param Sequence['AuditLogConfigResponse'] audit_log_configs: The configuration for logging of each type of permission.
        :param str service: Specifies a service that will be enabled for audit logging. For example, `storage.googleapis.com`, `cloudsql.googleapis.com`. `allServices` is a special value that covers all services.
        """
        pulumi.set(__self__, "audit_log_configs", audit_log_configs)
        pulumi.set(__self__, "service", service)

    @property
    @pulumi.getter(name="auditLogConfigs")
    def audit_log_configs(self) -> Sequence['outputs.AuditLogConfigResponse']:
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
class AuditLogConfigResponse(dict):
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
            pulumi.log.warn(f"Key '{key}' not found in AuditLogConfigResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AuditLogConfigResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AuditLogConfigResponse.__key_warning(key)
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
class BindingResponse(dict):
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
class CommonFeatureSpecResponse(dict):
    """
    CommonFeatureSpec contains Hub-wide configuration information
    """
    def __init__(__self__, *,
                 anthosobservability: 'outputs.AnthosObservabilityFeatureSpecResponse',
                 appdevexperience: 'outputs.AppDevExperienceFeatureSpecResponse',
                 multiclusteringress: 'outputs.MultiClusterIngressFeatureSpecResponse'):
        """
        CommonFeatureSpec contains Hub-wide configuration information
        :param 'AnthosObservabilityFeatureSpecResponse' anthosobservability: Anthos Observability spec
        :param 'AppDevExperienceFeatureSpecResponse' appdevexperience: Appdevexperience specific spec.
        :param 'MultiClusterIngressFeatureSpecResponse' multiclusteringress: Multicluster Ingress-specific spec.
        """
        pulumi.set(__self__, "anthosobservability", anthosobservability)
        pulumi.set(__self__, "appdevexperience", appdevexperience)
        pulumi.set(__self__, "multiclusteringress", multiclusteringress)

    @property
    @pulumi.getter
    def anthosobservability(self) -> 'outputs.AnthosObservabilityFeatureSpecResponse':
        """
        Anthos Observability spec
        """
        return pulumi.get(self, "anthosobservability")

    @property
    @pulumi.getter
    def appdevexperience(self) -> 'outputs.AppDevExperienceFeatureSpecResponse':
        """
        Appdevexperience specific spec.
        """
        return pulumi.get(self, "appdevexperience")

    @property
    @pulumi.getter
    def multiclusteringress(self) -> 'outputs.MultiClusterIngressFeatureSpecResponse':
        """
        Multicluster Ingress-specific spec.
        """
        return pulumi.get(self, "multiclusteringress")


@pulumi.output_type
class CommonFeatureStateResponse(dict):
    """
    CommonFeatureState contains Hub-wide Feature status information.
    """
    def __init__(__self__, *,
                 appdevexperience: 'outputs.AppDevExperienceFeatureStateResponse',
                 state: 'outputs.FeatureStateResponse'):
        """
        CommonFeatureState contains Hub-wide Feature status information.
        :param 'AppDevExperienceFeatureStateResponse' appdevexperience: Appdevexperience specific state.
        :param 'FeatureStateResponse' state: The "running state" of the Feature in this Hub.
        """
        pulumi.set(__self__, "appdevexperience", appdevexperience)
        pulumi.set(__self__, "state", state)

    @property
    @pulumi.getter
    def appdevexperience(self) -> 'outputs.AppDevExperienceFeatureStateResponse':
        """
        Appdevexperience specific state.
        """
        return pulumi.get(self, "appdevexperience")

    @property
    @pulumi.getter
    def state(self) -> 'outputs.FeatureStateResponse':
        """
        The "running state" of the Feature in this Hub.
        """
        return pulumi.get(self, "state")


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
class FeatureResourceStateResponse(dict):
    """
    FeatureResourceState describes the state of a Feature *resource* in the GkeHub API. See `FeatureState` for the "running state" of the Feature in the Hub and across Memberships.
    """
    def __init__(__self__, *,
                 state: str):
        """
        FeatureResourceState describes the state of a Feature *resource* in the GkeHub API. See `FeatureState` for the "running state" of the Feature in the Hub and across Memberships.
        :param str state: The current state of the Feature resource in the Hub API.
        """
        pulumi.set(__self__, "state", state)

    @property
    @pulumi.getter
    def state(self) -> str:
        """
        The current state of the Feature resource in the Hub API.
        """
        return pulumi.get(self, "state")


@pulumi.output_type
class FeatureStateResponse(dict):
    """
    FeatureState describes the high-level state of a Feature. It may be used to describe a Feature's state at the environ-level, or per-membershop, depending on the context.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "updateTime":
            suggest = "update_time"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in FeatureStateResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        FeatureStateResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        FeatureStateResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 code: str,
                 description: str,
                 update_time: str):
        """
        FeatureState describes the high-level state of a Feature. It may be used to describe a Feature's state at the environ-level, or per-membershop, depending on the context.
        :param str code: The high-level, machine-readable status of this Feature.
        :param str description: A human-readable description of the current status.
        :param str update_time: The time this status and any related Feature-specific details were updated.
        """
        pulumi.set(__self__, "code", code)
        pulumi.set(__self__, "description", description)
        pulumi.set(__self__, "update_time", update_time)

    @property
    @pulumi.getter
    def code(self) -> str:
        """
        The high-level, machine-readable status of this Feature.
        """
        return pulumi.get(self, "code")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        A human-readable description of the current status.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> str:
        """
        The time this status and any related Feature-specific details were updated.
        """
        return pulumi.get(self, "update_time")


@pulumi.output_type
class MultiClusterIngressFeatureSpecResponse(dict):
    """
    **Multi-cluster Ingress**: The configuration for the MultiClusterIngress feature.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "configMembership":
            suggest = "config_membership"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in MultiClusterIngressFeatureSpecResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        MultiClusterIngressFeatureSpecResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        MultiClusterIngressFeatureSpecResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 billing: str,
                 config_membership: str):
        """
        **Multi-cluster Ingress**: The configuration for the MultiClusterIngress feature.
        :param str billing: Deprecated: This field will be ignored and should not be set. Customer's billing structure.
        :param str config_membership: Fully-qualified Membership name which hosts the MultiClusterIngress CRD. Example: `projects/foo-proj/locations/global/memberships/bar`
        """
        pulumi.set(__self__, "billing", billing)
        pulumi.set(__self__, "config_membership", config_membership)

    @property
    @pulumi.getter
    def billing(self) -> str:
        """
        Deprecated: This field will be ignored and should not be set. Customer's billing structure.
        """
        return pulumi.get(self, "billing")

    @property
    @pulumi.getter(name="configMembership")
    def config_membership(self) -> str:
        """
        Fully-qualified Membership name which hosts the MultiClusterIngress CRD. Example: `projects/foo-proj/locations/global/memberships/bar`
        """
        return pulumi.get(self, "config_membership")


@pulumi.output_type
class StatusResponse(dict):
    """
    Status specifies state for the subcomponent.
    """
    def __init__(__self__, *,
                 code: str,
                 description: str):
        """
        Status specifies state for the subcomponent.
        :param str code: Code specifies AppDevExperienceFeature's subcomponent ready state.
        :param str description: Description is populated if Code is Failed, explaining why it has failed.
        """
        pulumi.set(__self__, "code", code)
        pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter
    def code(self) -> str:
        """
        Code specifies AppDevExperienceFeature's subcomponent ready state.
        """
        return pulumi.get(self, "code")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        Description is populated if Code is Failed, explaining why it has failed.
        """
        return pulumi.get(self, "description")


