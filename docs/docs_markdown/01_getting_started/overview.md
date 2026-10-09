# About Drawlib

Drawlib is a pure-Python library engineered around the dual paradigms of **"Illustration as Code"** and **"Illustrated Documentation as Code"**.

It empowers human developers, system architects, and **autonomous AI coding agents** to design, version-control, and publish clean architectural schemas, workflow charts, and entire multi-page technical documentation websites directly from declarative Python code.



<figure class="drawlib-image" style="text-align: center;">
  <img src="overview_images/overview_paradigm_shift.png" alt="overview_1" />
  <figcaption class="drawlib-caption">Legacy Diagramming Approaches vs. Drawlib Illustration as Code</figcaption>
</figure>

<details class="drawlib-code-details">
<summary>Source Code</summary>

```python
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=126, height=48)

hdr_dark = Styles.DarkBold.patch(text_size=11.5)
hdr_white = Styles.WhiteBold.patch(text_size=11.5)
ts_title = Styles.DarkBold.patch(text_size=10.5, halign="left")
ts_sub = Styles.Dark.patch(text_size=10.0, halign="left")

# Left container: Legacy Approaches (Fragmented & Fragile)
rectangle((29.5, 24.0), width=53.0, height=42.0, style=Styles.SecondaryNeutral.patch(shape_r=2.0))
rectangle((29.5, 40.5), width=50.0, height=5.5, style=Styles.Neutral.patch(shape_r=1.2), text="Legacy Approaches (Fragile)", text_style=hdr_dark)

rectangle((29.5, 31.5), width=50.0, height=9.2, style=Styles.Neutral.patch(shape_r=1.2))
phosphor.x_circle((8.2, 31.5), width=4.6, style=Styles.Danger)
text((12.0, 33.4), "GUI Drag-and-Drop Tools", style=ts_title)
text((12.0, 29.5), "No Git diffs • Binary PNG rot", style=ts_sub)

rectangle((29.5, 20.5), width=50.0, height=9.2, style=Styles.Neutral.patch(shape_r=1.2))
phosphor.warning((8.2, 20.5), width=4.6, style=Styles.Danger)
text((12.0, 22.4), "Raw SVG XML Generation", style=ts_title)
text((12.0, 18.5), "Text overflows • Manual path math", style=ts_sub)

rectangle((29.5, 9.5), width=50.0, height=9.2, style=Styles.Neutral.patch(shape_r=1.2))
phosphor.x_circle((8.2, 9.5), width=4.6, style=Styles.Danger)
text((12.0, 11.4), "Low-Level Matplotlib", style=ts_title)
text((12.0, 7.5), "Academic API • Heavy boilerplate", style=ts_sub)

# Right container: The Drawlib Solution ("Illustration as Code")
rectangle((96.5, 24.0), width=53.0, height=42.0, style=Styles.Neutral.patch(shape_r=2.0))
rectangle((96.5, 40.5), width=50.0, height=5.5, style=Styles.PrimaryFlat.patch(shape_r=1.2), text="Drawlib: Illustration as Code", text_style=hdr_white)

rectangle((96.5, 31.5), width=50.0, height=9.2, style=Styles.PrimaryNeutral.patch(shape_r=1.2))
phosphor.shapes((75.2, 31.5), width=4.6, style=Styles.Primary)
text((79.0, 33.4), "Declarative Domain APIs", style=ts_title)
text((79.0, 29.5), "Graphs, Diagrams, SmartArts, Charts", style=ts_sub)

rectangle((96.5, 20.5), width=50.0, height=9.2, style=Styles.PrimaryNeutral.patch(shape_r=1.2))
phosphor.git_branch((75.2, 20.5), width=4.6, style=Styles.Primary)
text((79.0, 22.4), "Git & PR Friendly", style=ts_title)
text((79.0, 18.5), "Clean diffs + SQLite build cache", style=ts_sub)

rectangle((96.5, 9.5), width=50.0, height=9.2, style=Styles.PrimaryNeutral.patch(shape_r=1.2))
phosphor.robot((75.2, 9.5), width=4.6, style=Styles.Primary)
text((79.0, 11.4), "AI-Native Self-Correction", style=ts_title)
text((79.0, 7.5), "CLI rules + grid (-g) verification", style=ts_sub)

# Transition arrows from Legacy pain points to Drawlib solutions
line((56.8, 31.5), (69.2, 31.5), arrow_head="->", style=Styles.DarkBold)
line((56.8, 20.5), (69.2, 20.5), arrow_head="->", style=Styles.DarkBold)
line((56.8, 9.5), (69.2, 9.5), arrow_head="->", style=Styles.DarkBold)

save()
```

</details>



---

## The Paradigm Shift: Why Illustration as Code?

In modern software development accelerated by AI coding assistants, code refactoring and feature additions move at an unprecedented pace. However, system architecture documentation, database schemas, and workflow diagrams are frequently left behind—leading to **documentation rot** and onboarding bottlenecks.

### The Limits of GUI Tools in Modern Workflows

Traditional technical diagramming relies on drag-and-drop GUI tools (such as Draw.io, Visio, Lucidchart, or Figma). While convenient for quick whiteboard sketches, managing illustrations as exported binary files (PNG, JPEG) introduces critical flaws:

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

Drawlib treats architectural illustrations as first-class software artifacts governed by standard engineering practices:

1. **Deterministic & Reproducible**: Geometry, spacing, palette shades, and typography are mathematically defined in code. Re-running the build guarantees bit-for-bit identical visual output.
2. **Pull-Request Friendly**: Modifying an architecture (such as adding a microservice or updating an API gateway route) appears as clean, human-readable code diffs in Git.
3. **High-Level Domain Primitives**: Declarative abstractions (`ArchitectureDiagram`, `ChevronProcess`, `Table`, `ArchitectureGraph`) eliminate layout boilerplate while preserving pixel-perfect control.
4. **Algorithmic Geometry**: Leverage loops, list comprehensions, and trigonometric functions to generate grids, circular cycles, and trees without manual drag-and-drop positioning.
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
  <img src="overview_images/drawlib_layered_architecture.png" alt="overview_2" />
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
text((15.5, 18.8), "drawlib.shapes (24 shapes) • lines • text • icons • images", style=sub_dark)

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
   Provides **24** vector shapes (including `cylinder`, `face`, and `bubblespeech`), flexible line connectors with routing and arrowheads, typography, and standardized icon sets (Phosphor, FontAwesome, GCP).
3. **Layer 3: High-Level Visualizations & Geometry (`drawlib.graph`, `drawlib.smartarts`, `drawlib.charts`, `drawlib.diagrams`, `drawlib.math`)**  
   Ready-to-use domain components: auto-layout graphs (`LayerGraph`, `ArchitectureGraph`, `TreeGraph`, `RadialGraph`, `GridGraph`), cloud architectures, flowcharts, sequence diagrams, UML class/state diagrams, ER diagrams, data charts, process flows, geographic maps (`drawlib.smartarts.GeoMap`), and geometry & path/color interpolation utilities (`drawlib.math`).
4. **Layer 4: Animation, Presentation & Document Builder (`drawlib.anim`, `drawlib.slide`, `drawlib.tools`)**  
   Provides multi-frame animation (`drawlib.anim` for APNG & Animated WebP), a 16:9 widescreen slide stage & compiler (`drawlib.slide`), and a programmatic build, preview server, and cache API (`drawlib.tools`) that compiles Markdown files with embedded `drawlib` blocks into responsive static HTML sites, GitHub-ready Markdown, slide decks, and standalone PDF publications.
