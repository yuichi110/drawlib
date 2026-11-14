# 14. CLI Toolchain & Autonomous AI Agent Workflows

Drawlib is engineered from the ground up for both human developers and multimodal AI coding assistants. Because every diagram, document, and slide deck compiles headlessly through a deterministic Command Line Interface (`drawlib`), AI agents never have to guess pixel coordinates blindly or rely on manual GUI clicks.

Instead, an AI coding agent reads on-demand API manuals (`drawlib rules show`), scaffolds a project (`drawlib init`), renders single-diagram coordinate grids (`drawlib show -g`), visually inspects its own output multimodally, self-corrects overlaps in a single pass, and validates every link before delivery (`drawlib serve --check`).

```drawlib align=center code=fold file=ai_multimodal_loop.png caption="Figure 14.1: The 3-Stage Autonomous AI Multimodal Self-Correction Loop"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line, lines
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=158, height=70)

text(
    (79.0, 63.8),
    "Autonomous 3-Stage Multimodal AI Self-Correction Loop",
    style=Styles.DarkBold.patch(text_size=12.8),
)

# Step 0: Rules & Authoring (Neutral)
rectangle((22.5, 39.5), width=32.5, height=33.0, style=Styles.Neutral.patch(shape_r=2.0))
phosphor.book_open((22.5, 50.8), width=5.0, style=Styles.PrimaryBold)
text((22.5, 44.0), "0. Rules & Code", style=Styles.DarkBold.patch(text_size=11.0))
text(
    (22.5, 31.8),
    "• rules show <topic>\n• Author .md / .py\n• styles.py & utils.py",
    style=Styles.Dark.patch(text_size=10.0),
)

# Stage 1: Static & Anchor Check (PrimaryNeutral)
rectangle((60.2, 39.5), width=32.5, height=33.0, style=Styles.PrimaryNeutral.patch(shape_r=2.0))
phosphor.list_checks((60.2, 50.8), width=5.0, style=Styles.PrimaryBold)
text((60.2, 44.0), "Stage 1: Static", style=Styles.DarkBold.patch(text_size=11.0))
text(
    (60.2, 31.8),
    "• 2+ figs & Hero L5-15\n• text_size >= 10.0\n• Verify anchors",
    style=Styles.Dark.patch(text_size=10.0),
)

# Stage 2: Micro-Geometry Grid Vision (Focal PrimaryFlat Hero)
rectangle((97.8, 39.5), width=32.5, height=33.0, style=Styles.PrimaryFlat.patch(shape_r=2.0))
phosphor.grid_four((97.8, 50.8), width=5.0, style=Styles.WhiteBold)
text((97.8, 44.0), "Stage 2: Grid (-g)", style=Styles.WhiteBold.patch(text_size=11.0))
text(
    (97.8, 31.8),
    "• drawlib show -g\n• 10/5u grid vision\n• Fix text overlaps",
    style=Styles.White.patch(text_size=10.0),
)

# Stage 3: Macro-Page Review (SecondaryNeutral)
rectangle((135.5, 39.5), width=32.5, height=33.0, style=Styles.SecondaryNeutral.patch(shape_r=2.0))
phosphor.browser((135.5, 50.8), width=5.0, style=Styles.SecondaryBold)
text((135.5, 44.0), "Stage 3: Macro", style=Styles.DarkBold.patch(text_size=11.0))
text(
    (135.5, 31.8),
    "• build & serve --check\n• 1280x920 browser\n• PDF / DOCX / PPTX",
    style=Styles.Dark.patch(text_size=10.0),
)

# Forward pipeline arrows
line((38.8, 39.5), (43.9, 39.5), arrow_head="->", style=Styles.DarkBold)
line((76.5, 39.5), (81.5, 39.5), arrow_head="->", style=Styles.DarkBold)
line((114.1, 39.5), (119.2, 39.5), arrow_head="->", style=Styles.DarkBold)

# Closed-loop feedback path from Stage 2 back to Step 0
lines([(97.8, 22.8), (97.8, 11.0), (22.5, 11.0), (22.5, 22.2)], arrow_head="->", style=Styles.PrimaryBold)
rectangle((60.2, 11.0), width=64.0, height=7.6, style=Styles.White.patch(shape_r=1.5))
text(
    (60.2, 11.0),
    "Self-Correction Loop: Exact 1-Shot Coordinate Fix",
    style=Styles.DarkBold.patch(text_size=10.2),
)

save()
```

