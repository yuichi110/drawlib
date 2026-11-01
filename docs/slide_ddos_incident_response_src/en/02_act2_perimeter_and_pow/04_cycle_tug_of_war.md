::: block xy=(80, 40) width=1760 height=70
# Cycle Tug-of-War: Block, CDN & Origin Telemetry
:::

::: block xy=(80, 140) width=680 height=810
## Competing Objectives in Logs

- **Attacker's Goal: Drive Origin Up**
  Evade WAF filters and randomize parameters so requests penetrate to **Origin (Blue)** and burn server resources.
- **Defender's Goal: Drive Block & CDN Up**
  Absorb attacks via **Edge Block (Red)** and **CDN Cache (Amber)** while keeping **Origin flat** with **zero false positives**.
- **5-Day Cat-and-Mouse Waveform**
  Every **Blue spike** marks an attacker bypass; every **Red takeover** marks a new defense rule sealing the leak.
:::

::: block xy=(800, 140) width=1040 height=810
```drawlib
from drawlib.canvas import setup
from drawlib.charts.line import LineChart
from drawlib.smartarts import KpiCards, Panel
from drawlib.styles import Styles

setup(width=115, height=90)

panel = Panel(
    "5-Day Traffic Tug-of-War: Edge Blocked vs. CDN Cached vs. Origin Served",
    style=Styles.Neutral,
    header_style=Styles.PrimaryBold,
    text_style=Styles.BlackBold.patch(text_size=14.5),
    header_variant="underline",
    header_height=8.0,
    header_align="center",
)
panel.draw(xy=(2.0, 2.0), width=111.0, height=86.0)

# Top Goal Comparison Cards via KpiCards (2 columns)
goals = KpiCards(
    style=Styles.White,
    metric_style=Styles.PrimaryBold.patch(text_size=15.5),
    text_style=Styles.BlackBold.patch(text_size=12.8),
    description_style=Styles.Dark.patch(text_size=11.5),
    accent_style=Styles.PrimaryFlat,
    accent_position="left_pill",
    metric_layout="left_column",
    metric_width_ratio=0.33,
    spacing=3.5,
)
goals.add(
    "Origin↑",
    "Attacker Goal (Blue)",
    "Bypass WAF & bust CDN",
    style=Styles.PrimaryNeutral,
)
goals.add(
    "Block↑",
    "Defender Goal (Red)",
    "Flat Origin + 0% user drop",
    style=Styles.DangerNeutral,
    metric_style=Styles.DangerBold.patch(text_size=15.5),
    accent_style=Styles.DangerFlat,
)
goals.draw(xy=(6.5, 65.5), width=102.0, height=12.5, columns=2)

# Main Cloudflare-style Multi-Series LineChart (no area fill, no vertex circles)
chart = LineChart(
    axis_line_style=Styles.Primary,
    categories=[
        "Day 1", "", "", "",
        "Day 2", "", "", "",
        "Day 3", "", "", "",
        "Day 4", "", "", "",
        "Day 5", "", "", "",
    ],
    width=101.0,
    height=50.5,
    show_points=False,
    point_shape="none",
    axis_text_style=Styles.DarkBold.patch(text_size=12.2),
    grid_style=Styles.MutedDashed,
)

chart.add_series(
    "Edge Blocked (1.93M)",
    [
        1.0, 132.0, 4.0, 2.0,
        2.0, 20.0, 32.0, 18.0,
        9.0, 22.0, 6.0, 21.0,
        19.0, 15.0, 2.0, 16.0,
        30.0, 26.0, 33.0, 28.0,
    ],
    style=Styles.DangerFlat,
    line_width=2.5,
)
chart.add_series(
    "Origin Served (1.03M)",
    [
        1.0, 39.0, 52.0, 21.0,
        57.0, 6.0, 9.0, 5.0,
        4.0, 36.0, 55.0, 32.0,
        2.0, 1.5, 1.5, 17.0,
        2.0, 1.2, 1.2, 1.0,
    ],
    style=Styles.PrimaryFlat,
    line_width=2.5,
)
chart.add_series(
    "CDN Cached (173k)",
    [
        0.8, 2.0, 1.2, 1.0,
        1.5, 1.8, 2.2, 1.2,
        1.5, 18.0, 38.0, 5.0,
        1.2, 1.0, 1.0, 14.0,
        1.5, 1.2, 1.2, 1.0,
    ],
    style=Styles.WarningFlat,
    line_width=2.3,
)

chart.configure_y_axis(min_value=0.0, max_value=150.0, tick_step=30.0, format="{:.0f}k")
chart.draw(xy=(7.0, 5.5))
chart.draw_legend(xy=(9.5, 59.5), text_style=Styles.DarkBold.patch(text_size=11.8), orientation="horizontal", item_gap=3.0)
```
:::

::: block xy=(1720, 995) width=140 height=30
```drawlib
import utils
utils.draw_page_number()
```
:::

::: note
When the Defender's 5-step cycle and the Attacker's 5-step cycle collide in production, this 5-day traffic telemetry log is the result—a real-time tug-of-war across three metrics:
- **Attacker's Objective (Maximize Origin — Blue Line)**: The attacker wants every request to bypass the edge and force the **Origin** to execute expensive logic. Each time the attacker discovered a WAF blind spot (Day 1, Day 2, and Day 3), Origin traffic spiked to **50k+ requests/hour**.
- **Defender's Objective (Maximize Block & CDN — Red & Amber Lines)**: Our goal as defenders is to convert that blue Origin line into **Edge Blocked (Red)** and **CDN Cached (Amber)**—while never falsely blocking legitimate users.
- **Convergence by Day 5**: Notice how after multiple cat-and-mouse iterations, by Day 5 the **Origin (Blue)** line is pinned flat near zero (serving only legitimate human traffic), while the **Edge Blocked (Red)** line smoothly absorbs 100% of the ongoing **30k/hr** attack stream.
:::
