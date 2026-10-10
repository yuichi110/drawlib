::: block (80, 40) (1760, 70)
# Why Geo-Blocking Failed (3/4): Global Proxy Mesh (120+ Countries)
:::

::: block (80, 140) (680, 810)
## Wave 3: Worldwide Escalation

- **120+ Countries Activated (+1h)**
  Once Asian regions were blocked, the botnet unleashed a global residential proxy pool across the Americas, Europe, Africa, and Oceania.
- **Country Blacklisting Exhausted**
  Adding individual countries became futile as traffic arrived from `US`, `BR`, `DE`, `GB`, `TR`, `ZA`, and `AU`.
- **WAF Rule #3: Allow ONLY Japan (`JP`)**
  Inverted our WAF policy to block the entire world outside Japan—buying just 4 hours.
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
    (70.2, "3. World (+1h)", Styles.AccentFlat, Styles.WhiteBold),
    (95.5, "4. Japan (+4h)", Styles.White, Styles.Dark),
]
for wx, wlabel, bstyle, tstyle in waves:
    rectangle((wx, 81.5), width=23.5, height=7.0, style=bstyle.patch(shape_r=1.5))
    text((wx, 81.5), wlabel, style=tstyle.patch(text_size=11.5))

# Map viewport (World)
world = GeoMap(
    GeoMap.World.All,
    area_style=Styles.White,
    background_style=Styles.PrimaryNeutral.patch(shape_r=1.5),
)
world.set_area_styles(
    ["China", "Vietnam", "Thailand", "Indonesia", "India", "Philippines", "Malaysia"],
    Styles.SecondaryNeutral,
)
world.set_area_styles(
    [
        "United States", "Canada", "Mexico", "Brazil", "Argentina",
        "United Kingdom", "Germany", "France", "Spain", "Italy", "Poland",
        "Turkey", "Russia", "Egypt", "Nigeria", "South Africa", "Saudi Arabia", "Australia",
    ],
    Styles.AccentFlat,
)
world.set_area_styles(["Japan"], Styles.PrimaryFlat)
world.draw(xy=(6.0, 16.5), width=103.0, height=59.0, lon_range=(-135, 160), lat_range=(-52, 68))

tokyo_xy = world.lonlat_to_xy(139.69, 35.69)

# Global launch nodes converging on Tokyo
world_nodes = [
    (-98.0, 39.0, -0.22),   # North America (US)
    (-48.0, -18.0, 0.20),   # South America (Brazil)
    (10.0, 50.0, -0.20),    # Europe (Germany/UK/France)
    (35.0, 39.0, -0.14),    # Middle East / Turkey
    (24.0, -28.0, 0.16),    # Southern Africa
    (135.0, -25.0, -0.20),  # Australia
    (95.0, 60.0, -0.16),    # Russia / Northern Eurasia
]
for lon, lat, bend in world_nodes:
    src_xy = world.lonlat_to_xy(lon, lat)
    line_curved(src_xy, tokyo_xy, bend=bend, arrow_head="->", style=Styles.AccentBold.patch(line_width=2.0))
    circle(src_xy, radius=1.0, style=Styles.DarkFlat)

circle(tokyo_xy, radius=1.5, style=Styles.PrimaryFlat)
rectangle((tokyo_xy[0] - 5.5, tokyo_xy[1] - 7.5), width=23.0, height=6.0, style=Styles.PrimaryFlat.patch(shape_r=1.2))
text((tokyo_xy[0] - 5.5, tokyo_xy[1] - 7.5), "Tokyo (JP)", style=Styles.WhiteBold.patch(text_size=11.5))

# Bottom Status Banner
rectangle((57.5, 9.5), width=103.0, height=8.5, style=Styles.White.patch(shape_r=1.5, shape_line_width=1.5))
text((57.5, 9.5), "WAF Rule #3: Allow ONLY Japan (JP)  ->  Bypassed in 4 Hours!", style=Styles.AccentBold.patch(text_size=13.0))
```
:::

::: block (1720, 995) (140, 30)
```drawlib
import utils
utils.draw_page_number()
```
:::

::: note
Within an hour of blocking neighboring Asian countries, the attacker stopped relying on regional pools and activated a global residential proxy mesh across **more than 120 countries**—including the United States, Brazil, Germany, the UK, Turkey, South Africa, and Australia.
At that point, maintaining a country blacklist was impossible. Because our service is a Japanese speech synthesis web app, we flipped our Cloud Armor policy to a strict **Japan-Only Whitelist (`origin.region_code != 'JP' -> 403`)**, blocking the entire rest of the world. That extreme measure held for only **4 hours**.
:::