---

## 14.1 Bootstrapping Projects & AI Agent Rules (`drawlib init`)

The `drawlib init` command group handles two foundational setup tasks: scaffolding project workspaces (`drawlib init project`) and provisioning AI coding assistant instruction files (`drawlib init agent`).

Running `drawlib init agent` installs Drawlib's architectural conventions, `720pt` typography math, coordinate anchor rules, and 3-stage verification protocol directly into your AI assistant's native rule directory. Drawlib `v0.3.10` provides 9 built-in agent targets—and because `AGENTS.md` is an open multi-tool standard, it also works seamlessly with `AGENTS.md`-compatible tools (including OpenCode and Kiro):

| CLI Target | AI Coding Assistant | Generated Workspace Path | Rule Format & Loading Behavior |
| :--- | :--- | :--- | :--- |
| **`antigravity`** | Google Antigravity | `.agents/rules/drawlib.md` | YAML frontmatter (`trigger: model_decision` or `always_on`) |
| **`gemini`** | Gemini CLI | `GEMINI.md` | Non-destructive HTML comment marker merge (`~/.gemini/GEMINI.md` with `--global`) |
| **`claude`** | Claude Code | `.claude/rules/drawlib.md` | Modular Markdown rule coexisting cleanly with root `CLAUDE.md` |
| **`cursor`** | Cursor | `.cursor/rules/drawlib.mdc` | MDC frontmatter (`description`, `alwaysApply`) |
| **`codex`** | OpenAI Codex / `AGENTS.md` | `AGENTS.md` | Non-destructive HTML marker merge; shared by Codex, Kiro & `AGENTS.md` agents |
| **`copilot`** | GitHub Copilot | `.github/instructions/drawlib.instructions.md` | YAML frontmatter (`applyTo: "**/*_src/**, **/*.md, **/*.py"`) |
| **`windsurf`** | Windsurf | `.windsurf/rules/drawlib.md` | Cascade workspace rule with YAML trigger frontmatter |
| **`cline`** | Cline | `.clinerules/drawlib.md` | Individually toggleable rule inside `.clinerules/` |
| **`roo`** | Roo Code | `.roo/rules/drawlib.md` | Modular workspace or `--global` Roo rule file |

Pass `--detect` to inspect existing configuration folders in any repository and generate matching rule files automatically, or `-m auto` (default) so the rule activates on demand without consuming context tokens on unrelated backend tasks:

```bash
# List all supported AI coding agent targets and destination paths
uv run drawlib init agent list

# Auto-detect configured AI assistants in the current repo and install rules
uv run drawlib init agent --detect

# Explicitly generate modular rules for specific assistants (or 'all' for all 7 modular files)
uv run drawlib init agent antigravity claude cursor copilot

# Force always-on loading for dedicated documentation repositories
uv run drawlib init agent antigravity --mode always

# Install user-wide global Drawlib rules into ~/.claude/rules/ or ~/.gemini/config/rules/
uv run drawlib init agent claude --global
```

---

## 14.2 Compilation, Incremental Caching & Dev Server

Once a project is scaffolded, five core CLI command groups drive day-to-day authoring, rapid visual inspection, multi-target publishing, and CI quality gates:

