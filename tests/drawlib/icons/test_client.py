# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for Client icons."""

from pathlib import Path

from drawlib._icons.png_icons.client._base import CLIENT_PROVIDER
from drawlib.canvas import clear, save
from drawlib.diagrams.architecture import ArchitectureDiagram, ClientIcon, Node
from drawlib.icons import client
from drawlib.styles import Styles
from drawlib.types import Style


class TestClientIcons:
    """Tests for official Client icon provider and diagram enum."""

    def test_client_all_icons(self, tmp_path: Path) -> None:
        """Verify all 60 official client icons render cleanly."""
        clear()
        names = [
            "chrome",
            "safari",
            "edge",
            "firefox",
            "brave",
            "opera",
            "vivaldi",
            "arc",
            "tor_browser",
            "chromium",
            "windows",
            "macos",
            "ios",
            "android",
            "chromeos",
            "linux",
            "ubuntu",
            "app_store",
            "play_store",
            "microsoft_store",
            "apple",
            "microsoft",
            "samsung",
            "sony",
            "panasonic",
            "dell",
            "hp",
            "lenovo",
            "asus",
            "acer",
            "kindle",
            "amazon_fire",
            "fire_tv",
            "alexa",
            "fitbit",
            "switchbot",
            "netflix",
            "youtube",
            "nintendo",
            "playstation",
            "xbox",
            "toyota",
            "tesla",
            "bmw",
            "caterpillar",
            "komatsu",
            "john_deere",
            "fanuc",
            "siemens",
            "abb",
            "logitech",
            "canon",
            "epson",
            "brother",
            "ricoh",
            "zebra",
            "honeywell",
            "meta",
            "bluetooth",
            "usb",
        ]
        for idx, name in enumerate(names):
            col = idx % 10
            row = idx // 10
            fn = getattr(client, name)
            fn(xy=(8 + col * 9.3, 85 - row * 14), width=7, style=Style(), variant="default")

        out = tmp_path / "test_client_all.png"
        save(str(out))
        assert out.is_file()

    def test_client_architecture_enum(self, tmp_path: Path) -> None:
        """Verify ClientIcon works inside ArchitectureDiagram nodes."""
        clear()
        diag = ArchitectureDiagram(
            node_style=Styles.PrimaryFlat,
            node_text_style=Styles.Dark,
            edge_style=Styles.Primary,
            edge_text_style=Styles.Dark,
        )
        n1 = diag.add(Node("Chrome", width=20, height=20, icon=ClientIcon.CHROME), (20, 50))
        n2 = diag.add(Node("Alexa", width=20, height=20, icon=ClientIcon.ALEXA), (50, 50))
        n3 = diag.add(Node("Tesla", width=20, height=20, icon=ClientIcon.TESLA), (80, 50))
        diag.connect(n1, n2)
        diag.connect(n2, n3)
        diag.draw((5, 10))
        out = tmp_path / "test_arch_client.png"
        save(str(out))
        assert out.is_file()

    def test_client_provider_metadata(self) -> None:
        """Verify provider package name."""
        assert CLIENT_PROVIDER.name == "client"
        assert CLIENT_PROVIDER.package_name == "icon_client"
