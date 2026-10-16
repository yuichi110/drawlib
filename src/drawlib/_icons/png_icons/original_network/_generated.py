# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Network concept icon functions."""

from __future__ import annotations

from typing import Literal

from drawlib._core.l2_types import Coordinate, PosFloat
from drawlib._core.l3_styles import Style
from drawlib._icons.png_icons.original_network._base import _write


def aaa_server(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing aaa server.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="nac_server", style=style, variant=variant)


def access_point(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing access point.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="wireless_ap", style=style, variant=variant)


def access_switch(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing access switch.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="l2_switch", style=style, variant=variant)


def adc(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing adc.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="load_balancer", style=style, variant=variant)


def ap(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing ap.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="wireless_ap", style=style, variant=variant)


def branch_router(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing branch router.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="router", style=style, variant=variant)


def call_manager(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing call manager.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="voice_gateway", style=style, variant=variant)


def carrier_cloud(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing carrier cloud.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="wan_cloud", style=style, variant=variant)


def carrier_router(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing carrier router.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="core_router", style=style, variant=variant)


def chassis_router(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing chassis router.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="core_router", style=style, variant=variant)


def chassis_switch(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing chassis switch.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="core_switch", style=style, variant=variant)


def client_pc(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing client pc.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="client_pc", style=style, variant=variant)


def core_router(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing core router.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="core_router", style=style, variant=variant)


def core_switch(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing core switch.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="core_switch", style=style, variant=variant)


def datacenter_switch(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing datacenter switch.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="datacenter_switch", style=style, variant=variant)


def desktop_pc(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing desktop pc.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="client_pc", style=style, variant=variant)


def dwdm(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing dwdm.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="optical_transport", style=style, variant=variant)


def edge_router(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing edge router.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="wan_router", style=style, variant=variant)


def fabric_switch(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing fabric switch.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="datacenter_switch", style=style, variant=variant)


def fiber_switch(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing fiber switch.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="optical_transport", style=style, variant=variant)


def firewall(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing firewall.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="firewall", style=style, variant=variant)


def ids(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing ids.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="ids_ips", style=style, variant=variant)


def ids_ips(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing ids ips.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="ids_ips", style=style, variant=variant)


def internet_cloud(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing internet cloud.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="wan_cloud", style=style, variant=variant)


def intrusion_prevention(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing intrusion prevention.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="ids_ips", style=style, variant=variant)


def ip_phone(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing ip phone.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="ip_phone", style=style, variant=variant)


def ips(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing ips.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="ids_ips", style=style, variant=variant)


def ise(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing ise.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="nac_server", style=style, variant=variant)


def isr_router(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing isr router.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="router", style=style, variant=variant)


def l2_switch(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing l2 switch.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="l2_switch", style=style, variant=variant)


def l3_switch(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing l3 switch.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="l3_switch", style=style, variant=variant)


def load_balancer(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing load balancer.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="load_balancer", style=style, variant=variant)


def mpls_cloud(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing mpls cloud.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="wan_cloud", style=style, variant=variant)


def multilayer_switch(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing multilayer switch.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="l3_switch", style=style, variant=variant)


def nac_server(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing nac server.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="nac_server", style=style, variant=variant)


def network_firewall(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing network firewall.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="firewall", style=style, variant=variant)


def network_server(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing network server.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="server", style=style, variant=variant)


def ngfw(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing ngfw.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="firewall", style=style, variant=variant)


def optical_transport(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing optical transport.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="optical_transport", style=style, variant=variant)


def pbx(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing pbx.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="voice_gateway", style=style, variant=variant)


def proxy_appliance(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing proxy appliance.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="web_security", style=style, variant=variant)


def rack_server(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing rack server.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="server", style=style, variant=variant)


def radius_server(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing radius server.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="nac_server", style=style, variant=variant)


def roadm(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing roadm.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="optical_transport", style=style, variant=variant)


def router(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing router.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="router", style=style, variant=variant)


def sd_wan(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing sd wan.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="wan_router", style=style, variant=variant)


def secure_web_gateway(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing secure web gateway.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="web_security", style=style, variant=variant)


def server(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing server.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="server", style=style, variant=variant)


def sip_gateway(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing sip gateway.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="voice_gateway", style=style, variant=variant)


def spine_leaf_switch(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing spine leaf switch.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="datacenter_switch", style=style, variant=variant)


def swg(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing swg.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="web_security", style=style, variant=variant)


def switch(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing switch.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="l2_switch", style=style, variant=variant)


def traffic_manager(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing traffic manager.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="load_balancer", style=style, variant=variant)


def voice_gateway(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing voice gateway.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="voice_gateway", style=style, variant=variant)


def voip_phone(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing voip phone.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="ip_phone", style=style, variant=variant)


def vpn(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing vpn.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="vpn_gateway", style=style, variant=variant)


def vpn_concentrator(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing vpn concentrator.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="vpn_gateway", style=style, variant=variant)


def vpn_gateway(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing vpn gateway.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="vpn_gateway", style=style, variant=variant)


def wan_cloud(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing wan cloud.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="wan_cloud", style=style, variant=variant)


def wan_router(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing wan router.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="wan_router", style=style, variant=variant)


def web_security(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing web security.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="web_security", style=style, variant=variant)


def wifi_ap(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing wifi ap.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="wireless_ap", style=style, variant=variant)


def wifi_router(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing wifi router.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="wireless_router", style=style, variant=variant)


def wireless_ap(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing wireless ap.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="wireless_ap", style=style, variant=variant)


def wireless_controller(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing wireless controller.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="wireless_controller", style=style, variant=variant)


def wireless_router(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing wireless router.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="wireless_router", style=style, variant=variant)


def wlan_controller(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing wlan controller.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="wireless_controller", style=style, variant=variant)


def wlc(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing wlc.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="wireless_controller", style=style, variant=variant)


def workgroup_switch(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing workgroup switch.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="l2_switch", style=style, variant=variant)


def workstation(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original Network concept icon representing workstation.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="client_pc", style=style, variant=variant)
