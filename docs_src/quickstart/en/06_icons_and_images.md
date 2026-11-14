# 6. 34 Icon Suites & Media Assets

Architecture blueprints and technical guides immediately gain clarity when services carry recognizable UI glyphs, official cloud icons, and crisp raster illustrations. Drawlib bundles **34 on-demand cached icon suites** in `drawlib.icons` alongside non-destructive raster processing and sub-canvas composition in `drawlib.images`.

```drawlib align=center code=fold file=icon_suites_showcase.png caption="Figure 6.1: Representative Icons Across Drawlib's 34 Built-In UI, Cloud, Domain Brand, and Original 2D Suites"
from drawlib.canvas import save, setup
from drawlib.icons import (
    ai,
    aws,
    azure,
    cnative,
    data,
    gcp,
    original_ai,
    original_cnative,
    original_data,
    original_security,
    phosphor,
)
from drawlib.shapes import rectangle
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=144, height=68)

hdr = Styles.DarkBold.patch(text_size=10.5, halign="left")
lbl = Styles.DarkBold.patch(text_size=10.0)
xs_l = [15.5, 30.2, 44.8, 59.5]
xs_r = [84.5, 99.2, 113.8, 128.5]

# 4 neutral category cards
rectangle((37.5, 49.5), width=64.0, height=26.5, style=Styles.PrimaryNeutral.patch(shape_r=2.2))
rectangle((106.5, 49.5), width=64.0, height=26.5, style=Styles.Neutral.patch(shape_r=2.2))
rectangle((37.5, 18.5), width=64.0, height=26.5, style=Styles.Neutral.patch(shape_r=2.2))
rectangle((106.5, 18.5), width=64.0, height=26.5, style=Styles.SecondaryNeutral.patch(shape_r=2.2))

# 1. Phosphor UI Vector Glyphs
text((9.0, 59.0), "1. UI Vector Glyphs (phosphor)", style=hdr)
phosphor.cpu((xs_l[0], 50.2), width=7.2, style=Styles.Dark)
phosphor.database((xs_l[1], 50.2), width=7.2, style=Styles.PrimaryBold)
phosphor.shield_check((xs_l[2], 50.2), width=7.2, style=Styles.Success.patch(icon_style="fill"))
phosphor.git_branch((xs_l[3], 50.2), width=7.2, style=Styles.SecondaryBold)
for cx, name in zip(xs_l, ["cpu", "database", "shield", "git_branch"]):
    text((cx, 41.0), name, style=lbl)

# 2. Official Cloud Provider Suites (gcp, aws, azure)
text((78.0, 59.0), "2. Cloud Suites (gcp, aws, azure)", style=hdr)
gcp.cloud_run((xs_r[0], 50.2), width=7.8, style=Styles.Primary)
gcp.bigquery((xs_r[1], 50.2), width=7.8, style=Styles.Primary)
aws.aws_lambda((xs_r[2], 50.2), width=7.8, style=Styles.Primary)
azure.cosmos_db((xs_r[3], 50.2), width=7.8, style=Styles.Primary)
for cx, name in zip(xs_r, ["Cloud Run", "BigQuery", "Lambda", "Cosmos DB"]):
    text((cx, 41.0), name, style=lbl)

# 3. 15 Multi-Brand Domain Suites (ai .. workspace)
text((9.0, 28.0), "3. 15 Domain Suites (ai, cnative, data...)", style=hdr)
ai.gemini((xs_l[0], 19.2), width=7.8, style=Styles.Primary)
cnative.kubernetes((xs_l[1], 19.2), width=7.8, style=Styles.Primary)
cnative.docker((xs_l[2], 19.2), width=7.8, style=Styles.Primary)
data.postgresql((xs_l[3], 19.2), width=7.8, style=Styles.Primary)
for cx, name in zip(xs_l, ["gemini", "k8s", "docker", "postgres"]):
    text((cx, 10.0), name, style=lbl)

# 4. 15 original_* 2D Twin Suites with style= tinting & border
text((78.0, 28.0), "4. 15 original_* Suites (style= Tinted)", style=hdr)
tinted = Styles.Secondary.patch(
    image_tint_color=Colors.White,
    image_border_color=Colors.Secondary,
    image_border_width=1.0,
)
original_ai.ai_agent((xs_r[0], 19.2), width=7.8, style=tinted)
original_data.data_lakehouse((xs_r[1], 19.2), width=7.8, style=tinted)
original_security.zero_trust((xs_r[2], 19.2), width=7.8, style=tinted)
original_cnative.argo((xs_r[3], 19.2), width=7.8, style=tinted)
for cx, name in zip(xs_r, ["ai_agent", "lakehouse", "zero_trust", "argo"]):
    text((cx, 10.0), name, style=lbl)

save()
```

---

## 6.1 Overview of Drawlib's 34 Built-In Icon Suites

