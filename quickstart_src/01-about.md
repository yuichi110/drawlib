# 1. About Drawlib

Drawlib is a pure-Python library designed to establish **"Illustration as Code"** and **"Documentation as Code"** as first-class engineering disciplines. Instead of relying on manual drag-and-drop vector drawing tools that produce opaque binary assets, Drawlib generates crisp, version-controlled diagrams and technical specifications directly from readable Python code.

## The Problem with Traditional Diagramming

Modern software teams manage code, infrastructure, and CI/CD pipelines as version-controlled text. Yet technical illustrations are frequently created in GUI tools (draw.io, Figma, PowerPoint, Visio) or complex DSLs:

1. **Binary or Opaque File Formats**: XML/JSON blobs produced by GUI tools cannot be meaningfully reviewed in Pull Requests (`git diff`).
2. **Drift and Staleness**: As services, schemas, and endpoints evolve, manual diagram updates are neglected, causing architecture documentation to fall out of sync.
3. **Inconsistent Styling**: Without centralized design tokens, each team member uses different fonts, margins, line weights, and arbitrary colors.
4. **Low-Level Plotting Boilerplate**: Tools like matplotlib or raw SVG libraries require hundreds of lines of low-level trigonometry and coordinate math for simple rounded boxes and curved arrows.

## Drawlib's Three Architectural Pillars

```drawlib 620px center file:about_pillars.png caption:"Figure 1.1: Drawlib Core Architectural Pillars"
from drawlib.canvas import setup
from drawlib.icons import phosphor
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=120, height=44)

pillars = [
    (20, phosphor.code, "Illustration as Code", "Declarative Python API\nVersion-Controlled\nPR & Diff Friendly", Styles.PrimaryFlat),
    (60, phosphor.palette, "Design Token Themes", "Google & Default Themes\nSemantic 6-Color Roles\n10 Systematic Variants", Styles.SecondaryFlat),
    (100, phosphor.book_open, "Documentation as Code", "Embedded in Markdown\nMulti-Target Compilers\nHTML, PDF, WebP, PNG", Styles.AccentFlat),
]

for x, icon_fn, title, bullets, style in pillars:
    rectangle(xy=(x, 22), width=34, height=36, r=3, style=Styles.MutedDashed)
    icon_fn(xy=(x, 34), width=7, style=style)
    text(xy=(x, 26), text=title, style=Styles.PrimaryBold.patch(text_size=10))
    text(xy=(x, 14), text=bullets, style=Styles.Primary.patch(text_size=7.5))
```

1. **High-Level Declarative Components**: Rather than assembling raw polygons by hand, Drawlib provides pre-engineered modules for cloud architectures (`ArchitectureDiagram`), pipelines (`ChevronProcess`), sequence flows (`SequenceDiagram`), tables (`Table`), and charts (`BarChart`).
2. **Centralized Style Tokens**: Themes (`DefaultStyles`, `GoogleStyles`, `MonochromeStyles`) decouple geometry from presentation. Updating a theme propagates across an entire multi-document project instantly.
3. **Unified Document Compiler**: Drawlib embeds directly into Markdown files using ````drawlib```` blocks, building searchable static HTML sites, GitHub-flavored Markdown, and printable PDF books from a single source of truth.
