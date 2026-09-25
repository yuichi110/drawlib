# Drawlib Fonts Guidelines

Drawlib provides a comprehensive typography engine supporting multilingual scripts, standardized weights (Light, Regular, Bold), monospace code rendering, and custom TrueType/OpenType font loading.

---

## 1. Imports & Core Architecture

All public font classes are imported from `drawlib.fonts`:

```python
from drawlib.fonts import (
    # Universal & Default Fonts (CJK + Latin)
    Font,

    # Alphabet & Technical Typography
    FontSansSerif,
    FontSerif,
    FontMonoSpace,
    FontRoboto,
    FontSourceCode,

    # Regional & Non-Latin Scripts
    FontJapanese,
    FontChinese,
    FontKorean,
    FontArabic,
    FontThai,
    FontBrahmic,

    # Custom Font File Loader
    FontFile,
)
```

### On-Demand Download & Local Caching
To keep the base Drawlib installation lightweight (~few megabytes), fonts are downloaded dynamically upon first access and cached in the local user directory (`~/.cache/drawlib/fonts/`).

You can inspect and manage cached font files using CLI commands:
```bash
# List all locally cached font files:
uv run drawlib cache list

# Clear font cache to free disk space:
uv run drawlib cache clear
```

---

## 2. Font Class Catalog

### 2.1. `Font` (Default Universal Font)
`Font` is the default family. It maps to Noto Sans / Noto Serif and supports Latin, Japanese (Kanji/Kana), Chinese (Simplified/Traditional), and Korean (Hangul) simultaneously:

```python
Font.SANSSERIF_LIGHT
Font.SANSSERIF_REGULAR    # Default font for shapes and canvas text
Font.SANSSERIF_BOLD
Font.SERIF_LIGHT
Font.SERIF_REGULAR
Font.SERIF_BOLD
```

### 2.2. Alphabet Families
Tailored for clean Western technical documentation:

- **`FontRoboto`**: Clean modern neo-grotesque sans-serif.
  - `FontRoboto.ROBOTO_LIGHT`
  - `FontRoboto.ROBOTO_REGULAR`
  - `FontRoboto.ROBOTO_BOLD`
  - `FontRoboto.MONO_REGULAR`
- **`FontMonoSpace`**: Fixed-width font for data payloads, IP addresses, and tabular metrics.
  - `FontMonoSpace.ROBOTO_MONO_REGULAR`
  - `FontMonoSpace.ROBOTO_MONO_BOLD`
  - `FontMonoSpace.COURIER_REGULAR`
  - `FontMonoSpace.SOURCECODEPRO_REGULAR`
- **`FontSourceCode`**: Monospace font optimized for syntax highlighting in `drawlib.smartarts.SourceCode`.
  - `FontSourceCode.ROBOTO_MONO`
  - `FontSourceCode.SOURCECODEPRO`
  - `FontSourceCode.COURIER`

### 2.3. Regional Script Families
Specialized typography for international technical documentation:

- **`FontJapanese`**: Optimized glyphs for Japanese documentation (`Font.SANSSERIF_REGULAR` / `Font.SANSSERIF_BOLD` or system fonts).
- **`FontChinese`**: Optimized for Chinese documentation (`SIMPLIFIED_SANSSERIF_REGULAR`, `TRADITIONAL_SANSSERIF_REGULAR`).
- **`FontKorean`**: Optimized for Korean documentation (`Font.SANSSERIF_REGULAR`).
- **`FontArabic`**: Right-to-left cursive Arabic typography (`SANSSERIF_REGULAR`, `KUFI_REGULAR`, `NASKH_REGULAR`).
- **`FontThai`**: Thai script typography (`Font.SANSSERIF_REGULAR`).
- **`FontBrahmic`**: Devanagari and South Asian scripts (`DEVANAGARI_SANSSERIF_REGULAR`, `BENGALI_SANSSERIF_REGULAR`).

---

## 3. Custom Fonts via `FontFile`

