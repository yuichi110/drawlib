# About Drawlib

Drawlib is a pure-Python library engineered around the dual paradigms of **"Illustration as Code"** and **"Documentation as Code"**.

It empowers human developers, system architects, and **autonomous AI coding agents** to design, version-control, and publish clean architectural schemas, workflow charts, and entire multi-page technical documentation websites directly from declarative Python code.

---

## The Paradigm Shift: Why Illustration as Code?

Traditional technical diagramming relies heavily on drag-and-drop GUI software (such as Microsoft Visio, Lucidchart, Figma, or Draw.io). While accessible for quick whiteboard brainstorming, GUI tools introduce severe architectural bottlenecks into modern software development:

- **No Meaningful Version Control**: Binary files or monolithic XML/JSON blobs make Git diffs unreadable and merge conflicts impossible to resolve collaboratively.
- **Visual Drift & Branding Decay**: Colors, stroke widths, alignments, and font sizes drift unpredictably across team members, diluting corporate visual consistency.
- **High Maintenance Overhead**: Keeping diagrams in sync with rapid codebase changes requires opening external tools, manually re-drawing components, exporting PNGs, and updating image links.

### The Drawlib Solution

Drawlib treats architectural illustrations as first-class software artifacts governed by standard engineering practices:

1. **Deterministic & Reproducible**: Geometry, spacing, palette shades, and typography are mathematically defined in code. Re-running the build guarantees bit-for-bit identical visual output.
2. **Pull-Request Friendly**: Modifying an architecture (such as adding a microservice or updating an API gateway route) appears as clean, human-readable code diffs in Git.
3. **Algorithmic Geometry**: Leverage loops, list comprehensions, and trigonometric functions to generate grids, circular cycles, and trees without manual drag-and-drop positioning.
4. **Centralized Style Governance**: Theme tokens (`DefaultStyles`, `GoogleStyles`, `MonochromeStyles`) ensure that shapes, connectors, text, and icons adhere to a cohesive visual hierarchy.

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

```drawlib fold-code 650px center file:drawlib_layered_architecture.png caption:"Drawlib Layered Architecture"
from drawlib.canvas import setup
from drawlib.shapes import rectangle
from drawlib.styles import Styles

setup(width=120, height=60)

# Layers
rectangle((60, 50), width=110, height=11, style=Styles.PrimaryFlat, text="Layer 4: Document Builder & CLI (HTML, Markdown, PDF)", text_style=Styles.WhiteBold)
rectangle((60, 37), width=110, height=11, style=Styles.AccentFlat, text="Layer 3: High-Level Visualizations (Diagrams, Charts, SmartArts)", text_style=Styles.WhiteBold)
rectangle((60, 24), width=110, height=11, style=Styles.SecondaryFlat, text="Layer 2: Drawing Primitives (Shapes, Lines, Text, Icons, Images)", text_style=Styles.WhiteBold)
rectangle((60, 11), width=110, height=11, style=Styles.SuccessFlat, text="Layer 1: Core Engine (Canvas, Coordinates, Theming, Fonts)", text_style=Styles.WhiteBold)
```

1. **Layer 1: Core Engine (`drawlib.canvas`, `drawlib.styles`)**  
   Manages canvas lifecycle, Cartesian coordinate systems, theme resolution, and universal font typography.
2. **Layer 2: Drawing Primitives (`drawlib.shapes`, `drawlib.lines`, `drawlib.text`, `drawlib.icons`, `drawlib.images`)**  
   Provides 23 vector shapes (including 3D cylinders), flexible line connectors with routing and arrowheads, typography, and standardized icon sets (Phosphor, FontAwesome, GCP).
3. **Layer 3: High-Level Visualizations (`drawlib.graph`, `drawlib.smartarts`, `drawlib.charts`, `drawlib.diagrams`)**  
   Ready-to-use domain components: auto-layout graphs, cloud architectures, flowcharts, sequence diagrams, UML class diagrams, ER diagrams, data charts, and process flows.
4. **Layer 4: Document Builder & CLI (`drawlib._builder`, `drawlib._cli`)**  
   Compiles Markdown files with embedded `drawlib` blocks into responsive static HTML sites, GitHub-ready Markdown, and standalone PDF publications.
