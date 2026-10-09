# 6. Standardized Icons & Media Assets

Diagrams communicate faster when accompanied by standard iconography and project logos. Drawlib bundles extensive vector icon packages under `drawlib.icons` and provides chainable image transformations via `drawlib.images`.

## Phosphor Vector Icons (`drawlib.icons.phosphor`)

`drawlib.icons.phosphor` provides ~1,500 scalable vector icons covering computing, networking, devices, users, interfaces, and tools:

Every icon is a pure Python function accepting `xy`, `width`, and `style` (including `style.angle` for rotation):

```drawlib 620px center file:icons_phosphor.png caption:"Figure 6.1: Vector Iconography from Phosphor"
from drawlib.canvas import setup
from drawlib.icons import phosphor
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=120, height=44)

icons_list = [
    (15, phosphor.desktop, "phosphor.desktop", Styles.PrimaryFlat),
    (38, phosphor.database, "phosphor.database", Styles.SecondaryFlat),
    (61, phosphor.cloud, "phosphor.cloud", Styles.AccentFlat),
    (84, phosphor.shield_check, "phosphor.shield", Styles.DangerFlat),
    (107, phosphor.lock_key, "phosphor.lock", Styles.SuccessFlat),
]

for x, fn, label, st in icons_list:
    rectangle(xy=(x, 22), width=20, height=36, r=2, style=Styles.MutedDashed)
    fn(xy=(x, 28), width=10, style=st)
    text(xy=(x, 10), text=label, style=Styles.PrimaryBold.patch(text_size=7.5))
```

## Google Cloud Architecture Icons (`drawlib.icons.gcp`)

For cloud infrastructure and microservice topologies, Drawlib includes 250+ official Google Cloud icons:

```drawlib 620px center file:icons_gcp.png caption:"Figure 6.2: Official Google Cloud Service Architecture Icons"
from drawlib.canvas import setup
from drawlib.icons import gcp
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=120, height=44)

services = [
    (18, gcp.cloud_load_balancing, "Cloud Load Balancing"),
    (46, gcp.cloud_run, "Cloud Run"),
    (74, gcp.cloud_sql, "Cloud SQL"),
    (102, gcp.bigquery, "BigQuery"),
]

for idx, (x, icon_fn, label) in enumerate(services):
    rectangle(xy=(x, 22), width=24, height=36, r=2, style=Styles.MutedDashed)
    icon_fn(xy=(x, 28), width=10, style=Styles.Primary)
    text(xy=(x, 10), text=label, style=Styles.DarkBold.patch(text_size=8))
    if idx < len(services) - 1:
        next_x = services[idx + 1][0]
        line((x + 12, 28), (next_x - 12, 28), arrow_head="->", style=Styles.DarkBold)
```

## External Media & In-Memory Images (`drawlib.images`)

Embed external PNG, WebP, or JPEG images with the `image()` function or transform them via `Dimage`:

- **`image(xy, width, image=path_or_dimage, style=...)`**: Embeds raster images with optional border styles.
- **`Dimage(path)`**: In-memory image representation supporting chainable operations (`.mirror()`, `.sepia()`, `.crop()`).

```python
from drawlib.images import Dimage, image
from drawlib.styles import Styles

# Load external logo, apply horizontal mirror, and render to canvas
mirrored_logo = Dimage("_assets/linux.png").mirror()
image(xy=(50, 30), width=20, image=mirrored_logo, style=Styles.PrimaryOutline)
```
