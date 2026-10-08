# Chapter 6: AI Agent Integration and Prompting

Drawlib is engineered from the ground up to be "Agent-First", enabling AI coding assistants (Claude, Cursor, Gemini, Copilot) to generate accurate, publication-ready diagrams autonomously. Once basic instructions are registered, the AI interacts with the Drawlib CLI to inspect rules, test drawings, and output verified code.

```drawlib 640px center file:fig_agent_interaction.png caption:"Figure 6.1: Autonomous Interaction Model between Drawlib and AI Agents"
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
rectangle((22.0, 24.0), width=32.0, height=38.0, r=2.0, style=Styles.PrimaryOutline)
rectangle((22.0, 40.0), width=30.0, height=5.5, r=1.5, style=Styles.PrimaryFlat, text="Drawlib (CLI & Rules)", text_style=header_ts)

phosphor.book_bookmark(xy=(9.5, 31.0), width=4.5, style=Styles.Primary)
text((13.5, 31.0), text="drawlib rules show\nOn-demand API specs & rules", style=ts_body)

phosphor.terminal_window(xy=(9.5, 21.5), width=4.5, style=Styles.Primary)
text((13.5, 21.5), text="drawlib show -g\nMillimeter grid output for QA", style=ts_body)

phosphor.gear(xy=(9.5, 12.0), width=4.5, style=Styles.Primary)
text((13.5, 12.0), text="drawlib build\nAutomated PDF / HTML engine", style=ts_body)

# 2. AI Agent (Cursor / Claude / Gemini)
rectangle((71.0, 24.0), width=32.0, height=38.0, r=2.0, style=Styles.AccentOutline)
rectangle((71.0, 40.0), width=30.0, height=5.5, r=1.5, style=Styles.AccentFlat, text="AI Agent (Autonomous)", text_style=header_ts)

phosphor.chats(xy=(58.5, 31.0), width=4.5, style=Styles.Accent)
text((62.5, 31.0), text="1. Query Knowledge Base\nInspect signatures via CLI rules", style=ts_body)

phosphor.code(xy=(58.5, 21.5), width=4.5, style=Styles.Accent)
text((62.5, 21.5), text="2. Prototype in Scratch\nSafe sandbox at .drawlib/scratch/", style=ts_body)

phosphor.eye(xy=(58.5, 12.0), width=4.5, style=Styles.Accent)
text((62.5, 12.0), text="3. Multimodal Inspection\nAuto-detect & fix layout issues", style=ts_body)

# 3. Docs / Illustration (Deliverables)
rectangle((120.0, 24.0), width=32.0, height=38.0, r=2.0, style=Styles.SuccessOutline)
rectangle((120.0, 40.0), width=30.0, height=5.5, r=1.5, style=Styles.SuccessFlat, text="Docs / Illustration", text_style=header_ts)

phosphor.file_text(xy=(107.5, 31.0), width=4.5, style=Styles.Success)
text((111.5, 31.0), text="*.md Technical Specs\nInline ```drawlib``` integration", style=ts_body)

phosphor.file_pdf(xy=(107.5, 21.5), width=4.5, style=Styles.Success)
text((111.5, 21.5), text="*.pdf / Web Site\nPolished, illustrated reports", style=ts_body)

phosphor.git_branch(xy=(107.5, 12.0), width=4.5, style=Styles.Success)
text((111.5, 12.0), text="Git Version Control\nReview diagrams as code diffs", style=ts_body)

# Connectors
line((39.5, 24.0), (53.5, 24.0), arrow_head="<->", style=Styles.DarkBold)
text((46.5, 28.5), text="Rules & Queries", style=Styles.DarkBold.patch(text_size=7.5))
text((46.5, 19.5), text="APIs / Grid Images", style=Styles.Dark.patch(text_size=7.2))

line((88.5, 24.0), (102.5, 24.0), arrow_head="->", style=Styles.DarkBold)
text((95.5, 28.5), text="Verified Code", style=Styles.DarkBold.patch(text_size=7.5))
text((95.5, 19.5), text="Document Sync", style=Styles.Dark.patch(text_size=7.2))
```

## 6.1 Using the Built-In Rule System (`drawlib rules`)

Drawlib embeds comprehensive API specifications and best practices directly in its CLI. Agents can consult rules on demand:

```bash
# List all available rule manuals
uv run drawlib rules list

# Read core agent workflow instructions
uv run drawlib rules show agent-instruction

# Check canvas coordinate system rules
uv run drawlib rules show overview

# Check specific domain module specifications
uv run drawlib rules show lib-smartarts
uv run drawlib rules show lib-diagrams
uv run drawlib rules show lib-charts
```

## 6.2 Setting Project Rule Files

Register these essential rules in `.cursorrules` or `.agents/rules/` so agents follow Drawlib principles automatically:

```markdown
# Drawlib Drawing Rules
- Do NOT generate raw SVG or low-level matplotlib code; always use high-level modules (smartarts, diagrams, charts).
- The canvas origin (0, 0) is at the bottom-left corner.
- Design tokens must be imported and referenced in PascalCase: `Styles` and `Colors`.
- Embedded code blocks must specify `file:<name>.png` and `caption:"..."`.
```

## 6.3 The Autonomous Visual Feedback Loop

Instruct your agent to execute this 4-step self-correction loop when creating illustrations:
1. **Draft Code**: Write the ````drawlib```` block in the document.
2. **Render Grid Preview**:
   ```bash
   uv run drawlib show doc.md arch.png -g -o .drawlib/scratch/arch.png
   ```
3. **Multimodal Review**: Inspect the rendered PNG for label overflow, line overlaps, or tight margins.
4. **Iterative Refinement**: Adjust coordinates and finalize the code.
