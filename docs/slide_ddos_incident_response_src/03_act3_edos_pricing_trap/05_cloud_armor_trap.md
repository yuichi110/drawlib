::: block xy=(80, 40) width=1760 height=70
# Cloud Billing Log: How Cloud Armor Became the #1 Cost
:::

::: block xy=(80, 140) width=680 height=810
```drawlib
from drawlib.canvas import setup
import utils

setup(width=70, height=84)
utils.draw_kpi_cards(
    [
        ("39.6%", "#1 Bill: Cloud Armor", "WAF fees beat all compute!"),
        ("99.9%", "Edge Block Rate", "Origin CPU stayed ~$1/day"),
        ("$225/d", "Peak WAF Fee Spike", "$0.75/1M reqs during EDoS"),
        ("98%↓", "Post-CF Cutover", "GCP bill dropped to flat base"),
    ],
    width=70,
    height=84,
)
```
:::

::: block xy=(800, 140) width=1040 height=810
```drawlib
from drawlib.canvas import setup
from drawlib.charts.bar import BarChart
from drawlib.smartarts import Panel, Table
from drawlib.styles import Styles

setup(width=115, height=90)

# Top Card: Daily Stacked Billing Trajectory (Modeled on GCP Billing Report)
p_top = Panel(
    "Daily GCP Billing by Service Across Incident Phases ($ USD / Day)",
    style=Styles.Neutral,
    header_style=Styles.PrimaryBold,
    text_style=Styles.BlackBold.patch(text_size=14.5),
    header_variant="underline",
    header_height=8.0,
    header_align="center",
)
p_top.draw(xy=(2.0, 36.0), width=111.0, height=52.0)

chart = BarChart(
    axis_line_style=Styles.Primary,
    categories=[
        "Base\nD1-4",
        "Flood1\nD5-6",
        "Flood2\nD7-9",
        "WAF\nD10-12",
        "PoW\nD13-17",
        "Probe\nD18-20",
        "EDoS1\nD24",
        "EDoS2\nD25",
        "CF Cut\nD26+",
    ],
    width=99.0,
    height=34.5,
    bar_mode="stack",
    bar_width_ratio=0.58,
    bar_r=0.8,
    axis_text_style=Styles.DarkBold.patch(text_size=11.8),
    grid_style=Styles.MutedDashed,
)

chart.add_series(
    "Cloud Run (CPU)",
    [2.0, 26.0, 34.0, 14.0, 3.0, 4.0, 3.0, 2.5, 2.0],
    style=Styles.AccentFlat,
)
chart.add_series(
    "Cloud Logging",
    [0.5, 18.0, 24.0, 8.0, 1.5, 2.0, 2.0, 1.5, 0.5],
    style=Styles.WarningFlat,
)
chart.add_series(
    "GCLB & CDN",
    [0.0, 0.0, 0.0, 10.0, 4.0, 5.0, 15.0, 8.0, 0.0],
    style=Styles.Cyan4Flat,
)
chart.add_series(
    "Cloud Armor WAF",
    [0.0, 0.0, 0.0, 12.0, 3.0, 32.0, 205.0, 58.0, 0.0],
    style=Styles.PrimaryFlat,
)

chart.configure_y_axis(min_value=0.0, max_value=250.0, tick_step=50.0, format="${:.0f}")
chart.draw(xy=(8.0, 38.0))
chart.draw_legend(xy=(8.5, 76.0), text_style=Styles.DarkBold.patch(text_size=11.8), orientation="horizontal", item_gap=2.8)

# Bottom Card: Service Cost Breakdown Table
p_bot = Panel(
    "Monthly GCP Billing Breakdown by Service (Ranked by Total Cost)",
    style=Styles.Neutral,
    header_style=Styles.PrimaryBold,
    text_style=Styles.BlackBold.patch(text_size=14.5),
    header_variant="underline",
    header_height=7.5,
    header_align="center",
)
p_bot.draw(xy=(2.0, 2.0), width=111.0, height=31.5)

table = Table(
    cell_style=Styles.White,
    text_style=Styles.Dark.patch(text_size=12.0),
    header_cell_style=Styles.PrimaryFlat,
    header_text_style=Styles.WhiteBold.patch(text_size=12.2),
    border_style=Styles.MutedThin,
)
table.set_style_cell(
    background_color=(252, 232, 230),
    text_style=Styles.DangerBold.patch(text_size=12.0),
    rows=[1],
    columns=[0, 1, 2, 3],
)
data = [
    ["GCP Service", "Primary Cost Driver", "Peak Phase", "Bill Share"],
    ["1. Google Cloud Armor", "$0.75 / 1M evaluated reqs", "D24-25 EDoS Spike", "39.6% (#1)"],
    ["2. Cloud Run (Compute)", "Uncached TTS vCPU & egress", "D5-9 Direct Flood", "34.4% (#2)"],
    ["3. Logging + GCLB/CDN", "Flood access logs & L7 LB", "D5-9 & D10-25", "26.0% (18%+8%)"],
]
table.draw_flexible(xy=(5.5, 25.0), column_widths=[32.0, 33.0, 23.0, 16.0], row_heights=[5.5, 5.5, 5.5, 5.5], data=data)
```
:::

::: block xy=(1720, 995) width=140 height=30
```drawlib
import utils
utils.draw_page_number()
```
:::

::: note
This stacked daily billing chart is abstracted directly from our Google Cloud Billing Report across the incident month, and it tells the entire story in four distinct phases:
1. **Days 5–9 (Initial Direct Flood — Orange & Yellow Bars)**: Before we had a WAF, the cache-busting TTS flood drove up **Cloud Run compute (Orange, 34.4% of monthly bill)** alongside a massive hidden cost: **Cloud Logging (Yellow, 18.0% of monthly bill)** from gigabytes of high-velocity request logs.
2. **Days 10–17 (GCLB + Cloud Armor + PoW)**: Deploying Perimeter WAF and SHA-256 Proof-of-Work successfully crushed Cloud Run compute and logging costs back down near baseline.
3. **Days 24–25 (The Cloud Armor EDoS Explosion — Giant Blue Bar)**: When the attacker pivoted to a 300M req/day volumetric flood, look at Day 24: **Cloud Run (Orange) at the bottom of the bar is almost invisible (~$3/day)** because Cloud Armor blocked 99.9% of traffic—yet **Google Cloud Armor (Blue) shot up to $205+ in a single day**, becoming the **#1 cost of the entire month (39.6%)**!
4. **Days 26–30 (Post-Cloudflare Cutover)**: The moment we tore down GCLB/Cloud Armor and migrated to flat-rate Cloudflare Pro, daily GCP billing flatlined back to $2/day.
:::
