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
| **Silhouette Masking** | Native (font glyph color) | Supported via `Style(icon_color=...)` |
| **Asset Storage** | Bundled directly within Python package TTFs | Cached locally under `_assets/`, synced via GitHub |

---

## 2. Imports & Module Structure

All icon functions and modules are imported directly from `drawlib.icons`:

```python
# Primary icon modules and universal function
from drawlib.icons import font_icon, gcp, phosphor

# Supporting styling and color modules
from drawlib.preset_colors import (
    Color,
    CssColors,
    DefaultColors,
    GoogleColors,
    MonochromeColors,
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
    *,
    style: Style,
) -> None
```

#### Parameter Breakdown:
- **`xy` (tuple[float, float])**: The center coordinate `(x, y)` where the icon is anchored. By default, alignment is centered.
- **`width` (float)**: The horizontal width of the icon in canvas coordinate units. The height scales proportionally to maintain a strict 1:1 square aspect ratio.
- **`angle` (float)**: Counter-clockwise rotation angle in degrees (0.0 to 360.0) around the anchor point `xy`. Default is 0.0.
- **`style` (Style)**: Active `Style` instance (e.g. `Styles.Primary`, `Styles.PrimaryBold`, or custom `Style(icon_color=...)`). Required keyword-only argument.

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
from drawlib.styles import Styles

setup(width=120, height=45)

