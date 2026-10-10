::: block (80, 40) (1760, 70)
# Threat Actor Profile: Anatomy of an AI-Assisted Adversary
:::

::: block (80, 140) (680, 810)
## Behavioral Forensics

- **LLM-Speed Adaptation (<3 Hours)**
  De-obfuscated our custom frontend JS bundle and replicated HMAC signing in under 180 minutes.
- **Automated Threshold Probing**
  Tuned 5,000+ nodes to `6–8 req/10s` to stay just beneath our `10 req/10s` WAF rule.
- **Persistent Multi-Week Testing**
  Used our live production endpoint as a continuous adversarial training sandbox.
:::

::: block (800, 140) (1040, 810)
```drawlib
from drawlib.canvas import setup
from drawlib.shapes import rectangle
from drawlib.smartarts import Cycle
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=115, height=90)

rectangle((57.5, 45.0), width=111, height=86, style=Styles.Neutral.patch(shape_r=2.5))
text((57.5, 83.5), "Closed-Loop Adaptation Cycle of an AI-Orchestrated Botnet", style=Styles.BlackBold.patch(text_size=12.0))

cycle = Cycle(
    style=Styles.White,
    text_style=Styles.DarkBold.patch(text_size=9.5),
    description_style=Styles.Dark.patch(text_size=9.5),
    arrow_style=Styles.PrimaryBold,
    clockwise=True,
    start_angle=90.0,
    node_shape="rectangle",
    node_size=(26.0, 13.0),
    arrow_type="arc",
    arrow_width=1.8,
    arrow_head_width=4.0,
    arrow_color_mode="monochrome",
    description_placement="inside",
)

cycle.add(
    "1. AI Recon Agent",
    description="Detect 403 / WAF rule",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=9.5),
    description_style=Styles.White.patch(text_size=9.5),
)
cycle.add(
    "2. JS AST Parser",
    description="LLM de-obfuscates JS",
    style=Styles.PrimaryNeutral,
)
cycle.add(
    "3. Proxy Rotation",
    description="Hop CN -> Global -> JP",
    style=Styles.SecondaryNeutral,
)
cycle.add(
    "4. Sub-Limit Tuning",
    description="Throttle to 8 req/10s",
    style=Styles.PrimaryNeutral,
)
cycle.add(
    "5. EDoS Pivot",
    description="300M/day billing flood",
    style=Styles.AccentFlat,
    text_style=Styles.WhiteBold.patch(text_size=9.5),
    description_style=Styles.White.patch(text_size=9.5),
)

cycle.set_center(
    text="AI Botnet",
    description="Controller",
    radius=12.5,
    style=Styles.DarkFlat,
    text_style=Styles.WhiteBold.patch(text_size=11.0),
    description_style=Styles.White.patch(text_size=9.5),
)

cycle.draw(xy=(57.5, 42.0), radius=27.5, align="center")
```
:::

::: block (1720, 995) (140, 30)
```drawlib
import utils
utils.draw_page_number()
```
:::

::: note
Why would a sophisticated threat actor spend weeks attacking a $10/month hobby speech synthesis service with zero monetizable user data?
- **AI-Assisted Reverse Engineering**: The 3-hour turnaround between deploying our obfuscated JS signature and the botnet replicating the exact signing algorithm strongly points to an **LLM-assisted coding workflow** (feeding minified JS bundles into an LLM to generate Python/Go request signers).
- **Automated Rate-Limit Probing**: Whenever we adjusted per-IP rate limits, the swarm automatically binary-searched the exact threshold and dialed per-node request rates just underneath it.
- **Production as an Adversarial Sandbox**: Modern botnet operators and AI security researchers routinely use real-world public APIs as live proving grounds to test residential proxy rotation and WAF evasion frameworks before attacking high-value commercial targets.
:::
