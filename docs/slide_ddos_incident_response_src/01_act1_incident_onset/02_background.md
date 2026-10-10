::: block (80, 40) (1760, 70)
# Background: A 10-Year Hobby Service Enters the Cloud
:::

::: block (80, 140) (680, 810)
## Architecture Evolution

- **10 Years of Peace (2015–2025)**
  Japanese TTS web service running at **$10/mo** on a single VPS.
- **Serverless Migration (Mid-2025)**
  Containerized onto **Google Cloud Run** for zero-ops maintenance.
- **Hidden Vulnerability**
  Direct public URL (`run.app`) with **no CDN or Edge WAF** and uncapped pay-per-use scaling.
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
text((57.5, 83.0), "Legacy Fixed-Cost VPS vs. Direct Public Cloud Run", style=Styles.BlackBold.patch(text_size=15.0))

d = ArchitectureDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=12.5),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=12.0),
    node_card_style=Styles.White,
)

# Top Era: 2015-2025 VPS
era1 = d.add(
    NodeGroup(title="2015–2025: Legacy Single VPS ($10/mo Cap)", padding=4.0,
              style=Styles.PrimaryNeutral.patch(shape_r=2.0),
              text_style=Styles.PrimaryBold.patch(text_size=12.5, halign="left")),
    xy=(7.0, 46.0),
)
u1 = era1.add(Node((24, 17), "Web Users\nLow Volume", icon=PhosphorIcon.USERS, icon_size=6.5), xy=(14.5, 13.5))
vps = era1.add(Node((28, 17), "Single Linux VPS\n$10/mo Hard Cap", icon=PhosphorIcon.HARD_DRIVES, icon_size=6.5), xy=(52.0, 13.5))
patch1 = era1.add(Node((25, 17), "Manual Patching\nHigh Ops Toil", icon=PhosphorIcon.WRENCH, icon_size=6.5, card_style=Styles.Neutral), xy=(88.5, 13.5))
d.connect(u1, vps, label="HTTPS", padding=0.8)
d.connect(vps, patch1, label="Toil", style=Styles.Muted, padding=0.8)

# Bottom Era: Mid-2025 Cloud Run
era2 = d.add(
    NodeGroup(title="Mid-2025: Public Cloud Run (Uncapped Pay-Per-Use)", padding=4.0,
              style=Styles.SecondaryNeutral.patch(shape_r=2.0),
              text_style=Styles.AccentBold.patch(text_size=12.5, halign="left")),
    xy=(7.0, 7.0),
)
u2 = era2.add(Node((24, 17), "Internet\n& Botnets", icon=PhosphorIcon.GLOBE, icon_size=6.5, style=Styles.Accent), xy=(14.5, 13.5))
crun = era2.add(
    Node((28, 17), "Cloud Run\nPublic Ingress", icon=GcpIcon.CLOUD_RUN, icon_size=7.0,
         style=Styles.White, text_style=Styles.WhiteBold.patch(text_size=12.5), card_style=Styles.PrimaryFlat),
    xy=(52.0, 13.5),
)
bill = era2.add(
    Node((25, 17), "Auto-Scale Bill\nCPU + Egress", icon=PhosphorIcon.WARNING_OCTAGON, icon_size=6.5,
         style=Styles.White, text_style=Styles.WhiteBold.patch(text_size=12.5), card_style=Styles.AccentFlat),
    xy=(88.5, 13.5),
)
d.connect(u2, crun, label="No WAF", style=Styles.AccentBold, text_style=Styles.AccentBold.patch(text_size=12.0), padding=0.8)
d.connect(crun, bill, label="$$$ Spike", style=Styles.AccentBold, text_style=Styles.AccentBold.patch(text_size=12.0), padding=0.8)

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
Let's look at the background of the target system before the attack began.
- **10 Years of Peaceful Operation (2015–2025)**: The application is a solo-maintained Japanese Text-to-Speech (TTS) synthesis service. For a decade, it ran on a single traditional VPS costing roughly $10/month. On a fixed-price VPS, a traffic spike simply saturates the single CPU core and drops connections—it can never bankrupt the operator.
- **The Serverless Migration (Mid-2025)**: To eliminate manual Linux OS upgrades and maintenance toil, the service was containerized and migrated to Google Cloud Run.
- **The Hidden Architectural Vulnerability**: Because TTS waveform generation requires heavy DSP computation per request, placing Cloud Run directly on the public internet (`ingress = all`) without an upstream CDN or WAF meant that every malicious request automatically spun up more container instances and billed directly for vCPU-seconds and network egress.
:::
