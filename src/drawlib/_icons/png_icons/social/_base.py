# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Social Media, Messaging, Streaming, Tech Community & AdTech icon provider."""

from __future__ import annotations

from drawlib._icons.png_icons._base import PngIconProvider

SOCIAL_ALIASES: dict[str, str] = {
    "abematv": "abema",
    "adwords": "google_ads",
    "b_hatena": "hatena",
    "bsky": "bluesky",
    "devto": "dev_to",
    "fb": "facebook",
    "fb_messenger": "messenger",
    "ga": "google_analytics",
    "ga4": "google_analytics",
    "gtm": "google_tag_manager",
    "hackernews": "hacker_news",
    "hatena_blog": "hatena",
    "hatena_bookmark": "hatena",
    "hn": "hacker_news",
    "ig": "instagram",
    "insta": "instagram",
    "kakaotalk": "kakao",
    "lycorp": "yahoo_japan",
    "nico": "nicovideo",
    "niconico": "nicovideo",
    "podcasts": "apple_podcasts",
    "snap": "snapchat",
    "speakerdeck": "speaker_deck",
    "stackoverflow": "stack_overflow",
    "tg": "telegram",
    "twitter": "x",
    "wa": "whatsapp",
    "weixin": "wechat",
    "yahoo_jp": "yahoo_japan",
    "ycombinator": "hacker_news",
    "yt": "youtube",
}

SOCIAL_PROVIDER = PngIconProvider(
    name="social",
    package_name="icon_social",
    asset_subdir="icons/social",
    aliases=SOCIAL_ALIASES,
)

_write = SOCIAL_PROVIDER.write