weights = [
    ("thin", Styles.Primary.patch(icon_style="thin")),
    ("light", Styles.Primary.patch(icon_style="light")),
    ("regular", Styles.Primary.patch(icon_style="regular")),
    ("bold", Styles.Primary.patch(icon_style="bold")),
    ("fill", Styles.Primary.patch(icon_style="fill")),
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
    text((x, y_text), name, style=Styles.Dark.patch(text_size=11))

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
from drawlib.styles import Styles

setup(width=100, height=40)

# Colored outline icons
phosphor.shield_check((20, 22), width=10, style=Styles.GreenBold)
text((20, 9), "GreenBold", style=Styles.Green.patch(text_size=10))

phosphor.database((50, 22), width=10, style=Styles.Blue)
text((50, 9), "Blue", style=Styles.Blue.patch(text_size=10))

# Solid filled silhouette icon using flat preset
phosphor.heart((80, 22), width=10, style=Styles.RedFlat)
text((80, 9), "RedFlat", style=Styles.Red.patch(text_size=10))

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
from drawlib.preset_colors import Color
from drawlib.styles import Styles
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
COLOR_GITHUB = Color.from_hex("#24292e")
COLOR_DOCKER = Color.from_hex("#2496ed")
COLOR_PYTHON = Color.from_hex("#3776ab")

# Render Brand Icons
font_icon((20, 24), width=11, code=CODE_GITHUB, file=FILE_BRANDS, style=Style(icon_color=COLOR_GITHUB))
text((20, 10), "GitHub", style=Styles.Primary.patch(text_color=COLOR_GITHUB, text_size=10))

font_icon((45, 24), width=11, code=CODE_DOCKER, file=FILE_BRANDS, style=Style(icon_color=COLOR_DOCKER))
text((45, 10), "Docker", style=Styles.Primary.patch(text_color=COLOR_DOCKER, text_size=10))

font_icon((70, 24), width=11, code=CODE_PYTHON, file=FILE_BRANDS, style=Style(icon_color=COLOR_PYTHON))
text((70, 10), "Python", style=Styles.Primary.patch(text_color=COLOR_PYTHON, text_size=10))

# Render Solid Infrastructure Icons
font_icon((95, 24), width=11, code=CODE_SERVER, file=FILE_SOLID, style=Styles.PrimaryBold)
text((95, 10), "Server", style=Styles.Primary.patch(text_size=10))

font_icon((118, 24), width=11, code=CODE_TERMINAL, file=FILE_SOLID, style=Styles.SuccessBold)
text((118, 10), "CLI", style=Styles.Success.patch(text_size=10))

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
from drawlib.styles import Styles

setup(width=120, height=45)

# Render core compute, storage, container, and database services
gcp.compute_engine((20, 25), width=11, style=Styles.Primary)
text((20, 11), "Compute Engine", style=Styles.Primary.patch(text_size=9))

gcp.google_kubernetes_engine((47, 25), width=11, style=Styles.Primary)
text((47, 11), "GKE", style=Styles.Primary.patch(text_size=9))

gcp.cloud_storage((74, 25), width=11, style=Styles.Primary)
text((74, 11), "Cloud Storage", style=Styles.Primary.patch(text_size=9))

gcp.bigquery((101, 25), width=11, style=Styles.Primary)
text((101, 11), "BigQuery", style=Styles.Primary.patch(text_size=9))

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
from drawlib.icons import phosphor
from drawlib.shapes import circle
from drawlib.text import text
from drawlib.types import Style
from drawlib.styles import Styles

setup(width=100, height=45)

# Center-aligned (default)
phosphor.hard_drives((25, 24), width=12, style=Styles.Primary)
circle((25, 24), radius=0.6, style=Styles.RedFlat)
text((25, 9), "center, center", style=Styles.Primary.patch(text_size=9))

# Bottom-left aligned: icon expands up and right from (x, y)
align_bl = Styles.Primary.patch(text_halign="left", text_valign="bottom")
phosphor.hard_drives((65, 18), width=12, style=align_bl)
circle((65, 18), radius=0.6, style=Styles.RedFlat)
text((71, 9), "left, bottom", style=Styles.Primary.patch(text_size=9))

save()
```

### 6.2. Rotation Angle (`angle`)

The `angle` argument rotates the icon counter-clockwise around its anchor point `xy`:

```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.text import text
from drawlib.styles import Styles

setup(width=120, height=40)

angles = [0, 45, 90, 180, 270]
start_x = 16
pad_x = 22

for i, ang in enumerate(angles):
    x = start_x + pad_x * i
    phosphor.airplane((x, 24), width=11, angle=ang, style=Styles.BlueBold)
    text((x, 9), f"{ang}°", style=Styles.Dark.patch(text_size=10))

save()
```

### 6.3. Color Tinting and Silhouette Masking

Vector icons and raster GCP icons handle color customization differently:

1. **Phosphor Vector Icons**:
   Tinting directly colors the vector glyph via `icon_color` or preset style:
   ```python
   phosphor.database((20, 20), width=10, style=Styles.Blue)
   phosphor.database((40, 20), width=10, style=Styles.Primary.patch(icon_color=(200, 50, 50)))
   ```

2. **GCP Multi-Color Icons**:
   - **Default**: Preserves official Google brand colors (Red, Blue, Green, Yellow).
   - **Alpha Transparency (`image_alpha`)**: Fades the entire icon (useful for background or inactive states).
   - **Silhouette Color Mask (`image_tint_color`)**: Replaces the multi-color artwork with a solid flat silhouette mask.
   - **Border Outline (`image_border_color`, `image_border_width`, `image_border_style`)**: Draws an explicit boundary frame around the icon bounding box.

```drawlib show-code file:icons_gcp_styling.png
from drawlib.canvas import save, setup
from drawlib.icons import gcp
from drawlib.styles import Colors, Styles
from drawlib.text import text
from drawlib.types import Style

setup(width=120, height=45)

# 1. Default multi-color artwork
gcp.cloud_run((18, 25), width=11, style=Styles.Primary)
text((18, 10), "Default Multi-color", style=Styles.Primary.patch(text_size=8))

# 2. Semi-transparent (decommissioned / background service)
gcp.cloud_run((45, 25), width=11, style=Styles.Primary.patch(image_alpha=0.35))
text((45, 10), "image_alpha=0.35", style=Styles.Primary.patch(text_size=8))

# 3. Solid color silhouette mask
gcp.cloud_run((72, 25), width=11, style=Styles.Primary.patch(image_tint_color=Colors.Red))
text((72, 10), "image_tint_color=Red", style=Styles.Primary.patch(text_size=8))

# 4. Outlined boundary box
box_style = Styles.Primary.patch(image_border_color=Colors.Black, image_border_width=1.0, image_border_style="dashed")
gcp.cloud_run((99, 25), width=11, style=box_style)
text((99, 10), "Framed Box", style=Styles.Primary.patch(text_size=8))

save()
```

---

## 7. Combining Icons with Containers, Badges, and Labels

In production cloud architecture schemas and workflow diagrams, icons rarely exist in isolation. They are composed with container cards, status badges, directional lines, and multi-line descriptive text.

### 7.1. Structural Composition Patterns

```text
 ┌────────────────────────────────────────────────────────┐
 │ Container Card (rectangle with r=2, style=Styles.MutedFlat) │
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
from drawlib.styles import Styles

setup(width=80, height=50)

icon_x, icon_y = 40, 30
icon_w = 12

# 1. Render icon
gcp.google_kubernetes_engine((icon_x, icon_y), width=icon_w, style=Styles.Primary)

# 2. Render primary and secondary labels
text((icon_x, icon_y - (icon_w / 2) - 4), "GKE Ingress", style=Styles.PrimaryBold.patch(text_size=10))
text((icon_x, icon_y - (icon_w / 2) - 9), "v1.30 Production", style=Styles.Dark.patch(text_size=8))

save()
```

### 7.3. Pattern 2: Icon Inside Container Card with Status Badge

```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.icons import gcp, phosphor
from drawlib.shapes import circle, rectangle
from drawlib.text import text
from drawlib.styles import Styles

setup(width=100, height=60)

card_x, card_y = 50, 30
card_w, card_h = 36, 42

# 1. Card container background
rectangle((card_x, card_y), width=card_w, height=card_h, r=3, style=Styles.MutedFlat)
rectangle((card_x, card_y), width=card_w, height=card_h, r=3, style=Styles.MutedSolid)

# 2. Cloud service icon
gcp.compute_engine((card_x, card_y + 6), width=14, style=Styles.Primary)

# 3. Label block
text((card_x, card_y - 7), "Worker Node 01", style=Styles.PrimaryBold.patch(text_size=10))
text((card_x, card_y - 13), "n2-standard-4", style=Styles.Dark.patch(text_size=8))

# 4. Status badge (top-right corner indicator)
badge_x = card_x + (card_w / 2) - 4
badge_y = card_y + (card_h / 2) - 4
circle((badge_x, badge_y), radius=3.2, style=Styles.GreenFlat)
phosphor.check((badge_x, badge_y), width=3.8, style=Styles.WhiteBold)

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
from drawlib.styles import Styles

setup(width=120, height=40)

steps = [
    (1, "Request", phosphor.paper_plane_tilt, 20),
    (2, "Authenticate", phosphor.lock_key, 50),
    (3, "Authorize", phosphor.shield_check, 80),
    (4, "Deliver", phosphor.check_circle, 110),
]

for num, label, icon_fn, x in steps:
    # 1. Main action icon
    icon_fn((x, 22), width=10, style=Styles.BlueBold)
    text((x, 9), label, style=Styles.DarkBold.patch(text_size=9))

    # 2. Numbered badge at top-left corner of icon
    b_x, b_y = x - 6, 28
    circle((b_x, b_y), radius=2.5, style=Styles.TealFlat)
    text((b_x, b_y), str(num), style=Styles.WhiteBold.patch(text_size=8))

# Connectors between milestones
line((28, 22), (42, 22), arrow_head="->", style=Styles.PrimaryBold)
line((58, 22), (72, 22), arrow_head="->", style=Styles.PrimaryBold)
line((88, 22), (102, 22), arrow_head="->", style=Styles.PrimaryBold)

save()
```

---

## 8. Complete Cloud Architecture Schemas (Production Examples)

The following end-to-end examples demonstrate production architectures combining GCP icons, Phosphor icons, boundary boxes, badges, and connectors.

### 8.1. High-Availability Multi-Tier Web Application on GCP

This architecture features an internet-facing Cloud Armor and Load Balancer tier, scalable Cloud Run microservices, Cloud SQL database storage, Redis caching, and integrated Cloud Monitoring:

```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.icons import gcp, phosphor
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=155, height=95)

