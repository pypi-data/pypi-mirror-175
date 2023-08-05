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
    'AnthosClusterArgs',
    'AuditConfigArgs',
    'AuditLogConfigArgs',
    'BindingArgs',
    'BuildArtifactArgs',
    'CloudRunLocationArgs',
    'DefaultPoolArgs',
    'ExecutionConfigArgs',
    'ExprArgs',
    'GkeClusterArgs',
    'PrivatePoolArgs',
    'SerialPipelineArgs',
    'StageArgs',
    'StandardArgs',
    'StrategyArgs',
]

@pulumi.input_type
class AnthosClusterArgs:
    def __init__(__self__, *,
                 membership: Optional[pulumi.Input[str]] = None):
        """
        Information specifying an Anthos Cluster.
        :param pulumi.Input[str] membership: Membership of the GKE Hub-registered cluster to which to apply the Skaffold configuration. Format is `projects/{project}/locations/{location}/memberships/{membership_name}`.
        """
        if membership is not None:
            pulumi.set(__self__, "membership", membership)

    @property
    @pulumi.getter
    def membership(self) -> Optional[pulumi.Input[str]]:
        """
        Membership of the GKE Hub-registered cluster to which to apply the Skaffold configuration. Format is `projects/{project}/locations/{location}/memberships/{membership_name}`.
        """
        return pulumi.get(self, "membership")

    @membership.setter
    def membership(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "membership", value)


@pulumi.input_type
class AuditConfigArgs:
    def __init__(__self__, *,
                 audit_log_configs: Optional[pulumi.Input[Sequence[pulumi.Input['AuditLogConfigArgs']]]] = None,
                 service: Optional[pulumi.Input[str]] = None):
        """
        Specifies the audit configuration for a service. The configuration determines which permission types are logged, and what identities, if any, are exempted from logging. An AuditConfig must have one or more AuditLogConfigs. If there are AuditConfigs for both `allServices` and a specific service, the union of the two AuditConfigs is used for that service: the log_types specified in each AuditConfig are enabled, and the exempted_members in each AuditLogConfig are exempted. Example Policy with multiple AuditConfigs: { "audit_configs": [ { "service": "allServices", "audit_log_configs": [ { "log_type": "DATA_READ", "exempted_members": [ "user:jose@example.com" ] }, { "log_type": "DATA_WRITE" }, { "log_type": "ADMIN_READ" } ] }, { "service": "sampleservice.googleapis.com", "audit_log_configs": [ { "log_type": "DATA_READ" }, { "log_type": "DATA_WRITE", "exempted_members": [ "user:aliya@example.com" ] } ] } ] } For sampleservice, this policy enables DATA_READ, DATA_WRITE and ADMIN_READ logging. It also exempts `jose@example.com` from DATA_READ logging, and `aliya@example.com` from DATA_WRITE logging.
        :param pulumi.Input[Sequence[pulumi.Input['AuditLogConfigArgs']]] audit_log_configs: The configuration for logging of each type of permission.
        :param pulumi.Input[str] service: Specifies a service that will be enabled for audit logging. For example, `storage.googleapis.com`, `cloudsql.googleapis.com`. `allServices` is a special value that covers all services.
        """
        if audit_log_configs is not None:
            pulumi.set(__self__, "audit_log_configs", audit_log_configs)
        if service is not None:
            pulumi.set(__self__, "service", service)

    @property
    @pulumi.getter(name="auditLogConfigs")
    def audit_log_configs(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['AuditLogConfigArgs']]]]:
        """
        The configuration for logging of each type of permission.
        """
        return pulumi.get(self, "audit_log_configs")

    @audit_log_configs.setter
    def audit_log_configs(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['AuditLogConfigArgs']]]]):
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
class AuditLogConfigArgs:
    def __init__(__self__, *,
                 exempted_members: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 log_type: Optional[pulumi.Input['AuditLogConfigLogType']] = None):
        """
        Provides the configuration for logging a type of permissions. Example: { "audit_log_configs": [ { "log_type": "DATA_READ", "exempted_members": [ "user:jose@example.com" ] }, { "log_type": "DATA_WRITE" } ] } This enables 'DATA_READ' and 'DATA_WRITE' logging, while exempting jose@example.com from DATA_READ logging.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] exempted_members: Specifies the identities that do not cause logging for this type of permission. Follows the same format of Binding.members.
        :param pulumi.Input['AuditLogConfigLogType'] log_type: The log type that this config enables.
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
    def log_type(self) -> Optional[pulumi.Input['AuditLogConfigLogType']]:
        """
        The log type that this config enables.
        """
        return pulumi.get(self, "log_type")

    @log_type.setter
    def log_type(self, value: Optional[pulumi.Input['AuditLogConfigLogType']]):
        pulumi.set(self, "log_type", value)


@pulumi.input_type
class BindingArgs:
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
class BuildArtifactArgs:
    def __init__(__self__, *,
                 image: Optional[pulumi.Input[str]] = None,
                 tag: Optional[pulumi.Input[str]] = None):
        """
        Description of an a image to use during Skaffold rendering.
        :param pulumi.Input[str] image: Image name in Skaffold configuration.
        :param pulumi.Input[str] tag: Image tag to use. This will generally be the full path to an image, such as "gcr.io/my-project/busybox:1.2.3" or "gcr.io/my-project/busybox@sha256:abc123".
        """
        if image is not None:
            pulumi.set(__self__, "image", image)
        if tag is not None:
            pulumi.set(__self__, "tag", tag)

    @property
    @pulumi.getter
    def image(self) -> Optional[pulumi.Input[str]]:
        """
        Image name in Skaffold configuration.
        """
        return pulumi.get(self, "image")

    @image.setter
    def image(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "image", value)

    @property
    @pulumi.getter
    def tag(self) -> Optional[pulumi.Input[str]]:
        """
        Image tag to use. This will generally be the full path to an image, such as "gcr.io/my-project/busybox:1.2.3" or "gcr.io/my-project/busybox@sha256:abc123".
        """
        return pulumi.get(self, "tag")

    @tag.setter
    def tag(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "tag", value)


@pulumi.input_type
class CloudRunLocationArgs:
    def __init__(__self__, *,
                 location: pulumi.Input[str]):
        """
        Information specifying where to deploy a Cloud Run Service.
        :param pulumi.Input[str] location: The location for the Cloud Run Service. Format must be `projects/{project}/locations/{location}`.
        """
        pulumi.set(__self__, "location", location)

    @property
    @pulumi.getter
    def location(self) -> pulumi.Input[str]:
        """
        The location for the Cloud Run Service. Format must be `projects/{project}/locations/{location}`.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: pulumi.Input[str]):
        pulumi.set(self, "location", value)


