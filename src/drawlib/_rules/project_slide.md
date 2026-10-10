# Drawlib Presentation Slide Deck Guidelines (`project-slide`)

A **`slide` project** (`drawlib init slide`) compiles Markdown slide files (`slide_src/*.md`) into an **interactive 16:9 widescreen web presentation deck (`slide_html/index.html`)** with dual-window Presenter View (`?presenter=1`), a **high-resolution 1920×1080 vector PDF (`slide.pdf`)**, and **standalone vector/animated slide assets (`slide_images/`)**.

*(For general project scaffolding, see `uv run drawlib rules show project-overview`. For the Python runtime API in `drawlib.slide`—including `current_slide`, `SlideContext`, `BoundingBox`, and `build_slide()`—run `uv run drawlib rules show lib-slide`. For the 3-stage review loop, see `uv run drawlib rules show review-guide`.)*

---

## 1. Dual Coordinate Systems: 1920×1080 Stage vs. Drawlib Canvas

When authoring Drawlib slides, two distinct coordinate systems work together:

1. **Slide Stage (`::: block (x, y) (w, h)`) — Top-Left Origin `(0, 0)`**:
   - Every slide renders on a fixed **1920 × 1080 pixel** widescreen stage (16:9 aspect ratio).
   - Container blocks (`::: block`) are positioned in CSS stage pixels where **`(0, 0)` is the top-left corner**:
     - `x` increases rightward (`0` → `1920`).
     - `y` increases downward (`0` → `1080`).
2. **Drawlib Canvas (````drawlib```` Python block) — Bottom-Left Origin `(0, 0)`**:
   - Inside any ````drawlib```` code block, `setup(width=W, height=H)` defines a Cartesian drawing canvas where **`(0, 0)` is the bottom-left corner**:
     - `x` increases rightward (`0` → `W`).
     - `y` increases upward (`0` → `H`).

```text
  SLIDE STAGE (1920×1080 px, Top-Left Origin)          DRAWLIB CANVAS (Cartesian, Bottom-Left Origin)
  (0, 0) ───────────────────────────► (1920, 0)        (0, H) ▲
    │  ::: block (80, 40) (1760, 60)      │                   │   setup(width=W, height=H)
    │  ┌───────────────────────────────┐  │                   │   ┌───────────────────────────┐
    │  │ # Slide Title                 │  │                   │   │                           │
    │  └───────────────────────────────┘  │                   │   │     (W/2, H/2) Center     │
    │                                     │                   │   │                           │
    ▼                                     │                   └───┴───────────────────────────►
  (0, 1080) ───────────────────────── (1920, 1080)          (0, 0)                          (W, 0)
```

```drawlib center fold-code file:project_slide_stage_anatomy.png caption:"1920x1080 Slide Stage Coordinates (Top-Left Origin) vs. Drawlib Canvas (Bottom-Left Origin)"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=150, height=60, dpi=150)

rectangle((75, 30), width=144, height=54, style=Styles.MutedDashed.patch(shape_r=2.5))
text(
    (75, 52),
    "16:9 Slide Stage (1920x1080 Top-Left) + Embedded Drawlib Canvas (Bottom-Left)",
    style=Styles.DarkBold.patch(text_size=12.0),
)

# Header block representation
rectangle((62, 42.5), width=106, height=7.5, style=Styles.PrimaryNeutral.patch(shape_r=1.2))
text((62, 42.5), "::: block (80, 40) (1760, 60)  ->  # Slide Heading Title", style=Styles.PrimaryBold.patch(text_size=10.2))

# Page number block
rectangle((130, 42.5), width=26, height=7.5, style=Styles.Neutral.patch(shape_r=1.2))
text((130, 42.5), "(1700, 1010)\nPage 3 / 12", style=Styles.DarkBold.patch(text_size=9.5))

# Left Narrative Column
rectangle((36, 22), width=54, height=27, style=Styles.Neutral.patch(shape_r=1.8))
phosphor.list_bullets((15, 30.5), width=4.5, style=Styles.PrimaryBold)
text((38, 30.5), "Left Narrative Block", style=Styles.DarkBold.patch(text_size=11.0))
text(
    (36, 19),
    "::: block (80, 140) (740, 840)\n• Concise Markdown bullets\n• Key architectural takeaways",
    style=Styles.Dark.patch(text_size=10.0),
)

# Right Diagram Column
rectangle((106, 22), width=74, height=27, style=Styles.PrimaryFlat.patch(shape_r=1.8))
phosphor.presentation_chart((76, 30.5), width=4.8, style=Styles.WhiteBold)
text((108, 30.5), "Right Vector Diagram Block", style=Styles.WhiteBold.patch(text_size=11.0))
text(
    (106, 19),
    "::: block (860, 140) (980, 840)\nsetup(width=98, height=84) -> file:arch.svg\nAspect Ratio 98:84 matches 980x840px!",
    style=Styles.White.patch(text_size=10.0),
)

save()
```

