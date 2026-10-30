# Drawlib Slide Presentation & Stage Guidelines

This document covers the **`drawlib.slide` Python module API** (`current_slide`, `draw_page_number()`, `draw_section_header()`, `SlideContext`, `BoundingBox`, `build_slide()`, and `build_pptx()`).

*(For Markdown slide authoring, 1920×1080 stage coordinates, `::: block` and `::: note` syntax, layout templates, interactive animations, and Presenter View, run `uv run drawlib rules show project-slide`.)*

---

## 1. Public API Overview (`drawlib.slide`)

All slide runtime helpers, stage/page helpers, data models, and compilation functions are imported from `drawlib.slide`:

```python
from drawlib.slide import (
    BoundingBox,
    SlideContext,
    build_pptx,
    build_slide,
    current_slide,
    draw_page_number,
    draw_section_header,
)
```

| Symbol | Category | Description |
| :--- | :--- | :--- |
| `current_slide` | Runtime Proxy | Dynamic `contextvars`-backed proxy exposing the active slide's 1-based index and total slide count during deck compilation. |
| `draw_page_number` | Stage Helper | Renders a standardized bottom-right slide counter badge (`current_slide.text` or custom `template`) on a transparent canvas (`14×3`, `alpha=0.0`). |
| `draw_section_header` | Stage Helper | Renders a full-bleed 16:9 section header slide (`192×108`) with 4 selectable layout variants (`"split"`, `"centered"`, `"banner"`, `"minimal"`). |
| `SlideContext` | Frozen Dataclass | Immutable context model (`index: int = 1`, `total: int = 1`) holding slide numbering state. |
| `BoundingBox` | Frozen Dataclass | Immutable stage geometry model (`x: float`, `y: float`, `width: float`, `height: float`) in 1920×1080 stage pixels. |
| `build_slide` | Compiler Function | Programmatically compiles a `slide_src/` Markdown directory into a standalone HTML presentation deck. |
| `build_pptx` | Compiler Function | Programmatically compiles a `slide_src/` Markdown directory into a native editable 16:9 MS PowerPoint (`.pptx`) presentation deck. |

---

## 2. Dynamic Slide Counter (`current_slide`) & `draw_page_number()`

`current_slide` is a dynamic runtime proxy (`_CurrentSlideProxy`) that reads the active `SlideContext` during `build_slide()` execution. When evaluated outside slide compilation (e.g., standalone script execution), it safely defaults to `index=1`, `total=1` (`"1 / 1"`).

### 2.1. `current_slide` Properties & Methods

| Property / Method | Return Type | Description | Example Output |
| :--- | :--- | :--- | :--- |
| `current_slide.index` | `int` | Current 1-based slide index in sorted deck order. | `4` |
| `current_slide.total` | `int` | Total number of slides in the presentation deck. | `9` |
| `current_slide.text` | `str` | Standard formatted slide counter string (`"{index} / {total}"`). | `"4 / 9"` |
| `current_slide.format(template)` | `str` | Custom formatted string using `{index}` and `{total}` placeholders. | `current_slide.format("Slide {index} of {total}")` → `"Slide 4 of 9"` |
| `str(current_slide)` | `str` | Equivalent to `current_slide.text`. | `"4 / 9"` |

### 2.2. Built-In Page Number Helper (`draw_page_number`)

Use `draw_page_number()` directly inside a bottom-right `::: block xy=(1700, 1010) width=140 height=30` block:

````markdown
::: block xy=(1700, 1010) width=140 height=30
```drawlib file=page.svg
from drawlib.slide import draw_page_number

draw_page_number()
```
:::
````

```python
draw_page_number(
    width=14,
    height=3,
    *,
    template="{index} / {total}",
    style=None,        # Defaults to Styles.Muted.patch(text_size=65.0)
    auto_setup=True,   # Calls clear() and setup(width=width, height=height, alpha=0.0)
)
```

---

## 3. Full-Bleed Section Header Helper (`draw_section_header`)

