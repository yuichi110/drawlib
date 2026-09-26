# Drawlib Icons Guidelines

Drawlib provides a comprehensive, production-grade icon rendering system via `drawlib.icons`. Designed to support technical architectures, cloud infrastructure schemas, workflow diagrams, and UI mockups, Drawlib blends vector font glyphs with high-resolution vendor cloud graphics into a unified, code-driven drawing workflow.

---

## 1. Architectural Philosophy & Icon Ecosystem

Icons serve as immediate visual anchors in technical diagrams. A cloud architecture schema without service icons requires excessive reading, whereas an illustration with standardized, crisp icons communicates topology, data flow, and technology stacks at a glance.

Drawlib implements a dual-engine architecture for icon rendering:

```text
┌───────────────────────────────────────────────────────────────────────────────────┐
│                           Public Icon API (drawlib.icons)                         │
│             from drawlib.icons import phosphor, gcp, font_icon                    │
└────────────────────────────────────────┬──────────────────────────────────────────┘
                                         │
                    ┌────────────────────┴────────────────────┐
                    ▼                                         ▼
   ┌─────────────────────────────────┐       ┌─────────────────────────────────┐
   │     Vector Font Icon Engine     │       │     Raster PNG Asset Engine     │
   │  - Phosphor Icons (~1,500 glyphs│       │  - GCP Architecture (250+ icons)│
   │  - FontAwesome (via font_icon)  │       │  - Official vendor multi-color  │
   │  - 5 Weights: thin, light,      │       │  - Auto-caching & lazy download │
   │    regular, bold, fill          │       │  - Full alpha & silhouette mask │
   └────────────────┬────────────────┘       └────────────────┬────────────────┘
                    │                                         │
                    ▼                                         ▼
   ┌─────────────────────────────────┐       ┌─────────────────────────────────┐
   │       Canvas text() Primitive   │       │      Canvas image() Primitive   │
   │  Renders TTF glyph at (x, y)    │       │  Renders RGBA PNG at (x, y)     │
   │  Scales via font_size           │       │  Scales via pixel width         │
   └─────────────────────────────────┘       └─────────────────────────────────┘
```

### 1.1. Vector Font Icons vs. Raster PNG Icons

| Feature | Vector Font Icons (`phosphor`, `font_icon`) | Raster PNG Icons (`gcp`) |
| :--- | :--- | :--- |
| **Underlying Engine** | TrueType Font glyphs via canvas `text()` | High-resolution PNGs via canvas `image()` |
| **Resolution & Scaling**| Infinite vector scalability; razor-sharp at any zoom | Fixed 256x256 pixel assets; optimized for diagrams |
| **Color Rendering** | Monochrome by default; tinted via `text_color` / preset | Official vendor multi-color branding |
| **Weight Variations** | 5 distinct weights (`thin`, `light`, `regular`, `bold`, `fill`) | Single official artwork (weight simulated via borders) |
| **Silhouette Masking** | Native (font glyph color) | Supported via `Style(fill_color=...)` |
| **Asset Storage** | Bundled directly within Python package TTFs | Cached locally under `_assets/`, synced via GitHub |

---

## 2. Imports & Module Structure

All icon functions and modules are imported directly from `drawlib.icons`:

```python
# Primary icon modules and universal function
from drawlib.icons import font_icon, gcp, phosphor

# Supporting styling and color modules
from drawlib.colors import (
    Colors,
    Colors140,
    ColorsDefault,
    ColorsEssentials,
    ColorsMonochrome,
    from_hex,
    with_alpha,
)
from drawlib.types import Style
```

Drawlib also registers submodules in `sys.modules` to support explicit submodule import styles:

```python
import drawlib.icons.gcp as gcp
import drawlib.icons.phosphor as phosphor
```

---

## 3. Phosphor Vector Icons Deep Dive