| Command Group | Key Subcommands & Flags | Core Purpose |
| :--- | :--- | :--- |
| **`drawlib build`** | `html`, `pdf`, `docx`, `slide`, `pptx`, `markdown`, `image` (`-s`, `-u`, `--no-cache`) | Compiles `<target>_src/` into HTML portals/books/decks, vector PDFs, editable `.docx`/`.pptx` Office files, GitHub Markdown, and batch PNG/WebP/GIF images. |
| **`drawlib show`** | `<file> [target] -s styles.py -u utils.py -g -o preview.png` | Renders a single `.py` script or named Markdown block (`file=arch.png`) headlessly to disk with an optional `10/5`-unit coordinate grid (`-g`). |
| **`drawlib serve`** | `<html_dir> [-p 8000] [--no-browser] [--check]` | Launches a zero-dependency local HTTP preview server, or runs `--check` in CI to verify zero broken `<a href>` links or missing `<img src>` assets. |
| **`drawlib cache`** | `list`, `clear --images`, `clear --all`, `download --all`, `download --browser` | Manages `.drawlib/cache.db` SQLite diagram hashes and pre-downloads fonts, 34 icon suites, GeoJSON maps, and Playwright headless Chromium. |
| **`drawlib rules`** | `list`, `show <topic> [--raw \| --rebuild]`, `build --all`, `clear` | Built-in self-documenting manual (`overview`, `cli`, `style-guide`, `review-guide`, `lib-*`) with on-demand reference illustrations for humans and LLMs. |

### Inside `.drawlib/cache.db`: SHA-256 Content-Addressed Caching

Re-executing 50 Python diagrams on every prose typo fix would slow down iterative writing. Before running any `drawlib` block or `.py` script, Drawlib computes a deterministic **SHA-256 digest** across four inputs:
1. The exact Python source code of the diagram block or script.
2. The full contents of `styles.py` (`-s`) and `utils.py` (`-u`).
3. Local static files referenced as string literals (such as `"_assets/logo.png"`).
4. Target output format (`png`, `webp`, `svg`), relative path, and slide context.

On a cache hit in `.drawlib/cache.db`, Drawlib restores the compiled binary in **under 1 millisecond** without invoking Matplotlib. The database automatically writes `.drawlib/.gitignore` (`*`), invalidates entries when `drawlib` or `matplotlib` versions upgrade, and evicts the oldest 50% of blobs above `1 GiB`. If your diagram imports an external custom Python module outside `styles.py` and `utils.py`, pass `--no-cache` or run `drawlib cache clear --images`:

```bash
# 1. Inspect a single named Markdown diagram headlessly with the 10/5-unit grid (-g)
uv run drawlib show doc_src/en/01_overview.md system_arch.png \
    -s doc_src/styles.py -u doc_src/utils.py -g --no-cache -o .drawlib/scratch/arch_grid.png

# 2. Multi-target builds (HTML, A4 PDF with TOC, MS Word .docx, 16:9 Slides & PowerPoint .pptx)
uv run drawlib build html docs_src/ -o docs_html/ -s docs_src/styles.py -u docs_src/utils.py
uv run drawlib build pdf doc_src/ -o manual.pdf --page-break --generate-index -s doc_src/styles.py
uv run drawlib build docx doc_src/ -o manual.docx --page-break --generate-index --dpi 200
uv run drawlib build slide slide_src/ -o slide_html/ -s slide_src/styles.py
uv run drawlib build pptx slide_src/ -o slide.pptx --dpi 240 -s slide_src/styles.py
uv run drawlib build markdown docs_src/ -o docs_markdown/
uv run drawlib build image images_src/ -o images/ -f webp

# 3. CI pre-warming, SQLite image cache reset, broken-link check & on-demand rules lookup
uv run drawlib cache download --all
uv run drawlib cache clear --images
uv run drawlib serve docs_html/ --check
uv run drawlib rules list
uv run drawlib rules show lib-smartarts-overview --raw
```

