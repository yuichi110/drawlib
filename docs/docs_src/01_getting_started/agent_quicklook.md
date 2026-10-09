# AI-Driven Workflow & Agent Setup

Drawlib v0.3 is engineered from the ground up for **autonomous AI coding agents** (such as Claude Code, Cursor, Gemini, and GitHub Copilot).

Instead of requiring human engineers to manually craft technical specifications and draw architecture diagrams, Drawlib makes it possible to delegate the **entire documentation lifecycle** to AI agents.

---

## Why Drawlib is Ideal for AI Agents

When tasked with generating technical illustrations, AI agents typically struggle with raw SVG generation or GUI design tools:
- **Raw SVGs are brittle**: LLMs frequently miscalculate coordinate bounds, leading to clipped text and misaligned arrows.
- **Low-level Matplotlib requires boilerplate**: Matplotlib is designed for statistical plots, not clean software architecture schemas.
- **GUI tools cannot be driven by agents**: AI agents cannot drag and drop shapes in Visio or Figma.

### The Drawlib Advantage for LLMs
1. **High-Level Declarative Abstractions**:  
   Instead of drawing raw boxes and wires, an agent simply writes `ArchitectureDiagram`, `ERDiagram`, or `FlowDiagram`. The library handles orthogonal routing, padding, and marker styling automatically.
2. **Built-in Visual Harmony**:  
   Predefined semantic styles (`Styles.PrimaryFlat`, `Styles.AccentFlat`) ensure that AI-generated diagrams look publication-ready without fine-tuning color codes.
---

## Drawlib & AI Agent Collaboration Model

Drawlib provides a tightly integrated tripartite architecture between the library's on-demand knowledge engine, the autonomous AI coding agent, and version-controlled project documentation:

```drawlib fold-code 650px center file:agent_collaboration_model.png caption:"Drawlib & AI Agent Autonomous Interaction Model"
from drawlib.canvas import setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=142, height=54)

header_ts = Styles.WhiteBold.patch(text_size=9.5)
ts_body = Styles.Dark.patch(text_size=7.5, halign="left")

# 1. Drawlib (CLI & Knowledge Base)
rectangle((22.0, 24.0), width=32.0, height=38.0, style=Styles.PrimaryOutline.patch(shape_r=2.0))
rectangle((22.0, 40.0), width=30.0, height=5.5, style=Styles.PrimaryFlat.patch(shape_r=1.5), text="Drawlib CLI & Engine", text_style=header_ts)

phosphor.book_bookmark(xy=(9.5, 31.0), width=4.5, style=Styles.Primary)
text((13.5, 31.0), text="drawlib rules show\nOn-demand API manuals", style=ts_body)

phosphor.terminal_window(xy=(9.5, 21.5), width=4.5, style=Styles.Primary)
text((13.5, 21.5), text="drawlib show -g\nMillimeter coordinate grid", style=ts_body)

phosphor.gear(xy=(9.5, 12.0), width=4.5, style=Styles.Primary)
text((13.5, 12.0), text="drawlib build\nHTML / PDF / Markdown compiler", style=ts_body)

# 2. AI Agent (Autonomous Partner)
rectangle((71.0, 24.0), width=32.0, height=38.0, style=Styles.AccentOutline.patch(shape_r=2.0))
rectangle((71.0, 40.0), width=30.0, height=5.5, style=Styles.AccentFlat.patch(shape_r=1.5), text="AI Coding Agent", text_style=header_ts)

phosphor.chats(xy=(58.5, 31.0), width=4.5, style=Styles.Accent)
text((62.5, 31.0), text="1. On-Demand Rules Query\nFetch syntax without bloat", style=ts_body)

phosphor.code(xy=(58.5, 21.5), width=4.5, style=Styles.Accent)
text((62.5, 21.5), text="2. Isolated Scratch Prototyping\nDraft in .drawlib/scratch/", style=ts_body)

phosphor.eye(xy=(58.5, 12.0), width=4.5, style=Styles.Accent)
text((62.5, 12.0), text="3. Multimodal Review\nInspect & fix overlaps", style=ts_body)

# 3. Docs / Illustration (Deliverables)
rectangle((120.0, 24.0), width=32.0, height=38.0, style=Styles.SuccessOutline.patch(shape_r=2.0))
rectangle((120.0, 40.0), width=30.0, height=5.5, style=Styles.SuccessFlat.patch(shape_r=1.5), text="Docs & Deliverables", text_style=header_ts)

phosphor.file_text(xy=(107.5, 31.0), width=4.5, style=Styles.Success)
text((111.5, 31.0), text="*.md Specifications\nEmbedded ```drawlib``` blocks", style=ts_body)

phosphor.file_pdf(xy=(107.5, 21.5), width=4.5, style=Styles.Success)
text((111.5, 21.5), text="*.pdf & Web Sites\nPublication-grade assets", style=ts_body)

phosphor.git_branch(xy=(107.5, 12.0), width=4.5, style=Styles.Success)
text((111.5, 12.0), text="Git PR Code Review\nDiffable illustration code", style=ts_body)

# Connections (Drawlib <-> AI -> Docs)
line((39.5, 24.0), (53.5, 24.0), arrow_head="<->", style=Styles.DarkBold)
text((46.5, 28.5), text="Rules Query", style=Styles.DarkBold.patch(text_size=7.5))
text((46.5, 19.5), text="Grid Images", style=Styles.Dark.patch(text_size=7.0))

line((88.5, 24.0), (102.5, 24.0), arrow_head="->", style=Styles.DarkBold)
text((95.5, 28.5), text="Commit Code", style=Styles.DarkBold.patch(text_size=7.5))
text((95.5, 19.5), text="Compiled Output", style=Styles.Dark.patch(text_size=7.0))
save()
```

