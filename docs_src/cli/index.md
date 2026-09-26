# CLI Overview & Global Options

Drawlib provides a comprehensive command line interface (`drawlib`) built on Python and Typer. It manages document builds, asset downloads, template inspection, development previewing, and AI coding agent guidelines.

---

## 1. Invoking the CLI

Depending on your workflow and environment management, you can invoke the CLI in several ways:

### Using uv (Recommended)

In a project managed with `uv`, run commands with `uv run`:

```bash
$ uv run drawlib --help
```

> **Tip**: If your virtual environment is currently activated (`source .venv/bin/activate`), you can call `drawlib` directly without `uv run`.

### Using pip / Active Virtual Environment

If Drawlib is installed in your active virtual environment or global Python environment:

```bash
$ drawlib --help
```

### Python Module Execution

You can also run Drawlib directly through the Python module:

```bash
$ python -m drawlib --help
```

> **Note on Command Syntax**: Throughout this CLI documentation, commands are written as `drawlib <command> ...` for brevity. If you are using `uv` without an activated virtual environment, simply prefix them with `uv run` (e.g., `uv run drawlib build html docs_src/`).

---

## 2. Command Hierarchy

The CLI is organized into specialized subcommands:

| Command | Purpose | Key Subcommands & Options |
| :--- | :--- | :--- |
| **`build`** | Compiles documents or drawing scripts into images, Markdown, HTML, or PDF. | `image`, `markdown`, `html`, `pdf` |
| **`serve`** | Launches a local HTTP development server for live previewing. | `--port`, `--check`, `--no-browser` |
| **`init`** | Scaffolds starter projects with templates. | `simple`, `site`, `pdf`, `--here` |
| **`show`** | Executes and renders a specific illustration block in a GUI viewer or file. | `--grid`, `--output`, `--config` |
| **`export`** | Headless extraction and export of a diagram directly to an image file. | `--output`, `--grid`, `--config` |
| **`cache`** | Manages local caches for dynamic release assets (fonts and icons). | `clear`, `list`, `download` |
| **`template`** | Manages built-in Jinja2 templates for HTML and PDF output. | `html`, `pdf`, `export`, `validate` |
| **`css`** | Manages built-in CSS stylesheets. | `html`, `pdf`, `export` |
| **`rules`** | Displays drawing guidelines and architectural rules for AI agents. | `show`, `build`, `topics`, `list` |