@pulumi.input_type
class DefaultPoolArgs:
    def __init__(__self__, *,
                 artifact_storage: Optional[pulumi.Input[str]] = None,
                 service_account: Optional[pulumi.Input[str]] = None):
        """
        Execution using the default Cloud Build pool.
        :param pulumi.Input[str] artifact_storage: Optional. Cloud Storage location where execution outputs should be stored. This can either be a bucket ("gs://my-bucket") or a path within a bucket ("gs://my-bucket/my-dir"). If unspecified, a default bucket located in the same region will be used.
        :param pulumi.Input[str] service_account: Optional. Google service account to use for execution. If unspecified, the project execution service account (-compute@developer.gserviceaccount.com) will be used.
        """
        if artifact_storage is not None:
            pulumi.set(__self__, "artifact_storage", artifact_storage)
        if service_account is not None:
            pulumi.set(__self__, "service_account", service_account)

    @property
    @pulumi.getter(name="artifactStorage")
    def artifact_storage(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. Cloud Storage location where execution outputs should be stored. This can either be a bucket ("gs://my-bucket") or a path within a bucket ("gs://my-bucket/my-dir"). If unspecified, a default bucket located in the same region will be used.
        """
        return pulumi.get(self, "artifact_storage")

    @artifact_storage.setter
    def artifact_storage(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "artifact_storage", value)

    @property
    @pulumi.getter(name="serviceAccount")
    def service_account(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. Google service account to use for execution. If unspecified, the project execution service account (-compute@developer.gserviceaccount.com) will be used.
        """
        return pulumi.get(self, "service_account")

    @service_account.setter
    def service_account(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service_account", value)


@pulumi.input_type
class ExecutionConfigArgs:
    def __init__(__self__, *,
                 usages: pulumi.Input[Sequence[pulumi.Input['ExecutionConfigUsagesItem']]],
                 artifact_storage: Optional[pulumi.Input[str]] = None,
                 default_pool: Optional[pulumi.Input['DefaultPoolArgs']] = None,
                 execution_timeout: Optional[pulumi.Input[str]] = None,
                 private_pool: Optional[pulumi.Input['PrivatePoolArgs']] = None,
                 service_account: Optional[pulumi.Input[str]] = None,
                 worker_pool: Optional[pulumi.Input[str]] = None):
        """
        Configuration of the environment to use when calling Skaffold.
        :param pulumi.Input[Sequence[pulumi.Input['ExecutionConfigUsagesItem']]] usages: Usages when this configuration should be applied.
        :param pulumi.Input[str] artifact_storage: Optional. Cloud Storage location in which to store execution outputs. This can either be a bucket ("gs://my-bucket") or a path within a bucket ("gs://my-bucket/my-dir"). If unspecified, a default bucket located in the same region will be used.
        :param pulumi.Input['DefaultPoolArgs'] default_pool: Optional. Use default Cloud Build pool.
        :param pulumi.Input[str] execution_timeout: Optional. Execution timeout for a Cloud Build Execution. This must be between 10m and 24h in seconds format. If unspecified, a default timeout of 1h is used.
        :param pulumi.Input['PrivatePoolArgs'] private_pool: Optional. Use private Cloud Build pool.
        :param pulumi.Input[str] service_account: Optional. Google service account to use for execution. If unspecified, the project execution service account (-compute@developer.gserviceaccount.com) is used.
        :param pulumi.Input[str] worker_pool: Optional. The resource name of the `WorkerPool`, with the format `projects/{project}/locations/{location}/workerPools/{worker_pool}`. If this optional field is unspecified, the default Cloud Build pool will be used.
        """
        pulumi.set(__self__, "usages", usages)
        if artifact_storage is not None:
            pulumi.set(__self__, "artifact_storage", artifact_storage)
        if default_pool is not None:
            pulumi.set(__self__, "default_pool", default_pool)
        if execution_timeout is not None:
            pulumi.set(__self__, "execution_timeout", execution_timeout)
        if private_pool is not None:
            pulumi.set(__self__, "private_pool", private_pool)
        if service_account is not None:
            pulumi.set(__self__, "service_account", service_account)
        if worker_pool is not None:
            pulumi.set(__self__, "worker_pool", worker_pool)

    @property
    @pulumi.getter
    def usages(self) -> pulumi.Input[Sequence[pulumi.Input['ExecutionConfigUsagesItem']]]:
        """
        Usages when this configuration should be applied.
        """
        return pulumi.get(self, "usages")

    @usages.setter
    def usages(self, value: pulumi.Input[Sequence[pulumi.Input['ExecutionConfigUsagesItem']]]):
        pulumi.set(self, "usages", value)

    @property
    @pulumi.getter(name="artifactStorage")
    def artifact_storage(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. Cloud Storage location in which to store execution outputs. This can either be a bucket ("gs://my-bucket") or a path within a bucket ("gs://my-bucket/my-dir"). If unspecified, a default bucket located in the same region will be used.
        """
        return pulumi.get(self, "artifact_storage")

    @artifact_storage.setter
    def artifact_storage(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "artifact_storage", value)

    @property
    @pulumi.getter(name="defaultPool")
    def default_pool(self) -> Optional[pulumi.Input['DefaultPoolArgs']]:
        """
        Optional. Use default Cloud Build pool.
        """
        return pulumi.get(self, "default_pool")

    @default_pool.setter
    def default_pool(self, value: Optional[pulumi.Input['DefaultPoolArgs']]):
        pulumi.set(self, "default_pool", value)

    @property
    @pulumi.getter(name="executionTimeout")
    def execution_timeout(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. Execution timeout for a Cloud Build Execution. This must be between 10m and 24h in seconds format. If unspecified, a default timeout of 1h is used.
        """
        return pulumi.get(self, "execution_timeout")

    @execution_timeout.setter
    def execution_timeout(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "execution_timeout", value)

    @property
    @pulumi.getter(name="privatePool")
    def private_pool(self) -> Optional[pulumi.Input['PrivatePoolArgs']]:
        """
        Optional. Use private Cloud Build pool.
        """
        return pulumi.get(self, "private_pool")

    @private_pool.setter
    def private_pool(self, value: Optional[pulumi.Input['PrivatePoolArgs']]):
        pulumi.set(self, "private_pool", value)

    @property
    @pulumi.getter(name="serviceAccount")
    def service_account(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. Google service account to use for execution. If unspecified, the project execution service account (-compute@developer.gserviceaccount.com) is used.
        """
        return pulumi.get(self, "service_account")

    @service_account.setter
    def service_account(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service_account", value)

    @property
    @pulumi.getter(name="workerPool")
    def worker_pool(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. The resource name of the `WorkerPool`, with the format `projects/{project}/locations/{location}/workerPools/{worker_pool}`. If this optional field is unspecified, the default Cloud Build pool will be used.
        """
        return pulumi.get(self, "worker_pool")

    @worker_pool.setter
    def worker_pool(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "worker_pool", value)


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
class GkeClusterArgs:
    def __init__(__self__, *,
                 cluster: Optional[pulumi.Input[str]] = None,
                 internal_ip: Optional[pulumi.Input[bool]] = None):
        """
        Information specifying a GKE Cluster.
        :param pulumi.Input[str] cluster: Information specifying a GKE Cluster. Format is `projects/{project_id}/locations/{location_id}/clusters/{cluster_id}.
        :param pulumi.Input[bool] internal_ip: Optional. If true, `cluster` is accessed using the private IP address of the control plane endpoint. Otherwise, the default IP address of the control plane endpoint is used. The default IP address is the private IP address for clusters with private control-plane endpoints and the public IP address otherwise. Only specify this option when `cluster` is a [private GKE cluster](https://cloud.google.com/kubernetes-engine/docs/concepts/private-cluster-concept).
        """
        if cluster is not None:
            pulumi.set(__self__, "cluster", cluster)
        if internal_ip is not None:
            pulumi.set(__self__, "internal_ip", internal_ip)

    @property
    @pulumi.getter
    def cluster(self) -> Optional[pulumi.Input[str]]:
        """
        Information specifying a GKE Cluster. Format is `projects/{project_id}/locations/{location_id}/clusters/{cluster_id}.
        """
        return pulumi.get(self, "cluster")

    @cluster.setter
    def cluster(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cluster", value)

    @property
    @pulumi.getter(name="internalIp")
    def internal_ip(self) -> Optional[pulumi.Input[bool]]:
        """
        Optional. If true, `cluster` is accessed using the private IP address of the control plane endpoint. Otherwise, the default IP address of the control plane endpoint is used. The default IP address is the private IP address for clusters with private control-plane endpoints and the public IP address otherwise. Only specify this option when `cluster` is a [private GKE cluster](https://cloud.google.com/kubernetes-engine/docs/concepts/private-cluster-concept).
        """
        return pulumi.get(self, "internal_ip")

    @internal_ip.setter
    def internal_ip(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "internal_ip", value)


@pulumi.input_type
class PrivatePoolArgs:
    def __init__(__self__, *,
                 worker_pool: pulumi.Input[str],
                 artifact_storage: Optional[pulumi.Input[str]] = None,
                 service_account: Optional[pulumi.Input[str]] = None):
        """
        Execution using a private Cloud Build pool.
        :param pulumi.Input[str] worker_pool: Resource name of the Cloud Build worker pool to use. The format is `projects/{project}/locations/{location}/workerPools/{pool}`.
        :param pulumi.Input[str] artifact_storage: Optional. Cloud Storage location where execution outputs should be stored. This can either be a bucket ("gs://my-bucket") or a path within a bucket ("gs://my-bucket/my-dir"). If unspecified, a default bucket located in the same region will be used.
        :param pulumi.Input[str] service_account: Optional. Google service account to use for execution. If unspecified, the project execution service account (-compute@developer.gserviceaccount.com) will be used.
        """
        pulumi.set(__self__, "worker_pool", worker_pool)
        if artifact_storage is not None:
            pulumi.set(__self__, "artifact_storage", artifact_storage)
        if service_account is not None:
            pulumi.set(__self__, "service_account", service_account)

    @property
    @pulumi.getter(name="workerPool")
    def worker_pool(self) -> pulumi.Input[str]:
        """
        Resource name of the Cloud Build worker pool to use. The format is `projects/{project}/locations/{location}/workerPools/{pool}`.
        """
        return pulumi.get(self, "worker_pool")

    @worker_pool.setter
    def worker_pool(self, value: pulumi.Input[str]):
        pulumi.set(self, "worker_pool", value)

    @property
    @pulumi.getter(name="artifactStorage")
    def artifact_storage(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. Cloud Storage location where execution outputs should be stored. This can either be a bucket ("gs://my-bucket") or a path within a bucket ("gs://my-bucket/my-dir"). If unspecified, a default bucket located in the same region will be used.
        """
        return pulumi.get(self, "artifact_storage")

    @artifact_storage.setter
    def artifact_storage(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "artifact_storage", value)

    @property
    @pulumi.getter(name="serviceAccount")
    def service_account(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. Google service account to use for execution. If unspecified, the project execution service account (-compute@developer.gserviceaccount.com) will be used.
        """
        return pulumi.get(self, "service_account")

    @service_account.setter
    def service_account(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service_account", value)


@pulumi.input_type
class SerialPipelineArgs:
    def __init__(__self__, *,
                 stages: Optional[pulumi.Input[Sequence[pulumi.Input['StageArgs']]]] = None):
        """
        SerialPipeline defines a sequential set of stages for a `DeliveryPipeline`.
        :param pulumi.Input[Sequence[pulumi.Input['StageArgs']]] stages: Each stage specifies configuration for a `Target`. The ordering of this list defines the promotion flow.
        """
        if stages is not None:
            pulumi.set(__self__, "stages", stages)

    @property
    @pulumi.getter
    def stages(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['StageArgs']]]]:
        """
        Each stage specifies configuration for a `Target`. The ordering of this list defines the promotion flow.
        """
        return pulumi.get(self, "stages")

    @stages.setter
    def stages(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['StageArgs']]]]):
        pulumi.set(self, "stages", value)


@pulumi.input_type
class StageArgs:
    def __init__(__self__, *,
                 profiles: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 strategy: Optional[pulumi.Input['StrategyArgs']] = None,
                 target_id: Optional[pulumi.Input[str]] = None):
        """
        Stage specifies a location to which to deploy.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] profiles: Skaffold profiles to use when rendering the manifest for this stage's `Target`.
        :param pulumi.Input['StrategyArgs'] strategy: Optional. The strategy to use for a `Rollout` to this stage.
        :param pulumi.Input[str] target_id: The target_id to which this stage points. This field refers exclusively to the last segment of a target name. For example, this field would just be `my-target` (rather than `projects/project/locations/location/targets/my-target`). The location of the `Target` is inferred to be the same as the location of the `DeliveryPipeline` that contains this `Stage`.
        """
        if profiles is not None:
            pulumi.set(__self__, "profiles", profiles)
        if strategy is not None:
            pulumi.set(__self__, "strategy", strategy)
        if target_id is not None:
            pulumi.set(__self__, "target_id", target_id)

    @property
    @pulumi.getter
    def profiles(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Skaffold profiles to use when rendering the manifest for this stage's `Target`.
        """
        return pulumi.get(self, "profiles")

    @profiles.setter
    def profiles(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "profiles", value)

    @property
    @pulumi.getter
    def strategy(self) -> Optional[pulumi.Input['StrategyArgs']]:
        """
        Optional. The strategy to use for a `Rollout` to this stage.
        """
        return pulumi.get(self, "strategy")

    @strategy.setter
    def strategy(self, value: Optional[pulumi.Input['StrategyArgs']]):
        pulumi.set(self, "strategy", value)

    @property
    @pulumi.getter(name="targetId")
    def target_id(self) -> Optional[pulumi.Input[str]]:
        """
        The target_id to which this stage points. This field refers exclusively to the last segment of a target name. For example, this field would just be `my-target` (rather than `projects/project/locations/location/targets/my-target`). The location of the `Target` is inferred to be the same as the location of the `DeliveryPipeline` that contains this `Stage`.
        """
        return pulumi.get(self, "target_id")

    @target_id.setter
    def target_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "target_id", value)


@pulumi.input_type
class StandardArgs:
    def __init__(__self__, *,
                 verify: Optional[pulumi.Input[bool]] = None):
        """
        Standard represents the standard deployment strategy.
        :param pulumi.Input[bool] verify: Whether to verify a deployment.
        """
        if verify is not None:
            pulumi.set(__self__, "verify", verify)

    @property
    @pulumi.getter
    def verify(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether to verify a deployment.
        """
        return pulumi.get(self, "verify")

    @verify.setter
    def verify(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "verify", value)


@pulumi.input_type
class StrategyArgs:
    def __init__(__self__, *,
                 standard: Optional[pulumi.Input['StandardArgs']] = None):
        """
        Strategy contains deployment strategy information.
        :param pulumi.Input['StandardArgs'] standard: Standard deployment strategy executes a single deploy and allows verifying the deployment.
        """
        if standard is not None:
            pulumi.set(__self__, "standard", standard)

    @property
    @pulumi.getter
    def standard(self) -> Optional[pulumi.Input['StandardArgs']]:
        """
        Standard deployment strategy executes a single deploy and allows verifying the deployment.
        """
        return pulumi.get(self, "standard")

    @standard.setter
    def standard(self, value: Optional[pulumi.Input['StandardArgs']]):
        pulumi.set(self, "standard", value)


