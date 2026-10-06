# Drawlib Slide Architecture Plan 3.0 (SLIDE_PLAN3.md)

**The Pure Code & Complete Declarative Model: Abolishing Magic Layouts in Favor of Unified Cartesian Blocks and First-Class Slide APIs**

---

## 1. Executive Summary & Design Philosophy

### 1.1. Why Architecture 3.0? (The Final Decoupling from HTML Frameworks)
In traditional presentation frameworks (Marp, Slidev, Reveal.js) and in Drawlib's earlier exploratory phases ([SLIDE_PLAN.md](SLIDE_PLAN.md), [SLIDE_PLAN2.md](SLIDE_PLAN2.md)), slide generation relied on HTML/CSS layout templates:
- **1.0 (CSS Slots)**: Divided slides into rigid Flexbox/Grid slots (`layout: split-right`, `slot: right`, `ratio: "4:6"`). This contradicted Drawlib's spatial coordinate philosophy.
- **2.0 (Hybrid Stage + Master Chrome)**: Unified spatial positioning onto a 1920×1080 stage, but retained framework "magic": `layout: cover`, `layout: canvas`, `header: "..."`, `footer: "..."`, and `paginate: true/false`. HTML `<header>` and `<footer>` elements were injected automatically into the DOM.

However, automatic HTML/CSS injection creates persistent friction for engineers and AI agents:
1. **Style Fragmentation**: Customizing a footer's color, position, font, or badge required fighting with `slide.css` instead of using Drawlib's native Python design tokens (`Styles`, `Colors`).
2. **Canvas Conflicts**: Creating full-bleed infographics or hero diagrams required learning special negation rules (`layout: canvas`, `header: none`, `footer: none`) to suppress the framework's injected chrome.
3. **Philosophical Inconsistency**: Drawlib is **"Illustration as Code"**. Presentation slides should not be an exception where layout is obscured behind template magic.

**Slide Architecture 3.0** completely eliminates framework abstractions and achieves a **Pure Code & Complete Declarative Model**:
- **Zero Built-In Chrome**: No HTML `<header>` or `<footer>` elements are injected into the DOM.
- **Pure 1920 × 1080 Stage**: Every slide is an unencumbered 1920×1080 Cartesian stage with top-left origin `(0, 0)`.
- **Single Universal Positioning Primitive**: **`::: block (x, y) (w, h) [options]`** governs every visual element on stage (headers, text columns, diagrams, cards, footers).
- **First-Class Slide Introspection API (`current_slide`)**: Slide metadata (page number, total count) is accessed via Python code (`from drawlib.slide import current_slide`), styled with Python design tokens, and rendered wherever the author chooses.

---

## 2. Core Architectural Pillars

