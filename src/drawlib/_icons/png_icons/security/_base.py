# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Security vendor and OSS icon provider configuration and writer."""

from __future__ import annotations

from drawlib._icons.png_icons._base import PngIconProvider

SECURITY_ALIASES: dict[str, str] = {
    "aqua": "aqua_security",
    "azure_ad": "entra_id",
    "bigip": "f5",
    "burp": "burp_suite",
    "check_point": "checkpoint",
    "chronicle": "google_secops",
    "cisco_duo": "duo",
    "defender": "microsoft_defender",
    "entra": "entra_id",
    "falcon": "crowdstrike",
    "fireeye": "trellix",
    "fortigate": "fortinet",
    "gpg": "gnupg",
    "ibm_qradar": "qradar",
    "letsencrypt": "lets_encrypt",
    "mcafee": "trellix",
    "nessus": "tenable",
    "one_password": "onepassword",
    "paloalto": "palo_alto",
    "panw": "palo_alto",
    "ping": "ping_identity",
    "portswigger": "burp_suite",
    "s1": "sentinelone",
    "sumologic": "sumo_logic",
    "trend": "trend_micro",
    "vectra": "vectra_ai",
    "wg": "wireguard",
    "yubikey": "yubico",
}

SECURITY_PROVIDER = PngIconProvider(
    name="security",
    package_name="icon_security",
    asset_subdir="icons/security",
    aliases=SECURITY_ALIASES,
)

_write = SECURITY_PROVIDER.write
