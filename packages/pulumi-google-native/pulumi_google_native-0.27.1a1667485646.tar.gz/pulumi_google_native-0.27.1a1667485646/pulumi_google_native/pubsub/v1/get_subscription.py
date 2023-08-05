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
    'GetSubscriptionResult',
    'AwaitableGetSubscriptionResult',
    'get_subscription',
    'get_subscription_output',
]

@pulumi.output_type
class GetSubscriptionResult:
    def __init__(__self__, ack_deadline_seconds=None, bigquery_config=None, dead_letter_policy=None, detached=None, enable_exactly_once_delivery=None, enable_message_ordering=None, expiration_policy=None, filter=None, labels=None, message_retention_duration=None, name=None, push_config=None, retain_acked_messages=None, retry_policy=None, state=None, topic=None, topic_message_retention_duration=None):
        if ack_deadline_seconds and not isinstance(ack_deadline_seconds, int):
            raise TypeError("Expected argument 'ack_deadline_seconds' to be a int")
        pulumi.set(__self__, "ack_deadline_seconds", ack_deadline_seconds)
        if bigquery_config and not isinstance(bigquery_config, dict):
            raise TypeError("Expected argument 'bigquery_config' to be a dict")
        pulumi.set(__self__, "bigquery_config", bigquery_config)
        if dead_letter_policy and not isinstance(dead_letter_policy, dict):
            raise TypeError("Expected argument 'dead_letter_policy' to be a dict")
        pulumi.set(__self__, "dead_letter_policy", dead_letter_policy)
        if detached and not isinstance(detached, bool):
            raise TypeError("Expected argument 'detached' to be a bool")
        pulumi.set(__self__, "detached", detached)
        if enable_exactly_once_delivery and not isinstance(enable_exactly_once_delivery, bool):
            raise TypeError("Expected argument 'enable_exactly_once_delivery' to be a bool")
        pulumi.set(__self__, "enable_exactly_once_delivery", enable_exactly_once_delivery)
        if enable_message_ordering and not isinstance(enable_message_ordering, bool):
            raise TypeError("Expected argument 'enable_message_ordering' to be a bool")
        pulumi.set(__self__, "enable_message_ordering", enable_message_ordering)
        if expiration_policy and not isinstance(expiration_policy, dict):
            raise TypeError("Expected argument 'expiration_policy' to be a dict")
        pulumi.set(__self__, "expiration_policy", expiration_policy)
        if filter and not isinstance(filter, str):
            raise TypeError("Expected argument 'filter' to be a str")
        pulumi.set(__self__, "filter", filter)
        if labels and not isinstance(labels, dict):
            raise TypeError("Expected argument 'labels' to be a dict")
        pulumi.set(__self__, "labels", labels)
        if message_retention_duration and not isinstance(message_retention_duration, str):
            raise TypeError("Expected argument 'message_retention_duration' to be a str")
        pulumi.set(__self__, "message_retention_duration", message_retention_duration)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if push_config and not isinstance(push_config, dict):
            raise TypeError("Expected argument 'push_config' to be a dict")
        pulumi.set(__self__, "push_config", push_config)
        if retain_acked_messages and not isinstance(retain_acked_messages, bool):
            raise TypeError("Expected argument 'retain_acked_messages' to be a bool")
        pulumi.set(__self__, "retain_acked_messages", retain_acked_messages)
        if retry_policy and not isinstance(retry_policy, dict):
            raise TypeError("Expected argument 'retry_policy' to be a dict")
        pulumi.set(__self__, "retry_policy", retry_policy)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if topic and not isinstance(topic, str):
            raise TypeError("Expected argument 'topic' to be a str")
        pulumi.set(__self__, "topic", topic)
        if topic_message_retention_duration and not isinstance(topic_message_retention_duration, str):
            raise TypeError("Expected argument 'topic_message_retention_duration' to be a str")
        pulumi.set(__self__, "topic_message_retention_duration", topic_message_retention_duration)

    @property
    @pulumi.getter(name="ackDeadlineSeconds")
    def ack_deadline_seconds(self) -> int:
        """
        The approximate amount of time (on a best-effort basis) Pub/Sub waits for the subscriber to acknowledge receipt before resending the message. In the interval after the message is delivered and before it is acknowledged, it is considered to be _outstanding_. During that time period, the message will not be redelivered (on a best-effort basis). For pull subscriptions, this value is used as the initial value for the ack deadline. To override this value for a given message, call `ModifyAckDeadline` with the corresponding `ack_id` if using non-streaming pull or send the `ack_id` in a `StreamingModifyAckDeadlineRequest` if using streaming pull. The minimum custom deadline you can specify is 10 seconds. The maximum custom deadline you can specify is 600 seconds (10 minutes). If this parameter is 0, a default value of 10 seconds is used. For push delivery, this value is also used to set the request timeout for the call to the push endpoint. If the subscriber never acknowledges the message, the Pub/Sub system will eventually redeliver the message.
        """
        return pulumi.get(self, "ack_deadline_seconds")

    @property
    @pulumi.getter(name="bigqueryConfig")
    def bigquery_config(self) -> 'outputs.BigQueryConfigResponse':
        """
        If delivery to BigQuery is used with this subscription, this field is used to configure it.
        """
        return pulumi.get(self, "bigquery_config")

    @property
    @pulumi.getter(name="deadLetterPolicy")
    def dead_letter_policy(self) -> 'outputs.DeadLetterPolicyResponse':
        """
        A policy that specifies the conditions for dead lettering messages in this subscription. If dead_letter_policy is not set, dead lettering is disabled. The Cloud Pub/Sub service account associated with this subscriptions's parent project (i.e., service-{project_number}@gcp-sa-pubsub.iam.gserviceaccount.com) must have permission to Acknowledge() messages on this subscription.
        """
        return pulumi.get(self, "dead_letter_policy")

    @property
    @pulumi.getter
    def detached(self) -> bool:
        """
        Indicates whether the subscription is detached from its topic. Detached subscriptions don't receive messages from their topic and don't retain any backlog. `Pull` and `StreamingPull` requests will return FAILED_PRECONDITION. If the subscription is a push subscription, pushes to the endpoint will not be made.
        """
        return pulumi.get(self, "detached")

    @property
    @pulumi.getter(name="enableExactlyOnceDelivery")
    def enable_exactly_once_delivery(self) -> bool:
        """
        If true, Pub/Sub provides the following guarantees for the delivery of a message with a given value of `message_id` on this subscription: * The message sent to a subscriber is guaranteed not to be resent before the message's acknowledgement deadline expires. * An acknowledged message will not be resent to a subscriber. Note that subscribers may still receive multiple copies of a message when `enable_exactly_once_delivery` is true if the message was published multiple times by a publisher client. These copies are considered distinct by Pub/Sub and have distinct `message_id` values.
        """
        return pulumi.get(self, "enable_exactly_once_delivery")

    @property
    @pulumi.getter(name="enableMessageOrdering")
    def enable_message_ordering(self) -> bool:
        """
        If true, messages published with the same `ordering_key` in `PubsubMessage` will be delivered to the subscribers in the order in which they are received by the Pub/Sub system. Otherwise, they may be delivered in any order.
        """
        return pulumi.get(self, "enable_message_ordering")

    @property
    @pulumi.getter(name="expirationPolicy")
    def expiration_policy(self) -> 'outputs.ExpirationPolicyResponse':
        """
        A policy that specifies the conditions for this subscription's expiration. A subscription is considered active as long as any connected subscriber is successfully consuming messages from the subscription or is issuing operations on the subscription. If `expiration_policy` is not set, a *default policy* with `ttl` of 31 days will be used. The minimum allowed value for `expiration_policy.ttl` is 1 day. If `expiration_policy` is set, but `expiration_policy.ttl` is not set, the subscription never expires.
        """
        return pulumi.get(self, "expiration_policy")

    @property
    @pulumi.getter
    def filter(self) -> str:
        """
        An expression written in the Pub/Sub [filter language](https://cloud.google.com/pubsub/docs/filtering). If non-empty, then only `PubsubMessage`s whose `attributes` field matches the filter are delivered on this subscription. If empty, then no messages are filtered out.
        """
        return pulumi.get(self, "filter")

    @property
    @pulumi.getter
    def labels(self) -> Mapping[str, str]:
        """
        See [Creating and managing labels](https://cloud.google.com/pubsub/docs/labels).
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter(name="messageRetentionDuration")
    def message_retention_duration(self) -> str:
        """
        How long to retain unacknowledged messages in the subscription's backlog, from the moment a message is published. If `retain_acked_messages` is true, then this also configures the retention of acknowledged messages, and thus configures how far back in time a `Seek` can be done. Defaults to 7 days. Cannot be more than 7 days or less than 10 minutes.
        """
        return pulumi.get(self, "message_retention_duration")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the subscription. It must have the format `"projects/{project}/subscriptions/{subscription}"`. `{subscription}` must start with a letter, and contain only letters (`[A-Za-z]`), numbers (`[0-9]`), dashes (`-`), underscores (`_`), periods (`.`), tildes (`~`), plus (`+`) or percent signs (`%`). It must be between 3 and 255 characters in length, and it must not start with `"goog"`.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="pushConfig")
    def push_config(self) -> 'outputs.PushConfigResponse':
        """
        If push delivery is used with this subscription, this field is used to configure it.
        """
        return pulumi.get(self, "push_config")

    @property
    @pulumi.getter(name="retainAckedMessages")
    def retain_acked_messages(self) -> bool:
        """
        Indicates whether to retain acknowledged messages. If true, then messages are not expunged from the subscription's backlog, even if they are acknowledged, until they fall out of the `message_retention_duration` window. This must be true if you would like to [`Seek` to a timestamp] (https://cloud.google.com/pubsub/docs/replay-overview#seek_to_a_time) in the past to replay previously-acknowledged messages.
        """
        return pulumi.get(self, "retain_acked_messages")

    @property
    @pulumi.getter(name="retryPolicy")
    def retry_policy(self) -> 'outputs.RetryPolicyResponse':
        """
        A policy that specifies how Pub/Sub retries message delivery for this subscription. If not set, the default retry policy is applied. This generally implies that messages will be retried as soon as possible for healthy subscribers. RetryPolicy will be triggered on NACKs or acknowledgement deadline exceeded events for a given message.
        """
        return pulumi.get(self, "retry_policy")

    @property
    @pulumi.getter
    def state(self) -> str:
        """
        An output-only field indicating whether or not the subscription can receive messages.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def topic(self) -> str:
        """
        The name of the topic from which this subscription is receiving messages. Format is `projects/{project}/topics/{topic}`. The value of this field will be `_deleted-topic_` if the topic has been deleted.
        """
        return pulumi.get(self, "topic")

    @property
    @pulumi.getter(name="topicMessageRetentionDuration")
    def topic_message_retention_duration(self) -> str:
        """
        Indicates the minimum duration for which a message is retained after it is published to the subscription's topic. If this field is set, messages published to the subscription's topic in the last `topic_message_retention_duration` are always available to subscribers. See the `message_retention_duration` field in `Topic`. This field is set only in responses from the server; it is ignored if it is set in any requests.
        """
        return pulumi.get(self, "topic_message_retention_duration")