Every icon function in `drawlib.icons` follows the universal **center-anchored `xy = (cx, cy)`** contract with a `1:1` square `width=` and a mandatory keyword-only `*, style: Style` parameter. Binary icon packs download automatically on first reference and cache locally (`uv run drawlib cache download --all` pre-fetches all 34 suites for offline CI).

| Tier | Suites (34 Total) | Rendering & `style=` Customization |
| :--- | :--- | :--- |
| **1. General UI Vector Icons (1)** | `phosphor` (1,500+ icons, plus low-level `font_icon`) | Crisp TrueType vector glyphs supporting 5 weights via `style.icon_style` (`"thin"`, `"light"`, `"regular"`, `"bold"`, `"fill"`—or `Styles.*Bold` / `*Flat`) and direct coloring via `style.icon_color`. |
| **2. Cloud Provider Suites (3)** | `gcp`, `aws`, `azure` | Official `512x512` RGBA service icons for Google Cloud, AWS, and Microsoft Azure architectures. |
| **3. Multi-Brand Domain Suites (15)** | `ai`, `business`, `client`, `cloud`, `cnative`, `code`, `data`, `devops`, `facility`, `itservice`, `network`, `security`, `server`, `social`, `workspace` | Curated multi-color vendor logos across AI/LLMs, CI/CD & DevOps, containers/Kubernetes (`cnative`), databases/streaming (`data`), frontend/mobile (`client`), hardware (`server`, `facility`), networking, and security. |
| **4. `original_*` 2D Twin Suites (15)** | `original_ai` through `original_workspace` | Unified flat 2D brand twins plus vendor-neutral concept icons (`original_ai.ai_agent`, `original_data.data_lakehouse`, `original_security.zero_trust`). Accepts `style=` background tinting (`image_tint_color`), framing (`image_border_*`), `alpha`, and `angle` (and monochrome recoloring via `Dimage.colorize()`). |

---

## 6.2 Standalone Icon Calls vs. High-Level Enum Tokens

Drawlib provides two ergonomic ways to place icons depending on whether you are composing a custom canvas or declaring a structured diagram:

1. **Direct Canvas Calls (`drawlib.icons.<suite>.<name>`)**: Call `phosphor.cpu((25, 20), width=8.0, style=Styles.PrimaryBold)` (or `Styles.Accent.patch(icon_style="fill")`) and `gcp.cloud_run((60, 20), width=9.0, style=Styles.Primary)` to place an icon at exact canvas coordinates `(cx, cy)`.
2. **Typed Enum Tokens (`PhosphorIcon`, `GcpIcon`, `AwsIcon`, `CnativeIcon`, etc.)**: High-level diagram builders (`drawlib.diagrams.architecture`, `drawlib.diagrams.sequence`, and icon-aware `SmartArts`) export strongly typed `StrEnum` tokens so nodes automatically align icons alongside labels without manual coordinate math.

```python
from drawlib.canvas import save, setup
from drawlib.diagrams.architecture import ArchitectureDiagram, GcpIcon, Node, PhosphorIcon
from drawlib.icons import phosphor
from drawlib.styles import Styles

setup(width=120, height=40)

# 1. Standalone direct icon call at exact center (cx, cy)
phosphor.sparkle((16, 20), width=7.5, style=Styles.Accent.patch(icon_style="fill"))

# 2. Enum tokens inside high-level ArchitectureDiagram nodes
arch = ArchitectureDiagram(
    node_style=Styles.PrimaryBold,
    node_text_style=Styles.DarkBold.patch(text_size=11.0),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=10.0),
    node_card_style=Styles.Neutral,
)
gw = arch.add(Node("Edge Gateway", width=34, height=16, icon=PhosphorIcon.SHIELD_CHECK), xy=(52, 20))
svc = arch.add(
    Node(
        "Cloud Run API",
        width=34,
        height=16,
        icon=GcpIcon.CLOUD_RUN,
        card_style=Styles.PrimaryNeutral,
    ),
    xy=(98, 20),
)
arch.connect(gw, svc, arrow="->")
arch.draw()

save()
```

---

## 6.3 Raster Assets (`image`), `Dimage` Pipelines & Nested Sub-Canvases

For screenshots, product photos, mascots, and composite sub-diagrams, `drawlib.images` provides three composable tools:

