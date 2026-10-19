# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for Original Social icons."""

from pathlib import Path

from drawlib._icons.png_icons.original_social._base import (
    ORIGINAL_SOCIAL_PROVIDER,
)
from drawlib.canvas import clear, save
from drawlib.diagrams.architecture import ArchitectureDiagram, Node, OriginalSocialIcon
from drawlib.icons import original_social
from drawlib.styles import Styles
from drawlib.types import Style

ALL_16_CONCEPT_ICONS = [
    "ad_targeting",
    "chatbot_account",
    "community_forum",
    "content_moderation",
    "conversion_funnel",
    "influencer",
    "live_streaming",
    "podcast_mic",
    "push_campaign",
    "short_video",
    "social_graph",
    "social_login",
    "tech_blog",
    "timeline_feed",
    "user_engagement",
    "viral_share",
]

ALL_50_BRAND_ICONS = [
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


class TestOriginalSocialIcons:
    """Tests for `drawlib.icons.original_social` and `OriginalSocialIcon`."""

    def test_original_social_all_66_icons(self, tmp_path: Path) -> None:
        """Verify all 66 original social concepts and brand icons exist and render."""
        clear()
        all_66 = ALL_16_CONCEPT_ICONS + ALL_50_BRAND_ICONS
        assert len(all_66) == 66
        for idx, name in enumerate(all_66):
            assert hasattr(original_social, name), f"Missing canonical icon: {name}"
            assert hasattr(OriginalSocialIcon, name.upper()), f"Missing enum: {name.upper()}"
            col = idx % 11
            row = idx // 11
            fn = getattr(original_social, name)
            fn(xy=(6 + col * 8.6, 88 - row * 14), width=6.5, style=Style(), variant="default")

        out = tmp_path / "test_original_social_all.png"
        save(str(out))
        assert out.is_file()

    def test_original_social_aliases(self, tmp_path: Path) -> None:
        """Verify shorthand aliases resolve to canonical original_social icons."""
        clear()
        original_social.sso_social(xy=(12, 70), width=8, style=Style())
        original_social.feed(xy=(24, 70), width=8, style=Style())
        original_social.creator(xy=(36, 70), width=8, style=Style())
        original_social.reels(xy=(48, 70), width=8, style=Style())
        original_social.funnel(xy=(60, 70), width=8, style=Style())
        original_social.official_account(xy=(72, 70), width=8, style=Style())
        original_social.twitter(xy=(12, 45), width=8, style=Style())
        original_social.ig(xy=(24, 45), width=8, style=Style())
        original_social.yt(xy=(36, 45), width=8, style=Style())
        original_social.ga4(xy=(48, 45), width=8, style=Style())

        out = tmp_path / "test_original_social_aliases.png"
        save(str(out))
        assert out.is_file()

    def test_original_social_architecture_enum(self, tmp_path: Path) -> None:
        """Verify OriginalSocialIcon works inside ArchitectureDiagram nodes."""
        clear()
        diag = ArchitectureDiagram(
            node_style=Styles.PrimaryFlat,
            node_text_style=Styles.Dark,
            edge_style=Styles.Primary,
            edge_text_style=Styles.Dark,
        )
        n1 = diag.add(
            Node("Influencer", width=20, height=20, icon=OriginalSocialIcon.INFLUENCER),
            (20, 50),
        )
        n2 = diag.add(
            Node("Viral Share", width=20, height=20, icon=OriginalSocialIcon.VIRAL_SHARE),
            (50, 50),
        )
        n3 = diag.add(
            Node("Conversion", width=20, height=20, icon=OriginalSocialIcon.CONVERSION_FUNNEL),
            (80, 50),
        )
        diag.connect(n1, n2)
        diag.connect(n2, n3)
        diag.draw((5, 10))
        out = tmp_path / "test_arch_original_social.png"
        save(str(out))
        assert out.is_file()

    def test_original_social_provider_metadata(self) -> None:
        """Verify provider package name and aliases mapping."""
        assert ORIGINAL_SOCIAL_PROVIDER.name == "original_social"
        assert ORIGINAL_SOCIAL_PROVIDER.package_name == "icon_original_social"
        assert ORIGINAL_SOCIAL_PROVIDER.asset_subdir == "icons/original_social"
        assert ORIGINAL_SOCIAL_PROVIDER.aliases["creator"] == "influencer"
        assert ORIGINAL_SOCIAL_PROVIDER.aliases["feed"] == "timeline_feed"
        assert ORIGINAL_SOCIAL_PROVIDER.aliases["funnel"] == "conversion_funnel"
        assert ORIGINAL_SOCIAL_PROVIDER.aliases["ga4"] == "google_analytics"
        assert ORIGINAL_SOCIAL_PROVIDER.aliases["official_account"] == "chatbot_account"
        assert ORIGINAL_SOCIAL_PROVIDER.aliases["reels"] == "short_video"
        assert ORIGINAL_SOCIAL_PROVIDER.aliases["sso_social"] == "social_login"
        assert ORIGINAL_SOCIAL_PROVIDER.aliases["twitter"] == "x"
