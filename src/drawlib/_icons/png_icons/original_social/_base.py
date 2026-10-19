# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Social Media, Messaging, Streaming, Tech Community & AdTech icon provider."""

from __future__ import annotations

from drawlib._icons.png_icons._base import PngIconProvider

ORIGINAL_SOCIAL_ALIASES: dict[str, str] = {
    "abematv": "abema",
    "ad_campaign": "ad_targeting",
    "adwords": "google_ads",
    "ambassador": "influencer",
    "article": "tech_blog",
    "attribution": "conversion_funnel",
    "audio_room": "podcast_mic",
    "auto_reply": "chatbot_account",
    "b_hatena": "hatena",
    "blog_post": "tech_blog",
    "broadcast_message": "push_campaign",
    "bsky": "bluesky",
    "creator": "influencer",
    "cvr": "conversion_funnel",
    "devto": "dev_to",
    "digital_ad": "ad_targeting",
    "fb": "facebook",
    "fb_messenger": "messenger",
    "feed": "timeline_feed",
    "follower_graph": "social_graph",
    "forum": "community_forum",
    "funnel": "conversion_funnel",
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
    "kol": "influencer",
    "likes": "user_engagement",
    "live": "live_streaming",
    "live_broadcast": "live_streaming",
    "lycorp": "yahoo_japan",
    "meetup": "community_forum",
    "moderation": "content_moderation",
    "network_graph": "social_graph",
    "news_feed": "timeline_feed",
    "nico": "nicovideo",
    "niconico": "nicovideo",
    "oauth_login": "social_login",
    "official_account": "chatbot_account",
    "podcast": "podcast_mic",
    "podcasts": "apple_podcasts",
    "push_notification": "push_campaign",
    "qa_board": "community_forum",
    "reactions": "user_engagement",
    "reels": "short_video",
    "repost": "viral_share",
    "retargeting": "ad_targeting",
    "retweet": "viral_share",
    "review_rating": "user_engagement",
    "share": "viral_share",
    "shorts": "short_video",
    "snap": "snapchat",
    "social_bot": "chatbot_account",
    "spam_filter": "content_moderation",
    "speakerdeck": "speaker_deck",
    "sso_social": "social_login",
    "stackoverflow": "stack_overflow",
    "tech_writing": "tech_blog",
    "tg": "telegram",
    "timeline": "timeline_feed",
    "trust_and_safety": "content_moderation",
    "twitter": "x",
    "ugc": "user_engagement",
    "vertical_video": "short_video",
    "viral": "viral_share",
    "voice_chat": "podcast_mic",
    "wa": "whatsapp",
    "webinar": "live_streaming",
    "weixin": "wechat",
    "yahoo_jp": "yahoo_japan",
    "ycombinator": "hacker_news",
    "yt": "youtube",
}

ORIGINAL_SOCIAL_PROVIDER = PngIconProvider(
    name="original_social",
    package_name="icon_original_social",
    asset_subdir="icons/original_social",
    aliases=ORIGINAL_SOCIAL_ALIASES,
)

_write = ORIGINAL_SOCIAL_PROVIDER.write
