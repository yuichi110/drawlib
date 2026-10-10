::: block (80, 40) (1760, 70)
# The Attacker's Cycle: 5-Step Probing & WAF Inference
:::

::: block (80, 140) (680, 810)
## Assumed Adversary Loop

- **Flow Analysis & Vector Selection (Steps 1–2)**
  Analyze legitimate user access flows and select an attack method with minimal bot cost and maximum target CPU or billing damage.
- **Parallel Probing & Rule Inference (Steps 3–4)**
  Test multiple attack patterns in parallel and compare passed (`200`) vs. blocked (`403`/`429`) responses to infer WAF rules.
- **Blind-Spot Concentration (Step 5)**
  Once the unblocked weak spot is found, concentrate all botnet traffic onto that pattern—and repeat when blocked.
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
text((57.5, 83.0), "Assumed Attacker's 5-Step Adaptation Cycle", style=Styles.BlackBold.patch(text_size=14.5))

cycle = Cycle(
    style=Styles.White,
    text_style=Styles.DarkBold.patch(text_size=12.0),
    description_style=Styles.Dark.patch(text_size=10.8),
    arrow_style=Styles.AccentBold,
    clockwise=True,
    start_angle=90.0,
    node_shape="rectangle",
    node_size=(27.5, 14.5),
    arrow_type="arc",
    arrow_width=1.8,
    arrow_head_width=3.8,
    arrow_color_mode="monochrome",
    description_placement="inside",
)

cycle.add(
    "1. Analyze User Flow",
    description="Map normal site & API flow",
    style=Styles.SecondaryNeutral,
)
cycle.add(
    "2. Pick High-ROI Vector",
    description="Low cost, max target damage",
    style=Styles.PrimaryNeutral,
)
cycle.add(
    "3. Parallel Probing",
    description="Test multi-patterns at once",
    style=Styles.White,
)
cycle.add(
    "4. Infer WAF Rules",
    description="Compare 200 vs 403/429",
    style=Styles.SecondaryNeutral,
)
cycle.add(
    "5. Hit Weak Point",
    description="Focus full flood on gap",
    style=Styles.AccentFlat,
    text_style=Styles.WhiteBold.patch(text_size=12.0),
    description_style=Styles.White.patch(text_size=10.8),
)

cycle.set_center(
    text="Attacker",
    description="Botnet Loop",
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
Why did simple single-layer defenses fail so quickly? Because the attacker was executing a parallel 5-step adaptation cycle of their own:
1. **Analyze Legitimate User Flow**: Inspect our web app, JavaScript bundles, and API endpoints to understand how real users request audio synthesis.
2. **Select Low-Cost, High-Damage Vector**: Choose attack patterns that cost the botnet almost nothing to send while maximizing our CPU load (cache-busting TTS parameters) or cloud bill (300M/day EDoS requests).
3. **Launch Parallel Multi-Pattern Probes**: Test diverse combinations of proxy countries, request rates, and headers simultaneously.
4. **Infer WAF Rules via Response Comparison**: Compare which probe patterns succeeded (`200 OK`) versus which were rejected (`403 Forbidden` or `429 Too Many Requests`) to reverse-engineer our exact WAF rules and rate-limit thresholds.
5. **Concentrate Fire on the Weak Point**: Shift the entire botnet swarm into the unblocked pattern—and whenever we closed that gap, loop back to find the next blind spot.
:::
