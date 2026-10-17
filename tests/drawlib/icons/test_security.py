# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for Security and Original Security icons."""

from pathlib import Path

from drawlib._icons.png_icons.original_security._base import ORIGINAL_SECURITY_PROVIDER
from drawlib._icons.png_icons.security._base import SECURITY_PROVIDER
from drawlib.canvas import clear, save
from drawlib.diagrams.architecture import (
    ArchitectureDiagram,
    Node,
    OriginalSecurityIcon,
    SecurityIcon,
)
from drawlib.icons import original_security, security
from drawlib.styles import Styles
from drawlib.types import Style


class TestSecurityIcons:
    """Tests for official Security vendor/OSS icon provider and diagram enum."""

    def test_security_all_vendor_icons(self, tmp_path: Path) -> None:
        """Verify all 60 official security vendor and OSS icons render cleanly."""
        clear()
        names = [
            "okta",
            "auth0",
            "entra_id",
            "cyberark",
            "ping_identity",
            "onelogin",
            "duo",
            "teleport",
            "onepassword",
            "bitwarden",
            "crowdstrike",
            "sentinelone",
            "microsoft_defender",
            "trend_micro",
            "sophos",
            "trellix",
            "symantec",
            "kaspersky",
            "malwarebytes",
            "wazuh",
            "palo_alto",
            "fortinet",
            "checkpoint",
            "zscaler",
            "netskope",
            "cloudflare",
            "imperva",
            "f5",
            "proofpoint",
            "wireguard",
            "qradar",
            "google_secops",
            "sumo_logic",
            "graylog",
            "darktrace",
            "vectra_ai",
            "suricata",
            "zeek",
            "snort",
            "wireshark",
            "wiz",
            "aqua_security",
            "sysdig",
            "lacework",
            "tenable",
            "qualys",
            "rapid7",
            "checkmarx",
            "veracode",
            "owasp",
            "burp_suite",
            "metasploit",
            "nmap",
            "osquery",
            "lets_encrypt",
            "digicert",
            "sectigo",
            "venafi",
            "yubico",
            "gnupg",
        ]
        for idx, name in enumerate(names):
            col = idx % 10
            row = idx // 10
            fn = getattr(security, name)
            fn(xy=(10 + col * 9, 85 - row * 14), width=7, style=Style(), variant="default")

        out = tmp_path / "test_security_vendors.png"
        save(str(out))
        assert out.is_file()

    def test_security_aliases(self, tmp_path: Path) -> None:
        """Verify common shorthand aliases resolve to canonical security icons."""
        clear()
        security.azure_ad(xy=(15, 70), width=10, style=Style())
        security.falcon(xy=(30, 70), width=10, style=Style())
        security.defender(xy=(45, 70), width=10, style=Style())
        security.panw(xy=(60, 70), width=10, style=Style())
        security.chronicle(xy=(75, 70), width=10, style=Style())
        security.yubikey(xy=(90, 70), width=10, style=Style())
        security.gpg(xy=(15, 45), width=10, style=Style())
        security.burp(xy=(30, 45), width=10, style=Style())

        out = tmp_path / "test_security_aliases.png"
        save(str(out))
        assert out.is_file()

    def test_security_architecture_enum(self, tmp_path: Path) -> None:
        """Verify SecurityIcon works inside ArchitectureDiagram nodes."""
        clear()
        diag = ArchitectureDiagram(
            node_style=Styles.PrimaryFlat,
            node_text_style=Styles.Dark,
            edge_style=Styles.Primary,
            edge_text_style=Styles.Dark,
        )
        n1 = diag.add(Node("Okta", width=20, height=20, icon=SecurityIcon.OKTA), (20, 50))
        n2 = diag.add(Node("CrowdStrike", width=20, height=20, icon=SecurityIcon.CROWDSTRIKE), (50, 50))
        n3 = diag.add(Node("QRadar", width=20, height=20, icon=SecurityIcon.QRADAR), (80, 50))
        diag.connect(n1, n2)
        diag.connect(n2, n3)
        diag.draw((5, 10))
        out = tmp_path / "test_arch_security.png"
        save(str(out))
        assert out.is_file()

    def test_security_provider_metadata(self) -> None:
        """Verify provider package name and aliases mapping."""
        assert SECURITY_PROVIDER.name == "security"
        assert SECURITY_PROVIDER.package_name == "icon_security"
        assert SECURITY_PROVIDER.aliases["azure_ad"] == "entra_id"
        assert SECURITY_PROVIDER.aliases["falcon"] == "crowdstrike"
        assert SECURITY_PROVIDER.aliases["gpg"] == "gnupg"


