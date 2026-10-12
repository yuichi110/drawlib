::: block xy=(110, 220) width=860 height=640
# Surviving a 300M+ Req/Day DDoS & EDoS Attack

### A Real-World Serverless Postmortem on Google Cloud Run & Edge WAF Architecture

How an AI-orchestrated botnet pushed a 10-year hobby speech synthesis service from $10/month to a $6,750/month WAF billing crisis — and how 5-layer edge defense defeated it for $20/month flat.

**Incident Postmortem & Cloud Security Case Study** · **2026**
:::

::: block xy=(980, 140) width=840 height=780
```drawlib
from drawlib.canvas import setup
from drawlib.diagrams.architecture import ArchitectureDiagram, GcpIcon, Node, NodeGroup, PhosphorIcon
from drawlib.smartarts import Panel
from drawlib.styles import Styles
from drawlib.text import text

setup(width=105, height=98)

# Outer framing panel
panel = Panel(
    "End-to-End Defense Evolution Overview",
    style=Styles.Neutral,
    header_style=Styles.PrimaryBold,
    text_style=Styles.BlackBold.patch(text_size=16.0),
    header_variant="underline",
    header_height=9.0,
    header_align="center",
)
panel.draw(xy=(2.0, 2.0), width=101.0, height=94.0)
text((52.5, 83.2), "Direct Origin Exposure -> WAF Billing Shock -> Flat-Rate Edge Victory", style=Styles.Dark.patch(text_size=12.8))

d = ArchitectureDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=13.5),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=12.5),
)

# Attackers & Legitimate Users on Left
botnet = d.add(
    Node("AI Botnet\n300M+ Req/Day", width=16, height=16, icon=PhosphorIcon.SKULL, icon_size=8.0,
         style=Styles.Danger),
    xy=(14.0, 56.0),
)
users = d.add(
    Node("Real Users\nBrowser + PoW", width=16, height=16, icon=PhosphorIcon.USERS, icon_size=8.0,
         style=Styles.Primary),
    xy=(14.0, 21.0),
)

# Edge Shield Group in Middle
edge_group = d.add(
    NodeGroup(title="Flat-Rate Edge ($20/mo)", padding=5.5,
              style=Styles.PrimaryNeutral.patch(shape_r=2.0),
              text_style=Styles.PrimaryBold.patch(text_size=13.5, halign="left")),
    xy=(36.0, 8.0),
)
waf = edge_group.add(
    Node("5-Layer WAF\nASN / TLS / Rate", width=17, height=16, icon=PhosphorIcon.SHIELD_CHECK, icon_size=8.5,
         style=Styles.Primary),
    xy=(15.5, 48.0),
)
drop = edge_group.add(
    Node("100% Bot Drop\n$0 Overages", width=17, height=15, icon=PhosphorIcon.PROHIBIT, icon_size=7.5,
         style=Styles.Danger),
    xy=(15.5, 14.5),
)

# Protected Origin on Right
origin = d.add(
    Node("Cloud Run\nTTS Origin ($10/mo)", width=17, height=17, icon=GcpIcon.CLOUD_RUN, icon_size=8.5),
    xy=(89.0, 56.0),
)

d.connect(botnet, waf, label="Flood", style=Styles.AccentBold, text_style=Styles.AccentBold.patch(text_size=12.5), padding=0.5)
d.connect(users, waf, label="HTTPS", routing="direct", style=Styles.PrimaryBold, text_style=Styles.PrimaryBold.patch(text_size=12.5), padding=0.5)
d.connect(waf, drop, label="Drop", style=Styles.AccentBold, text_style=Styles.AccentBold.patch(text_size=12.5), padding=0.5)
d.connect(waf, origin, label="Clean", style=Styles.PrimaryBold, text_style=Styles.PrimaryBold.patch(text_size=12.5), padding=0.5)

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
