::: block (110, 220) (860, 640)
# Surviving a 300M+ Req/Day DDoS & EDoS Attack

### A Real-World Serverless Postmortem on Google Cloud Run & Edge WAF Architecture

How an AI-orchestrated botnet pushed a 10-year hobby speech synthesis service from $10/month to a $6,750/month WAF billing crisis — and how 5-layer edge defense defeated it for $20/month flat.

**Incident Postmortem & Cloud Security Case Study** · **2026**
:::

::: block (980, 140) (840, 780)
```drawlib
from drawlib.canvas import setup
from drawlib.diagrams.architecture import ArchitectureDiagram, GcpIcon, Node, NodeGroup, PhosphorIcon
from drawlib.shapes import rectangle
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=105, height=98)

# Outer subtle framing card
rectangle((52.5, 49.0), width=101, height=94, style=Styles.Neutral.patch(shape_r=3.0))
text((52.5, 90.0), "End-to-End Defense Evolution Overview", style=Styles.BlackBold.patch(text_size=15.0))
text((52.5, 84.0), "Direct Origin Exposure -> WAF Billing Shock -> Flat-Rate Edge Victory", style=Styles.Muted.patch(text_size=12.0))

d = ArchitectureDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=12.5),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=12.0),
    node_card_style=Styles.White,
)

# Attackers & Legitimate Users on Left
botnet = d.add(
    Node((24, 19), "AI Botnet\n300M+ Req/Day", icon=PhosphorIcon.SKULL, icon_size=7.0,
         style=Styles.Accent, card_style=Styles.SecondaryNeutral),
    xy=(15.0, 56.0),
)
users = d.add(
    Node((24, 19), "Real Users\nBrowser + PoW", icon=PhosphorIcon.USERS, icon_size=7.0,
         style=Styles.Primary, card_style=Styles.PrimaryNeutral),
    xy=(15.0, 22.0),
)

# Edge Shield Group in Middle
edge_group = d.add(
    NodeGroup(title="Flat-Rate Edge ($20/mo)", padding=4.0,
              style=Styles.PrimaryNeutral.patch(shape_r=2.0),
              text_style=Styles.PrimaryBold.patch(text_size=12.5, halign="left")),
    xy=(36.0, 9.0),
)
waf = edge_group.add(
    Node((24, 19), "5-Layer WAF\nASN / TLS / Rate", icon=PhosphorIcon.SHIELD_CHECK, icon_size=7.5,
         style=Styles.White, text_style=Styles.WhiteBold.patch(text_size=12.5), card_style=Styles.PrimaryFlat),
    xy=(15.5, 47.0),
)
drop = edge_group.add(
    Node((24, 15), "100% Bot Drop\n$0 Overages", icon=PhosphorIcon.PROHIBIT, icon_size=6.0,
         style=Styles.White, text_style=Styles.WhiteBold.patch(text_size=12.5), card_style=Styles.AccentFlat),
    xy=(15.5, 16.0),
)

# Protected Origin on Right
origin = d.add(
    Node((23, 21), "Cloud Run\nTTS Origin\n($10/mo)", icon=GcpIcon.CLOUD_RUN, icon_size=7.5,
         card_style=Styles.Neutral),
    xy=(88.5, 47.0),
)

d.connect(botnet, waf, label="Flood", style=Styles.AccentBold, text_style=Styles.AccentBold.patch(text_size=12.0), padding=1.0)
d.connect(users, waf, label="HTTPS", style=Styles.PrimaryBold, text_style=Styles.PrimaryBold.patch(text_size=12.0), padding=1.0)
d.connect(waf, drop, label="Drop", style=Styles.AccentBold, text_style=Styles.AccentBold.patch(text_size=12.0), padding=1.0)
d.connect(waf, origin, label="Clean", style=Styles.PrimaryBold, text_style=Styles.PrimaryBold.patch(text_size=12.0), padding=1.0)

d.draw(xy=(2.0, 3.0))
```
:::

::: note
Welcome to this postmortem on surviving a 300-million-request-per-day DDoS and Economic Denial of Sustainability (EDoS) attack on Google Cloud Run.

In this presentation, we walk through a real-world multi-week incident against a Japanese speech synthesis web service that had operated peacefully for 10 years at $10/month:
- **Act 1 (The Incident Onset)**: How migrating from a fixed-capacity VPS to serverless auto-scaling on Cloud Run turned a CPU-bound synthesis API into an uncapped financial liability.
- **Act 2 (Perimeter WAF & Proof-of-Work)**: Deploying Google Cloud Load Balancing and Cloud Armor, battling rapid proxy geo-hopping, and building a custom SHA-256 Proof-of-Work challenge in Web Workers.
- **Act 3 (The EDoS Pivot & WAF Pricing Trap)**: How the attacker pivoted to a 300M req/day volumetric flood against lightweight endpoints, triggering a $225/day ($6,750/month) Cloud Armor evaluation fee trap even while blocking 99.9% of requests.
- **Act 4 (Multi-Layered Edge Victory)**: Migrating under fire to flat-rate Cloudflare Pro ($20/month) and combining 5 orthogonal signals—ASN blocks, User-Agent hygiene, HTTP/1.1 protocol fingerprinting, sub-threshold rate limiting, and SHA-256 PoW—to achieve 100% availability at zero overage cost.
:::