### Why Agents Don't Hallucinate Drawlib Code
Unlike traditional libraries where agents often hallucinate outdated APIs or struggle with deprecated options, Drawlib eliminates hallucinations through **active command-line guidance**:
1. **On-Demand Rule Injection**: Rather than stuffing thousands of tokens of API documentation into the agent's prompt context, the agent simply queries `drawlib rules show <topic>` when it needs exact signatures.
2. **Deterministic Geometry**: Agents do not have to guess rendering outcomes; they run `drawlib show -g` to render images with absolute millimeter grids and verify their work visually.

To enable your AI agent to author Drawlib illustrations and documentation, configure your environment with Drawlib's core guidelines.

### 1. Configure Workspace Rules
Add the Drawlib agent instructions to your project's rule file:

- **Cursor**: Paste the instructions into `.cursorrules` or `.cursor/rules/drawlib.md`.
- **Claude Code**: Add instructions to your project's `CLAUDE.md`.
- **Gemini / Generic Agents**: Place instructions in `.agents/rules/drawlib.md`.

You can dump the official agent instruction template directly using the CLI:

```bash
# Display the bootstrap agent manual
$ uv run drawlib rules show agent-instruction
```

### 2. Project-First Rule (`drawlib init`)
Teach your agent to **never create bare `.py` files in an uninitialized directory** or build project folders manually. Always scaffold a Drawlib project first so `styles.py` (theme & language fonts), `utils.py`, `_assets/`, and `build.sh` are properly configured:

```bash
# Standalone diagram image(s) only -> images_src/*.py -> images/*.png
$ uv run drawlib init images [-l <lang>] [-s <style>]

# Linear technical document / RFC / PDF -> doc_src/*.md
$ uv run drawlib init doc [target] [-l <lang>] [-s <style>]

# Multi-page documentation website -> docs_src/**/*.md
$ uv run drawlib init site [target] [-l <lang>] [-s <style>]

# 16:9 presentation slide deck -> slide_src/*.md
$ uv run drawlib init slide [target] [-l <lang>] [-s <style>]
```

### 3. Essential Commands & On-Demand Rules Catalog
Ensure your agent knows how to query on-demand rule topics and preview drawings with a coordinate grid:

| Purpose | Command |
| :--- | :--- |
| **List Available Rule Topics** | `uv run drawlib rules list` |
| **Canvas & Lifecycle Overview** | `uv run drawlib rules show overview` |
| **Style Guide & 50%+ Neutral Rule** | `uv run drawlib rules show style-guide` |
| **Animation Loop & Idioms** | `uv run drawlib rules show anim-guide` |
| **16:9 Slide Authoring & Layouts** | `uv run drawlib rules show slide-guide` |
| **Project Scaffolding & Structure** | `uv run drawlib rules show project` |
| **CLI Reference (`build`, `show`, `cache`)** | `uv run drawlib rules show cli` |
| **Unified API Cheat Sheet** | `uv run drawlib rules show api` |
| **Auto-Layout Graphs (`drawlib.graph`)** | `uv run drawlib rules show lib-graph` |
| **Domain Diagrams (`drawlib.diagrams`)** | `uv run drawlib rules show lib-diagrams` |
| **SmartArts & GeoMap (`drawlib.smartarts`)** | `uv run drawlib rules show lib-smartarts` |
| **Quantitative Charts (`drawlib.charts`)** | `uv run drawlib rules show lib-charts` |
| **Render Named Markdown Block Preview** | `uv run drawlib show <md_path> <diagram.png> -g -o .drawlib/scratch/preview.png` |
| **Render Standalone Script Preview** | `uv run drawlib show <script.py> -g -o .drawlib/scratch/preview.png` |
| **Build Full Project** | `./<target>_src/build.sh` or `uv run drawlib build html docs_src/ -o docs_html/` |

---

## The Autonomous Verification Loop

Teach your agent to follow Drawlib's autonomous self-correction loop when creating diagrams:

```drawlib fold-code 700px center file:ai_feedback_loop.png caption:"Autonomous AI Visual Self-Correction Loop"
from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=144, height=50)

# Agent loop boxes: Hero focal node in PrimaryFlat, supporting nodes in calm Neutral cards
rectangle((22, 20), width=26, height=20, style=Styles.PrimaryFlat, text="1. LLM Agent\n(Reads Code)", text_style=Styles.WhiteBold)
rectangle((56, 20), width=26, height=20, style=Styles.Neutral, text="2. Generate\nDrawlib Code")
rectangle((90, 20), width=26, height=20, style=Styles.Neutral, text="3. Render Grid\n(-g Image)")
rectangle((122, 20), width=24, height=20, style=Styles.SecondaryNeutral, text="4. Auto\nReview")

# Forward arrows
line((35, 20), (43, 20), arrow_head="->", style=Styles.DarkBold)
line((69, 20), (77, 20), arrow_head="->", style=Styles.DarkBold)
line((103, 20), (110, 20), arrow_head="->", style=Styles.DarkBold)

# Feedback loop
line((122, 30), (122, 38), style=Styles.DarkDashed)
line((122, 38), (56, 38), style=Styles.DarkDashed)
line((56, 38), (56, 30), arrow_head="->", style=Styles.DarkDashed)
text((89, 42.5), "Self-Correct Coordinates & Re-render", style=Styles.DarkBold.patch(text_size=9.5))
save()
```

1. **Inspect Context**: The agent inspects actual repository files (models, API routers, database schemas) to understand the architecture.
2. **Draft Illustration**: The agent scaffolds a project via `drawlib init` (if not already present) and authors the drawing code in `images_src/<name>.py` or an embedded ````drawlib```` Markdown block with `file:<diagram.png>`.
3. **Render Image with Grid (`-g`)**:  
   `uv run drawlib show <md_path> <diagram.png> -g -o .drawlib/scratch/preview.png` (or `uv run drawlib show images_src/<name>.py -g -o .drawlib/scratch/preview.png`).
4. **Multimodal Self-Review**: The agent inspects the rendered PNG with its vision/file viewing tool, checking for:
   - Label overflow or text clipping outside boxes.
   - Overlapping arrow lines or awkward elbow routings.
   - Missing perimeter margins around canvas borders.
5. **Auto-Adjust & Finalize**: The agent adjusts coordinates, re-renders until clean, and builds the final project outputs.

---

> [!TIP]
> For complete system prompts, rule topic catalogues, and advanced automated CI/CD integration, proceed to **[Chapter 9: AI Agents & Advanced Integration](../09_ai_agents_and_advanced/ai_agent_instructions.md)**.