```text
┌────────────────────────────────────────────────────────────────────────────┐ 1920 x 1080
│ (0, 0) Pure Canvas Stage                                                   │
│                                                                            │
│  ::: block (80, 40) (1760, 60)                                             │
│  # Declared Slide Header Title                                             │
│                                                                            │
│  ┌─────────────────────────┐   ┌────────────────────────────────────────┐  │
│  │ ::: block               │   │ ::: block (860, 140) (980, 840)        │  │
│  │ (80, 140) (740, 840)    │   │ ```drawlib file:arch.svg               │  │
│  │                         │   │ # Render diagram at 100% container     │  │
│  │ - **Point 1**: Text     │   │ ...                                    │  │
│  │ - **Point 2**: Text     │   │ ```                                    │  │
│  └─────────────────────────┘   └────────────────────────────────────────┘  │
│                                                                            │
│  ::: block (1700, 1020) (140, 40)                                          │
│  ```drawlib file:page.svg -> text((7, 2), current_slide.text)              │
└────────────────────────────────────────────────────────────────────────────┘
```

### 2.1. The 1920 × 1080 Stage
- **Fixed Aspect Ratio**: Every slide is rendered onto a fixed `1920px × 1080px` virtual stage, scaled responsively in the browser via CSS `transform: scale()`.
- **Top-Left Cartesian Origin `(0, 0)`**: Matches standard screen coordinates.
- **Zero Injected HTML Chrome**: The slide DOM contains only the stage wrapper and the author's declared blocks:
  ```html
  <section class="slide active" data-slide-index="1">
    <div class="slide-body">
      <!-- Only declared ::: block elements appear here -->
    </div>
  </section>
  ```

### 2.2. Single Universal Primitive: `::: block (x, y) (w, h) [options]`
Every visual container on the slide uses identical syntax:
```text
::: block (x, y) (width, height) [options]
... markdown content or drawlib code block ...
:::
```

| Parameter / Option | Syntax | Purpose |
| :--- | :--- | :--- |
| **Stage Coordinates** | `(x, y)` | Top-left stage coordinates in pixels (e.g. `(80, 140)`). |
| **Dimensions** | `(w, h)` | Width and height bounding box in pixels (e.g. `(740, 840)`). |
| **Typography** | `font:<size>` | Scoped font size (e.g. `font:22px` or `font:1.2rem`). |
| **Density** | `compact` | Tighter line-height (1.35) and smaller margins. |
| **Alignment** | `center`, `left`, `right` | Text alignment within the block. |
| **Stacking Layer** | `z:<index>` | Z-index depth for background/foreground composition (e.g. `z:5`, `z:10`). |
| **Custom CSS** | `style:"..."` | Additional inline styles (e.g. `style:"background: #f8f9fa; border-radius: 8px;"`). |
| **CSS Classes** | `class:"..."` | Custom CSS class names. |

### 2.3. Separation of Concerns for ````drawlib```` Blocks
- ````drawlib file:<name>.svg```` is placed **inside** `::: block (x, y) (w, h)`.
- **`::: block`** is exclusively responsible for stage placement (`left`, `top`, `width`, `height`, `z-index`).
- **````drawlib````** is exclusively responsible for drawing logic. The resulting vector graphic automatically fills 100% of the containing block (`width: 100%; height: 100%; object-fit: contain;`).

### 2.4. Zero-Config Fallback (AI & Human Ergonomics)
If an author or AI agent creates a slide without any `::: block` directives, the compiler automatically wraps the entire body in the default content area:
```text
::: block (80, 140) (1760, 840)
... plain markdown content ...
:::
```
This ensures rapid prototyping and plain notes render immediately without errors.

---

## 3. Pythonic Slide Metaprogramming: `current_slide` API

### 3.1. Philosophy
Slide numbers, presentation progress, and deck totals are not static text; they are dynamic runtime metadata. Instead of relying on template engine macros (`{{page}} / {{total}}`) or HTML template injection, Drawlib provides a first-class, immutable introspection object:
```python
from drawlib.slide import current_slide
```

### 3.2. Object Specification
```python
@dataclasses.dataclass(frozen=True)
class SlideContext:
    """Runtime context providing slide index and deck metadata."""
    index: int      # 1-based index of current slide (e.g. 4)
    total: int      # Total number of slides in the deck (e.g. 9)

    @property
    def text(self) -> str:
        """Formatted slide counter string, e.g. '4 / 9'."""
        return f"{self.index} / {self.total}"

    def format(self, template: str = "{index} / {total}") -> str:
        """Render a custom format string, e.g. '{index} of {total}' -> '4 of 9'."""
        return template.format(index=self.index, total=self.total)
```

### 3.3. Usage Scenarios

#### Scenario A: Full Canvas Infographic (One-Piece Slide)
On full-bleed slides (`(0, 0) (1920, 1080)`), no separate footer block is required. The author simply places the page number directly in Python canvas space:
```python
from drawlib.canvas import setup
from drawlib.text import text
from drawlib.styles import Styles
from drawlib.slide import current_slide

setup(width=192, height=108)

# ... Main technical illustration ...

