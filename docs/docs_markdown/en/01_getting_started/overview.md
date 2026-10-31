# Why Drawlib

Traditional technical documentation fragments **source code** (Git), **diagrams** (external GUI tools), and **prose** (external wikis)—causing architecture diagrams to inevitably fall out of sync as code evolves.

Drawlib eliminates this fragmentation through **"Illustration as Code"** and **"Illustrated Documentation as Code"**, keeping Python code, diagrams, and multi-format publications synchronized inside a single Git repository.



<figure class="drawlib-image" style="text-align: center;">
  <img src="../../images/01_getting_started/overview/overview_paradigm_shift.png" alt="overview_1" />
  <figcaption class="drawlib-caption">Traditional Workflow vs. Drawlib Workflow (APNG Animation)</figcaption>
</figure>

<details class="drawlib-code-details">
<summary>Source Code</summary>

```python
from __future__ import annotations

import os
from drawlib.anim import Animation
from drawlib.canvas import save, setup
from drawlib.icons import ai, code, devops, phosphor, workspace
from drawlib.images import image
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.styles import Styles
from drawlib.text import text

# 16:9 widescreen canvas matching index.md (128 x 72)
setup(width=128, height=72)
anim = Animation(fps=10.0, loop=0)

FAVICON_PATH = (
    "_assets/favicon.png"
    if os.path.exists("_assets/favicon.png")
    else "../_assets/favicon.png"
)

TITLE_TRAD = Styles.DarkBold.patch(text_size=15.5, halign="left")
TITLE_DRAWLIB = Styles.PrimaryBold.patch(text_size=15.5, halign="left")
SUB_MUTED = Styles.MutedBold.patch(text_size=10.5, halign="right")
SUB_PRIMARY = Styles.PrimaryBold.patch(text_size=10.5, halign="right")

TOOL_TEXT = Styles.DarkBold.patch(text_size=11.0, halign="left")
STEP_TEXT = Styles.DarkBold.patch(text_size=11.5, halign="left")
STEP_TEXT_WHITE = Styles.WhiteBold.patch(text_size=11.5, halign="left")

TOOL_CARD = Styles.Neutral.patch(
    shape_fill_color=(246, 248, 252),
    shape_line_color=(200, 212, 228),
    shape_line_width=1.2,
    shape_r=1.6,
)
STEP_CARD = Styles.Neutral.patch(
    shape_fill_color=(255, 255, 255),
    shape_line_color=(208, 218, 232),
    shape_line_width=1.2,
    shape_r=1.6,
)
STEP_CARD_HERO = Styles.PrimaryFlat.patch(shape_r=1.6)


def draw_drawio_badge(xy: tuple[float, float], size: float = 5.0) -> None:
    """Draw a clean Draw.io-style orange diagram app icon."""
    cx, cy = xy
    rectangle(
        xy,
        width=size,
        height=size,
        style=Styles.Neutral.patch(
            shape_fill_color=(240, 135, 5),
            shape_line_width=0,
            shape_r=0.9,
        ),
    )
    top_pt = (cx, cy + size * 0.23)
    bl_pt = (cx - size * 0.24, cy - size * 0.23)
    br_pt = (cx + size * 0.24, cy - size * 0.23)
    wire = Styles.White.patch(line_width=1.1)
    line(top_pt, bl_pt, style=wire)
    line(top_pt, br_pt, style=wire)
    node_st = Styles.Neutral.patch(shape_fill_color=(255, 255, 255), shape_line_width=0, shape_r=0.2)
    for pt in (top_pt, bl_pt, br_pt):
        rectangle(pt, width=size * 0.30, height=size * 0.22, style=node_st)


def draw_step_badge(xy: tuple[float, float], num: str, *, inverted: bool = False) -> None:
    """Draw numbered circular step badge."""
    if inverted:
        circle(
            xy,
            radius=2.6,
            style=Styles.Neutral.patch(
                shape_fill_color=(255, 255, 255),
                shape_line_width=0,
            ),
        )
        text(xy, num, style=Styles.PrimaryBold.patch(text_size=10.5))
    else:
        circle(
            xy,
            radius=2.6,
            style=Styles.Neutral.patch(
                shape_fill_color=(238, 244, 255),
                shape_line_color=(180, 198, 228),
                shape_line_width=1.1,
            ),
        )
        text(xy, num, style=Styles.PrimaryBold.patch(text_size=10.5))


def draw_traditional_scene(visible_steps: int) -> None:
    """Scene 1: Traditional 4-step workflow across Word, VS Code, and Draw.io."""
    # Header
    phosphor.arrows_left_right((10.5, 64.0), width=4.8, style=Styles.Danger)
    text((14.8, 64.0), "Traditional Workflow", style=TITLE_TRAD)
    text((120.0, 64.0), "Switching Across 3 Disconnected Tools", style=SUB_MUTED)
    line((8.0, 58.2), (120.0, 58.2), style=Styles.MutedThin)

    steps = [
        ("1", "word", "Word", "Write initial design spec in Word", 49.5),
        ("2", "vscode_ai", "VS Code", "Develop application code", 37.0),
        ("3", "drawio", "Draw.io", "Read code & manually draw diagrams in Draw.io", 24.5),
        ("4", "word", "Word", "Read code, write Word spec & paste diagrams", 12.0),
    ]

    for idx in range(visible_steps):
        num, tool_key, tool_label, desc, y = steps[idx]

        # Context-switch connector between different tools
        if idx > 0:
            prev_y = steps[idx - 1][4]
            line(
                (21.5, prev_y - 4.7),
                (21.5, y + 4.7),
                arrow_head="->",
                style=Styles.DangerDashed.patch(line_width=1.3),
            )

        # Left tool pill (x = 8.0 .. 35.0, cx = 21.5, width = 27.0)
        rectangle((21.5, y), width=27.0, height=9.2, style=TOOL_CARD)
        if tool_key == "word":
            workspace.word((15.0, y), width=5.0, style=Styles.Neutral)
            text((19.2, y), tool_label, style=TOOL_TEXT)
        elif tool_key == "vscode_ai":
            code.vscode((12.4, y), width=4.4, style=Styles.Neutral)
            ai.gemini((17.3, y), width=4.3, style=Styles.Neutral)
            text((21.2, y), tool_label, style=TOOL_TEXT)
        else:
            draw_drawio_badge((15.0, y), size=4.8)
            text((19.2, y), tool_label, style=TOOL_TEXT)

        # Right action card (x = 37.5 .. 120.0, cx = 78.75, width = 82.5)
        rectangle((78.75, y), width=82.5, height=9.2, style=STEP_CARD)
        draw_step_badge((42.5, y), num)
        text((47.0, y), desc, style=STEP_TEXT)


def draw_drawlib_scene(visible_steps: int) -> None:
    """Scene 2: Drawlib 3-step workflow unified inside VS Code + GitHub Repo + AI Agent."""
    # Header
    image((10.5, 64.0), width=5.4, image=FAVICON_PATH)
    text((15.0, 64.0), "Drawlib Workflow", style=TITLE_DRAWLIB)
    text((120.0, 64.0), "Unified in VS Code + GitHub Repository", style=SUB_PRIMARY)
    line((8.0, 58.2), (120.0, 58.2), style=Styles.MutedThin)

    # Unified GitHub / Git Repository container (x = 7.0 .. 121.0, y = 6.0 .. 55.0)
    rectangle(
        (64.0, 30.5),
        width=114.0,
        height=49.0,
        style=Styles.PrimaryNeutral.patch(
            shape_fill_color=(245, 248, 255),
            shape_line_color=(165, 185, 232),
            shape_line_width=1.4,
            shape_r=2.2,
        ),
    )
    devops.github((11.8, 51.0), width=4.2, style=Styles.Neutral)
    text(
        (15.4, 51.0),
        "GitHub / Git Repository (Specs, Source Code & Illustrated Docs Together)",
        style=Styles.DarkBold.patch(text_size=10.5, halign="left"),
    )

    steps = [
        ("1", "Design specs in Git Repo with AI Agent & Drawlib", 40.2, False),
        ("2", "Develop application code", 26.8, False),
        ("3", "AI Agent reads repo code & auto-writes illustrated docs", 13.4, True),
    ]

    for idx in range(visible_steps):
        num, desc, y, is_hero = steps[idx]

        if idx > 0:
            prev_y = steps[idx - 1][2]
            line(
                (23.5, prev_y - 4.9),
                (23.5, y + 4.9),
                arrow_head="->",
                style=Styles.PrimaryBold.patch(line_width=1.4),
            )

        # Left tool pill: Always VS Code + Gemini AI Agent across all 3 steps
        rectangle(
            (23.5, y),
            width=27.0,
            height=9.6,
            style=STEP_CARD.patch(shape_line_color=(175, 192, 230)),
        )
        code.vscode((14.4, y), width=4.4, style=Styles.Neutral)
        ai.gemini((19.3, y), width=4.3, style=Styles.Neutral)
        text((23.2, y), "VS Code", style=TOOL_TEXT)

        # Right action card (x = 39.5 .. 118.0, cx = 78.75, width = 78.5)
        rectangle(
            (78.75, y),
            width=78.5,
            height=9.6,
            style=STEP_CARD_HERO if is_hero else STEP_CARD,
        )
        draw_step_badge((44.2, y), num, inverted=is_hero)
        text(
            (48.6, y),
            desc,
            style=STEP_TEXT_WHITE if is_hero else STEP_TEXT,
        )


# -------------------------------------------------------------------------
# Scene 1: Traditional Workflow (4 progressive steps + read hold)
# -------------------------------------------------------------------------
with anim.frame(duration=0.95):
    draw_traditional_scene(1)

with anim.frame(duration=0.95):
    draw_traditional_scene(2)

with anim.frame(duration=0.95):
    draw_traditional_scene(3)

with anim.frame(duration=2.70):
    draw_traditional_scene(4)

# -------------------------------------------------------------------------
# Scene 2: Drawlib Workflow (3 progressive steps + read hold)
# -------------------------------------------------------------------------
with anim.frame(duration=1.05):
    draw_drawlib_scene(1)

with anim.frame(duration=1.00):
    draw_drawlib_scene(2)

with anim.frame(duration=3.20):
    draw_drawlib_scene(3)

save()
```

