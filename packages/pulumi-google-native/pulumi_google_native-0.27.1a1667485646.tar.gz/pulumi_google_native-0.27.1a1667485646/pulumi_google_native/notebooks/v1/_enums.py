# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'AcceleratorConfigType',
    'ExecutionTemplateJobType',
    'ExecutionTemplateScaleTier',
    'InstanceBootDiskType',
    'InstanceDataDiskType',
    'InstanceDiskEncryption',
    'InstanceNicType',
    'LocalDiskInitializeParamsDiskType',
    'ReservationAffinityConsumeReservationType',
    'RuntimeAcceleratorConfigType',
    'RuntimeAccessConfigAccessType',
    'RuntimeSoftwareConfigPostStartupScriptBehavior',
    'ScheduleState',
    'SchedulerAcceleratorConfigType',
    'UpgradeHistoryEntryAction',
    'UpgradeHistoryEntryState',
    'VirtualMachineConfigNicType',
]


class AcceleratorConfigType(str, Enum):
    """
    Type of this accelerator.
    """
    ACCELERATOR_TYPE_UNSPECIFIED = "ACCELERATOR_TYPE_UNSPECIFIED"
    """
    Accelerator type is not specified.
    """
    NVIDIA_TESLA_K80 = "NVIDIA_TESLA_K80"
    """
    Accelerator type is Nvidia Tesla K80.
    """
    NVIDIA_TESLA_P100 = "NVIDIA_TESLA_P100"
    """
    Accelerator type is Nvidia Tesla P100.
    """
    NVIDIA_TESLA_V100 = "NVIDIA_TESLA_V100"
    """
    Accelerator type is Nvidia Tesla V100.
    """
    NVIDIA_TESLA_P4 = "NVIDIA_TESLA_P4"
    """
    Accelerator type is Nvidia Tesla P4.
    """
    NVIDIA_TESLA_T4 = "NVIDIA_TESLA_T4"
    """
    Accelerator type is Nvidia Tesla T4.
    """
    NVIDIA_TESLA_A100 = "NVIDIA_TESLA_A100"
    """
    Accelerator type is Nvidia Tesla A100.
    """
    NVIDIA_TESLA_T4_VWS = "NVIDIA_TESLA_T4_VWS"
    """
    Accelerator type is NVIDIA Tesla T4 Virtual Workstations.
    """
    NVIDIA_TESLA_P100_VWS = "NVIDIA_TESLA_P100_VWS"
    """
    Accelerator type is NVIDIA Tesla P100 Virtual Workstations.
    """
    NVIDIA_TESLA_P4_VWS = "NVIDIA_TESLA_P4_VWS"
    """
    Accelerator type is NVIDIA Tesla P4 Virtual Workstations.
    """
    TPU_V2 = "TPU_V2"
    """
    (Coming soon) Accelerator type is TPU V2.
    """
    TPU_V3 = "TPU_V3"
    """
    (Coming soon) Accelerator type is TPU V3.
    """


class ExecutionTemplateJobType(str, Enum):
    """
    The type of Job to be used on this execution.
    """
    JOB_TYPE_UNSPECIFIED = "JOB_TYPE_UNSPECIFIED"
    """
    No type specified.
    """
    VERTEX_AI = "VERTEX_AI"
    """
    Custom Job in `aiplatform.googleapis.com`. Default value for an execution.
    """
    DATAPROC = "DATAPROC"
    """
    Run execution on a cluster with Dataproc as a job. https://cloud.google.com/dataproc/docs/reference/rest/v1/projects.regions.jobs
    """


