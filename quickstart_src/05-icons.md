# 5. Icons & External Images

Drawlib bundles rich icon modules under `drawlib.icons` and provides seamless external image embedding with in-memory transformations via `drawlib.images`.

## 1. Phosphor Icons (`drawlib.icons.phosphor`)

`phosphor` provides ~1,500 scalable vector font icons covering devices, networking, users, arrows, and UI metaphors. Each icon is a Python function accepting `xy`, `width`, `angle`, and `style`:

```drawlib 580px center caption:"Figure 5.1: Vector Icons from drawlib.icons.phosphor"
from drawlib.canvas import setup
from drawlib.icons import phosphor
from drawlib.styles import Styles
from drawlib.text import text

setup(width=100, height=42)

items = [
    (16, phosphor.desktop, "desktop", Styles.Accent),
    (38, phosphor.database, "database", Styles.Secondary),
    (60, phosphor.cloud, "cloud", Styles.Primary),
    (84, phosphor.shield_check, "shield_check", Styles.Success),
]

for x, fn, label, st in items:
    fn(xy=(x, 26), width=11, style=st)
    text(xy=(x, 10), text=f"phosphor.{label}", style=Styles.Primary, size=9)
```

## 2. Google Cloud Platform Icons (`drawlib.icons.gcp`)

`drawlib.icons.gcp` provides 250+ official multi-color Google Cloud service and category icons designed for cloud architecture blueprints:

```drawlib 580px center caption:"Figure 5.2: Official Google Cloud Service Icons from drawlib.icons.gcp"
from drawlib.canvas import setup
from drawlib.icons import gcp
from drawlib.lines import line
from drawlib.styles import Styles
from drawlib.text import text

setup(width=100, height=42)

services = [
    (16, gcp.cloud_load_balancing, "Load Balancing"),
    (40, gcp.cloud_run, "Cloud Run"),
    (64, gcp.cloud_sql, "Cloud SQL"),
    (86, gcp.bigquery, "BigQuery"),
]

for idx, (x, fn, label) in enumerate(services):
    fn(xy=(x, 26), width=11, style=Styles.Primary)
    text(xy=(x, 10), text=label, style=Styles.Primary, size=9)
    if idx < len(services) - 1:
        next_x = services[idx + 1][0]
        line((x + 8, 26), (next_x - 8, 26), arrowhead="->", style=Styles.PrimaryBold)
```

## 3. External Images & Media (`drawlib.images`)

For project logos, team avatars, or hardware badges, Drawlib provides the `image()` function and the `Dimage` utility class from `drawlib.images`. You can render raster images directly from file paths or apply chainable transformations (such as mirroring or sepia filtering):

```drawlib 580px center caption:"Figure 5.3: External Image Embedding and Dimage Transformations"
from drawlib.canvas import setup
from drawlib.images import Dimage, image
from drawlib.styles import Styles
from drawlib.text import text

setup(width=100, height=42)

# 1. Direct file path with border styling
image(
    xy=(20, 24),
    width=16,
    image="_assets/linux.png",
    style=Styles.Primary.patch(image_border_width=1),
)
text(xy=(20, 8), text="image('_assets/linux.png')", style=Styles.Primary, size=8)

# 2. Transformed with Dimage (mirror)
dimg1 = Dimage("_assets/linux.png").mirror()
image(xy=(50, 24), width=16, image=dimg1)
text(xy=(50, 8), text="Dimage.mirror()", style=Styles.Secondary, size=8)

# 3. Transformed with Dimage (sepia)
dimg2 = Dimage("_assets/linux.png").sepia()
image(xy=(80, 24), width=16, image=dimg2)
text(xy=(80, 8), text="Dimage.sepia()", style=Styles.Accent, size=8)
```

