# 1. Why Drawlib?

Modern software systems evolve at unprecedented speed through pull requests, automated CI/CD pipelines, and AI coding agents (Claude Code, Cursor, Gemini CLI, GitHub Copilot)—shifting the primary engineering bottleneck from writing implementation code to **visualizing system architecture and preventing "Documentation Rot"**. When diagrams and specs are maintained in disconnected manual tools, documentation quickly falls behind the codebase, slowing down onboarding and burying design intent inside ephemeral chat logs and commit histories.

Drawlib eliminates this disconnect by delivering **"Illustration as Code"** and **"Illustrated Documentation as Code" (IDaC)**: unifying declarative pure-Python visuals, inline Markdown embedding, and multi-format technical publishing inside a single Git repository so humans and AI coding agents can author, diff, verify, and publish living visual documentation as code.

```drawlib align=center code=fold file=why_drawlib_hero.png caption="Figure 1.1: Fragmented Legacy Diagramming vs. Drawlib Unified Git Workflow"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.smartarts import CardList, Panel
from drawlib.styles import Styles

setup(width=148, height=66)

left_panel = Panel(
    "Fragmented Legacy Workflow",
    style=Styles.Neutral.patch(shape_r=2.2),
    header_style=Styles.MutedNeutral,
    text_style=Styles.DarkBold.patch(text_size=12.0),
    icon=phosphor.warning,
    icon_style=Styles.DangerBold,
    header_height=9.0,
)
left_panel.draw((5.0, 5.0), width=65.0, height=56.0)

legacy_cards = CardList(
    style=Styles.White.patch(shape_r=1.6),
    text_style=Styles.DarkBold.patch(text_size=11.0),
    description_style=Styles.Dark.patch(text_size=10.0),
    badge_style=Styles.MutedNeutral,
    badge_text_style=Styles.DarkBold.patch(text_size=10.5),
    icon_style=Styles.DarkBold,
    spacing=2.2,
    show_arrows=True,
    arrow_style=Styles.MutedBold,
)
legacy_cards.add(
    "Manual GUI Editing",
    "Opaque binary/XML files outside code review",
    badge_text="1",
    icon=phosphor.wrench,
)
legacy_cards.add(
    "Copy-Paste PNG Chores",
    "Re-export screenshots into Wikis, Docs & Slides",
    badge_text="2",
    icon=phosphor.images,
)
legacy_cards.add(
    "Silent Architecture Drift",
    "Unreviewable PR diffs & stale production docs",
    badge_text="3",
    icon=phosphor.warning,
    style=Styles.DangerNeutral.patch(shape_r=1.6),
    icon_style=Styles.DangerBold,
)
legacy_cards.draw((8.5, 8.0), width=58.0, height=41.0)

line((71.2, 33.0), (76.8, 33.0), arrow_head="->", style=Styles.DarkBold)

right_panel = Panel(
    "Drawlib Unified Git Workflow",
    style=Styles.PrimaryNeutral.patch(shape_r=2.2),
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=12.0),
    icon=phosphor.check_circle,
    icon_style=Styles.PrimaryBold,
    header_height=9.0,
)
right_panel.draw((78.0, 5.0), width=65.0, height=56.0)

drawlib_cards = CardList(
    style=Styles.White.patch(shape_r=1.6),
    text_style=Styles.DarkBold.patch(text_size=11.0),
    description_style=Styles.Dark.patch(text_size=10.0),
    badge_style=Styles.SecondaryNeutral,
    badge_text_style=Styles.DarkBold.patch(text_size=10.5),
    icon_style=Styles.DarkBold,
    spacing=2.2,
    show_arrows=True,
    arrow_style=Styles.DarkBold,
)
drawlib_cards.add(
    "Git-Native Python & Markdown",
    "Readable PR diffs in a single source of truth",
    badge_text="1",
    icon=phosphor.git_branch,
)
drawlib_cards.add(
    "Drawlib Compiler & AI Grid Loop",
    "Deterministic coordinates + -g visual verification",
    badge_text="2",
    icon=phosphor.cpu,
    style=Styles.PrimaryFlat.patch(shape_r=1.6),
    text_style=Styles.WhiteBold.patch(text_size=11.0),
    description_style=Styles.White.patch(text_size=10.0),
    badge_style=Styles.White,
    badge_text_style=Styles.PrimaryBold.patch(text_size=10.5),
    icon_style=Styles.PrimaryBold,
)
drawlib_cards.add(
    "Multi-Target Publishing",
    "HTML, Catalog, PDF, DOCX, 16:9 Slide & PPTX",
    badge_text="3",
    icon=phosphor.globe,
    style=Styles.SecondaryNeutral.patch(shape_r=1.6),
)
drawlib_cards.draw((81.5, 8.0), width=58.0, height=41.0)

save()
```

