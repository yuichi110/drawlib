::: block xy=(80, 40) width=1760 height=70
# Composite WAF Rules: 10 Custom Rules & 2 Rate Limits
:::

::: block xy=(80, 140) width=1760 height=810
```drawlib
from drawlib.canvas import setup
from drawlib.charts.bar import BarChart
from drawlib.smartarts import Panel, Table
from drawlib.styles import Colors, Styles

setup(width=176, height=81)

# Left Card: Ordered Rule Chain Table (Modeled on Cloudflare Security Rules & Rate Limits)
p_left = Panel(
    "Production WAF Rule Chain (10 Custom + 2 Rate Limits)",
    style=Styles.Neutral,
    header_style=Styles.PrimaryBold,
    text_style=Styles.BlackBold.patch(text_size=13.2),
    header_variant="underline",
    header_height=8.5,
    header_align="center",
)
p_left.draw(xy=(2.0, 2.0), width=95.0, height=77.0)

table = Table(
    cell_style=Styles.White,
    text_style=Styles.Dark.patch(text_size=11.2),
    header_cell_style=Styles.PrimaryFlat,
    header_text_style=Styles.WhiteBold.patch(text_size=11.5),
    border_style=Styles.MutedThin,
)
table.set_style_cell_evenodd(
    even_color=(248, 250, 252),
    even_text_style=Styles.Dark.patch(text_size=11.2),
    odd_color=Colors.White,
    odd_text_style=Styles.Dark.patch(text_size=11.2),
)
# Restore Header Row style after evenodd
table.set_style_cell(
    background_color=Colors.Primary,
    text_style=Styles.WhiteBold.patch(text_size=11.5),
    rows=[0],
    columns=[0, 1, 2, 3],
)
# Highlight the 4 primary high-volume rules (ASN, HTTP/1.1, Challenge+Cookie, Rate Limit)
table.set_style_cell(
    background_color=(232, 240, 254),
    text_style=Styles.PrimaryBold.patch(text_size=11.2),
    rows=[2, 3, 7, 8],
    columns=[0, 3],
)
table.set_style_cell(
    background_color=(252, 232, 230),
    text_style=Styles.DangerBold.patch(text_size=11.2),
    rows=[1, 2, 3, 4, 5, 6, 8],
    columns=[2],
)
table.set_style_cell(
    background_color=(255, 242, 204),
    text_style=Styles.AccentBold.patch(text_size=11.2),
    rows=[7],
    columns=[2],
)

rule_data = [
    ["Rule Layer", "Match Condition", "Action", "Events"],
    ["#1 Tor / Anon Geo", "Country in {T1, A1, XX}", "Block", "18.5k"],
    ["#2 Cloud ASNs", "ASN in {Cloud / VPS}", "Block", "245.0k"],
    ["#3 HTTP/1.1 API", "URI /api/* & HTTP/1.1", "Block", "165.0k"],
    ["#4-5 OS / Browser", "URI /api/* & UA Anomaly", "Block", "32.0k"],
    ["#6-7 Client Hdrs", "URI /api/* & Sec-Fetch", "Block", "26.5k"],
    ["#8 Trace Recon", "URI == /cdn-cgi/trace", "Block", "8.0k"],
    ["#9-10 Chal+Cookie", "Page Chal -> API Cookie", "Chal+Blk", "210.0k"],
    ["RL #1-2 Rate Cap", "5/30s (/chal) & 15/30s", "Block", "145.0k"],
]
table.draw_flexible(
    xy=(4.5, 68.5),
    column_widths=[27.5, 34.5, 14.5, 13.5],
    row_heights=[7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0],
    data=rule_data,
)

# Right Card: Horizontal BarChart of Hit Distribution Across Rules
p_right = Panel(
    "Mitigated Events by Rule (850k Total)",
    style=Styles.Neutral,
    header_style=Styles.PrimaryBold,
    text_style=Styles.BlackBold.patch(text_size=13.2),
    header_variant="underline",
    header_height=8.5,
    header_align="center",
)
p_right.draw(xy=(100.0, 2.0), width=74.0, height=77.0)

chart = BarChart(
    axis_line_style=Styles.Primary,
    categories=[
        "#8 Trace\n(0.9%)",
        "#1 Tor/Geo\n(2.2%)",
        "#6-7 Hdrs\n(3.1%)",
        "#4-5 OS/UA\n(3.8%)",
        "RL Rate\n(17.1%)",
        "#3 HTTP/1.1\n(19.4%)",
        "#9-10 Cookie\n(24.7%)",
        "#2 Cloud ASN\n(28.8%)",
    ],
    width=61.0,
    height=63.5,
    orientation="horizontal",
    bar_width_ratio=0.62,
    bar_r=0.8,
    axis_text_style=Styles.DarkBold.patch(text_size=10.8),
    grid_style=Styles.MutedDashed,
    value_text_style=Styles.BlackBold.patch(text_size=11.0),
    value_format="{:.1f}k",
)
chart.add_series(
    "Mitigated Events (k)",
    [8.0, 18.5, 26.5, 32.0, 145.0, 165.0, 210.0, 245.0],
    style=Styles.PrimaryFlat,
)
chart.configure_x_axis(min_value=0.0, max_value=300.0, tick_step=100.0, format="{:.0f}k")
chart.draw(xy=(109.5, 5.5))
```
:::

::: block xy=(1720, 995) width=140 height=30
```drawlib
import utils
utils.draw_page_number()
```
:::

::: note
Here is the concrete production rule chain abstracted from our Cloudflare Security Rules and Rate Limiting dashboard, showing how 10 custom rules and 2 rate-limiting rules worked together:
- **Four Heavy-Lifting Pillars (90% of Mitigated Volume)**:
  1. **#2 Block Cloud & Hosting ASNs (245.0k / 28.8%)**: Drops commercial cloud and datacenter VMs at top priority.
  2. **#9–10 Page Managed Challenge + API `cf_clearance` Cookie Gate (210.0k / 24.7%)**: Because challenging AJAX `/api/*` endpoints directly breaks frontend apps, Rule #9 applies a Managed Challenge on HTML page entry (`~31%` Challenge Solve Rate), and Rule #10 blocks any direct `/api/*` call missing the issued `cf_clearance` clearance cookie.
  3. **#3 Block Legacy HTTP/1.1 on `/api/*` (165.0k / 19.4%)**: Eliminates residential proxy relays that fail to negotiate HTTP/2 or HTTP/3.
  4. **RL #1–2 Dual-Threshold Rate Limits (145.0k / 17.1%)**: Enforces a tight `5 req / 30s` cap on `/api/challenge` alongside a `15 req / 30s` global fallback per IP.
- **Four Surgical Hygiene Guardrails (10% of Mitigated Volume)**:
  - **#4–5 Unknown OS / Browser Spoof (32.0k / 3.8%)**, **#6–7 API Client & `Sec-Fetch` Headers (26.5k / 3.1%)**, **#1 Tor / Anonymous Geo (18.5k / 2.2%)**, and **#8 `/cdn-cgi/trace` Recon Block (8.0k / 0.9%)** caught specialized probe bots that slipped past volumetric filters.
:::
