# Drawlib Canvas Guidelines

The `canvas` is the foundational drawing surface of Drawlib.  
Drawlib operates on an **"Illustration as Code"** model: canvas dimensions, resolution, background coloring, coordinate grids, and output generation are controlled entirely through declarative Python function calls.

---

## 1. Imports & Core Architecture

All canvas lifecycle functions can be imported from `drawlib.canvas`:

```python
from drawlib.canvas import (
    canvas,       # Underlying singleton Canvas instance
    clear,        # Reset canvas state and options between images
    config,       # Set canvas dimensions, grid, background color, DPI
    get_dimage,   # Render canvas in-memory and return a Dimage object
    initialize,   # Re-initialize the drawing environment (calls clear())
    save,         # Save canvas drawing to an image file on disk
    show,         # Display canvas in a local desktop preview window
)
```

### Canvas Lifecycle Model
Drawlib maintains an internal canvas state. When drawing functions (`rectangle()`, `circle()`, `line()`, `text()`, etc.) are called, visual elements ("artists") are registered to the active canvas.

```text
               ┌────────────────────────────────────────────────────────┐
               │                     CANVAS LIFECYCLE                   │
               └────────────────────────────────────────────────────────┘

1. Configure Canvas              2. Draw Elements               3. Output Result
┌───────────────────────┐       ┌──────────────────────┐       ┌────────────────────────┐
│ config(width, height) │ ────> │ shapes, lines, text, │ ────> │ save() / show()        │
│ Set size, grid, bg    │       │ smartarts, diagrams  │       │ Export to file or view │
└───────────────────────┘       └──────────────────────┘       └────────────────────────┘
            ▲                                                               │
            │                                                               │
            └────────────────────────── clear() ────────────────────────────┘
                               Reset state for next image
```

> **Crucial Rule for Multi-Image Scripts**:  
> Always call `clear()` between sequential drawings in the same script. If `clear()` is omitted, shapes from earlier drawings bleed onto the subsequent canvases.

---

## 2. Coordinate System & Geometry

Drawlib uses a mathematical Cartesian coordinate space:

- **Origin `(0, 0)`**: Strictly located at the **bottom-left corner** of the canvas.
- **X-Axis**: Increases horizontally from left to right (`0` to `width`).
- **Y-Axis**: Increases vertically from bottom to top (`0` to `height`).
- **Default Anchor**: Shape and text coordinates `(x, y)` refer to the **geometric center** by default (unless alignment parameters such as `text_halign` or `text_valign` are customized).

```text
  Y ^
    │ (0, height)                                 (width, height)
    │  ┌──────────────────────────────────────────────┐
    │  │                                              │
    │  │                                              │
    │  │                   (cx, cy)                   │
    │  │               [Center Anchor]                │
    │  │                                              │
    │  │                                              │
    │  └──────────────────────────────────────────────┘
    │ (0, 0)                                      (width, 0)
────┼─────────────────────────────────────────────────────────> X
  0 │
```

### Canvas Sizing Heuristics
Choose dimensions according to diagram scope:
- **Small Badge / Icon / Pill**: `config(width=80, height=40)`
- **Standard Component Diagram / Flowchart**: `config(width=140, height=70)`
- **Widescreen 16:9 Architectural Schema**: `config(width=160, height=90)`
- **High-Density Dashboard / Data Pipeline**: `config(width=200, height=100)`

---

## 3. Function Specifications

### 3.1. `config()`
Configures canvas geometry, resolution, coordinate grids, and background appearance.

```python
config(
    width: int | None = None,
    height: int | None = None,
    dpi: int | None = None,
    background_color: tuple[int, int, int] | tuple[int, int, int, float] | None = None,
    background_alpha: float | None = None,
    grid: bool | None = None,
    grid_only: bool | None = None,
    grid_style: Style | None = None,
    grid_centerstyle: Style | None = None,
    grid_xpitch: int | None = None,
    grid_ypitch: int | None = None,
)
```