Use `draw_section_header()` inside a full-bleed `::: block xy=(0, 0) width=1920 height=1080` block (`01_section.md`) to render a chapter/section divider slide:

````markdown
::: block xy=(0, 0) width=1920 height=1080
```drawlib file=section_cover.svg
from drawlib.slide import draw_section_header

draw_section_header(
    2,
    "Core Engine & Primitives",
    "Cartesian Geometry, Shapes, Connectors, Typography & Design Tokens",
    [
        "Coordinate System & Canvas Lifecycle",
        "23 Geometric Shapes & 10 Line Connectors",
        "Semantic Style Presets & Typography",
    ],
    total_sections=5,
    variant="split",
)
```
:::
````

### 3.1. Layout Variants (`variant`)

| `variant` | Visual Structure (`192.0 × 108.0` Canvas) | Topic Cards (`topics`) | Best For |
| :--- | :--- | :--- | :--- |
| **`"split"`** *(default)* | Left dark panel (`w=72`, `Styles.DarkFlat`) with large 2-digit section number (`01`) and progress dots; vertical `Styles.PrimaryFlat` bar; right neutral panel (`w=120`, `Styles.Neutral`). | Vertical `CardList(badge_shape="circle")` on the lower-right panel (auto-centers title vertically when `topics=()`). | Technical deep-dive decks previewing 3–5 topics per chapter. |
| **`"centered"`** | Full neutral canvas with top accent bar and centered pill (`SECTION 01 • Part 1 of 5`), hero title, subtitle, and accent underline. | Horizontal `CardList(badge_shape="circle")` across the lower half. | Keynote-style talks, executive summaries, or clean chapter transitions without topics. |
| **`"banner"`** | Full-width top `Styles.DarkFlat` hero band with rounded `Styles.PrimaryFlat` number badge box, white title/subtitle, and top-right progress dots. | Horizontal `CardList(badge_shape="rounded_rect")` in the lower workspace. | Highlighting multi-part themes or parallel tracks side by side. |
| **`"minimal"`** | Light editorial `Styles.Neutral` canvas with a left vertical `Styles.PrimaryFlat` accent stripe and compact `SECTION 01` pill. | Wide vertical `CardList(badge_shape="rounded_rect")` below the horizontal rule. | RFC/spec-style decks and **`MonochromeStyles` / print PDFs** avoiding heavy dark fills. |

### 3.2. Key Parameters
- `section_num: int`: 1-based section number (`>= 1`).
- `title: str`: Main section title.
- `subtitle: str = ""`: Optional one-line subtitle.
- `topics: Sequence[str | tuple[str, str]] = ()`: Optional list of topic titles or `(title, description)` pairs.
- `total_sections: int = 0`: Total sections in the deck (`> 0` displays progress dots and `"Part X of Y"` badge; `0` omits them).
- `variant: Literal["split", "centered", "banner", "minimal"] = "split"`: Layout pattern.
- `section_label: str = "SECTION"`: Label text (e.g. `"SECTION"`, `"CHAPTER"`, `"ACT"`).
- `badge_text: str | None = None`: Custom badge override (e.g. `"Act I — Detection"`).
- `show_page_number: bool = True`, `show_decorations: bool = True`, `auto_setup: bool = True`.
- Optional `Style | None` overrides for every element (`left_panel_style`, `right_panel_style`, `divider_bar_style`, `title_style`, `subtitle_style`, `topic_card_style`, `topic_badge_style`, etc.).

---

## 4. Slide Context Model (`SlideContext`)

`SlideContext` is the underlying frozen dataclass stored in a Python `contextvars.ContextVar` during slide compilation:

```python
from drawlib.slide import SlideContext

ctx = SlideContext(index=3, total=10)
assert ctx.index == 3
assert ctx.total == 10
assert ctx.text == "3 / 10"
assert ctx.format("{index} of {total}") == "3 of 10"
```

