# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security icon provider configuration and writer."""

from __future__ import annotations

from drawlib._icons.png_icons._base import PngIconProvider

ORIGINAL_SECURITY_ALIASES: dict[str, str] = {
    "active_directory": "directory_service",
    "ad": "directory_service",
    "anti_ddos": "ddos_protection",
    "anti_phishing": "email_security",
    "antivirus": "edr_xdr",
    "bastion": "pam_bastion",
    "bastion_host": "pam_bastion",
    "ca": "pki_ca",
    "certificate_authority": "pki_ca",
    "certificate_tls": "pki_ca",
    "cipher": "encryption",
    "cloud_access_security": "casb",
    "cti": "threat_intel",
    "dast": "vulnerability_scan",
    "data_encryption": "encryption",
    "data_loss_prevention": "dlp",
    "ddos": "ddos_protection",
    "deception": "honeypot",
    "decoy": "honeypot",
    "edr": "edr_xdr",
    "endpoint_security": "edr_xdr",
    "hsm": "hsm_kms",
    "iam": "iam_sso",
    "identity": "iam_sso",
    "identity_auth": "iam_sso",
    "ids": "ids_ips",
    "intrusion_prevention": "ids_ips",
    "ips": "ids_ips",
    "ipsec_vpn": "vpn_gateway",
    "key_management": "hsm_kms",
    "kms": "hsm_kms",
    "ldap": "directory_service",
    "log_analytics": "siem",
    "mfa": "mfa_auth",
    "ndr": "ids_ips",
    "network_firewall": "firewall",
    "ngfw": "firewall",
    "pam": "pam_bastion",
    "passkey": "mfa_auth",
    "password_vault": "secret_vault",
    "playbook": "soar",
    "privileged_access": "pam_bastion",
    "sase": "zero_trust",
    "sast": "vulnerability_scan",
    "scrubbing_center": "ddos_protection",
    "sdp": "zero_trust",
    "secrets_manager": "secret_vault",
    "secure_email_gateway": "email_security",
    "security_analytics": "siem",
    "security_automation": "soar",
    "security_operations": "soc_center",
    "security_scan": "vulnerability_scan",
    "seg": "email_security",
    "single_sign_on": "iam_sso",
    "soc": "soc_center",
    "sso": "iam_sso",
    "threat_hunting": "threat_intel",
    "threat_intelligence": "threat_intel",
    "tls_cert": "pki_ca",
    "totp": "mfa_auth",
    "two_factor": "mfa_auth",
    "vpn": "vpn_gateway",
    "vpn_tunnel": "vpn_gateway",
    "vuln_scanner": "vulnerability_scan",
    "web_application_firewall": "waf",
    "xdr": "edr_xdr",
    "zero_trust_proxy": "zero_trust",
    "ztna": "zero_trust",
}

ORIGINAL_SECURITY_PROVIDER = PngIconProvider(
    name="original_security",
    package_name="icon_original_security",
    asset_subdir="icons/original_security",
    aliases=ORIGINAL_SECURITY_ALIASES,
)

_write = ORIGINAL_SECURITY_PROVIDER.write
