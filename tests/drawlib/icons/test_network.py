# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for Network (Cisco) icons drawing."""

from pathlib import Path

import pytest

from drawlib._icons.png_icons.network._base import NETWORK_PROVIDER
from drawlib._icons.png_icons.original_network._base import ORIGINAL_NETWORK_PROVIDER
from drawlib.canvas import clear, save
from drawlib.diagrams.architecture import ArchitectureDiagram, NetworkIcon, Node, OriginalNetworkIcon
from drawlib.icons import network, original_network
from drawlib.styles import Styles
from drawlib.types import Style


class TestNetworkIcons:
    """Tests for Network (Cisco) icon provider and architecture diagram enum."""

    def test_network_cisco_icons_and_variants(self, tmp_path: Path) -> None:
        """Verify Cisco icons across default, classic, and modern variants."""
        clear()
        network.cisco_router(xy=(15, 75), width=12, style=Style(), variant="default")
        network.cisco_router(xy=(35, 75), width=12, style=Style(), variant="classic")
        network.cisco_router(xy=(55, 75), width=12, style=Style(), variant="modern")
        network.cisco_core_router(xy=(75, 75), width=12, style=Style())

        network.cisco_l2_switch(xy=(15, 50), width=12, style=Style())
        network.cisco_l3_switch(xy=(35, 50), width=12, style=Style(), variant="modern")
        network.cisco_core_switch(xy=(55, 50), width=12, style=Style())
        network.cisco_firewall(xy=(75, 50), width=12, style=Style(), variant="modern")

        network.cisco_wireless_ap(xy=(15, 25), width=12, style=Style())
        network.cisco_wan_cloud(xy=(35, 25), width=12, style=Style())
        network.cisco_ip_phone(xy=(55, 25), width=12, style=Style(), variant="modern")
        network.cisco_client_pc(xy=(75, 25), width=12, style=Style())

        out = tmp_path / "test_network.png"
        save(str(out))
        assert out.is_file()

    def test_network_classic_resolves_to_default(self) -> None:
        """Verify variant='classic' resolves to the exact same PNG file as variant='default'."""
        p_default = NETWORK_PROVIDER.get_icon_path("cisco_router", variant="default")
        p_classic = NETWORK_PROVIDER.get_icon_path("cisco_router", variant="classic")
        p_modern = NETWORK_PROVIDER.get_icon_path("cisco_router", variant="modern")
        assert p_default == p_classic
        assert p_default != p_modern
        assert p_default.endswith("cisco_router_default.png")
        assert p_modern.endswith("cisco_router_modern.png")

    def test_network_architecture_diagram_enum(self, tmp_path: Path) -> None:
        """Verify NetworkIcon works inside ArchitectureDiagram nodes."""
        clear()
        diag = ArchitectureDiagram(
            node_style=Styles.PrimaryFlat,
            node_text_style=Styles.Dark,
            edge_style=Styles.Primary,
            edge_text_style=Styles.Dark,
        )
        n1 = diag.add(Node("WAN", width=20, height=20, icon=NetworkIcon.CISCO_WAN_ROUTER), (20, 50))
        n2 = diag.add(Node("Core", width=20, height=20, icon=NetworkIcon.CISCO_CORE_SWITCH), (50, 50))
        n3 = diag.add(Node("FW", width=20, height=20, icon=NetworkIcon.CISCO_FIREWALL), (80, 50))
        diag.connect(n1, n2)
        diag.connect(n2, n3)
        diag.draw((5, 10))
        out = tmp_path / "test_arch_network.png"
        save(str(out))
        assert out.is_file()

    def test_network_vendor_icons(self, tmp_path: Path) -> None:
        """Verify official vendor and OSS network logos."""
        clear()
        network.cloudflare(xy=(15, 80), width=12, style=Style())
        network.nginx(xy=(35, 80), width=12, style=Style())
        network.traefik(xy=(55, 80), width=12, style=Style())
        network.wireguard(xy=(75, 80), width=12, style=Style())

        network.fortinet(xy=(15, 60), width=12, style=Style())
        network.palo_alto(xy=(35, 60), width=12, style=Style())
        network.f5(xy=(55, 60), width=12, style=Style())
        network.cisco(xy=(75, 60), width=12, style=Style())

        network.tp_link(xy=(15, 40), width=12, style=Style())
        network.netgear(xy=(35, 40), width=12, style=Style())
        network.godaddy(xy=(55, 40), width=12, style=Style())
        network.lets_encrypt(xy=(75, 40), width=12, style=Style())

        out = tmp_path / "test_network_vendors.png"
        save(str(out))
        assert out.is_file()

    def test_nonexistent_network_icon_error(self) -> None:
        """Verify FileNotFoundError when requesting an invalid Network icon file."""
        with pytest.raises(FileNotFoundError):
            NETWORK_PROVIDER.get_icon_path("non_existent_cisco_icon_xyz")


