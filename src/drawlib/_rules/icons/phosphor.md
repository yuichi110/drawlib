# Drawlib Phosphor Icons Guidelines (`lib-icons-phosphor`)

API specification and usage guidelines for `drawlib.icons.phosphor` (`PhosphorIcon`) and the low-level `drawlib.icons.font_icon()` renderer. See `lib-icons-overview` for cross-tier icon rules.

---

## 1. Overview & API Signatures

`drawlib.icons.phosphor` provides **1,512 monochrome vector icons** across **5 visual weights** (**7,560 total glyph variants**) rendered via TrueType font glyphs (`icon_phosphor` asset package). Because Phosphor icons are vector font glyphs rather than bitmaps, they scale infinitely and adopt `style.icon_color` from any `Style` preset.

### 1.1. `phosphor.<icon_name>()`
Every icon is exposed as a dedicated function in `drawlib.icons.phosphor`. **`style: Style` is a required keyword-only argument.**

```python
from drawlib.diagrams.architecture import PhosphorIcon
from drawlib.icons import phosphor
from drawlib.styles import Styles
from drawlib.types import Style

def <icon_name>(
    xy: tuple[float, float],
    width: float,
    *,
    style: Style,
) -> None: ...
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | *Required* | **Center `(cx, cy)`** coordinate in canvas units. |
| `width` | `float` | *Required* | Icon width (and height, `1:1` square) in canvas units ($> 0$). |
| `style` | `Style` | *Required (Keyword-Only)* | Controls glyph color via `style.icon_color` (`Styles.Primary`, `Styles.White`, `Styles.Danger`), glyph weight via `style.icon_style` (`"thin"`, `"light"`, `"regular"`, `"bold"`, `"fill"`), `alpha`, `angle`, `halign`, and `valign`. |

---

## 2. The 5 Visual Weights (`style.icon_style`) & Color Styling (`icon_color`)

Phosphor weight is controlled via `style.icon_style` (or preset style variants):
- **`"regular"`**: Balanced stroke weight (`Styles.Primary`, `Styles.Dark`, or `style.patch(icon_style="regular")`).
- **`"bold"`**: High-contrast thicker stroke (`Styles.PrimaryBold`, `Styles.WhiteBold`, or `style.patch(icon_style="bold")`).
- **`"light"` / `"thin"`**: Delicate hairline strokes (`Styles.PrimaryLight`, `Styles.PrimaryThin`, or `style.patch(icon_style="thin")`).
- **`"fill"`**: Solid filled silhouette (`Styles.PrimaryFlat`, or `style.patch(icon_style="fill")`).

### Matching `style.icon_color` to Card Backgrounds
- On light neutral cards (`Styles.Neutral`, `Styles.PrimaryNeutral`, `Styles.SecondaryNeutral`), pass `style=Styles.Primary`, `Styles.Secondary`, `Styles.Accent`, or `Styles.Dark`.
- On dark saturated cards (`Styles.PrimaryFlat`, `Styles.AccentFlat`, `Styles.DangerFlat`, `Styles.DarkFlat`), pass `style=Styles.White` (or `Styles.White.patch(icon_style="fill")`).

```drawlib code=fold align=center file=icons_phosphor_weights_rules.png caption="Phosphor Icon Weights (thin, light, regular, bold, fill) via style.icon_style"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=144, height=46)

weights = ["thin", "light", "regular", "bold", "fill"]
for idx, w in enumerate(weights):
    cx = 18.0 + idx * 27.0
    is_fill = w == "fill"
    card_st = Styles.PrimaryFlat if is_fill else Styles.Neutral
    icon_st = Styles.White.patch(icon_style=w) if is_fill else Styles.Primary.patch(icon_style=w)
    lbl_st = Styles.WhiteBold if is_fill else Styles.DarkBold

    rectangle((cx, 23), width=23, height=30, style=card_st.patch(shape_r=2))
    phosphor.shield_check((cx, 27), width=9.5, style=icon_st)
    text((cx, 13), f'"{w}"', style=lbl_st.patch(text_size=10.0))

