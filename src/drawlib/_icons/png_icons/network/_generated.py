# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Network concept icon functions."""

from __future__ import annotations

from typing import Literal

from drawlib._core.l2_types import Coordinate, PosFloat
from drawlib._core.l3_styles import Style
from drawlib._icons.png_icons.network._base import _write


def cisco_aaa_server(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco aaa server.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_ise", style=style, variant=variant)


def cisco_access_switch(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco access switch.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_l2_switch", style=style, variant=variant)


def cisco_ap(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco ap.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_wireless_ap", style=style, variant=variant)


def cisco_asa(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco asa.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_firewall", style=style, variant=variant)


def cisco_carrier_router(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco carrier router.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_core_router", style=style, variant=variant)


def cisco_chassis_router(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco chassis router.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_core_router", style=style, variant=variant)


def cisco_chassis_switch(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco chassis switch.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_core_switch", style=style, variant=variant)


def cisco_client_pc(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco client pc.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_client_pc", style=style, variant=variant)


def cisco_content_switch(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco content switch.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_load_balancer", style=style, variant=variant)


def cisco_core_router(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco core router.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_core_router", style=style, variant=variant)


def cisco_core_switch(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco core switch.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_core_switch", style=style, variant=variant)


def cisco_cucm(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco cucm.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_voice_gateway", style=style, variant=variant)


def cisco_datacenter_switch(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco datacenter switch.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_nexus_switch", style=style, variant=variant)


def cisco_dwdm(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco dwdm.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_optical_transport", style=style, variant=variant)


def cisco_edge_router(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco edge router.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_wan_router", style=style, variant=variant)


def cisco_firepower(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco firepower.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_firewall", style=style, variant=variant)


def cisco_firewall(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco firewall.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_firewall", style=style, variant=variant)


def cisco_ids_ips(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco ids ips.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_ids_ips", style=style, variant=variant)


def cisco_internet_cloud(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco internet cloud.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_wan_cloud", style=style, variant=variant)


def cisco_ip_phone(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco ip phone.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_ip_phone", style=style, variant=variant)


def cisco_ips(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco ips.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_ids_ips", style=style, variant=variant)


def cisco_ise(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco ise.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_ise", style=style, variant=variant)


def cisco_isr_router(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco isr router.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_router", style=style, variant=variant)


def cisco_l2_switch(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco l2 switch.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_l2_switch", style=style, variant=variant)


def cisco_l3_switch(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco l3 switch.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_l3_switch", style=style, variant=variant)


def cisco_load_balancer(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco load balancer.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_load_balancer", style=style, variant=variant)


def cisco_mpls_cloud(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco mpls cloud.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_wan_cloud", style=style, variant=variant)


def cisco_multilayer_switch(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco multilayer switch.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_l3_switch", style=style, variant=variant)


def cisco_nac(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco nac.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_ise", style=style, variant=variant)


def cisco_nexus_switch(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco nexus switch.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_nexus_switch", style=style, variant=variant)


def cisco_optical_transport(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco optical transport.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_optical_transport", style=style, variant=variant)


def cisco_roadm(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco roadm.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_optical_transport", style=style, variant=variant)


def cisco_router(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco router.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_router", style=style, variant=variant)


def cisco_sd_wan(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco sd wan.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_wan_router", style=style, variant=variant)


def cisco_server(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco server.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_server", style=style, variant=variant)


def cisco_ucs_server(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco ucs server.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_server", style=style, variant=variant)


def cisco_umbrella(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco umbrella.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_web_security", style=style, variant=variant)


def cisco_voice_gateway(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco voice gateway.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_voice_gateway", style=style, variant=variant)


def cisco_voip_phone(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco voip phone.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_ip_phone", style=style, variant=variant)


def cisco_vpn_concentrator(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco vpn concentrator.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_vpn_gateway", style=style, variant=variant)


def cisco_vpn_gateway(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco vpn gateway.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_vpn_gateway", style=style, variant=variant)


def cisco_wan_cloud(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco wan cloud.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_wan_cloud", style=style, variant=variant)


def cisco_wan_router(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco wan router.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_wan_router", style=style, variant=variant)


def cisco_web_security(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco web security.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_web_security", style=style, variant=variant)


def cisco_wifi_ap(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco wifi ap.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_wireless_ap", style=style, variant=variant)


def cisco_wireless_ap(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco wireless ap.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_wireless_ap", style=style, variant=variant)


def cisco_wireless_controller(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco wireless controller.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_wireless_controller", style=style, variant=variant)


def cisco_wireless_router(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco wireless router.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_wireless_router", style=style, variant=variant)


def cisco_wlc(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco wlc.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_wireless_controller", style=style, variant=variant)


def cisco_workgroup_switch(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco workgroup switch.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_l2_switch", style=style, variant=variant)


def cisco_workstation(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco workstation.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_client_pc", style=style, variant=variant)


def cisco_wsa(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default", "classic", "modern"] = "default",
) -> None:
    """Draws an Network concept icon representing cisco wsa.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default' or 'classic' or 'modern'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cisco_web_security", style=style, variant=variant)
