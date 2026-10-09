# Chapter 12: Slide Deck Presentations (`slide`)

In addition to technical documents (`doc`) and multi-page documentation websites (`site`), Drawlib provides first-class support for **16:9 presentation slide decks** (`slide`).

Without relying on drag-and-drop GUI software like PowerPoint or Google Slides, you can author, version-control, and publish conference-ready slide decks directly using Markdown and declarative Python drawing code.

```drawlib 650px center file:fig_slide_layout.png caption:"Figure 12.1: Drawlib Slide Generation Architecture and Dual Outputs"
from drawlib.canvas import setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=140, height=56)

header_ts = Styles.WhiteBold.patch(text_size=9.5)
ts_body = Styles.Dark.patch(text_size=7.5, halign="left")

# 1. Slide Source Markdown & Canvas
rectangle((24.0, 26.0), width=36.0, height=38.0, style=Styles.PrimaryOutline.patch(shape_r=2.0))
rectangle((24.0, 42.0), width=34.0, height=5.5, style=Styles.PrimaryFlat.patch(shape_r=1.5), text="Markdown 16:9 Stage", text_style=header_ts)

phosphor.presentation(xy=(10.0, 33.0), width=4.5, style=Styles.Primary)
text((14.0, 33.0), text="1 Markdown = 1 Slide\n1920x1080 fixed stage", style=ts_body)

phosphor.layout(xy=(10.0, 23.5), width=4.5, style=Styles.Primary)
text((14.0, 23.5), text="SlideContext & Layout\nHeader, content, footer", style=ts_body)

phosphor.code(xy=(10.0, 14.0), width=4.5, style=Styles.Primary)
text((14.0, 14.0), text="```drawlib code blocks\nInline architecture diagrams", style=ts_body)

# 2. Build Pipeline
rectangle((70.0, 26.0), width=28.0, height=38.0, style=Styles.AccentOutline.patch(shape_r=2.0))
rectangle((70.0, 42.0), width=26.0, height=5.5, style=Styles.AccentFlat.patch(shape_r=1.5), text="Compiler Engine", text_style=header_ts)

phosphor.gear(xy=(60.0, 31.0), width=4.5, style=Styles.Accent)
text((64.0, 31.0), text="drawlib build\nSlide AST parsing", style=ts_body)

phosphor.arrows_split(xy=(60.0, 19.0), width=4.5, style=Styles.Accent)
text((64.0, 19.0), text="HTML & PDF\nDual build pipeline", style=ts_body)

# 3. Deliverables
rectangle((116.0, 26.0), width=36.0, height=38.0, style=Styles.SuccessOutline.patch(shape_r=2.0))
rectangle((116.0, 42.0), width=34.0, height=5.5, style=Styles.SuccessFlat.patch(shape_r=1.5), text="Dual Outputs", text_style=header_ts)

phosphor.desktop(xy=(102.0, 33.0), width=4.5, style=Styles.Success)
text((106.0, 33.0), text="Web Presentation\nKeyboard nav & full screen (F)", style=ts_body)

phosphor.file_pdf(xy=(102.0, 23.5), width=4.5, style=Styles.Success)
text((106.0, 23.5), text="1-Slide-1-Page PDF\nPrint & distribution vector PDF", style=ts_body)

phosphor.image(xy=(102.0, 14.0), width=4.5, style=Styles.Success)
text((106.0, 14.0), text="slide_images/\nExtracted high-res diagrams", style=ts_body)

# Connections
line((43.0, 26.0), (55.0, 26.0), arrow_head="->", style=Styles.DarkBold)
text((49.0, 30.0), text="Compile", style=Styles.DarkBold.patch(text_size=7.5))

line((85.0, 26.0), (97.0, 26.0), arrow_head="->", style=Styles.DarkBold)
text((91.0, 30.0), text="Generate", style=Styles.DarkBold.patch(text_size=7.5))
```

## 12.1 Scaffolding a Slide Project (`drawlib init slide`)

Initialize a slide presentation project with a single command:

```bash
# Standard slide deck in current directory (creates slide_src/)
drawlib init slide

# With custom project name, theme, and language:
drawlib init slide my_presentation -s google -l en
```

### Directory Anatomy
```text
my_presentation/
├── slide_src/                 # [SOURCE] Slide Markdown sources and drawing code
│   ├── 01_title.md            # Title slide
│   ├── 02_agenda.md           # Agenda slide
│   ├── 03_architecture.md     # Architecture diagram slide
│   ├── styles.py              # Presentation-wide styling overrides
│   ├── utils.py               # Slide layout components and cards
│   ├── slide.js               # Keyboard navigation and presenter engine
│   ├── build.sh               # Master sequential build script
│   ├── build_html.sh          # Web presentation build script
│   ├── build_pdf.sh           # 16:9 vector PDF export script
│   └── serve.sh               # Local live-reload presentation server
├── slide_html/                # [OUTPUT] Interactive web presentation (index.html)
├── slide.pdf                  # [OUTPUT] Multi-page 16:9 vector presentation PDF
└── slide_images/              # [OUTPUT] Standalone extracted slide diagrams
```

## 12.2 The 16:9 Slide Authoring Model

Drawlib slide decks use an intuitive **"One Markdown File = One Slide"** convention:

- Slide sequence is determined strictly by alphabetical sorting (`01_title.md`, `02_agenda.md`, `03_overview.md`, etc.).
- Every slide is rendered onto a fixed `1920 × 1080` pixel canvas stage that automatically scales to fill any display or projector while preserving its 16:9 aspect ratio.

### Slide Markdown Example
````markdown
# Modernizing System Architecture

<div class="subtitle">Stepwise Migration to an Event-Driven Topology</div>

```drawlib 1400px center file:arch_slide.png
from drawlib.canvas import setup
from drawlib.shapes import rectangle
from drawlib.lines import line
from drawlib.styles import Styles

setup(width=160, height=45)
rectangle((30, 22.5), width=35, height=18, style=Styles.Neutral, text="API Gateway")
rectangle((80, 22.5), width=35, height=18, style=Styles.PrimaryFlat, text="Event Broker", text_style=Styles.WhiteBold)
rectangle((130, 22.5), width=35, height=18, style=Styles.SecondaryNeutral, text="Order Worker")
line((47.5, 22.5), (62.5, 22.5), arrow_head="->", style=Styles.DarkBold)
line((97.5, 22.5), (112.5, 22.5), arrow_head="->", style=Styles.DarkBold)
```
````

## 12.3 Dual Outputs & Presenter Experience

Compiling a `slide` project produces two presentation artifacts optimized for different contexts:

1. **Interactive Web Presentation (`slide_html/index.html`)**:
   - Designed for live presenting on projectors, external displays, or browser screen-shares.
   - **Keyboard Navigation**:
     - `Space` / `→` / `PageDown`: Advance to the next slide
     - `←` / `PageUp`: Go back to the previous slide
     - `F`: Toggle full screen
     - `O` / `Esc`: Toggle slide overview grid
2. **1-Slide-1-Page Vector PDF (`slide.pdf`)**:
   - Designed for attendee distribution, printing, or uploading to slide hosting platforms.
   - Captured via headless Chromium (Playwright), ensuring every slide is rendered with vector sharpness at true 16:9 dimensions (`@page { size: 1920px 1080px; margin: 0; }`).