save()
```

---

## 3. Curated High-Frequency Phosphor Icons by Category

All 1,512 icon names use `snake_case` functions (`phosphor.<name>`) and `UPPER_SNAKE_CASE` enum members (`PhosphorIcon.<NAME>`). Python reserved keywords have a trailing underscore (`phosphor.infinity_` / `PhosphorIcon.INFINITY_`, `phosphor. try_` if applicable).

| Category | Representative `phosphor.<name>` Functions (`PhosphorIcon.<NAME>`) |
| :--- | :--- |
| **Compute, Server & Hardware** | `cpu`, `hard_drive`, `hard_drives`, `memory`, `desktop`, `Desktop_tower`, `laptop`, `device_mobile`, `terminal`, `terminal_window`, `plugs_connected` |
| **Cloud, Network & Connectivity** | `cloud`, `cloud_arrow_up`, `cloud_arrow_down`, `cloud_check`, `globe`, `globe_hemisphere_west`, `wifi_high`, `broadcast`, `share_network`, `arrows_left_right`, `arrows_split` |
| **Database, Storage & Files** | `database`, `archive`, `folder`, `folder_open`, `file`, `file_text`, `file_code`, `file_sql`, `file_csv`, `file_pdf`, `clipboard_text`, `table` |
| **Code, Git & DevOps** | `code`, `code_block`, `git_branch`, `git_commit`, `git_merge`, `git_pull_request`, `git_fork`, `bug`, `wrench`, `gear`, `gear_six`, `package`, `rocket_launch`, `webhooks_logo` |
| **Security, IAM & Compliance** | `shield`, `shield_check`, `shield_warning`, `lock`, `lock_key`, `lock_open`, `key`, `fingerprint`, `user_check`, `Identification_badge`, `eye`, `eye_slash`, `detective` |
| **AI, Analytics & Charts** | `brain`, `sparkle`, `magic_wand`, `robot`, `chart_bar`, `chart_line`, `chart_line_up`, `chart_pie_slice`, `gauge`, `pulse`, `activity`, `funnel`, `magnifying_glass` |
| **Status, Alerts & Workflow** | `check_circle`, `warning`, `warning_circle`, `x_circle`, `info`, `question`, `bell`, `bell_ringing`, `clock`, `timer`, `hourglass`, `lightning`, `fire`, `flag` |
| **Users, Teams & Commerce** | `user`, `users`, `users_three`, `user_circle`, `user_gear`, `buildings`, `storefront`, `shopping_cart`, `credit_card`, `currency_dollar`, `receipt`, `handshake`, `chat_circle_text` |

---

## 4. Using `PhosphorIcon` in High-Level Components (`SmartArts` & `Diagrams`)

Pass `PhosphorIcon.<NAME>` directly to `ArchitectureDiagram` (`Node`, `NodeGroup`), `SequenceDiagram` (`add_participant`), `FlowDiagram`, or `SmartArts` (`CardGrid`, `ChevronProcess`, `FeatureList`, `HexagonCluster`, etc.):

```python
from drawlib.diagrams.architecture import ArchitectureDiagram, Node, PhosphorIcon
from drawlib.styles import Styles

d = ArchitectureDiagram(node_style=Styles.Primary, node_card_style=Styles.Neutral)
api = d.add(Node("API Gateway", width=24, height=18, icon=PhosphorIcon.GLOBE), xy=(10, 10))
db = d.add(Node("Primary DB", width=24, height=18, icon=PhosphorIcon.DATABASE), xy=(50, 10))
d.connect(api, db, label="SQL")
```

---

## 5. Low-Level `font_icon()` Function

For rendering arbitrary Unicode codepoints from a `FontIcon` or a local custom `.ttf`/`.otf` icon font file, use `drawlib.icons.font_icon`:

```python
from pathlib import Path
from drawlib.fonts import FontIcon
from drawlib.icons import font_icon
from drawlib.types import Style

def font_icon(
    xy: tuple[float, float],
    width: float,
    codepoint: str,
    font: FontIcon | str | Path,
    *,
    style: Style,
) -> None: ...
```
- `codepoint`: Single Unicode character (e.g. `"\ue1c4"`).
- `font`: `FontIcon` enum member (`FontIcon.PHOSPHOR_REGULAR`, `FontIcon.PHOSPHOR_BOLD`, `FontIcon.PHOSPHOR_FILL`, etc.) or path to a custom `.ttf`/`.otf` font file.
- `style`: Required keyword-only `Style` (`style.icon_color` colors the rendered glyph).
