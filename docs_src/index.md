# Welcome to the Drawlib Documentation!

Drawlib is a pure-Python drawing library and documentation compiler crafted to facilitate **"Illustration as Code"** and **"Documentation as Code"**.

```drawlib fold-code 600px center caption:"Code makes Illustration"
from drawlib.canvas import config
from drawlib.colors import Colors, Colors140
from drawlib.shapes import circle, rectangle
from drawlib.text import text
from drawlib.types import Style

config(width=100, height=40)

circle(xy=(25, 20), radius=12, style=Style(fill_color=Colors140.Turquoise, line_color=Colors.Navy, line_width=2))
text(xy=(25, 20), text="Circle", style=Style(text_color=Colors.White, text_size=16))

rectangle(xy=(75, 20), width=24, height=24, style=Style(fill_color=Colors140.Coral, line_color=Colors.Navy, line_width=2))
text(xy=(75, 20), text="Rectangle", style=Style(text_color=Colors.White, text_size=16))
```

---

## Getting Started

- **[About Drawlib](./introductions/about.md)**: Philosophy, motivation, and "Illustration as Code".
- **[Installation Guide](./introductions/install.md)**: Installation instructions for Python 3.11+.
- **[Quick Start Guide](./introductions/quick_start.md)**: Create your first illustration in 2 minutes.

---

## Documentation Sections

Explore the comprehensive guides organized in the sidebar:

1. **[Introductions](./introductions/about.md)**: Getting started, philosophy, links, and release notes.
2. **[Document Builder](./doc_builder/index.md)**: Built-in compiler for responsive HTML sites, GitHub Markdown, and Chromium PDF.
3. **[CLI Reference](./cli/index.md)**: Command line interface (`build`, `serve`, `init`, `show`, `export`, `cache`).
4. **[Foundations](./foundations/canvas.md)**: Canvas, Cartesian coordinates, 21 shapes, lines, text, icons, and images.
5. **[Styles & Theming](./styles/index.md)**: Color systems, typography fonts, official themes (`default`, `essentials`, `monochrome`), and custom presets.
6. **[SmartArts Diagrams](./smartarts/index.md)**: High-level cards, tables, trees, mind maps, chevrons, and code blocks.
7. **[Technical Diagrams](./diagrams/architecture.md)**: Architecture, sequence, flow, UML class, ER, and state diagrams.
8. **[Charts](./charts/index.md)**: Pure-Python vector charts (Bar, Line, Area, Pie, Radar, Scatter, Gantt).
9. **[Advanced Topics](./advanced_topics/math.md)**: Geometry math, dynamic code rendering (`get_dimage_from_code`), debugging, and library settings.

---

<p align="center"><em>© 2026 drawlib by Yuichi Ito. Released under the Apache 2.0 License.</em></p>
