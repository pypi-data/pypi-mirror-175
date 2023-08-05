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

__all__ = [
    'GetServiceResult',
    'AwaitableGetServiceResult',
    'get_service',
    'get_service_output',
]

@pulumi.output_type
class GetServiceResult:
    def __init__(__self__, app_engine=None, basic_service=None, cloud_endpoints=None, cloud_run=None, cluster_istio=None, custom=None, display_name=None, gke_namespace=None, gke_service=None, gke_workload=None, istio_canonical_service=None, mesh_istio=None, name=None, telemetry=None, user_labels=None):
        if app_engine and not isinstance(app_engine, dict):
            raise TypeError("Expected argument 'app_engine' to be a dict")
        pulumi.set(__self__, "app_engine", app_engine)
        if basic_service and not isinstance(basic_service, dict):
            raise TypeError("Expected argument 'basic_service' to be a dict")
        pulumi.set(__self__, "basic_service", basic_service)
        if cloud_endpoints and not isinstance(cloud_endpoints, dict):
            raise TypeError("Expected argument 'cloud_endpoints' to be a dict")
        pulumi.set(__self__, "cloud_endpoints", cloud_endpoints)
        if cloud_run and not isinstance(cloud_run, dict):
            raise TypeError("Expected argument 'cloud_run' to be a dict")
        pulumi.set(__self__, "cloud_run", cloud_run)
        if cluster_istio and not isinstance(cluster_istio, dict):
            raise TypeError("Expected argument 'cluster_istio' to be a dict")
        pulumi.set(__self__, "cluster_istio", cluster_istio)
        if custom and not isinstance(custom, dict):
            raise TypeError("Expected argument 'custom' to be a dict")
        pulumi.set(__self__, "custom", custom)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if gke_namespace and not isinstance(gke_namespace, dict):
            raise TypeError("Expected argument 'gke_namespace' to be a dict")
        pulumi.set(__self__, "gke_namespace", gke_namespace)
        if gke_service and not isinstance(gke_service, dict):
            raise TypeError("Expected argument 'gke_service' to be a dict")
        pulumi.set(__self__, "gke_service", gke_service)
        if gke_workload and not isinstance(gke_workload, dict):
            raise TypeError("Expected argument 'gke_workload' to be a dict")
        pulumi.set(__self__, "gke_workload", gke_workload)
        if istio_canonical_service and not isinstance(istio_canonical_service, dict):
            raise TypeError("Expected argument 'istio_canonical_service' to be a dict")
        pulumi.set(__self__, "istio_canonical_service", istio_canonical_service)
        if mesh_istio and not isinstance(mesh_istio, dict):
            raise TypeError("Expected argument 'mesh_istio' to be a dict")
        pulumi.set(__self__, "mesh_istio", mesh_istio)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if telemetry and not isinstance(telemetry, dict):
            raise TypeError("Expected argument 'telemetry' to be a dict")
        pulumi.set(__self__, "telemetry", telemetry)
        if user_labels and not isinstance(user_labels, dict):
            raise TypeError("Expected argument 'user_labels' to be a dict")
        pulumi.set(__self__, "user_labels", user_labels)

    @property
    @pulumi.getter(name="appEngine")
    def app_engine(self) -> 'outputs.AppEngineResponse':
        """
        Type used for App Engine services.
        """
        return pulumi.get(self, "app_engine")

    @property
    @pulumi.getter(name="basicService")
    def basic_service(self) -> 'outputs.BasicServiceResponse':
        """
        Message that contains the service type and service labels of this service if it is a basic service. Documentation and examples here (https://cloud.google.com/stackdriver/docs/solutions/slo-monitoring/api/api-structures#basic-svc-w-basic-sli).
        """
        return pulumi.get(self, "basic_service")

    @property
    @pulumi.getter(name="cloudEndpoints")
    def cloud_endpoints(self) -> 'outputs.CloudEndpointsResponse':
        """
        Type used for Cloud Endpoints services.
        """
        return pulumi.get(self, "cloud_endpoints")

    @property
    @pulumi.getter(name="cloudRun")
    def cloud_run(self) -> 'outputs.CloudRunResponse':
        """
        Type used for Cloud Run services.
        """
        return pulumi.get(self, "cloud_run")

    @property
    @pulumi.getter(name="clusterIstio")
    def cluster_istio(self) -> 'outputs.ClusterIstioResponse':
        """
        Type used for Istio services that live in a Kubernetes cluster.
        """
        return pulumi.get(self, "cluster_istio")

    @property
    @pulumi.getter
    def custom(self) -> 'outputs.CustomResponse':
        """
        Custom service type.
        """
        return pulumi.get(self, "custom")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> str:
        """
        Name used for UI elements listing this Service.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter(name="gkeNamespace")
    def gke_namespace(self) -> 'outputs.GkeNamespaceResponse':
        """
        Type used for GKE Namespaces.
        """
        return pulumi.get(self, "gke_namespace")

    @property
    @pulumi.getter(name="gkeService")
    def gke_service(self) -> 'outputs.GkeServiceResponse':
        """
        Type used for GKE Services (the Kubernetes concept of a service).
        """
        return pulumi.get(self, "gke_service")

    @property
    @pulumi.getter(name="gkeWorkload")
    def gke_workload(self) -> 'outputs.GkeWorkloadResponse':
        """
        Type used for GKE Workloads.
        """
        return pulumi.get(self, "gke_workload")

    @property
    @pulumi.getter(name="istioCanonicalService")
    def istio_canonical_service(self) -> 'outputs.IstioCanonicalServiceResponse':
        """
        Type used for canonical services scoped to an Istio mesh. Metrics for Istio are documented here (https://istio.io/latest/docs/reference/config/metrics/)
        """
        return pulumi.get(self, "istio_canonical_service")

    @property
    @pulumi.getter(name="meshIstio")
    def mesh_istio(self) -> 'outputs.MeshIstioResponse':
        """
        Type used for Istio services scoped to an Istio mesh.
        """
        return pulumi.get(self, "mesh_istio")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name for this Service. The format is: projects/[PROJECT_ID_OR_NUMBER]/services/[SERVICE_ID] 
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def telemetry(self) -> 'outputs.TelemetryResponse':
        """
        Configuration for how to query telemetry on a Service.
        """
        return pulumi.get(self, "telemetry")

    @property
    @pulumi.getter(name="userLabels")
    def user_labels(self) -> Mapping[str, str]:
        """
        Labels which have been used to annotate the service. Label keys must start with a letter. Label keys and values may contain lowercase letters, numbers, underscores, and dashes. Label keys and values have a maximum length of 63 characters, and must be less than 128 bytes in size. Up to 64 label entries may be stored. For labels which do not have a semantic value, the empty string may be supplied for the label value.
        """
        return pulumi.get(self, "user_labels")


class AwaitableGetServiceResult(GetServiceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetServiceResult(
            app_engine=self.app_engine,
            basic_service=self.basic_service,
            cloud_endpoints=self.cloud_endpoints,
            cloud_run=self.cloud_run,
            cluster_istio=self.cluster_istio,
            custom=self.custom,
            display_name=self.display_name,
            gke_namespace=self.gke_namespace,
            gke_service=self.gke_service,
            gke_workload=self.gke_workload,
            istio_canonical_service=self.istio_canonical_service,
            mesh_istio=self.mesh_istio,
            name=self.name,
            telemetry=self.telemetry,
            user_labels=self.user_labels)


def get_service(service_id: Optional[str] = None,
                v3_id: Optional[str] = None,
                v3_id1: Optional[str] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetServiceResult:
    """
    Get the named Service.
    """
    __args__ = dict()
    __args__['serviceId'] = service_id
    __args__['v3Id'] = v3_id
    __args__['v3Id1'] = v3_id1
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('google-native:monitoring/v3:getService', __args__, opts=opts, typ=GetServiceResult).value

    return AwaitableGetServiceResult(
        app_engine=__ret__.app_engine,
        basic_service=__ret__.basic_service,
        cloud_endpoints=__ret__.cloud_endpoints,
        cloud_run=__ret__.cloud_run,
        cluster_istio=__ret__.cluster_istio,
        custom=__ret__.custom,
        display_name=__ret__.display_name,
        gke_namespace=__ret__.gke_namespace,
        gke_service=__ret__.gke_service,
        gke_workload=__ret__.gke_workload,
        istio_canonical_service=__ret__.istio_canonical_service,
        mesh_istio=__ret__.mesh_istio,
        name=__ret__.name,
        telemetry=__ret__.telemetry,
        user_labels=__ret__.user_labels)


@_utilities.lift_output_func(get_service)
def get_service_output(service_id: Optional[pulumi.Input[str]] = None,
                       v3_id: Optional[pulumi.Input[str]] = None,
                       v3_id1: Optional[pulumi.Input[str]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetServiceResult]:
    """
    Get the named Service.
    """
    ...