To render text using an external TrueType (`.ttf`) or OpenType (`.otf`) font file:

```python
from drawlib.fonts import FontFile
from drawlib.text import text
from drawlib.types import Style

custom_font = FontFile("path/to/my_font.ttf")

text((50, 50), "Custom Typography", style=Style(text_font=custom_font, text_size=20))
```

---

## 4. Typography Hierarchy & Size Heuristics

When designing technical diagrams, maintain a clear typographic scale:

| Level | Recommended `text_size` | Recommended Weight | Example Use Case |
| :--- | :--- | :--- | :--- |
| **Diagram Title** | `22` - `26` | Bold (`FontRoboto.ROBOTO_BOLD`) | Top header or canvas title |
| **Container / Group Box** | `16` - `18` | Bold / Medium | Kubernetes pod boundary, VPC network label |
| **Node / Shape Title** | `13` - `15` | Bold (`white_bold`, `bold`) | Service names (`"Auth Service"`, `"Worker"`) |
| **Node Subtitle / Port** | `10` - `12` | Regular (`ROBOTO_REGULAR`) | Subtitle or protocol (`"port: 8080"`, `"POST /v1"`) |
| **Line Label** | `10` - `12` | Regular / Italic | Arrow description (`"gRPC (mTLS)"`) |

---

## 5. Practical Code Examples

### 5.1. Applying Roboto and Monospace Fonts in Architecture Schemas

```drawlib fold-code 600px center caption:"Typographic Scale with Roboto and Monospace"
from drawlib.canvas import config, save
from drawlib.fonts import FontMonoSpace, FontRoboto
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.text import text
from drawlib.types import Style

config(width=140, height=65)

# Header title
text((70, 56), "API Gateway Routing Schema", style=Style(text_font=FontRoboto.ROBOTO_BOLD, text_size=20))

# Service node with mixed typography
rectangle((40, 28), width=36, height=22, style="blue_flat")
text((40, 33), "Edge Gateway", style=Style(text_font=FontRoboto.ROBOTO_BOLD, text_size=14, text_color=(255, 255, 255)))
text((40, 23), "10.0.0.1:443", style=Style(text_font=FontMonoSpace.ROBOTO_MONO_REGULAR, text_size=11, text_color=(220, 235, 255)))

# Backend node
rectangle((100, 28), width=36, height=22, style="green_flat")
text((100, 33), "Payment Service", style=Style(text_font=FontRoboto.ROBOTO_BOLD, text_size=14, text_color=(255, 255, 255)))
text((100, 23), "10.0.1.15:8080", style=Style(text_font=FontMonoSpace.ROBOTO_MONO_REGULAR, text_size=11, text_color=(220, 255, 230)))

# Connecting arrow with technical label
line((58, 28), (82, 28), arrowhead="->", style="bold")
text((70, 32), "/v1/charges", style=Style(text_font=FontMonoSpace.ROBOTO_MONO_REGULAR, text_size=11))
```

### 5.2. Multilingual International Architecture Diagram

```drawlib fold-code 600px center caption:"Multilingual Diagram with Universal CJK Font"
from drawlib.canvas import config, save
from drawlib.fonts import Font
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.types import Style

config(width=120, height=50)

cjk_bold = Style(text_font=Font.SANSSERIF_BOLD, text_size=13, text_color=(255, 255, 255))

rectangle((30, 25), width=32, height=18, style="blue_flat", text="ユーザー認証\n(Auth)", textstyle=cjk_bold)
rectangle((90, 25), width=32, height=18, style="purple_flat", text="決済ゲートウェイ\n(Gateway)", textstyle=cjk_bold)
line((46, 25), (74, 25), arrowhead="->", style="bold")
```

---

## 6. Related Rules
- Text Alignment & Formatting: `uv run drawlib rules show text`
- Visual Styles: `uv run drawlib rules show preset_styles`
- Canvas Sizing: `uv run drawlib rules show canvas`
