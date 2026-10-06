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

```drawlib 650px center file:agent_collaboration_model.png caption:"Drawlib & AI Agent Autonomous Interaction Model"
from drawlib.canvas import setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=142, height=54)

header_ts = Styles.WhiteBold.patch(text_size=9.5)
ts_body = Styles.Dark.patch(text_size=7.5, text_halign="left")

# 1. Drawlib (CLI & Knowledge Base)
rectangle((22.0, 24.0), width=32.0, height=38.0, r=2.0, style=Styles.PrimaryOutline)
rectangle((22.0, 40.0), width=30.0, height=5.5, r=1.5, style=Styles.PrimaryFlat, text="Drawlib CLI & Engine", text_style=header_ts)

phosphor.book_bookmark(xy=(9.5, 31.0), width=4.5, style=Styles.Primary)
text((13.5, 31.0), text="drawlib rules show\nOn-demand API manuals", style=ts_body)

phosphor.terminal_window(xy=(9.5, 21.5), width=4.5, style=Styles.Primary)
text((13.5, 21.5), text="drawlib show -g\nMillimeter coordinate grid", style=ts_body)

phosphor.gear(xy=(9.5, 12.0), width=4.5, style=Styles.Primary)
text((13.5, 12.0), text="drawlib build\nHTML / PDF / Markdown compiler", style=ts_body)

# 2. AI Agent (Autonomous Partner)
rectangle((71.0, 24.0), width=32.0, height=38.0, r=2.0, style=Styles.AccentOutline)
rectangle((71.0, 40.0), width=30.0, height=5.5, r=1.5, style=Styles.AccentFlat, text="AI Coding Agent", text_style=header_ts)

phosphor.chats(xy=(58.5, 31.0), width=4.5, style=Styles.Accent)
text((62.5, 31.0), text="1. On-Demand Rules Query\nFetch syntax without bloat", style=ts_body)

phosphor.code(xy=(58.5, 21.5), width=4.5, style=Styles.Accent)
text((62.5, 21.5), text="2. Isolated Scratch Prototyping\nDraft in .drawlib/scratch/", style=ts_body)

phosphor.eye(xy=(58.5, 12.0), width=4.5, style=Styles.Accent)
text((62.5, 12.0), text="3. Multimodal Review\nInspect & fix overlaps", style=ts_body)

# 3. Docs / Illustration (Deliverables)
rectangle((120.0, 24.0), width=32.0, height=38.0, r=2.0, style=Styles.SuccessOutline)
rectangle((120.0, 40.0), width=30.0, height=5.5, r=1.5, style=Styles.SuccessFlat, text="Docs & Deliverables", text_style=header_ts)

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

### 2. Essential Commands to Teach Your Agent
Ensure your agent knows how to query rules and preview drawings:

| Purpose | Command |
|---|---|
| **Query Module Syntax** | `uv run drawlib rules show <topic>` (e.g. `lib-diagrams`, `lib-smartarts`) |
| **List Available Rules** | `uv run drawlib rules list` |
| **Render Grid Preview** | `uv run drawlib show <path> -g -o .drawlib/scratch/test.png` |
| **Build Full Docs** | `./build.sh` or `uv run drawlib build html docs_src/ -o docs_html/` |

---

## The Autonomous Verification Loop

Teach your agent to follow Drawlib's autonomous self-correction loop when creating diagrams:

```drawlib 700px center file:ai_feedback_loop.png caption:"Autonomous AI Visual Self-Correction Loop"
from drawlib.canvas import setup
from drawlib.shapes import rectangle
from drawlib.lines import line
from drawlib.styles import Styles

setup(width=130, height=45)

# Agent loop boxes: Hero focal node in PrimaryFlat, supporting nodes in calm Neutral cards
rectangle((20, 22.5), width=26, height=20, style=Styles.PrimaryFlat, text="1. LLM Agent\n(Reads Code)", text_style=Styles.WhiteBold)
rectangle((56, 22.5), width=28, height=20, style=Styles.Neutral, text="2. Generate\nDrawlib Code")
rectangle((92, 22.5), width=26, height=20, style=Styles.Neutral, text="3. Render Grid\n(-g Image)")
rectangle((118, 22.5), width=18, height=20, style=Styles.SecondaryNeutral, text="4. Auto\nReview")

# Forward arrows
line((33, 22.5), (42, 22.5), arrow_head="->", style=Styles.DarkBold)
line((70, 22.5), (79, 22.5), arrow_head="->", style=Styles.DarkBold)
line((105, 22.5), (109, 22.5), arrow_head="->", style=Styles.DarkBold)

# Feedback loop
line((118, 32.5), (118, 38), style=Styles.DarkDashed)
line((118, 38), (56, 38), style=Styles.DarkDashed)
line((56, 38), (56, 32.5), arrow_head="->", style=Styles.DarkDashed)
```

1. **Inspect Context**: The agent inspects actual repository files (models, API routers, database schemas) to understand the architecture.
2. **Draft Illustration**: The agent writes drawing prototype code in an isolated scratch script (`.drawlib/scratch/test.py`) or embedded Markdown block. Do not pollute the root directory; ensure `.drawlib/` is in `.gitignore`.
3. **Render Image with Grid (`-g`)**:  
   `uv run drawlib show .drawlib/scratch/test.py -g -o .drawlib/scratch/test.png`
4. **Multimodal Self-Review**: The agent inspects the rendered PNG with its vision/file viewing tool, checking for:
   - Label overflow or text clipping outside boxes.
   - Overlapping arrow lines or awkward elbow routings.
   - Missing perimeter margins around canvas borders.
5. **Auto-Adjust & Finalize**: The agent adjusts coordinates and integrates the verified code directly into the documentation.

---

> [!TIP]
> For complete system prompts, rule topic catalogues, and advanced automated CI/CD integration, proceed to **[Chapter 7: AI Agents & Advanced Integration](../07_ai_agents_and_advanced/ai_agent_instructions.md)**.
