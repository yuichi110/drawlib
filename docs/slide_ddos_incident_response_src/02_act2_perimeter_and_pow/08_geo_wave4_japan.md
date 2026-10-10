::: block (80, 40) (1760, 70)
# Why Geo-Blocking Failed (4/4): Domestic Japanese Proxies
:::

::: block (80, 140) (680, 810)
## Wave 4: Inside the Perimeter

- **100% Domestic Japanese IPs (+4h)**
  Within 4 hours of enabling our Japan-only whitelist, the flood returned at full scale—originating entirely inside Japan.
- **Compromised Home Routers & Proxies**
  Attack traffic routed through domestic consumer fiber ISPs across **Hokkaido, Miyagi, Aichi, Osaka, Hiroshima, and Fukuoka**.
- **Geo-Blocking Defeated**
  Blocking Japanese IPs would lock out our own real users—forcing us to move up to application-layer defenses.
:::

::: block (800, 140) (1040, 810)
```drawlib
from drawlib.canvas import setup
from drawlib.lines import line_curved
from drawlib.shapes import circle, rectangle
from drawlib.smartarts import GeoMap
from drawlib.styles import Styles
from drawlib.text import text

setup(width=115, height=90)

rectangle((57.5, 45.0), width=111, height=86, style=Styles.Neutral.patch(shape_r=2.5))

# 4-Wave Progress Indicator
waves = [
    (19.5, "1. China (0h)", Styles.SecondaryNeutral, Styles.Dark),
    (44.8, "2. Asia (+15m)", Styles.SecondaryNeutral, Styles.Dark),
    (70.2, "3. World (+1h)", Styles.SecondaryNeutral, Styles.Dark),
    (95.5, "4. Japan (+4h)", Styles.AccentFlat, Styles.WhiteBold),
]
for wx, wlabel, bstyle, tstyle in waves:
    rectangle((wx, 81.5), width=23.5, height=7.0, style=bstyle.patch(shape_r=1.5))
    text((wx, 81.5), wlabel, style=tstyle.patch(text_size=11.5))

# Map viewport (Japan 47 Prefectures)
jp = GeoMap(
    GeoMap.Countries.Japan,
    area_style=Styles.White,
    background_style=Styles.PrimaryNeutral.patch(shape_r=1.5),
)
jp.set_area_styles(
    [
        "Hokkaido", "Miyagi", "Niigata", "Saitama", "Chiba",
        "Kanagawa", "Aichi", "Osaka", "Hyogo", "Hiroshima", "Fukuoka",
    ],
    Styles.AccentFlat,
)
jp.set_area_styles(["Tokyo"], Styles.PrimaryFlat)
jp.draw(xy=(6.0, 16.5), width=103.0, height=59.0, lon_range=(122.0, 152.0), lat_range=(29.5, 46.2))

tokyo_xy = jp.get_area_xy("Tokyo")

# Domestic prefecture proxy nodes converging on Tokyo
jp_nodes = [
    ("Hokkaido", 0.22),
    ("Miyagi", 0.20),
    ("Niigata", -0.20),
    ("Aichi", 0.22),
    ("Osaka", 0.24),
    ("Hiroshima", -0.22),
    ("Fukuoka", -0.25),
]
for pref, bend in jp_nodes:
    src_xy = jp.get_area_xy(pref)
    line_curved(src_xy, tokyo_xy, bend=bend, arrow_head="->", style=Styles.AccentBold.patch(line_width=2.3))
    circle(src_xy, radius=1.0, style=Styles.DarkFlat)

circle(tokyo_xy, radius=1.5, style=Styles.PrimaryFlat)

# Callout badges on map
rectangle((31.0, 62.0), width=42.0, height=11.5, style=Styles.DarkFlat.patch(shape_r=1.5))
text((31.0, 64.5), "JP Home Residential ISPs", style=Styles.WhiteBold.patch(text_size=12.0))
text((31.0, 59.3), "Hokkaido / Osaka / Fukuoka / ...", style=Styles.White.patch(text_size=11.0))

rectangle((85.5, 27.5), width=38.0, height=11.5, style=Styles.PrimaryFlat.patch(shape_r=1.5))
text((85.5, 30.0), "Tokyo Origin (Cloud Run)", style=Styles.WhiteBold.patch(text_size=12.0))
text((85.5, 24.8), "Cannot block domestic JP users!", style=Styles.White.patch(text_size=11.0))

# Bottom Status Banner
rectangle((57.5, 9.5), width=103.0, height=8.5, style=Styles.White.patch(shape_r=1.5, shape_line_width=1.5))
text((57.5, 9.5), "Geo-Blocking Defeated: 100% of Attack Now Inside Japanese ISPs!", style=Styles.AccentBold.patch(text_size=13.0))
```
:::

::: block (1720, 995) (140, 30)
```drawlib
import utils
utils.draw_page_number()
```
:::

::: note
Four hours after we locked Cloud Armor down to Japan-only traffic, the attacker completed their geographic adaptation: 100% of the botnet traffic shifted to **domestic Japanese residential proxy nodes** (compromised home routers and residential proxy SDKs on consumer fiber ISPs from Hokkaido to Fukuoka).
Because malicious requests now shared the exact same Japanese ISP networks as our legitimate users, **geographic IP filtering was completely checkmated**. Blocking Japan meant shutting down our service. We had to move up the stack to application-layer challenges.
:::
