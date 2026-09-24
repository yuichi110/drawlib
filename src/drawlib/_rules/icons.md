# Drawlib Icons Guidelines

Drawlib bundles vector icons from Phosphor and FontAwesome, as well as cloud architecture icons from Google Cloud Platform (GCP).

## 1. Imports
```python
from drawlib.icons import font_awesome, gcp, phosphor
from drawlib.types import Style
```

## 2. Icon Functions & Syntax
Icon drawing functions are named after the icon name in `snake_case`:
- **Phosphor icons**: `phosphor.<icon_name>(xy, width, style=None, angle=0)`
  - Examples: `phosphor.cloud(...)`, `phosphor.database(...)`, `phosphor.gear(...)`, `phosphor.user(...)`
- **FontAwesome icons**: `font_awesome.<icon_name>(xy, width, style=None, angle=0)`
  - Examples: `font_awesome.github(...)`, `font_awesome.server(...)`, `font_awesome.docker(...)`
- **GCP icons**: `gcp.<service_name>(xy, width, angle=0)`
  - Examples: `gcp.compute_engine(...)`, `gcp.cloud_storage(...)`, `gcp.bigquery(...)`

## 3. Styling
- `style`: Can be a preset style string (e.g. `"blue"`, `"green_flat"`, `"red_bold"`) or `Style(line_color=...)`.

## 4. Minimal Example
```python
from drawlib.canvas import config, save
from drawlib.icons import gcp, phosphor
from drawlib.text import text

config(width=100, height=50)
phosphor.cloud((25, 30), width=15, style="blue")
text((25, 15), "API Gateway", size=12)

phosphor.database((75, 30), width=15, style="green")
text((75, 15), "Database", size=12)
save()
```