# Slide counter badge at bottom right
text((180, 4), current_slide.text, style=Styles.WhiteMuted)
```

#### Scenario B: Modular Slide Counter Block
On standard slides, a small block placed at `(1700, 1020) (140, 40)` renders the page number badge with full styling control:
```markdown
::: block (1700, 1020) (140, 40)
```drawlib file:page_04.svg
from drawlib.canvas import setup
from drawlib.text import text
from drawlib.styles import Styles
from drawlib.slide import current_slide

setup(width=14, height=4)
text((7, 2), current_slide.text, style=Styles.Muted)
```
:::
```

#### Scenario C: Data-Driven Progress Visualizations
Because `current_slide.index` and `current_slide.total` are standard Python integers, authors can create bespoke visual indicators:
```python
# Segmented progress bar along bottom of slide
progress = current_slide.index / current_slide.total
rectangle((96, 1), width=192 * progress, height=2, style=Styles.AccentFlat)
```

---

## 4. Complete Slide Authoring Patterns (Standard Examples)

### 4.1. Title / Cover Slide
No special `layout: cover` directive. The block is simply centered on the 1920×1080 stage:
```markdown
::: block (160, 260) (1600, 560) center
# Drawlib Presentation
## Illustration as Code for Modern Engineers

Declarative Python Diagramming & Modern Presentation Architecture

---

**Yuichi Ito** | Drawlib Author  
*October 2026*
:::
```

### 4.2. Standard Content Slide with 2 Columns (Text + Architecture Diagram)
Header, text, diagram, and page counter are all explicitly declared with clean coordinates:
```markdown
::: block (80, 40) (1760, 60)
# Scalable Topologies in Code
:::

::: block (80, 140) (740, 840) font:22px
Drawlib provides high-level domain modules for cloud architecture:

- **Client Ingress**: Web SPA, Mobile App, Edge Workers terminating TLS
- **Kubernetes Cluster**: Isolated container pods with auto-scaling
- **Data Persistence**: Sharded primary database + Pub/Sub event streaming
- **Clean Syntax**: Connect nodes with labels and automatic orthogonal routing
:::

::: block (860, 140) (980, 840) z:5
```drawlib file:arch_diagram.svg
from drawlib.canvas import setup
from drawlib.diagrams.architecture import ArchitectureDiagram, GcpIcon, Node, NodeGroup
from drawlib.styles import Styles

setup(width=115, height=75)
arch = ArchitectureDiagram(node_style=Styles.PrimaryFlat, edge_style=Styles.Primary)
client = arch.add(Node("Client App", icon=GcpIcon.APP_ENGINE, icon_size=7.5), (14.0, 42.0))
gateway = arch.add(Node("API Gateway", icon=GcpIcon.CLOUD_API_GATEWAY, icon_size=7.5), (38.0, 42.0))
arch.connect(client, gateway, label="HTTPS/REST", routing="orthogonal")
arch.draw(xy=(3.0, 3.0))
```
:::

::: block (1700, 1020) (140, 40)
```drawlib file:page_04.svg
from drawlib.canvas import setup
from drawlib.text import text
from drawlib.styles import Styles
from drawlib.slide import current_slide

setup(width=14, height=4)
text((7, 2), current_slide.text, style=Styles.Muted)
```
:::
```

### 4.3. Full-Bleed 1920×1080 Hero Diagram (Canvas Mode)
No `layout: canvas`. The block spans `(0, 0) (1920, 1080)` without interference from headers or footers:
```markdown
::: block (0, 0) (1920, 1080)
```drawlib file:full_hero_canvas.svg
from drawlib.canvas import setup
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.slide import current_slide
from drawlib.text import text

setup(width=192, height=108)

# Full stage canvas drawing
rectangle((96, 54), width=192, height=108, style=Styles.WhiteFlat)
rectangle((96, 90), width=172, height=14, style=Styles.PrimaryFlat,
          text="FULL CANVAS STAGE — 1920 × 1080 PURE DRAWING", text_style=Styles.WhiteBold)

# Slide counter inside graphic
text((180, 5), current_slide.text, style=Styles.Muted)
```
:::
```

### 4.4. Multi-Block Overlap & Bleed (Stacking & Depth)
```markdown
::: block (80, 40) (1760, 60)
# Edge Gateway & Mesh Architecture
:::

