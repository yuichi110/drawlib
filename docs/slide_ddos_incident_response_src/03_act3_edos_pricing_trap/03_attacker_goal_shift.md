::: block (80, 40) (1760, 70)
# The Turning Point: How PoW Shifted the Attacker's Goal
:::

::: block (80, 140) (680, 810)
## A Shift in Adversary Objective

- **Before PoW: Focused on Calling TTS API**
  Up to this point, every tactic (4 geo-waves & JS cracking) aimed specifically at calling `POST /synthesize`.
- **SHA-256 PoW Closed the Synthesis Door**
  Requiring 65,000 hashes per call made mass TTS generation computationally infeasible.
- **After PoW: "Just Reach the Origin"**
  No longer fixated on the TTS API, the attacker's new goal became sneaking massive request volume past our defenses to hit the Origin on *any* endpoint.
:::

::: block (800, 140) (1040, 810)
```drawlib
from drawlib.canvas import setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=115, height=90)

rectangle((57.5, 45.0), width=111, height=86, style=Styles.Neutral.patch(shape_r=2.5))
text((57.5, 82.5), "Evolution of the Attacker's Goal: Before vs. After PoW", style=Styles.BlackBold.patch(text_size=14.5))

# Top Panel: Before PoW
rectangle((57.5, 62.0), width=101.0, height=27.0, style=Styles.PrimaryNeutral.patch(shape_r=2.0, shape_line_width=1.4))
text((11.0, 71.8), "BEFORE PoW: Obsessed with Calling the TTS Synthesis API", style=Styles.PrimaryBold.patch(text_size=12.5, halign="left"))

rectangle((23.0, 58.5), width=24.0, height=13.5, style=Styles.White.patch(shape_r=1.5))
phosphor.robot((23.0, 61.5), width=5.5, style=Styles.Dark)
text((23.0, 54.8), "Botnet Swarm", style=Styles.DarkBold.patch(text_size=11.5))

rectangle((57.5, 58.5), width=26.0, height=13.5, style=Styles.White.patch(shape_r=1.5))
text((57.5, 60.5), "Crack JS & Geo", style=Styles.DarkBold.patch(text_size=11.5))
text((57.5, 56.0), "Target specific API", style=Styles.Dark.patch(text_size=10.5))

rectangle((92.0, 58.5), width=26.0, height=13.5, style=Styles.PrimaryFlat.patch(shape_r=1.5))
text((92.0, 60.8), "POST /synthesize", style=Styles.WhiteBold.patch(text_size=11.5))
text((92.0, 56.0), "Goal: Call TTS API", style=Styles.White.patch(text_size=10.5))

line((35.5, 58.5), (44.0, 58.5), arrow_head="->", style=Styles.PrimaryBold)
line((71.0, 58.5), (78.5, 58.5), arrow_head="->", style=Styles.PrimaryBold)

# Center Divider Pill: SHA-256 PoW Trigger
rectangle((57.5, 41.5), width=76.0, height=7.5, style=Styles.DarkFlat.patch(shape_r=1.8))
text((57.5, 41.5), "SHA-256 Proof-of-Work Blocks /synthesize  ->  Goal Pivots!", style=Styles.WhiteBold.patch(text_size=12.0))
line((57.5, 48.0), (57.5, 45.5), arrow_head="->", style=Styles.DarkBold)
line((57.5, 37.5), (57.5, 35.0), arrow_head="->", style=Styles.AccentBold)

# Bottom Panel: After PoW
rectangle((57.5, 20.5), width=101.0, height=27.0, style=Styles.SecondaryNeutral.patch(shape_r=2.0, shape_line_width=1.4))
text((11.0, 30.3), "AFTER PoW: Sneak Massive Traffic Through to Origin (Any Endpoint)", style=Styles.AccentBold.patch(text_size=12.5, halign="left"))

rectangle((23.0, 17.0), width=24.0, height=13.5, style=Styles.White.patch(shape_r=1.5))
phosphor.robot((23.0, 20.0), width=5.5, style=Styles.Accent)
text((23.0, 13.3), "Botnet Swarm", style=Styles.DarkBold.patch(text_size=11.5))

rectangle((57.5, 17.0), width=26.0, height=13.5, style=Styles.White.patch(shape_r=1.5))
text((57.5, 19.0), "Drop TTS Focus", style=Styles.DarkBold.patch(text_size=11.5))
text((57.5, 14.5), "Evade WAF filters", style=Styles.Dark.patch(text_size=10.5))

rectangle((92.0, 17.0), width=26.0, height=13.5, style=Styles.AccentFlat.patch(shape_r=1.5))
text((92.0, 19.3), "Hit Origin (Any URL)", style=Styles.WhiteBold.patch(text_size=11.5))
text((92.0, 14.5), "Goal: Max Penetration", style=Styles.White.patch(text_size=10.5))

line((35.5, 17.0), (44.0, 17.0), arrow_head="->", style=Styles.AccentBold)
line((71.0, 17.0), (78.5, 17.0), arrow_head="->", style=Styles.AccentBold)
```
:::

::: block (1720, 995) (140, 30)
```drawlib
import utils
utils.draw_page_number()
```
:::

::: note
Deploying SHA-256 Proof-of-Work marked the psychological and strategic turning point of the entire incident:
- **Up until PoW (Act 1 & Act 2)**: The attacker was laser-focused on calling our audio synthesis API (`POST /synthesize`) directly—going so far as to rotate through 4 geographic proxy waves and reverse-engineer our obfuscated JavaScript signing logic in 3 hours just to keep invoking TTS synthesis.
- **After PoW (Act 3 onward)**: Once SHA-256 Proof-of-Work made calling `/synthesize` computationally prohibitive, the attacker completely stopped caring about the TTS synthesis API. From this point forward, their sole objective appeared to be **sneaking massive volumes of HTTP requests past our WAF filters so they would reach the Origin—regardless of which endpoint they hit**.
:::
