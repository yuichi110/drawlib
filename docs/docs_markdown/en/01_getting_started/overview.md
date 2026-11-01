# Why Drawlib

Traditional technical documentation fragments **source code** (Git), **diagrams** (external GUI tools), and **prose** (external wikis)—causing architecture diagrams to inevitably fall out of sync as code evolves.

Drawlib eliminates this fragmentation through **"Illustration as Code"** and **"Illustrated Documentation as Code"**, keeping Python code, diagrams, and multi-format publications synchronized inside a single Git repository.



<figure class="drawlib-image" style="text-align: center;">
  <img src="../../images/01_getting_started/overview/overview_paradigm_shift.png" alt="overview_1" />
  <figcaption class="drawlib-caption">Traditional Workflow vs. Drawlib Workflow (APNG Animation)</figcaption>
</figure>



<div class="drawlib-source-link">
  <a href="https://github.com/yuichi110/drawlib/blob/main/docs/docs_src/en/01_getting_started/overview.md" target="_blank" rel="noopener noreferrer">View animation source code on GitHub &rarr;</a>
</div>

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
