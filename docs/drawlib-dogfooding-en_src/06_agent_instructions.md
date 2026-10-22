# Chapter 6: AI Agent Integration and Prompting

Drawlib is engineered from the ground up to be "Agent-First", enabling AI coding assistants (Claude, Cursor, Gemini, Copilot) to generate accurate, publication-ready diagrams autonomously. Once basic instructions are registered, the AI interacts with the Drawlib CLI to inspect rules, test drawings, and output verified code.

```drawlib align=center file=fig_agent_interaction.png caption="Figure 6.1: Autonomous Interaction Model between Drawlib and AI Agents"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=136, height=54)

header_ts = Styles.WhiteBold.patch(text_size=10.5)
ts_body = Styles.Dark.patch(text_size=10.0, halign="left")
ts_arrow_top = Styles.DarkBold.patch(text_size=10.0)
ts_arrow_sub = Styles.Dark.patch(text_size=9.5)

# 1. Drawlib (CLI & Knowledge Base)
rectangle((21.5, 27.0), width=35.0, height=44.0, style=Styles.PrimaryNeutral.patch(shape_r=2.0))
rectangle((21.5, 45.0), width=33.0, height=6.0, style=Styles.PrimaryFlat.patch(shape_r=1.5), text="1. Drawlib CLI", text_style=header_ts)

phosphor.book_bookmark(xy=(7.8, 35.0), width=4.4, style=Styles.Primary)
text((10.8, 35.0), text="drawlib rules\nAPI specs & guides", style=ts_body)

phosphor.terminal_window(xy=(7.8, 23.5), width=4.4, style=Styles.Primary)
text((10.8, 23.5), text="drawlib show -g\nGrid QA preview", style=ts_body)

phosphor.gear(xy=(7.8, 12.0), width=4.4, style=Styles.Primary)
text((10.8, 12.0), text="drawlib build\nPDF & HTML compiler", style=ts_body)

# 2. AI Agent (Cursor / Claude / Gemini)
rectangle((68.0, 27.0), width=35.0, height=44.0, style=Styles.Neutral.patch(shape_r=2.0))
rectangle((68.0, 45.0), width=33.0, height=6.0, style=Styles.AccentFlat.patch(shape_r=1.5), text="2. AI Agent", text_style=header_ts)

phosphor.chats(xy=(54.3, 35.0), width=4.4, style=Styles.Accent)
text((57.3, 35.0), text="1. Anchor & Font QA\nCheck coords & size", style=ts_body)

phosphor.code(xy=(54.3, 23.5), width=4.4, style=Styles.Accent)
text((57.3, 23.5), text="2. Grid Prototype\nTest in scratch/", style=ts_body)

phosphor.eye(xy=(54.3, 12.0), width=4.4, style=Styles.Accent)
text((57.3, 12.0), text="3. Visual Review\nFix overlap & margins", style=ts_body)

# 3. Docs / Illustration (Deliverables)
rectangle((114.5, 27.0), width=35.0, height=44.0, style=Styles.SecondaryNeutral.patch(shape_r=2.0))
rectangle((114.5, 45.0), width=33.0, height=6.0, style=Styles.DarkFlat.patch(shape_r=1.5), text="3. Verified Docs", text_style=header_ts)

phosphor.file_text(xy=(100.8, 35.0), width=4.4, style=Styles.Dark)
text((103.8, 35.0), text="*.md Tech Specs\nCode & diagrams", style=ts_body)

phosphor.file_pdf(xy=(100.8, 23.5), width=4.4, style=Styles.Dark)
text((103.8, 23.5), text="PDF / Web / Slide\nPolished artifacts", style=ts_body)

phosphor.git_branch(xy=(100.8, 12.0), width=4.4, style=Styles.Dark)
text((103.8, 12.0), text="Git Diff Tracking\nReview via PR diffs", style=ts_body)

# Connectors
line((39.5, 27.0), (50.0, 27.0), arrow_head="<->", style=Styles.DarkBold)
text((44.75, 31.5), text="Query", style=ts_arrow_top)
text((44.75, 22.0), text="Grid QA", style=ts_arrow_sub)

line((86.0, 27.0), (96.5, 27.0), arrow_head="->", style=Styles.DarkBold)
text((91.25, 31.5), text="Output", style=ts_arrow_top)
text((91.25, 22.0), text="Auto-Sync", style=ts_arrow_sub)

save()
```