- **`image(xy, width=..., image="_assets/linux.png", style=...)`**: Places a raster file, `PIL.Image.Image`, or `Dimage` centered at `xy = (cx, cy)` while automatically preserving its aspect ratio. Always store project images under `_assets/` and reference relative paths (`"_assets/linux.png"`). Use `style.patch(angle=..., alpha=..., image_tint_color=..., image_border_width=..., image_border_color=..., image_border_style=...)` to rotate, tint transparent backgrounds, or frame images cleanly.
- **Immutable `Dimage` Filter Chains**: Wrap any image in `Dimage("_assets/linux.png")` to chain non-destructive pixel operations—each returning a fresh `Dimage`:
  - **Geometry & Alpha Cleanup**: `.resize(width, height)`, `.crop(x, y, width, height)` *(where `(0, 0)` is the **bottom-left** pixel corner, matching Drawlib's Cartesian axes!)*, `.mirror()`, `.flip()`, `.trim()`, `.make_transparent(color="auto", tolerance=15)`, `.fill(color)`, and `.alpha(0.8)`.
  - **Color & Stylistic Filters**: `.grayscale()`, `.sepia()`, `.colorize(from_black_to=..., from_white_to=...)`, `.brightness(0.9)`, `.invert()`, `.posterize(num_colors=4)`, `.mosaic(block_size=16)`, `.blur()`, and `.line_extraction()`.
- **Nested Sub-Canvas Composition (`get_dimage_from_code`)**: Executes a self-contained Drawlib Python snippet in an isolated process and returns the rendered canvas in memory as a `Dimage`, making it easy to embed miniature badges or Picture-in-Picture diagrams inside larger layouts.

```drawlib align=center code=fold file=dimage_pipeline.png caption='Figure 6.2: Non-Destructive Dimage("_assets/linux.png") Transformation Pipeline and Styled Card Embedding'
from drawlib.canvas import save, setup
from drawlib.images import Dimage, get_dimage_from_code, image
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=144, height=62)

base = Dimage("_assets/linux.png")
xs = [20.5, 54.8, 89.2, 123.5]
card_w, card_h, cy = 28.5, 50.0, 31.0

title_st = Styles.DarkBold.patch(text_size=10.5)
code_st = Styles.Dark.patch(text_size=10.0)

# Stage 1: Original raster asset
rectangle((xs[0], cy), width=card_w, height=card_h, style=Styles.Neutral.patch(shape_r=2.2))
text((xs[0], 51.0), "1. Original", style=title_st)
image((xs[0], 31.8), width=14.5, image=base)
text((xs[0], 12.0), "Dimage(\n'_assets/linux.png')", style=code_st)

# Stage 2: Bottom-left Cartesian crop + mirror + rotated placement
rectangle((xs[1], cy), width=card_w, height=card_h, style=Styles.PrimaryNeutral.patch(shape_r=2.2))
text((xs[1], 51.0), "2. Crop & Tilt", style=title_st)
cropped = base.crop(110, 340, 455, 440).mirror()
image(
    (xs[1], 31.8),
    width=14.5,
    image=cropped,
    style=Styles.Primary.patch(
        angle=10,
        image_border_width=1.2,
        image_border_color=Colors.Primary,
    ),
)
text((xs[1], 12.0), ".crop().mirror()\n+ angle=10", style=code_st)

# Stage 3: Grayscale / filter chain
rectangle((xs[2], cy), width=card_w, height=card_h, style=Styles.Neutral.patch(shape_r=2.2))
text((xs[2], 51.0), "3. Filtered", style=title_st)
image((xs[2], 31.8), width=14.5, image=base.grayscale())
text((xs[2], 12.0), ".grayscale()\n(.sepia / .blur)", style=code_st)

# Stage 4: Embedded inside a styled card with get_dimage_from_code() badge
rectangle((xs[3], cy), width=card_w, height=card_h, style=Styles.SecondaryNeutral.patch(shape_r=2.2))
text((xs[3], 51.0), "4. Card Embed", style=title_st)
rectangle(
    (xs[3], 43.8),
    width=22.5,
    height=5.6,
    style=Styles.PrimaryFlat.patch(shape_r=1.4),
    text="Linux Node",
    text_style=Styles.WhiteBold.patch(text_size=10.0),
)
framed = base.resize(270, 320).fill(Colors.White)
image(
    (xs[3], 29.2),
    width=12.2,
    image=framed,
    style=Styles.Primary.patch(
        image_border_width=1.5,
        image_border_color=Colors.Primary,
    ),
)
sub_badge = get_dimage_from_code("""
from drawlib.canvas import setup
from drawlib.shapes import checkmark, circle
from drawlib.styles import Styles
setup(width=36, height=36)
circle((18, 18), radius=15, style=Styles.SuccessFlat)
checkmark((18, 18), width=15, style=Styles.WhiteFlat)
""").make_transparent(color="auto", tolerance=15)
image((xs[3] + 6.5, 22.8), width=5.6, image=sub_badge)
text((xs[3], 12.0), ".fill() + sub-canvas\nget_dimage_from_code", style=code_st)

# Pipeline arrows between cards
for i in range(3):
    line((xs[i] + 14.8, cy), (xs[i + 1] - 14.8, cy), arrow_head="->", style=Styles.DarkBold)

save()
```
