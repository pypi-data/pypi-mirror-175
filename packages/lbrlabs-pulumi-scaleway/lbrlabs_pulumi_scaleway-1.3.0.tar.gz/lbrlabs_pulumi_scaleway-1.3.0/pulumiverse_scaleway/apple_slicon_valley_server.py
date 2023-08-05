# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['AppleSliconValleyServerArgs', 'AppleSliconValleyServer']

@pulumi.input_type
class AppleSliconValleyServerArgs:
    def __init__(__self__, *,
                 type: pulumi.Input[str],
                 name: Optional[pulumi.Input[str]] = None,
                 project_id: Optional[pulumi.Input[str]] = None,
                 zone: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a AppleSliconValleyServer resource.
        :param pulumi.Input[str] type: The commercial type of the server. You find all the available types on
               the [pricing page](https://www.scaleway.com/en/pricing/#apple-silicon). Updates to this field will recreate a new
               resource.
        :param pulumi.Input[str] name: The name of the server.
        :param pulumi.Input[str] project_id: `project_id`) The ID of the project the server is
               associated with.
        :param pulumi.Input[str] zone: `zone`) The zone in which
               the server should be created.
        """
        pulumi.set(__self__, "type", type)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project_id is not None:
            pulumi.set(__self__, "project_id", project_id)
        if zone is not None:
            pulumi.set(__self__, "zone", zone)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """
        The commercial type of the server. You find all the available types on
        the [pricing page](https://www.scaleway.com/en/pricing/#apple-silicon). Updates to this field will recreate a new
        resource.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the server.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> Optional[pulumi.Input[str]]:
        """
        `project_id`) The ID of the project the server is
        associated with.
        """
        return pulumi.get(self, "project_id")

    @project_id.setter
    def project_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project_id", value)

    @property
    @pulumi.getter
    def zone(self) -> Optional[pulumi.Input[str]]:
        """
        `zone`) The zone in which
        the server should be created.
        """
        return pulumi.get(self, "zone")

    @zone.setter
    def zone(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "zone", value)


@pulumi.input_type
class _AppleSliconValleyServerState:
    def __init__(__self__, *,
                 created_at: Optional[pulumi.Input[str]] = None,
                 deletable_at: Optional[pulumi.Input[str]] = None,
                 ip: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 organization_id: Optional[pulumi.Input[str]] = None,
                 project_id: Optional[pulumi.Input[str]] = None,
                 state: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 updated_at: Optional[pulumi.Input[str]] = None,
                 vnc_url: Optional[pulumi.Input[str]] = None,
                 zone: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering AppleSliconValleyServer resources.
        :param pulumi.Input[str] created_at: The date and time of the creation of the Apple Silicon server.
        :param pulumi.Input[str] deletable_at: The minimal date and time on which you can delete this server due to Apple licence
        :param pulumi.Input[str] ip: IPv4 address of the server (IPv4 address).
        :param pulumi.Input[str] name: The name of the server.
        :param pulumi.Input[str] organization_id: The organization ID the server is associated with.
        :param pulumi.Input[str] project_id: `project_id`) The ID of the project the server is
               associated with.
        :param pulumi.Input[str] state: The state of the server. Check the possible values on
               our [sdk](https://github.com/scaleway/scaleway-sdk-go/blob/master/api/applesilicon/v1alpha1/applesilicon_sdk.go#L103).
        :param pulumi.Input[str] type: The commercial type of the server. You find all the available types on
               the [pricing page](https://www.scaleway.com/en/pricing/#apple-silicon). Updates to this field will recreate a new
               resource.
        :param pulumi.Input[str] updated_at: The date and time of the last update of the Apple Silicon server.
        :param pulumi.Input[str] vnc_url: URL of the VNC.
        :param pulumi.Input[str] zone: `zone`) The zone in which
               the server should be created.
        """
        if created_at is not None:
            pulumi.set(__self__, "created_at", created_at)
        if deletable_at is not None:
            pulumi.set(__self__, "deletable_at", deletable_at)
        if ip is not None:
            pulumi.set(__self__, "ip", ip)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if organization_id is not None:
            pulumi.set(__self__, "organization_id", organization_id)
        if project_id is not None:
            pulumi.set(__self__, "project_id", project_id)
        if state is not None:
            pulumi.set(__self__, "state", state)
        if type is not None:
            pulumi.set(__self__, "type", type)
        if updated_at is not None:
            pulumi.set(__self__, "updated_at", updated_at)
        if vnc_url is not None:
            pulumi.set(__self__, "vnc_url", vnc_url)
        if zone is not None:
            pulumi.set(__self__, "zone", zone)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[pulumi.Input[str]]:
        """
        The date and time of the creation of the Apple Silicon server.
        """
        return pulumi.get(self, "created_at")

    @created_at.setter
    def created_at(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "created_at", value)

    @property
    @pulumi.getter(name="deletableAt")
    def deletable_at(self) -> Optional[pulumi.Input[str]]:
        """
        The minimal date and time on which you can delete this server due to Apple licence
        """
        return pulumi.get(self, "deletable_at")

    @deletable_at.setter
    def deletable_at(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "deletable_at", value)

    @property
    @pulumi.getter
    def ip(self) -> Optional[pulumi.Input[str]]:
        """
        IPv4 address of the server (IPv4 address).
        """
        return pulumi.get(self, "ip")

    @ip.setter
    def ip(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ip", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the server.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="organizationId")
    def organization_id(self) -> Optional[pulumi.Input[str]]:
        """
        The organization ID the server is associated with.
        """
        return pulumi.get(self, "organization_id")

    @organization_id.setter
    def organization_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "organization_id", value)

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> Optional[pulumi.Input[str]]:
        """
        `project_id`) The ID of the project the server is
        associated with.
        """
        return pulumi.get(self, "project_id")

    @project_id.setter
    def project_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project_id", value)

    @property
    @pulumi.getter
    def state(self) -> Optional[pulumi.Input[str]]:
        """
        The state of the server. Check the possible values on
        our [sdk](https://github.com/scaleway/scaleway-sdk-go/blob/master/api/applesilicon/v1alpha1/applesilicon_sdk.go#L103).
        """
        return pulumi.get(self, "state")

    @state.setter
    def state(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "state", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        The commercial type of the server. You find all the available types on
        the [pricing page](https://www.scaleway.com/en/pricing/#apple-silicon). Updates to this field will recreate a new
        resource.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="updatedAt")
    def updated_at(self) -> Optional[pulumi.Input[str]]:
        """
        The date and time of the last update of the Apple Silicon server.
        """
        return pulumi.get(self, "updated_at")

    @updated_at.setter
    def updated_at(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "updated_at", value)

    @property
    @pulumi.getter(name="vncUrl")
    def vnc_url(self) -> Optional[pulumi.Input[str]]:
        """
        URL of the VNC.
        """
        return pulumi.get(self, "vnc_url")

    @vnc_url.setter
    def vnc_url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vnc_url", value)

    @property
    @pulumi.getter
    def zone(self) -> Optional[pulumi.Input[str]]:
        """
        `zone`) The zone in which
        the server should be created.
        """
        return pulumi.get(self, "zone")

    @zone.setter
    def zone(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "zone", value)


class AppleSliconValleyServer(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project_id: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 zone: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Creates and manages Scaleway Apple silicon M1. For more information,
        see [the documentation](https://www.scaleway.com/en/docs/compute/apple-silicon/concepts).

        ## Examples

        ### Basic

        ```python
        import pulumi
        import lbrlabs_scaleway as scaleway

        server = scaleway.AppleSliconValleyServer("server", type="M1-M")
        ```

        ## Import

        Instance servers can be imported using the `{zone}/{id}`, e.g. bash

        ```sh
         $ pulumi import scaleway:index/appleSliconValleyServer:AppleSliconValleyServer server fr-par-1/11111111-1111-1111-1111-111111111111
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: The name of the server.
        :param pulumi.Input[str] project_id: `project_id`) The ID of the project the server is
               associated with.
        :param pulumi.Input[str] type: The commercial type of the server. You find all the available types on
               the [pricing page](https://www.scaleway.com/en/pricing/#apple-silicon). Updates to this field will recreate a new
               resource.
        :param pulumi.Input[str] zone: `zone`) The zone in which
               the server should be created.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AppleSliconValleyServerArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Creates and manages Scaleway Apple silicon M1. For more information,
        see [the documentation](https://www.scaleway.com/en/docs/compute/apple-silicon/concepts).

        ## Examples

        ### Basic

        ```python
        import pulumi
        import lbrlabs_scaleway as scaleway

        server = scaleway.AppleSliconValleyServer("server", type="M1-M")
        ```

        ## Import

        Instance servers can be imported using the `{zone}/{id}`, e.g. bash

        ```sh
         $ pulumi import scaleway:index/appleSliconValleyServer:AppleSliconValleyServer server fr-par-1/11111111-1111-1111-1111-111111111111
        ```

        :param str resource_name: The name of the resource.
        :param AppleSliconValleyServerArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AppleSliconValleyServerArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project_id: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 zone: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AppleSliconValleyServerArgs.__new__(AppleSliconValleyServerArgs)

            __props__.__dict__["name"] = name
            __props__.__dict__["project_id"] = project_id
            if type is None and not opts.urn:
                raise TypeError("Missing required property 'type'")
            __props__.__dict__["type"] = type
            __props__.__dict__["zone"] = zone
            __props__.__dict__["created_at"] = None
            __props__.__dict__["deletable_at"] = None
            __props__.__dict__["ip"] = None
            __props__.__dict__["organization_id"] = None
            __props__.__dict__["state"] = None
            __props__.__dict__["updated_at"] = None
            __props__.__dict__["vnc_url"] = None
        super(AppleSliconValleyServer, __self__).__init__(
            'scaleway:index/appleSliconValleyServer:AppleSliconValleyServer',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            created_at: Optional[pulumi.Input[str]] = None,
            deletable_at: Optional[pulumi.Input[str]] = None,
            ip: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            organization_id: Optional[pulumi.Input[str]] = None,
            project_id: Optional[pulumi.Input[str]] = None,
            state: Optional[pulumi.Input[str]] = None,
            type: Optional[pulumi.Input[str]] = None,
            updated_at: Optional[pulumi.Input[str]] = None,
            vnc_url: Optional[pulumi.Input[str]] = None,
            zone: Optional[pulumi.Input[str]] = None) -> 'AppleSliconValleyServer':
        """
        Get an existing AppleSliconValleyServer resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] created_at: The date and time of the creation of the Apple Silicon server.
        :param pulumi.Input[str] deletable_at: The minimal date and time on which you can delete this server due to Apple licence
        :param pulumi.Input[str] ip: IPv4 address of the server (IPv4 address).
        :param pulumi.Input[str] name: The name of the server.
        :param pulumi.Input[str] organization_id: The organization ID the server is associated with.
        :param pulumi.Input[str] project_id: `project_id`) The ID of the project the server is
               associated with.
        :param pulumi.Input[str] state: The state of the server. Check the possible values on
               our [sdk](https://github.com/scaleway/scaleway-sdk-go/blob/master/api/applesilicon/v1alpha1/applesilicon_sdk.go#L103).
        :param pulumi.Input[str] type: The commercial type of the server. You find all the available types on
               the [pricing page](https://www.scaleway.com/en/pricing/#apple-silicon). Updates to this field will recreate a new
               resource.
        :param pulumi.Input[str] updated_at: The date and time of the last update of the Apple Silicon server.
        :param pulumi.Input[str] vnc_url: URL of the VNC.
        :param pulumi.Input[str] zone: `zone`) The zone in which
               the server should be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AppleSliconValleyServerState.__new__(_AppleSliconValleyServerState)

        __props__.__dict__["created_at"] = created_at
        __props__.__dict__["deletable_at"] = deletable_at
        __props__.__dict__["ip"] = ip
        __props__.__dict__["name"] = name
        __props__.__dict__["organization_id"] = organization_id
        __props__.__dict__["project_id"] = project_id
        __props__.__dict__["state"] = state
        __props__.__dict__["type"] = type
        __props__.__dict__["updated_at"] = updated_at
        __props__.__dict__["vnc_url"] = vnc_url
        __props__.__dict__["zone"] = zone
        return AppleSliconValleyServer(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> pulumi.Output[str]:
        """
        The date and time of the creation of the Apple Silicon server.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="deletableAt")
    def deletable_at(self) -> pulumi.Output[str]:
        """
        The minimal date and time on which you can delete this server due to Apple licence
        """
        return pulumi.get(self, "deletable_at")

    @property
    @pulumi.getter
    def ip(self) -> pulumi.Output[str]:
        """
        IPv4 address of the server (IPv4 address).
        """
        return pulumi.get(self, "ip")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the server.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="organizationId")
    def organization_id(self) -> pulumi.Output[str]:
        """
        The organization ID the server is associated with.
        """
        return pulumi.get(self, "organization_id")

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> pulumi.Output[str]:
        """
        `project_id`) The ID of the project the server is
        associated with.
        """
        return pulumi.get(self, "project_id")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        The state of the server. Check the possible values on
        our [sdk](https://github.com/scaleway/scaleway-sdk-go/blob/master/api/applesilicon/v1alpha1/applesilicon_sdk.go#L103).
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The commercial type of the server. You find all the available types on
        the [pricing page](https://www.scaleway.com/en/pricing/#apple-silicon). Updates to this field will recreate a new
        resource.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="updatedAt")
    def updated_at(self) -> pulumi.Output[str]:
        """
        The date and time of the last update of the Apple Silicon server.
        """
        return pulumi.get(self, "updated_at")

    @property
    @pulumi.getter(name="vncUrl")
    def vnc_url(self) -> pulumi.Output[str]:
        """
        URL of the VNC.
        """
        return pulumi.get(self, "vnc_url")

    @property
    @pulumi.getter
    def zone(self) -> pulumi.Output[str]:
        """
        `zone`) The zone in which
        the server should be created.
        """
        return pulumi.get(self, "zone")

