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
3. **On-Demand Rule Injection**:  
   Drawlib includes a complete built-in manual that agents can query via the CLI at runtime (`drawlib rules show <topic>`), eliminating context-window bloat and outdated training data.

---

## Equipping Your AI Agent

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

```drawlib 700px center caption:"Autonomous AI Visual Self-Correction Loop"
from drawlib.canvas import setup
from drawlib.shapes import rectangle
from drawlib.lines import line
from drawlib.styles import Styles

setup(width=130, height=45)

# Agent loop boxes
rectangle((20, 22.5), width=26, height=20, style=Styles.PrimaryFlat, text="1. LLM Agent\n(Reads Code)", text_style=Styles.WhiteBold)
rectangle((56, 22.5), width=28, height=20, style=Styles.AccentFlat, text="2. Generate\nDrawlib Code", text_style=Styles.WhiteBold)
rectangle((92, 22.5), width=26, height=20, style=Styles.SecondaryFlat, text="3. Render Grid\n(-g Image)", text_style=Styles.WhiteBold)
rectangle((118, 22.5), width=18, height=20, style=Styles.SuccessFlat, text="4. Auto\nReview", text_style=Styles.WhiteBold)

# Forward arrows
line((33, 22.5), (42, 22.5), arrowhead="->", style=Styles.PrimaryBold)
line((70, 22.5), (79, 22.5), arrowhead="->", style=Styles.PrimaryBold)
line((105, 22.5), (109, 22.5), arrowhead="->", style=Styles.PrimaryBold)

# Feedback loop
line((118, 32.5), (118, 38), style=Styles.DangerBold)
line((118, 38), (56, 38), style=Styles.DangerBold)
line((56, 38), (56, 32.5), arrowhead="->", style=Styles.DangerBold)
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
