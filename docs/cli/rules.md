# `drawlib rules`

The `drawlib rules` command provides instant access to exhaustive API specifications, architectural guidelines, and production drawing examples. These manuals are specifically curated for AI coding agents (such as Deepmind Antigravity, Claude, and ChatGPT) and human engineers developing illustrations programmatically.

---

## 1. Syntax Overview

```bash
drawlib rules [COMMAND] [TOPIC] [OPTIONS]
```

If invoked without arguments (`drawlib rules`), it prints a summary of available topics and quick commands.

---

## 2. Available Subcommands

| Subcommand | Description | Example |
| :--- | :--- | :--- |
| **`show`** | Prints the complete architectural rule guide for a specific topic. | `drawlib rules show shapes` |
| **`list`** (alias: `topics`) | Lists all available rule topics and cached build status. | `drawlib rules list` |
| **`build`** | Compiles rule Markdown and illustrations into cached package assets. | `drawlib rules build smartarts` |

---

## 3. Available Topics

Drawlib features 11 comprehensive rule topics:

| Topic | Primary Focus |
| :--- | :--- |
| **`overview`** | Package architecture, coordinate spaces, Cartesian geometry, and rendering pipeline. |
| **`cli`** | Complete command line interface and subcommands. |
| **`docs_build`** | Markdown parsing, code block options, HTML/Markdown/PDF compilation, and templates. |
| **`shapes`** | All 21 geometric primitives, block arrows, anchors, and alignment transforms. |
| **`lines`** | Straight, curved, bezier, chained, and arc lines with arrowhead semantics. |
| **`text`** | Typography, text alignments, multiline rendering, and vertical text. |
| **`icons`** | Phosphor vector font icons and official Google Cloud Platform architecture icons. |
| **`preset_styles`** | Palettes (`default`, `essentials`, `monochrome`) and custom theme modeling. |
| **`smartarts`** | 11 high-level components (SourceCode, Tables, MindMaps, Chevrons, Trees, etc.). |
| **`charts`** | 7 pure-Python vector charts (Bar, Line, Area, Pie, Radar, Scatter, Gantt). |
| **`diagrams`** | Domain diagrams (Architecture, Sequence, Flow, Class, ER, State Machine). |

---

## 4. Usage Examples

### Inspecting Guidelines for AI Agents
When working with AI coding assistants, you can inject specific Drawlib rules directly into their context:

```bash
# Output full shapes manual:
drawlib rules show shapes

# Output sequence diagram rules:
drawlib rules show diagrams
```

### Forcing Asset Rebuild
```bash
drawlib rules build all --force
```

---

<p align="center"><em>© 2026 drawlib by Yuichi Ito. Released under the Apache 2.0 License.</em></p>