# 1. Diagram Title & Subtitle
text((77.5, 88), "High-Availability Multi-Tier Web Application on GCP", style=Styles.DarkBold.patch(text_size=15))
text((77.5, 82), "End-to-End Traffic Routing, Microservices, Caching, and Persistence", style=Styles.Muted.patch(text_size=9.5))

# 2. Boundary Containers: GCP Project & VPC Network
rectangle((88, 41), width=124, height=68, r=4, style=Styles.MutedDashed)
text((30, 71), "Google Cloud Project (prod-us-central1)", style=Styles.DarkBold.patch(text_size=9.5, text_halign="left"))

rectangle((88, 38), width=116, height=54, r=3, style=Styles.Muted)
text((34, 61), "Custom VPC Network (10.0.0.0/16)", style=Styles.Muted.patch(text_size=8.5, text_halign="left"))

# 3. Public Internet Tier (Users & CDN)
phosphor.user((13, 42), width=9, style=Styles.DarkBold)
text((13, 33), "Web Clients", style=Styles.DarkBold.patch(text_size=9))
text((13, 28), "HTTPS / SSL", style=Styles.Muted.patch(text_size=8))

# 4. Ingress Tier: Cloud Armor & Load Balancing
rectangle((44, 42), width=20, height=38, r=2, style=Styles.Neutral)
gcp.cloud_armor((44, 53), width=7.5, style=Styles.Primary)
text((44, 45.5), "Cloud Armor", style=Styles.DarkBold.patch(text_size=8))
gcp.cloud_load_balancing((44, 34), width=7.5, style=Styles.Primary)
text((44, 26.5), "Global ALB", style=Styles.DarkBold.patch(text_size=8))

