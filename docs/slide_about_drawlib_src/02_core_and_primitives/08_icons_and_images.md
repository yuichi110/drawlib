::: block (80, 50) (1760, 120)
# Standardized Icons & Image Processing (`drawlib.icons`, `drawlib.images`)
1,500+ Phosphor vector glyphs, 250+ official GCP cloud icons, and in-memory `Dimage` transformations.
:::

::: block (80, 190) (780, 770) compact
### 1. Dual Icon Engine (`phosphor` & `gcp`)

```python
from drawlib.icons import gcp, phosphor
from drawlib.images import Dimage, image
from drawlib.styles import Styles

# Vector Phosphor icons (5 weights: thin, light, regular, bold, fill)
phosphor.cpu((20, 65), width=12, style=Styles.PrimaryBold)
phosphor.database((45, 65), width=12, style=Styles.PrimaryFlat)

# Official Google Cloud architecture icons (multi-color PNGs)
gcp.compute_engine((20, 40), width=14, style=Styles.Neutral)
gcp.cloud_sql((45, 40), width=14, style=Styles.Neutral)
```

### 2. Bitmap Manipulation with `Dimage`
- Load external `.png`/`.jpg`/`.webp` assets or capture sub-diagrams in memory via `get_dimage_from_code()`.
- Chain non-destructive effects: `.grayscale()`, `.sepia()`, `.invert()`, `.brightness()`, `.blur()`, `.mosaic()`, `.trim()`, and `.make_transparent()`.

```python
image((30, 15), width=16, image="_assets/linux.png")
image((65, 15), width=16, image=Dimage("_assets/linux.png").grayscale())
```
:::

::: block (900, 180) (940, 780)
```drawlib file:icons_showcase.svg
from drawlib.canvas import clear, save, setup
from drawlib.icons import gcp, phosphor
from drawlib.images import Dimage, image
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=100, height=82)

# Row 1: Phosphor Vector Icons (5 Weights & Semantic Colors)
rectangle((50, 68), width=90, height=22, style=Styles.LightFlat.patch(shape_r=2.5))
text((9, 76), "1. Phosphor Vector Icons (1,500+ Icons × 5 Weights)", style=Styles.DarkBold.patch(text_size=9.0, halign="left"))

p_items = [
    (18, phosphor.cloud, Styles.Primary.patch(icon_style="thin"), "thin"),
    (34, phosphor.cpu, Styles.Primary.patch(icon_style="regular"), "regular"),
    (50, phosphor.database, Styles.PrimaryBold, "bold"),
    (66, phosphor.shield_check, Styles.PrimaryFlat, "fill"),
    (82, phosphor.robot, Styles.SecondaryFlat, "robot (fill)"),
]
for cx, fn, st, lbl in p_items:
    fn((cx, 67), width=9.0, style=st)
    text((cx, 59.5), lbl, style=Styles.DarkBold.patch(text_size=7.5))

# Row 2: Official GCP Cloud Icons (250+ Icons)
rectangle((50, 41), width=90, height=22, style=Styles.LightFlat.patch(shape_r=2.5))
text((9, 49), "2. Official Google Cloud Architecture Icons (250+ Icons)", style=Styles.DarkBold.patch(text_size=9.0, halign="left"))

gcp_items = [
    (18, gcp.cloud_load_balancing, "Load Balancing"),
    (39, gcp.google_kubernetes_engine, "GKE Cluster"),
    (61, gcp.cloud_sql, "Cloud SQL"),
    (82, gcp.bigquery, "BigQuery"),
]
for cx, fn, lbl in gcp_items:
    fn((cx, 40), width=10.0, style=Styles.Neutral)
    text((cx, 32.5), lbl, style=Styles.DarkBold.patch(text_size=7.5))

# Row 3: Dimage Raster Processing (_assets/linux.png)
rectangle((50, 14), width=90, height=22, style=Styles.LightFlat.patch(shape_r=2.5))
text((9, 22), "3. Dimage Raster Image Processing (_assets/linux.png)", style=Styles.DarkBold.patch(text_size=9.0, halign="left"))

linux_img = Dimage("_assets/linux.png")
image((24, 13.5), width=10.5, image=linux_img)
text((24, 5.0), "Original", style=Styles.DarkBold.patch(text_size=7.5))

image((50, 13.5), width=10.5, image=linux_img.grayscale())
text((50, 5.0), ".grayscale()", style=Styles.DarkBold.patch(text_size=7.5))

image((76, 13.5), width=10.5, image=linux_img.sepia())
text((76, 5.0), ".sepia()", style=Styles.DarkBold.patch(text_size=7.5))

save()
```
:::

::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils
utils.draw_page_number()
```
:::

::: note
- Standardized icons make technical architectures readable at a glance.
- `drawlib.icons` provides over 1,500 vector `phosphor` icons across 5 typographic weights (`thin`, `light`, `regular`, `bold`, `fill`) and 250+ official `gcp` cloud service icons.
- `drawlib.images` complements vector icons with `image()` and `Dimage`, allowing you to embed bitmap logos and apply transformations like `.grayscale()` and `.sepia()` directly in Python.
:::
