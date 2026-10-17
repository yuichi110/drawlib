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
    "adguard_home": "adguard",
    "ap": "wireless_ap",
    "apache_apisix": "apisix",
    "arista_networks": "arista",
    "aruba_networks": "aruba",
    "asus_router": "asus",
    "big_ip": "f5",
    "bind9": "bind",
    "branch_router": "router",
    "call_manager": "voice_gateway",
    "carrier_cloud": "wan_cloud",
    "carrier_router": "core_router",
    "certbot": "lets_encrypt",
    "cf": "cloudflare",
    "chassis_router": "core_router",
    "chassis_switch": "core_switch",
    "check_point": "checkpoint",
    "cisco_meraki": "meraki",
    "desktop_pc": "client_pc",
    "dlink": "d_link",
    "dwdm": "optical_transport",
    "edge_router": "wan_router",
    "f5_big_ip": "f5",
    "fabric_switch": "datacenter_switch",
    "fiber_switch": "optical_transport",
    "fortigate": "fortinet",
    "frr": "frrouting",
    "hpe_aruba": "aruba",
    "ids": "ids_ips",
    "internet_cloud": "wan_cloud",
    "intrusion_prevention": "ids_ips",
    "ips": "ids_ips",
    "isc_bind": "bind",
    "ise": "nac_server",
    "isr_router": "router",
    "juniper_networks": "juniper",
    "kong_gateway": "kong",
    "letsencrypt": "lets_encrypt",
    "mpls_cloud": "wan_cloud",
    "multilayer_switch": "l3_switch",
    "network_firewall": "firewall",
    "network_server": "server",
    "ngfw": "firewall",
    "nlnet_unbound": "unbound",
    "omada": "tp_link",
    "palo_alto_networks": "palo_alto",
    "pan_os": "palo_alto",
    "pbx": "voice_gateway",
    "pdns": "powerdns",
    "pihole": "pi_hole",
    "proxy_appliance": "web_security",
    "rack_server": "server",
    "radius_server": "nac_server",
    "roadm": "optical_transport",
    "routeros": "mikrotik",
    "sd_wan": "wan_router",
    "secure_web_gateway": "web_security",
    "sip_gateway": "voice_gateway",
    "spine_leaf_switch": "datacenter_switch",
    "squid_cache": "squid",
    "swg": "web_security",
    "switch": "l2_switch",
    "tplink": "tp_link",
    "traffic_manager": "load_balancer",
    "traefik_proxy": "traefik",
    "unifi": "ubiquiti",
    "varnish_cache": "varnish",
    "voip_phone": "ip_phone",
    "vpn": "vpn_gateway",
    "vpn_concentrator": "vpn_gateway",
    "wg": "wireguard",
    "wifi_ap": "wireless_ap",
    "wifi_router": "wireless_router",
    "wlan_controller": "wireless_controller",
    "wlc": "wireless_controller",
    "workgroup_switch": "l2_switch",
    "workstation": "client_pc",
    "yamaha_rtx": "yamaha",
}

ORIGINAL_NETWORK_PROVIDER = PngIconProvider(
    name="original_network",
    package_name="icon_original_network",
    asset_subdir="icons/original_network",
    aliases=ORIGINAL_NETWORK_ALIASES,
)

_write = ORIGINAL_NETWORK_PROVIDER.write
