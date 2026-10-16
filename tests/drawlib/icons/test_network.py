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
from drawlib.canvas import clear, save
from drawlib.diagrams.architecture import ArchitectureDiagram, NetworkIcon, Node
from drawlib.icons import network
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

    def test_network_cisco_aliases(self, tmp_path: Path) -> None:
        """Verify Cisco shorthand aliases."""
        clear()
        network.cisco_isr_router(xy=(20, 60), width=12, style=Style())
        network.cisco_access_switch(xy=(40, 60), width=12, style=Style())
        network.cisco_multilayer_switch(xy=(60, 60), width=12, style=Style())
        network.cisco_asa(xy=(80, 60), width=12, style=Style())
        network.cisco_ap(xy=(20, 30), width=12, style=Style(), variant="modern")
        network.cisco_wlc(xy=(40, 30), width=12, style=Style())
        network.cisco_ucs_server(xy=(60, 30), width=12, style=Style())
        network.cisco_workstation(xy=(80, 30), width=12, style=Style(), variant="modern")
        out = tmp_path / "test_network_aliases.png"
        save(str(out))
        assert out.is_file()

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

    def test_nonexistent_network_icon_error(self) -> None:
        """Verify FileNotFoundError when requesting an invalid Network icon file."""
        with pytest.raises(FileNotFoundError):
            NETWORK_PROVIDER.get_icon_path("non_existent_cisco_icon_xyz")
