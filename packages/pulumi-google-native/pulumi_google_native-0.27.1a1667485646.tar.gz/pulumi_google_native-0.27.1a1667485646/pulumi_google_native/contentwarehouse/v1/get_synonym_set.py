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
    'GetSynonymSetResult',
    'AwaitableGetSynonymSetResult',
    'get_synonym_set',
    'get_synonym_set_output',
]

@pulumi.output_type
class GetSynonymSetResult:
    def __init__(__self__, context=None, name=None, synonyms=None):
        if context and not isinstance(context, str):
            raise TypeError("Expected argument 'context' to be a str")
        pulumi.set(__self__, "context", context)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if synonyms and not isinstance(synonyms, list):
            raise TypeError("Expected argument 'synonyms' to be a list")
        pulumi.set(__self__, "synonyms", synonyms)

    @property
    @pulumi.getter
    def context(self) -> str:
        """
        This is a freeform field. Example contexts can be "sales," "engineering," "real estate," "accounting," etc. The context can be supplied during search requests.
        """
        return pulumi.get(self, "context")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The resource name of the SynonymSet This is mandatory for google.api.resource. Format: projects/{project_number}/locations/{location}/synonymSets/{context}.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def synonyms(self) -> Sequence['outputs.GoogleCloudContentwarehouseV1SynonymSetSynonymResponse']:
        """
        List of Synonyms for the context.
        """
        return pulumi.get(self, "synonyms")


class AwaitableGetSynonymSetResult(GetSynonymSetResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSynonymSetResult(
            context=self.context,
            name=self.name,
            synonyms=self.synonyms)


def get_synonym_set(location: Optional[str] = None,
                    project: Optional[str] = None,
                    synonym_set_id: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSynonymSetResult:
    """
    Gets a SynonymSet for a particular context. Throws a NOT_FOUND exception if the Synonymset does not exist
    """
    __args__ = dict()
    __args__['location'] = location
    __args__['project'] = project
    __args__['synonymSetId'] = synonym_set_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('google-native:contentwarehouse/v1:getSynonymSet', __args__, opts=opts, typ=GetSynonymSetResult).value

    return AwaitableGetSynonymSetResult(
        context=__ret__.context,
        name=__ret__.name,
        synonyms=__ret__.synonyms)


@_utilities.lift_output_func(get_synonym_set)
def get_synonym_set_output(location: Optional[pulumi.Input[str]] = None,
                           project: Optional[pulumi.Input[Optional[str]]] = None,
                           synonym_set_id: Optional[pulumi.Input[str]] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSynonymSetResult]:
    """
    Gets a SynonymSet for a particular context. Throws a NOT_FOUND exception if the Synonymset does not exist
    """
    ...
