# Drawlib Slide Presentation & Stage Guidelines

Drawlib provides native support for generating modern, high-resolution **16:9 widescreen presentation slide decks** with embedded vector diagrams and interactive web features.  
Slides are authored in declarative Markdown files under `slide_src/`, compiled into standalone static HTML presentation decks (`slide_html/index.html` + `slide.js`), and exported to print-ready vector presentation PDFs (`slide.pdf`).

---

## 1. Architecture & Slide Stage Concept

### 1.1. Universal 16:9 Presentation Stage (1920x1080)
Drawlib presentation slides render on a fixed **1920x1080 pixel stage** with a standard 16:9 widescreen aspect ratio.  
The coordinate origin `(0, 0)` is located at the **bottom-left corner** of the slide stage, consistent with Drawlib's Cartesian geometry.

```text
(0, 1080) ┌────────────────────────────────────────┐ (1920, 1080)
          │  Header & Slide Title                  │
          │                                        │
          │  Stage Content Area                    │
          │  (Markdown, Diagrams, SmartArts)       │
          │                                        │
          │  Footer / Slide Counter (current_slide)│
  (0, 0)  └────────────────────────────────────────┘ (1920, 0)
```

---

## 2. Public API (`drawlib.slide`)

All slide-specific runtime helpers and models are imported from `drawlib.slide`:

```python
from drawlib.slide import BoundingBox, SlideContext, build_slide, current_slide
```

### 2.1. Dynamic Slide Counter (`current_slide`)
`current_slide` is a dynamic runtime proxy providing access to the current slide number and total slide count:

| Property / Method | Returns | Description | Example |
| :--- | :--- | :--- | :--- |
| `current_slide.index` | `int` | Current 1-based slide index. | `4` |
| `current_slide.total` | `int` | Total number of slides in the deck. | `9` |
| `current_slide.text` | `str` | Formatted slide counter. | `"4 / 9"` |
| `current_slide.format(template)` | `str` | Custom formatted slide counter. | `current_slide.format("{index} of {total}")` |

#### Drawing Slide Numbers on Canvas:
```python
from drawlib.canvas import save, setup
from drawlib.slide import current_slide
from drawlib.styles import Styles
from drawlib.text import text

setup(width=120, height=20)
# Renders e.g. "4 / 9" in bottom-right corner:
text((110, 10), current_slide.text, style=Styles.MutedSmall)
```

### 2.2. Bounding Box Model (`BoundingBox`)
Represents an explicit layout area on the 1920x1080 slide stage:

```python
from drawlib.slide import BoundingBox

box = BoundingBox(x=100.0, y=200.0, width=800.0, height=600.0)
```

### 2.3. Slide Compilation API (`build_slide`)
Programmatically compiles a slide project directory into an interactive presentation deck:

```python
from drawlib.slide import build_slide

build_slide(
    input_dir="slide_src/",
    output_dir="slide_html/",
    image_format="webp",
    style_theme="default",
)
```

---

## 3. Slide Authoring in Markdown (`slide_src/`)

Each slide in a presentation deck is authored as an independent Markdown file sorted numerically or alphabetically:

```text
slide_src/
├── 01_title.md            # Title / Cover slide
├── 02_agenda.md           # Table of contents
├── 03_architecture.md     # Architectural diagram slide
├── 04_workflow.md         # Process pipeline slide
├── _assets/               # Presentation images and icons
├── styles.py              # Deck-wide styling and color overrides
├── utils.py               # Slide layout helpers (cards, badges, grids)
├── slide.css              # Custom presentation stylesheet
├── build.sh               # Master build script
├── build_html.sh          # HTML presentation deck compilation
├── build_pdf.sh           # Vector PDF export via headless Chromium
└── serve.sh               # Local presentation preview server
```

### 3.1. Frontmatter Configuration
Each slide file can specify optional YAML frontmatter:

```markdown
---
title: System Architecture Overview
layout: default
background: "#0f172a"
---

# Microservices Topologies
```

---

## 4. Layout Containers (`::: block` and `::: box`)

Drawlib slides support flexible container blocks with absolute and slot-based positioning:

```markdown
::: block xy: (100, 200) size: (800, 600)
### Left Content Column
- High-throughput API gateway
- Asynchronous message bus
:::

::: block xy: (1000, 200) size: (800, 600)
```drawlib file:arch_diagram.png
from drawlib.canvas import setup
from drawlib.shapes import rectangle
from drawlib.styles import Styles

setup(width=100, height=60)
rectangle((50, 30), width=60, height=30, style=Styles.PrimaryFlat, text="Core Service")
```
:::
```

### Supported Block Positioning Options:
- `xy: (x, y)`: Absolute stage position from bottom-left corner.
- `size: (w, h)`: Container width and height in stage pixels.
- `slot: left | right | header | footer`: Semantic predefined layout slots.

---

## 5. Interactive Web Presentation Deck Engine (`slide.js`)

HTML presentation decks compiled with Drawlib feature an ultra-lightweight, zero-dependency presentation engine:

### Keyboard Shortcuts:
| Key | Action | Description |
| :--- | :--- | :--- |
| `Right Arrow` / `Space` / `PageDown` | Next Slide | Advance to the next presentation slide. |
| `Left Arrow` / `PageUp` | Previous Slide | Return to the preceding slide. |
| `Home` / `End` | Start / End | Jump to the first or last slide. |
| `F` | Fullscreen | Toggle browser fullscreen presentation mode. |
| `O` / `Esc` | Overview Grid | Toggle slide overview thumbnail grid for instant jumping. |

---

## 6. Vector PDF Compilation (`build_pdf.sh`)

Slides export to 16:9 print-ready vector presentation PDFs using headless Chromium:
```bash
./slide_src/build_pdf.sh
# Compiles to ./slide.pdf at 1920x1080 resolution
```

All fonts, embedded SVG vectors, and Drawlib diagram primitives are preserved with vector sharpness.

---

## 7. Best Practice Checklist for Slides

1. **16:9 Widescreen Alignment**:
   Design embedded Drawlib diagrams with 16:9 or 2:1 canvas aspect ratios (e.g. `setup(width=120, height=60)`).
2. **Typography Hierarchy**:
   Use `text_size=18–24` for diagram headings and `text_size=12–14` for node labels to ensure legibility across projectors and shared screens.
3. **Contrast & Theme Harmony**:
   Align diagram themes with the presentation stylesheet (`slide.css`) using `Styles.PrimaryFlat` and `Styles.WhiteBold`.
4. **Slide Counter Placement**:
   Place `current_slide.text` in bottom-right corner with subtle muted styling (`Styles.MutedSmall`).