### 1.1. Golden Rule: Match Canvas Aspect Ratio to Block Dimensions
Always set `setup(width=W, height=H)` proportional to the enclosing `::: block (x, y) (w, h)` pixel size (typically dividing pixel dimensions by `10`):

| Enclosing `::: block` Size `(w, h)` | Recommended `setup(width, height)` | Aspect Ratio |
| :--- | :--- | :--- |
| `(1020, 840)` *(Right diagram column)* | `setup(width=102, height=84)` | `102 : 84` |
| `(980, 840)` *(Standard right diagram column)* | `setup(width=98, height=84)` | `98 : 84` |
| `(960, 840)` *(Half-width diagram column)* | `setup(width=96, height=84)` | `8 : 7` |
| `(1760, 840)` *(Full-width content area)* | `setup(width=176, height=84)` | `176 : 84` |
| `(980, 1080)` *(Right half full-bleed)* | `setup(width=98, height=108)` | `98 : 108` |
| `(1920, 1080)` *(Full-canvas hero slide)* | `setup(width=192, height=108)` | `16 : 9` |

Matching the aspect ratio prevents unwanted horizontal or vertical letterboxing inside the block container.

---

## 2. Slide Project Structure (`slide_src/`)

Scaffold a new presentation project with `uv run drawlib init slide [target] [-l <lang>] [-s <style>]`:

```text
slide_src/
├── 01_title.md            # Slide 1: Title / Cover slide
├── 02_agenda.md           # Slide 2: Agenda / Roadmap
├── 03_architecture.md     # Slide 3: Cloud / System Architecture
├── 04_workflow.md         # Slide 4: Animated CI/CD Pipeline
├── _assets/               # Static images/logos copied to output _assets/
├── styles.py              # Deck-wide Drawlib Style / Color overrides
├── utils.py               # Reusable Python slide helpers (e.g. draw_page_number)
├── style.css              # Presentation theme & typography stylesheet
├── slide.js               # Interactive web presentation & Presenter View engine
├── build.sh               # Master build script (HTML + PDF + Images)
├── build_html.sh          # Compile HTML slide deck (slide_html/)
├── build_pdf.sh           # Export 1920×1080 vector PDF (slide.pdf)
├── build_image.sh         # Extract standalone slide diagram assets (slide_images/)
└── serve.sh               # Local preview server (drawlib serve)
```