class ExecutionTemplateScaleTier(str, Enum):
    """
    Required. Scale tier of the hardware used for notebook execution. DEPRECATED Will be discontinued. As right now only CUSTOM is supported.
    """
    SCALE_TIER_UNSPECIFIED = "SCALE_TIER_UNSPECIFIED"
    """
    Unspecified Scale Tier.
    """
    BASIC = "BASIC"
    """
    A single worker instance. This tier is suitable for learning how to use Cloud ML, and for experimenting with new models using small datasets.
    """
    STANDARD1 = "STANDARD_1"
    """
    Many workers and a few parameter servers.
    """
    PREMIUM1 = "PREMIUM_1"
    """
    A large number of workers with many parameter servers.
    """
    BASIC_GPU = "BASIC_GPU"
    """
    A single worker instance with a K80 GPU.
    """
    BASIC_TPU = "BASIC_TPU"
    """
    A single worker instance with a Cloud TPU.
    """
    CUSTOM = "CUSTOM"
    """
    The CUSTOM tier is not a set tier, but rather enables you to use your own cluster specification. When you use this tier, set values to configure your processing cluster according to these guidelines: * You _must_ set `ExecutionTemplate.masterType` to specify the type of machine to use for your master node. This is the only required setting.
    """


class InstanceBootDiskType(str, Enum):
    """
    Input only. The type of the boot disk attached to this instance, defaults to standard persistent disk (`PD_STANDARD`).
    """
    DISK_TYPE_UNSPECIFIED = "DISK_TYPE_UNSPECIFIED"
    """
    Disk type not set.
    """
    PD_STANDARD = "PD_STANDARD"
    """
    Standard persistent disk type.
    """
    PD_SSD = "PD_SSD"
    """
    SSD persistent disk type.
    """
    PD_BALANCED = "PD_BALANCED"
    """
    Balanced persistent disk type.
    """
    PD_EXTREME = "PD_EXTREME"
    """
    Extreme persistent disk type.
    """


class InstanceDataDiskType(str, Enum):
    """
    Input only. The type of the data disk attached to this instance, defaults to standard persistent disk (`PD_STANDARD`).
    """
    DISK_TYPE_UNSPECIFIED = "DISK_TYPE_UNSPECIFIED"
    """
    Disk type not set.
    """
    PD_STANDARD = "PD_STANDARD"
    """
    Standard persistent disk type.
    """
    PD_SSD = "PD_SSD"
    """
    SSD persistent disk type.
    """
    PD_BALANCED = "PD_BALANCED"
    """
    Balanced persistent disk type.
    """
    PD_EXTREME = "PD_EXTREME"
    """
    Extreme persistent disk type.
    """


class InstanceDiskEncryption(str, Enum):
    """
    Input only. Disk encryption method used on the boot and data disks, defaults to GMEK.
    """
    DISK_ENCRYPTION_UNSPECIFIED = "DISK_ENCRYPTION_UNSPECIFIED"
    """
    Disk encryption is not specified.
    """
    GMEK = "GMEK"
    """
    Use Google managed encryption keys to encrypt the boot disk.
    """
    CMEK = "CMEK"
    """
    Use customer managed encryption keys to encrypt the boot disk.
    """


class InstanceNicType(str, Enum):
    """
    Optional. The type of vNIC to be used on this interface. This may be gVNIC or VirtioNet.
    """
    UNSPECIFIED_NIC_TYPE = "UNSPECIFIED_NIC_TYPE"
    """
    No type specified.
    """
    VIRTIO_NET = "VIRTIO_NET"
    """
    VIRTIO
    """
    GVNIC = "GVNIC"
    """
    GVNIC
    """


class LocalDiskInitializeParamsDiskType(str, Enum):
    """
    Input only. The type of the boot disk attached to this instance, defaults to standard persistent disk (`PD_STANDARD`).
    """
    DISK_TYPE_UNSPECIFIED = "DISK_TYPE_UNSPECIFIED"
    """
    Disk type not set.
    """
    PD_STANDARD = "PD_STANDARD"
    """
    Standard persistent disk type.
    """
    PD_SSD = "PD_SSD"
    """
    SSD persistent disk type.
    """
    PD_BALANCED = "PD_BALANCED"
    """
    Balanced persistent disk type.
    """
    PD_EXTREME = "PD_EXTREME"
    """
    Extreme persistent disk type.
    """


