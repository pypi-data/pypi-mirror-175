# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'AppEngineHttpTargetHttpMethod',
    'HttpTargetHttpMethod',
]


class AppEngineHttpTargetHttpMethod(str, Enum):
    """
    The HTTP method to use for the request. PATCH and OPTIONS are not permitted.
    """
    HTTP_METHOD_UNSPECIFIED = "HTTP_METHOD_UNSPECIFIED"
    """
    HTTP method unspecified. Defaults to POST.
    """
    POST = "POST"
    """
    HTTP POST
    """
    GET = "GET"
    """
    HTTP GET
    """
    HEAD = "HEAD"
    """
    HTTP HEAD
    """
    PUT = "PUT"
    """
    HTTP PUT
    """
    DELETE = "DELETE"
    """
    HTTP DELETE
    """
    PATCH = "PATCH"
    """
    HTTP PATCH
    """
    OPTIONS = "OPTIONS"
    """
    HTTP OPTIONS
    """


class HttpTargetHttpMethod(str, Enum):
    """
    Which HTTP method to use for the request.
    """
    HTTP_METHOD_UNSPECIFIED = "HTTP_METHOD_UNSPECIFIED"
    """
    HTTP method unspecified. Defaults to POST.
    """
    POST = "POST"
    """
    HTTP POST
    """
    GET = "GET"
    """
    HTTP GET
    """
    HEAD = "HEAD"
    """
    HTTP HEAD
    """
    PUT = "PUT"
    """
    HTTP PUT
    """
    DELETE = "DELETE"
    """
    HTTP DELETE
    """
    PATCH = "PATCH"
    """
    HTTP PATCH
    """
    OPTIONS = "OPTIONS"
    """
    HTTP OPTIONS
    """