```drawlib 700px center caption:"Drawlib Unified CLI Command Hierarchy"
from drawlib.canvas import save, setup
from drawlib.colors import Colors, Colors140
from drawlib.fonts import FontRoboto
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.text import text
from drawlib.types import Style
from drawlib.config import styles

setup(width=140, height=80)

# Colors
blue_primary = Colors140.RoyalBlue
purple_primary = Colors140.DarkSlateBlue
teal_primary = Colors140.Teal
orange_primary = Colors140.DarkOrange

# Root CLI Box
rectangle(
    (70, 68),
    width=44,
    height=16,
    r=3,
    style=styles.primary.patch(shape_fill_color=Colors140.GhostWhite, shape_line_color=purple_primary, shape_line_width=2.5),
)
text((70, 72), "drawlib CLI", style=styles.primary.patch(text_size=15, text_font=FontRoboto.ROBOTO_BOLD, text_color=purple_primary))
text((70, 64), "drawlib [OPTIONS] <command>", style=styles.primary.patch(text_size=10, text_color=Colors140.DarkSlateGray))

# 3 Category Clusters
# Cluster 1: Document & Project (Left)
rectangle(
    (26, 32),
    width=40,
    height=42,
    r=4,
    style=styles.primary.patch(shape_fill_color=Colors140.AliceBlue, shape_line_color=blue_primary, shape_line_width=1.8),
)
text((26, 47), "Documentation", style=styles.primary.patch(text_size=13, text_font=FontRoboto.ROBOTO_BOLD, text_color=blue_primary))

rectangle((26, 37), width=32, height=7, r=2, style=styles.primary.patch(shape_fill_color=Colors.White, shape_line_color=blue_primary, shape_line_width=1))
text((26, 37), "build (html/md/pdf)", style=styles.primary.patch(text_size=10, text_font=FontRoboto.ROBOTO_BOLD))

rectangle((26, 27), width=32, height=7, r=2, style=styles.primary.patch(shape_fill_color=Colors.White, shape_line_color=blue_primary, shape_line_width=1))
text((26, 27), "serve (preview site)", style=styles.primary.patch(text_size=10, text_font=FontRoboto.ROBOTO_BOLD))

rectangle((26, 17), width=32, height=7, r=2, style=styles.primary.patch(shape_fill_color=Colors.White, shape_line_color=blue_primary, shape_line_width=1))
text((26, 17), "init (scaffold project)", style=styles.primary.patch(text_size=10, text_font=FontRoboto.ROBOTO_BOLD))

# Cluster 2: Diagram Inspection (Center)
rectangle(
    (70, 32),
    width=40,
    height=42,
    r=4,
    style=styles.primary.patch(shape_fill_color=Colors140.HoneyDew, shape_line_color=teal_primary, shape_line_width=1.8),
)
text((70, 47), "Inspection & Export", style=styles.primary.patch(text_size=13, text_font=FontRoboto.ROBOTO_BOLD, text_color=teal_primary))

rectangle((70, 34), width=32, height=9, r=2, style=styles.primary.patch(shape_fill_color=Colors.White, shape_line_color=teal_primary, shape_line_width=1))
text((70, 34), "show (GUI preview)", style=styles.primary.patch(text_size=10, text_font=FontRoboto.ROBOTO_BOLD))

rectangle((70, 21), width=32, height=9, r=2, style=styles.primary.patch(shape_fill_color=Colors.White, shape_line_color=teal_primary, shape_line_width=1))
text((70, 21), "export (save image)", style=styles.primary.patch(text_size=10, text_font=FontRoboto.ROBOTO_BOLD))

# Cluster 3: Assets & System (Right)
rectangle(
    (114, 32),
    width=40,
    height=42,
    r=4,
    style=styles.primary.patch(shape_fill_color=Colors140.Linen, shape_line_color=orange_primary, shape_line_width=1.8),
)
text((114, 48), "Assets & Standards", style=styles.primary.patch(text_size=13, text_font=FontRoboto.ROBOTO_BOLD, text_color=orange_primary))

rectangle((114, 39), width=32, height=6.5, r=2, style=styles.primary.patch(shape_fill_color=Colors.White, shape_line_color=orange_primary, shape_line_width=1))
text((114, 39), "cache (fonts/icons)", style=styles.primary.patch(text_size=9.5, text_font=FontRoboto.ROBOTO_BOLD))

rectangle((114, 30), width=32, height=6.5, r=2, style=styles.primary.patch(shape_fill_color=Colors.White, shape_line_color=orange_primary, shape_line_width=1))
text((114, 30), "template (Jinja2)", style=styles.primary.patch(text_size=9.5, text_font=FontRoboto.ROBOTO_BOLD))

rectangle((114, 21), width=32, height=6.5, r=2, style=styles.primary.patch(shape_fill_color=Colors.White, shape_line_color=orange_primary, shape_line_width=1))
text((114, 21), "css (presets)", style=styles.primary.patch(text_size=9.5, text_font=FontRoboto.ROBOTO_BOLD))

rectangle((114, 12), width=32, height=6.5, r=2, style=styles.primary.patch(shape_fill_color=Colors.White, shape_line_color=orange_primary, shape_line_width=1))
text((114, 12), "rules (AI guidelines)", style=styles.primary.patch(text_size=9.5, text_font=FontRoboto.ROBOTO_BOLD))

# Connect Root to Clusters
line((55, 60), (32, 53), arrowhead="->", style=styles.primary.patch(line_width=1.8, line_color=blue_primary))
line((70, 60), (70, 53), arrowhead="->", style=styles.primary.patch(line_width=1.8, line_color=teal_primary))
line((85, 60), (108, 53), arrowhead="->", style=styles.primary.patch(line_width=1.8, line_color=orange_primary))

save()
```

---

## 3. Global Options

These options apply across all `drawlib` subcommands:

| Option | Flag | Description |
| :--- | :--- | :--- |
| `--version` | `-v` | Displays the installed software and API version and exits. |
| `--verbose` | | Enables verbose logging output (logging level `DEBUG`). |
| `--debug` | | Alias for `--verbose`. |
| `--quiet` | | Suppresses informational messages, displaying only errors. |
| `--developer` | | Enables verbose logging and disables user-facing error suppression, showing raw Python tracebacks. |
| `--help` | `-h` | Displays help message and command syntax. |

---

## 4. Next Steps

- **[`drawlib build`](./build.md)**: Compile Markdown and Python scripts to production targets.
- **[`drawlib serve`](./serve.md)**: Host documentation locally with automated asset integrity validation.
- **[`drawlib init`](./init.md)**: Bootstrap starter projects.
- **[`drawlib show` & `export`](./inspect.md)**: Interactive previewing and single-block rendering.
- **[`drawlib cache` & Assets](./assets.md)**: Manage font and icon caches.
- **[`drawlib rules`](./rules.md)**: AI agent rules and API reference manuals.

---

<p align="center"><em>© 2026 drawlib by Yuichi Ito. Released under the Apache 2.0 License.</em></p>
