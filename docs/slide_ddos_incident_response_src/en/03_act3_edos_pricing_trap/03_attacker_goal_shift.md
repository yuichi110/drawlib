::: block xy=(80, 40) width=1760 height=70
# The Turning Point: How PoW Shifted the Attacker's Goal
:::

::: block xy=(80, 140) width=680 height=810
## A Shift in Adversary Objective

- **Before PoW: Focused on Calling TTS API**
  Up to this point, every tactic (4 geo-waves & JS cracking) aimed specifically at calling `POST /synthesize`.
- **SHA-256 PoW Closed the Synthesis Door**
  Requiring 65,000 hashes per call made mass TTS generation computationally infeasible.
- **After PoW: "Just Reach the Origin"**
  No longer fixated on the TTS API, the attacker's new goal became sneaking massive request volume past our defenses to hit the Origin on *any* endpoint.
:::

::: block xy=(800, 140) width=1040 height=810
```drawlib
from drawlib.canvas import setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.smartarts import CardList, Panel
from drawlib.styles import Styles
from drawlib.text import text

setup(width=115, height=90)

outer = Panel(
    "Evolution of the Attacker's Goal: Before vs. After PoW",
    style=Styles.Neutral,
    header_style=Styles.PrimaryBold,
    text_style=Styles.BlackBold.patch(text_size=15.5),
    header_variant="underline",
    header_height=9.0,
    header_align="center",
)
outer.draw(xy=(2.0, 2.0), width=111.0, height=86.0)

# Top Panel: Before PoW
p_top = Panel(
    "BEFORE PoW: Obsessed with Calling TTS API (/synthesize)",
    style=Styles.PrimaryNeutral,
    header_style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=13.2),
    icon=phosphor.target,
    icon_style=Styles.White,
    header_variant="filled",
    header_height=7.5,
)
p_top.draw(xy=(6.5, 48.0), width=102.0, height=28.5)
top_xy, top_w, top_h = p_top.get_content_box(xy=(6.5, 48.0), width=102.0, height=28.5, padding=(3.5, 2.5))

cl_top = CardList(
    style=Styles.White,
    text_style=Styles.BlackBold.patch(text_size=13.0),
    description_style=Styles.Dark.patch(text_size=11.8),
    badge_shape="circle",
    badge_style=Styles.PrimaryNeutral,
    icon_style=Styles.PrimaryBold,
    direction="horizontal",
    show_arrows=True,
    arrow_style=Styles.PrimaryBold,
    spacing=4.5,
)
cl_top.add("1. Botnet Swarm", "5,000+ proxy IPs", icon=phosphor.robot)
cl_top.add("2. Crack JS & Geo", "Target specific API", icon=phosphor.key)
cl_top.add(
    "3. POST /synthesize",
    "Goal: Call TTS API",
    icon=phosphor.speaker_high,
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=13.0),
    description_style=Styles.White.patch(text_size=11.8),
    badge_style=Styles.White,
    icon_style=Styles.PrimaryBold,
)
cl_top.draw(top_xy, width=top_w, height=top_h)

# Center Divider Pill: SHA-256 PoW Trigger
rectangle((57.5, 41.2), width=84.0, height=7.2, style=Styles.DarkFlat.patch(shape_r=1.8))
text((57.5, 41.2), "SHA-256 Proof-of-Work Blocks /synthesize  ->  Goal Pivots!", style=Styles.WhiteBold.patch(text_size=13.0))
line((57.5, 47.6), (57.5, 45.0), arrow_head="->", style=Styles.DarkBold)
line((57.5, 37.4), (57.5, 34.8), arrow_head="->", style=Styles.AccentBold)

# Bottom Panel: After PoW
p_bot = Panel(
    "AFTER PoW: Sneak Massive Traffic to Origin (Any Endpoint)",
    style=Styles.SecondaryNeutral,
    header_style=Styles.AccentFlat,
    text_style=Styles.WhiteBold.patch(text_size=13.2),
    icon=phosphor.warning,
    icon_style=Styles.White,
    header_variant="filled",
    header_height=7.5,
)
p_bot.draw(xy=(6.5, 5.5), width=102.0, height=28.5)
bot_xy, bot_w, bot_h = p_bot.get_content_box(xy=(6.5, 5.5), width=102.0, height=28.5, padding=(3.5, 2.5))

cl_bot = CardList(
    style=Styles.White,
    text_style=Styles.BlackBold.patch(text_size=13.0),
    description_style=Styles.Dark.patch(text_size=11.8),
    badge_shape="circle",
    badge_style=Styles.SecondaryNeutral,
    icon_style=Styles.AccentBold,
    direction="horizontal",
    show_arrows=True,
    arrow_style=Styles.AccentBold,
    spacing=4.5,
)
cl_bot.add("1. Botnet Swarm", "300M+ req/day", icon=phosphor.robot)
cl_bot.add("2. Drop TTS Focus", "Evade WAF filters", icon=phosphor.funnel)
cl_bot.add(
    "3. Hit Origin (Any URL)",
    "Goal: Max Penetration",
    icon=phosphor.fire,
    style=Styles.AccentFlat,
    text_style=Styles.WhiteBold.patch(text_size=13.0),
    description_style=Styles.White.patch(text_size=11.8),
    badge_style=Styles.White,
    icon_style=Styles.AccentBold,
)
cl_bot.draw(bot_xy, width=bot_w, height=bot_h)
```
:::

::: block xy=(1720, 995) width=140 height=30
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