- **File Discovery & Chapter Subdirectories**: All `.md` / `.markdown` files in `slide_src/` and any nested chapter subdirectories (e.g., `00_opening/01_title.md`, `01_why_drawlib/01_section.md` — skipping directories starting with `.` or `_`, `README.md`, and `navbar.md`) are discovered recursively and compiled in sorted relative-path order. Slides inside chapter subdirectories automatically inherit root `styles.py`, `utils.py`, and `_assets/`.
- **Pure Markdown & Zero Frontmatter**: Do not add YAML frontmatter (`---`) at the top of slide files. Every visual element on a slide is placed inside one or more `::: block` containers.
- **Relative Paths Only (No Absolute Paths or file:// URLs)**: All markdown links, image references (`![logo](_assets/logo.png)`), and diagram asset references must use relative paths. Never write machine-specific absolute paths (`/usr/...`, `/home/...`, `C:\...`) or `file://` URLs in slide source files.

---

## 3. Stage Container Block Syntax (`::: block` / `::: box`)

Use `::: block` (or its alias `::: box`) to place Markdown text, tables, images, or ````drawlib```` diagrams at exact pixel coordinates on the 1920×1080 stage:

````markdown
::: block (x, y) (w, h) [options...]
<Markdown content or ```drawlib code fence>
:::
````

### 3.1. Default Coordinates
If `(x, y)` or `(w, h)` are omitted, `::: block` defaults to the standard full content area:
- Default `(x, y)`: `(80, 140)`
- Default `(w, h)`: `(1760, 840)`

### 3.2. Complete Container Options Reference

| Option Token | Syntax Examples | Compiled CSS / Behavior |
| :--- | :--- | :--- |
| **Position `(x, y)`** | `(80, 140)`, `(0, 0)` | `position: absolute; left: 80px; top: 140px;` |
| **Dimensions `(w, h)`** | `(740, 840)`, `(1920, 1080)` | `width: 740px; height: 840px;` |
| **Font Size** | `font:22px`, `fontsize:1.2rem`, `fs:18`, or bare `20px` | `font-size: 22px;` (bare numbers auto-append `px`). |
| **Compact Density** | `compact` | Adds `.compact` class to `<div class="slide-block compact">` for tighter line-height and smaller list/heading margins. |
| **Text Alignment** | `left`, `center`, `right`, or `align:center` | `text-align: center;` |
| **Layer Depth (`z-index`)** | `z:5`, `z-index:10`, `z_index:1` | `z-index: 5;` — controls foreground/background stacking when blocks overlap. |
| **Custom CSS Class** | `class:"card highlight"` | Appends custom CSS classes to the container `<div>`. |
| **Inline CSS Style** | `style:"background: #f8fafc; border-radius: 12px"` | Appends custom inline CSS rules to the container `<div>`. |

*(Both `key:value` and `key=value` syntaxes are supported for keyed tokens.)*

---

## 4. Standard 1920×1080 Stage Layout Templates

### 4.1. Standard Slide Anatomy (Header, Page Number, Footer)
Most content slides share three consistent structural blocks around the main content zone (`Y: 140` to `980`):

````markdown
::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils
utils.draw_page_number()
```
:::

::: block (80, 40) (1760, 60)
# Slide Heading Title
:::

<!-- Main Content Blocks Here (Y: 140 .. 980) -->

::: block (80, 1010) (820, 30) font:14px
*Deck Footer / Presentation Title*
:::
````

### 4.2. Template A: Title / Cover Slide (`01_title.md`)
````markdown
::: block (160, 240) (1160, 600)
# Presentation Title
## Subtitle or Core Value Proposition

Brief one-line summary of the presentation topic

---

**Speaker Name** | Role / Organization  
*October 2026*
:::

::: block (1360, 260) (400, 480)
![Hero Logo](_assets/logo.png)
:::
````

### 4.3. Template B: Two-Column Split (Narrative Left + Diagram Right)
The workhorse layout for technical presentations: left column (`W: 700–760px`) for concise bullet points, right column (`W: 960–1020px`) for a vector diagram.

````markdown
::: block (80, 40) (1760, 60)
# Cloud Microservices Topology
:::

::: block (80, 140) (740, 840)
## Key Architectural Decisions

- **API Gateway**: Centralized TLS termination and rate limiting
- **Service Mesh**: mTLS zero-trust east-west communication
- **Event Streaming**: Asynchronous decoupling via Pub/Sub
:::

::: block (860, 140) (980, 840)
```drawlib file:arch_topology.svg
from drawlib.canvas import clear, save, setup
from drawlib.shapes import rectangle
from drawlib.styles import Styles

clear()
setup(width=98, height=84)
rectangle((49, 42), width=80, height=60, style=Styles.Neutral, text="Architecture Diagram")
save()
```
:::
````

### 4.4. Template C: Half-Stage Full-Bleed Stack (`z:` Layering)
Extend a diagram across the entire vertical height (`Y: 0` to `1080`) on the right side while keeping text on the left:

````markdown
::: block (80, 40) (820, 60)
# Full-Bleed Stage Architecture
:::

::: block (80, 160) (780, 800) font:22px
## Spatial Freedom with `z:` Layers
- Left column stays inside standard margins (`X: 80..860`)
- Right diagram bleeds from `Y: 0` to `Y: 1080` (`(940, 0) (980, 1080) z:5`)
:::

::: block (940, 0) (980, 1080) z:5
```drawlib file:bleed_stack.svg
from drawlib.canvas import clear, save, setup
from drawlib.shapes import rectangle
from drawlib.styles import Styles

clear()
setup(width=98, height=108)
rectangle((49, 54), width=90, height=100, style=Styles.MutedDashed)
save()
```
:::
````

### 4.5. Template D: Full-Canvas Hero Slide (`(0, 0) (1920, 1080)`)
Use a single `(0, 0) (1920, 1080)` block with `setup(width=192, height=108)` to draw the entire slide as a pure 16:9 vector canvas ("一枚絵"):

````markdown
::: block (1700, 1010) (140, 30) z:10
```drawlib file:page.svg
import utils
utils.draw_page_number()
```
:::

::: block (0, 0) (1920, 1080)
```drawlib file:full_hero_canvas.svg
from drawlib.canvas import clear, save, setup
from drawlib.shapes import rectangle
from drawlib.styles import Styles

clear()
setup(width=192, height=108)
rectangle((96, 54), width=192, height=108, style=Styles.WhiteFlat)
rectangle((96, 90), width=172, height=14, style=Styles.PrimaryFlat,
          text="FULL CANVAS HERO STAGE", text_style=Styles.WhiteBold)
save()
```
:::
````

---

## 5. Embedding `drawlib` Diagrams, SVG Fonts & Interactive Animations

### 5.1. Default Inline Vector SVG & Automatic Font Bundling
In slide projects, ````drawlib```` blocks default to **inline SVG** (`file:<name>.svg`):
- The compiled `<svg>` is embedded directly into `<div class="slide-svg-container">`, giving crisp vector scaling at any screen resolution and making all diagram labels searchable with `Ctrl+F`.
- **Automatic SVG Font & Font-Icon Bundling**:
   - Whenever a slide SVG diagram uses Drawlib fonts (`Font`, `FontRoboto`, `FontSourceCode`, CJK fonts, etc.) or font icons (`phosphor`, `fontawesome`), Drawlib automatically embeds font metadata, copies the required `.ttf` / `.otf` files into `_assets/fonts/`, and injects `@font-face` rules into the compiled `style.css`.
   - Both browser viewing (`index.html`) and headless Chromium PDF export (`build_pdf.sh`) render custom fonts and Phosphor/FontAwesome icons identically without requiring system-installed fonts.

### 5.2. Interactive `<canvas>` Animations (`anim-trigger`, `anim-loop`, `anim-pause`)
When a ````drawlib```` block outputs an animated image (**`.png` APNG recommended and default**, or `.apng` / `.webp`), Drawlib embeds its Base64 payload (`data-base64`) into an interactive `<canvas class="drawlib-anim-canvas">` player so it works seamlessly both over HTTP and when opened directly via `file://`. Control playback directly from the code fence attributes:

| Fence Attribute | Values | Default | Behavior |
| :--- | :--- | :--- | :--- |
| `anim-trigger:<mode>` | `auto` \| `click` | `auto` | `click` holds playback at Frame 0 (`READY` badge) until the user clicks the diagram, presses `A`, or clicks **Play Animation** in Presenter View. |
| `anim-loop:<mode>` | `infinite` \| `once` | `infinite` | `once` stops at the final frame (`ENDED` badge); clicking again or pressing `A` resets to Frame 0 (`READY` state). |
| `anim-pause:<frames>` | Comma-separated 0-based indices (e.g. `2,4`) | *(none)* | Automatically pauses playback upon reaching the specified 0-based frame indices (`PAUSED` badge); click or press `A` to resume to the next step. |

#### Interactive Animation Example in a Slide:
````markdown
::: block (880, 140) (960, 840)
```drawlib file:workflow_pipeline.png anim-trigger:click anim-loop:once anim-pause:2,4
from drawlib.anim import Animation
from drawlib.canvas import clear, save, setup
from drawlib.shapes import rectangle
from drawlib.styles import Styles

clear()
setup(width=96, height=84)
anim = Animation(fps=1.0, loop=0)

steps = ["1. Git Push", "2. Detect Diff", "3. Cache Check", "4. Build HTML", "5. Deploy"]
for active_idx in range(len(steps)):
    with anim.frame(duration=0.9):
        for i, label in enumerate(steps):
            st = Styles.AccentFlat if i == active_idx else Styles.Neutral
            txt = Styles.WhiteBold if i == active_idx else Styles.Dark
            rectangle((48, 70 - i * 14), width=60, height=10, style=st, text=label, text_style=txt)
save()
```
:::
````

---

## 6. Speaker Notes (`::: note`) & Dual-Window Presenter View

### 6.1. Authoring Speaker Notes (`::: note` / `::: notes`)
Add speaker notes anywhere inside a slide Markdown file using `::: note` (or `::: notes`). Notes are stripped from the visible slide stage and compiled into `<aside class="slide-notes" hidden>` for Presenter View:

````markdown
::: note
- Emphasize that **SQLite hash caching** restores unchanged diagrams in **< 1ms**.
- Press `A` or click **Play Animation** to step through the pipeline animation, which pauses at Frame 2 and Frame 4.
:::
````
*(If a slide contains multiple `::: note` blocks, they are automatically joined with a blank line `\n\n`.)*

### 6.2. Dual-Window Presenter View (`?presenter=1`)
Press `P` or `S` (or click the `🗒` button in the bottom-right slide controls) to launch the synchronized **Presenter View** window:
- **Real-Time Dual-Window Sync**: Synchronized with the main audience window via `BroadcastChannel` and `postMessage`.
- **2-Column Presenter Workspace**:
  - **Left Column**: Scrollable vertical strip of live 16:9 slide thumbnails for instant jumping.
  - **Right Column**:
    - **Top**: Current slide 16:9 live preview.
    - **Middle Control Bar**: `◀ Prev`, `Next ▶`, **`▶ Play Animation` / `⏸ Pause` / `▶ Resume` / `↺ Replay` button** (automatically synced with `<canvas>` animations on the main screen; disabled when the current slide has no animations), and an elapsed presentation timer (`Click to pause/resume`, `Double-click to reset`).
    - **Bottom**: Formatted Speaker Notes panel with `A-` / `A+` font-size buttons.

### 6.3. Keyboard Shortcuts (`slide.js`)
| Key | Action | Description |
| :--- | :--- | :--- |
| `Right Arrow` / `Space` / `PageDown` | Next Slide | Advance to the next slide. |
| `Left Arrow` / `PageUp` | Previous Slide | Return to the previous slide. |
| `Home` / `End` | First / Last Slide | Jump to the first or last slide in the deck. |
| `A` | Trigger Animation | Play, pause, resume, or replay `<canvas>` animations on the active slide. |
| `P` / `S` | Presenter View | Open synchronized dual-window Presenter View (`?presenter=1`). |
| `O` / `Esc` | Overview Grid | Toggle the thumbnail overview grid of all slides. |
| `F` | Fullscreen | Toggle browser fullscreen mode. |

---

## 7. Reusable Deck Helpers (`utils.py`) & Vector PDF Export

### 7.1. Sharing Layout Macros via `utils.py`
During slide compilation, `slide_src/` is automatically added to Python's import path so any ````drawlib```` block can `import utils` (or `from drawlib.utils import ...`). Use `utils.py` to keep slide Markdown files clean and DRY:
- **Page Counter Helper (`utils.draw_page_number()`)**: Uses `from drawlib.slide import current_slide` with a transparent canvas (`setup(..., alpha=0.0)`) so every slide displays `"2 / 9"`, `"3 / 9"`, etc.
- **Custom SmartArt / Card Macros**: Define deck-specific components (e.g. `draw_curved_agenda()`, `draw_kpi_cards()`, `service_card()`) in `utils.py` and invoke them with data tuples in each slide.

### 7.2. Building HTML & Exporting 1920×1080 Vector PDF
```bash
# Run full slide build (HTML + PDF + Images):
./slide_src/build.sh

# Or run individual CLI commands:
uv run drawlib build html slide_src/ -o slide_html/ -s slide_src/styles.py -u slide_src/utils.py
uv run drawlib build pdf slide_src/ -o slide.pdf -s slide_src/styles.py -u slide_src/utils.py
uv run drawlib serve slide_html/
```

---

## 8. Autonomous 3-Stage Review Checklist for `slide` Projects

1. **Stage 1 — Coordinate & Aspect Ratio Audit**:
   - `::: block (x, y) (w, h)` uses **top-left `(0, 0)`** in `1920×1080` pixels (`Y=40` is top header; `Y=1010` is bottom footer).
   - `setup(width=W, height=H)` inside ````drawlib```` uses **bottom-left `(0, 0)`** (`Y=H` is top; `Y=0` is bottom).
   - Always begin each slide ````drawlib```` block with `clear()` followed by `setup(width=..., height=...)` matching the enclosing `::: block` `(w, h)` aspect ratio.
   - Use `file:<name>.svg` for static diagrams and `file:<name>.png` (or `.webp`) when using `Animation()`.
   - **Relative Paths Only**: Verify that all markdown links, image elements (`![logo](_assets/logo.png)`), and script asset paths use relative paths. Never use absolute paths or `file://` URLs.
2. **Stage 2 — Grid Preview (`drawlib show ... -g` + `view_file`)**:
   - Export complex slide diagrams with `-g` to `.drawlib/scratch/preview.png` and inspect via `view_file` to ensure zero text collisions, `50%+` neutral balance, and clean perimeter margins.
3. **Stage 3 — Full Slide Stage / PDF Verification (`view_file`)**:
   - Run `./slide_src/build.sh` and inspect `slide.pdf` (or `1920×1080` browser screenshots of `slide_html/index.html`) via `view_file` to verify that text and diagrams do not overflow or collide across `::: block` boundaries.