```drawlib align=center code=fold file=cli_command_map.png caption="Figure 14.2: Drawlib CLI Command Ecosystem & SHA-256 SQLite Build Cache Pipeline"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=158, height=76)

text(
    (79.0, 70.2),
    "Drawlib CLI Toolchain & SHA-256 Incremental Cache Architecture",
    style=Styles.DarkBold.patch(text_size=12.8),
)

# Top Row of CLI Command Groups (3 cards, width=46.0)
rectangle((29.0, 56.5), width=46.0, height=16.5, style=Styles.Neutral.patch(shape_r=2.0))
phosphor.folder_plus((11.5, 60.5), width=4.6, style=Styles.PrimaryBold)
text((31.5, 60.5), "drawlib init", style=Styles.DarkBold.patch(text_size=11.2))
text((29.0, 52.2), "project (5 types) | agent (--detect)", style=Styles.Dark.patch(text_size=10.0))

rectangle((79.0, 56.5), width=46.0, height=16.5, style=Styles.Neutral.patch(shape_r=2.0))
phosphor.book_open((61.5, 60.5), width=4.6, style=Styles.PrimaryBold)
text((81.5, 60.5), "drawlib rules", style=Styles.DarkBold.patch(text_size=11.2))
text((79.0, 52.2), "list | show <topic> (--raw)", style=Styles.Dark.patch(text_size=10.0))

rectangle((129.0, 56.5), width=46.0, height=16.5, style=Styles.PrimaryNeutral.patch(shape_r=2.0))
phosphor.grid_four((111.5, 60.5), width=4.6, style=Styles.PrimaryBold)
text((131.5, 60.5), "drawlib show", style=Styles.DarkBold.patch(text_size=11.2))
text((129.0, 52.2), "<file> [target] -g -o preview.png", style=Styles.Dark.patch(text_size=10.0))

# Middle Row of CLI Command Groups (build is the 1 PrimaryFlat focal card)
rectangle((29.0, 37.0), width=46.0, height=16.5, style=Styles.PrimaryFlat.patch(shape_r=2.0))
phosphor.cpu((11.5, 41.0), width=4.6, style=Styles.WhiteBold)
text((31.5, 41.0), "drawlib build", style=Styles.WhiteBold.patch(text_size=11.2))
text((29.0, 32.7), "html | pdf | docx | slide | pptx | image", style=Styles.White.patch(text_size=10.0))

rectangle((79.0, 37.0), width=46.0, height=16.5, style=Styles.SecondaryNeutral.patch(shape_r=2.0))
phosphor.globe((61.5, 41.0), width=4.6, style=Styles.SecondaryBold)
text((81.5, 41.0), "drawlib serve", style=Styles.DarkBold.patch(text_size=11.2))
text((79.0, 32.7), "<dir> -p 8000 | --check (CI gate)", style=Styles.Dark.patch(text_size=10.0))

rectangle((129.0, 37.0), width=46.0, height=16.5, style=Styles.Neutral.patch(shape_r=2.0))
phosphor.database((111.5, 41.0), width=4.6, style=Styles.SecondaryBold)
text((131.5, 41.0), "drawlib cache", style=Styles.DarkBold.patch(text_size=11.2))
text((129.0, 32.7), "list | clear --images | download --all", style=Styles.Dark.patch(text_size=10.0))

# Bottom Pipeline Bar: .drawlib/cache.db SHA-256 Engine
rectangle((79.0, 14.0), width=146.0, height=16.5, style=Styles.Neutral.patch(shape_r=2.2))
rectangle((31.0, 14.0), width=42.0, height=11.5, style=Styles.White.patch(shape_r=1.5))
text((31.0, 14.0), "Code + styles/utils + _assets", style=Styles.DarkBold.patch(text_size=10.0))

line((52.0, 14.0), (59.5, 14.0), arrow_head="->", style=Styles.DarkBold)

rectangle((78.5, 14.0), width=36.0, height=11.5, style=Styles.PrimaryNeutral.patch(shape_r=1.5))
text((78.5, 14.0), "SHA-256 cache.db", style=Styles.DarkBold.patch(text_size=10.2))

line((96.5, 14.0), (104.0, 14.0), arrow_head="->", style=Styles.DarkBold)

rectangle((126.5, 14.0), width=43.0, height=11.5, style=Styles.White.patch(shape_r=1.5))
text((126.5, 14.0), "Hit: <1ms | Miss: Render", style=Styles.DarkBold.patch(text_size=10.0))

# Connect build -> SHA-256 pipeline outer boundary cleanly
line((29.0, 28.5), (29.0, 22.6), arrow_head="->", style=Styles.DarkBold)

save()
```