</details>



---

## The Paradigm Shift: Why Illustration as Code?

In modern software development accelerated by AI coding assistants, code refactoring and feature additions move at an unprecedented pace. However, system architecture documentation, database schemas, and workflow diagrams are frequently left behind—leading to **documentation rot** and onboarding bottlenecks.

### The Limits of GUI Tools in Modern Workflows

Traditional technical diagramming relies on drag-and-drop GUI tools (such as Draw.io, Visio, Lucidchart, or Figma). While convenient for quick whiteboard sketches, managing illustrations as exported binary files (PNG, JPEG) across disconnected wikis introduces critical flaws:

- **Severe Tool Fragmentation**: Updating a single microservice route requires editing code in Git, manually opening an external GUI canvas to redraw boxes, exporting a PNG, and re-uploading it to an external document or wiki.
- **No Meaningful Version Control**: Binary images cannot produce meaningful Git diffs in pull requests. Reviewers cannot inspect what architectural components changed.
- **AI Agents Cannot Edit Binary Assets**: While AI coding agents can read and edit codebases seamlessly, they cannot manipulate pixels or drag-and-drop canvas elements in GUI software.
- **Visual & Branding Drift**: Colors, stroke widths, paddings, and font sizes drift unpredictably across team members, diluting corporate design standards.

