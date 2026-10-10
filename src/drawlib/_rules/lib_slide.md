# Drawlib Slide Presentation & Stage Guidelines

This document covers the **`drawlib.slide` Python module API** (`current_slide`, `SlideContext`, `BoundingBox`, and `build_slide()`).

*(For Markdown slide authoring, 1920×1080 stage coordinates, `::: block` and `::: note` syntax, layout templates, interactive animations, and Presenter View, run `uv run drawlib rules show project-slide`.)*

---

## 1. Public API Overview (`drawlib.slide`)

All slide runtime helpers, data models, and compilation functions are imported from `drawlib.slide`:

```python
from drawlib.slide import (
    BoundingBox,
    SlideContext,
    build_slide,
    current_slide,
)
```

| Symbol | Category | Description |
| :--- | :--- | :--- |
| `current_slide` | Runtime Proxy | Dynamic `contextvars`-backed proxy exposing the active slide's 1-based index and total slide count during deck compilation. |
| `SlideContext` | Frozen Dataclass | Immutable context model (`index: int = 1`, `total: int = 1`) holding slide numbering state. |
| `BoundingBox` | Frozen Dataclass | Immutable stage geometry model (`x: float`, `y: float`, `width: float`, `height: float`) in 1920×1080 stage pixels. |
| `build_slide` | Compiler Function | Programmatically compiles a `slide_src/` Markdown directory into a standalone HTML presentation deck. |

---

## 2. Dynamic Slide Counter (`current_slide`)

`current_slide` is a dynamic runtime proxy (`_CurrentSlideProxy`) that reads the active `SlideContext` during `build_slide()` execution. When evaluated outside slide compilation (e.g., standalone script execution), it safely defaults to `index=1`, `total=1` (`"1 / 1"`).

### 2.1. Properties & Methods

| Property / Method | Return Type | Description | Example Output |
| :--- | :--- | :--- | :--- |
| `current_slide.index` | `int` | Current 1-based slide index in sorted deck order. | `4` |
| `current_slide.total` | `int` | Total number of slides in the presentation deck. | `9` |
| `current_slide.text` | `str` | Standard formatted slide counter string (`"{index} / {total}"`). | `"4 / 9"` |
| `current_slide.format(template)` | `str` | Custom formatted string using `{index}` and `{total}` placeholders. | `current_slide.format("Slide {index} of {total}")` → `"Slide 4 of 9"` |
| `str(current_slide)` | `str` | Equivalent to `current_slide.text`. | `"4 / 9"` |

### 2.2. Standard Usage: Reusable Page Number Helper in `utils.py`

In a slide project (`slide_src/utils.py`), define a reusable helper that renders `current_slide.text` on a transparent canvas (`alpha=0.0`):

```python
# slide_src/utils.py
from drawlib.canvas import clear, setup
from drawlib.slide import current_slide
from drawlib.styles import Style, Styles
from drawlib.text import text


def draw_page_number(
    width: int = 14,
    height: int = 3,
    style: Style | None = None,
) -> None:
    """Draw a standardized slide page number badge."""
    clear()
    setup(width=width, height=height, alpha=0.0)
    effective_style = style or Styles.Black.patch(
        text_size=65,
        text_color=(128, 128, 128),
    )
    text((width / 2.0, height / 2.0), current_slide.text, style=effective_style)
```

Then embed it in the bottom-right corner (`(1700, 1010) (140, 30)`) of any slide Markdown file:

````markdown
::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils
utils.draw_page_number()
```
:::
````

---

## 3. Slide Context Model (`SlideContext`)

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

## 4. Stage Bounding Box Model (`BoundingBox`)

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

## 5. Programmatic Slide Compilation API (`build_slide`)

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

### 5.1. Parameter Reference

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

### 5.2. Compilation Pipeline & Output Artifacts
When `build_slide()` runs, it performs the following steps automatically:
1. **Slide Discovery**: Collects and sorts all `.md` / `.markdown` files in `input_dir`, automatically excluding files and subdirectories starting with `_` or `.` (e.g., `_planning.md`, `_drafts/`, `_assets/`) as well as special files (`README.md`, `navbar.md`).
2. **Slide Context Binding**: Iterates through slides `1..N`, setting `SlideContext(index=idx, total=N)` so `current_slide` resolves accurately inside every ````drawlib```` block.
3. **Diagram Rendering & Inline SVG Embedding**: Compiles ````drawlib```` blocks into `images/<slide_stem>/` (with SQLite hash caching) and inlines `.svg` diagrams or attaches interactive `<canvas>` players for `.webp` / `.png` animations.
4. **Speaker Notes & Container Blocks**: Extracts `::: note` blocks into `<aside class="slide-notes" hidden>` and transforms `::: block (x, y) (w, h)` into positioned `<div class="slide-block">` stage elements.
5. **Asset Deployment & SVG Font Auto-Bundling**: Copies `_assets/`, `slide.js`, and `style.css` to `output_dir`, and automatically bundles any TTF/OTF text or icon fonts referenced by inline SVGs into `_assets/fonts/` with `@font-face` rules injected into `style.css`.

---

## 6. Slide Design Best Practices (`slide-guide`) & Project System Guide (`project-slide`)

- **Slide Design & Storytelling Best Practices (`slide-guide`)**: For the **Dual-Layer (`::: block` simple visual stage + `::: note` deep explanation) rule**, mandatory Cover / Agenda / Section Divider arc, layout variety, and high-level component selection, run:
  ```bash
  uv run drawlib rules show slide-guide
  ```
- **Slide Project System & Stage Syntax (`project-slide`)**: For `slide_src/` file discovery (`_` prefix and `README.md` exclusion), `1920×1080` stage coordinates, `::: block` / `::: note` syntax, interactive animations (`anim-trigger`, `anim-loop`, `anim-pause`), and Presenter View (`?presenter=1`), run:
  ```bash
  uv run drawlib rules show project-slide
  ```