#### Parameter Breakdown:
| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `width` | `int` | `100` | Canvas width in logical coordinate units. |
| `height` | `int` | `100` | Canvas height in logical coordinate units. |
| `dpi` | `int` | `100` | Dots per inch for rasterization and image sharpness. |
| `background_color` | `tuple` | `(255, 255, 255)` | Canvas background color (RGB or RGBA). |
| `background_alpha` | `float` | `1.0` | Background transparency (`0.0` = fully transparent, `1.0` = opaque). |
| `grid` | `bool` | `False` | Overlays coordinate grid lines with center axes. |
| `grid_only` | `bool` | `False` | Renders coordinate grid only (useful for design scaffolding). |
| `grid_style` | `Style` | Gray dashed | Custom line style for standard grid lines. |
| `grid_centerstyle`| `Style` | Bold gray dashed | Custom line style for center axes (`x=width/2`, `y=height/2`). |
| `grid_xpitch` | `int` | `width / 10` | Spacing between vertical grid lines. |
| `grid_ypitch` | `int` | `height / 10` | Spacing between horizontal grid lines. |

### 3.2. `save()`
Exports the current canvas drawing to an image file on disk.

```python
save(
    file: str | None = None,
    format: str | None = None,
)
```

- **`file`**: Path to the output image file.
  - If omitted, Drawlib saves the image as `<script_name>.png` in the directory of the running script.
  - Supports absolute paths or relative paths.
- **`format`**: File format extension (`"png"`, `"svg"`, `"pdf"`, `"webp"`). If omitted, inferred from the filename extension or defaults to `"png"`.

### 3.3. `show()`
Opens an interactive desktop GUI window showing the rendered illustration.  
- In headless environments (CI/CD, Docker, remote AI sessions), use `save()` or CLI `drawlib export` instead.

### 3.4. `clear()` and `initialize()`
Resets canvas geometry, removes all registered artists, and restores default configuration settings.
- `initialize()` is a convenience alias for `clear()`.

### 3.5. `get_dimage() -> Dimage`
Renders the canvas in-memory into a Drawlib `Dimage` object without saving to disk.
- Ideal for image processing pipelines, combining diagrams dynamically, or testing assertions in unit tests.

---

## 4. Practical Code Examples

### 4.1. Basic Architecture Diagram with Custom Dimensions

```drawlib fold-code 600px center caption:"Basic Microservices Architecture"
from drawlib.canvas import config, save
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.text import text

# Configure a 140x60 canvas with a subtle light background
config(width=140, height=60, background_color=(248, 249, 250))

# Service nodes
rectangle((30, 30), width=32, height=18, style=styles.blue_flat, text="Web Frontend", textstyle=styles.white_bold)
rectangle((75, 30), width=32, height=18, style=styles.purple_flat, text="API Gateway", textstyle=styles.white_bold)
rectangle((120, 30), width=32, height=18, style=styles.green_flat, text="Auth Service", textstyle=styles.white_bold)

# Connecting lines with arrowheads
line((46, 30), (59, 30), arrowhead="->", style=styles.bold)
line((91, 30), (104, 30), arrowhead="->", style=styles.bold)

# Annotations
text((70, 52), "System Boundary", style=styles.bold)
```

### 4.2. Transparent Canvas for Embedded Badges

```drawlib fold-code 500px center caption:"Transparent Status Pill"
from drawlib.canvas import config, save
from drawlib.colors import Colors
from drawlib.shapes import rectangle

# 0.0 alpha produces a transparent PNG background
config(width=80, height=30, background_alpha=0.0)

# Rounded status pill
rectangle(
    (40, 15),
    width=72,
    height=22,
    r=11,
    style=styles.green_flat,
    text="DEPLOYED - v2.4.0",
    textstyle=styles.white_bold,
)
```

### 4.3. Multi-Image Sequential Generation

When writing standalone Python scripts producing multiple assets:

```python
from drawlib.canvas import clear, config, save
from drawlib.preset_styles import get_styles
from drawlib.shapes import circle, rectangle

styles = get_styles()

# Image 1: Architecture
config(width=120, height=60)
rectangle((60, 30), width=40, height=20, style=styles.blue_flat, text="Stage 1")
save("output_stage1.png")

# ALWAYS CLEAR BEFORE NEXT IMAGE
clear()

# Image 2: Deployment
config(width=100, height=100)
circle((50, 50), radius=30, style=styles.green_flat, text="Stage 2")
save("output_stage2.png")
```

---

## 5. Related Rules
- Shapes Primitives: `uv run drawlib rules show shapes`
- Lines & Arrowhead Routing: `uv run drawlib rules show lines`
- Visual Styles & Palettes: `uv run drawlib rules show preset_styles`
- CLI & Fast Verification: `uv run drawlib rules show cli`
