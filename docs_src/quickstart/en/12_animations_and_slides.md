# 12. Multi-Frame Animations & 16:9 Slide Decks

Static diagrams capture architecture snapshots, while time-stepped animations and widescreen presentations explain how systems evolve in motion. Drawlib natively compiles multi-frame **APNG (`.png`)**, **Animated WebP (`.webp`)**, and **dither-free Animated GIF (`.gif`)** assets via `drawlib.anim`, and transforms Markdown sources into interactive **16:9 HTML decks**, **vector PDFs**, and **editable PowerPoint (`.pptx`)** presentations via `drawlib.slide`.

```drawlib align=center code=fold file=anim_pipeline.png caption="Figure 12.1: Looping Multi-Frame APNG Pipeline Walkthrough Built with Animation and ChevronProcess"
from drawlib.anim import Animation
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.smartarts import ChevronProcess
from drawlib.styles import Styles
from drawlib.text import text

setup(width=156, height=52)
anim = Animation(fps=1.5, loop=0)

stages = [
    ("1. Commit", "Git Source"),
    ("2. Lint", "Static Audit"),
    ("3. Render", "Grid Check"),
    ("4. Build", "HTML & PDF"),
    ("5. Publish", "Live Docs"),
]

for step in range(len(stages)):
    is_last = step == len(stages) - 1
    with anim.frame(duration=2.5 if is_last else 0.75):
        rectangle((78, 26), width=146, height=42, style=Styles.MutedDashed.patch(shape_r=2.2))
        phosphor.play_circle((10.5, 41.0), width=4.4, style=Styles.DarkBold)
        text(
            (14.5, 41.0),
            "Progressive Release Pipeline (Multi-Frame APNG)",
            style=Styles.DarkBold.patch(text_size=11.0, halign="left"),
        )
        rectangle(
            (134.5, 41.0),
            width=25.0,
            height=6.2,
            style=Styles.PrimaryNeutral.patch(shape_r=1.5),
            text=f"Frame {step + 1} / {len(stages)}",
            text_style=Styles.DarkBold.patch(text_size=10.0),
        )
        line((10, 20.5), (146, 20.5), style=Styles.MutedDashed)

        proc = ChevronProcess(
            style=Styles.Neutral,
            text_style=Styles.DarkBold.patch(text_size=10.6),
            description_style=Styles.Dark.patch(text_size=10.0),
            corner_angle=62.0,
            spacing=1.6,
            flat_left_end=True,
        )
        for i, (title, desc) in enumerate(stages):
            is_active = i == step
            c_style = Styles.PrimaryFlat if is_active else (Styles.PrimaryNeutral if i < step else Styles.Neutral)
            t_style = Styles.WhiteBold.patch(text_size=10.6) if is_active else Styles.DarkBold.patch(text_size=10.6)
            d_style = Styles.White.patch(text_size=10.0) if is_active else Styles.Dark.patch(text_size=10.0)
            proc.add(
                title,
                description=desc,
                style=c_style,
                text_style=t_style,
                description_style=d_style,
                show=(i <= step),
            )
        proc.draw(xy=(10.0, 10.0), width=136.0, height=21.0)

save()
```

---

## 12.1 Multi-Frame Animations with drawlib.anim

### Canvas Lifecycle & The `Animation` API

Import `Animation` from `drawlib.anim`, call `setup(width=..., height=...)` **once before** the frame loop, and wrap each frame's drawing calls inside `with anim.frame(duration=..., clear=True):`:

