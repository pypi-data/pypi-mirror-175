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

__all__ = ['JobArgs', 'Job']

@pulumi.input_type
class JobArgs:
    def __init__(__self__, *,
                 placement: pulumi.Input['JobPlacementArgs'],
                 region: pulumi.Input[str],
                 hadoop_job: Optional[pulumi.Input['HadoopJobArgs']] = None,
                 hive_job: Optional[pulumi.Input['HiveJobArgs']] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 pig_job: Optional[pulumi.Input['PigJobArgs']] = None,
                 presto_job: Optional[pulumi.Input['PrestoJobArgs']] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 pyspark_job: Optional[pulumi.Input['PySparkJobArgs']] = None,
                 reference: Optional[pulumi.Input['JobReferenceArgs']] = None,
                 request_id: Optional[pulumi.Input[str]] = None,
                 scheduling: Optional[pulumi.Input['JobSchedulingArgs']] = None,
                 spark_job: Optional[pulumi.Input['SparkJobArgs']] = None,
                 spark_r_job: Optional[pulumi.Input['SparkRJobArgs']] = None,
                 spark_sql_job: Optional[pulumi.Input['SparkSqlJobArgs']] = None,
                 trino_job: Optional[pulumi.Input['TrinoJobArgs']] = None):
        """
        The set of arguments for constructing a Job resource.
        :param pulumi.Input['JobPlacementArgs'] placement: Job information, including how, when, and where to run the job.
        :param pulumi.Input['HadoopJobArgs'] hadoop_job: Optional. Job is a Hadoop job.
        :param pulumi.Input['HiveJobArgs'] hive_job: Optional. Job is a Hive job.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Optional. The labels to associate with this job. Label keys must contain 1 to 63 characters, and must conform to RFC 1035 (https://www.ietf.org/rfc/rfc1035.txt). Label values may be empty, but, if present, must contain 1 to 63 characters, and must conform to RFC 1035 (https://www.ietf.org/rfc/rfc1035.txt). No more than 32 labels can be associated with a job.
        :param pulumi.Input['PigJobArgs'] pig_job: Optional. Job is a Pig job.
        :param pulumi.Input['PrestoJobArgs'] presto_job: Optional. Job is a Presto job.
        :param pulumi.Input['PySparkJobArgs'] pyspark_job: Optional. Job is a PySpark job.
        :param pulumi.Input['JobReferenceArgs'] reference: Optional. The fully qualified reference to the job, which can be used to obtain the equivalent REST path of the job resource. If this property is not specified when a job is created, the server generates a job_id.
        :param pulumi.Input[str] request_id: Optional. A unique id used to identify the request. If the server receives two SubmitJobRequest (https://cloud.google.com/dataproc/docs/reference/rpc/google.cloud.dataproc.v1#google.cloud.dataproc.v1.SubmitJobRequest)s with the same id, then the second request will be ignored and the first Job created and stored in the backend is returned.It is recommended to always set this value to a UUID (https://en.wikipedia.org/wiki/Universally_unique_identifier).The id must contain only letters (a-z, A-Z), numbers (0-9), underscores (_), and hyphens (-). The maximum length is 40 characters.
        :param pulumi.Input['JobSchedulingArgs'] scheduling: Optional. Job scheduling configuration.
        :param pulumi.Input['SparkJobArgs'] spark_job: Optional. Job is a Spark job.
        :param pulumi.Input['SparkRJobArgs'] spark_r_job: Optional. Job is a SparkR job.
        :param pulumi.Input['SparkSqlJobArgs'] spark_sql_job: Optional. Job is a SparkSql job.
        :param pulumi.Input['TrinoJobArgs'] trino_job: Optional. Job is a Trino job.
        """
        pulumi.set(__self__, "placement", placement)
        pulumi.set(__self__, "region", region)
        if hadoop_job is not None:
            pulumi.set(__self__, "hadoop_job", hadoop_job)
        if hive_job is not None:
            pulumi.set(__self__, "hive_job", hive_job)
        if labels is not None:
            pulumi.set(__self__, "labels", labels)
        if pig_job is not None:
            pulumi.set(__self__, "pig_job", pig_job)
        if presto_job is not None:
            pulumi.set(__self__, "presto_job", presto_job)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if pyspark_job is not None:
            pulumi.set(__self__, "pyspark_job", pyspark_job)
        if reference is not None:
            pulumi.set(__self__, "reference", reference)
        if request_id is not None:
            pulumi.set(__self__, "request_id", request_id)
        if scheduling is not None:
            pulumi.set(__self__, "scheduling", scheduling)
        if spark_job is not None:
            pulumi.set(__self__, "spark_job", spark_job)
        if spark_r_job is not None:
            pulumi.set(__self__, "spark_r_job", spark_r_job)
        if spark_sql_job is not None:
            pulumi.set(__self__, "spark_sql_job", spark_sql_job)
        if trino_job is not None:
            pulumi.set(__self__, "trino_job", trino_job)

    @property
    @pulumi.getter
    def placement(self) -> pulumi.Input['JobPlacementArgs']:
        """
        Job information, including how, when, and where to run the job.
        """
        return pulumi.get(self, "placement")

    @placement.setter
    def placement(self, value: pulumi.Input['JobPlacementArgs']):
        pulumi.set(self, "placement", value)

    @property
    @pulumi.getter
    def region(self) -> pulumi.Input[str]:
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: pulumi.Input[str]):
        pulumi.set(self, "region", value)

    @property
    @pulumi.getter(name="hadoopJob")
    def hadoop_job(self) -> Optional[pulumi.Input['HadoopJobArgs']]:
        """
        Optional. Job is a Hadoop job.
        """
        return pulumi.get(self, "hadoop_job")

    @hadoop_job.setter
    def hadoop_job(self, value: Optional[pulumi.Input['HadoopJobArgs']]):
        pulumi.set(self, "hadoop_job", value)

    @property
    @pulumi.getter(name="hiveJob")
    def hive_job(self) -> Optional[pulumi.Input['HiveJobArgs']]:
        """
        Optional. Job is a Hive job.
        """
        return pulumi.get(self, "hive_job")

    @hive_job.setter
    def hive_job(self, value: Optional[pulumi.Input['HiveJobArgs']]):
        pulumi.set(self, "hive_job", value)

    @property
    @pulumi.getter
    def labels(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Optional. The labels to associate with this job. Label keys must contain 1 to 63 characters, and must conform to RFC 1035 (https://www.ietf.org/rfc/rfc1035.txt). Label values may be empty, but, if present, must contain 1 to 63 characters, and must conform to RFC 1035 (https://www.ietf.org/rfc/rfc1035.txt). No more than 32 labels can be associated with a job.
        """
        return pulumi.get(self, "labels")

    @labels.setter
    def labels(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "labels", value)

    @property
    @pulumi.getter(name="pigJob")
    def pig_job(self) -> Optional[pulumi.Input['PigJobArgs']]:
        """
        Optional. Job is a Pig job.
        """
        return pulumi.get(self, "pig_job")

    @pig_job.setter
    def pig_job(self, value: Optional[pulumi.Input['PigJobArgs']]):
        pulumi.set(self, "pig_job", value)

    @property
    @pulumi.getter(name="prestoJob")
    def presto_job(self) -> Optional[pulumi.Input['PrestoJobArgs']]:
        """
        Optional. Job is a Presto job.
        """
        return pulumi.get(self, "presto_job")

    @presto_job.setter
    def presto_job(self, value: Optional[pulumi.Input['PrestoJobArgs']]):
        pulumi.set(self, "presto_job", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter(name="pysparkJob")
    def pyspark_job(self) -> Optional[pulumi.Input['PySparkJobArgs']]:
        """
        Optional. Job is a PySpark job.
        """
        return pulumi.get(self, "pyspark_job")

    @pyspark_job.setter
    def pyspark_job(self, value: Optional[pulumi.Input['PySparkJobArgs']]):
        pulumi.set(self, "pyspark_job", value)

    @property
    @pulumi.getter
    def reference(self) -> Optional[pulumi.Input['JobReferenceArgs']]:
        """
        Optional. The fully qualified reference to the job, which can be used to obtain the equivalent REST path of the job resource. If this property is not specified when a job is created, the server generates a job_id.
        """
        return pulumi.get(self, "reference")

    @reference.setter
    def reference(self, value: Optional[pulumi.Input['JobReferenceArgs']]):
        pulumi.set(self, "reference", value)

    @property
    @pulumi.getter(name="requestId")
    def request_id(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. A unique id used to identify the request. If the server receives two SubmitJobRequest (https://cloud.google.com/dataproc/docs/reference/rpc/google.cloud.dataproc.v1#google.cloud.dataproc.v1.SubmitJobRequest)s with the same id, then the second request will be ignored and the first Job created and stored in the backend is returned.It is recommended to always set this value to a UUID (https://en.wikipedia.org/wiki/Universally_unique_identifier).The id must contain only letters (a-z, A-Z), numbers (0-9), underscores (_), and hyphens (-). The maximum length is 40 characters.
        """
        return pulumi.get(self, "request_id")

    @request_id.setter
    def request_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "request_id", value)

    @property
    @pulumi.getter
    def scheduling(self) -> Optional[pulumi.Input['JobSchedulingArgs']]:
        """
        Optional. Job scheduling configuration.
        """
        return pulumi.get(self, "scheduling")

    @scheduling.setter
    def scheduling(self, value: Optional[pulumi.Input['JobSchedulingArgs']]):
        pulumi.set(self, "scheduling", value)

    @property
    @pulumi.getter(name="sparkJob")
    def spark_job(self) -> Optional[pulumi.Input['SparkJobArgs']]:
        """
        Optional. Job is a Spark job.
        """
        return pulumi.get(self, "spark_job")

    @spark_job.setter
    def spark_job(self, value: Optional[pulumi.Input['SparkJobArgs']]):
        pulumi.set(self, "spark_job", value)

    @property
    @pulumi.getter(name="sparkRJob")
    def spark_r_job(self) -> Optional[pulumi.Input['SparkRJobArgs']]:
        """
        Optional. Job is a SparkR job.
        """
        return pulumi.get(self, "spark_r_job")

    @spark_r_job.setter
    def spark_r_job(self, value: Optional[pulumi.Input['SparkRJobArgs']]):
        pulumi.set(self, "spark_r_job", value)

    @property
    @pulumi.getter(name="sparkSqlJob")
    def spark_sql_job(self) -> Optional[pulumi.Input['SparkSqlJobArgs']]:
        """
        Optional. Job is a SparkSql job.
        """
        return pulumi.get(self, "spark_sql_job")

    @spark_sql_job.setter
    def spark_sql_job(self, value: Optional[pulumi.Input['SparkSqlJobArgs']]):
        pulumi.set(self, "spark_sql_job", value)

    @property
    @pulumi.getter(name="trinoJob")
    def trino_job(self) -> Optional[pulumi.Input['TrinoJobArgs']]:
        """
        Optional. Job is a Trino job.
        """
        return pulumi.get(self, "trino_job")

    @trino_job.setter
    def trino_job(self, value: Optional[pulumi.Input['TrinoJobArgs']]):
        pulumi.set(self, "trino_job", value)


class Job(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 hadoop_job: Optional[pulumi.Input[pulumi.InputType['HadoopJobArgs']]] = None,
                 hive_job: Optional[pulumi.Input[pulumi.InputType['HiveJobArgs']]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 pig_job: Optional[pulumi.Input[pulumi.InputType['PigJobArgs']]] = None,
                 placement: Optional[pulumi.Input[pulumi.InputType['JobPlacementArgs']]] = None,
                 presto_job: Optional[pulumi.Input[pulumi.InputType['PrestoJobArgs']]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 pyspark_job: Optional[pulumi.Input[pulumi.InputType['PySparkJobArgs']]] = None,
                 reference: Optional[pulumi.Input[pulumi.InputType['JobReferenceArgs']]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 request_id: Optional[pulumi.Input[str]] = None,
                 scheduling: Optional[pulumi.Input[pulumi.InputType['JobSchedulingArgs']]] = None,
                 spark_job: Optional[pulumi.Input[pulumi.InputType['SparkJobArgs']]] = None,
                 spark_r_job: Optional[pulumi.Input[pulumi.InputType['SparkRJobArgs']]] = None,
                 spark_sql_job: Optional[pulumi.Input[pulumi.InputType['SparkSqlJobArgs']]] = None,
                 trino_job: Optional[pulumi.Input[pulumi.InputType['TrinoJobArgs']]] = None,
                 __props__=None):
        """
        Submits a job to a cluster.
        Auto-naming is currently not supported for this resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['HadoopJobArgs']] hadoop_job: Optional. Job is a Hadoop job.
        :param pulumi.Input[pulumi.InputType['HiveJobArgs']] hive_job: Optional. Job is a Hive job.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Optional. The labels to associate with this job. Label keys must contain 1 to 63 characters, and must conform to RFC 1035 (https://www.ietf.org/rfc/rfc1035.txt). Label values may be empty, but, if present, must contain 1 to 63 characters, and must conform to RFC 1035 (https://www.ietf.org/rfc/rfc1035.txt). No more than 32 labels can be associated with a job.
        :param pulumi.Input[pulumi.InputType['PigJobArgs']] pig_job: Optional. Job is a Pig job.
        :param pulumi.Input[pulumi.InputType['JobPlacementArgs']] placement: Job information, including how, when, and where to run the job.
        :param pulumi.Input[pulumi.InputType['PrestoJobArgs']] presto_job: Optional. Job is a Presto job.
        :param pulumi.Input[pulumi.InputType['PySparkJobArgs']] pyspark_job: Optional. Job is a PySpark job.
        :param pulumi.Input[pulumi.InputType['JobReferenceArgs']] reference: Optional. The fully qualified reference to the job, which can be used to obtain the equivalent REST path of the job resource. If this property is not specified when a job is created, the server generates a job_id.
        :param pulumi.Input[str] request_id: Optional. A unique id used to identify the request. If the server receives two SubmitJobRequest (https://cloud.google.com/dataproc/docs/reference/rpc/google.cloud.dataproc.v1#google.cloud.dataproc.v1.SubmitJobRequest)s with the same id, then the second request will be ignored and the first Job created and stored in the backend is returned.It is recommended to always set this value to a UUID (https://en.wikipedia.org/wiki/Universally_unique_identifier).The id must contain only letters (a-z, A-Z), numbers (0-9), underscores (_), and hyphens (-). The maximum length is 40 characters.
        :param pulumi.Input[pulumi.InputType['JobSchedulingArgs']] scheduling: Optional. Job scheduling configuration.
        :param pulumi.Input[pulumi.InputType['SparkJobArgs']] spark_job: Optional. Job is a Spark job.
        :param pulumi.Input[pulumi.InputType['SparkRJobArgs']] spark_r_job: Optional. Job is a SparkR job.
        :param pulumi.Input[pulumi.InputType['SparkSqlJobArgs']] spark_sql_job: Optional. Job is a SparkSql job.
        :param pulumi.Input[pulumi.InputType['TrinoJobArgs']] trino_job: Optional. Job is a Trino job.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: JobArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Submits a job to a cluster.
        Auto-naming is currently not supported for this resource.

        :param str resource_name: The name of the resource.
        :param JobArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(JobArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 hadoop_job: Optional[pulumi.Input[pulumi.InputType['HadoopJobArgs']]] = None,
                 hive_job: Optional[pulumi.Input[pulumi.InputType['HiveJobArgs']]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 pig_job: Optional[pulumi.Input[pulumi.InputType['PigJobArgs']]] = None,
                 placement: Optional[pulumi.Input[pulumi.InputType['JobPlacementArgs']]] = None,
                 presto_job: Optional[pulumi.Input[pulumi.InputType['PrestoJobArgs']]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 pyspark_job: Optional[pulumi.Input[pulumi.InputType['PySparkJobArgs']]] = None,
                 reference: Optional[pulumi.Input[pulumi.InputType['JobReferenceArgs']]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 request_id: Optional[pulumi.Input[str]] = None,
                 scheduling: Optional[pulumi.Input[pulumi.InputType['JobSchedulingArgs']]] = None,
                 spark_job: Optional[pulumi.Input[pulumi.InputType['SparkJobArgs']]] = None,
                 spark_r_job: Optional[pulumi.Input[pulumi.InputType['SparkRJobArgs']]] = None,
                 spark_sql_job: Optional[pulumi.Input[pulumi.InputType['SparkSqlJobArgs']]] = None,
                 trino_job: Optional[pulumi.Input[pulumi.InputType['TrinoJobArgs']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = JobArgs.__new__(JobArgs)

            __props__.__dict__["hadoop_job"] = hadoop_job
            __props__.__dict__["hive_job"] = hive_job
            __props__.__dict__["labels"] = labels
            __props__.__dict__["pig_job"] = pig_job
            if placement is None and not opts.urn:
                raise TypeError("Missing required property 'placement'")
            __props__.__dict__["placement"] = placement
            __props__.__dict__["presto_job"] = presto_job
            __props__.__dict__["project"] = project
            __props__.__dict__["pyspark_job"] = pyspark_job
            __props__.__dict__["reference"] = reference
            if region is None and not opts.urn:
                raise TypeError("Missing required property 'region'")
            __props__.__dict__["region"] = region
            __props__.__dict__["request_id"] = request_id
            __props__.__dict__["scheduling"] = scheduling
            __props__.__dict__["spark_job"] = spark_job
            __props__.__dict__["spark_r_job"] = spark_r_job
            __props__.__dict__["spark_sql_job"] = spark_sql_job
            __props__.__dict__["trino_job"] = trino_job
            __props__.__dict__["done"] = None
            __props__.__dict__["driver_control_files_uri"] = None
            __props__.__dict__["driver_output_resource_uri"] = None
            __props__.__dict__["job_uuid"] = None
            __props__.__dict__["status"] = None
            __props__.__dict__["status_history"] = None
            __props__.__dict__["yarn_applications"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["project", "region"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Job, __self__).__init__(
            'google-native:dataproc/v1:Job',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Job':
        """
        Get an existing Job resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = JobArgs.__new__(JobArgs)

        __props__.__dict__["done"] = None
        __props__.__dict__["driver_control_files_uri"] = None
        __props__.__dict__["driver_output_resource_uri"] = None
        __props__.__dict__["hadoop_job"] = None
        __props__.__dict__["hive_job"] = None
        __props__.__dict__["job_uuid"] = None
        __props__.__dict__["labels"] = None
        __props__.__dict__["pig_job"] = None
        __props__.__dict__["placement"] = None
        __props__.__dict__["presto_job"] = None
        __props__.__dict__["project"] = None
        __props__.__dict__["pyspark_job"] = None
        __props__.__dict__["reference"] = None
        __props__.__dict__["region"] = None
        __props__.__dict__["scheduling"] = None
        __props__.__dict__["spark_job"] = None
        __props__.__dict__["spark_r_job"] = None
        __props__.__dict__["spark_sql_job"] = None
        __props__.__dict__["status"] = None
        __props__.__dict__["status_history"] = None
        __props__.__dict__["trino_job"] = None
        __props__.__dict__["yarn_applications"] = None
        return Job(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def done(self) -> pulumi.Output[bool]:
        """
        Indicates whether the job is completed. If the value is false, the job is still in progress. If true, the job is completed, and status.state field will indicate if it was successful, failed, or cancelled.
        """
        return pulumi.get(self, "done")

    @property
    @pulumi.getter(name="driverControlFilesUri")
    def driver_control_files_uri(self) -> pulumi.Output[str]:
        """
        If present, the location of miscellaneous control files which may be used as part of job setup and handling. If not present, control files may be placed in the same location as driver_output_uri.
        """
        return pulumi.get(self, "driver_control_files_uri")

    @property
    @pulumi.getter(name="driverOutputResourceUri")
    def driver_output_resource_uri(self) -> pulumi.Output[str]:
        """
        A URI pointing to the location of the stdout of the job's driver program.
        """
        return pulumi.get(self, "driver_output_resource_uri")

    @property
    @pulumi.getter(name="hadoopJob")
    def hadoop_job(self) -> pulumi.Output['outputs.HadoopJobResponse']:
        """
        Optional. Job is a Hadoop job.
        """
        return pulumi.get(self, "hadoop_job")

    @property
    @pulumi.getter(name="hiveJob")
    def hive_job(self) -> pulumi.Output['outputs.HiveJobResponse']:
        """
        Optional. Job is a Hive job.
        """
        return pulumi.get(self, "hive_job")

    @property
    @pulumi.getter(name="jobUuid")
    def job_uuid(self) -> pulumi.Output[str]:
        """
        A UUID that uniquely identifies a job within the project over time. This is in contrast to a user-settable reference.job_id that may be reused over time.
        """
        return pulumi.get(self, "job_uuid")

    @property
    @pulumi.getter
    def labels(self) -> pulumi.Output[Mapping[str, str]]:
        """
        Optional. The labels to associate with this job. Label keys must contain 1 to 63 characters, and must conform to RFC 1035 (https://www.ietf.org/rfc/rfc1035.txt). Label values may be empty, but, if present, must contain 1 to 63 characters, and must conform to RFC 1035 (https://www.ietf.org/rfc/rfc1035.txt). No more than 32 labels can be associated with a job.
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter(name="pigJob")
    def pig_job(self) -> pulumi.Output['outputs.PigJobResponse']:
        """
        Optional. Job is a Pig job.
        """
        return pulumi.get(self, "pig_job")

    @property
    @pulumi.getter
    def placement(self) -> pulumi.Output['outputs.JobPlacementResponse']:
        """
        Job information, including how, when, and where to run the job.
        """
        return pulumi.get(self, "placement")

    @property
    @pulumi.getter(name="prestoJob")
    def presto_job(self) -> pulumi.Output['outputs.PrestoJobResponse']:
        """
        Optional. Job is a Presto job.
        """
        return pulumi.get(self, "presto_job")

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        return pulumi.get(self, "project")

    @property
    @pulumi.getter(name="pysparkJob")
    def pyspark_job(self) -> pulumi.Output['outputs.PySparkJobResponse']:
        """
        Optional. Job is a PySpark job.
        """
        return pulumi.get(self, "pyspark_job")

    @property
    @pulumi.getter
    def reference(self) -> pulumi.Output['outputs.JobReferenceResponse']:
        """
        Optional. The fully qualified reference to the job, which can be used to obtain the equivalent REST path of the job resource. If this property is not specified when a job is created, the server generates a job_id.
        """
        return pulumi.get(self, "reference")

    @property
    @pulumi.getter
    def region(self) -> pulumi.Output[str]:
        return pulumi.get(self, "region")

    @property
    @pulumi.getter
    def scheduling(self) -> pulumi.Output['outputs.JobSchedulingResponse']:
        """
        Optional. Job scheduling configuration.
        """
        return pulumi.get(self, "scheduling")

    @property
    @pulumi.getter(name="sparkJob")
    def spark_job(self) -> pulumi.Output['outputs.SparkJobResponse']:
        """
        Optional. Job is a Spark job.
        """
        return pulumi.get(self, "spark_job")

    @property
    @pulumi.getter(name="sparkRJob")
    def spark_r_job(self) -> pulumi.Output['outputs.SparkRJobResponse']:
        """
        Optional. Job is a SparkR job.
        """
        return pulumi.get(self, "spark_r_job")

    @property
    @pulumi.getter(name="sparkSqlJob")
    def spark_sql_job(self) -> pulumi.Output['outputs.SparkSqlJobResponse']:
        """
        Optional. Job is a SparkSql job.
        """
        return pulumi.get(self, "spark_sql_job")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output['outputs.JobStatusResponse']:
        """
        The job status. Additional application-specific status information may be contained in the type_job and yarn_applications fields.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="statusHistory")
    def status_history(self) -> pulumi.Output[Sequence['outputs.JobStatusResponse']]:
        """
        The previous job status.
        """
        return pulumi.get(self, "status_history")

    @property
    @pulumi.getter(name="trinoJob")
    def trino_job(self) -> pulumi.Output['outputs.TrinoJobResponse']:
        """
        Optional. Job is a Trino job.
        """
        return pulumi.get(self, "trino_job")

    @property
    @pulumi.getter(name="yarnApplications")
    def yarn_applications(self) -> pulumi.Output[Sequence['outputs.YarnApplicationResponse']]:
        """
        The collection of YARN applications spun up by this job.Beta Feature: This report is available for testing purposes only. It may be changed before final release.
        """
        return pulumi.get(self, "yarn_applications")

