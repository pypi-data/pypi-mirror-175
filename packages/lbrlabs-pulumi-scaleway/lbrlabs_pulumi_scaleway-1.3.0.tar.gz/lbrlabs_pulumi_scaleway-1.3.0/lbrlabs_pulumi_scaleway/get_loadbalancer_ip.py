# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = [
    'GetLoadbalancerIpResult',
    'AwaitableGetLoadbalancerIpResult',
    'get_loadbalancer_ip',
    'get_loadbalancer_ip_output',
]

@pulumi.output_type
class GetLoadbalancerIpResult:
    """
    A collection of values returned by getLoadbalancerIp.
    """
    def __init__(__self__, id=None, ip_address=None, ip_id=None, lb_id=None, organization_id=None, project_id=None, region=None, reverse=None, zone=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ip_address and not isinstance(ip_address, str):
            raise TypeError("Expected argument 'ip_address' to be a str")
        pulumi.set(__self__, "ip_address", ip_address)
        if ip_id and not isinstance(ip_id, str):
            raise TypeError("Expected argument 'ip_id' to be a str")
        pulumi.set(__self__, "ip_id", ip_id)
        if lb_id and not isinstance(lb_id, str):
            raise TypeError("Expected argument 'lb_id' to be a str")
        pulumi.set(__self__, "lb_id", lb_id)
        if organization_id and not isinstance(organization_id, str):
            raise TypeError("Expected argument 'organization_id' to be a str")
        pulumi.set(__self__, "organization_id", organization_id)
        if project_id and not isinstance(project_id, str):
            raise TypeError("Expected argument 'project_id' to be a str")
        pulumi.set(__self__, "project_id", project_id)
        if region and not isinstance(region, str):
            raise TypeError("Expected argument 'region' to be a str")
        pulumi.set(__self__, "region", region)
        if reverse and not isinstance(reverse, str):
            raise TypeError("Expected argument 'reverse' to be a str")
        pulumi.set(__self__, "reverse", reverse)
        if zone and not isinstance(zone, str):
            raise TypeError("Expected argument 'zone' to be a str")
        pulumi.set(__self__, "zone", zone)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="ipAddress")
    def ip_address(self) -> Optional[str]:
        return pulumi.get(self, "ip_address")

    @property
    @pulumi.getter(name="ipId")
    def ip_id(self) -> Optional[str]:
        return pulumi.get(self, "ip_id")

    @property
    @pulumi.getter(name="lbId")
    def lb_id(self) -> str:
        """
        The associated load-balancer ID if any
        """
        return pulumi.get(self, "lb_id")

    @property
    @pulumi.getter(name="organizationId")
    def organization_id(self) -> str:
        """
        (Defaults to provider `organization_id`) The ID of the organization the LB IP is associated with.
        """
        return pulumi.get(self, "organization_id")

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> str:
        return pulumi.get(self, "project_id")

    @property
    @pulumi.getter
    def region(self) -> str:
        return pulumi.get(self, "region")

    @property
    @pulumi.getter
    def reverse(self) -> str:
        """
        The reverse domain associated with this IP.
        """
        return pulumi.get(self, "reverse")

    @property
    @pulumi.getter
    def zone(self) -> str:
        return pulumi.get(self, "zone")


class AwaitableGetLoadbalancerIpResult(GetLoadbalancerIpResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetLoadbalancerIpResult(
            id=self.id,
            ip_address=self.ip_address,
            ip_id=self.ip_id,
            lb_id=self.lb_id,
            organization_id=self.organization_id,
            project_id=self.project_id,
            region=self.region,
            reverse=self.reverse,
            zone=self.zone)


def get_loadbalancer_ip(ip_address: Optional[str] = None,
                        ip_id: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetLoadbalancerIpResult:
    """
    Gets information about a Load Balancer IP.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_scaleway as scaleway

    my_ip = scaleway.get_loadbalancer_ip(ip_id="11111111-1111-1111-1111-111111111111")
    ```


    :param str ip_address: The IP address.
           Only one of `ip_address` and `ip_id` should be specified.
    :param str ip_id: The IP ID.
           Only one of `ip_address` and `ip_id` should be specified.
    """
    __args__ = dict()
    __args__['ipAddress'] = ip_address
    __args__['ipId'] = ip_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('scaleway:index/getLoadbalancerIp:getLoadbalancerIp', __args__, opts=opts, typ=GetLoadbalancerIpResult).value

    return AwaitableGetLoadbalancerIpResult(
        id=__ret__.id,
        ip_address=__ret__.ip_address,
        ip_id=__ret__.ip_id,
        lb_id=__ret__.lb_id,
        organization_id=__ret__.organization_id,
        project_id=__ret__.project_id,
        region=__ret__.region,
        reverse=__ret__.reverse,
        zone=__ret__.zone)


@_utilities.lift_output_func(get_loadbalancer_ip)
def get_loadbalancer_ip_output(ip_address: Optional[pulumi.Input[Optional[str]]] = None,
                               ip_id: Optional[pulumi.Input[Optional[str]]] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetLoadbalancerIpResult]:
    """
    Gets information about a Load Balancer IP.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_scaleway as scaleway

    my_ip = scaleway.get_loadbalancer_ip(ip_id="11111111-1111-1111-1111-111111111111")
    ```


    :param str ip_address: The IP address.
           Only one of `ip_address` and `ip_id` should be specified.
    :param str ip_id: The IP ID.
           Only one of `ip_address` and `ip_id` should be specified.
    """
    ...
