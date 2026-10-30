# Chapter 12: Slide Deck Presentations (`slide`)

In addition to technical documents (`doc`) and multi-page documentation websites (`site`), Drawlib provides first-class support for **16:9 presentation slide decks** (`slide`).

Without relying on drag-and-drop GUI software like PowerPoint or Google Slides, you can author, version-control, and publish conference-ready slide decks directly using Markdown and declarative Python drawing code.

```drawlib align=center file=fig_slide_layout.png caption="Figure 12.1: Drawlib Slide Generation Architecture and Multi-Format Outputs"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=136, height=54)

header_ts = Styles.WhiteBold.patch(text_size=10.5)
ts_body = Styles.Dark.patch(text_size=10.0, halign="left")
ts_arrow = Styles.DarkBold.patch(text_size=10.0)

# 1. Slide Source Markdown & Canvas
rectangle((21.5, 27.0), width=35.0, height=44.0, style=Styles.PrimaryNeutral.patch(shape_r=2.0))
rectangle((21.5, 45.0), width=33.0, height=6.0, style=Styles.PrimaryFlat.patch(shape_r=1.5), text="1. Markdown 16:9", text_style=header_ts)

phosphor.presentation(xy=(7.8, 35.0), width=4.4, style=Styles.Primary)
text((10.8, 35.0), text="1 MD = 1 Slide\n1920x1080 stage", style=ts_body)

phosphor.layout(xy=(7.8, 23.5), width=4.4, style=Styles.Primary)
text((10.8, 23.5), text="::: block / note\nVisual stage & notes", style=ts_body)

phosphor.code(xy=(7.8, 12.0), width=4.4, style=Styles.Primary)
text((10.8, 12.0), text="current_slide\nAuto content bounds", style=ts_body)

# 2. Build Pipeline
rectangle((68.0, 27.0), width=35.0, height=44.0, style=Styles.Neutral.patch(shape_r=2.0))
rectangle((68.0, 45.0), width=33.0, height=6.0, style=Styles.AccentFlat.patch(shape_r=1.5), text="2. Build Engine", text_style=header_ts)

phosphor.gear(xy=(54.3, 35.0), width=4.4, style=Styles.Accent)
text((57.3, 35.0), text="drawlib build\nSlide AST parser", style=ts_body)

phosphor.database(xy=(54.3, 23.5), width=4.4, style=Styles.Accent)
text((57.3, 23.5), text=".drawlib/cache.db\nIncremental render", style=ts_body)

phosphor.arrows_split(xy=(54.3, 12.0), width=4.4, style=Styles.Accent)
text((57.3, 12.0), text="HTML / PDF / PPTX\nMulti-target engine", style=ts_body)

# 3. Deliverables
rectangle((114.5, 27.0), width=35.0, height=44.0, style=Styles.SecondaryNeutral.patch(shape_r=2.0))
rectangle((114.5, 45.0), width=33.0, height=6.0, style=Styles.DarkFlat.patch(shape_r=1.5), text="3. Slide Outputs", text_style=header_ts)

phosphor.desktop(xy=(100.8, 35.0), width=4.4, style=Styles.Dark)
text((103.8, 35.0), text="Web Presentation\nPresenter View (P)", style=ts_body)

phosphor.file_pdf(xy=(100.8, 23.5), width=4.4, style=Styles.Dark)
text((103.8, 23.5), text="PDF & PPTX Decks\nPrint & editable slides", style=ts_body)

phosphor.image(xy=(100.8, 12.0), width=4.4, style=Styles.Dark)
text((103.8, 12.0), text="*_images/\nExtracted diagrams", style=ts_body)

# Connections
line((39.5, 27.0), (50.0, 27.0), arrow_head="->", style=Styles.DarkBold)
text((44.75, 31.0), text="Parse", style=ts_arrow)

line((86.0, 27.0), (96.5, 27.0), arrow_head="->", style=Styles.DarkBold)
text((91.25, 31.0), text="Export", style=ts_arrow)

save()
```

## 12.1 Scaffolding a Slide Project (`drawlib init slide`)

Initialize a slide presentation project with a single command:

```bash
# Standard slide deck in current directory (creates slide_src/)
uv run drawlib init slide

# With custom project name, theme, and language:
uv run drawlib init slide my_presentation -s google -l en
```

### Directory Anatomy
Running `uv run drawlib init slide my_presentation -s google -l en` creates the following workspace layout:

```text
.
├── my_presentation_src/           # [SOURCE] Slide Markdown sources and drawing code
│   ├── _assets/                   # Static images and logos referenced in slides
│   ├── 01_title.md                # Title slide
│   ├── 02_agenda.md               # Agenda slide
│   ├── 03_architecture.md         # Architecture diagram slide
│   ├── styles.py                  # Presentation-wide styling overrides
│   ├── utils.py                   # Slide layout helpers and components
│   ├── slide.js                   # Keyboard navigation and presenter view engine
│   ├── build.sh                   # Master sequential build script
│   ├── build_html.sh              # Web presentation build script
│   ├── build_pdf.sh               # 16:9 vector PDF export script
│   └── serve.sh                   # Local live-reload presentation server
├── my_presentation_html/          # [OUTPUT] Interactive web presentation (index.html)
├── my_presentation.pdf            # [OUTPUT] Multi-page 16:9 vector presentation PDF
└── my_presentation_images/        # [OUTPUT] Standalone extracted slide diagrams
```

## 12.2 The 16:9 Slide Authoring Model (`::: block` / `::: note` and `current_slide`)

Drawlib slide decks combine an intuitive **"One Markdown File = One Slide"** convention with a **Dual-Layer Architecture (`::: block` and `::: note`)** and dynamic **`current_slide` (`SlideContext`)** layout calculation:

1. **Dual-Layer Architecture (`::: block` vs. `::: note`)**:
   - **`::: block` (Visual Stage Layer)**: Renders concise bullet cards, multi-column layouts, and embedded ````drawlib```` diagrams onto the `1920 × 1080` visual stage for the audience.
   - **`::: note` (Speaker Notes & Handout Layer)**: Holds detailed speaker talking points and comprehensive explanations below the slide. Hidden from the main audience projection, it appears in **Presenter View** during live talks.
2. **Dynamic Stage Bounds via `current_slide` (`SlideContext`)**:
   - Importing `from drawlib.slide import current_slide` inside a slide's ````drawlib```` block exposes `current_slide.content_box`, allowing diagrams to automatically size themselves to the remaining stage area below headings and `::: block` elements.

### Slide Markdown Example
````markdown
# Modernizing System Architecture

<div class="subtitle">Stepwise Migration to an Event-Driven Topology</div>

::: block
- **Decoupled Services**: Isolate API Gateway from background workers via an event broker
- **Resilience**: Automated backpressure handling and idempotent retries under peak load
:::

```drawlib align=center code=fold file=arch_slide.png caption="Event-Driven Pipeline"
from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.slide import current_slide
from drawlib.styles import Styles

# Inspect available slide stage area via current_slide.content_box
box = current_slide.content_box
setup(width=132, height=38)

ts_card = Styles.DarkBold.patch(text_size=11.0)
ts_primary = Styles.WhiteBold.patch(text_size=11.0)

rectangle((24, 19), width=34, height=18, style=Styles.Neutral, text="API Gateway", text_style=ts_card)
rectangle((66, 19), width=34, height=18, style=Styles.PrimaryFlat, text="Event Broker", text_style=ts_primary)
rectangle((108, 19), width=34, height=18, style=Styles.SecondaryNeutral, text="Order Worker", text_style=ts_card)

line((41, 19), (49, 19), arrow_head="->", style=Styles.DarkBold)
line((83, 19), (91, 19), arrow_head="->", style=Styles.DarkBold)
save()
```

::: note
Walk the audience through our transition from synchronous RPC chains to asynchronous event streaming.
Highlight how horizontal scaling on the Order Worker eliminates checkout latency spikes during flash sales.
:::
````

## 12.3 Multi-Format Outputs (Web, PDF & PowerPoint) and Presenter View

In addition to the standard HTML and vector PDF builds, `slide` projects can also export editable MS PowerPoint decks on demand:

1. **Interactive Web Presentation (`my_presentation_html/index.html`)**:
   - Designed for live presenting on projectors, external displays, or browser screen-shares.
   - **Keyboard Navigation & Presenter View**:
     - `Space` / `→` / `PageDown`: Advance to the next slide
     - `←` / `PageUp`: Go back to the previous slide
     - `P` key (or append `?presenter=1` to the URL): Launch **Presenter View**, displaying the current slide, next slide preview, elapsed timer, and `::: note` speaker notes while staying synchronized in real time with the audience display window.
     - `F`: Toggle full screen
     - `O` / `Esc`: Toggle slide overview grid
2. **1-Slide-1-Page Vector PDF (`my_presentation.pdf`)**:
   - Designed for attendee distribution, printing, or uploading to slide hosting platforms (SpeakerDeck, DocSend).
   - Captured via automatically managed headless Chromium (Playwright), ensuring every slide is rendered with vector sharpness at true 16:9 dimensions (`@page { size: 1920px 1080px; margin: 0; }`).
3. **Optional Editable 16:9 MS PowerPoint Export (`drawlib build pptx`)**:
   - When conference organizers or stakeholders require an editable `.pptx` deck, export a 16:9 MS PowerPoint file (with `::: note` content mapped directly to PowerPoint speaker notes) via the CLI (similarly, `doc` projects support editable MS Word export via `uv run drawlib build docx <src> -o <out.docx> --generate-index`):
   ```bash
   uv run drawlib build pptx my_presentation_src/ -o my_presentation.pptx
   ```