### The Pitfalls of Raw SVG & Direct Matplotlib Generation

When engineers attempt to automate diagramming via code, they often ask AI agents to generate raw SVG XML or low-level Matplotlib scripts. In practice, both approaches quickly break down:

- **Raw SVG Generation**:
  - LLMs cannot accurately compute font glyph widths or dynamic multi-line text wrapping without a browser layout engine, frequently causing text to overflow boundary boxes.
  - Computing precise connection vectors, orthogonal routes, and arrowheads by hand requires excessive trigonometric calculations that easily misalign.
  - Generating hundreds of raw `<path>` and `<polygon>` elements creates unmaintainable blobs of XML that humans cannot easily review or audit.
- **Direct Matplotlib Scripting**:
  - Matplotlib was originally engineered for academic data visualization (scatter plots, histograms, line graphs), not software systems engineering.
  - It lacks native abstractions for architectural components (nodes, boundary containers, sequence lifelines, decision gates, standardized cloud icons).
  - Authors must write dozens of lines of low-level boilerplate just to draw and style a single labeled box with an icon.

### The Drawlib Solution: "Illustration as Code"

Drawlib treats architectural illustrations and technical documents as first-class software artifacts governed by standard engineering practices:

1. **Single Source of Truth in Git**: Code, Markdown prose, and declarative Python diagrams live side by side in the same repository and update atomically in a single commit.
2. **Deterministic & Reproducible**: Geometry, spacing, palette shades, and typography are mathematically defined in code. Re-running the build guarantees bit-for-bit identical visual output.
3. **High-Level Domain Primitives**: Declarative abstractions (`ArchitectureDiagram`, `ChevronProcess`, `Table`, `ArchitectureGraph`) eliminate layout boilerplate while preserving pixel-perfect control.
4. **Multi-Format Compilation**: Compile a single Markdown source into static HTML websites, GitHub Markdown, vector-crisp PDFs, MS Word (`.docx`) documents, and 16:9 HTML/PDF/PowerPoint (`.pptx`) slide decks.
5. **Centralized Style Governance**: Theme tokens (`DefaultStyles`, `GoogleStyles`, `MonochromeStyles`) ensure that shapes, connectors, text, and icons adhere to a cohesive visual hierarchy.

