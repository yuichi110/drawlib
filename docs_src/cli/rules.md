# `drawlib rules`

The `drawlib rules` command provides instant access to exhaustive API specifications, architectural guidelines, and production drawing examples. These manuals are specifically curated for AI coding agents (such as Deepmind Antigravity, Claude, and ChatGPT) and human engineers developing illustrations programmatically.

> **Tip**: If you are using `uv`, run commands with `uv run` (e.g., `uv run drawlib rules`).

---

## 1. Syntax Overview

```bash
drawlib rules [COMMAND] [ARGS...] [OPTIONS]
```

If invoked without arguments (`drawlib rules`), it displays contextual help and lists all available subcommands.

---

## 2. Available Subcommands

| Subcommand | Description | Example |
| :--- | :--- | :--- |
| **`show`** | Prints the complete architectural rule guide for a specific topic. | `drawlib rules show lib-shapes` |
| **`list`** | Lists all available rule topics and cached build status. | `drawlib rules list` |
| **`build`** | Compiles rule Markdown and illustrations into cached package assets. | `drawlib rules build lib-smartarts` |
| **`clear`** | Deletes all cached rule documents and generated illustration assets. | `drawlib rules clear` |

---

## 3. Available Topics

Drawlib features 20 comprehensive rule topics divided into General Guidelines and Library Modules:

### General Guidelines
| Topic | Primary Focus |
| :--- | :--- |
| **`overview`** | Package architecture, coordinate spaces, Cartesian geometry, and rendering pipeline. |
| **`overview-min`** | Concise overview (<10k chars) for context-constrained rule files. |
| **`cli`** | Complete command line interface and subcommands. |
| **`docs-build`** | Markdown parsing, code block options, HTML/Markdown/PDF compilation, and templates. |

### Library Modules (`drawlib.*`)
| Topic | Primary Focus |
| :--- | :--- |
| **`lib-canvas`** | Canvas configuration, coordinate space, clear/save lifecycle, and background. |
| **`lib-shapes`** | All 22 geometric primitives, block arrows, anchors, and alignment transforms. |
| **`lib-lines`** | Straight, curved, bezier, chained, and arc lines with arrowhead semantics. |
| **`lib-text`** | Typography, text alignments, multiline rendering, and vertical text. |
| **`lib-colors`** | Color models, RGB/RGBA tuples, hex conversion, and palette classes. |
| **`lib-styles`** | Styles and utils architecture, active preset styles, colors palette, and dynamic custom scripts. |
| **`lib-preset-styles`** | Systematic style naming rules (`<color>_<variant>`) and palette classes. |
| **`lib-fonts`** | Font configuration, system/file fonts, CJK/multilingual typography, and cache. |
| **`lib-images`** | Embedding bitmap and vector images, scaling, rotation, and Dimage. |
| **`lib-icons`** | Phosphor vector font icons and official Google Cloud Platform architecture icons. |
| **`lib-math`** | Geometry helpers, coordinate calculations, angles, distance, and bounding box. |
| **`lib-types`** | Type models, Style class, base classes, and Drawlib type conventions. |
| **`lib-smartarts`** | Tables, trees, mindmaps, and structured visual elements. |
| **`lib-charts`** | Bar, line, pie, scatter, radar, area, and Gantt charts. |
| **`lib-diagrams`** | Domain diagrams (Architecture, Sequence, Flow, Class, ER, State Machine). |
| **`lib-tools`** | Python developer API for document building, diagram export, and cache management. |

---

## 4. Usage Examples

### Inspecting Guidelines for AI Agents
When working with AI coding assistants, you can inject specific Drawlib rules directly into their context:

```bash
# Output full shapes manual:
drawlib rules show lib-shapes

# Output sequence diagram rules:
drawlib rules show lib-diagrams
```

### Forcing Asset Rebuild
```bash
drawlib rules build --all --force
```

---

<p align="center"><em>© 2026 drawlib by Yuichi Ito. Released under the Apache 2.0 License.</em></p>
