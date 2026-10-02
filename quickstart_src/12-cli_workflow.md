# 12. Developer CLI & Build Automation

Drawlib provides a unified command-line interface (`drawlib`) that automates rapid illustration previewing, document compilation, cache management, and local web serving.

## Unified CLI Subcommands

| Command | Usage & Flags | Description |
| :--- | :--- | :--- |
| **`build html`** | `drawlib build html <src> -o <out> [--css google]` | Compiles Markdown documents and embedded diagrams into a responsive static website. |
| **`build pdf`** | `drawlib build pdf <src> -o <out.pdf> [--generate-index]` | Merges chapters in alphabetical order into a publication-ready PDF book with auto-generated table of contents. |
| **`build markdown`** | `drawlib build markdown <src> -o <out>` | Pre-renders embedded diagrams into standalone PNGs for GitHub repository browsing. |
| **`build image`** | `drawlib build image <src> -o <out>` | Batch-executes standalone Python scripts (`images_src/*.py`) into an image directory. |
| **`show`** | `drawlib show <file> [target] [-g] [-o <out.png>]` | Previews an individual script or embedded Markdown block instantly with optional coordinate grid overlay. |
| **`serve`** | `drawlib serve <dir> [-p 8000] [--check]` | Launches a local HTTP preview server and verifies internal links and assets. |
| **`cache`** | `drawlib cache list / clear [--images]` | Inspects or clears the SQLite build cache. |

```drawlib 640px center caption:"Figure 12.1: Unified Drawlib CLI Build & Preview Pipeline"
from drawlib.canvas import setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=120, height=48)

# Input
rectangle(xy=(18, 24), width=24, height=34, r=2, style=Styles.PrimaryOutline)
phosphor.file_text(xy=(18, 30), width=8, style=Styles.Primary)
text(xy=(18, 16), text="Source Docs\n(docs_src/)", style=Styles.PrimaryBold, size=9)

# CLI Engine
rectangle(xy=(56, 24), width=26, height=34, r=2, style=Styles.SecondaryOutline)
phosphor.terminal_window(xy=(56, 30), width=8, style=Styles.Secondary)
text(xy=(56, 16), text="drawlib CLI\n& SQLite Cache", style=Styles.SecondaryBold, size=9)

line((30, 24), (43, 24), arrowhead="->", style=Styles.PrimaryBold)

# Output Targets
targets = [
    (38, "build html -> docs_html/", Styles.AccentFlat),
    (24, "build pdf -> book.pdf", Styles.PrimaryFlat),
    (10, "build markdown -> docs/", Styles.SuccessFlat),
]

for y_pos, label, st in targets:
    line((69, 24), (82, y_pos), arrowhead="->", style=Styles.PrimaryBold)
    rectangle(xy=(101, y_pos), width=36, height=10, r=1.5, style=st, text=label, text_style=Styles.WhiteBold)
```

## High-Performance Incremental Build Cache

Full documentation builds can contain dozens of diagrams. Drawlib avoids redundant compilation using a SHA-256 **SQLite build cache** (`.drawlib/cache.db`):

- **Zero-Latency Repeat Builds**: When a Markdown file or drawing script is compiled, Drawlib computes a SHA-256 hash of its code block, styles, and options. Unchanged diagrams are restored instantly from cache.
- **Forced Rebuilds**: Pass `--no-cache` to bypass the cache, or run `drawlib cache clear --images` to purge cached illustrations.