| Attribute / Method | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `index` | `int` | `1` | 1-based index of the current slide. |
| `total` | `int` | `1` | Total number of slides in the deck. |
| `text` | `str` *(property)* | `"1 / 1"` | Returns `f"{self.index} / {self.total}"`. |
| `format(template="{index} / {total}")` | `str` | — | Formats `template` with `index=self.index, total=self.total`. |

---

## 5. Stage Bounding Box Model (`BoundingBox`)

`BoundingBox` is an immutable dataclass representing a rectangular region on the 1920×1080 pixel presentation stage:

```python
from drawlib.slide import BoundingBox

box = BoundingBox(x=80.0, y=140.0, width=740.0, height=840.0)
```

| Attribute | Type | Description |
| :--- | :--- | :--- |
| `x` | `float` | Horizontal coordinate of the top-left corner in stage pixels (`0` to `1920`). |
| `y` | `float` | Vertical coordinate of the top-left corner in stage pixels (`0` to `1080`). |
| `width` | `float` | Width of the bounding box in stage pixels. |
| `height` | `float` | Height of the bounding box in stage pixels. |

---

## 6. Programmatic Slide Compilation API (`build_slide`)

`build_slide()` compiles a directory of slide Markdown files (`01_title.md`, `02_agenda.md`, etc.) into a standalone interactive HTML presentation deck:

```python
from drawlib.slide import build_slide

output_index_html = build_slide(
    input_dir="docs/slide_about_drawlib_src",
    output_dir="docs/slide_about_drawlib_html",
    title="Drawlib Presentation",
    theme="default",
    image_format="svg",
    styles_path=None,
    utils_path=None,
    no_cache=False,
)
```

### 6.1. Parameter Reference

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `input_dir` | `str` | *(required)* | Source directory containing slide `.md` files, `_assets/`, `style.css`, `slide.js`, `styles.py`, and `utils.py`. |
| `output_dir` | `str \| None` | `None` | Target output directory. If `None` and `input_dir` ends with `_src`, resolves to `input_dir[:-4]`; otherwise `<input_dir>/slide`. |
| `title` | `str \| None` | `None` | Optional HTML `<title>` override. If `None`, automatically extracted from the first `# Heading` of the first slide. |
| `theme` | `str \| None` | `None` | Optional presentation theme identifier (`data-theme` attribute on `<body>`). |
| `image_format` | `str` | `"svg"` | Default output format (`"svg"`, `"webp"`, `"png"`) for ````drawlib```` blocks that do not specify an explicit file extension. |
| `styles_path` | `str \| None` | `None` | Optional path to a custom `styles.py` file (defaults to `<input_dir>/styles.py` if present). |
| `utils_path` | `str \| None` | `None` | Optional path to a custom `utils.py` file (defaults to `<input_dir>/utils.py` if present). |
| `no_cache` | `bool` | `False` | When `True`, bypasses the SQLite diagram build cache and forces re-execution of all ````drawlib```` blocks. |

**Returns**: `str` — Absolute filesystem path to the generated `index.html` file.

### 6.2. Compilation Pipeline & Output Artifacts
When `build_slide()` runs, it performs the following steps automatically:
1. **Slide Discovery**: Collects and sorts all `.md` / `.markdown` files in `input_dir`, automatically excluding files and subdirectories starting with `_` or `.` (e.g., `_planning.md`, `_drafts/`, `_assets/`) as well as special files (`README.md`, `navbar.md`).
2. **Slide Context Binding**: Iterates through slides `1..N`, setting `SlideContext(index=idx, total=N)` so `current_slide` resolves accurately inside every ````drawlib```` block.
3. **Diagram Rendering & Inline SVG Embedding**: Compiles ````drawlib```` blocks into `images/<slide_stem>/` (with SQLite hash caching) and inlines `.svg` diagrams or attaches interactive `<canvas>` players for `.webp` / `.png` animations.
4. **Speaker Notes & Container Blocks**: Extracts `::: note` blocks into `<aside class="slide-notes" hidden>` and transforms `::: block xy=(x, y) width=W height=H` into positioned `<div class="slide-block">` stage elements.
5. **Asset Deployment & SVG Font Auto-Bundling**: Copies `_assets/`, `slide.js`, and `style.css` to `output_dir`, and automatically bundles any TTF/OTF text or icon fonts referenced by inline SVGs into `_assets/fonts/` with `@font-face` rules injected into `style.css`.

