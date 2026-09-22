---
trigger: always_on
---

# Architecture Guidelines for drawlib

This document describes the project structure and architectural principles of the `drawlib` project.

## 1. Project Root Structure
- `src/drawlib/`: The main source code directory.
  - `apis.py`: The global gateway re-exporting public symbols.
  - `core/`: Core drawing engine implementation details.
  - `doc_builder/`: Markdown AST parsing & document compiler module.
  - `cli/`: Unified command-line interface logic.
- `docs_src/`: Source of truth for documentation and technical guides written in Markdown.
- `docs/`: Generated Markdown documentation for GitHub repository browsing (do not edit directly).
- `docs_html/`: Generated static HTML site for web hosting (do not edit directly).
- `tests/`: Contains unit and integration tests.
- `tools/`: Project developer CLI (`tools/dcli/`) and maintenance scripts (`tools/scripts/`).
- `pyproject.toml`: Project metadata and tool configurations (Ruff, Pyright, uv).

## 2. Package Architecture
`drawlib` follows a flat, single-package architecture (Pattern A):
- Standard Python package layout (`src/drawlib/`).
- Package releases and versioning are managed via Semantic Versioning in PyPI/Git tags.
- Three major components reside under `src/drawlib/`: `core` (drawing engine), `doc_builder` (document compiler), and `cli` (command line interface).

## 3. Module Hierarchy (Internal Structure)

### 3.1. Public API (`apis.py`)
- Located at `src/drawlib/apis.py`.
- Acts as the main facade exporting symbols intended for end-users.
- Imports from `drawlib.core` and flattens the export namespace.

### 3.2. Core Implementation (`core/`)
The `core/` directory contains internal drawing logic and is not meant to be accessed directly by users.
- **Layered Structure**: `l1_core`, `l2_models`, `l2_types`, `l3_fonts`, `l3_styles`, `l4_theme`, `l5_canvas`, `l6_icons`, `l7_dutils`, `l7_smartarts`, `l7_umls`.

### 3.3. Document Builder (`doc_builder/`)
- Handles Markdown parsing, `drawlib` code block execution, and HTML/PDF/Markdown compilation (see `.agents/rules/docs.md` for full specifications and workflows).

### 3.4. Command Line Interface (`cli/`)
- Unified CLI entrypoint (`drawlib.cli.main:main`) and argument parser.

## 4. Dependency & Safety Rules
- **Layered Access**: Higher-level modules may depend on lower-level modules, but not vice versa.
- **Validation**: Style model attributes must be validated using guarded properties.
