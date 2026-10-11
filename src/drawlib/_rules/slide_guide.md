# Drawlib Slide Deck Design & Best Practices Guide (`slide-guide`)

This guide defines the **narrative structure, visual hierarchy, Dual-Layer (`::: block` vs. `::: note`) authoring standard, layout variety, and component selection rules** for creating professional 16:9 presentation decks with Drawlib.

*(For technical `slide_src/` directory structure, `1920×1080` coordinate systems, `::: block` options, animation attributes, and build scripts, run `uv run drawlib rules show project-slide`. For the `drawlib.slide` Python runtime API, run `uv run drawlib rules show lib-slide`.)*

---

## 1. Core Principle: Dual-Layer Authoring (`::: block` vs. `::: note`)

The single most common failure when creating technical presentations—especially for AI coding agents—is **"Document-on-Slide" (スライドのドキュメント化)**: cramming long paragraphs, 6–8 dense bullet points, and full technical explanations directly onto the visible slide stage (`::: block`).

Drawlib enforces a strict **Dual-Layer Separation Principle**:
1. **Layer 1 — Audience Stage (`::: block`): Visual-First & Scannable in 3 Seconds**
   - **Diagrams Take Center Stage**: Allocate **50%–75%+** of the slide stage to rich Drawlib illustrations (`SmartArts`, `Diagrams`, `Graphs`, `Charts`, `Icons`).
   - **Minimal Keyword Text**: Keep stage text to **1 clear slide headline** and **at most 3–4 short bullet points** per block.
   - **1 Line per Bullet (Phrase, Not Prose)**: Write concise noun phrases, key-value pairs, or metrics (`**L7 Spoofing**: Bypasses edge firewall via valid TLS`, ~5–12 words or 20–35 CJK characters). Never write multi-sentence paragraphs inside `::: block`.
2. **Layer 2 — Presenter Notes (`::: note`): Complete Technical Explanation (Mandatory)**
   - **Standard on Every Content Slide**: Every content slide must include a `::: note` block containing the full technical narrative, background context, step-by-step walkthrough of the diagram, and talking points.
   - **Offload Complexity to `::: note`**: Whenever you need to explain *why* an architecture works, detailed incident timelines, edge cases, or exact formulas, write that explanation inside `::: note` instead of crowding `::: block`.
   - **Dual Benefit**: During live delivery, `::: note` renders cleanly in **Presenter View (`?presenter=1`, `P` / `S` key)** while staying hidden from the audience screen and vector PDF (`slide.pdf`). In Git, anyone reading the `.md` source file gets a complete, self-contained technical document.

```drawlib center fold-code file:slide_guide_dual_layer.png caption:"Dual-Layer Slide Principle: Visual-First Audience Stage (::: block) + Deep Explanation in Speaker Notes (::: note)"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=152, height=64, dpi=150)

rectangle((76, 32), width=146, height=58, style=Styles.MutedDashed.patch(shape_r=2.5))
text(
    (76, 55.5),
    "Dual-Layer Slide Standard: Simple Visual Stage (::: block) + Rich Notes (::: note)",
    style=Styles.DarkBold.patch(text_size=12.0),
)

# Left Card: Layer 1 - Audience Stage (::: block)
rectangle((41, 27.5), width=64, height=42, style=Styles.PrimaryNeutral.patch(shape_r=2.0))
phosphor.presentation_chart((15, 43.0), width=5.0, style=Styles.PrimaryBold)
text((43, 43.0), "1. Audience Stage (::: block)", style=Styles.PrimaryBold.patch(text_size=11.5))
text(
    (41, 35.5),
    "Visible on 1920x1080 Screen & PDF",
    style=Styles.Muted.patch(text_size=9.8),
)
line((13, 32.5), (69, 32.5), style=Styles.Primary)
text(
    (41, 20.0),
    "• 50%–75% Rich Drawlib Visuals\n• Max 3–4 short bullets (1 line each)\n• Keywords & KPIs (3-second scan)\n• ZERO long prose paragraphs",
    style=Styles.Dark.patch(text_size=10.2),
)

# Center Arrow
line((74, 27.5), (84, 27.5), arrow_head="<->", style=Styles.DarkBold)
text((79, 32.5), "Offload\nDetails", style=Styles.DarkBold.patch(text_size=9.8))

# Right Card: Layer 2 - Presenter Notes (::: note)
rectangle((115, 27.5), width=60, height=42, style=Styles.SecondaryNeutral.patch(shape_r=2.0))
phosphor.note((91, 43.0), width=5.0, style=Styles.SecondaryBold)
text((117, 43.0), "2. Speaker Notes (::: note)", style=Styles.SecondaryBold.patch(text_size=11.5))
text(
    (115, 35.5),
    "Presenter View (?presenter=1) & Git .md",
    style=Styles.Muted.patch(text_size=9.8),
)
line((89, 32.5), (141, 32.5), style=Styles.Secondary)
text(
    (115, 20.0),
    "• Mandatory on every content slide\n• Full background & causal rationale\n• Step-by-step diagram walkthrough\n• Deep metrics, Q&A & edge cases",
    style=Styles.Dark.patch(text_size=10.2),
)

save()
```