class ReservationAffinityConsumeReservationType(str, Enum):
    """
    Optional. Type of reservation to consume
    """
    TYPE_UNSPECIFIED = "TYPE_UNSPECIFIED"
    """
    Default type.
    """
    NO_RESERVATION = "NO_RESERVATION"
    """
    Do not consume from any allocated capacity.
    """
    ANY_RESERVATION = "ANY_RESERVATION"
    """
    Consume any reservation available.
    """
    SPECIFIC_RESERVATION = "SPECIFIC_RESERVATION"
    """
    Must consume from a specific reservation. Must specify key value fields for specifying the reservations.
    """


class RuntimeAcceleratorConfigType(str, Enum):
    """
    Accelerator model.
    """
    ACCELERATOR_TYPE_UNSPECIFIED = "ACCELERATOR_TYPE_UNSPECIFIED"
    """
    Accelerator type is not specified.
    """
    NVIDIA_TESLA_K80 = "NVIDIA_TESLA_K80"
    """
    b/241005111 K80 deprecation in Google Managed Notebooks Accelerator type is Nvidia Tesla K80.
    """
    NVIDIA_TESLA_P100 = "NVIDIA_TESLA_P100"
    """
    Accelerator type is Nvidia Tesla P100.
    """
    NVIDIA_TESLA_V100 = "NVIDIA_TESLA_V100"
    """
    Accelerator type is Nvidia Tesla V100.
    """
    NVIDIA_TESLA_P4 = "NVIDIA_TESLA_P4"
    """
    Accelerator type is Nvidia Tesla P4.
    """
    NVIDIA_TESLA_T4 = "NVIDIA_TESLA_T4"
    """
    Accelerator type is Nvidia Tesla T4.
    """
    NVIDIA_TESLA_A100 = "NVIDIA_TESLA_A100"
    """
    Accelerator type is Nvidia Tesla A100.
    """
    TPU_V2 = "TPU_V2"
    """
    (Coming soon) Accelerator type is TPU V2.
    """
    TPU_V3 = "TPU_V3"
    """
    (Coming soon) Accelerator type is TPU V3.
    """
    NVIDIA_TESLA_T4_VWS = "NVIDIA_TESLA_T4_VWS"
    """
    Accelerator type is NVIDIA Tesla T4 Virtual Workstations.
    """
    NVIDIA_TESLA_P100_VWS = "NVIDIA_TESLA_P100_VWS"
    """
    Accelerator type is NVIDIA Tesla P100 Virtual Workstations.
    """
    NVIDIA_TESLA_P4_VWS = "NVIDIA_TESLA_P4_VWS"
    """
    Accelerator type is NVIDIA Tesla P4 Virtual Workstations.
    """


class RuntimeAccessConfigAccessType(str, Enum):
    """
    The type of access mode this instance.
    """
    RUNTIME_ACCESS_TYPE_UNSPECIFIED = "RUNTIME_ACCESS_TYPE_UNSPECIFIED"
    """
    Unspecified access.
    """
    SINGLE_USER = "SINGLE_USER"
    """
    Single user login.
    """
    SERVICE_ACCOUNT = "SERVICE_ACCOUNT"
    """
    Service Account mode. In Service Account mode, Runtime creator will specify a SA that exists in the consumer project. Using Runtime Service Account field. Users accessing the Runtime need ActAs (Service Account User) permission.
    """


class RuntimeSoftwareConfigPostStartupScriptBehavior(str, Enum):
    """
    Behavior for the post startup script.
    """
    POST_STARTUP_SCRIPT_BEHAVIOR_UNSPECIFIED = "POST_STARTUP_SCRIPT_BEHAVIOR_UNSPECIFIED"
    """
    Unspecified post startup script behavior. Will run only once at creation.
    """
    RUN_EVERY_START = "RUN_EVERY_START"
    """
    Runs the post startup script provided during creation at every start.
    """
    DOWNLOAD_AND_RUN_EVERY_START = "DOWNLOAD_AND_RUN_EVERY_START"
    """
    Downloads and runs the provided post startup script at every start.
    """


