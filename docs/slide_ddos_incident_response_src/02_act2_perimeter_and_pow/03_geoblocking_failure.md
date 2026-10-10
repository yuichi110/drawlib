::: block (80, 40) (1760, 70)
# Why Geo-Blocking Failed: The Proxy Whack-a-Mole
:::

::: block (80, 130) (1760, 170)
- **Initial Hypothesis**: Since our TTS service targets Japanese users, blocking overseas attack origins in Cloud Armor should stop the flood.
- **Reality**: Within **24 hours**, the botnet hopped across **4 proxy waves**, ending inside **Japanese domestic residential ISPs** where geo-blocking is useless.
:::

::: block (80, 320) (1760, 630)
```drawlib
from drawlib.canvas import setup
from drawlib.icons import phosphor
from drawlib.shapes import rectangle
from drawlib.smartarts import ChevronProcess
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=176, height=63)

rectangle((88.0, 31.5), width=172, height=59, style=Styles.Neutral.patch(shape_r=2.5))
text((88.0, 56.0), "24-Hour Geographic Proxy Escalation Timeline", style=Styles.BlackBold.patch(text_size=12.5))

# Top Chevron Process across the 4 waves
waves = ChevronProcess(
    style=Styles.PrimaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=10.5),
    description_style=Styles.Dark.patch(text_size=9.5),
    corner_angle=60.0,
    spacing=2.0,
    flat_left_end=True,
)
waves.add("Wave 1: Single Region", description="95% China (CN) IPs")
waves.add("Wave 2: Regional Shift", description="SG / VN / ID / BR / US")
waves.add("Wave 3: Global Mesh", description="120+ Countries (JP-Only Rule)", style=Styles.SecondaryNeutral)
waves.add(
    "Wave 4: Domestic JP",
    description="JP Residential ISPs + Cloud",
    style=Styles.AccentFlat,
    text_style=Styles.WhiteBold.patch(text_size=10.5),
    description_style=Styles.White.patch(text_size=9.5),
)
waves.draw(xy=(8.0, 35.0), width=160.0, height=16.0)

# Bottom 4 Detail Cards aligned under each chevron stage
cards = [
    (27.0, "WAF Rule #1", "Block CN Region", "Bypassed in 15 mins", phosphor.globe_hemisphere_east, Styles.White, Styles.Primary),
    (67.5, "WAF Rule #2", "Block 10+ Countries", "Bypassed in 1 hour", phosphor.arrows_split, Styles.White, Styles.Primary),
    (108.0, "WAF Rule #3", "Allow ONLY Japan (JP)", "Bypassed in 4 hours", phosphor.shield_warning, Styles.White, Styles.Accent),
    (148.5, "Geo-Block Defeated", "Attacker inside JP ISPs!", "Cannot block own users", phosphor.warning_octagon, Styles.SecondaryNeutral, Styles.Accent),
]

for cx, title_str, action_str, result_str, icon_fn, card_st, icon_st in cards:
    rectangle((cx, 17.5), width=37.0, height=26.0, style=card_st.patch(shape_r=2.0))
    icon_fn((cx, 25.0), width=5.5, style=icon_st)
    text((cx, 18.5), title_str, style=Styles.BlackBold.patch(text_size=10.5))
    text((cx, 13.5), action_str, style=Styles.Dark.patch(text_size=9.5))
    text((cx, 8.5), result_str, style=Styles.AccentBold.patch(text_size=9.5))
```
:::

::: block (1720, 995) (140, 30)
```drawlib
import utils
utils.draw_page_number()
```
:::

::: note
Our first Cloud Armor rules relied on geographic IP filtering (`origin.region_code`), which triggered an immediate cat-and-mouse escalation:
- **Wave 1 (Single Country)**: Initially, 95% of attack requests originated from China (`CN`). We deployed a Cloud Armor rule blocking `CN`. Traffic dropped to zero—for exactly 15 minutes.
- **Wave 2 (Regional Expansion)**: The flood resumed at identical volume from Singapore (`SG`), Vietnam (`VN`), Indonesia (`ID`), Brazil (`BR`), and the US.
- **Wave 3 (The "Japan-Only" Nuclear Option)**: Rather than playing country whack-a-mole across 120+ countries, we inverted the rule to **Allow ONLY `JP` (`origin.region_code == 'JP'`)** and block the rest of the world.
- **Wave 4 (Domestic Proxy Infiltration)**: Within 4 hours, the attacker routed traffic through **Japanese domestic residential proxies** (hijacked home routers/PCs on major Japanese fiber ISPs) and Tokyo cloud regions. At that point, country-level geo-blocking became completely useless without blocking our own Japanese user base.
:::