::: block (80, 160) (780, 800) font:22px z:10
# Total Spatial Freedom
Position text overlays directly across bleeding diagrams with deterministic z-index.
:::

::: block (940, 0) (980, 1080) z:5
```drawlib file:bleed_stack.svg
# Bleeds across the entire height of the slide from Y: 0 to Y: 1080
...
```
:::
```

---

## 5. Architectural Comparison Matrix

| Capability | Architecture 1.0 (CSS Slots) | Architecture 2.0 (Hybrid Stage) | Architecture 3.0 (Pure Code & Declarative) |
| :--- | :--- | :--- | :--- |
| **Stage Coordinates** | CSS Flex / Grid columns | 1920×1080 Stage | **1920×1080 Pure Stage** |
| **Layout Directive** | `layout: split-right`, `ratio` | `layout: cover / canvas / default` | **Abolished** (Zero magic layouts) |
| **HTML Chrome Injection** | Injected `<header>`, `<footer>` | Injected `<header>`, `<footer>` | **Abolished** (Zero injected chrome) |
| **Positioning Syntax** | `slot: right`, `options.xy` | `::: box`, ````drawlib (x,y)```` | **`::: block (x,y)(w,h)` (Unified)** |
| **Diagram Embedding** | Tied to layout slots | Standalone directive | **Nested inside `::: block`** |
| **Page Counter** | Hardcoded DOM element | Hardcoded DOM element | **`from drawlib.slide import current_slide`** |
| **Frontmatter** | Mandatory layout keys | Header, footer, paginate | **Zero mandatory keys** (Pure markdown) |
| **AI Ergonomics** | Low (fragile slot CSS) | Medium (some magic conventions) | **Maximum** (1 primitive, pure math) |

---

## 6. Implementation & Refactoring Plan

### 6.1. Compiler (`src/drawlib/_slide/compiler.py`)
1. **Slide Context Management**:
   - Create `_current_slide_context: ContextVar[SlideContext]`.
   - Update `current_slide` proxy to read from context.
   - When processing slide `idx` of `total_slides`, set `SlideContext(index=idx, total=total_slides)`.
2. **Prune HTML Chrome Injection**:
   - Remove `<header class="slide-header">` and `<footer class="slide-footer">` generation from `_assemble_slide_section`.
   - Remove `header`, `footer`, `paginate`, and `layout` parsing from frontmatter.
   - Render clean `<section class="slide" data-slide-index="{idx}"> <div class="slide-body">{rendered_body}</div> </section>`.
3. **Zero-Config Fallback**:
   - Preserve automatic fallback wrapping in `::: block (80, 140) (1760, 840)` if no `::: block` is present.

### 6.2. Public Module (`src/drawlib/slide.py`)
- Re-export `current_slide` and `SlideContext`.

### 6.3. CSS Templates (`src/drawlib/_css_templates/slide/`)
- Remove `.slide-header`, `.slide-footer`, `.layout-cover`, `.layout-canvas`, and `.layout-agenda` rules from `default.css.template`, `google.css.template`, and `monochrome.css.template`.
- Retain core stage layout (`.presentation-stage`, `.slide`, `.slide-body`, `.slide-block`, `.drawlib-image`).

### 6.4. Scaffolding & Project Templates (`src/drawlib/_project_templates/slide/`)
- Update `en/` and `ja/` markdown templates to use the 3.0 pure declarative block syntax.
- Update `slide_src/*.md` in the current workspace.

### 6.5. Test Suite Verification
- Update `tests/test_slide.py` to test `current_slide` API (`index`, `total`, `text`, `format`) and chrome-free compilation.
- Verify with `./dcli check all` and `./dcli test all`.
