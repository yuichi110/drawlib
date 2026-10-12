::: block xy=(80, 40) width=1760 height=70
# Why Geo-Blocking Failed (1/4): Initial Flood from China
:::

::: block xy=(80, 140) width=680 height=810
## Wave 1: Single-Country Origin

- **95%+ Traffic from China (`CN`)**
  Initial Cloud Armor telemetry showed almost the entire cache-busting TTS flood originating from Chinese IP ranges.
- **WAF Rule #1: Block `CN` Region**
  Deployed an edge geo-filter in Cloud Armor to drop all requests from China (`403 Forbidden`).
- **Bypassed in 15 Minutes**
  Attack volume dropped to zero briefly—until the botnet's automated failover shifted proxy regions.
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
waves.add("1. China (0h)", style=Styles.AccentFlat, text_style=Styles.WhiteBold.patch(text_size=12.5))
waves.add("2. Asia (+15m)")
waves.add("3. World (+1h)")
waves.add("4. Japan (+4h)")
waves.draw(xy=(6.0, 77.5), width=103.0, height=7.8)

# Map viewport (East Asia)
asia = GeoMap(
    GeoMap.World.Asia,
    area_style=Styles.White,
    background_style=Styles.PrimaryNeutral.patch(shape_r=1.5),
)
asia.set_area_styles(["China"], Styles.AccentFlat)
asia.set_area_styles(["Japan"], Styles.PrimaryFlat)
asia.draw(xy=(6.0, 16.5), width=103.0, height=58.5, lon_range=(73, 148), lat_range=(16, 53))

tokyo_xy = asia.lonlat_to_xy(139.69, 35.69)

# Attack launch points inside China
cn_nodes = [
    ("Beijing", 116.40, 39.90, -0.18),
    ("Shenyang", 123.43, 41.80, -0.22),
    ("Shanghai", 121.47, 31.23, 0.15),
    ("Guangzhou", 113.26, 23.13, 0.22),
    ("Chengdu", 104.06, 30.67, -0.12),
]
for _, lon, lat, bend in cn_nodes:
    src_xy = asia.lonlat_to_xy(lon, lat)
    line_curved(src_xy, tokyo_xy, bend=bend, arrow_head="->", style=Styles.AccentBold.patch(line_width=2.4))
    circle(src_xy, radius=1.1, style=Styles.DarkFlat)

circle(tokyo_xy, radius=1.5, style=Styles.PrimaryFlat)

cn_center = asia.lonlat_to_xy(103.0, 36.5)
rectangle((cn_center[0] - 4.0, cn_center[1]), width=34.0, height=7.5, style=Styles.DarkFlat.patch(shape_r=1.2))
text((cn_center[0] - 4.0, cn_center[1]), "China Botnet (95%)", style=Styles.WhiteBold.patch(text_size=13.0))

rectangle((tokyo_xy[0] - 5.0, tokyo_xy[1] + 9.0), width=28.0, height=7.0, style=Styles.PrimaryFlat.patch(shape_r=1.2))
text((tokyo_xy[0] - 5.0, tokyo_xy[1] + 9.0), "Tokyo Origin", style=Styles.WhiteBold.patch(text_size=12.5))

# Bottom Status Banner
rectangle((57.5, 9.5), width=103.0, height=8.5, style=Styles.White.patch(shape_r=1.5, shape_line_width=1.5))
text((57.5, 9.5), "WAF Rule #1: Block China (CN)  ->  Bypassed in 15 Minutes!", style=Styles.AccentBold.patch(text_size=14.0))
```
:::

::: block xy=(1720, 995) width=140 height=30
```drawlib
import utils
utils.draw_page_number()
```
:::

::: note
When we first inspected Cloud Armor telemetry using our 5-step defense cycle, the pattern looked obvious: over 95% of the malicious TTS synthesis requests were coming from IP addresses in China (`CN`).
Since our service is a Japanese text-to-speech tool aimed at domestic users, blocking China at the Cloud Armor edge seemed like an easy win.
We deployed WAF Rule #1 (`origin.region_code == 'CN' -> 403 Forbidden`), and attack traffic immediately dropped to zero. However, the relief lasted only **15 minutes** before the attacker's adaptation loop routed around our block.
:::
