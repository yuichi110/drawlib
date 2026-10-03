# Drawlib HTML Slide Feature Plan (SLIDE_PLAN.md)

This document outlines the architectural design, component specification, and implementation plan for adding an HTML-based presentation slide deck feature to `drawlib`.

---

## 1. Overview & Vision

### 1.1. Core Concept: "Illustration as Code" Meets "Web-Standard Slides"
`drawlib` provides powerful declarative tools for creating cloud topologies, sequence diagrams, flowcharts, and technical charts using Python.
Slide authoring tools typically fall into two extremes:
1. **Fully Graphical / Canvas-based**: Entire slides are rendered as flat bitmap images (no selectable text, blurry typography, inflexible responsive scaling).
2. **Text-based without Native Drawing (Marp, Reveal.js)**: Strong text layout and CSS, but diagrams rely on basic ASCII/Mermaid or external pre-rendered PNGs that easily fall out of sync with code.

**Drawlib's Hybrid Architecture**:
- **Web-standard typography**: Title, markdown bullets, code blocks (with syntax highlighting), and tables are rendered as clean, accessible HTML/CSS.
- **First-class Vector Diagrams & SmartArts (All-in-Drawlib Native SVG)**:
  - Technical diagrams, cloud topologies, and SmartArts (e.g. Curved Agenda, Timelines, Process Chevrons) are **drawn completely in Drawlib (shapes + text)** and exported as **Native SVG (`.svg`)**.
  - Text inside diagrams is preserved as native `<text>` elements. There is **zero coordinate synchronization friction between Python and HTML**, and **zero font baseline drift**.
  - Diagrams support browser `Ctrl+F` search, mouse selection, and vector scaling without complex HTML overlays or fragile CSS hover hacks.
- **Dynamic Animations (Drawlib Animated WebP)**: Live CI/CD pipelines, state transitions, and step-by-step algorithms are exported as lightweight looping WebP animations (`.webp`) via `drawlib.anim.Animation`.
- **Modular SmartArt Calling**: SmartArts and diagrams can be placed using standard layout slots (`slot: left`, `slot: right`) or positioned directly on the 1920×1080 stage using coordinate bounds (`xy=(x, y)`, `size=(w, h)`).
- **1 Slide = 1 Markdown file**: High maintainability, clean Git diffs, seamless team collaboration, and individual slide testing via `drawlib show`.

---

## 2. Component Architecture: `_slide/` & Project Custom Templates

Rather than bloating the build engine (`_builder/`) with slide-specific markup, slide layouts and modular SmartArt components are organized into clean domain packages with user extensibility.

### 2.1. Directory Structure & Template Discovery
```text
drawlib/ (Library Core)
├── _slide/                           # Built-in slide components & themes
│   ├── base.py                      # SmartArt base class & BoundingBox
│   ├── registry.py                  # Component registry & resolver
│   ├── google/                      # Google-themed SmartArts (curved_agenda, etc.)
│   └── default/                     # Standard SmartArts (timeline, chevron_process)
└── _css_templates/slide/            # CSS theme presets (google, default, dark)

slide_src/ (User Presentation Project)
├── _slide_templates/                 # ★ Project-Local Custom SmartArts (User Extensible)
│   ├── curved_agenda.py             # Custom curved agenda or override
│   ├── release_roadmap.py           # Custom roadmap SmartArt
│   └── kpi_cards.py                 # Custom metrics component
├── 01_title.md
├── 02_agenda.md
└── styles.py
```

#### Template Resolution Order (Lookup Hierarchy)
When a slide invokes a SmartArt component (e.g. ````smartart:curved_agenda````):
1. **Project Directory**: `slide_src/_slide_templates/<name>.py` *(Allows users to add new custom components or override built-in ones)*.
2. **Built-in Library**: `drawlib._slide.<theme>.<name>`.

### 2.2. Anatomy of a Modular SmartArt Component
A SmartArt component receives the Markdown content, target dimensions (`BoundingBox`), and styling parameters, and generates both the Drawlib illustration and its slide container placement:

```python
# slide_src/_slide_templates/curved_agenda.py
from dataclasses import dataclass
from drawlib.canvas import clear, save, setup
from drawlib.lines import bezier
from drawlib.shapes import circle
from drawlib.text import text
from drawlib.styles import Colors, Style, Styles
from drawlib.slide import SmartArtComponent, BoundingBox

class CurvedAgenda(SmartArtComponent):
    """Draws a mathematical curved agenda directly in Drawlib, emitted as Native SVG."""

    name = "curved_agenda"

    def render(self, box: BoundingBox, items: list[str], output_file: str) -> None:
        """Render both geometry and text entirely in Drawlib."""
        n = len(items)
        clear()
        setup(width=box.width / 10, height=box.height / 10)

        # 1. Draw mathematical bezier curve
        # 2. Draw numbered circles and node badges
        # 3. Draw text items directly with proper padding
        # 4. Save as SVG (with svg.fonttype = 'none')
        save(output_file, format="svg")
```

---

## 3. High-Precision Vector Rendering & Text Searchability

A core requirement for technical presentations is that **text inside diagrams (e.g., "API Gateway", "Kafka Queue") must be fully searchable via browser `Ctrl+F` and selectable via mouse dragging**.

### 3.1. Why "All-in-Drawlib Native SVG" Beats "HTML Text Overlays"
Earlier prototypes attempted to separate the graphic background (Drawlib) from foreground text (HTML `<div>` / `<span>` overlay cards).
This approach proved problematic for technical diagrams:
1. **Font Engine Discrepancy**: Matplotlib/FreeType calculates character metrics and baselines slightly differently from browser rendering engines (Blink/WebKit). Tight bounding boxes and connector lines inevitably suffer 2–4px alignment drift.
2. **Over-engineering**: Complex CSS hover effects on individual diagram text nodes add unnecessary layout fragility without improving presentation value.

**The Solution: Native SVG Output (`matplotlib.rcParams['svg.fonttype'] = 'none'`)**:
- All shapes, connection lines, icons, and text labels are rendered together by Drawlib.
- Matplotlib writes exact mathematical coordinates into native SVG `<text>` elements:
  ```xml
  <text style="font-size: 13px; text-anchor: middle; fill: #1e1e1e;" x="256.7" y="231.0">API Gateway</text>
  ```
- **Guaranteed Precision**: 100% mathematical alignment between lines, boxes, and text.
- **Searchable & Selectable**: Browser `Ctrl+F` instantly finds and highlights text inside the SVG. Mouse selection and copy-paste work natively.
- **Font Fallback Resilience**: By applying sensible padding (10–15%) inside boxes and using universal fonts (DejaVu, Roboto, Noto), client-side font substitution never clips or breaks labels.

### 3.2. Icon & Image Handling in Vector Diagrams
| Asset Type | Implementation Mechanism | Behavior in SVG Output | Font / Tofu Risk |
| :--- | :--- | :--- | :--- |
| **`GcpIcon`** (Google Cloud) | PNG Raster Assets | Automatically embedded as base64 `<image xlink:href="data:image/png;base64,...">` | **Zero (100% reliable)** |
| **Photos & Avatars** (JPEG/PNG) | Bitmap Images via `image()` | Automatically embedded as base64 `<image xlink:href="data:image/jpeg;base64,...">` | **Zero (100% reliable)** |
| **`PhosphorIcon`** / **FontAwesome** | Vector Icon Font (TTF) | Emitted as unicode text (`<text font-family="Phosphor"></text>`). Compiler automatically injects `@font-face` into CSS | **Zero (Fully rendered vector)** |

### 3.3. Static SVG vs. Animated WebP Coexistence
Technical presentations require both ultra-sharp searchable diagrams and dynamic step-by-step workflows:

| Diagram Characteristic | Recommended Output Format | Engine Mechanism | Key Benefits |
| :--- | :--- | :--- | :--- |
| **Static Architectural Diagrams & SmartArts** | **Native SVG (`.svg`)** | Matplotlib SVG backend (`svg.fonttype = 'none'`) | Browser `Ctrl+F` search, crisp vector scaling, zero tofu icons |
| **Dynamic Pipelines & State Transitions** | **Animated WebP (`.webp`)** | `drawlib.anim.Animation` frame capture | Native browser autoplay/looping, ~130KB lightweight payload |

