::: block (80, 40) (1760, 70)
# The Defender's Cycle: 5-Step Iterative Mitigation
:::

::: block (80, 140) (680, 810)
## Telemetry-Driven Defense Loop

- **Observe & Extract (Steps 1–2)**
  Inspect attack traffic reaching the origin and isolate shared bot fingerprints (Geo, UA, ASN, HTTP protocol).
- **Design & Apply (Steps 3–4)**
  Engineer targeted blocking rules that avoid false positives on organic users, then deploy to Edge WAF or API.
- **Measure & Iterate (Step 5)**
  Evaluate block rate, origin CPU, and cloud billing—looping back to Step 1 whenever residual traffic leaks through.
:::

::: block (800, 140) (1040, 810)
```drawlib
from drawlib.canvas import setup
from drawlib.shapes import rectangle
from drawlib.smartarts import Cycle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=115, height=90)

rectangle((57.5, 45.0), width=111, height=86, style=Styles.Neutral.patch(shape_r=2.5))
text((57.5, 83.0), "Defender's 5-Step Iterative Defense Cycle", style=Styles.BlackBold.patch(text_size=14.5))

cycle = Cycle(
    style=Styles.White,
    text_style=Styles.DarkBold.patch(text_size=12.0),
    description_style=Styles.Dark.patch(text_size=10.8),
    arrow_style=Styles.PrimaryBold,
    clockwise=True,
    start_angle=90.0,
    node_shape="rectangle",
    node_width=27.5,
    node_height=14.5,
    arrow_type="arc",
    arrow_width=1.8,
    arrow_head_width=3.8,
    arrow_color_mode="monochrome",
    description_placement="inside",
)

cycle.add(
    "1. Inspect Traffic",
    description="Check leaked origin logs",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=12.0),
    description_style=Styles.White.patch(text_size=10.8),
)
cycle.add(
    "2. Find Commonality",
    description="Extract shared bot tells",
    style=Styles.PrimaryNeutral,
)
cycle.add(
    "3. Design Rule",
    description="Plan zero-FP filter",
    style=Styles.White,
)
cycle.add(
    "4. Apply Setting",
    description="Deploy to WAF / API",
    style=Styles.SecondaryNeutral,
)
cycle.add(
    "5. Measure Effect",
    description="Audit CPU, bill & leaks",
    style=Styles.PrimaryNeutral,
)

cycle.set_center(
    text="Defender",
    description="SRE Loop",
    radius=11.5,
    style=Styles.DarkFlat,
    text_style=Styles.WhiteBold.patch(text_size=13.5),
    description_style=Styles.White.patch(text_size=11.5),
)

cycle.draw(xy=(57.5, 41.0), radius=30.5, align="center")
```
:::

::: block (1720, 995) (140, 30)
```drawlib
import utils
utils.draw_page_number()
```
:::

::: note
Throughout this incident, our defense followed a disciplined 5-step operational cycle:
1. **Inspect Attack Traffic Reaching Origin**: Analyze request logs that bypassed existing filters and hit our Cloud Run instances.
2. **Identify Common Bot Patterns**: Compare malicious requests against legitimate user traffic to find shared attributes (source country, ASN, User-Agent string, request rate, or HTTP protocol version).
3. **Design Blocking Configuration**: Formulate a WAF rule or application challenge that blocks the identified pattern without causing false positives for real Japanese users.
4. **Apply Configuration**: Roll out the rule to production (Cloud Armor, Cloud Run, or Cloudflare WAF).
5. **Measure Effectiveness**: Monitor block rates, container CPU utilization, and billing metrics—and whenever residual attack traffic leaked through, immediately start the next cycle from Step 1.
:::
