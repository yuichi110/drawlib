# 12. Developer CLI & Build Automation

Drawlib provides a unified command-line interface (`drawlib`) that automates rapid illustration previewing, document compilation, cache management, and local web serving.

## Unified CLI Subcommands

| Command | Usage & Flags | Description |
| :--- | :--- | :--- |
| **`build html`** | `drawlib build html <src> -o <out> [--css google]` | Compiles Markdown documents and embedded diagrams into a responsive static website. |
| **`build pdf`** | `drawlib build pdf <src> -o <out.pdf> [--generate-index]` | Merges chapters into a publication-ready vector PDF (auto-downloads headless Chromium on first run). |
| **`build docx`** | `drawlib build docx <src> -o <out.docx> [--generate-index]` | Exports `doc` Markdown chapters and diagrams into an editable MS Word (`.docx`) document. |
| **`build slide`** | `drawlib build slide <src> -o <out>` | Compiles slide Markdown files into an interactive 16:9 HTML presentation deck with Presenter View. |
| **`build pptx`** | `drawlib build pptx <src> -o <out.pptx>` | Exports `slide` Markdown files into an editable 16:9 MS PowerPoint (`.pptx`) deck with speaker notes. |
| **`build markdown`** | `drawlib build markdown <src> -o <out>` | Pre-renders embedded diagrams into standalone PNGs for GitHub repository browsing. |
| **`build image`** | `drawlib build image <src> -o <out>` | Batch-executes standalone Python scripts (`images_src/*.py`) or extracts embedded diagrams. |
| **`show`** | `drawlib show <file> [target] [-g] [-o <out.png>]` | Previews an individual script or embedded Markdown block instantly with optional coordinate grid overlay. |
| **`serve`** | `drawlib serve <dir> [-p 8000] [--check]` | Launches a local HTTP preview server and verifies internal links and assets. |
| **`cache`** | `drawlib cache list / download [--all\|--browser] / clear` | Pre-downloads fonts, icons, maps, and headless Chromium, or clears the SQLite build cache. |

```drawlib align=center file=cli_pipeline.png caption="Figure 12.1: Unified Drawlib CLI Build & Preview Pipeline"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=136, height=58)

# Input
rectangle(xy=(19, 29), width=26, height=42, style=Styles.Neutral.patch(shape_r=2.0))
phosphor.file_text(xy=(19, 37), width=7, style=Styles.Primary)
text(xy=(19, 20), text="Source Docs\n(*_src/)", style=Styles.DarkBold.patch(text_size=10.5))

# CLI Engine
rectangle(xy=(57, 29), width=28, height=42, style=Styles.PrimaryNeutral.patch(shape_r=2.0))
phosphor.terminal_window(xy=(57, 37), width=7, style=Styles.Primary)
text(xy=(57, 20), text="drawlib CLI\n& SQLite Cache", style=Styles.DarkBold.patch(text_size=10.5))

line((32, 29), (43, 29), arrow_head="->", style=Styles.DarkBold)

# Output Targets
targets = [
    (49.0, "build html / slide -> Web", Styles.Neutral, Styles.DarkBold.patch(text_size=10.0)),
    (35.7, "build pdf -> Vector PDF", Styles.PrimaryFlat, Styles.WhiteBold.patch(text_size=10.0)),
    (22.3, "build docx / pptx -> Office", Styles.SecondaryNeutral, Styles.DarkBold.patch(text_size=10.0)),
    (9.0, "build md / image -> MD & PNG", Styles.Neutral, Styles.DarkBold.patch(text_size=10.0)),
]

for y_pos, label, st, txt_st in targets:
    line((71, 29), (85, y_pos), arrow_head="->", style=Styles.DarkBold)
    rectangle(xy=(107.5, y_pos), width=45, height=10, style=st.patch(shape_r=1.8), text=label, text_style=txt_st)

save()
```

## High-Performance Incremental Build Cache

Full documentation builds can contain dozens of diagrams. Drawlib avoids redundant compilation using a SHA-256 **SQLite build cache** (`.drawlib/cache.db`):

- **Zero-Latency Repeat Builds**: When a Markdown file or drawing script is compiled, Drawlib computes a SHA-256 hash of its code block, styles, and options. Unchanged diagrams are restored instantly from cache.
- **Forced Rebuilds**: Pass `--no-cache` to bypass the cache, or run `drawlib cache clear --images` to purge cached illustrations.