---

## 1.1 Why Existing Visual Tooling Fails Humans and AI Agents

Engineering teams typically piece together four workarounds for diagrams and technical visuals, each breaking down when maintaining production documentation with AI coding agents:

- **GUI Diagramming Tools & Binary PNGs (`draw.io`, `Figma`, `Visio`, `Slides`)**: Visual editors store diagrams as binary images (`PNG`/`JPEG`) or sprawling XML files. Binary images cannot be diffed in Git pull requests, cannot be inspected or edited by AI coding agents, vary wildly in font/color consistency across authors, and force manual re-exports into wikis, Word specs, and slide decks—guaranteeing silent documentation rot.
- **Text-to-Diagram DSLs (`Mermaid`, `PlantUML`, `Graphviz`)**: Domain-specific text syntaxes integrate cleanly into Markdown, but delegate spatial geometry to rigid black-box layout engines. Inserting a single dependency edge can unexpectedly reshuffle an entire topology, fine-grained brand typography and spacing controls are minimal, and native support for quantitative statistical charts (`BoxChart`, `HeatmapChart`) or rich SmartArts is absent.
- **Raw SVG Generation by AI Agents**: Asking an AI agent to emit raw `<svg>` markup directly fails in practice—computing multilingual (CJK/Latin) font metrics and text wrapping is error-prone (causing labels to overflow box borders), manual arrow routing produces crossed lines and misaligned arrowheads, and hundreds of low-level `<path>` and `<rect>` coordinates are impossible for humans to review or maintain.
- **Scientific Plotting Libraries (`Matplotlib`, `Seaborn`)**: Numeric plotting packages excel at statistical arrays, yet lack native high-level primitives for cloud architecture nodes, container groups, connector routing, standardized icon suites, UML/ER models, SmartArts, and multi-target document compilation. Assembling a clean microservice diagram requires hundreds of lines of low-level imperative boilerplate that frequently triggers AI coordinate and syntax errors.

| Capability | GUI Suites (`draw.io` / `Visio`) | Text DSLs (`Mermaid` / `PlantUML`) | Raw SVG / `Matplotlib` | **Drawlib (`v0.3.10`)** |
| :--- | :--- | :--- | :--- | :--- |
| **Git PR Diffability** | Poor (opaque binary / noisy XML) | High (concise text) | Low (verbose `<path>` / boilerplate) | **High (declarative Python)** |
| **Layout Control** | Manual pixel dragging only | Black-box auto-layout only | Manual axis / pixel math | **Exact Cartesian + 5 Graph Solvers** |
| **Visual Scope** | Diagrams & wireframes | Basic flow / sequence / ER | Low-level shapes or numeric plots | **Icons + SmartArts + Charts + Diagrams + Anim** |
| **Publishing Targets** | Manual image export | Embedded web blocks only | Standalone image files | **HTML, Catalog, PDF, `.docx`, Slide & `.pptx`** |
| **AI Self-Correction** | Unusable by coding agents | Blind to rendered overlaps | High CJK clipping & routing error rate | **Deterministic `-g` Grid Multimodal Loop** |

---

## 1.2 The Three Pillars of Drawlib

Drawlib `v0.3.10` is engineered around three tightly integrated pillars that turn visual communication into a reproducible software engineering discipline.

