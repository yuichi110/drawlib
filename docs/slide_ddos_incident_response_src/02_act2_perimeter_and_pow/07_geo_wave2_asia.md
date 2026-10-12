::: block xy=(80, 40) width=1760 height=70
# Why Geo-Blocking Failed (2/4): Regional Shift Across Asia
:::

::: block xy=(80, 140) width=680 height=810
## Wave 2: Neighboring Asian Proxies

- **Instant Regional Failover (+15m)**
  Just 15 minutes after blocking `CN`, the flood resumed at full volume from surrounding Asian countries.
- **APAC Stepping-Stone Swarm**
  Traffic poured in simultaneously from **Korea (`KR`), Taiwan (`TW`), Vietnam (`VN`), Singapore (`SG`), Indonesia (`ID`), Philippines (`PH`), and India (`IN`)**.
- **WAF Rule #2: Block 10+ Asian Regions**
  Expanded the geo-blacklist across APAC—only to trigger a global rotation within 1 hour.
:::

::: block xy=(800, 140) width=1040 height=810
```drawlib
from drawlib.canvas import setup
from drawlib.lines import line_curved
from drawlib.shapes import circle, rectangle
from drawlib.smartarts import ChevronProcess, GeoMap
from drawlib.styles import Styles
from drawlib.text import text

setup(width=115, height=90)

rectangle((57.5, 45.0), width=111, height=86, style=Styles.Neutral.patch(shape_r=2.5))

# 4-Wave Progress Indicator via ChevronProcess
waves = ChevronProcess(
    style=Styles.White,
    text_style=Styles.DarkBold.patch(text_size=12.5),
    description_style=Styles.Dark.patch(text_size=11.0),
    corner_angle=60.0,
    spacing=1.5,
    flat_left_end=True,
)
waves.add("1. China (0h)", style=Styles.SecondaryNeutral)
waves.add("2. Asia (+15m)", style=Styles.AccentFlat, text_style=Styles.WhiteBold.patch(text_size=12.5))
waves.add("3. World (+1h)")
waves.add("4. Japan (+4h)")
waves.draw(xy=(6.0, 77.5), width=103.0, height=7.8)

# Map viewport (East, Southeast & South Asia)
asia = GeoMap(
    GeoMap.World.Asia,
    area_style=Styles.White,
    background_style=Styles.PrimaryNeutral.patch(shape_r=1.5),
)
asia.set_area_styles(["China"], Styles.SecondaryNeutral)
asia.set_area_styles(
    [
        "South Korea", "Taiwan", "Vietnam", "Thailand", "Cambodia",
        "Philippines", "Malaysia", "Indonesia", "India", "Bangladesh",
    ],
    Styles.AccentFlat,
)
asia.set_area_styles(["Japan"], Styles.PrimaryFlat)
asia.draw(xy=(6.0, 16.5), width=103.0, height=58.5, lon_range=(58, 156), lat_range=(-11, 46))

tokyo_xy = asia.lonlat_to_xy(139.69, 35.69)

# Blocked China badge
cn_xy = asia.lonlat_to_xy(101.0, 37.5)
rectangle(cn_xy, width=30.0, height=7.0, style=Styles.DarkFlat.patch(shape_r=1.2))
text(cn_xy, "CN: 403 Blocked", style=Styles.WhiteBold.patch(text_size=12.5))

# Stepping-stone launch points across Asia
asia_nodes = [
    (126.98, 37.57, -0.22),  # Seoul
    (121.56, 25.03, -0.15),  # Taipei
    (105.83, 21.03, 0.14),   # Hanoi
    (100.50, 13.76, 0.16),   # Bangkok
    (120.98, 14.60, 0.20),   # Manila
    (103.82, 1.35, 0.20),    # Singapore
    (106.85, -6.21, 0.24),   # Jakarta
    (77.21, 20.00, 0.22),    # India
]
for lon, lat, bend in asia_nodes:
    src_xy = asia.lonlat_to_xy(lon, lat)
    line_curved(src_xy, tokyo_xy, bend=bend, arrow_head="->", style=Styles.AccentBold.patch(line_width=2.2))
    circle(src_xy, radius=1.0, style=Styles.DarkFlat)

circle(tokyo_xy, radius=1.5, style=Styles.PrimaryFlat)
rectangle((tokyo_xy[0] - 2.0, tokyo_xy[1] + 7.5), width=27.0, height=6.8, style=Styles.PrimaryFlat.patch(shape_r=1.2))
text((tokyo_xy[0] - 2.0, tokyo_xy[1] + 7.5), "Tokyo Origin", style=Styles.WhiteBold.patch(text_size=12.5))

# Bottom Status Banner
rectangle((57.5, 9.5), width=103.0, height=8.5, style=Styles.White.patch(shape_r=1.5, shape_line_width=1.5))
text((57.5, 9.5), "WAF Rule #2: Block 10+ APAC Regions  ->  Bypassed in 1 Hour!", style=Styles.AccentBold.patch(text_size=14.0))
```
:::

::: block xy=(1720, 995) width=140 height=30
```drawlib
import utils
utils.draw_page_number()
```
:::

::: note
Within 15 minutes of blocking China, the attacker's adaptation loop detected our `403` geo-filter and switched proxy pools to neighboring Asian countries.
Requests began pouring in from South Korea, Taiwan, Vietnam, Thailand, the Philippines, Singapore, Indonesia, and India.
We responded by adding more than 10 Asian countries to the Cloud Armor blacklist (WAF Rule #2). That manual whack-a-mole held for less than **1 hour** before the attacker escalated to a worldwide proxy mesh.
:::