# 5. Compute Tier: Cloud Run Service (Primary Hero Node)
rectangle((74, 42), width=24, height=34, r=2, style=Styles.PrimaryNeutral)
gcp.cloud_run((74, 49), width=10, style=Styles.Primary)
text((74, 38), "App Backend", style=Styles.DarkBold.patch(text_size=9))
text((74, 33), "Cloud Run", style=Styles.Muted.patch(text_size=8))
# Replica indicator badge
circle((83, 56), radius=2.5, style=Styles.PrimaryFlat)
text((83, 56), "x8", style=Styles.WhiteBold.patch(text_size=7))

# 6. Caching Tier: Memorystore Redis
rectangle((106, 52), width=22, height=18, r=2, style=Styles.SecondaryNeutral)
gcp.memorystore((106, 55.5), width=7.5, style=Styles.Primary)
text((106, 47.5), "Memorystore", style=Styles.DarkBold.patch(text_size=8))

# 7. Database Tier: Cloud SQL HA
rectangle((106, 28), width=22, height=18, r=2, style=Styles.SecondaryNeutral)
gcp.cloud_sql((106, 31.5), width=7.5, style=Styles.Primary)
text((106, 23.5), "Cloud SQL HA", style=Styles.DarkBold.patch(text_size=8))

# 8. Storage & Observability Tier
rectangle((134, 42), width=20, height=38, r=2, style=Styles.Neutral)
gcp.cloud_storage((134, 53), width=7.5, style=Styles.Primary)
text((134, 45.5), "GCS Assets", style=Styles.DarkBold.patch(text_size=8))
gcp.cloud_monitoring((134, 34), width=7.5, style=Styles.Primary)
text((134, 26.5), "Monitoring", style=Styles.DarkBold.patch(text_size=8))

