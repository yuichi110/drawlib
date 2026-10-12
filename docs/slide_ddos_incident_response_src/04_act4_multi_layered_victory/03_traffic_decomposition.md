::: block xy=(80, 40) width=1760 height=70
# Traffic Forensics: Decomposing the Two Botnet Fleets
:::

::: block xy=(80, 130) width=1760 height=170
- **Log Forensics Breakthrough**: Inspecting Cloudflare request logs by **ASN**, **HTTP Protocol Version**, and **User-Agent** revealed the attack was actually **two distinct botnet fleets**.
- **Protocol Mismatch Tell**: Fleet B spoofed modern Chrome/Safari User-Agents (`Chrome/134`), but its proxy software spoke **HTTP/1.1** (real browsers always negotiate **HTTP/2 or HTTP/3**!).
:::

::: block xy=(80, 320) width=1760 height=630
```drawlib
from drawlib.canvas import setup
from drawlib.charts.pie import PieChart
from drawlib.smartarts import Panel, Table
from drawlib.styles import Colors, Styles

setup(width=176, height=63)

# Left Card: Donut PieChart of Traffic Composition
p_left = Panel(
    "Attack Fleet Breakdown",
    style=Styles.Neutral,
    header_style=Styles.PrimaryBold,
    text_style=Styles.BlackBold.patch(text_size=15.0),
    header_variant="underline",
    header_height=8.0,
    header_align="center",
)
p_left.draw(xy=(3.0, 2.0), width=60.0, height=59.0)

pie = PieChart(
    radius=14.2,
    hole_ratio=0.44,
    center_text="300M\n/Day",
    center_text_style=Styles.BlackBold.patch(text_size=12.5),
    value_text_style=Styles.WhiteBold.patch(text_size=12.5),
)
pie.add_slice("Fleet A: Cloud ASNs (55%)", 55.0, style=Styles.PrimaryFlat)
pie.add_slice("Fleet B: Home HTTP/1.1 (44.5%)", 44.5, style=Styles.AccentFlat)
pie.add_slice("Real Users: HTTP/2+3 (0.5%)", 0.5, style=Styles.SecondaryFlat)
pie.draw(xy=(18.8, 22.0))
pie.draw_legend(xy=(6.0, 16.5), text_style=Styles.DarkBold.patch(text_size=12.0), orientation="vertical")

# Right Card: Forensic Comparison Table
p_right = Panel(
    "Forensic Fingerprint Comparison: Bot Fleets vs. Real Users",
    style=Styles.Neutral,
    header_style=Styles.PrimaryBold,
    text_style=Styles.BlackBold.patch(text_size=15.0),
    header_variant="underline",
    header_height=8.0,
    header_align="center",
)
p_right.draw(xy=(67.0, 2.0), width=107.0, height=59.0)

table = Table(
    cell_style=Styles.White,
    text_style=Styles.Dark.patch(text_size=12.0),
    header_cell_style=Styles.PrimaryFlat,
    header_text_style=Styles.WhiteBold.patch(text_size=12.2),
    border_style=Styles.MutedThin,
)
table.set_style_cell_evenodd(
    even_color=(248, 250, 252),
    even_text_style=Styles.Dark.patch(text_size=12.0),
    odd_color=Colors.White,
    odd_text_style=Styles.Dark.patch(text_size=12.0),
)
table.set_style_cell(
    background_color=Colors.Primary,
    text_style=Styles.WhiteBold.patch(text_size=12.2),
    rows=[0],
    columns=[0, 1, 2, 3],
)
table.set_style_cell(
    background_color=(252, 232, 230),
    text_style=Styles.AccentBold.patch(text_size=12.0),
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
table.draw_flexible(xy=(69.5, 49.8), column_widths=[19.5, 26.5, 30.0, 26.0], row_heights=[7.2, 7.2, 7.2, 7.2, 7.2, 7.2], data=forensics)
```
:::

::: block xy=(1720, 995) width=140 height=30
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
