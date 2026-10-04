# Slide Deck Project Guide (`drawlib init slide`)

The `slide` starter template creates 16:9 presentation slide decks with rich architectural diagrams, metrics cards, badges, and structured layouts.

Drawlib compiles your slide deck into both an **interactive HTML web presentation** and a **1-slide-per-page vector PDF**, perfectly sized for conferences, client briefings, and team reviews.

---

## 1. Project Initialization

Scaffold a presentation project using `drawlib init`:

```bash
# Create in a new subdirectory:
drawlib init slide my_deck/

# With Google styling and custom output base name:
drawlib init slide my_deck/ -o keynote -s google

# Or scaffold directly in current working directory:
drawlib init slide --here
```

---

## 2. Directory Layout & Anatomy

```text
my_deck/
├── slide_src/                 # [SOURCE OF TRUTH] Author Markdown slides here
│   ├── 01_title.md            # Title slide
│   ├── 02_agenda.md           # Agenda slide
│   ├── 03_architecture.md     # Architecture slide with diagrams
│   ├── styles.py              # Slide-wide styling and color overrides
│   ├── utils.py               # Slide layout helpers (cards, badges, grids)
│   ├── slide.js               # Slide runtime keyboard / navigation engine
│   ├── build.sh               # Master build script (HTML + PDF + Images)
│   ├── build_html.sh          # HTML presentation deck build (slide_html/)
│   ├── build_pdf.sh           # 16:9 vector PDF presentation export (slide.pdf)
│   ├── build_image.sh         # Extract embedded drawlib blocks to slide_images/
│   ├── serve.sh               # Local preview server script
│   └── README.md              # Slide authoring guide
├── slide_html/                # [GENERATED] HTML presentation deck (index.html)
├── slide.pdf                  # [GENERATED] High-quality vector presentation PDF
└── slide_images/              # [GENERATED] Extracted standalone diagram images
```

---

## 3. Multiple Presentation Outputs

A `slide` project produces presentation artifacts tailored for every scenario:

| Output | Audience & Environment | Key Features | Build Script |
| :--- | :--- | :--- | :--- |
| **`slide_html/index.html`** | Interactive Presenting | 1920x1080 fixed stage, auto-scaling viewport, keyboard navigation (`Space`, `Arrows`, `F`), overview grid | `build_html.sh` |
| **`slide.pdf`** | Offline Distribution | 1 slide per page, vector-sharp graphics, exact 16:9 aspect ratio (`@page { size: 16in 9in; margin: 0; }`) | `build_pdf.sh` |
| **`slide_images/`** | Slides & Social Media | Extracted standalone slide illustrations for external decks and sharing | `build_image.sh` |

---

## 4. Authoring Slides

Each Markdown file in `slide_src/` represents a single slide. Use standard Markdown alongside helper components from `utils.py`:

````markdown
# Architecture Overview

<div class="subtitle">Event-Driven Ingestion Pipeline</div>

```drawlib 1500px center file:arch_flow.png
from drawlib.canvas import setup
from drawlib.shapes import rectangle
from drawlib.lines import line
from drawlib.styles import Styles

setup(width=160, height=50)
rectangle((30, 25), width=35, height=20, style=Styles.PrimaryFlat, text="Producer", text_style=Styles.WhiteBold)
rectangle((80, 25), width=35, height=20, style=Styles.AccentFlat, text="Kafka", text_style=Styles.WhiteBold)
rectangle((130, 25), width=35, height=20, style=Styles.SecondaryFlat, text="Consumer", text_style=Styles.WhiteBold)
line((47.5, 25), (62.5, 25), arrow_head="->", style=Styles.PrimaryBold)
line((97.5, 25), (112.5, 25), arrow_head="->", style=Styles.PrimaryBold)
```
````

---

## 5. Modular Build Scripts Architecture

- **`build_html.sh`**:
  Compiles slides into the web presentation deck in `slide_html/index.html`.
- **`build_pdf.sh`**:
  Uses headless Chromium to capture each slide into a multi-page vector PDF (`slide.pdf`).
- **`build_image.sh`**:
  Extracts embedded ````drawlib```` blocks into standalone diagram images in `slide_images/`.
- **`build.sh` (Master Script)**:
  Runs HTML, PDF, and Image builds in sequence.

---

## 6. Local Preview & Presenting

Launch the local development preview server:

```bash
./slide_src/serve.sh
```

Or run directly:

```bash
uv run drawlib serve slide_html/
```

### Keyboard Shortcuts:
- **`→` / `Space` / `PageDown`**: Next slide
- **`←` / `PageUp`**: Previous slide
- **`F`**: Toggle full screen
- **`O` / `Esc`**: Toggle slide overview grid
