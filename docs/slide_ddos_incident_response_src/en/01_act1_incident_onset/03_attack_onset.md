::: block xy=(80, 40) width=1760 height=70
# The Attack Onset: Cache-Busting TTS Flood
:::

::: block xy=(80, 140) width=680 height=810
## Telemetry & Billing Shock

- **Cloud Run + Cloud Logging Surge**
  Compute/egress and high-volume request logging jumped **15–20x above daily baseline**.
- **100% Cache-Miss Exploitation**
  Bots randomized `text`, `pitch`, and `speed` query parameters on every call.
- **CPU & Log Saturation**
  Every request forced cold DSP audio synthesis and wrote gigabytes of access logs.
:::

::: block xy=(800, 140) width=1040 height=810
```drawlib
from drawlib.canvas import setup
from drawlib.charts.bar import BarChart
from drawlib.smartarts import ChevronProcess, Panel
from drawlib.styles import Styles

setup(width=115, height=90)

# Top Card: Initial Cloud Run + Cloud Logging Cost Spike BarChart
p_top = Panel(
    "Phase 1 Daily Billing Spike: Cloud Run CPU + Cloud Logging ($ USD / Day)",
    style=Styles.Neutral,
    header_style=Styles.PrimaryBold,
    text_style=Styles.BlackBold.patch(text_size=14.2),
    header_variant="underline",
    header_height=8.0,
    header_align="center",
)
p_top.draw(xy=(2.0, 36.5), width=111.0, height=51.5)

chart = BarChart(
    axis_line_style=Styles.Primary,
    categories=["Day 1-2\n(Normal)", "Day 3-4\n(Normal)", "Day 5\n(Onset)", "Day 6\n(Flood)", "Day 7-8\n(Peak)"],
    width=95.0,
    height=34.0,
    bar_mode="stack",
    bar_width_ratio=0.52,
    bar_r=1.0,
    axis_text_style=Styles.DarkBold.patch(text_size=12.5),
    grid_style=Styles.MutedDashed,
)
chart.add_series("Cloud Run (CPU & Egress)", [2.0, 2.2, 24.0, 34.0, 32.0], style=Styles.AccentFlat)
chart.add_series("Cloud Logging (Ingestion)", [0.5, 0.5, 16.0, 24.0, 22.0], style=Styles.WarningFlat)
chart.configure_y_axis(min_value=0.0, max_value=65.0, tick_step=20.0, format="${:.0f}")
chart.draw(xy=(10.0, 39.0))
chart.draw_legend(xy=(15.0, 75.8), text_style=Styles.DarkBold.patch(text_size=12.0), orientation="horizontal", item_gap=4.5)

# Bottom Card: Cache-Busting Exploitation Pipeline
p_bot = Panel(
    "How Parameter Mutation Defeated Application Caching",
    style=Styles.Neutral,
    header_style=Styles.PrimaryBold,
    text_style=Styles.BlackBold.patch(text_size=14.5),
    header_variant="underline",
    header_height=7.5,
    header_align="center",
)
p_bot.draw(xy=(2.0, 2.0), width=111.0, height=31.5)

pipeline = ChevronProcess(
    style=Styles.PrimaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=13.5),
    description_style=Styles.Dark.patch(text_size=12.0),
    corner_angle=60.0,
    spacing=2.0,
    flat_left_end=True,
)
pipeline.add("1. Mutate Params", description="Random text/pitch/speed")
pipeline.add("2. 100% Cache Miss", description="Unique hash per call", style=Styles.SecondaryNeutral)
pipeline.add(
    "3. Full DSP + Logs",
    description="100% CPU + Log Flood",
    style=Styles.AccentFlat,
    text_style=Styles.WhiteBold.patch(text_size=13.5),
    description_style=Styles.White.patch(text_size=12.0),
)
pipeline.draw(xy=(6.5, 5.5), width=102.0, height=18.5)
```
:::

::: block xy=(1720, 995) width=140 height=30
```drawlib
import utils
utils.draw_page_number()
```
:::

::: note
The incident was first discovered not through an uptime alert, but through a Google Cloud billing anomaly notification:
- **Dual Cost Spike (Cloud Run + Cloud Logging)**: Within 48 hours, daily charges jumped nearly 20x above the historical baseline. Notably, while **Cloud Run CPU & egress (Orange)** accounted for ~58% of this initial surge, **Cloud Logging (Amber)** accounted for ~42%—because every single flood request generated structured container and HTTP request log entries!
- **Why Application Caching Failed**: The attacker specifically targeted the CPU-heavy `/synthesize` endpoint. Instead of replaying identical URLs (which would hit an in-memory or CDN cache), the botnet randomized the `text`, `pitch`, and `speed` parameters on every single HTTP request.
- **Maximum Resource Amplification**: Because every request had a unique parameter signature, the cache hit ratio dropped to 0%, forcing a full DSP waveform synthesis cycle in Python/C++ on every call.
:::