---

## AI-Native by Design

Drawlib is purposely designed for the era of **AI-assisted software development**.

Large Language Models (LLMs) and AI coding agents (such as Claude Code, Cursor, Gemini) excel at writing declarative code, but struggle with manual visual tools. Because Drawlib drawings are expressed entirely as clean Python code or embedded Markdown blocks (` ```drawlib `), AI agents can:

- **Understand Existing Diagrams**: Parse and refactor diagrams simply by reading Python source code.
- **Generate Complex Diagrams**: Autonomously write full cloud architectures, sequence diagrams, and flowcharts based on repository code analysis.
- **Inspect Syntax Rules On-Demand**: AI agents can query the library's built-in manual directly via the CLI (`drawlib rules show <topic>`).
- **Autonomous Visual Self-Correction**: Agents can export images with coordinate overlays (`drawlib show -g`), visually inspect them with multimodal vision tools, and self-correct label clipping or line overlaps.

---

## Layered Architecture

Drawlib is structured into four cohesive layers, ensuring both low-level flexibility and high-level productivity:



<figure class="drawlib-image" style="text-align: center;">
  <img src="../../images/01_getting_started/overview/drawlib_layered_architecture.png" alt="overview_2" />
  <figcaption class="drawlib-caption">Drawlib Layered Architecture</figcaption>
</figure>

<details class="drawlib-code-details">
<summary>Source Code</summary>

```python
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=120, height=54)

title_dark = Styles.DarkBold.patch(text_size=11.5, halign="left")
sub_dark = Styles.Dark.patch(text_size=10.5, halign="left")
title_white = Styles.WhiteBold.patch(text_size=11.5, halign="left")
sub_white = Styles.White.patch(text_size=10.5, halign="left")

