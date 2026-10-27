# Drawlib SourceCode SmartArt Guidelines (`lib-smartarts-source-code`)

`SourceCode` renders syntax-highlighted code snippets directly as sharp vector shapes and text using Pygments tokenization.
Unlike stateful item-based SmartArts, `SourceCode` is stateless (attempting `SourceCode()` raises `TypeError`): render code directly via `SourceCode.draw(...)` or the `sourcecode(...)` function alias, and configure token styles via `SourceCodeStyles.get(...)` or the `get_source_code_styles(...)` function alias.

---

## 1. Supported Languages, CJK Fonts & Themes

- **Code Languages (`code_lang`)**:
  `"python"`, `"bash"`, `"go"`, `"rust"`, `"typescript"`, `"javascript"`, `"json"`, `"yaml"`, `"sql"`, `"docker"`, `"toml"`, `"c"`, `"c++"`, `"c#"`, `"java"`, `"kotlin"`, `"swift"`, `"html"`, `"css"`, `"protobuf"`, `"markdown"`, `"none"` / `"plain"` / `"text"`, etc. Passing `None` infers the lexer from `file` or guesses from `code`.
- **Font Languages (`font_lang`)**:
  `"en"` (default, uses `FontSourceCode.SOURCECODEPRO`), `"ja"`, `"zh-cn"`, `"zh-tw"`, `"ko"` (automatically selects `FontSourceCode.SOURCEHANCODEJP` for all tokens and line numbers so CJK comments and strings never render as tofu). You can also pass an explicit `font: FontSourceCode | FontFile | None = None` override.
- **Preset Themes (`styles`)**:
  - `"default"`: Slate light card with blue keywords, green strings, and red functions.
  - `"dark"` / `"monokai"` / `"github-dark"`: Dark editor card (`(39, 40, 34)`) with vibrant syntax tokens (`"github-dark"` and `"monokai"` are supported aliases for the dark theme).
  - `"google"`: Clean white Google-styled card with Google Blue/Green/Yellow/Red syntax tokens.
  - `"monochrome"`: High-contrast grayscale palette for black-and-white print documents.

---

## 2. `SourceCodeStyles` & `get_source_code_styles` API

```python
from drawlib.smartarts import (
    SourceCode,
    SourceCodeStyles,
    get_source_code_styles,
    sourcecode,
)

# Classmethod or function alias (identical signature)
styles = SourceCodeStyles.get(
    styles: str = "default",
    font_lang: str = "en",
    *,
    font: FontSourceCode | FontFile | None = None,
    text_size: float = 12.0,
) -> SourceCodeStyles

styles = get_source_code_styles(
    styles: str = "default",
    font_lang: str = "en",
    *,
    font: FontSourceCode | FontFile | None = None,
    text_size: float = 12.0,
) -> SourceCodeStyles
```

### Customizing Token & Box Styles (`SourceCodeStyles.patch`)

`SourceCodeStyles` is a frozen Pydantic model with attributes `box_style`, `linenum_style`, `default`, `keyword`, `string`, `comment`, `number`, `function`, `type_`, and `operator`. Create a customized copy via `.patch(...)`:

```python
custom_styles = styles.patch(
    *,
    box_style: Style | None = None,
    linenum_style: Style | None = None,
    default: Style | None = None,
    keyword: Style | None = None,
    string: Style | None = None,
    comment: Style | None = None,
    number: Style | None = None,
    function: Style | None = None,
    type_: Style | None = None,
    type: Style | None = None,      # Convenience alias for type_
    operator: Style | None = None,
    text_size: float | None = None, # Updates text_size across all 9 token/linenum styles at once
) -> SourceCodeStyles
```

---

## 3. `SourceCode.draw`, `sourcecode`, & `SourceCode.get_text`

```python
SourceCode.draw(
    xy: tuple[float, float],           # Anchor coordinate (x, y) of the code container
    width: float,                      # Total container width in canvas units
    code: str | None = None,           # Code string to render (mutually exclusive with `file`)
    *,
    styles: SourceCodeStyles,          # Required style configuration
    file: str | None = None,           # Path to source file (mutually exclusive with `code`)
    code_lang: str | None = None,      # Language: "python", "json", "yaml", "sql", etc.
    show_linenum: bool = False,        # Whether to display line numbers in a left gutter
    align: Literal["top_left", "bottom_left", "center"] = "top_left",
    scale: float = 1.0,                # Proportional scaling anchored at xy
) -> type[SourceCode]

# Function alias with identical parameters:
sourcecode(
    xy: tuple[float, float],
    width: float,
    code: str | None = None,
    *,
    styles: SourceCodeStyles,
    file: str | None = None,
    code_lang: str | None = None,
    show_linenum: bool = False,
    align: Literal["top_left", "bottom_left", "center"] = "top_left",
    scale: float = 1.0,
) -> None

# Helper to load code text from a relative or absolute file path:
code_text = SourceCode.get_text(
    file: str,
    strip: bool = True,
) -> str
```

- **Height Calculation**: Container height is computed automatically from the number of lines in `code` / `file` and `styles.default.text_size`.
- **Anchor (`align`)**: Defaults to `"top_left"` (container extends rightward `+x` and downward `-y`), or pass `align="bottom_left"` / `align="center"`.

---

## 4. Production Example: Embedded Configuration Block

```drawlib code=show
from drawlib.canvas import save, setup
from drawlib.shapes import rectangle
from drawlib.smartarts import SourceCode, SourceCodeStyles
from drawlib.styles import Styles

setup(width=110, height=105)

# Outer window frame
rectangle(xy=(55, 52.5), width=96, height=95, style=Styles.DarkSolid.patch(shape_r=2))
# Header bar
rectangle(
    xy=(55, 94),
    width=96,
    height=12,
    style=Styles.DarkFlat.patch(shape_r=2),
    text="Kubernetes Deployment Spec (v1)",
    text_style=Styles.WhiteBold.patch(text_size=11.0),
)

k8s_yaml = """apiVersion: apps/v1
kind: Deployment
metadata:
  name: auth-service
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: auth-service
  template:
    spec:
      containers:
      - name: auth
        image: gcr.io/company/auth:v1.4.2"""

code_styles = SourceCodeStyles.get("github-dark", font_lang="en", text_size=10.0)
SourceCode.draw(
    xy=(11, 86),
    width=88,
    code=k8s_yaml,
    styles=code_styles,
    code_lang="yaml",
    show_linenum=True,
    align="top_left",
)
save()
```