class ScheduleState(str, Enum):
    STATE_UNSPECIFIED = "STATE_UNSPECIFIED"
    """
    Unspecified state.
    """
    ENABLED = "ENABLED"
    """
    The job is executing normally.
    """
    PAUSED = "PAUSED"
    """
    The job is paused by the user. It will not execute. A user can intentionally pause the job using PauseJobRequest.
    """
    DISABLED = "DISABLED"
    """
    The job is disabled by the system due to error. The user cannot directly set a job to be disabled.
    """
    UPDATE_FAILED = "UPDATE_FAILED"
    """
    The job state resulting from a failed CloudScheduler.UpdateJob operation. To recover a job from this state, retry CloudScheduler.UpdateJob until a successful response is received.
    """
    INITIALIZING = "INITIALIZING"
    """
    The schedule resource is being created.
    """
    DELETING = "DELETING"
    """
    The schedule resource is being deleted.
    """


class SchedulerAcceleratorConfigType(str, Enum):
    """
    Type of this accelerator.
    """
    SCHEDULER_ACCELERATOR_TYPE_UNSPECIFIED = "SCHEDULER_ACCELERATOR_TYPE_UNSPECIFIED"
    """
    Unspecified accelerator type. Default to no GPU.
    """
    NVIDIA_TESLA_K80 = "NVIDIA_TESLA_K80"
    """
    Nvidia Tesla K80 GPU.
    """
    NVIDIA_TESLA_P100 = "NVIDIA_TESLA_P100"
    """
    Nvidia Tesla P100 GPU.
    """
    NVIDIA_TESLA_V100 = "NVIDIA_TESLA_V100"
    """
    Nvidia Tesla V100 GPU.
    """
    NVIDIA_TESLA_P4 = "NVIDIA_TESLA_P4"
    """
    Nvidia Tesla P4 GPU.
    """
    NVIDIA_TESLA_T4 = "NVIDIA_TESLA_T4"
    """
    Nvidia Tesla T4 GPU.
    """
    NVIDIA_TESLA_A100 = "NVIDIA_TESLA_A100"
    """
    Nvidia Tesla A100 GPU.
    """
    TPU_V2 = "TPU_V2"
    """
    TPU v2.
    """
    TPU_V3 = "TPU_V3"
    """
    TPU v3.
    """


class UpgradeHistoryEntryAction(str, Enum):
    """
    Action. Rolloback or Upgrade.
    """
    ACTION_UNSPECIFIED = "ACTION_UNSPECIFIED"
    """
    Operation is not specified.
    """
    UPGRADE = "UPGRADE"
    """
    Upgrade.
    """
    ROLLBACK = "ROLLBACK"
    """
    Rollback.
    """


class UpgradeHistoryEntryState(str, Enum):
    """
    The state of this instance upgrade history entry.
    """
    STATE_UNSPECIFIED = "STATE_UNSPECIFIED"
    """
    State is not specified.
    """
    STARTED = "STARTED"
    """
    The instance upgrade is started.
    """
    SUCCEEDED = "SUCCEEDED"
    """
    The instance upgrade is succeeded.
    """
    FAILED = "FAILED"
    """
    The instance upgrade is failed.
    """


class VirtualMachineConfigNicType(str, Enum):
    """
    Optional. The type of vNIC to be used on this interface. This may be gVNIC or VirtioNet.
    """
    UNSPECIFIED_NIC_TYPE = "UNSPECIFIED_NIC_TYPE"
    """
    No type specified.
    """
    VIRTIO_NET = "VIRTIO_NET"
    """
    VIRTIO
    """
    GVNIC = "GVNIC"
    """
    GVNIC
    """