class TestOriginalSecurityIcons:
    """Tests for Original Security icon provider and architecture diagram enum."""

    def test_original_security_concept_icons(self, tmp_path: Path) -> None:
        """Verify all 24 vendor-neutral security concept icons render cleanly."""
        clear()
        original_security.iam_sso(xy=(15, 80), width=12, style=Style(), variant="default")
        original_security.mfa_auth(xy=(30, 80), width=12, style=Style())
        original_security.pam_bastion(xy=(45, 80), width=12, style=Style())
        original_security.directory_service(xy=(60, 80), width=12, style=Style())
        original_security.firewall(xy=(75, 80), width=12, style=Style())
        original_security.waf(xy=(90, 80), width=12, style=Style())

        original_security.ddos_protection(xy=(15, 60), width=12, style=Style())
        original_security.vpn_gateway(xy=(30, 60), width=12, style=Style())
        original_security.zero_trust(xy=(45, 60), width=12, style=Style())
        original_security.edr_xdr(xy=(60, 60), width=12, style=Style())
        original_security.ids_ips(xy=(75, 60), width=12, style=Style())
        original_security.dlp(xy=(90, 60), width=12, style=Style())

        original_security.casb(xy=(15, 40), width=12, style=Style())
        original_security.email_security(xy=(30, 40), width=12, style=Style())
        original_security.pki_ca(xy=(45, 40), width=12, style=Style())
        original_security.hsm_kms(xy=(60, 40), width=12, style=Style())
        original_security.secret_vault(xy=(75, 40), width=12, style=Style())
        original_security.encryption(xy=(90, 40), width=12, style=Style())

        original_security.siem(xy=(15, 20), width=12, style=Style())
        original_security.soar(xy=(30, 20), width=12, style=Style())
        original_security.soc_center(xy=(45, 20), width=12, style=Style())
        original_security.threat_intel(xy=(60, 20), width=12, style=Style())
        original_security.vulnerability_scan(xy=(75, 20), width=12, style=Style())
        original_security.honeypot(xy=(90, 20), width=12, style=Style())

        out = tmp_path / "test_original_security_concepts.png"
        save(str(out))
        assert out.is_file()

    def test_original_security_vendor_icons(self, tmp_path: Path) -> None:
        """Verify all 60 2D pastel security vendor and OSS icons render cleanly."""
        clear()
        names = [
            "okta",
            "auth0",
            "entra_id",
            "cyberark",
            "ping_identity",
            "onelogin",
            "duo",
            "teleport",
            "onepassword",
            "bitwarden",
            "crowdstrike",
            "sentinelone",
            "microsoft_defender",
            "trend_micro",
            "sophos",
            "trellix",
            "symantec",
            "kaspersky",
            "malwarebytes",
            "wazuh",
            "palo_alto",
            "fortinet",
            "checkpoint",
            "zscaler",
            "netskope",
            "cloudflare",
            "imperva",
            "f5",
            "proofpoint",
            "wireguard",
            "qradar",
            "google_secops",
            "sumo_logic",
            "graylog",
            "darktrace",
            "vectra_ai",
            "suricata",
            "zeek",
            "snort",
            "wireshark",
            "wiz",
            "aqua_security",
            "sysdig",
            "lacework",
            "tenable",
            "qualys",
            "rapid7",
            "checkmarx",
            "veracode",
            "owasp",
            "burp_suite",
            "metasploit",
            "nmap",
            "osquery",
            "lets_encrypt",
            "digicert",
            "sectigo",
            "venafi",
            "yubico",
            "gnupg",
        ]
        for idx, name in enumerate(names):
            col = idx % 10
            row = idx // 10
            fn = getattr(original_security, name)
            fn(xy=(10 + col * 9, 85 - row * 14), width=7, style=Style(), variant="default")

        out = tmp_path / "test_original_security_vendors.png"
        save(str(out))
        assert out.is_file()

    def test_original_security_aliases(self, tmp_path: Path) -> None:
        """Verify common shorthand aliases resolve to canonical security icons."""
        clear()
        original_security.iam(xy=(20, 70), width=12, style=Style())
        original_security.mfa(xy=(40, 70), width=12, style=Style())
        original_security.ztna(xy=(60, 70), width=12, style=Style())
        original_security.edr(xy=(80, 70), width=12, style=Style())

        original_security.hsm(xy=(20, 40), width=12, style=Style())
        original_security.secrets_manager(xy=(40, 40), width=12, style=Style())
        original_security.soc(xy=(60, 40), width=12, style=Style())
        original_security.vuln_scanner(xy=(80, 40), width=12, style=Style())

        original_security.falcon(xy=(20, 15), width=12, style=Style())
        original_security.panw(xy=(40, 15), width=12, style=Style())
        original_security.yubikey(xy=(60, 15), width=12, style=Style())
        original_security.gpg(xy=(80, 15), width=12, style=Style())

        out = tmp_path / "test_original_security_aliases.png"
        save(str(out))
        assert out.is_file()

    def test_original_security_architecture_enum(self, tmp_path: Path) -> None:
        """Verify OriginalSecurityIcon works inside ArchitectureDiagram nodes."""
        clear()
        diag = ArchitectureDiagram(
            node_style=Styles.PrimaryFlat,
            node_text_style=Styles.Dark,
            edge_style=Styles.Primary,
            edge_text_style=Styles.Dark,
        )
        n1 = diag.add(Node("WAF", width=20, height=20, icon=OriginalSecurityIcon.WAF), (20, 50))
        n2 = diag.add(Node("Zero Trust", width=20, height=20, icon=OriginalSecurityIcon.ZERO_TRUST), (50, 50))
        n3 = diag.add(Node("CrowdStrike", width=20, height=20, icon=OriginalSecurityIcon.CROWDSTRIKE), (80, 50))
        diag.connect(n1, n2)
        diag.connect(n2, n3)
        diag.draw((5, 10))
        out = tmp_path / "test_arch_original_security.png"
        save(str(out))
        assert out.is_file()

    def test_original_security_provider_metadata(self) -> None:
        """Verify provider package name and aliases mapping."""
        assert ORIGINAL_SECURITY_PROVIDER.name == "original_security"
        assert ORIGINAL_SECURITY_PROVIDER.package_name == "icon_original_security"
        assert ORIGINAL_SECURITY_PROVIDER.aliases["ztna"] == "zero_trust"
        assert ORIGINAL_SECURITY_PROVIDER.aliases["kms"] == "hsm_kms"
        assert ORIGINAL_SECURITY_PROVIDER.aliases["falcon"] == "crowdstrike"
