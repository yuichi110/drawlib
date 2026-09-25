# 5. Icons: Phosphor & Google Cloud (GCP)

Drawlib bundles rich icon modules under `drawlib.icons` so you can build expressive system architecture diagrams without hunting for external image assets.

## 1. Phosphor Icons (`drawlib.icons.phosphor`)

`phosphor` provides ~1,500 scalable vector font icons covering devices, networking, users, arrows, and UI metaphors. Each icon is a Python function accepting `xy`, `width`, `angle`, and `style`:

```drawlib 580px center caption:"Figure 5.1: Vector Icons from drawlib.icons.phosphor"
from drawlib.canvas import config
from drawlib.icons import phosphor
from drawlib.text import text

config(width=100, height=42)

items = [
    (16, phosphor.desktop, "desktop", styles.blue),
    (38, phosphor.database, "database", styles.green),
    (60, phosphor.cloud, "cloud", styles.blue),
    (84, phosphor.shield_check, "shield_check", styles.red),
]

for x, fn, label, st in items:
    fn(xy=(x, 26), width=11, style=st)
    text(xy=(x, 10), text=f"phosphor.{label}", style=styles.primary, size=9)
```

## 2. Google Cloud Platform Icons (`drawlib.icons.gcp`)

`drawlib.icons.gcp` provides 250+ official multi-color Google Cloud service and category icons designed for cloud architecture blueprints:

```drawlib 580px center caption:"Figure 5.2: Official Google Cloud Service Icons from drawlib.icons.gcp"
from drawlib.canvas import config
from drawlib.icons import gcp
from drawlib.lines import line
from drawlib.text import text

config(width=100, height=42)

services = [
    (16, gcp.cloud_load_balancing, "Load Balancing"),
    (40, gcp.cloud_run, "Cloud Run"),
    (64, gcp.cloud_sql, "Cloud SQL"),
    (86, gcp.bigquery, "BigQuery"),
]

for idx, (x, fn, label) in enumerate(services):
    fn(xy=(x, 26), width=11, style=styles.primary)
    text(xy=(x, 10), text=label, style=styles.primary, size=9)
    if idx < len(services) - 1:
        next_x = services[idx + 1][0]
        line((x + 8, 26), (next_x - 8, 26), arrowhead="->", style=styles.blue)
```