# 9. Inter-service Connectors
line((19, 42), (34, 42), arrow_head="->", style=Styles.DarkBold)
line((54, 42), (62, 42), arrow_head="->", style=Styles.DarkBold)
line((86, 46), (95, 52), arrow_head="<->", style=Styles.DarkBold)
line((86, 36), (95, 28), arrow_head="<->", style=Styles.DarkBold)
line((86, 42), (124, 42), arrow_head="->", style=Styles.MutedDashed)

save()
```

### 8.2. Event-Driven Real-Time Data Pipeline

This schema models an IoT ingestion pipeline using Cloud Pub/Sub, stream processing via Cloud Functions, analytical data warehousing in BigQuery, and BI reporting in Looker:

```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.icons import gcp, phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=145, height=65)

# Title
text((72.5, 58), "Event-Driven Serverless Ingestion & Analytics Pipeline", style=Styles.DarkBold.patch(text_size=15))

# Step 1: External IoT Producer
phosphor.cpu((16, 30), width=10, style=Styles.DarkBold)
text((16, 19), "IoT Sensors", style=Styles.DarkBold.patch(text_size=9))
text((16, 14), "MQTT Stream", style=Styles.Muted.patch(text_size=8))

# Step 2: Message Buffer (Pub/Sub - Hero Ingest Hub)
rectangle((45, 30), width=24, height=28, r=2, style=Styles.PrimaryNeutral)
gcp.pubsub((45, 36), width=10, style=Styles.Primary)
text((45, 25), "Cloud Pub/Sub", style=Styles.DarkBold.patch(text_size=9))
text((45, 20), "Buffer Topic", style=Styles.Muted.patch(text_size=8))

# Step 3: Serverless Worker (Cloud Functions)
rectangle((76, 30), width=24, height=28, r=2, style=Styles.Neutral)
gcp.cloud_functions((76, 36), width=10, style=Styles.Primary)
text((76, 25), "Cloud Functions", style=Styles.DarkBold.patch(text_size=9))
text((76, 20), "Transform / Parse", style=Styles.Muted.patch(text_size=8))

# Step 4: Analytical Data Warehouse (BigQuery)
rectangle((107, 30), width=24, height=28, r=2, style=Styles.SecondaryNeutral)
gcp.bigquery((107, 36), width=10, style=Styles.Primary)
text((107, 25), "BigQuery", style=Styles.DarkBold.patch(text_size=9))
text((107, 20), "Partitioned Tables", style=Styles.Muted.patch(text_size=8))

# Step 5: Dashboard Visualization (Looker)
phosphor.chart_line_up((134, 30), width=10, style=Styles.DarkBold)
text((134, 19), "Looker Studio", style=Styles.DarkBold.patch(text_size=9))
text((134, 14), "Real-time BI", style=Styles.Muted.patch(text_size=8))

# Connectors
line((23, 30), (33, 30), arrow_head="->", style=Styles.DarkBold)
line((57, 30), (64, 30), arrow_head="->", style=Styles.DarkBold)
line((88, 30), (95, 30), arrow_head="->", style=Styles.DarkBold)
line((119, 30), (127, 30), arrow_head="->", style=Styles.DarkBold)

save()
```

### 8.3. Hybrid Cloud Infrastructure Schema

Demonstrating seamless interoperability between on-premise infrastructure (Phosphor vector servers) and Google Cloud Interconnect:

```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.icons import gcp, phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=145, height=62)

# Section Headers
text((72.5, 55), "Hybrid Enterprise On-Premises to GCP Interconnect", style=Styles.DarkBold.patch(text_size=14))

# On-Premise Datacenter Boundary
rectangle((30, 26), width=46, height=36, r=2, style=Styles.Neutral)
text((30, 39), "Corporate On-Premises Datacenter", style=Styles.DarkBold.patch(text_size=8.5))

phosphor.hard_drives((19, 25), width=9, style=Styles.DarkBold)
text((19, 15), "App Server", style=Styles.Dark.patch(text_size=8))

phosphor.database((41, 25), width=9, style=Styles.DarkBold)
text((41, 15), "Oracle DB", style=Styles.Dark.patch(text_size=8))

