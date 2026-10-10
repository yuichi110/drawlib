::: block (80, 40) (1760, 70)
# Traffic Forensics: Decomposing the Two Botnet Fleets
:::

::: block (80, 130) (1760, 170)
- **Log Forensics Breakthrough**: Inspecting Cloudflare request logs by **ASN**, **HTTP Protocol Version**, and **User-Agent** revealed the attack was actually **two distinct botnet fleets**.
- **Protocol Mismatch Tell**: Fleet B spoofed modern Chrome/Safari User-Agents (`Chrome/134`), but its proxy software spoke **HTTP/1.1** (real browsers always negotiate **HTTP/2 or HTTP/3**!).
:::

::: block (80, 320) (1760, 630)
```drawlib
from drawlib.canvas import setup
from drawlib.charts.pie import PieChart
from drawlib.shapes import rectangle
from drawlib.smartarts import Table
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=176, height=63)

# Left Card: Donut PieChart of Traffic Composition
rectangle((33.0, 31.5), width=60.0, height=59.0, style=Styles.Neutral.patch(shape_r=2.5))
text((33.0, 55.5), "Attack Fleet Breakdown", style=Styles.BlackBold.patch(text_size=14.0))

pie = PieChart(
    radius=14.5,
    hole_ratio=0.44,
    center_text="300M\n/Day",
    center_text_style=Styles.BlackBold.patch(text_size=11.0),
    value_text_style=Styles.WhiteBold.patch(text_size=11.0),
)
pie.add_slice("Fleet A: Cloud ASNs (55%)", 55.0, style=Styles.PrimaryFlat)
pie.add_slice("Fleet B: Home HTTP/1.1 (44.5%)", 44.5, style=Styles.AccentFlat)
pie.add_slice("Real Users: HTTP/2+3 (0.5%)", 0.5, style=Styles.SecondaryFlat)
pie.draw(xy=(18.5, 22.0))
pie.draw_legend(xy=(6.5, 16.5), text_style=Styles.DarkBold.patch(text_size=11.0), orientation="vertical")

# Right Card: Forensic Comparison Table
rectangle((120.5, 31.5), width=107.0, height=59.0, style=Styles.Neutral.patch(shape_r=2.5))
text((120.5, 55.5), "Forensic Fingerprint Comparison: Bot Fleets vs. Real Users", style=Styles.BlackBold.patch(text_size=14.0))

table = Table(
    cell_style=Styles.White,
    text_style=Styles.Dark.patch(text_size=11.0),
    header_cell_style=Styles.PrimaryFlat,
    header_text_style=Styles.WhiteBold.patch(text_size=11.0),
    border_style=Styles.MutedThin,
)
table.set_style_cell_evenodd(
    even_color=(248, 250, 252),
    even_text_style=Styles.Dark.patch(text_size=11.0),
    odd_color=Colors.White,
    odd_text_style=Styles.Dark.patch(text_size=11.0),
)
table.set_style_cell(
    background_color=(252, 232, 230),
    text_style=Styles.AccentBold.patch(text_size=11.0),
    rows=[3, 4],
    columns=[2],
)

forensics = [
    ["Signal", "Fleet A: Cloud VMs", "Fleet B: Home Proxies", "Real Users (0.5%)"],
    ["Network ASN", "AWS / GCP / OVH", "JP Home Fiber ISPs", "JP Consumer ISPs"],
    ["Rate per IP", "Burst (20–100 / 10s)", "Stealth (6–8 / 10s)", "1–3 req / min"],
    ["User-Agent", "python / Go / Old UA", "Spoofed Chrome 130", "Chrome / Safari"],
    ["HTTP Version", "HTTP/1.1 or HTTP/2", "HTTP/1.1 ONLY!", "HTTP/2 or HTTP/3"],
    ["WAF Action", "Block Hosting ASNs", "Block HTTP/1.1", "Zero-Friction Pass"],
]
table.draw_flexible(xy=(69.5, 51.0), column_widths=[19.0, 26.5, 30.5, 26.0], row_heights=[7.2, 7.2, 7.2, 7.2, 7.2, 7.2], data=forensics)
```
:::

::: block (1720, 995) (140, 30)
```drawlib
import utils
utils.draw_page_number()
```
:::

::: note
To eliminate the remaining 25% sub-threshold leak without blocking legitimate Japanese users on the same ISPs, we performed deep HTTP telemetry forensics in Cloudflare Analytics and discovered the botnet consisted of **two distinct fleets**:
1. **Fleet A — Datacenter & Cloud VMs (55% of volume)**: Originated from commercial cloud/VPS Autonomous System Numbers (ASNs). Since a consumer web app never receives legitimate human browser clicks from headless datacenter ASNs, we blocked entire cloud hosting ASNs outright at the WAF edge.
2. **Fleet B — Hijacked Domestic Residential Proxies (44.5% of volume)**: Shared the exact same Japanese consumer ISP ASNs as our real users and spoofed modern `User-Agent` strings (`Chrome/134.0`).
- **The Smoking-Gun Protocol Mismatch**: Every modern web browser (Chrome, Safari, Firefox, Edge) connecting to Cloudflare over TLS negotiates **HTTP/2 or HTTP/3 (QUIC)** via ALPN. Fleet B's residential proxy forwarding software, however, hardcoded **HTTP/1.1**! Blocking or challenging `http.request.version == "HTTP/1.1"` instantly wiped out Fleet B with zero false positives.
:::