---

## 14.3 Deep-Dive: The 3-Stage Autonomous AI Review Loop

Inspecting a single PNG in isolation is not enough to guarantee publication quality: a diagram might have subtle label overlaps inside the canvas (micro-geometry defects) or shrink to microscopic text inside an HTML column or 16:9 slide (macro-page defects). AI agents eliminate both failure modes by executing all three verification stages before finishing:

1. **Stage 1 — Static Code & Anchor Pre-Check**:
   - Confirm `>= 2` embedded `drawlib` diagrams per documentation page and a **Top Hero diagram starting on Lines 5–15** with `code=fold` (so readers see a visual summary above the fold).
   - Confirm zero pixel width caps (`width=500px`/`600px` omitted), `text_size >= 10.0`, strictly relative Markdown paths, and exact coordinate anchor semantics (`Center` vs. `Bottom-Left` vs. `Top-Left`).
2. **Stage 2 — Micro-Geometry Grid Review (`drawlib show -g`)**:
   - Export each created or modified diagram headlessly with `-g` (`uv run drawlib show <file> <target.png> -s styles.py -u utils.py -g -o .drawlib/scratch/<unique>_grid.png`) and inspect the PNG with multimodal vision.
   - Because `-g` overlays **10-unit major grid lines** (labeled numerically) and **5-unit minor dashed lines**, the agent reads off exact coordinate adjustments in a single iteration—fixing any text border clipping, arrowhead collisions, perimeter margins (`< 4–6` units), or rainbow color overuse (`< 50%` neutral fills).
3. **Stage 3 — Macro-Page & Deliverable Verification**:
   - Compile the project (`./<target>_src/build.sh`), run `uv run drawlib serve <target>_html/ --check` to verify zero broken internal links or missing image assets, and capture a **`1280×920` headless Chromium screenshot** of the rendered HTML (or inspect compiled `PDF`, `DOCX`, and `PPTX` pages).
   - Confirm that the Top Hero sits cleanly above the fold and that in-diagram typography matches surrounding `16px` HTML prose (or `26px` slide prose on `1920×1080` decks), then clean up `.drawlib/scratch/`.

---

## 14.4 Scaling with Parallel Multi-Agent Delegation

When creating or updating multi-chapter whitepapers (`doc`), multi-section portals (`site`/`catalog`), or 20-slide decks (`slide`), loading dozens of high-resolution grid preview PNGs into a single agent's context window wastes tokens and latency. Drawlib's modular file architecture maps cleanly onto a **3-Phase Orchestrator–Subagent Workflow**:

- **Phase 1 — Parent Orchestrator Scaffolds Shared Foundation**: The parent agent runs `drawlib init project`, finalizes shared `drawlib.toml`, `styles.py` (`ja/styles.py`), `utils.py`, `_assets/`, and `<lang>/navbar.md` or numbered chapter filenames first.
- **Phase 2 — Parallel Subagents Author Disjoint Files (`--no-cache`)**: Each subagent receives exclusive ownership of disjoint `.md` or `.py` files (treating shared config files as read-only) and runs Stage 1 + Stage 2 grid reviews (`drawlib show ... -g --no-cache -o .drawlib/scratch/<worker>_<stem>.png`) using **unique scratch filenames**—never running `./build.sh` concurrently so `.drawlib/cache.db` never experiences SQLite lock contention.
- **Phase 3 — Parent Runs Unified Build & Link Gate**: Once all subagents complete Stage 2 visual verification, the parent orchestrator runs `./<target>_src/build.sh` once, validates cross-page links with `drawlib serve --check`, performs Stage 3 browser/PDF review, and removes `.drawlib/scratch/`.