## 6.1 Using the Built-In Rule System (`drawlib rules`)

Drawlib embeds comprehensive API specifications and best practices directly in its CLI. Agents can consult rules on demand:

```bash
# List all available rule manuals
uv run drawlib rules list

# Read core agent workflow instructions
uv run drawlib rules show agent-instruction

# Check canvas coordinate system (bottom-left origin) and lifecycle rules
uv run drawlib rules show overview

# Check color tokens, typography, and the 50%+ neutral baseline rule
uv run drawlib rules show style-guide

# Check the 3-stage multimodal review loop and 720pt font sizing math
uv run drawlib rules show review-guide

# Check project archetype guides (doc / site / slide / images)
uv run drawlib rules show project-overview
uv run drawlib rules show project-doc
uv run drawlib rules show project-site
uv run drawlib rules show project-slide
uv run drawlib rules show project-images

# Check complete API index and specific domain module specifications
uv run drawlib rules show api
uv run drawlib rules show lib-smartarts
uv run drawlib rules show lib-diagrams
uv run drawlib rules show lib-graph
uv run drawlib rules show lib-charts
```

## 6.2 Setting Project Rule Files

Register these essential rules in `.cursorrules` or `.agents/rules/` so agents follow Drawlib `v0.3.0` principles automatically:

```markdown
# Drawlib Drawing Rules
- Project-First Rule: Never create bare `.py` files in an uninitialized folder; always scaffold a project first via `uv run drawlib init <doc|site|slide|images>`.
- Do NOT generate raw SVG or low-level matplotlib code; always use high-level modules (smartarts, diagrams, graph, charts).
- The canvas origin (0, 0) is at the bottom-left corner.
- Design tokens must be imported and referenced in PascalCase: `Styles` and `Colors`.
- 50%+ Neutral Baseline: Ground at least 50% of shapes in calm neutral cards (`Styles.Neutral`, `Styles.PrimaryNeutral`, `Styles.SecondaryNeutral`), reserving saturated fills (`Styles.PrimaryFlat`, `Styles.AccentFlat`) strictly for 1–2 primary focal points or headers.
- Maintain `text_size >= 10.0` (standard 10.0–11.5, headers 11.5–12.5).
- Embedded code blocks must specify `file=<name>.png` and `caption="..."` (plus optional `code=fold` / `code=show`) using `=` syntax, without narrow pixel width caps (`width=600px`).
```

## 6.3 The Autonomous 3-Stage Review Loop

Instruct your AI agent to execute this **Autonomous 3-Stage Review Loop** when creating illustrations and documentation:

1. **Stage 1 — Static & Coordinate Anchor Check**:
   - Verify coordinate anchors: primitives (`shapes`, `text`, `icons`) use **Center `(cx, cy)`**, whereas high-level components (`SmartArts`, `Charts`, `Diagrams`) use **Bottom-Left `(x0, y0)`**.
   - Ensure compact canvas dimensions (`width=120..136`), `text_size >= 10.0`, and an explicit `save()` call.
2. **Stage 2 — Micro-Geometry Grid Review (`drawlib show -g`)**:
   ```bash
   uv run drawlib show doc.md arch.png -s styles.py -u utils.py -g -o .drawlib/scratch/arch_grid.png
   ```
   - Export the diagram with the 10-unit/5-unit coordinate grid overlay and inspect the image multimodally to fix any text clipping, arrow overlaps, tight margins (`>= 4–6` units), or 50%+ neutral balance issues in one shot.
3. **Stage 3 — Macro-Page Browser HTML / PDF Review**:
   ```bash
   ./build.sh
   uv run drawlib serve report_html/ --check
   ```
   - Run the project build, verify zero broken links or missing images via `drawlib serve <html_dir> --check`, and inspect the rendered HTML/PDF page to confirm visual harmony between prose and diagrams.
