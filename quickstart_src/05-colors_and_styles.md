# 5. Styling System: GoogleStyles & Design Tokens

Drawlib decouples visual presentation from geometric drawing logic using a systematic **Design Token & Style Matrix**. This ensures consistent line widths, colors, borders, and typography across large documentation projects.

## Semantic Roles & Style Matrix

Drawlib defines 6 core semantic roles across all color palettes:

| Semantic Role | Typical Architectural Meaning | Google Theme Hex |
| :--- | :--- | :--- |
| **`primary`** | Main computation, core services, active state | Google Blue (`#4285F4`) |
| **`secondary`** | Data stores, caches, asynchronous queues | Google Dark Gray (`#5F6368`) |
| **`accent`** | Ingress gateways, external clients, key callouts | Google Amber (`#FBBC04`) |
| **`muted`** | Boundaries, VPC containers, structural lines | Google Light Gray (`#DADCE0`) |
| **`danger`** | Errors, alerts, vulnerabilities, security zones | Google Red (`#EA4335`) |
| **`success`** | Verified status, health checks, completed stages | Google Green (`#34A853`) |

Each semantic role provides **10 orthogonal style variants**:
- **Borders & Fills**: `bordered` (default), `flat`, `solid`, `light`
- **Outlines**: `outline`, `outline_bold`, `outline_light`
- **Dashed Lines**: `dashed`, `dashed_bold`, `dashed_light`

```drawlib 640px center caption:"Figure 5.1: The 6 Semantic Roles Across Core Style Variants"
from drawlib.canvas import setup
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=120, height=52)

roles = [
    (14, "primary", Styles.primary_flat, Styles.primary_outline, Styles.primary_dashed),
    (32, "secondary", Styles.secondary_flat, Styles.secondary_outline, Styles.secondary_dashed),
    (50, "accent", Styles.accent_flat, Styles.accent_outline, Styles.accent_dashed),
    (68, "muted", Styles.muted_flat, Styles.muted_outline, Styles.muted_dashed),
    (86, "danger", Styles.danger_flat, Styles.danger_outline, Styles.danger_dashed),
    (104, "success", Styles.success_flat, Styles.success_outline, Styles.success_dashed),
]

for x, label, st_flat, st_out, st_dash in roles:
    text((x, 48), label, style=Styles.bold, size=9)
    # Flat box
    rectangle((x, 37), width=15, height=12, r=1.5, style=st_flat, text="flat", textstyle=Styles.white_bold)
    # Outline box
    rectangle((x, 22), width=15, height=12, r=1.5, style=st_out, text="outline", textstyle=Styles.primary)
    # Dashed box
    rectangle((x, 7), width=15, height=12, r=1.5, style=st_dash, text="dashed", textstyle=Styles.primary)
```

## Creating Custom Styles with `.patch()`

Styles are immutable by design. To derive a variant with modified properties (e.g. customized font size or fill opacity), call `.patch()` on an existing style:

```python
from drawlib.styles import Styles

# Derive a custom style by modifying specific attributes
callout_style = Styles.accent_flat.patch(
    shape_fill_alpha=0.85,
    text_size=11.0,
    shape_line_width=1.5,
)
```

## Typography & Universal Fonts (`drawlib.fonts`)

Typography is a critical component of professional technical diagrams. Drawlib provides CJK/Latin cross-platform font families:

- **`Font`**: Universal Google Noto Sans family supporting English, Japanese, Chinese, and Korean.
- **`FontRoboto`**: Clean sans-serif optimized for modern UI and cloud architecture documentation.
- **`FontMonoSpace`**: Roboto Mono for code blocks, URLs, and JSON keys.
- **`FontFile(path)`**: Custom TrueType/OpenType font files.

```drawlib 620px center caption:"Figure 5.2: Typography Hierarchy & Font Families"
from drawlib.canvas import setup
from drawlib.fonts import Font, FontMonoSpace, FontRoboto
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=120, height=44)

type_samples = [
    (20, "Noto Universal", "Font.SANSSERIF_BOLD", Font.SANSSERIF_BOLD, Styles.primary_flat),
    (60, "Roboto Sans", "FontRoboto.ROBOTO_BOLD", FontRoboto.ROBOTO_BOLD, Styles.secondary_flat),
    (100, "Roboto Mono", "FontMonoSpace.ROBOTO_MONO", FontMonoSpace.ROBOTO_MONO_REGULAR, Styles.accent_flat),
]

for x, title, sub, font_obj, st in type_samples:
    rectangle((x, 22), width=34, height=36, r=2.5, style=Styles.muted_dashed)
    rectangle((x, 32), width=30, height=10, r=1.5, style=st, text=title, textstyle=Styles.white_bold)
    text((x, 20), sub, style=Styles.bold, size=7.5)
    text((x, 11), "Quick brown fox jumps\n1234567890", style=Styles.primary.patch(text_font=font_obj, text_size=7.5))
```