### Example: Authoring a Complex Technical Slide Correctly

````markdown
::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils
utils.draw_page_number()
```
:::

::: block (80, 40) (1760, 60)
# Why L7 DDoS Bypasses Traditional Firewalls
:::

::: block (80, 140) (720, 820)
## Key Threat Characteristics

- **Valid TLS Handshake**: Indistinguishable from normal users at L3/L4
- **Cache-Busting Queries**: Randomized URLs force origin hits
- **DB Pool Exhaustion**: 5,000 RPS saturates backend connections
- **Mitigation**: Edge behavioral WAF + adaptive rate limiting
:::

::: block (840, 140) (1000, 820)
```drawlib file:l7_attack_arch.svg
from drawlib.canvas import clear, save, setup
from drawlib.icons import phosphor
from drawlib.styles import Styles
import utils

clear()
setup(width=100, height=82)
# High-level cards & connectors with icons & 50%+ neutral balance
utils.service_card((24, 52), width=34, height=22, title="CDN / Edge WAF", subtitle="Cache Hit: 3%", icon=phosphor.shield_warning, style=Styles.PrimaryNeutral)
utils.service_card((76, 52), width=34, height=22, title="Primary DB", subtitle="Pool Exhausted!", icon=phosphor.database, style=Styles.DangerFlat, title_style=Styles.WhiteBold, subtitle_style=Styles.White)
utils.connect((41, 52), (59, 52), label="5,000 RPS")
save()
```
:::

::: block (80, 1010) (820, 30) font:14px
*DDoS Incident Response Playbook*
:::

::: note
**Presenter Talking Points & Technical Deep Dive**:
1. **Why L3/L4 Volumetric Defense Failed**: Traditional SYN flood filters and bandwidth scrubbing saw normal packet sizes and valid TLS 1.3 handshakes. Total bandwidth remained under 800 Mbps, well below our 10 Gbps pipe limit.
2. **Walkthrough of the Architecture Diagram (Right)**:
   - Point to the CDN Edge node: attackers rotated query parameters (`?search=<uuid>`) so cache hit ratio dropped from 94% to 3%.
   - Point to the Primary DB node (highlighted in `DangerFlat`): each cache miss triggered a heavyweight SQL join, exhausting the 500-connection pool within 40 seconds.
3. **Key Takeaway**: We must enforce JA3/JA4 TLS fingerprinting and per-path rate limiting at the Cloud Armor / WAF tier before requests ever reach the application pods.
:::
````

---

## 2. Deck Narrative Arc & Mandatory Structural Slides

A presentation deck is a visual story, not a flat dump of topical pages. Every deck must follow a clear narrative arc with four mandatory structural slide types:

```drawlib center fold-code file:slide_guide_deck_arc.png caption:"Mandatory 4-Part Presentation Deck Narrative Arc"
from drawlib.canvas import save, setup
from drawlib.smartarts import ChevronProcess
from drawlib.styles import Styles

setup(width=152, height=44, dpi=150)

proc = ChevronProcess(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=10.5),
    description_style=Styles.Dark.patch(text_size=9.5),
    corner_angle=60.0,
    spacing=2.2,
    flat_left_end=True,
)
proc.add(
    "1. Cover Slide",
    description="01_title.md\nTitle, Tagline, Hero\n(No body / page #)",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=10.5),
    description_style=Styles.White.patch(text_size=9.5),
)
proc.add(
    "2. Agenda Slide",
    description="02_agenda.md\nChapter Roadmap\n(draw_curved_agenda)",
    style=Styles.PrimaryNeutral,
    text_style=Styles.PrimaryBold.patch(text_size=10.5),
)
proc.add(
    "3. Chapter Loop",
    description="01_section.md + Content\nSection Divider ->\nVisual Content Slides",
    style=Styles.Neutral,
)
proc.add(
    "4. Summary & Action",
    description="Closing Slide\nKey Takeaways, KPIs\n& Next Steps",
    style=Styles.SecondaryNeutral,
    text_style=Styles.SecondaryBold.patch(text_size=10.5),
)
proc.draw(xy=(5, 7), width=142.0, height=30.0)