- **Exact Constructor Signature**: `anim = Animation(fps=10.0, loop=0)` (or `frame_rate=10.0` as an alias for `fps`; `loop=0` plays in a continuous infinite loop).
- **No `file=` Argument on `Animation`**: `Animation` registers automatically with the active canvas and **never** accepts a `file=...` parameter. In standalone scripts, pass the destination path to `save("out.png")`, `save("out.webp")`, or `save("out.gif")`; inside Markdown ```` ```drawlib ```` blocks, set `file=name.png` (or `.webp` / `.gif`) on the fence and end the code block with `save()`.
- **Per-Frame Redraw (`clear=True`) & Final Hold**: By default, `with anim.frame(duration=None, clear=True):` clears the canvas cleanly before each frame so elements can move or change highlight styles without ghosting (`clear=False` is available for purely additive primitive sketches). Give the final frame an explicit hold (`duration=2.0`–`3.0`) so readers can absorb the completed diagram before playback loops.

| Output Format | Extension | Encoding & Visual Characteristics | Best Target Platforms |
| :--- | :--- | :--- | :--- |
| **APNG** | `.png` / `.apng` | Lossless 24-bit RGB + 8-bit alpha; renders natively in browsers and gracefully falls back to a crisp static frame in PDFs | HTML docs (`site` / `doc`), interactive slides, printable whitepapers |
| **Animated WebP** | `.webp` | Lossless 24-bit RGB + 8-bit alpha at ~50% smaller file size (`minimize_size=True`) | High-traffic web documentation portals, mobile web apps |
| **Animated GIF** | `.gif` | `v0.3.10` dither-free 256-color global Median Cut quantization (`Image.Dither.NONE`)—zero grain noise on flat `Neutral` cards | GitHub READMEs, Slack, Notion, Confluence, X/Twitter, legacy viewers |

### Progressive Component Idioms (`show=False`, `draw_ratio` & Interpolation)

Every high-level Drawlib module is engineered for jitter-free frame progression:

- **Slot-Preserving Reveals (`show=False`)**: Passing `show=False` to `SmartArts` items (`ChevronProcess`, `Table`, `GridLayout`, `Cycle`) or toggling `node.show = False` on `Diagrams` (`FlowDiagram`, `ArchitectureDiagram`, `SequenceDiagram`) hides the element and its connected edges while keeping all column widths, coordinates, and spacing 100% locked across frames.
- **Smooth Chart Growth (`draw_ratio`)**: Every chart series/slice/task (`LineChart`, `BarChart`, `AreaChart`, `PieChart`, `GanttChart`) exposes `s.draw_ratio` (`0.0` to `1.0`) and `s.draw_direction` (`"bottom_to_top"` or `"left_to_right"`) with locked `min_value` / `max_value` axes.
- **Motion & Color Interpolation**: Compute smooth trajectories (including eased ratios such as $t^2(3 - 2t)$) or waypoint steps with `drawlib.math.get_intermediate_points()` / `get_intermediate_path_points()`, and fade card fills via `drawlib.styles.get_intermediate_colors(c1, c2, num=..., include_ends=True)`.

```python
from drawlib.anim import Animation
from drawlib.canvas import save, setup
from drawlib.charts.bar import BarChart
from drawlib.styles import Styles

setup(width=110, height=64)
anim = Animation(fps=10.0, loop=0)

chart = BarChart(
    categories=["Q1", "Q2", "Q3", "Q4"],
    axis_line_style=Styles.MutedDashed,
    axis_text_style=Styles.Dark.patch(text_size=10.0),
    grid_style=Styles.MutedThin,
    width=86,
    height=44,
    title="Quarterly API Throughput (kRPS)",
    title_style=Styles.DarkBold.patch(text_size=12.5),
)
chart.configure_y_axis(min_value=0, max_value=120)
series = chart.add_series("Throughput", [42, 68, 94, 112], style=Styles.PrimaryFlat)

steps = 6
for i in range(1, steps + 1):
    t = i / steps
    eased = t * t * (3.0 - 2.0 * t)  # Smoothstep easing (0 -> 1)
    series.draw_ratio = eased
    with anim.frame(duration=2.2 if i == steps else 0.12):
        chart.draw(xy=(12, 8))

