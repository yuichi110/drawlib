# Drawlib Social Icons Guidelines (`lib-icons-social`)

API specification and complete catalog for `drawlib.icons.social` (`SocialIcon`, **50** official social network, community chat, streaming media, developer publishing, and AdTech brand logos) and `drawlib.icons.original_social` (`OriginalSocialIcon`, **66** flat 2D pastel icons: **50** brand twins + **16** vendor-neutral social, content moderation, and growth funnel concept icons). See `lib-icons-overview` for cross-tier icon rules.

---

## 1. API Signature & Twin Module Structure

Every icon function is **Center-Anchored at `xy = (cx, cy)`** with a `1:1` square aspect ratio and requires `*, style: Style` as a mandatory keyword-only argument:

```python
from drawlib.diagrams.architecture import Node, OriginalSocialIcon, SocialIcon
from drawlib.icons import original_social, original_social_icon, social, social_icon
from drawlib.styles import Styles

# 1. Direct module function calls (center-anchored at (cx, cy); style is required)
social.youtube((30, 25), width=9.0, style=Styles.Primary)
original_social.youtube((55, 25), width=9.0, style=Styles.Primary)
original_social.conversion_funnel((80, 25), width=9.0, style=Styles.Primary)

# 2. Dynamic string/Enum dispatchers
social_icon((30, 10), width=9.0, name="discord", style=Styles.Primary)
original_social_icon((55, 10), width=9.0, name="content_moderation", style=Styles.Primary)

# 3. High-level ArchitectureDiagram Node integration via Enum
ch_node = Node("Discord Server", width=24, height=18, icon=SocialIcon.DISCORD, icon_size=7.5)
mod_node = Node("Trust & Safety", width=24, height=18, icon=OriginalSocialIcon.CONTENT_MODERATION, icon_size=7.5)
```

| Module | Diagram Enum | Canonical Count | Asset Archive | Visual Purpose |
| :--- | :--- | :---: | :--- | :--- |
| `drawlib.icons.social` | `SocialIcon` | **50** | `icon_social` | Official logos for social networks, messaging apps, video/audio streaming, dev communities, and AdTech. |
| `drawlib.icons.original_social` | `OriginalSocialIcon` | **66** (`50` + `16`) | `icon_original_social` | Flat 2D pastel twins for all 50 brands plus **16 vendor-neutral social graph, media & growth concepts**. |

---

## 2. Complete 50 Shared Brand Icons (`social.*` & `original_social.*`)

| Category | Count | Canonical Function Names (`social.*` & `original_social.*`) |
| :--- | :---: | :--- |
| **Social Networks & Microblogging** | 10 | `bluesky`, `facebook`, `instagram`, `linkedin`, `mastodon`, `pinterest`, `reddit`, `snapchat`, `threads`, `x` |
| **Messaging & Community Chat** | 9 | `discord`, `kakao`, `line`, `messenger`, `signal`, `telegram`, `viber`, `wechat`, `whatsapp` |
| **Video, Audio & Media Streaming** | 11 | `abema`, `apple_podcasts`, `bilibili`, `nicovideo`, `soundcloud`, `spotify`, `tiktok`, `tver`, `twitch`, `vimeo`, `youtube` |
| **Developer Communities & Publishing** | 13 | `connpass`, `dev_to`, `hacker_news`, `hashnode`, `hatena`, `medium`, `note`, `qiita`, `speaker_deck`, `stack_overflow`, `substack`, `yahoo_japan`, `zenn` |
| **AdTech, Attribution & Analytics** | 7 | `amplitude`, `appsflyer`, `google_ads`, `google_analytics`, `google_tag_manager`, `meta_ads`, `mixpanel` |

---

## 3. Complete 16 Vendor-Neutral Social & Media Concept Icons (`original_social.*` Only)

| Canonical Function (`original_social.*`) | `OriginalSocialIcon` Enum | Architectural Role |
| :--- | :--- | :--- |
| `ad_targeting` | `AD_TARGETING` | Audience segmentation and personalized ad delivery engine |
| `chatbot_account` | `CHATBOT_ACCOUNT` | Automated webhook bot or conversational community agent |
| `community_forum` | `COMMUNITY_FORUM` | User discussion board, Q&A portal, or support forum |
| `content_moderation` | `CONTENT_MODERATION` | Automated toxicity filtering, spam detection, and policy review |
| `conversion_funnel` | `CONVERSION_FUNNEL` | Multi-stage user acquisition, activation, and checkout funnel |
| `influencer` | `INFLUENCER` | Creator account, brand ambassador, or key opinion leader node |
| `live_streaming` | `LIVE_STREAMING` | Real-time RTMP/WebRTC video ingest and live broadcast pipeline |
| `podcast_mic` | `PODCAST_MIC` | Audio recording, RSS podcast syndication, or voice room |
| `push_campaign` | `PUSH_CAMPAIGN` | Outbound mobile/web push notification and re-engagement campaign |
| `short_video` | `SHORT_VIDEO` | Vertical short-form video transcoding and recommendation feed |
| `social_graph` | `SOCIAL_GRAPH` | Follower/friend relationship graph and connection service |
| `social_login` | `SOCIAL_LOGIN` | OAuth2 / OIDC social sign-in federation gateway |
| `tech_blog` | `TECH_BLOG` | Engineering blog, developer portal, or CMS article publisher |
| `timeline_feed` | `TIMELINE_FEED` | Personalized home timeline fan-out and ranking service |
| `user_engagement` | `USER_ENGAGEMENT` | Likes, reactions, comments, and retention telemetry tracker |
| `viral_share` | `VIRAL_SHARE` | Referral loop, social sharing card, and word-of-mouth virality |

```drawlib code=fold align=center file=icons_social_rules_arch.png caption="Social Ingestion, Safety Moderation & Attribution Pipeline Using SocialIcon and OriginalSocialIcon"
from drawlib.canvas import save, setup
from drawlib.diagrams.architecture import (
    ArchitectureDiagram,
    Node,
    NodeGroup,
    OriginalSocialIcon,
    SocialIcon,
)
from drawlib.styles import Styles

setup(width=136, height=58)

d = ArchitectureDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=10.0),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=10.0),
    node_card_style=Styles.Neutral,
)

dc = d.add(
    Node("Discord\nCommunity", width=24, height=18, icon=SocialIcon.DISCORD, icon_size=7.5, card_style=Styles.PrimaryNeutral),
    xy=(6, 18),
)
pipe = d.add(NodeGroup(title="Engagement & Attribution Platform", padding=4.5), xy=(42, 4))
mod = pipe.add(Node("Safety\nModeration", width=24, height=18, icon=OriginalSocialIcon.CONTENT_MODERATION, icon_size=7.5, card_style=Styles.SecondaryNeutral), xy=(14, 14))
ga = pipe.add(Node("Google\nAnalytics", width=24, height=18, icon=SocialIcon.GOOGLE_ANALYTICS, icon_size=7.5, card_style=Styles.PrimaryNeutral), xy=(54, 14))

d.connect(dc, mod, label="Webhook", padding=1.5)
d.connect(mod, ga, label="Events", padding=1.5)
d.draw(xy=(4, 4))
save()
```
