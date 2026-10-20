# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for Social, Media, Community, and MarTech icons."""

from pathlib import Path

from drawlib._icons.png_icons.social._base import SOCIAL_PROVIDER
from drawlib.canvas import clear, save
from drawlib.diagrams.architecture import ArchitectureDiagram, Node, SocialIcon
from drawlib.icons import social
from drawlib.styles import Styles
from drawlib.types import Style

ALL_50_SOCIAL_ICONS = [
    "abema",
    "amplitude",
    "apple_podcasts",
    "appsflyer",
    "bilibili",
    "bluesky",
    "connpass",
    "dev_to",
    "discord",
    "facebook",
    "google_ads",
    "google_analytics",
    "google_tag_manager",
    "hacker_news",
    "hashnode",
    "hatena",
    "instagram",
    "kakao",
    "line",
    "linkedin",
    "mastodon",
    "medium",
    "messenger",
    "meta_ads",
    "mixpanel",
    "nicovideo",
    "note",
    "pinterest",
    "qiita",
    "reddit",
    "signal",
    "snapchat",
    "soundcloud",
    "speaker_deck",
    "spotify",
    "stack_overflow",
    "substack",
    "telegram",
    "threads",
    "tiktok",
    "tver",
    "twitch",
    "viber",
    "vimeo",
    "wechat",
    "whatsapp",
    "x",
    "yahoo_japan",
    "youtube",
    "zenn",
]


class TestSocialIcons:
    """Tests for official Social icon provider and diagram enum."""

    def test_all_social_icons(self, tmp_path: Path) -> None:
        """Verify all 50 social, messaging, streaming, community, and MarTech icons exist and render cleanly."""
        clear()
        assert len(ALL_50_SOCIAL_ICONS) == 50
        for idx, name in enumerate(ALL_50_SOCIAL_ICONS):
            assert hasattr(social, name), f"Missing social icon function: {name}"
            assert hasattr(SocialIcon, name.upper()), f"Missing SocialIcon enum: {name.upper()}"
            col = idx % 10
            row = idx // 10
            fn = getattr(social, name)
            fn(xy=(6 + col * 9.5, 85 - row * 17), width=7, style=Style(), variant="default")

        out = tmp_path / "test_social_all.png"
        save(str(out))
        assert out.is_file()

    def test_social_architecture_enum(self, tmp_path: Path) -> None:
        """Verify SocialIcon works inside ArchitectureDiagram nodes."""
        clear()
        diag = ArchitectureDiagram(
            node_style=Styles.PrimaryFlat,
            node_text_style=Styles.Dark,
            edge_style=Styles.Primary,
            edge_text_style=Styles.Dark,
        )
        n1 = diag.add(Node("X", width=20, height=20, icon=SocialIcon.X), (20, 50))
        n2 = diag.add(Node("LINE", width=20, height=20, icon=SocialIcon.LINE), (50, 50))
        n3 = diag.add(Node("GA4", width=20, height=20, icon=SocialIcon.GOOGLE_ANALYTICS), (80, 50))
        diag.connect(n1, n2)
        diag.connect(n2, n3)
        diag.draw((5, 10))
        out = tmp_path / "test_arch_social.png"
        save(str(out))
        assert out.is_file()

    def test_social_provider_metadata(self) -> None:
        """Verify provider package name."""
        assert SOCIAL_PROVIDER.name == "social"
        assert SOCIAL_PROVIDER.package_name == "icon_social"