save("throughput_growth.gif")
```

---

## 12.2 16:9 Slide Decks & PowerPoint Export (drawlib.slide)

Scaffolding a presentation project with `uv run drawlib init project slide pitch -l en,ja -s google` turns numbered Markdown files (`pitch_src/<lang>/*.md`) into a `1920×1080` (`16:9`) multi-target presentation suite:

- **Dual-Layer Stage & Speaker Notes (`::: block` & `::: note`)**:
  - **`::: block xy=(x, y) width=W height=H`**: Places visual-first cards, 2-column splits, `---` horizontal rules, and embedded ```` ```drawlib ```` diagrams at exact top-left pixel coordinates on the `1920×1080` stage (matching diagram aspect ratios via `setup(width=W/10, height=H/10)`).
  - **`::: note`**: Stores full presenter scripts and technical deep dives off-stage—rendered in synchronized **Dual-Window Presenter View (`?presenter=1`, `P` / `S` key)** and exported directly into PowerPoint speaker notes while keeping the audience slide clean.
- **Runtime Slide Context & Progressive Builds (`drawlib.slide`)**:
  - `from drawlib.slide import current_slide, draw_page_number, draw_section_header` provides `current_slide.index`, `current_slide.total`, and `current_slide.text` (`"4 / 12"`), enabling dynamic footers, progressive multi-slide builds, and full-bleed chapter dividers (`variant="split" | "centered" | "banner" | "minimal"`).
  - Interactive `<canvas>` animations inside slides can be stepped live on click or `A` keypress via fence attributes (`anim_trigger=click anim_loop=once anim_pause=(1, 3)`).

````markdown
::: block xy=(1700, 1010) width=140 height=30
```drawlib file=page.svg
from drawlib.slide import draw_page_number

draw_page_number()
```
:::

::: block xy=(80, 40) width=1760 height=60
# Zero-Trust API Gateway Rollout
:::

::: block xy=(80, 140) width=720 height=820
## Key Rollout Milestones

- **Edge mTLS**: Mutual certificate pinning
- **JWT Cache**: Sub-millisecond Redis lookup
- **Canary Gate**: Automated SLO rollback

---

*Active Deck Position: Slide 3*
:::

::: block xy=(840, 140) width=1000 height=820
```drawlib file=gateway_stage.svg
from drawlib.canvas import clear, save, setup
from drawlib.shapes import rectangle
from drawlib.slide import current_slide
from drawlib.styles import Styles

clear()
setup(width=100, height=82)
rectangle(
    (50, 41),
    width=76,
    height=34,
    style=Styles.PrimaryFlat.patch(shape_r=2.5),
    text=f"Gateway Topology ({current_slide.text})",
    text_style=Styles.WhiteBold.patch(text_size=14.5),
)
save()
```
:::

::: note
Walk through the three milestones on the left, then highlight how `current_slide` binds slide numbering automatically during HTML, PDF, and `.pptx` compilation.
:::
````

```drawlib align=center code=fold file=slide_anatomy.png caption="Figure 12.2: 16:9 Slide Deck Compilation Anatomy — Markdown Stage & Notes to HTML, Vector PDF, and Editable .pptx"
from drawlib.canvas import save, setup
from drawlib.diagrams.architecture import ArchitectureDiagram, Node, NodeGroup, PhosphorIcon
from drawlib.styles import Styles

setup(width=158, height=62)

d = ArchitectureDiagram(
    node_style=Styles.DarkBold,
    node_text_style=Styles.DarkBold.patch(text_size=10.5),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=10.0),
    node_card_style=Styles.Neutral,
)

src = d.add(
    NodeGroup(
        title="Slide Source (slide_src/<lang>/*.md)",
        width=48.0,
        height=52.0,
        style=Styles.PrimaryNeutral.patch(shape_r=2.2),
        text_style=Styles.DarkBold.patch(text_size=10.5, halign="left"),
    ),
    xy=(2.0, 3.0),
)
b_stage = src.add(
    Node(
        "::: block & # Title\n(1920x1080 Stage)",
        width=39.0,
        height=12.0,
        icon=PhosphorIcon.LAYOUT,
        icon_size=4.8,
        card_style=Styles.White.patch(shape_r=1.6),
    ),
    xy=(24.0, 39.5),
)
b_code = src.add(
    Node(
        "Embedded drawlib\n& current_slide",
        width=39.0,
        height=12.0,
        icon=PhosphorIcon.CODE,
        icon_size=4.8,
        card_style=Styles.White.patch(shape_r=1.6),
    ),
    xy=(24.0, 25.0),
)
b_note = src.add(
    Node(
        "::: note Script\n(Speaker Notes)",
        width=39.0,
        height=12.0,
        icon=PhosphorIcon.NOTE,
        icon_size=4.8,
        card_style=Styles.White.patch(shape_r=1.6),
    ),
    xy=(24.0, 10.5),
)

compiler = d.add(
    Node(
        "Slide Compiler\n& Chromium DOM",
        width=33.0,
        height=20.0,
        icon=PhosphorIcon.CPU,
        icon_size=5.6,
        style=Styles.WhiteBold,
        text_style=Styles.WhiteBold.patch(text_size=11.0),
        card_style=Styles.PrimaryFlat.patch(shape_r=2.2),
    ),
    xy=(75.5, 29.0),
)

out_html = d.add(
    Node(
        "16:9 HTML Deck\n(?presenter=1 & SVG)",
        width=41.0,
        height=13.0,
        icon=PhosphorIcon.PRESENTATION_CHART,
        icon_size=4.8,
        card_style=Styles.PrimaryNeutral.patch(shape_r=1.8),
    ),
    xy=(131.5, 45.5),
)
out_pdf = d.add(
    Node(
        "16:9 Vector PDF\n(slide_<lang>.pdf)",
        width=41.0,
        height=13.0,
        icon=PhosphorIcon.FILE_PDF,
        icon_size=4.8,
        card_style=Styles.Neutral.patch(shape_r=1.8),
    ),
    xy=(131.5, 29.0),
)
out_pptx = d.add(
    Node(
        "Editable .pptx Deck\n(Shapes & Notes)",
        width=41.0,
        height=13.0,
        icon=PhosphorIcon.SLIDESHOW,
        icon_size=4.8,
        card_style=Styles.SecondaryNeutral.patch(shape_r=1.8),
    ),
    xy=(131.5, 12.5),
)

d.connect(src, compiler, routing="direct", padding=0.8)
j_mid = d.junction((101.5, 29.0))
j_top = d.junction((101.5, 45.5))
j_bot = d.junction((101.5, 12.5))
d.connect(compiler, j_mid, arrow="-", routing="direct", padding=(0.8, 0.0))
d.connect(j_mid, j_top, arrow="-", routing="direct")
d.connect(j_mid, j_bot, arrow="-", routing="direct")
d.connect(j_top, out_html, arrow="->", routing="direct", padding=(0.0, 0.8))
d.connect(j_mid, out_pdf, arrow="->", routing="direct", padding=(0.0, 0.8))
d.connect(j_bot, out_pptx, arrow="->", routing="direct", padding=(0.0, 0.8))

d.draw(xy=(2.0, 2.0))
save()
```

### Scaffolding & Building HTML, PDF, and Editable PowerPoint (`.pptx`)

Every scaffolded `slide` project includes ready-to-run build scripts for interactive HTML, 16:9 vector PDF, and native Microsoft PowerPoint export (`drawlib build pptx` translates `::: block` cards, text boxes, lists, tables, and `::: note` speaker notes into editable `960×540 pt` PowerPoint elements while embedding diagrams at `240 DPI`):

```bash
# 1. Scaffold a bilingual 16:9 slide deck project
uv run drawlib init project slide pitch -l en,ja -s google

# 2. Compile interactive 16:9 HTML deck + 1920x1080 vector PDF + standalone assets
./pitch_src/build.sh

# 3. Export native editable PowerPoint decks (pitch_en.pptx & pitch_ja.pptx)
./pitch_src/build_pptx.sh
# Equivalent CLI command:
uv run drawlib build pptx pitch_src/ -o pitch.pptx -s pitch_src/styles.py -u pitch_src/utils.py
```
