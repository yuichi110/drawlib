::: block xy=(80, 40) width=1760 height=70
# Background: A 10-Year Hobby Service Enters the Cloud
:::

::: block xy=(80, 140) width=680 height=810
## Architecture Evolution

- **10 Years of Peace (2015–2025)**
  Japanese TTS web service running at **$10/mo** on a single VPS.
- **Serverless Migration (Mid-2025)**
  Containerized onto **Google Cloud Run** for zero-ops maintenance.
- **Hidden Vulnerability**
  Direct public URL (`run.app`) with **no CDN or Edge WAF** and uncapped pay-per-use scaling.
:::

::: block xy=(800, 140) width=1040 height=810
```drawlib
from drawlib.canvas import setup
from drawlib.diagrams.architecture import ArchitectureDiagram, GcpIcon, Node, NodeGroup, PhosphorIcon
from drawlib.smartarts import Panel
from drawlib.styles import Styles

setup(width=115, height=90)

panel = Panel(
    "Legacy Fixed-Cost VPS vs. Direct Public Cloud Run",
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

# Top Era: 2015-2025 VPS
era1 = d.add(
    NodeGroup(title="2015–2025: Legacy Single VPS ($10/mo Cap)", padding=5.0,
              style=Styles.PrimaryNeutral.patch(shape_r=2.0),
              text_style=Styles.PrimaryBold.patch(text_size=13.5, halign="left")),
    xy=(7.0, 45.5),
)
u1 = era1.add(Node("Web Users\nLow Volume", width=16, height=16, icon=PhosphorIcon.USERS, icon_size=8.0), xy=(14.5, 13.5))
vps = era1.add(Node("Single Linux VPS\n$10/mo Hard Cap", width=18, height=16, icon=PhosphorIcon.HARD_DRIVES, icon_size=8.0), xy=(52.0, 13.5))
patch1 = era1.add(Node("Manual Patching\nHigh Ops Toil", width=18, height=16, icon=PhosphorIcon.WRENCH, icon_size=8.0, style=Styles.Dark), xy=(88.5, 13.5))
d.connect(u1, vps, label="HTTPS", padding=0.5)
d.connect(vps, patch1, label="Toil", style=Styles.MutedBold, padding=0.5)

# Bottom Era: Mid-2025 Cloud Run
era2 = d.add(
    NodeGroup(title="Mid-2025: Public Cloud Run (Uncapped Pay-Per-Use)", padding=5.0,
              style=Styles.SecondaryNeutral.patch(shape_r=2.0),
              text_style=Styles.AccentBold.patch(text_size=13.5, halign="left")),
    xy=(7.0, 6.5),
)
u2 = era2.add(Node("Internet\n& Botnets", width=16, height=16, icon=PhosphorIcon.GLOBE, icon_size=8.0, style=Styles.Accent), xy=(14.5, 13.5))
crun = era2.add(
    Node("Cloud Run\nPublic Ingress", width=18, height=16, icon=GcpIcon.CLOUD_RUN, icon_size=8.5),
    xy=(52.0, 13.5),
)
bill = era2.add(
    Node("Auto-Scale Bill\nCPU + Egress", width=18, height=16, icon=PhosphorIcon.WARNING_OCTAGON, icon_size=8.0,
         style=Styles.Danger),
    xy=(88.5, 13.5),
)
d.connect(u2, crun, label="No WAF", style=Styles.AccentBold, text_style=Styles.AccentBold.patch(text_size=12.5), padding=0.5)
d.connect(crun, bill, label="$$$ Spike", style=Styles.AccentBold, text_style=Styles.AccentBold.patch(text_size=12.5), padding=0.5)

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
Let's look at the background of the target system before the attack began.
- **10 Years of Peaceful Operation (2015–2025)**: The application is a solo-maintained Japanese Text-to-Speech (TTS) synthesis service. For a decade, it ran on a single traditional VPS costing roughly $10/month. On a fixed-price VPS, a traffic spike simply saturates the single CPU core and drops connections—it can never bankrupt the operator.
- **The Serverless Migration (Mid-2025)**: To eliminate manual Linux OS upgrades and maintenance toil, the service was containerized and migrated to Google Cloud Run.
- **The Hidden Architectural Vulnerability**: Because TTS waveform generation requires heavy DSP computation per request, placing Cloud Run directly on the public internet (`ingress = all`) without an upstream CDN or WAF meant that every malicious request automatically spun up more container instances and billed directly for vCPU-seconds and network egress.
:::
