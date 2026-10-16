# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Network icon provider configuration and writer."""

from __future__ import annotations

from drawlib._icons.png_icons._base import PngIconProvider

ORIGINAL_NETWORK_ALIASES: dict[str, str] = {
    "aaa_server": "nac_server",
    "access_point": "wireless_ap",
    "access_switch": "l2_switch",
    "adc": "load_balancer",
    "ap": "wireless_ap",
    "branch_router": "router",
    "call_manager": "voice_gateway",
    "carrier_cloud": "wan_cloud",
    "carrier_router": "core_router",
    "chassis_router": "core_router",
    "chassis_switch": "core_switch",
    "desktop_pc": "client_pc",
    "dwdm": "optical_transport",
    "edge_router": "wan_router",
    "fabric_switch": "datacenter_switch",
    "fiber_switch": "optical_transport",
    "ids": "ids_ips",
    "internet_cloud": "wan_cloud",
    "intrusion_prevention": "ids_ips",
    "ips": "ids_ips",
    "ise": "nac_server",
    "isr_router": "router",
    "mpls_cloud": "wan_cloud",
    "multilayer_switch": "l3_switch",
    "network_firewall": "firewall",
    "network_server": "server",
    "ngfw": "firewall",
    "pbx": "voice_gateway",
    "proxy_appliance": "web_security",
    "rack_server": "server",
    "radius_server": "nac_server",
    "roadm": "optical_transport",
    "sd_wan": "wan_router",
    "secure_web_gateway": "web_security",
    "sip_gateway": "voice_gateway",
    "spine_leaf_switch": "datacenter_switch",
    "swg": "web_security",
    "switch": "l2_switch",
    "traffic_manager": "load_balancer",
    "voip_phone": "ip_phone",
    "vpn": "vpn_gateway",
    "vpn_concentrator": "vpn_gateway",
    "wifi_ap": "wireless_ap",
    "wifi_router": "wireless_router",
    "wlan_controller": "wireless_controller",
    "wlc": "wireless_controller",
    "workgroup_switch": "l2_switch",
    "workstation": "client_pc",
}

ORIGINAL_NETWORK_PROVIDER = PngIconProvider(
    name="original_network",
    package_name="icon_original_network",
    asset_subdir="icons/original_network",
    aliases=ORIGINAL_NETWORK_ALIASES,
)

_write = ORIGINAL_NETWORK_PROVIDER.write
