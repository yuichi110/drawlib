::: block (80, 40) (1760, 70)
# The Attacker's Pivot: From Resource Theft to Pure EDoS
:::

::: block (80, 140) (680, 810)
## Strategic Shift in Attack Vector

- **Phase 1 Blocked (`POST /synthesize`)**
  SHA-256 PoW made unauthorized TTS generation computationally infeasible.
- **Phase 2 Retaliation (`GET /challenge` & `/`)**
  Botnet pivoted to unauthenticated endpoints that require **zero PoW**.
- **300 Million Requests / Day**
  A **100x volumetric surge** (~3,500–10,000 RPS) designed purely to inflate cloud request & WAF bills.
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
        "Normal Baseline\n(Organic Users)",
        "Phase 1: CPU Theft\n(POST /synthesize)",
        "Phase 2: Pure EDoS\n(GET / & /challenge)",
    ],
    width=95.0,
    height=63.0,
    title="Daily Request Volume Escalation (Millions / Day)",
    title_style=Styles.BlackBold.patch(text_size=14.5),
    bar_width_ratio=0.5,
    bar_r=1.2,
    axis_text_style=Styles.DarkBold.patch(text_size=12.5),
    grid_style=Styles.MutedDashed,
    value_text_style=Styles.BlackBold.patch(text_size=13.0),
    value_format="{:g}M / day",
)
chart.add_series("Daily Request Volume", [0.1, 3.0, 300.0], style=Styles.AccentFlat)
chart.configure_y_axis(min_value=0.0, max_value=350.0, tick_step=50.0, format="{:.0f}M")
chart.draw(xy=(10.0, 12.0))
```
:::

::: block (1720, 995) (140, 30)
```drawlib
import utils
utils.draw_page_number()
```
:::

::: note
Once the SHA-256 Proof-of-Work challenge went live, the attacker realized they could no longer force our server to synthesize audio without burning massive CPU across their own botnet.
- **From Resource Theft to Pure EDoS**: Rather than walking away, the adversary pivoted immediately to **Phase 2: Economic Denial of Sustainability (EDoS)**.
- **Targeting Lightweight Public Endpoints**: Every Proof-of-Work system requires a public endpoint (`GET /challenge`) and a landing page (`GET /`) that can be requested *before* a client solves a puzzle.
- **300 Million Requests per Day**: The botnet unleashed a **100x volumetric surge**—scaling from ~3 million requests/day to **300+ million requests/day** (~3,500 sustained RPS, peaking at 10,000+ RPS) against `/` and `/challenge`, aiming to inflict maximum per-request cloud infrastructure and WAF billing damage.
:::