- **Official `save()` Format Support**: Re-add `"svg"` to `ImageFormat` in `_image.py` alongside `"png"`, `"webp"`, `"jpg"`, and `"pdf"`.
- **Animation Safety Guard**: Passing `format="svg"` to `Animation.save()` raises a descriptive `ValueError("Unsupported animation format 'svg'")`, guiding users to use `"webp"` or `"png"` (APNG) for animated graphics.

---

## 4. Markdown Authoring Experience: Modular SmartArts & Flow

Users can compose slides using standard flow layouts or coordinate-positioned SmartArts on the 1920×1080 stage.

### 4.1. Modular SmartArt Calling (`smartart:<name>`)
Users can invoke SmartArts directly within Markdown, passing either layout slots or explicit stage coordinates:

```markdown
---
header: "Presentation Agenda"
footer: "Drawlib: Illustration as Code"
paginate: true
---

# Topics Covered Today

```smartart:curved_agenda slot:right file:agenda.svg
1. Team Introductions チーム紹介
2. Architecture Overview アーキテクチャ概要
3. Multi-Format Publishing マルチフォーマット出力
4. Live CI/CD Pipeline パイプライン連携
5. Next Steps 次のステップ
```
```

Or with explicit coordinate bounds on the 1920×1080 canvas:
```markdown
```smartart:curved_agenda xy=(100, 200) size=(800, 750) file:agenda.svg
1. Team Introductions
2. Architecture Overview
3. Multi-Format Publishing
```

```drawlib xy=(950, 200) size=(870, 750) file:arch_diagram.svg
arch = ArchitectureDiagram(node_style=Styles.PrimaryFlat)
# ... build diagram ...
save()
```
```

### 4.2. Layout Split Slots (`slot: left`, `slot: right`)
For standard 2-column technical slides, users don't need to specify coordinates:

```markdown
---
layout: split-right
ratio: "4:6"
header: "Cloud & Microservices"
footer: "Drawlib: Illustration as Code"
---

# Scalable Topologies in Code

- **Client Tier**: Web SPA, Mobile App, Edge Workers
- **Ingress Gateway**: TLS termination, rate-limiting
- **Data Persistence**: Sharded primary database + Kafka event streaming

```drawlib 100% center file:arch_diagram.svg slot:right
arch = ArchitectureDiagram(node_style=Styles.PrimaryFlat)
# ... build diagram ...
save()
```
```


---

## 5. CSS Themes Architecture (`_css_templates/slide/`)

Following `drawlib`'s existing architecture, themes are placed under [`src/drawlib/_css_templates/slide/`](src/drawlib/_css_templates/):

```text
src/drawlib/_css_templates/slide/
├── default.css.template         # Modern developer light (Tailwind / VitePress inspired)
├── default-dark.css.template    # Deep slate & indigo dark theme
├── google.css.template          # Material Design / Google Slides light theme
├── google-dark.css.template     # Material Dark theme
├── github.css.template          # Developer GitHub-flavored slide theme
└── monochrome.css.template      # High-contrast black & white academic theme
```

### 5.1. Token Synchronization
CSS variables in `google.css.template` align directly with `drawlib.styles.GoogleColors`:
- `--slide-primary`: `#1a73e8` (Google Blue)
- `--slide-accent`: `#ea4335` (Google Red)
- `--slide-secondary`: `#188038` (Google Green)
- `--slide-yellow`: `#fbbc04` (Google Yellow)

---

## 6. Slide Engine Architecture (HTML / CSS / JS)

The generated slide deck is a **zero-dependency, standalone static HTML application**.

### 6.1. 16:9 Viewport Scaling & Stage Containment
- Logical resolution: `1920px × 1080px` (16:9).
- Responsive containment: JavaScript computes `scale = Math.min(windowWidth / 1920, windowHeight / 1080)` and applies `transform: scale(...)`.
- Result: **Pixel-perfect layout preservation on all display resolutions and aspect ratios**.

