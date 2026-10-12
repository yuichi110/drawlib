::: block xy=(80, 40) width=1760 height=70
# Perimeter Defense: GCLB & Cloud Armor WAF
:::

::: block xy=(80, 140) width=680 height=810
## Edge Shield Architecture

- **Private Origin Isolation**
  Locked down `run.app` direct URL (`ingress = internal-and-cloud-load-balancing`).
- **Global Anycast Ingress**
  Placed **Google Cloud Load Balancing (GCLB)** with **Serverless NEG** in front of Cloud Run.
- **Edge L7 WAF Policies**
  Attached **Cloud Armor** for edge IP rate limiting and geo-filtering before container invocation.
:::

::: block xy=(800, 140) width=1040 height=810
```drawlib
from drawlib.canvas import setup
from drawlib.diagrams.architecture import ArchitectureDiagram, GcpIcon, Node, NodeGroup, PhosphorIcon
from drawlib.smartarts import Panel
from drawlib.styles import Styles

setup(width=115, height=90)

panel = Panel(
    "Hardened Perimeter: GCLB + Cloud Armor -> Cloud Run",
    style=Styles.Neutral,
    header_style=Styles.PrimaryBold,
    text_style=Styles.BlackBold.patch(text_size=15.5),
    header_variant="underline",
    header_height=9.0,
    header_align="center",
)
panel.draw(xy=(2.0, 2.0), width=111.0, height=86.0)

d = ArchitectureDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=13.5),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=12.5),
)

# External Actors
bots = d.add(
    Node("Botnet Flood\nDirect Bypass", width=16, height=16, icon=PhosphorIcon.SKULL, icon_size=8.0,
         style=Styles.Accent),
    xy=(14.5, 22.0),
)
traffic = d.add(
    Node("Public Traffic\nHTTPS :443", width=16, height=16, icon=PhosphorIcon.GLOBE, icon_size=8.0),
    xy=(14.5, 58.0),
)

# Google Cloud Perimeter Group
gcp_edge = d.add(
    NodeGroup(title="Google Cloud Edge & VPC Perimeter", padding=5.5,
              style=Styles.PrimaryNeutral.patch(shape_r=2.0),
              text_style=Styles.PrimaryBold.patch(text_size=13.5, halign="left")),
    xy=(36.5, 7.0),
)

armor = gcp_edge.add(
    Node("Cloud Armor\nWAF & Rate", width=16, height=16, icon=GcpIcon.CLOUD_ARMOR, icon_size=8.5),
    xy=(16.5, 51.0),
)
neg = gcp_edge.add(
    Node("Serverless NEG\nInternal Bridge", width=16, height=16, icon=GcpIcon.CLOUD_LOAD_BALANCING, icon_size=8.5),
    xy=(48.5, 51.0),
)
crun = gcp_edge.add(
    Node("Cloud Run\nPrivate Origin", width=16, height=16, icon=GcpIcon.CLOUD_RUN, icon_size=8.5),
    xy=(48.5, 16.0),
)
blocked_url = gcp_edge.add(
    Node("Direct run.app\n403 Blocked", width=16, height=16, icon=PhosphorIcon.LOCK_KEY, icon_size=8.0,
         style=Styles.Danger),
    xy=(16.5, 16.0),
)

d.connect(traffic, armor, label="Anycast", padding=0.5)
d.connect(armor, neg, label="Pass", padding=0.5)
d.connect(neg, crun, label="Private", padding=0.5)
d.connect(bots, blocked_url, label="Denied", style=Styles.AccentBold, text_style=Styles.AccentBold.patch(text_size=12.5), padding=0.5)

d.draw(xy=(2.0, 2.0))
```
:::

::: block xy=(1720, 995) width=140 height=30
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
