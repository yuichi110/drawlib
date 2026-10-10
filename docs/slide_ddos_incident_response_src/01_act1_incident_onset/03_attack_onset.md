::: block (80, 40) (1760, 70)
# The Attack Onset: Cache-Busting TTS Flood
:::

::: block (80, 140) (680, 810)
## Telemetry & Billing Shock

- **4–5x Weekly Bill Multiplier**
  Cloud Run compute & egress costs jumped **400%+** overnight.
- **100% Cache-Miss Exploitation**
  Bots randomized `text`, `pitch`, and `speed` query parameters on every call.
- **CPU Saturation**
  Every single request forced a cold DSP audio synthesis cycle.
:::

::: block (800, 140) (1040, 810)
```drawlib
from drawlib.canvas import setup
from drawlib.charts.bar import BarChart
from drawlib.shapes import rectangle
from drawlib.smartarts import ChevronProcess
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=115, height=90)

# Top Card: Weekly Cloud Run Cost Spike BarChart
rectangle((57.5, 62.0), width=111, height=50, style=Styles.Neutral.patch(shape_r=2.5))

chart = BarChart(
    axis_line_style=Styles.Primary,
    categories=["Week -2\n(Normal)", "Week -1\n(Normal)", "Attack Day 1\n(Bot Flood)", "Attack Day 3\n(Unmitigated)"],
    width=96.0,
    height=38.0,
    title="Weekly Cloud Run Compute & Egress Run-Rate ($ USD)",
    title_style=Styles.BlackBold.patch(text_size=11.5),
    bar_width_ratio=0.55,
    bar_r=1.0,
    axis_text_style=Styles.Dark.patch(text_size=9.5),
    grid_style=Styles.MutedDashed,
    value_text_style=Styles.BlackBold.patch(text_size=9.5),
    value_format="${:.1f}/wk",
)
chart.add_series("Weekly Cloud Run Bill", [2.5, 2.6, 9.8, 12.0], style=Styles.AccentFlat)
chart.configure_y_axis(min_value=0.0, max_value=15.0, tick_step=5.0, format="${:.0f}")
chart.draw(xy=(9.0, 40.0))

# Bottom Card: Cache-Busting Exploitation Pipeline
rectangle((57.5, 18.0), width=111, height=30, style=Styles.Neutral.patch(shape_r=2.5))
text((57.5, 29.0), "How Parameter Mutation Defeated Application Caching", style=Styles.BlackBold.patch(text_size=11.0))

pipeline = ChevronProcess(
    style=Styles.PrimaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=10.0),
    description_style=Styles.Dark.patch(text_size=9.5),
    corner_angle=60.0,
    spacing=2.0,
    flat_left_end=True,
)
pipeline.add("1. Mutate Params", description="Random text/pitch/speed")
pipeline.add("2. 100% Cache Miss", description="Unique hash per request", style=Styles.SecondaryNeutral)
pipeline.add(
    "3. Full DSP Synthesis",
    description="100% vCPU + WAV Egress",
    style=Styles.AccentFlat,
    text_style=Styles.WhiteBold.patch(text_size=10.0),
    description_style=Styles.White.patch(text_size=9.5),
)
pipeline.draw(xy=(7.5, 7.0), width=100.0, height=17.0)
```
:::

::: block (1720, 995) (140, 30)
```drawlib
import utils
utils.draw_page_number()
```
:::

::: note
The incident was first discovered not through an uptime alert, but through a Google Cloud billing anomaly notification:
- **4–5x Weekly Cost Spike**: Within 48 hours, weekly Cloud Run charges jumped nearly 5x above the 10-year historical baseline.
- **Why Application Caching Failed**: The attacker specifically targeted the CPU-heavy `/synthesize` endpoint. Instead of replaying identical URLs (which would hit an in-memory or CDN cache), the botnet randomized the `text`, `pitch`, and `speed` parameters on every single HTTP request.
- **Maximum Resource Amplification**: Because every request had a unique parameter signature, the cache hit ratio dropped to 0%. Every bot request forced a full DSP waveform synthesis cycle in Python/C++, pegging container vCPUs at 100% and streaming megabytes of generated WAV audio back out over billable cloud egress.
:::
