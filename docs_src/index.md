# Welcome to the Drawlib Documentation!

Drawlib is a pure-Python drawing library and documentation compiler crafted to facilitate **"Illustration as Code"** and **"Documentation as Code"**.

```drawlib fold-code 600px center caption:"Code makes Illustration"
from drawlib.canvas import setup
from drawlib.shapes import circle, rectangle
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=100, height=40)

circle(
    xy=(25, 20),
    radius=12,
    style=Styles.Primary,
    text="Circle",
    textsize=16,
)

rectangle(
    xy=(75, 20),
    width=24,
    height=24,
    style=Styles.Secondary,
    text="Rectangle",
    textsize=16,
)
```

---

## Key Capabilities

### 1. Build Entire Documentation End-to-End

Drawlib is more than an illustration library—it is an **integrated documentation compiler**.

You can author full technical documentation in standard Markdown containing embedded `drawlib` code blocks. Without configuring external documentation generators (such as Sphinx, MkDocs, or Docusaurus), a single command (`drawlib build`) compiles everything into publication-ready outputs:

- **Responsive Static HTML (`docs_html/`)**: Full-featured documentation site with instant search, dark/light themes, and navigation sidebar.
- **GitHub-Optimized Markdown (`docs/`)**: Clean Markdown with syntax-highlighted code blocks followed by relative diagram images for browsing on GitHub.
- **Headless Vector PDF (`docs_pdf/`)**: High-fidelity, print-ready PDF generated via headless Chromium.

Because the entire documentation workflow is unified in Python and Markdown, human developers and AI coding agents can build, generate, and maintain complete documentation sites end-to-end.

```drawlib fold-code 700px center caption:"End-to-End Documentation System with Drawlib"
from drawlib.canvas import setup
from drawlib.fonts import FontRoboto
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=140, height=65)

# Styles
s_src = Styles.PrimaryFlat
s_engine = Styles.AccentFlat
s_out = Styles.SecondaryFlat

ts_title = Styles.WhiteBold.patch(text_size=10.5, text_font=FontRoboto.ROBOTO_BOLD)
ts_desc = Styles.WhiteLight.patch(text_size=8, text_font=FontRoboto.ROBOTO_REGULAR)
ts_engine_title = Styles.WhiteBold.patch(text_size=12, text_font=FontRoboto.ROBOTO_BOLD)
ts_engine_desc = Styles.WhiteLight.patch(text_size=8, text_font=FontRoboto.ROBOTO_REGULAR)

# Section Headers
text((25, 60), "Source Authoring", style=Styles.PrimaryBold.patch(text_size=11, text_font=FontRoboto.ROBOTO_BOLD))
text((70, 60), "Drawlib Compiler", style=Styles.AccentBold.patch(text_size=11, text_font=FontRoboto.ROBOTO_BOLD))
text((116, 60), "Publication Targets", style=Styles.SecondaryBold.patch(text_size=11, text_font=FontRoboto.ROBOTO_BOLD))

# 1. Source (Left)
rectangle((25, 33), width=36, height=44, style=s_src, r=2.5)
text((25, 51.5), "Documentation Source", style=ts_title)
text((25, 46.5), "Human or AI writes Markdown (.md)", style=Styles.White.patch(text_size=8, text_font=FontRoboto.ROBOTO_REGULAR))

# Mini editor window inside Source box
rectangle((25, 29), width=31, height=23, style=Styles.MutedSolid, r=1.5)
# Window dots
circle((13, 37.8), radius=0.7, style=Styles.Red)
circle((15.2, 37.8), radius=0.7, style=Styles.Yellow)
circle((17.4, 37.8), radius=0.7, style=Styles.Green)
text((26, 37.8), "system_guide.md", style=Styles.WhiteLight.patch(text_size=7, text_font=FontRoboto.ROBOTO_REGULAR))
line((10.5, 36.2), (39.5, 36.2), style=Styles.Muted)
# Editor text
text((12.5, 27.5), "# System Guide\nArchitecture overview...\n\n```drawlib\nrectangle(...)\n```", style=Styles.White.patch(text_size=6.8, text_font=FontRoboto.ROBOTO_REGULAR, text_halign="left"))

text((25, 13.5), "Text + Embedded Illustration Code", style=Styles.WhiteBold.patch(text_size=7.5, text_font=FontRoboto.ROBOTO_BOLD))

# 2. Engine (Center)
rectangle((70, 33), width=34, height=44, style=s_engine, r=2.5)
text((70, 50), "drawlib build", style=ts_engine_title)
text((70, 43.5), "All-in-One Compiler", style=Styles.WhiteBold.patch(text_size=9.5, text_font=FontRoboto.ROBOTO_BOLD))
text((57, 30), "• Parses Markdown AST\n• Executes Python blocks\n• Auto-generates images\n• Resolves internal links", style=Styles.WhiteLight.patch(text_size=8, text_font=FontRoboto.ROBOTO_REGULAR, text_halign="left"))
text((70, 16), "No External Tools Needed\n(Zero Sphinx / MkDocs)", style=Styles.WhiteBold.patch(text_size=8, text_font=FontRoboto.ROBOTO_BOLD))

# Arrow Left -> Center
line((43, 33), (53, 33), arrowhead="->", style=Styles.Bold)

# 3. Targets (Right)
rectangle((116, 49), width=36, height=13, style=s_out, r=1.5)
text((116, 52), "Responsive HTML Site", style=ts_title)
text((116, 46.5), "docs_html/ (Search, Dark Mode, Nav)", style=ts_desc)

rectangle((116, 33), width=36, height=13, style=s_out, r=1.5)
text((116, 36), "GitHub Markdown", style=ts_title)
text((116, 30.5), "docs/ (Syntax code + relative images)", style=ts_desc)

rectangle((116, 17), width=36, height=13, style=s_out, r=1.5)
text((116, 20), "Headless Vector PDF", style=ts_title)
text((116, 14.5), "docs_pdf/ (Chromium vector print)", style=ts_desc)

# Arrows Center -> Right targets
line((87, 45), (98, 49), arrowhead="->", style=Styles.Bold)
line((87, 33), (98, 33), arrowhead="->", style=Styles.Bold)
line((87, 21), (98, 17), arrowhead="->", style=Styles.Bold)
```

