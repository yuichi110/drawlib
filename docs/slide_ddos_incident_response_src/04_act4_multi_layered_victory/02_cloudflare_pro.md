::: block (80, 40) (1760, 70)
# Cloudflare Pro Migration & The 25% Sub-Threshold Leak
:::

::: block (80, 140) (680, 810)
## Why Per-IP Rate Limits Leaked

- **Flat $20/mo Cost Secured**
  Cut over DNS to Cloudflare Pro; 75% of the volumetric flood was blocked immediately at $0 overage.
- **10 Req / 10s Per-IP Threshold**
  Setting stricter per-IP limits risked blocking legitimate Japanese offices & carrier NATs.
- **Distributed Sub-Threshold Swarm**
  **5,000+ bot IPs** throttled down to **6–8 req / 10s each**, leaking **4,000 RPS (25%)** to origin!
:::

::: block (800, 140) (1040, 810)
```drawlib
from drawlib.canvas import setup
from drawlib.charts.bar import BarChart
from drawlib.shapes import rectangle
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=115, height=90)

rectangle((57.5, 45.0), width=111, height=86, style=Styles.Neutral.patch(shape_r=2.5))

chart = BarChart(
    axis_line_style=Styles.Primary,
    categories=[
        "Naive Bot\n(Blocked)",
        "Bot #1\n(Leaked)",
        "Bot #2\n(Leaked)",
        "Bot #5,000\n(Leaked)",
        "IP Ceiling\n(10 / 10s)",
    ],
    width=95.0,
    height=54.0,
    title="Per-IP Rate per 10s Window (5,000 IPs x 8 req/10s = 4,000 RPS Leak)",
    title_style=Styles.BlackBold.patch(text_size=13.5),
    bar_width_ratio=0.48,
    bar_r=1.0,
    axis_text_style=Styles.DarkBold.patch(text_size=12.0),
    grid_style=Styles.MutedDashed,
    value_text_style=Styles.BlackBold.patch(text_size=12.0),
    value_format="{:.0f}/10s",
)
chart.add_series("Per-IP Rate", [18.0, 8.0, 7.0, 8.0, 10.0], style=Styles.AccentFlat)
chart.configure_y_axis(min_value=0.0, max_value=20.0, tick_step=5.0)
chart.draw(xy=(10.0, 23.0))

# Bottom Callout Banner
rectangle((57.5, 11.0), width=102.0, height=12.5, style=Styles.SecondaryNeutral.patch(shape_r=2.0))
text(
    (57.5, 11.0),
    "Sub-Threshold Evasion: 5,000 IPs x 0.8 RPS/IP = 4,000 RPS bypassing per-IP limits!",
    style=Styles.AccentBold.patch(text_size=12.0),
)
```
:::

::: block (1720, 995) (140, 30)
```drawlib
import utils
utils.draw_page_number()
```
:::

::: note
Migrating DNS and ingress to **Cloudflare Pro ($20/month)** immediately eliminated our EDoS billing risk—whether Cloudflare blocked 1 million or 1 billion requests, our monthly WAF bill was fixed at $20.
- **The 25% Leak Problem**: However, standard IP rate limiting (`10 requests per 10 seconds per IP`) only stopped **75%** of the flood. The remaining **25%** still leaked through to Cloud Run.
- **Sub-Threshold Swarm Math**: Why did 25% bypass the rate limiter? Because the attacker controlled **over 5,000 concurrent residential and cloud IPs**, and calibrated each individual bot node to send **only 6 to 8 requests per 10 seconds**—staying safely below the `10 req/10s` per-IP ceiling while still aggregating to **4,000 RPS** against our origin!
:::