```drawlib align=center code=fold file=drawlib_pillars.png caption="Figure 1.2: Drawlib Architecture — From Primitives & Visual Engines to Multi-Target Publishing"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.shapes import rectangle
from drawlib.smartarts import ChevronProcess, Panel
from drawlib.styles import Styles
from drawlib.text import text

setup(width=148, height=66)

stages = ChevronProcess(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=11.5),
    description_style=Styles.Dark.patch(text_size=10.0),
    spacing=2.0,
    flat_left_end=True,
)
stages.add("1. Primitives & Icons")
stages.add(
    "2. High-Level Engines",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=11.5),
)
stages.add("3. Multi-Format Publishing", style=Styles.SecondaryNeutral)
stages.draw((6.0, 49.0), width=136.0, height=11.5)

p1 = Panel(
    "Foundation Layer",
    style=Styles.White.patch(shape_r=1.8),
    header_style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=11.0),
    icon=phosphor.cube,
    icon_style=Styles.DarkBold,
    header_height=7.8,
)
p1.draw((6.0, 18.0), width=43.0, height=28.0)
text(
    (10.0, 28.0),
    "• 43 Geometric Shapes\n• Curved & Manhattan Lines\n• CJK & Google Fonts\n• 34 Vector Icon Suites",
    style=Styles.Dark.patch(text_size=10.2, halign="left", text_line_spacing=1.45),
)

p2 = Panel(
    "Declarative Visuals",
    style=Styles.PrimaryNeutral.patch(shape_r=1.8),
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=11.0),
    icon=phosphor.stack,
    icon_style=Styles.PrimaryBold,
    header_height=7.8,
)
p2.draw((52.5, 18.0), width=43.0, height=28.0)
text(
    (56.5, 28.0),
    "• 18 Structured SmartArts\n• 10 Quantitative Charts\n• 6 Domain Diagrams\n• 5 Graph Layout Solvers",
    style=Styles.Dark.patch(text_size=10.2, halign="left", text_line_spacing=1.45),
)

p3 = Panel(
    "Unified Deliverables",
    style=Styles.White.patch(shape_r=1.8),
    header_style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=11.0),
    icon=phosphor.export,
    icon_style=Styles.DarkBold,
    header_height=7.8,
)
p3.draw((99.0, 18.0), width=43.0, height=28.0)
text(
    (103.0, 28.0),
    "• Static Site & Catalog\n• Linear HTML & GitHub MD\n• Headless Vector PDF\n• Editable .docx & .pptx",
    style=Styles.Dark.patch(text_size=10.2, halign="left", text_line_spacing=1.45),
)

rectangle((74.0, 9.5), width=136.0, height=9.5, style=Styles.MutedDashed.patch(shape_r=1.8))
phosphor.grid_four((13.0, 9.5), width=5.0, style=Styles.PrimaryBold)
text(
    (18.5, 9.5),
    "Pillar 3 — Autonomous AI Multimodal Loop: Deterministic (x, y) Geometry + CLI Grid Inspection (drawlib show -g)",
    style=Styles.DarkBold.patch(text_size=10.5, halign="left"),
)

save()
```

### 1.2.1 Pillar 1: Illustration as Code

Every visual asset in Drawlib is a pure-Python program backed by strict Pydantic type validation and reusable theme presets (`GoogleStyles`, `DefaultStyles`, `MonochromeStyles`):

- **Rich Composable Vocabulary**: Combine 43 geometric primitives, curved/orthogonal routed connectors, and **34 standardized vector icon suites** (`phosphor`, `gcp`, `aws`, `azure`, plus 15 domain and 15 flat original icon packs) with **18 SmartArts**, **10 quantitative charts**, **6 software/architecture diagram engines**, **5 automatic graph layout solvers** (`drawlib.graph`), and multi-frame **animations** (`APNG`, `WebP`, `GIF`).
- **Full Python Expressiveness**: Drive diagrams directly from real JSON schemas, OpenAPI specs, benchmark CSVs, or shared helper functions in `utils.py` rather than duplicating labels by hand.

### 1.2.2 Pillar 2: Illustrated Documentation as Code

Drawlib goes beyond standalone image generation by treating Markdown prose and embedded ```` ```drawlib ```` blocks as a single compilation unit:

- **Five Project Archetypes from One Toolchain**: Scaffold multi-page documentation portals (`site`), searchable API/CLI dictionaries (`catalog`), linear engineering whitepapers (`doc`), interactive `16:9` widescreen decks (`slide`), or standalone asset suites (`images`).
- **Multi-Format & Multi-Locale Publishing**: Compile localized `en/` and `ja/` sources with structural skeleton parity checks into responsive HTML (with SEO metadata and `llms.txt`), GitHub-Flavored Markdown, headless Chromium vector PDFs, editable Microsoft Word documents (`.docx`), and native PowerPoint decks (`.pptx`)—cached incrementally in `.drawlib/cache.db`.

### 1.2.3 Pillar 3: Autonomous AI Multimodal Loop

Drawlib is purpose-built from the ground up for collaboration between software engineers and multimodal AI coding agents:

- **Deterministic Coordinates + `-g` Grid Inspection**: Unlike black-box layout DSLs where agents cannot adjust a specific overlapping label, Drawlib's Cartesian coordinate plane and `drawlib show ... -g` (`10`-unit / `5`-unit grid overlay) give AI agents exact spatial coordinates.
- **Closed-Loop Visual Self-Correction**: An AI agent can inspect your codebase, author declarative Drawlib blocks, export a `-g` grid preview, inspect the rendered PNG multimodally to spot any text collision or margin imbalance, and self-correct coordinates in seconds—assisted by built-in documentation via `drawlib rules show`.