---

### 2. AI Agents Generate Grounded Docs & Diagrams from Codebase

Because Drawlib diagrams are written in clean, standard Python code, modern AI coding agents (such as Claude Code, Cursor, GitHub Copilot, and ChatGPT) can generate, inspect, and maintain technical illustrations naturally.

By placing Drawlib directly in your application or documentation repository:

- **AI Inspects Real Context**: Agents inspect actual database schemas (`models.py`), API endpoints, services, and configuration files before drawing a single box.
- **Grounded, High-Fidelity Diagrams**: The AI generates architecture diagrams, sequence diagrams, ER diagrams, and workflow charts that accurately reflect real code rather than imaginary mockups.
- **Single Pull Request Synchrony**: When you modify application logic, the AI agent updates the implementation code, Markdown documentation, and embedded Drawlib diagrams simultaneously in the same Pull Request.

```drawlib fold-code 700px center caption:"AI Coding Agents Generating Grounded Docs & Diagrams from Repository"
from drawlib.canvas import setup
from drawlib.fonts import FontRoboto
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=140, height=65)

# Styles
s_repo = Styles.PrimaryFlat
s_agent = Styles.AccentFlat
s_doc = Styles.SecondaryFlat

ts_title = Styles.WhiteBold.patch(text_size=10.5, text_font=FontRoboto.ROBOTO_BOLD)
ts_desc = Styles.WhiteLight.patch(text_size=8, text_font=FontRoboto.ROBOTO_REGULAR)

# Column Headers
text((24, 60), "1. Repository Context", style=Styles.PrimaryBold.patch(text_size=11, text_font=FontRoboto.ROBOTO_BOLD))
text((69, 60), "2. Autonomous AI Agent", style=Styles.AccentBold.patch(text_size=11, text_font=FontRoboto.ROBOTO_BOLD))
text((116, 60), "3. Grounded Docs & Diagrams", style=Styles.SecondaryBold.patch(text_size=11, text_font=FontRoboto.ROBOTO_BOLD))

# 1. Left: Repository Context items
rectangle((24, 48), width=34, height=13, style=s_repo, r=1.5)
text((24, 50.5), "Source Code & APIs", style=ts_title)
text((24, 45.5), "routes.py, controllers, logic", style=ts_desc)

rectangle((24, 33), width=34, height=13, style=s_repo, r=1.5)
text((24, 35.5), "Database & Schemas", style=ts_title)
text((24, 30.5), "models.py, migrations, OpenAPI", style=ts_desc)

rectangle((24, 18), width=34, height=13, style=s_repo, r=1.5)
text((24, 20.5), "Infra & Config", style=ts_title)
text((24, 15.5), "docker-compose, k8s, env", style=ts_desc)

# Arrows from Repo to Agent
line((41, 48), (53, 39), arrowhead="->", style=Styles.Bold)
line((41, 33), (53, 33), arrowhead="->", style=Styles.Bold)
line((41, 18), (53, 27), arrowhead="->", style=Styles.Bold)

# 2. Center: AI Agent
rectangle((69, 33), width=32, height=44, style=s_agent, r=2.5)
circle((69, 45), radius=4.5, style=Styles.White)
text((69, 45), "AI", style=Styles.AccentBold.patch(text_size=10, text_font=FontRoboto.ROBOTO_BOLD))
text((69, 37), "Coding Agent", style=Styles.WhiteBold.patch(text_size=11.5, text_font=FontRoboto.ROBOTO_BOLD))
text((69, 31.5), "Claude Code / Cursor / Copilot", style=Styles.WhiteLight.patch(text_size=7.5, text_font=FontRoboto.ROBOTO_REGULAR))
text((55, 21), "• Explores codebase & schemas\n• Synthesizes Drawlib code\n• Validates image output (-g)\n• Refines layout autonomously", style=Styles.WhiteLight.patch(text_size=7.2, text_font=FontRoboto.ROBOTO_REGULAR, text_halign="left"))

# Arrow Agent to Output
line((85, 33), (98, 33), arrowhead="->", style=Styles.Bold)

# 3. Right: Delivered Docs & Diagrams
rectangle((116, 33), width=36, height=44, style=s_doc, r=2.5)
text((116, 51.5), "Grounded Documentation", style=ts_title)
text((116, 46.5), "100% In-Sync with Real Code", style=Styles.WhiteBold.patch(text_size=8, text_font=FontRoboto.ROBOTO_BOLD))

# Mini visual card inside doc box
rectangle((116, 29), width=31, height=23, style=Styles.White, r=1.5)
text((116, 37.5), "System Architecture & Specs", style=Styles.SecondaryBold.patch(text_size=8, text_font=FontRoboto.ROBOTO_BOLD))

# 3 Mini mockup nodes inside card: App -> API -> DB
rectangle((105, 29), width=7.5, height=6.5, style=Styles.PrimaryFlat, r=1)
text((105, 29), "App", style=Styles.WhiteBold.patch(text_size=6, text_font=FontRoboto.ROBOTO_BOLD))

line((108.75, 29), (112.25, 29), arrowhead="->", style=Styles.Muted.patch(line_width=1.2))

rectangle((116, 29), width=7.5, height=6.5, style=Styles.AccentFlat, r=1)
text((116, 29), "API", style=Styles.WhiteBold.patch(text_size=6, text_font=FontRoboto.ROBOTO_BOLD))

line((119.75, 29), (123.25, 29), arrowhead="->", style=Styles.Muted.patch(line_width=1.2))

rectangle((127, 29), width=7.5, height=6.5, style=Styles.SecondaryFlat, r=1)
text((127, 29), "DB", style=Styles.WhiteBold.patch(text_size=6, text_font=FontRoboto.ROBOTO_BOLD))

text((116, 20.5), "ER Diagrams • Sequences • APIs", style=Styles.Muted.patch(text_size=7, text_font=FontRoboto.ROBOTO_REGULAR))

text((116, 13.5), "Updated in Same Pull Request", style=Styles.WhiteBold.patch(text_size=7.5, text_font=FontRoboto.ROBOTO_BOLD))
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
9. **[Advanced Topics](./advanced_topics/ai_agents.md)**: AI coding agents, geometry math, dynamic rendering (`get_dimage_from_code`), and debugging.

---

<p align="center"><em>© 2026 drawlib by Yuichi Ito. Released under the Apache 2.0 License.</em></p>
