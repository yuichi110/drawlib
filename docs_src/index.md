# Welcome to the Drawlib Documentation!

Drawlib is a pure Python drawing library crafted to facilitate **Illustration as Code** rather than focusing solely on creating polished illustrations manually.

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

- **[About Drawlib](./introductions/about.md)**: Introduction to Drawlib concepts, motivation, and philosophy.
- **[Installation Guide](./introductions/install.md)**: How to install Drawlib in your Python environment.
- **[Quick Start Guide](./introductions/quick_start.md)**: Create your first drawing in minutes.

---

## Documentation Sections

Explore the comprehensive guides organized in the sidebar:

1. **[Introductions](./introductions/about.md)**: Getting started, philosophy, links, and release notes.
2. **[Foundations](./foundations/canvas.md)**: Canvas, coordinate system, shapes, lines, text, icons, and images.
3. **[SmartArts Diagrams](./smartarts/index.md)**: High-level pre-built components (SourceCode, Tables, Trees, Lists, etc.).
4. **[Diagrams](./diagrams/architecture.md)**: Architecture, Class, ER, Flow, Sequence, and State diagrams.
5. **[Charts](./charts/index.md)**: Bar, Line, Area, Pie, Radar, Scatter, and Gantt charts.
6. **[Preset Styles](./preset_styles/official_default.md)**: Out-of-the-box themes and creating custom styles.
7. **[Advanced Topics](./advanced_topics/color.md)**: Fonts, colors, image processing, CLI, and debugging.

---

<p align="center"><em>© 2026 drawlib by Yuichi Ito. Released under the Apache 2.0 License.</em></p>

