# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for Original Client icons."""

from pathlib import Path

from drawlib._icons.png_icons.original_client._base import ORIGINAL_CLIENT_PROVIDER
from drawlib.canvas import clear, save
from drawlib.diagrams.architecture import ArchitectureDiagram, Node, OriginalClientIcon
from drawlib.icons import original_client
from drawlib.styles import Styles
from drawlib.types import Style


class TestOriginalClientIcons:
    """Tests for Original Client concept and pastel brand icon provider."""

    def test_original_client_all_icons(self, tmp_path: Path) -> None:
        """Verify all 92 original_client icons render cleanly."""
        clear()
        names = [
            # 32 concept icons
            "desktop_pc",
            "laptop",
            "smartphone",
            "tablet",
            "ereader",
            "smartwatch",
            "smart_ring",
            "smart_glasses",
            "vr_headset",
            "external_monitor",
            "smart_tv",
            "smart_speaker",
            "projector",
            "game_console",
            "kiosk_terminal",
            "pos_terminal",
            "printer",
            "barcode_scanner",
            "ip_phone",
            "webcam",
            "headset",
            "keyboard_mouse",
            "usb_drive",
            "smart_card",
            "qr_code",
            "nfc_tag",
            "gps_tracker",
            "drone",
            "connected_car",
            "heavy_machinery",
            "industrial_robot",
            "plc_controller",
            # 60 pastel brand icons
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
        assert len(names) == 92
        for idx, name in enumerate(names):
            col = idx % 10
            row = idx // 10
            fn = getattr(original_client, name)
            fn(xy=(8 + col * 9.3, 91 - row * 9.0), width=6.5, style=Style(), variant="default")

        out = tmp_path / "test_original_client_all.png"
        save(str(out))
        assert out.is_file()

    def test_original_client_aliases(self, tmp_path: Path) -> None:
        """Verify shorthand aliases resolve to canonical original_client icons."""
        clear()
        original_client.pc(xy=(10, 70), width=7, style=Style())
        original_client.macbook(xy=(20, 70), width=7, style=Style())
        original_client.ipad(xy=(30, 70), width=7, style=Style())
        original_client.excavator(xy=(40, 70), width=7, style=Style())
        original_client.robot_arm(xy=(50, 70), width=7, style=Style())
        original_client.google_chrome(xy=(60, 70), width=7, style=Style())
        original_client.cat(xy=(70, 70), width=7, style=Style())
        original_client.smart_glass(xy=(80, 70), width=7, style=Style())
        original_client.oura_ring(xy=(90, 70), width=7, style=Style())

        out = tmp_path / "test_original_client_aliases.png"
        save(str(out))
        assert out.is_file()

    def test_original_client_architecture_enum(self, tmp_path: Path) -> None:
        """Verify OriginalClientIcon works inside ArchitectureDiagram nodes."""
        clear()
        diag = ArchitectureDiagram(
            node_style=Styles.PrimaryFlat,
            node_text_style=Styles.Dark,
            edge_style=Styles.Primary,
            edge_text_style=Styles.Dark,
        )
        n1 = diag.add(Node("Laptop", width=20, height=20, icon=OriginalClientIcon.LAPTOP), (20, 50))
        n2 = diag.add(Node("Chrome", width=20, height=20, icon=OriginalClientIcon.CHROME), (50, 50))
        n3 = diag.add(Node("Robot", width=20, height=20, icon=OriginalClientIcon.INDUSTRIAL_ROBOT), (80, 50))
        diag.connect(n1, n2)
        diag.connect(n2, n3)
        diag.draw((5, 10))
        out = tmp_path / "test_arch_original_client.png"
        save(str(out))
        assert out.is_file()

    def test_original_client_provider_metadata(self) -> None:
        """Verify provider package name and aliases mapping."""
        assert ORIGINAL_CLIENT_PROVIDER.name == "original_client"
        assert ORIGINAL_CLIENT_PROVIDER.package_name == "icon_original_client"
        assert ORIGINAL_CLIENT_PROVIDER.aliases["pc"] == "desktop_pc"
        assert ORIGINAL_CLIENT_PROVIDER.aliases["excavator"] == "heavy_machinery"
        assert ORIGINAL_CLIENT_PROVIDER.aliases["google_chrome"] == "chrome"