save()
```

### 2.1. Cover / Title Slide (`01_title.md` or `00_opening/01_title.md`)
- **Purpose**: Establish the presentation title, core value proposition, presenter identity, and visual brand.
- **Strict Rules**:
  - **Never start body bullet points, problem explanations, or multi-box diagrams on Slide 1.**
  - **No Header Chrome or Page Counter**: Do not place a `(80, 40)` top slide header or `(1700, 1010)` page number (`1 / N`) on the cover slide.
  - Pair the title and metadata block (`(160, 240) (1160, 600)`) with a clean hero emblem, logo, or minimal conceptual visual on the right (`(1360, 260) (400, 480)`), or use a full-bleed cover canvas (`(0, 0) (1920, 1080)`).

### 2.2. Agenda / Roadmap Slide (`02_agenda.md` or `00_opening/02_agenda.md`)
- **Purpose**: Give the audience a clear mental map of the presentation's chapters before diving into details.
- **Strict Rules**:
  - Always include an Agenda slide immediately after the Cover slide (or after a 1-slide Executive Hook).
  - Use the built-in `utils.draw_curved_agenda()` helper or a `SmartArts` component (`ChevronProcess`, `BoxList`, `GridLayout`) rather than plain Markdown numbered lists.

### 2.3. Section / Chapter Divider Slides (`01_section.md` per Chapter)
- **Purpose**: Signal major topic transitions (every 3–6 slides) so the audience always knows where they are in the story.
- **Strict Rules**:
  - Organize decks of 8+ slides into numbered chapter subdirectories (e.g., `00_opening/`, `01_incident_overview/`, `02_root_cause/`, `03_defense_architecture/`, `04_summary/`).
  - Begin each chapter subdirectory with a dedicated **Section Divider slide** (`01_section.md`) featuring the chapter number, title, and a 1-line subtitle on a high-impact full-bleed or centered stage layout.
  - **Exclude Planning & Draft Files with `_`**: Store any deck outlines, storyboards, or scratch notes inside `slide_src/` with a leading underscore (e.g., `_CONTENTS_PLANNING.md`, `_drafts/`). Files/directories starting with `_` and `README.md` are automatically excluded from compilation.

### 2.4. Closing Summary / Takeaways Slide
- **Purpose**: Leave the audience with 3–4 memorable conclusions, quantitative outcomes, or concrete action items.
- **Strict Rules**:
  - Use `utils.draw_kpi_cards()`, `smartarts.GridLayout`, or `smartarts.BoxList` with Phosphor icons to summarize key takeaways visually.

---

## 3. Ban on Primitive Box-Spam: Use High-Level Components & `utils.py`

> **CRITICAL RULE**: Never construct slide illustrations out of raw `rectangle()` and `line()` calls ("Primitive Box-Spam"). Hand-rolled boxes without icons, semantic hierarchy, or structured layout engines make slides look amateurish and monotonous.

Always select the appropriate high-level Drawlib component or `utils.py` helper for the concept being presented:

| Slide Concept / Story | Required Drawlib Component / Helper | Avoid |
| :--- | :--- | :--- |
| **Agenda / Table of Contents** | `utils.draw_curved_agenda()`, `smartarts.BoxList` | Plain bullet lists or bare rectangles |
| **Headline KPIs / SLA Metrics** | `utils.draw_kpi_cards()`, `smartarts.GridLayout` | Unstyled text inside `rectangle()` |
| **Step-by-Step Process / Playbook** | `smartarts.ChevronProcess`, `diagrams.FlowDiagram`, `smartarts.Cycle` | Row of manual `rectangle()` + `line()` |
| **Cloud / Network / System Topology** | `diagrams.ArchitectureDiagram`, `graph.ArchitectureGraph`, `utils.service_card()` + `utils.connect()` | Bare boxes without icons or tier containers |
| **Attack / API / Protocol Timeline** | `diagrams.SequenceDiagram`, `diagrams.StateDiagram`, `charts.GanttChart` | Manual horizontal lines with text labels |
| **Quantitative Trends & Comparisons** | `charts.LineChart`, `AreaChart`, `BarChart`, `PieChart`, `RadarChart` | Writing numbers only in prose bullets |
| **Feature Matrix / Trade-off Analysis**| `smartarts.Table`, `smartarts.GridLayout` | Cramped Markdown tables with tiny fonts |
| **Layered / Defense-in-Depth Stack** | `smartarts.Pyramid`, `smartarts.TreeNode`, `graph.LayerGraph` | Stacked plain rectangles |
| **Visual Anchors on Every Node** | `icons.phosphor`, `icons.gcp`, `icons.fontawesome` | Text-only shapes with zero iconography |

---

## 4. Layout Variety & Visual Rhythm Across the Deck

Repeating the exact same `Left Text (740px) + Right Diagram (980px)` split across 10+ consecutive slides creates visual fatigue. Rotate among these **5 standard stage layouts** to match the geometry of each slide's content:

| Layout Pattern | `::: block` Stage Coordinates `(x, y) (w, h)` | Best Used For |
| :--- | :--- | :--- |
| **1. Two-Column Split**<br>*(Narrative Left + Diagram Right)* | Left: `(80, 140) (720, 820)`<br>Right: `(840, 140) (1000, 820)` → `setup(100, 82)` | Architecture topologies, vertical flows, radar/pie charts, 2x2 grids |
| **2. Top-Bottom Wide Split**<br>*(Summary Top + Wide Diagram Bottom)* | Top: `(80, 130) (1760, 190)`<br>Bottom: `(80, 340) (1760, 620)` → `setup(176, 62)` | Multi-stage horizontal pipelines (`ChevronProcess`), wide `SequenceDiagram`, `GanttChart`, timelines |
| **3. Full-Stage Visual Diagram**<br>*(100% Visual + `::: note` Narrative)* | Main: `(80, 140) (1760, 820)` → `setup(176, 82)` | Comprehensive end-to-end `ArchitectureDiagram`, `Table` comparison matrices, multi-cluster `ArchitectureGraph` |
| **4. KPI Cards + Chart Split**<br>*(Metrics Left + Trend Chart Right)* | Left: `(80, 140) (760, 820)` (`draw_kpi_cards`)<br>Right: `(880, 140) (960, 820)` (`LineChart` / `BarChart`) | Executive impact summaries, before/after benchmark comparisons, incident scale metrics |
| **5. Full-Bleed Hero / Divider**<br>*(1920×1080 Canvas)* | Stage: `(0, 0) (1920, 1080)` → `setup(192, 108)` | Cover slides (`01_title.md`), Chapter Section Dividers (`01_section.md`), high-impact closing slides |

---

## 5. Typography, Color Discipline & Spatial Margins

### 5.1. Calibrating In-Diagram `text_size` for 1920×1080 Slides (Block-Width Math)

Drawlib's rendering engine normalizes the full canvas width `setup(width=W, height=H)` to **`10 inches = 720 points`** (`720 × H/W pt` tall), and CSS fits the image into `::: block (x, y) (W_block, H_block)` via `object-fit: contain`. Therefore, the actual rendered font size on the **`1920×1080` slide stage** is:

$$\text{Rendered Slide Font Size (px)} = \text{text\_size} \times \text{scale} \times \min\!\left(\frac{W_{\text{block}}}{720},\; \frac{H_{\text{block}}}{720 \times (H / W)}\right)$$

> **CRITICAL SLIDE TYPOGRAPHY RULE**:
> Never blindly copy Web Documentation font sizes (`text_size = 9.5–10.5`, which are calibrated for `16px` HTML body text in a `900px` column) into a 2-column slide block!
> On a **`1920×1080` slide**, Markdown body text (`p`, `li`) is **`26px`** (`h2` is `34px`, `h1` is `52px`). If you place `text_size = 9.5` inside a `1000px` right-hand column (or a `700px` KPI column), it renders at only **`9px–13px`**—less than half the size of the `26px` slide text beside it!

Always calibrate `text_size` according to the enclosing **`::: block` width ($W_{\text{block}}$)** so rendered labels stay **`>= 18px–24px`** on the `1920×1080` stage:

| Enclosing `::: block` Type | Block Width $W_{\text{block}}$ | Scale Factor (`px/pt`) | Node / Axis / Table / Edge `text_size` | Card / Chart Title `text_size` | Rendered Size on `1920×1080` Stage |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Full-Width / Top-Bottom Wide** | `1760px` | `~2.44 px/pt` | **`11.0` – `13.0`** *(floor `10.5`)* | **`14.0` – `16.0`** | **`27px` – `32px`** *(matches `26px` prose)* |
| **Two-Column Split (Right Diagram)**| `960px` – `1040px` | `~1.33 – 1.44 px/pt` | **`13.5` – `15.5`** *(floor `12.5`)* | **`16.0` – `18.5`** | **`18px` – `22px`** *(clear & legible)* |
| **Narrow Column (KPI Cards, etc.)** | `660px` – `760px` | `~0.95 – 1.05 px/pt` | **`14.0` – `17.0`** *(KPI value `22.0+`)*| **`18.0` – `20.0`** | **`14px` – `24px`** *(never microscopic)* |

- **Match Canvas Aspect Ratio (`1:10` Rule)**: Always set `setup(width=W_block / 10, height=H_block / 10)` (e.g., `setup(width=104, height=81)` for `::: block (800, 140) (1040, 810)`). If $H / W > H_{\text{block}} / W_{\text{block}}$, `object-fit: contain` will letterbox the image horizontally and shrink all fonts!
- **Never Shrink 2-Column Diagrams with `scale < 1.0`**: Passing `d.draw(..., scale=0.8)` inside a 2-column block compounds font shrinkage. Instead, reduce the number of steps/nodes, tighten `step_y` / `padding`, or switch to a **Full-Stage** or **Top-Bottom Wide** block.
- **Shorten In-Node Labels & Widen Cards**: When using `text_size = 13.5–15.5` in 2-column diagrams, keep node labels to **1–3 punchy words per line** and increase node `width` / `height` or `column_widths` so larger text never clips.

### 5.2. 50%+ Neutral Baseline (No All-Red / Rainbow Slides)
- Even in incident postmortems or security decks, **never color every box red (`Danger`) or orange (`Warning`)**. When everything is highlighted as an alert, nothing stands out.
- Ground **50% or more of shapes in calm neutral styles** (`Styles.Neutral`, `Styles.PrimaryNeutral`, `Styles.SecondaryNeutral`, `Styles.MutedDashed`).
- Reserve saturated fills (`Styles.PrimaryFlat`, `Styles.AccentFlat`, `Styles.DangerFlat`, `Styles.SuccessFlat`) strictly for **1–2 primary focal points** per diagram (e.g., the single bottleneck database or the primary defense gateway).

### 5.3. Vertical Safe Zones & Language Consistency
- **Respect the Footer Safe Zone (`Y <= 960`)**: The slide footer and page counter live at `Y: 995..1040`. Ensure main content blocks end at or above `Y = 960` (`y + h <= 960`) so text and diagrams never collide with the footer.
- **Language & Terminology Consistency**: Match the language of slide headers (`# Title`), footer text, and diagram labels to the presentation's target language (e.g., in a Japanese deck initialized with `--lang ja`, write slide titles and footers in natural Japanese rather than leaving English template placeholders).

