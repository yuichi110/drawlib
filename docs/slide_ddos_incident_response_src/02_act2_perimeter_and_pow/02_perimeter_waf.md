::: block (80, 40) (1760, 70)
# Perimeter Defense: GCLB & Cloud Armor WAF
:::

::: block (80, 140) (680, 810)
## Edge Shield Architecture

- **Private Origin Isolation**
  Locked down `run.app` direct URL (`ingress = internal-and-cloud-load-balancing`).
- **Global Anycast Ingress**
  Placed **Google Cloud Load Balancing (GCLB)** with **Serverless NEG** in front of Cloud Run.
- **Edge L7 WAF Policies**
  Attached **Cloud Armor** for edge IP rate limiting and geo-filtering before container invocation.
:::

::: block (800, 140) (1040, 810)
```drawlib
from drawlib.canvas import setup
from drawlib.diagrams.architecture import ArchitectureDiagram, GcpIcon, Node, NodeGroup, PhosphorIcon
from drawlib.shapes import rectangle
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=115, height=90)

rectangle((57.5, 45.0), width=111, height=86, style=Styles.Neutral.patch(shape_r=2.5))
text((57.5, 83.5), "Hardened Perimeter: GCLB + Cloud Armor -> Serverless NEG -> Cloud Run", style=Styles.BlackBold.patch(text_size=11.5))

d = ArchitectureDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=9.5),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=9.5),
    node_card_style=Styles.White,
)

# External Actors
bots = d.add(
    Node((22, 17), "Botnet Flood\nDirect Bypass", icon=PhosphorIcon.SKULL, icon_size=6.5,
         style=Styles.Accent, card_style=Styles.SecondaryNeutral),
    xy=(15.0, 22.0),
)
traffic = d.add(
    Node((22, 17), "Public Traffic\nHTTPS :443", icon=PhosphorIcon.GLOBE, icon_size=6.5,
         card_style=Styles.PrimaryNeutral),
    xy=(15.0, 58.0),
)

# Google Cloud Perimeter Group
gcp_edge = d.add(
    NodeGroup(title="Google Cloud Global Edge & VPC Perimeter", padding=4.5,
              style=Styles.PrimaryNeutral.patch(shape_r=2.0),
              text_style=Styles.PrimaryBold.patch(text_size=9.5, halign="left")),
    xy=(36.0, 8.0),
)

armor = gcp_edge.add(
    Node((24, 18), "GCLB + Cloud Armor\nWAF & Rate Limit", icon=GcpIcon.CLOUD_ARMOR, icon_size=7.5,
         style=Styles.White, text_style=Styles.WhiteBold.patch(text_size=9.5), card_style=Styles.PrimaryFlat),
    xy=(16.0, 50.0),
)
neg = gcp_edge.add(
    Node((22, 16), "Serverless NEG\nInternal Bridge", icon=GcpIcon.CLOUD_LOAD_BALANCING, icon_size=7.0,
         card_style=Styles.White),
    xy=(45.0, 50.0),
)
crun = gcp_edge.add(
    Node((24, 18), "Cloud Run Origin\nInternal-Only Ingress", icon=GcpIcon.CLOUD_RUN, icon_size=7.5,
         card_style=Styles.White),
    xy=(45.0, 16.0),
)
blocked_url = gcp_edge.add(
    Node((24, 16), "Direct *.run.app\n403 Blocked", icon=PhosphorIcon.LOCK_KEY, icon_size=6.5,
         style=Styles.White, text_style=Styles.WhiteBold.patch(text_size=9.5), card_style=Styles.AccentFlat),
    xy=(16.0, 16.0),
)

d.connect(traffic, armor, label="Anycast", padding=1.0)
d.connect(armor, neg, label="Pass", padding=1.0)
d.connect(neg, crun, label="Private", padding=1.0)
d.connect(bots, blocked_url, label="Denied", style=Styles.AccentBold, text_style=Styles.AccentBold.patch(text_size=9.5), padding=1.0)

d.draw(xy=(2.0, 2.0))
```
:::

::: block (1720, 995) (140, 30)
```drawlib
import utils
utils.draw_page_number()
```
:::

::: note
To stop malicious traffic before it could invoke Cloud Run containers, we re-architected the network perimeter:
1. **Locking Down Direct Origin Access**: If an attacker knows or discovers the underlying `*.run.app` URL, they can bypass an external proxy entirely. We reconfigured Cloud Run ingress settings to `internal-and-cloud-load-balancing`, ensuring any direct request to `*.run.app` is rejected at Google's fabric edge.
2. **Global External Application Load Balancer (GCLB)**: We provisioned an Anycast IP frontend backed by a **Serverless Network Endpoint Group (NEG)** pointing to our Cloud Run service.
3. **Cloud Armor WAF Attachment**: With GCLB in place, we attached a **Google Cloud Armor** security policy to evaluate IP rate limits and geographic rules at Google's edge POPs before forwarding requests to Cloud Run.
:::