Phosphor Icons (<https://phosphoricons.com>) is an open-source, highly legible icon family crafted on a uniform 256x256 grid. Drawlib bundles the complete Phosphor library—providing approximately 1,500 distinct icons across 5 distinct typographic weights.

### 3.1. Function Signature & Parameter Contract

Every Phosphor icon is exposed as a Python function directly under the `phosphor` module:

```python
phosphor.<icon_name>(
    xy: tuple[float, float],
    width: float,
    angle: float = 0.0,
    style: Style | str | None = None,
) -> None
```

#### Parameter Breakdown:
- **`xy` (tuple[float, float])**: The center coordinate `(x, y)` where the icon is anchored. By default, alignment is centered (`text_halign="center"`, `text_valign="center"`).
- **`width` (float)**: The horizontal width of the icon in canvas coordinate units. The height scales proportionally to maintain a strict 1:1 square aspect ratio.
- **`angle` (float)**: Counter-clockwise rotation angle in degrees (0.0 to 360.0) around the anchor point `xy`. Default is 0.0.
- **`style` (Style | str | None)**: Predefined style shortcut string (e.g. `"blue"`, `"green_flat"`, `"red_bold"`) or a custom `Style` instance.

### 3.2. The Five Phosphor Weights (`icon_style`)

Phosphor provides 5 visual weights for each icon glyph, controlled via `Style(icon_style="...")`:

```text
┌───────────────┬───────────────────────────┬──────────────────────────────────────────┐
│ Weight Name   │ Visual Characteristic     │ Recommended Diagram Usage                │
├───────────────┼───────────────────────────┼──────────────────────────────────────────┤
│ "thin"        │ Ultra-fine 1px stroke     │ Subtle background indicators, watermarks │
│ "light"       │ Clean, delicate stroke    │ Dense technical schemas, sub-elements    │
│ "regular"     │ Standard balanced stroke  │ General diagram nodes, default icons     │
│ "bold"        │ Heavy, prominent stroke   │ Primary gateways, highlighted nodes      │
│ "fill"        │ Solid filled silhouette   │ Active / selected status, badges, alerts │
└───────────────┴───────────────────────────┴──────────────────────────────────────────┘
```

> **System Default**: If no style is specified, Phosphor icons default to `icon_style="thin"` with `text_color=Colors.Black`.

### 3.3. Code Demonstration of Phosphor Weights

```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.text import text
from drawlib.config import styles

setup(width=120, height=45)

weights = [
    ("thin", styles.primary.patch(icon_style="thin")),
    ("light", styles.primary.patch(icon_style="light")),
    ("regular", styles.primary.patch(icon_style="regular")),
    ("bold", styles.primary.patch(icon_style="bold")),
    ("fill", styles.primary.patch(icon_style="fill")),
]

start_x = 16
pad_x = 22
y_icon = 26
y_text = 10

for i, (name, style_obj) in enumerate(weights):
    x = start_x + pad_x * i
    # Render cloud icon in respective weight
    phosphor.cloud((x, y_icon), width=12, style=style_obj)
    # Render descriptive label underneath
    text((x, y_text), name, size=11, style=styles.charcoal)

save()
```

### 3.4. Preset Style Integration with Phosphor

Phosphor seamlessly maps Drawlib preset styles into appropriate icon weights and colors:

- `<color>`: Maps to icon color (`icon_color`).
- `flat`: Triggers `icon_style="fill"` (solid filled silhouette).
- `light`: Triggers `icon_style="light"`.
- `bold`: Triggers `icon_style="bold"`.

```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.text import text
from drawlib.config import styles

setup(width=100, height=40)

# Colored outline icons
phosphor.shield_check((20, 22), width=10, style=styles.green_bold)
text((20, 9), "green_bold", size=10, style=styles.green)

phosphor.database((50, 22), width=10, style=styles.blue)
text((50, 9), "blue", size=10, style=styles.blue)

# Solid filled silhouette icon using flat preset
phosphor.heart((80, 22), width=10, style=styles.red_flat)
text((80, 9), "red_flat", size=10, style=styles.red)

save()
```

---

## 4. FontAwesome Integration & Custom Font Icons via `font_icon()`

While Phosphor covers general system icons, diagrams frequently require proprietary corporate logos, brand icons (e.g. GitHub, Docker, Slack, AWS), or custom enterprise glyph libraries. Drawlib provides the low-level `font_icon()` primitive for arbitrary TrueType icon fonts.

### 4.1. Function Signature of `font_icon()`

```python
font_icon(
    xy: tuple[float, float],
    width: float,
    code: str,
    file: str,
    angle: float = 0.0,
    style: Style | str | None = None,
) -> None
```

#### Parameter Breakdown:
- **`xy` (tuple[float, float])**: Anchor coordinate `(x, y)` on the canvas.
- **`width` (float)**: Physical width in canvas coordinate units. Internally, `get_fontsize_from_charwidth()` converts this into typographical points.
- **`code` (str)**: Unicode character string or escape code representing the glyph (e.g. `"\uf09b"` for GitHub).
- **`file` (str)**: Path to the `.ttf` font file (relative to working directory or absolute).
- **`angle` (float)**: Rotation angle in degrees (default: 0.0).
- **`style` (Style | str | None)**: Style object or preset name controlling color, alignment, and alpha.

### 4.2. FontAwesome Free Brand & Solid Glyph Example

FontAwesome Free organizes glyphs across distinct font files: `brands.ttf`, `solid.ttf`, and `regular.ttf`.

```python
from drawlib.canvas import save, setup
from drawlib.colors import from_hex
from drawlib.config import styles
from drawlib.icons import font_icon
from drawlib.text import text
from drawlib.types import Style

setup(width=130, height=45)

# FontAwesome Free font file paths
FILE_BRANDS = "fonts/fontawesome-free/brands.ttf"
FILE_SOLID = "fonts/fontawesome-free/solid.ttf"

# Unicode code points
CODE_GITHUB = "\uf09b"
CODE_DOCKER = "\uf395"
CODE_PYTHON = "\uf3e2"
CODE_SERVER = "\uf233"
CODE_TERMINAL = "\uf120"

# Brand colors
COLOR_GITHUB = from_hex("#24292e")
COLOR_DOCKER = from_hex("#2496ed")
COLOR_PYTHON = from_hex("#3776ab")

# Render Brand Icons
font_icon((20, 24), width=11, code=CODE_GITHUB, file=FILE_BRANDS, style=Style(text_color=COLOR_GITHUB))
text((20, 10), "GitHub", size=10, style=Style(text_color=COLOR_GITHUB))

font_icon((45, 24), width=11, code=CODE_DOCKER, file=FILE_BRANDS, style=Style(text_color=COLOR_DOCKER))
text((45, 10), "Docker", size=10, style=Style(text_color=COLOR_DOCKER))

font_icon((70, 24), width=11, code=CODE_PYTHON, file=FILE_BRANDS, style=Style(text_color=COLOR_PYTHON))
text((70, 10), "Python", size=10, style=Style(text_color=COLOR_PYTHON))

# Render Solid Infrastructure Icons
font_icon((95, 24), width=11, code=CODE_SERVER, file=FILE_SOLID, style=styles.charcoal_bold)
text((95, 10), "Server", size=10, style=styles.charcoal)

font_icon((118, 24), width=11, code=CODE_TERMINAL, file=FILE_SOLID, style=styles.green_bold)
text((118, 10), "CLI", size=10, style=styles.green)

save()
```

---

## 5. Google Cloud Platform (GCP) Architecture Icons

Drawlib provides official, publication-quality Google Cloud Platform diagram icons via `drawlib.icons.gcp`. The collection includes more than 250 high-resolution multi-color icons covering all core GCP product categories.

### 5.1. Basic Syntax & Service Invocation

Each GCP service icon is exposed as a standalone function directly under `drawlib.icons.gcp`:

```python
gcp.<service_name>(
    xy: tuple[float, float],
    width: float,
    angle: float = 0.0,
    *,
    style: Style,
) -> None
```

```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.icons import gcp
from drawlib.text import text
from drawlib.config import styles

setup(width=120, height=45)

# Render core compute, storage, container, and database services
gcp.compute_engine((20, 25), width=11, style=styles.primary)
text((20, 11), "Compute Engine", size=9, style=styles.primary)

gcp.google_kubernetes_engine((47, 25), width=11, style=styles.primary)
text((47, 11), "GKE", size=9, style=styles.primary)

gcp.cloud_storage((74, 25), width=11, style=styles.primary)
text((74, 11), "Cloud Storage", size=9, style=styles.primary)

gcp.bigquery((101, 25), width=11, style=styles.primary)
text((101, 11), "BigQuery", size=9, style=styles.primary)

save()
```

### 5.2. Official Service Abbreviation Aliases

To streamline code authoring for common services, Drawlib provides canonical shorthand aliases:

```text
┌──────────────────────────────┬──────────────────────────────┬────────────────────────┐
│ Canonical Service Function   │ Convenient Shorthand Alias   │ Product Area           │
├──────────────────────────────┼──────────────────────────────┼────────────────────────┤
│ gcp.cloud_storage            │ gcp.gcs                      │ Object Storage         │
│ gcp.google_kubernetes_engine │ gcp.gke                      │ Managed Kubernetes     │
│ gcp.compute_engine           │ gcp.gce                      │ Virtual Machines       │
│ gcp.bigquery                 │ gcp.bq                       │ Serverless Analytics   │
└──────────────────────────────┴──────────────────────────────┴────────────────────────┘
```

Both forms are completely identical in execution:

```python
# These pairs invoke the exact same rendering logic
gcp.cloud_storage((30, 20), width=10)
gcp.gcs((30, 20), width=10)

gcp.google_kubernetes_engine((60, 20), width=10)
gcp.gke((60, 20), width=10)
```

### 5.3. Asset Delivery & Automatic Download Pipeline

GCP icons are official 256x256 PNG assets packaged under `RELEASE_ASSET_PACKAGES["icon_gcp"]`. Drawlib manages these assets automatically:

1. **Local Asset Check**: When `gcp.<service>()` is called, `PngIconProvider` checks `drawlib._assets/icons/gcp/<service>.png`.
2. **Developer Workspace Fallback**: If running in developer mode, it checks `release_assets/v0.3/icons/gcp/`.
3. **Automated Lazy Download**: If missing, `ensure_asset_available()` downloads the verified package archive from GitHub Releases and extracts it to the local cache.

---

## 6. Icon Positioning, Scaling, Rotation, and Styling

Drawlib provides fine-grained control over geometry, alignment, alpha transparency, and color tinting across all icon types.

### 6.1. Anchor Alignment System

By default, an icon's center is pinned to `xy`. You can align icons to edges or corners via `Style(text_halign=..., text_valign=...)`:

```text
                      text_valign="top"
             ┌────────────────────────────────┐
             │                                │
text_halign  │       (x, y) Center Anchor     │ text_halign
 ="left"     │  text_halign/valign="center"   │  ="right"
             │                                │
             └────────────────────────────────┘
                    text_valign="bottom"
```

```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.colors import Colors
from drawlib.icons import phosphor
from drawlib.shapes import circle
from drawlib.text import text
from drawlib.types import Style
from drawlib.config import styles

setup(width=100, height=45)

# Center-aligned (default)
phosphor.hard_drives((25, 24), width=12, style=styles.primary)
circle((25, 24), radius=0.6, style=styles.red_flat)
text((25, 9), "center, center", size=9, style=styles.primary)

# Bottom-left aligned: icon expands up and right from (x, y)
align_bl = styles.primary.patch(text_halign="left", text_valign="bottom")
phosphor.hard_drives((65, 18), width=12, style=align_bl)
circle((65, 18), radius=0.6, style=styles.red_flat)
text((71, 9), "left, bottom", size=9, style=styles.primary)

save()
```

### 6.2. Rotation Angle (`angle`)

The `angle` argument rotates the icon counter-clockwise around its anchor point `xy`:

```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.text import text
from drawlib.config import styles

setup(width=120, height=40)

angles = [0, 45, 90, 180, 270]
start_x = 16
pad_x = 22

for i, ang in enumerate(angles):
    x = start_x + pad_x * i
    phosphor.airplane((x, 24), width=11, angle=ang, style=styles.blue_bold)
    text((x, 9), f"{ang}°", size=10, style=styles.charcoal)

save()
```

### 6.3. Color Tinting and Silhouette Masking

Vector icons and raster GCP icons handle color customization differently:

1. **Phosphor Vector Icons**:
   Tinting directly colors the vector glyph via `icon_color` or preset style:
   ```python
   phosphor.database((20, 20), width=10, style=styles.blue)
   phosphor.database((40, 20), width=10, style=styles.primary.patch(icon_color=(200, 50, 50)))
   ```

2. **GCP Multi-Color Icons**:
   - **Default**: Preserves official Google brand colors (Red, Blue, Green, Yellow).
   - **Alpha Transparency (`image_alpha`)**: Fades the entire icon (useful for background or inactive states).
   - **Silhouette Color Mask (`image_tint_color`)**: Replaces the multi-color artwork with a solid flat silhouette mask.
   - **Border Outline (`image_border_color`, `image_border_width`, `image_border_style`)**: Draws an explicit boundary frame around the icon bounding box.

```python
from drawlib.canvas import save, setup
from drawlib.colors import Colors
from drawlib.icons import gcp
from drawlib.text import text
from drawlib.types import Style

setup(width=120, height=45)

# 1. Default multi-color artwork
gcp.cloud_run((18, 25), width=11, style=styles.primary)
text((18, 10), "Default Multi-color", size=8, style=styles.primary)

# 2. Semi-transparent (decommissioned / background service)
gcp.cloud_run((45, 25), width=11, style=styles.primary.patch(image_alpha=0.35))
text((45, 10), "image_alpha=0.35", size=8, style=styles.primary)

# 3. Solid color silhouette mask
gcp.cloud_run((72, 25), width=11, style=styles.primary.patch(image_tint_color=Colors.Red))
text((72, 10), "image_tint_color=Red", size=8, style=styles.primary)

# 4. Outlined boundary box
box_style = styles.primary.patch(image_border_color=Colors.Black, image_border_width=1.0, image_border_style="dashed")
gcp.cloud_run((99, 25), width=11, style=box_style)
text((99, 10), "Framed Box", size=8, style=styles.primary)

save()
```

---

## 7. Combining Icons with Containers, Badges, and Labels

In production cloud architecture schemas and workflow diagrams, icons rarely exist in isolation. They are composed with container cards, status badges, directional lines, and multi-line descriptive text.

### 7.1. Structural Composition Patterns

```text
 ┌────────────────────────────────────────────────────────┐
 │ Container Card (rectangle with r=2, style="silver_flat")│
 │                                                        │
 │        ┌──────────┐                                    │
 │        │   ICON   │    ◄── Icon (e.g. gcp.cloud_run)    │
 │        └────┬─────┘                                    │
 │             │ offset                                   │
 │             ▼                                          │
 │       Primary Label     ◄── Bold text                  │
 │      Secondary Label    ◄── Light gray text            │
 │                                                        │
 └───────────────────────┬────────────────────────────────┘
                         │
                         ▼ Status Badge (circle at corner)
```

### 7.2. Pattern 1: Icon with Standard Bottom Label

To achieve typographical harmony, place the primary label at an offset of `y - (width / 2) - 3.5` from the icon center:

```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.icons import gcp
from drawlib.text import text
from drawlib.config import styles

setup(width=80, height=50)

icon_x, icon_y = 40, 30
icon_w = 12

# 1. Render icon
gcp.google_kubernetes_engine((icon_x, icon_y), width=icon_w, style=styles.primary)

# 2. Render primary and secondary labels
text((icon_x, icon_y - (icon_w / 2) - 4), "GKE Ingress", style=styles.bold, size=10)
text((icon_x, icon_y - (icon_w / 2) - 9), "v1.30 Production", style=styles.charcoal, size=8)

save()
```

### 7.3. Pattern 2: Icon Inside Container Card with Status Badge

```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.icons import gcp, phosphor
from drawlib.shapes import circle, rectangle
from drawlib.text import text
from drawlib.config import styles

setup(width=100, height=60)

card_x, card_y = 50, 30
card_w, card_h = 36, 42

# 1. Card container background
rectangle((card_x, card_y), width=card_w, height=card_h, r=3, style=styles.silver_flat)
rectangle((card_x, card_y), width=card_w, height=card_h, r=3, style=styles.gray_solid)

# 2. Cloud service icon
gcp.compute_engine((card_x, card_y + 6), width=14, style=styles.primary)

# 3. Label block
text((card_x, card_y - 7), "Worker Node 01", style=styles.bold, size=10)
text((card_x, card_y - 13), "n2-standard-4", style=styles.charcoal, size=8)

# 4. Status badge (top-right corner indicator)
badge_x = card_x + (card_w / 2) - 4
badge_y = card_y + (card_h / 2) - 4
circle((badge_x, badge_y), radius=3.2, style=styles.green_flat)
phosphor.check((badge_x, badge_y), width=3.8, style=styles.white_bold)

save()
```

### 7.4. Pattern 3: Numbered Step Badges & Sequential Milestones

When documenting multi-step pipelines or authorization handshakes (e.g. OAuth2, SAML), pair icons with sequentially numbered badges indicating the order of operations:

```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import circle
from drawlib.text import text
from drawlib.config import styles

setup(width=120, height=40)

steps = [
    (1, "Request", phosphor.paper_plane_tilt, 20),
    (2, "Authenticate", phosphor.lock_key, 50),
    (3, "Authorize", phosphor.shield_check, 80),
    (4, "Deliver", phosphor.check_circle, 110),
]

for num, label, icon_fn, x in steps:
    # 1. Main action icon
    icon_fn((x, 22), width=10, style=styles.blue_bold)
    text((x, 9), label, style=styles.charcoal_bold, size=9)

    # 2. Numbered badge at top-left corner of icon
    b_x, b_y = x - 6, 28
    circle((b_x, b_y), radius=2.5, style=styles.teal_flat)
    text((b_x, b_y), str(num), style=styles.white_bold, size=8)

# Connectors between milestones
line((28, 22), (42, 22), arrowhead="->", style=styles.charcoal)
line((58, 22), (72, 22), arrowhead="->", style=styles.charcoal)
line((88, 22), (102, 22), arrowhead="->", style=styles.charcoal)

save()
```

---

## 8. Complete Cloud Architecture Schemas (Production Examples)

The following end-to-end examples demonstrate production architectures combining GCP icons, Phosphor icons, boundary boxes, badges, and connectors.

### 8.1. High-Availability Multi-Tier Web Application on GCP

This architecture features an internet-facing Cloud Armor and Load Balancer tier, scalable Cloud Run microservices, Cloud SQL database storage, Redis caching, and integrated Cloud Monitoring:

```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.colors import Colors, from_hex
from drawlib.icons import gcp, phosphor
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.text import text
from drawlib.types import Style
from drawlib.config import styles

setup(width=150, height=95)

# 1. Diagram Title & Subtitle
text((75, 88), "High-Availability Multi-Tier Web Application on GCP", style=styles.bold, size=17)
text((75, 82), "End-to-End Traffic Routing, Microservices, Caching, and Persistence", style=styles.charcoal, size=10)

# 2. Boundary Containers: GCP Project & VPC Network
rectangle((80, 42), width=130, height=66, r=4, style=styles.blue_dashed)
text((28, 71), "Google Cloud Project (prod-us-central1)", style=styles.blue_bold, size=10)

rectangle((86, 40), width=114, height=54, r=3, style=styles.silver_dashed)
text((42, 63), "Custom VPC Network (10.0.0.0/16)", style=styles.charcoal_bold, size=9)

# 3. Public Internet Tier (Users & CDN)
phosphor.user((14, 45), width=9, style=styles.charcoal_bold)
text((14, 37), "Web Clients", style=styles.bold, size=9)
text((14, 32), "HTTPS / SSL", style=styles.charcoal, size=8)

# 4. Ingress Tier: Cloud Armor & Load Balancing
rectangle((38, 45), width=18, height=30, r=2, style=styles.white_flat)
rectangle((38, 45), width=18, height=30, r=2, style=styles.blue_solid)
gcp.cloud_armor((38, 52), width=8, style=styles.primary)
text((38, 45), "Cloud Armor", size=8, style=styles.bold)
gcp.cloud_load_balancing((38, 35), width=8, style=styles.primary)
text((38, 28), "Global ALB", size=8, style=styles.bold)

# 5. Compute Tier: Cloud Run Service
rectangle((68, 45), width=24, height=34, r=2, style=styles.white_flat)
rectangle((68, 45), width=24, height=34, r=2, style=styles.green_solid)
gcp.cloud_run((68, 52), width=10, style=styles.primary)
text((68, 43), "App Backend", style=styles.green_bold, size=9)
text((68, 38), "Cloud Run", style=styles.charcoal, size=8)
# Replica indicator badge
circle((77, 58), radius=2.5, style=styles.green_flat)
text((77, 58), "x8", style=styles.white_bold, size=7)

# 6. Caching Tier: Memorystore Redis
rectangle((104, 55), width=22, height=22, r=2, style=styles.white_flat)
rectangle((104, 55), width=22, height=22, r=2, style=styles.red_solid)
gcp.memorystore((104, 60), width=8, style=styles.primary)
text((104, 51), "Memorystore", style=styles.bold, size=8)
text((104, 46), "Redis In-Memory", style=styles.charcoal, size=7)

# 7. Database Tier: Cloud SQL HA
rectangle((104, 27), width=22, height=22, r=2, style=styles.white_flat)
rectangle((104, 27), width=22, height=22, r=2, style=styles.blue_solid)
gcp.cloud_sql((104, 32), width=8, style=styles.primary)
text((104, 23), "Cloud SQL", style=styles.bold, size=8)
text((104, 18), "PostgreSQL HA", style=styles.charcoal, size=7)

# 8. Storage & Observability Tier
rectangle((132, 45), width=20, height=34, r=2, style=styles.white_flat)
rectangle((132, 45), width=20, height=34, r=2, style=styles.orange_solid)
gcp.cloud_storage((132, 53), width=8, style=styles.primary)
text((132, 45), "GCS Assets", size=8, style=styles.bold)
gcp.cloud_monitoring((132, 33), width=8, style=styles.primary)
text((132, 25), "Monitoring", size=8, style=styles.bold)

# 9. Inter-service Connectors
line((19, 45), (29, 45), arrowhead="->", style=styles.charcoal_bold)
line((47, 45), (56, 45), arrowhead="->", style=styles.blue_bold)
line((80, 48), (93, 55), arrowhead="<->", style=styles.red_bold)
line((80, 42), (93, 27), arrowhead="<->", style=styles.blue_bold)
line((80, 52), (122, 53), arrowhead="->", style=styles.orange_dashed)

save()
```

### 8.2. Event-Driven Real-Time Data Pipeline

This schema models an IoT ingestion pipeline using Cloud Pub/Sub, stream processing via Cloud Functions, analytical data warehousing in BigQuery, and BI reporting in Looker:

```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.icons import gcp, phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.text import text
from drawlib.config import styles

setup(width=140, height=65)

# Title
text((70, 58), "Event-Driven Serverless Ingestion & Analytics Pipeline", style=styles.bold, size=15)

# Step 1: External IoT Producer
phosphor.cpu((18, 30), width=10, style=styles.orange_bold)
text((18, 19), "IoT Sensors", style=styles.orange_bold, size=9)
text((18, 14), "MQTT Stream", style=styles.charcoal, size=8)

# Step 2: Message Buffer (Pub/Sub)
rectangle((45, 30), width=22, height=28, r=2, style=styles.blue_solid)
gcp.pubsub((45, 36), width=10, style=styles.primary)
text((45, 26), "Cloud Pub/Sub", style=styles.blue_bold, size=9)
text((45, 20), "Buffer Topic", style=styles.charcoal, size=8)

# Step 3: Serverless Worker (Cloud Functions)
rectangle((75, 30), width=22, height=28, r=2, style=styles.green_solid)
gcp.cloud_functions((75, 36), width=10, style=styles.primary)
text((75, 26), "Cloud Functions", style=styles.green_bold, size=9)
text((75, 20), "Transform / Parse", style=styles.charcoal, size=8)

# Step 4: Analytical Data Warehouse (BigQuery)
rectangle((105, 30), width=22, height=28, r=2, style=styles.blue_bold)
gcp.bigquery((105, 36), width=10, style=styles.primary)
text((105, 26), "BigQuery", style=styles.blue_bold, size=9)
text((105, 20), "Partitioned Tables", style=styles.charcoal, size=8)

# Step 5: Dashboard Visualization (Looker)
phosphor.chart_line_up((130, 30), width=10, style=styles.purple_bold)
text((130, 19), "Looker Studio", style=styles.purple_bold, size=9)
text((130, 14), "Real-time BI", style=styles.charcoal, size=8)

# Connectors
line((24, 30), (34, 30), arrowhead="->", style=styles.orange_bold)
line((56, 30), (64, 30), arrowhead="->", style=styles.blue_bold)
line((86, 30), (94, 30), arrowhead="->", style=styles.green_bold)
line((116, 30), (124, 30), arrowhead="->", style=styles.purple_bold)

save()
```

### 8.3. Hybrid Cloud Infrastructure Schema

Demonstrating seamless interoperability between on-premise infrastructure (Phosphor vector servers) and Google Cloud Interconnect:

```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.icons import gcp, phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.text import text
from drawlib.config import styles

setup(width=140, height=60)

# Section Headers
text((70, 54), "Hybrid Enterprise On-Premises to GCP Interconnect", style=styles.bold, size=14)

# On-Premise Datacenter Boundary
rectangle((30, 26), width=44, height=36, r=2, style=styles.charcoal_solid)
text((30, 40), "Corporate On-Premises Datacenter", style=styles.charcoal_bold, size=9)

phosphor.hard_drives((20, 24), width=9, style=styles.charcoal_bold)
text((20, 15), "App Server", size=8, style=styles.primary)

phosphor.database((40, 24), width=9, style=styles.charcoal_bold)
text((40, 15), "Oracle DB", size=8, style=styles.primary)

# Cloud Boundary
rectangle((105, 26), width=50, height=36, r=2, style=styles.blue_dashed)
text((105, 40), "Google Cloud Platform VPC", style=styles.blue_bold, size=9)

gcp.google_kubernetes_engine((95, 24), width=10, style=styles.primary)
text((95, 15), "GKE Cluster", size=8, style=styles.primary)

gcp.cloud_spanner((118, 24), width=10, style=styles.primary)
text((118, 15), "Cloud Spanner", size=8, style=styles.primary)

# Dedicated Cloud Interconnect
rectangle((67, 24), width=14, height=12, r=1, style=styles.teal_flat)
text((67, 26), "Cloud", style=styles.white_bold, size=8)
text((67, 20), "Interconnect", style=styles.white, size=7)

# Connectors
line((52, 24), (60, 24), arrowhead="<->", style=styles.teal_bold)
line((74, 24), (88, 24), arrowhead="<->", style=styles.teal_bold)
line((100, 24), (112, 24), arrowhead="<->", style=styles.blue_bold)

save()
```

### 8.4. Enterprise GitOps & Automated CI/CD Delivery Pipeline

This schema illustrates an automated GitOps delivery workflow from source code commit to container deployment in Google Kubernetes Engine:

```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.icons import gcp, phosphor
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.text import text
from drawlib.config import styles

setup(width=150, height=65)

# Pipeline Title
text((75, 58), "Automated GitOps & CI/CD Delivery Pipeline", style=styles.bold, size=15)

# Stage 1: Developer Workstation
rectangle((20, 28), width=24, height=32, r=2, style=styles.charcoal_solid)
phosphor.laptop((20, 36), width=10, style=styles.charcoal_bold)
text((20, 25), "Developer", style=styles.charcoal_bold, size=9)
text((20, 19), "git push", style=styles.charcoal, size=8)

# Stage 2: Source Repository & Webhook
rectangle((52, 28), width=24, height=32, r=2, style=styles.blue_solid)
phosphor.git_branch((52, 36), width=10, style=styles.blue_bold)
text((52, 25), "Cloud Source", style=styles.blue_bold, size=9)
text((52, 19), "Pull Request", style=styles.charcoal, size=8)

# Stage 3: Build & Automated Testing (Cloud Build)
rectangle((84, 28), width=24, height=32, r=2, style=styles.green_solid)
gcp.cloud_build((84, 36), width=10, style=styles.primary)
text((84, 25), "Cloud Build", style=styles.green_bold, size=9)
text((84, 19), "Unit / Lint / Test", style=styles.charcoal, size=8)

# Stage 4: Artifact Registry (OCI Images)
rectangle((116, 28), width=24, height=32, r=2, style=styles.orange_solid)
gcp.artifact_registry((116, 36), width=10, style=styles.primary)
text((116, 25), "Artifact Reg.", style=styles.orange_bold, size=9)
text((116, 19), "Vulnerability Scan", style=styles.charcoal, size=8)

# Connectors with Pipeline Direction
line((32, 28), (40, 28), arrowhead="->", style=styles.charcoal_bold)
line((64, 28), (72, 28), arrowhead="->", style=styles.blue_bold)
line((96, 28), (104, 28), arrowhead="->", style=styles.green_bold)

# Deployment Badge
circle((124, 38), radius=2.5, style=styles.green_flat)
phosphor.check((124, 38), width=3, style=styles.white_bold)

save()
```

---

## 9. Best Practices, Sizing Guidelines, and Layering Rules

### 9.1. Sizing Guidelines

Maintaining proportional icon sizing across a canvas prevents visual clutter and preserves legibility:

```text
┌────────────────────────────┬─────────────────────────────┬───────────────────────────┐
│ Diagram Role               │ Recommended Width (Units)   │ Example Context           │
├────────────────────────────┼─────────────────────────────┼───────────────────────────┤
│ Primary Gateway / Central  │ 12.0 – 16.0 canvas units    │ Central DB, Main ALB      │
│ Standard Service Node      │ 9.0 – 11.0 canvas units     │ Cloud Run, Compute Engine │
│ Embedded Container Node    │ 7.0 – 8.5 canvas units      │ Subnet instances, Pods    │
│ Status Badge Icon          │ 3.0 – 4.5 canvas units      │ Corner checkmark, warning │
└────────────────────────────┴─────────────────────────────┴───────────────────────────┘
```

### 9.2. Label Placement Formula

To ensure labels never overlap icons or borders, calculate text coordinates relative to icon parameters:

- **Horizontal Anchor**: Keep `x_text = x_icon` with `halign="center"`.
- **Vertical Anchor**:
  - Primary Title: `y_text = y_icon - (width / 2) - 4.0` with `size=9` or `10`.
  - Secondary Subtitle: `y_text_sub = y_text - 5.0` with `size=7` or `8`.
- If an icon is placed inside a container box of height `h`, ensure `h >= width + 18.0` to accommodate padding, the icon, and two lines of text.

### 9.3. Strict Layering Order (Z-Index Rules)

Because Drawlib paints elements sequentially, maintain this execution sequence to prevent connectors or container backgrounds from obscuring icons:

1. **Step 1: Backgrounds & Boundary Cards** (`rectangle()`, VPC boxes, subnets).
2. **Step 2: Connectors & Data Flow Lines** (`line()`, arrows, curved paths).
3. **Step 3: Service & Hardware Icons** (`gcp.*()`, `phosphor.*()`, `font_icon()`).
4. **Step 4: Status Badges & Pin Indicators** (`circle()`, corner badges).
5. **Step 5: Text Labels & Metric Callouts** (`text()`).

---

## 10. Common Pitfalls and Anti-Patterns

### Pitfall 1: Expecting Font Weights on GCP Raster Icons

`icon_style="bold"` and `icon_style="fill"` only apply to vector font icons (`phosphor`, `font_icon`). Applying `icon_style` to a GCP function has no effect because GCP icons are raster PNGs. To emphasize a GCP icon, increase its `width` or frame it in a bold boundary rectangle.

```python
# NO EFFECT: icon_style is ignored for raster PNGs
# gcp.compute_engine((20, 20), width=10, style=Style(icon_style="bold"))

# CORRECT: Increase width or add a styled container
gcp.compute_engine((20, 20), width=14)
```

### Pitfall 2: Rotating Icons Without Offsetting Labels

If an icon is rotated using `angle=90`, its anchor point remains `(x, y)`. If you calculate the label position below `(x, y - 10)` without accounting for the rotation, the visual balance may appear disjointed. If the label itself should not rotate, keep `text()` at `angle=0` and compute offsets carefully.

### Pitfall 3: Asset Missing in Offline / Air-Gapped Environments

GCP icons rely on cached PNG assets downloaded on-demand from GitHub Releases. In air-gapped CI environments without internet access, run asset pre-caching before execution:

```bash
# Developer CLI command to pre-fetch release assets:
./dcli assets sync --tag v0.3
```

### Pitfall 4: Misaligning Icons with `text_halign` and `text_valign`

Unlike shapes which default to `text_halign="center"`, custom icon styles configured with `Style(text_halign="left", text_valign="bottom")` shift the anchor from the icon's center to its lower-left corner. If you connect lines to `(x, y)` assuming it is the center, your arrows will point to the icon's corner instead of its middle.

---

## 11. Comprehensive Icon Catalog Index

### 11.1. Frequently Used Phosphor Icons by Category

```text
Infrastructure & Compute:
  cpu                   hard_drive            hard_drives           server
  desktop               laptop                device_mobile         terminal
  terminal_window       code                  browsers              globe

Cloud & Storage:
  cloud                 cloud_arrow_up        cloud_arrow_down      cloud_check
  database              folder                folder_simple         file
  file_text             file_code             file_csv              archive

Networking & Messaging:
  broadcast             wifi_high             arrows_left_right     git_branch
  git_commit            git_merge             git_pull_request      share_network
  envelope              chat_circle           bell                  rss

Security & Identity:
  lock                  lock_key              shield                shield_check
  shield_warning        key                   fingerprint           user
  users                 user_circle           user_gear             identification_card

Actions & Indicators:
  check                 check_circle          warning               warning_circle
  x                     x_circle              info                  gear
  magnifying_glass      funnel                chart_bar             chart_line_up
```

### 11.2. Major GCP Service Functions by Category

```text
Compute:
  gcp.compute_engine (alias: gce)             gcp.cloud_run
  gcp.google_kubernetes_engine (alias: gke)   gcp.cloud_functions
  gcp.app_engine                              gcp.batch
  gcp.vmware_engine                           gcp.anthos

Storage & Databases:
  gcp.cloud_storage (alias: gcs)              gcp.cloud_sql
  gcp.cloud_spanner                           gcp.bigtable
  gcp.firestore                               gcp.memorystore
  gcp.filestore                               gcp.database_migration_service

Networking:
  gcp.cloud_load_balancing                    gcp.virtual_private_cloud
  gcp.cloud_dns                               gcp.cloud_cdn
  gcp.cloud_nat                               gcp.cloud_interconnect
  gcp.network_connectivity_center             gcp.cloud_router

Big Data & Analytics:
  gcp.bigquery (alias: bq)                    gcp.pubsub
  gcp.dataflow                                gcp.dataproc
  gcp.data_catalog                            gcp.dataplex
  gcp.composer                                gcp.looker

AI & Machine Learning:
  gcp.vertex_ai                               gcp.automl
  gcp.document_ai                             gcp.speech_to_text
  gcp.text_to_speech                          gcp.translation_ai
  gcp.vision_ai                               gcp.contact_center_ai

Security & Operations:
  gcp.cloud_armor                             gcp.cloud_monitoring
  gcp.cloud_logging                           gcp.cloud_trace
  gcp.iam                                     gcp.secret_manager
  gcp.key_management_service                  gcp.security_command_center
```

### 11.3. Quick Reference of Icon Function Arguments

| Argument | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | *(Required)* | Canvas coordinate anchor point `(x, y)`. |
| `width` | `float` | *(Required)* | Icon width in canvas coordinate units. Height preserves 1:1 aspect ratio. |
| `angle` | `float` | `0.0` | Counter-clockwise rotation angle in degrees (0.0 to 360.0). |
| `style` | `Style \| str \| None`| `None` | Style object or preset string (e.g. `"blue"`, `"green_flat"`, `"red_bold"`). |

---

<p align="center"><em>© 2026 drawlib by Yuichi Ito. Released under the Apache 2.0 License.</em></p>