---

## 6. Slide Deck Best Practices Checklist (Do's & Don'ts)

| Category | ❌ Anti-Pattern (Never Do This) | ✅ Best Practice (Always Do This) |
| :--- | :--- | :--- |
| **Text vs. Notes** | Writing long paragraphs or 6–8 verbose bullets inside `::: block` | Keep `::: block` to **3–4 short 1-line phrases**; put all deep explanations in **`::: note`** |
| **Cover Slide** | Starting problem statements, bullet lists, or page numbers on `01_title.md` | Keep `01_title.md` strictly to **Title, Subtitle, Speaker/Date, and Hero Visual** (no header/page #) |
| **Navigation** | Jumping straight from Cover into technical details without a roadmap | Place an **Agenda slide (`02_agenda.md`)** and insert **Section Dividers (`01_section.md`)** between chapters |
| **Non-Slide Files**| Leaving `PLANNING.md` or `notes.md` unprefixed in `slide_src/` so they compile as slides | Prefix non-slide files/folders with **`_`** (e.g., `_CONTENTS_PLANNING.md`, `_drafts/`) |
| **Diagrams** | Drawing every slide with primitive `rectangle()` + `line()` boxes | Use **`SmartArts`**, **`Diagrams`**, **`Graphs`**, **`Charts`**, **`utils.py` helpers**, and **`phosphor`/`gcp` icons** |
| **Layout Rhythm** | Using identical Left-Text / Right-Diagram split on all 15+ slides | Alternate among **2-Column Split**, **Top-Bottom Wide Split**, **Full-Stage Visual**, and **KPI + Chart** layouts |
| **Color Balance** | Coloring all nodes `DangerFlat` / `WarningFlat` / `PrimaryFlat` | Maintain **50%+ Neutral** cards (`Styles.Neutral`, `PrimaryNeutral`) and highlight only **1–2 focal nodes** |
| **Diagram Fonts** | Using Web-doc `text_size=9.5` or `scale < 1.0` inside 2-column slide blocks (renders `<13px` vs `26px` prose) | Scale `text_size` by block width: **`11.0–13.0`** (full-width `1760px`), **`13.5–15.5`** (2-col `1000px`), **`14.0–17.0`** (narrow `700px`) |