---

## 7. Programmatic MS PowerPoint Export API (`build_pptx`)

`build_pptx()` (also re-exported from `drawlib.tools`) measures the `1920x1080` slide DOM via headless Chromium and writes native editable 16:9 (`960x540 pt`) Microsoft PowerPoint (`.pptx`) slides (`::: block` cards including `rgba` alpha, text boxes, bullet/numbered lists, tables, code blocks, and `::: note` speaker notes), with ````drawlib```` diagrams embedded as high-DPI static PNGs (default `dpi=240`, `anim_frame="last"`):

```python
from drawlib.slide import build_pptx

output_pptx = build_pptx(
    input_dir="docs/slide_about_drawlib_src",
    output_file="docs/slide_about_drawlib.pptx",
    title="Drawlib Presentation",
    theme="default",
    dpi=240,
    anim_frame="last",
    styles_path=None,
    utils_path=None,
    no_cache=False,
    timestamp=False,
)
```

### 7.1. Parameter Reference

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `input_dir` | `str` | *(required)* | Source directory containing slide `.md` files, `_assets/`, `style.css`, `styles.py`, and `utils.py`. |
| `output_file` | `str \| None` | `None` | Target `.pptx` file path. If `None`, resolves to `<stem>.pptx` alongside `input_dir`. |
| `title` | `str \| None` | `None` | Optional presentation title override in `.pptx` core properties (extracted from first `# Heading` if `None`). |
| `theme` | `str \| None` | `None` | Optional CSS theme preset override (`data-theme` / built-in slide stylesheet). |
| `dpi` | `int` | `240` | Rasterization DPI for embedded ````drawlib```` static PNG diagrams. |
| `anim_frame` | `Literal["first", "last"]` | `"last"` | Frame extracted as a static PNG when a slide block uses `Animation()`. |
| `styles_path` | `str \| None` | `None` | Optional path to a custom `styles.py` file (defaults to `<input_dir>/styles.py` if present). |
| `utils_path` | `str \| None` | `None` | Optional path to a custom `utils.py` file (defaults to `<input_dir>/utils.py` if present). |
| `no_cache` | `bool` | `False` | When `True`, bypasses the SQLite diagram build cache and forces re-execution of all ````drawlib```` blocks. |
| `timestamp` | `bool` | `False` | When `True`, writes the current build timestamp into `.pptx` metadata instead of deterministic normalization. |

**Returns**: `str` — Filesystem path to the generated `.pptx` file.

*(Note: `playwright` and `python-pptx` are standard dependencies of `drawlib`. Headless Chromium (`chromium-headless-shell`) downloads automatically on first `build_pdf` or `build_pptx` run, or can be pre-cached offline via `drawlib cache download --browser` / `--all`. In minimal Linux containers such as `python:3.12-slim` lacking OS shared libraries, run `playwright install-deps chromium`.)*

---

## 8. Slide Design Best Practices (`slide-guide`) & Project System Guide (`project-slide`)

- **Slide Design & Storytelling Best Practices (`slide-guide`)**: For the **Dual-Layer (`::: block` simple visual stage + `::: note` deep explanation) rule**, mandatory Cover / Agenda / Section Divider arc, layout variety, and high-level component selection, run:
  ```bash
  uv run drawlib rules show slide-guide
  ```
- **Slide Project System & Stage Syntax (`project-slide`)**: For `slide_src/` file discovery (`_` prefix and `README.md` exclusion), `1920×1080` stage coordinates, `::: block` / `::: note` syntax, interactive animations (`anim_trigger`, `anim_loop`, `anim_pause`), Presenter View (`?presenter=1`), and `.pdf` / `.pptx` export, run:
  ```bash
  uv run drawlib rules show project-slide
  ```