# Cloud Boundary
rectangle((112, 26), width=50, height=36, r=2, style=Styles.MutedDashed)
text((112, 39), "Google Cloud Platform VPC", style=Styles.DarkBold.patch(text_size=8.5))

gcp.google_kubernetes_engine((100, 25), width=10, style=Styles.Primary)
text((100, 15), "GKE Cluster", style=Styles.Dark.patch(text_size=8))

gcp.cloud_spanner((124, 25), width=10, style=Styles.Primary)
text((124, 15), "Cloud Spanner", style=Styles.Dark.patch(text_size=8))

# Dedicated Cloud Interconnect (Hero Bridge)
rectangle((71, 25), width=18, height=13, r=1.5, style=Styles.PrimaryFlat)
text((71, 27.5), "Cloud", style=Styles.WhiteBold.patch(text_size=8))
text((71, 22), "Interconnect", style=Styles.White.patch(text_size=7.5))

# Connectors
line((53, 25), (62, 25), arrow_head="<->", style=Styles.DarkBold)
line((80, 25), (93, 25), arrow_head="<->", style=Styles.DarkBold)
line((107, 25), (117, 25), arrow_head="<->", style=Styles.DarkBold)

save()
```

### 8.4. Enterprise GitOps & Automated CI/CD Delivery Pipeline

This schema illustrates an automated GitOps delivery workflow from source code commit to container deployment in Google Kubernetes Engine:

```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.icons import gcp, phosphor
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=150, height=65)

# Pipeline Title
text((75, 58), "Automated GitOps & CI/CD Delivery Pipeline", style=Styles.DarkBold.patch(text_size=15))

# Stage 1: Developer Workstation
rectangle((22, 28), width=26, height=32, r=2, style=Styles.Neutral)
phosphor.laptop((22, 36), width=10, style=Styles.DarkBold)
text((22, 24), "Developer", style=Styles.DarkBold.patch(text_size=9))
text((22, 18.5), "git push", style=Styles.Muted.patch(text_size=8))

# Stage 2: Source Repository & Webhook
rectangle((56, 28), width=26, height=32, r=2, style=Styles.Neutral)
phosphor.git_branch((56, 36), width=10, style=Styles.DarkBold)
text((56, 24), "Cloud Source", style=Styles.DarkBold.patch(text_size=9))
text((56, 18.5), "Pull Request", style=Styles.Muted.patch(text_size=8))

# Stage 3: Build & Automated Testing (Cloud Build - Hero Stage)
rectangle((90, 28), width=26, height=32, r=2, style=Styles.PrimaryNeutral)
gcp.cloud_build((90, 36), width=10, style=Styles.Primary)
text((90, 24), "Cloud Build", style=Styles.DarkBold.patch(text_size=9))
text((90, 18.5), "Unit / Lint / Test", style=Styles.Muted.patch(text_size=8))

# Stage 4: Artifact Registry (OCI Images)
rectangle((124, 28), width=26, height=32, r=2, style=Styles.SecondaryNeutral)
gcp.artifact_registry((124, 36), width=10, style=Styles.Primary)
text((124, 24), "Artifact Reg.", style=Styles.DarkBold.patch(text_size=9))
text((124, 18.5), "OCI Images", style=Styles.Muted.patch(text_size=8))

# Connectors with Pipeline Direction
line((35, 28), (43, 28), arrow_head="->", style=Styles.DarkBold)
line((69, 28), (77, 28), arrow_head="->", style=Styles.DarkBold)
line((103, 28), (111, 28), arrow_head="->", style=Styles.DarkBold)

# Deployment Badge
circle((133, 40), radius=2.5, style=Styles.PrimaryFlat)
phosphor.check((133, 40), width=3, style=Styles.WhiteBold)

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
| `style` | `Style \| None`| `None` | Style object (e.g. `Styles.Blue`, `Styles.GreenFlat`, `Styles.RedBold`). |

---

<p align="center"><em>© 2026 drawlib by Yuichi Ito. Released under the Apache 2.0 License.</em></p>
