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
    'GetPublicAdvertisedPrefixResult',
    'AwaitableGetPublicAdvertisedPrefixResult',
    'get_public_advertised_prefix',
    'get_public_advertised_prefix_output',
]

@pulumi.output_type
class GetPublicAdvertisedPrefixResult:
    def __init__(__self__, creation_timestamp=None, description=None, dns_verification_ip=None, fingerprint=None, ip_cidr_range=None, kind=None, name=None, public_delegated_prefixs=None, self_link=None, shared_secret=None, status=None):
        if creation_timestamp and not isinstance(creation_timestamp, str):
            raise TypeError("Expected argument 'creation_timestamp' to be a str")
        pulumi.set(__self__, "creation_timestamp", creation_timestamp)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if dns_verification_ip and not isinstance(dns_verification_ip, str):
            raise TypeError("Expected argument 'dns_verification_ip' to be a str")
        pulumi.set(__self__, "dns_verification_ip", dns_verification_ip)
        if fingerprint and not isinstance(fingerprint, str):
            raise TypeError("Expected argument 'fingerprint' to be a str")
        pulumi.set(__self__, "fingerprint", fingerprint)
        if ip_cidr_range and not isinstance(ip_cidr_range, str):
            raise TypeError("Expected argument 'ip_cidr_range' to be a str")
        pulumi.set(__self__, "ip_cidr_range", ip_cidr_range)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if public_delegated_prefixs and not isinstance(public_delegated_prefixs, list):
            raise TypeError("Expected argument 'public_delegated_prefixs' to be a list")
        pulumi.set(__self__, "public_delegated_prefixs", public_delegated_prefixs)
        if self_link and not isinstance(self_link, str):
            raise TypeError("Expected argument 'self_link' to be a str")
        pulumi.set(__self__, "self_link", self_link)
        if shared_secret and not isinstance(shared_secret, str):
            raise TypeError("Expected argument 'shared_secret' to be a str")
        pulumi.set(__self__, "shared_secret", shared_secret)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="creationTimestamp")
    def creation_timestamp(self) -> str:
        """
        Creation timestamp in RFC3339 text format.
        """
        return pulumi.get(self, "creation_timestamp")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        An optional description of this resource. Provide this property when you create the resource.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="dnsVerificationIp")
    def dns_verification_ip(self) -> str:
        """
        The IPv4 address to be used for reverse DNS verification.
        """
        return pulumi.get(self, "dns_verification_ip")

    @property
    @pulumi.getter
    def fingerprint(self) -> str:
        """
        Fingerprint of this resource. A hash of the contents stored in this object. This field is used in optimistic locking. This field will be ignored when inserting a new PublicAdvertisedPrefix. An up-to-date fingerprint must be provided in order to update the PublicAdvertisedPrefix, otherwise the request will fail with error 412 conditionNotMet. To see the latest fingerprint, make a get() request to retrieve a PublicAdvertisedPrefix.
        """
        return pulumi.get(self, "fingerprint")

    @property
    @pulumi.getter(name="ipCidrRange")
    def ip_cidr_range(self) -> str:
        """
        The IPv4 address range, in CIDR format, represented by this public advertised prefix.
        """
        return pulumi.get(self, "ip_cidr_range")

    @property
    @pulumi.getter
    def kind(self) -> str:
        """
        Type of the resource. Always compute#publicAdvertisedPrefix for public advertised prefixes.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression `[a-z]([-a-z0-9]*[a-z0-9])?` which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="publicDelegatedPrefixs")
    def public_delegated_prefixs(self) -> Sequence['outputs.PublicAdvertisedPrefixPublicDelegatedPrefixResponse']:
        """
        The list of public delegated prefixes that exist for this public advertised prefix.
        """
        return pulumi.get(self, "public_delegated_prefixs")

    @property
    @pulumi.getter(name="selfLink")
    def self_link(self) -> str:
        """
        Server-defined URL for the resource.
        """
        return pulumi.get(self, "self_link")

    @property
    @pulumi.getter(name="sharedSecret")
    def shared_secret(self) -> str:
        """
        The shared secret to be used for reverse DNS verification.
        """
        return pulumi.get(self, "shared_secret")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        The status of the public advertised prefix. Possible values include: - `INITIAL`: RPKI validation is complete. - `PTR_CONFIGURED`: User has configured the PTR. - `VALIDATED`: Reverse DNS lookup is successful. - `REVERSE_DNS_LOOKUP_FAILED`: Reverse DNS lookup failed. - `PREFIX_CONFIGURATION_IN_PROGRESS`: The prefix is being configured. - `PREFIX_CONFIGURATION_COMPLETE`: The prefix is fully configured. - `PREFIX_REMOVAL_IN_PROGRESS`: The prefix is being removed. 
        """
        return pulumi.get(self, "status")


class AwaitableGetPublicAdvertisedPrefixResult(GetPublicAdvertisedPrefixResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPublicAdvertisedPrefixResult(
            creation_timestamp=self.creation_timestamp,
            description=self.description,
            dns_verification_ip=self.dns_verification_ip,
            fingerprint=self.fingerprint,
            ip_cidr_range=self.ip_cidr_range,
            kind=self.kind,
            name=self.name,
            public_delegated_prefixs=self.public_delegated_prefixs,
            self_link=self.self_link,
            shared_secret=self.shared_secret,
            status=self.status)


def get_public_advertised_prefix(project: Optional[str] = None,
                                 public_advertised_prefix: Optional[str] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPublicAdvertisedPrefixResult:
    """
    Returns the specified PublicAdvertisedPrefix resource.
    """
    __args__ = dict()
    __args__['project'] = project
    __args__['publicAdvertisedPrefix'] = public_advertised_prefix
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('google-native:compute/beta:getPublicAdvertisedPrefix', __args__, opts=opts, typ=GetPublicAdvertisedPrefixResult).value

    return AwaitableGetPublicAdvertisedPrefixResult(
        creation_timestamp=__ret__.creation_timestamp,
        description=__ret__.description,
        dns_verification_ip=__ret__.dns_verification_ip,
        fingerprint=__ret__.fingerprint,
        ip_cidr_range=__ret__.ip_cidr_range,
        kind=__ret__.kind,
        name=__ret__.name,
        public_delegated_prefixs=__ret__.public_delegated_prefixs,
        self_link=__ret__.self_link,
        shared_secret=__ret__.shared_secret,
        status=__ret__.status)


@_utilities.lift_output_func(get_public_advertised_prefix)
def get_public_advertised_prefix_output(project: Optional[pulumi.Input[Optional[str]]] = None,
                                        public_advertised_prefix: Optional[pulumi.Input[str]] = None,
                                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetPublicAdvertisedPrefixResult]:
    """
    Returns the specified PublicAdvertisedPrefix resource.
    """
    ...