### 6.2. Navigation & Presentation Controller (Vanilla JS)
- `ArrowRight`, `Space`, `Enter`: Next slide.
- `ArrowLeft`, `Backspace`: Previous slide.
- `Home`, `End`: Jump to first / last slide.
- `F`: Toggle Fullscreen.
- `O` / `Escape`: Overview Grid View (instant visual slide selector).
- URL hash synchronization (`#1`, `#2`, ...).

### 6.3. Print & PDF Export (`@media print`)
Includes native print stylesheet rules:
- `@page { size: 16in 9in; margin: 0; }`
- `.slide { page-break-after: always; break-after: page; width: 16in !important; height: 9in !important; }`
- Enables one-click "Print to PDF" from Chrome/Edge with perfect vector fidelity.

---

## 7. Verified Working Prototype

A complete 6-slide prototype was built and verified in the repository:

```text
slide_src/                              # Source Markdown files
├── 01_title.md                        # Cover slide
├── 02_agenda.md                       # Curved agenda (SmartArt prototype)
├── 03_why_drawlib.md                  # Split layout + Table SmartArt
├── 04_architecture.md                 # Split layout + Native SVG Architecture diagram
├── 05_workflows.md                    # Split layout + FlowDiagram CI/CD pipeline
├── 06_ecosystem.md                    # Multi-format publishing table
├── styles.py                          # Deck-wide styles
└── slide.css                          # Custom presentation overrides

slide/                                 # Compiled HTML presentation deck
├── index.html                         # Full interactive presentation
├── slide.css                          # Google theme + responsive scaling
├── slide.js                           # Keyboard navigation + overview modal
├── Phosphor.ttf                       # Bundled icon font for SVG vector icons
├── agenda_curve.png                   # Generated curved arc background
├── arch_diagram.svg                   # Native SVG with searchable <text> and Phosphor icons
├── feature_matrix.png                 # Table SmartArt image
├── workflow_pipeline.png              # FlowDiagram pipeline static image
└── workflow_pipeline.webp             # FlowDiagram live animated WebP (163KB)
```

**Verification Results**:
- Browser serving verified via `uv run drawlib serve slide/`.
- `Ctrl+F` search verified inside `arch_diagram.svg` for "API Gateway", "Kafka Queue", "Auth Service".
- Phosphor vector icons verified without tofu (`▯`) artifacts.
- Animated WebP pipeline verified looping smoothly with node highlighting in Slide 5.
- Responsive window resizing verified with zero coordinate drift.

---

## 8. Implementation Roadmap

```text
Phase 1: Core Format & Component Foundation
  ├── Re-add "svg" to ImageFormat in src/drawlib/_core/l2_types/_image.py
  ├── Add Animation safety guard (ValueError on format="svg")
  ├── Create src/drawlib/_slide/ and base SmartArtComponent / BoundingBox interfaces
  ├── Create src/drawlib/_css_templates/slide/ themes (google, default, dark)
  └── Implement Phosphor/FontAwesome auto-embedding in SVG exporter

Phase 2: Built-in Modular SmartArts (All-in-Drawlib Native SVG)
  ├── Implement _slide/google/curved_agenda.py (pure Drawlib SVG)
  ├── Implement _slide/default/timeline.py and chevron_process.py
  └── Implement project-level template resolver (slide_src/_slide_templates/)

Phase 3: Compiler & CLI Integration
  ├── Update block options parser for smartart:<name>, slot, xy=(x,y), size=(w,h)
  ├── Implement compiler/slide.py (AST parser, template resolver, SVG generator)
  ├── Add `drawlib build slide` in commands/build.py
  └── Add `drawlib init slide` in commands/init.py

Phase 4: Tests & Public Documentation
  ├── Comprehensive pytest unit tests for SmartArt components & template resolver
  ├── End-to-end integration tests for CLI build and serve
  └── User guide in docs_src/slide.md
```