class AwaitableGetSubscriptionResult(GetSubscriptionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSubscriptionResult(
            ack_deadline_seconds=self.ack_deadline_seconds,
            bigquery_config=self.bigquery_config,
            dead_letter_policy=self.dead_letter_policy,
            detached=self.detached,
            enable_exactly_once_delivery=self.enable_exactly_once_delivery,
            enable_message_ordering=self.enable_message_ordering,
            expiration_policy=self.expiration_policy,
            filter=self.filter,
            labels=self.labels,
            message_retention_duration=self.message_retention_duration,
            name=self.name,
            push_config=self.push_config,
            retain_acked_messages=self.retain_acked_messages,
            retry_policy=self.retry_policy,
            state=self.state,
            topic=self.topic,
            topic_message_retention_duration=self.topic_message_retention_duration)


def get_subscription(project: Optional[str] = None,
                     subscription_id: Optional[str] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSubscriptionResult:
    """
    Gets the configuration details of a subscription.
    """
    __args__ = dict()
    __args__['project'] = project
    __args__['subscriptionId'] = subscription_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('google-native:pubsub/v1:getSubscription', __args__, opts=opts, typ=GetSubscriptionResult).value

    return AwaitableGetSubscriptionResult(
        ack_deadline_seconds=__ret__.ack_deadline_seconds,
        bigquery_config=__ret__.bigquery_config,
        dead_letter_policy=__ret__.dead_letter_policy,
        detached=__ret__.detached,
        enable_exactly_once_delivery=__ret__.enable_exactly_once_delivery,
        enable_message_ordering=__ret__.enable_message_ordering,
        expiration_policy=__ret__.expiration_policy,
        filter=__ret__.filter,
        labels=__ret__.labels,
        message_retention_duration=__ret__.message_retention_duration,
        name=__ret__.name,
        push_config=__ret__.push_config,
        retain_acked_messages=__ret__.retain_acked_messages,
        retry_policy=__ret__.retry_policy,
        state=__ret__.state,
        topic=__ret__.topic,
        topic_message_retention_duration=__ret__.topic_message_retention_duration)


@_utilities.lift_output_func(get_subscription)
def get_subscription_output(project: Optional[pulumi.Input[Optional[str]]] = None,
                            subscription_id: Optional[pulumi.Input[str]] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSubscriptionResult]:
    """
    Gets the configuration details of a subscription.
    """
    ...
