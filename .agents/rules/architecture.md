---
trigger: always_on
---

# Architecture Guidelines for drawlib

This document describes the project structure and architectural principles of the `drawlib` project.

## 1. Project Root Structure
- `src/drawlib/`: The main source code directory.
  - Public domain modules: `canvas.py`, `shapes.py`, `lines.py`, `text.py`, `preset_colors.py`, `preset_styles.py`, `styles.py`, `utils.py`, `icons.py`, `fonts.py`, `types.py`, `images.py`, `charts/`, `diagrams/`, `smartarts.py`, `math.py`, `builder.py`, `tools.py`.
  - `_core/`: Core drawing engine implementation details (`l1_core`, `l2_types`, `l3_colors`, `l3_external`, `l3_fonts`, `l3_images`, `l3_math`, `l3_styles`, `l4_canvas`).
  - `_preset_styles/`, `_charts/`, `_diagrams/`, `_smartarts/`, `_icons/`, `_css_templates/`, `_project_templates/`: Domain implementations and styling/template assets.
  - `_cli/`, `_builder/`, `_http_server/`: CLI entrypoint, doc & image build engines, and local preview server.
- `docs_src/`: Source of truth for documentation and technical guides written in Markdown.
- `docs/`: Generated Markdown documentation for GitHub repository browsing (do not edit directly).
- `docs_html/`: Generated static HTML site for web hosting (do not edit directly).
- `tests/`: Contains unit and integration tests.
- `tools/`: Project developer CLI (`tools/dcli/`) and maintenance scripts (`tools/scripts/`).
- `pyproject.toml`: Project metadata and tool configurations (Ruff, Pyright, uv).

## 2. Package Architecture
`drawlib` follows a modular Python package layout (`src/drawlib/`):
- Standard Python package layout.
- Package releases and versioning are managed via Semantic Versioning in PyPI/Git tags.
- Public domain facades (`canvas`, `shapes`, `lines`, `preset_colors`, `preset_styles`, `styles`, `utils`, etc.) re-export clean interfaces from internal modules.

## 3. Module Hierarchy (Internal Structure)

### 3.1. Public Facades
- Located at `src/drawlib/*.py`.
- Re-exports domain symbols intended for end-users (`canvas`, `shapes`, `lines`, `text`, `preset_colors`, `preset_styles`, `styles`, `utils`, etc.).

### 3.2. Core Implementation (`_core/`)
The `_core/` directory contains internal drawing logic and is not meant to be accessed directly by users.
- **Layered Structure**: `l1_core`, `l2_types`, `l3_colors`, `l3_external`, `l3_fonts`, `l3_images`, `l3_math`, `l3_styles`, `l4_canvas`. (Domain features like `_preset_styles`, `_icons`, `_charts`, `_diagrams`, and `_smartarts` reside at package level).

### 3.3. Document and Image Builder (`_builder/`)
- Handles Markdown parsing, `drawlib` code block execution, HTML/PDF/Markdown compilation, image building, and cache management.

### 3.4. Command Line Interface (`_cli/`)
- Unified CLI entrypoint (`drawlib._cli.main:main`) and argument parser.

## 4. Dependency & Safety Rules
- **Layered Access**: Higher-level modules may depend on lower-level modules, but not vice versa.
- **Validation**: Style model attributes must be validated using guarded properties.