class TestOriginalNetworkIcons:
    """Tests for Original Network (2D pastel) icon provider and architecture diagram enum."""

    def test_original_network_canonical_icons(self, tmp_path: Path) -> None:
        """Verify canonical 2D Original Network icons."""
        clear()
        original_network.router(xy=(15, 75), width=12, style=Style())
        original_network.wan_router(xy=(35, 75), width=12, style=Style())
        original_network.core_router(xy=(55, 75), width=12, style=Style())
        original_network.l2_switch(xy=(75, 75), width=12, style=Style())

        original_network.l3_switch(xy=(15, 50), width=12, style=Style())
        original_network.datacenter_switch(xy=(35, 50), width=12, style=Style())
        original_network.core_switch(xy=(55, 50), width=12, style=Style())
        original_network.firewall(xy=(75, 50), width=12, style=Style())

        original_network.wireless_ap(xy=(15, 25), width=12, style=Style())
        original_network.wan_cloud(xy=(35, 25), width=12, style=Style())
        original_network.ip_phone(xy=(55, 25), width=12, style=Style())
        original_network.client_pc(xy=(75, 25), width=12, style=Style())

        out = tmp_path / "test_original_network.png"
        save(str(out))
        assert out.is_file()

    def test_original_network_architecture_diagram_enum(self, tmp_path: Path) -> None:
        """Verify OriginalNetworkIcon works inside ArchitectureDiagram nodes."""
        clear()
        diag = ArchitectureDiagram(
            node_style=Styles.PrimaryFlat,
            node_text_style=Styles.Dark,
            edge_style=Styles.Primary,
            edge_text_style=Styles.Dark,
        )
        n1 = diag.add(Node("WAN", width=20, height=20, icon=OriginalNetworkIcon.WAN_ROUTER), (20, 50))
        n2 = diag.add(Node("Switch", width=20, height=20, icon=OriginalNetworkIcon.L3_SWITCH), (50, 50))
        n3 = diag.add(Node("FW", width=20, height=20, icon=OriginalNetworkIcon.FIREWALL), (80, 50))
        diag.connect(n1, n2)
        diag.connect(n2, n3)
        diag.draw((5, 10))
        out = tmp_path / "test_arch_original_network.png"
        save(str(out))
        assert out.is_file()

    def test_original_network_vendor_icons(self, tmp_path: Path) -> None:
        """Verify 2D pastel vendor and OSS network logos."""
        clear()
        original_network.cloudflare(xy=(15, 80), width=12, style=Style())
        original_network.nginx(xy=(35, 80), width=12, style=Style())
        original_network.wireguard(xy=(55, 80), width=12, style=Style())
        original_network.porkbun(xy=(75, 80), width=12, style=Style())

        original_network.fortinet(xy=(15, 50), width=12, style=Style())
        original_network.tp_link(xy=(35, 50), width=12, style=Style())
        original_network.godaddy(xy=(55, 50), width=12, style=Style())
        original_network.lets_encrypt(xy=(75, 50), width=12, style=Style())

        out = tmp_path / "test_original_network_vendors.png"
        save(str(out))
        assert out.is_file()

    def test_nonexistent_original_network_icon_error(self) -> None:
        """Verify FileNotFoundError when requesting an invalid Original Network icon file."""
        with pytest.raises(FileNotFoundError):
            ORIGINAL_NETWORK_PROVIDER.get_icon_path("non_existent_orig_network_icon_xyz")