# Layer 4: Animation, Slide & Doc Builder
rectangle((60.0, 45.0), width=112.0, height=10.0, style=Styles.PrimaryNeutral.patch(shape_r=1.5))
phosphor.stack((10.5, 45.0), width=5.2, style=Styles.Primary)
text((15.5, 47.0), "Layer 4: Animation, Slide & Doc Builder", style=title_dark)
text((15.5, 42.8), "drawlib.anim • drawlib.slide • drawlib.tools • CLI Compiler", style=sub_dark)

# Layer 3: High-Level Visualizations
rectangle((60.0, 33.0), width=112.0, height=10.0, style=Styles.Neutral.patch(shape_r=1.5))
phosphor.cube((10.5, 33.0), width=5.2, style=Styles.Primary)
text((15.5, 35.0), "Layer 3: High-Level Visualizations & Geometry", style=title_dark)
text((15.5, 30.8), "drawlib.graph • diagrams • smartarts • charts • math", style=sub_dark)

# Layer 2: Drawing Primitives
rectangle((60.0, 21.0), width=112.0, height=10.0, style=Styles.SecondaryNeutral.patch(shape_r=1.5))
phosphor.paint_brush((10.5, 21.0), width=5.2, style=Styles.Primary)
text((15.5, 23.0), "Layer 2: Drawing Primitives & Assets", style=title_dark)
text((15.5, 18.8), "drawlib.shapes (43 shapes) • lines • text • icons • images", style=sub_dark)

# Layer 1: Core Engine (Hero anchor)
rectangle((60.0, 9.0), width=112.0, height=10.0, style=Styles.PrimaryFlat.patch(shape_r=1.5))
phosphor.gear((10.5, 9.0), width=5.2, style=Styles.WhiteBold)
text((15.5, 11.0), "Layer 1: Core Engine (Foundation)", style=title_white)
text((15.5, 6.8), "drawlib.canvas • styles • types • fonts (Cartesian Engine)", style=sub_white)

save()
```

</details>



1. **Layer 1: Core Engine (`drawlib.canvas`, `drawlib.styles`, `drawlib.types`, `drawlib.fonts`)**  
   Manages canvas lifecycle, Cartesian coordinate systems, local coordinate transforms, theme resolution, and universal font typography.
2. **Layer 2: Drawing Primitives (`drawlib.shapes`, `drawlib.lines`, `drawlib.text`, `drawlib.icons`, `drawlib.images`)**  
   Provides **43** vector shapes (including `cylinder`, `cube`, `document`, `cloud`, `brace`, `gear`, `math_symbol`, `face`, and `bubblespeech`), flexible line connectors with routing and arrowheads, typography, and **34 standardized icon modules** totaling **4,538 icons** (`phosphor` vector icons, `gcp` / `aws` / `azure` cloud icons, 15 official domain brand packs, and 15 Drawlib Original 2D pastel packs).
3. **Layer 3: High-Level Visualizations & Geometry (`drawlib.graph`, `drawlib.smartarts`, `drawlib.charts`, `drawlib.diagrams`, `drawlib.math`)**  
   Ready-to-use domain components: auto-layout graphs (`LayerGraph`, `ArchitectureGraph`, `TreeGraph`, `RadialGraph`, `GridGraph`), cloud architectures, flowcharts, sequence diagrams, UML class/state diagrams, ER diagrams, data charts, process flows, geographic maps (`drawlib.smartarts.GeoMap`), and geometry & path/color interpolation utilities (`drawlib.math`).
4. **Layer 4: Animation, Presentation & Document Builder (`drawlib.anim`, `drawlib.slide`, `drawlib.tools`)**  
   Provides multi-frame animation (`drawlib.anim` for APNG & Animated WebP), a 16:9 widescreen slide stage & compiler (`drawlib.slide`), and a programmatic build, preview server, and cache API (`drawlib.tools`) that compiles Markdown files with embedded `drawlib` blocks into responsive static HTML sites, GitHub-ready Markdown, standalone PDF & MS Word (`.docx`) documents, and 16:9 HTML/PDF/PowerPoint (`.pptx`) slide decks.
