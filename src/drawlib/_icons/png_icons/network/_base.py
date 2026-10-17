# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Network icon provider configuration and writer."""

from __future__ import annotations

from drawlib._icons.png_icons._base import PngIconProvider

NETWORK_ALIASES: dict[str, str] = {
    "adguard_home": "adguard",
    "apache_apisix": "apisix",
    "arista_networks": "arista",
    "aruba_networks": "aruba",
    "asus_router": "asus",
    "big_ip": "f5",
    "bind9": "bind",
    "certbot": "lets_encrypt",
    "cf": "cloudflare",
    "check_point": "checkpoint",
    "cisco_aaa_server": "cisco_ise",
    "cisco_access_switch": "cisco_l2_switch",
    "cisco_ap": "cisco_wireless_ap",
    "cisco_asa": "cisco_firewall",
    "cisco_carrier_router": "cisco_core_router",
    "cisco_chassis_router": "cisco_core_router",
    "cisco_chassis_switch": "cisco_core_switch",
    "cisco_content_switch": "cisco_load_balancer",
    "cisco_cucm": "cisco_voice_gateway",
    "cisco_datacenter_switch": "cisco_nexus_switch",
    "cisco_dwdm": "cisco_optical_transport",
    "cisco_edge_router": "cisco_wan_router",
    "cisco_firepower": "cisco_firewall",
    "cisco_internet_cloud": "cisco_wan_cloud",
    "cisco_ips": "cisco_ids_ips",
    "cisco_isr_router": "cisco_router",
    "cisco_meraki": "meraki",
    "cisco_mpls_cloud": "cisco_wan_cloud",
    "cisco_multilayer_switch": "cisco_l3_switch",
    "cisco_nac": "cisco_ise",
    "cisco_roadm": "cisco_optical_transport",
    "cisco_sd_wan": "cisco_wan_router",
    "cisco_ucs_server": "cisco_server",
    "cisco_umbrella": "cisco_web_security",
    "cisco_voip_phone": "cisco_ip_phone",
    "cisco_vpn_concentrator": "cisco_vpn_gateway",
    "cisco_wifi_ap": "cisco_wireless_ap",
    "cisco_wlc": "cisco_wireless_controller",
    "cisco_workgroup_switch": "cisco_l2_switch",
    "cisco_workstation": "cisco_client_pc",
    "cisco_wsa": "cisco_web_security",
    "dlink": "d_link",
    "f5_big_ip": "f5",
    "fortigate": "fortinet",
    "frr": "frrouting",
    "hpe_aruba": "aruba",
    "isc_bind": "bind",
    "juniper_networks": "juniper",
    "kong_gateway": "kong",
    "letsencrypt": "lets_encrypt",
    "nlnet_unbound": "unbound",
    "omada": "tp_link",
    "palo_alto_networks": "palo_alto",
    "pan_os": "palo_alto",
    "pdns": "powerdns",
    "pihole": "pi_hole",
    "routeros": "mikrotik",
    "squid_cache": "squid",
    "tplink": "tp_link",
    "traefik_proxy": "traefik",
    "unifi": "ubiquiti",
    "varnish_cache": "varnish",
    "wg": "wireguard",
    "yamaha_rtx": "yamaha",
}

NETWORK_PROVIDER = PngIconProvider(
    name="network",
    package_name="icon_network",
    asset_subdir="icons/network",
    aliases=NETWORK_ALIASES,
)

_write = NETWORK_PROVIDER.write
