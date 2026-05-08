# Architecture Guidelines for drawlib

This document describes the project structure and architectural principles of the `drawlib` project.

## 1. Project Root Structure
- `src/drawlib/`: The main source code directory.
- `tests/`: Contains unit and integration tests.
- `tasks/`: Automation scripts and configuration for development workflows (e.g., dependency management, building).
- `pyproject.toml`: Project metadata and tool configurations (Ruff, Pyright, uv).

## 2. Versioning Strategy
`drawlib` uses a versioned directory structure to manage library evolution while maintaining backward compatibility.

- **Version Directories**: Major versions or significant API iterations are placed in directories like `src/drawlib/v0_1/`, `src/drawlib/v0_2/`, etc.
- **Latest Version**: The highest version directory (currently `v0_2`) is considered the primary development target.
- **Top-level Entry Point**: `src/drawlib/apis.py` serves as the global gateway, re-exporting all public symbols from the latest version directory.
- **Deprecation**: Older version directories are kept for backward compatibility but are eventually deprecated. New features should only be added to the latest version.

## 3. Module Hierarchy (Internal Structure)
Each version directory (e.g., `v0_2/`) follows a strict layered architecture to separate public APIs from internal implementation.

### 3.1. Public API (`apis.py`)
- Located at `src/drawlib/v0_x/apis.py`.
- This file acts as the facade for the version. It exports only the symbols intended for end-users.
- It imports from the `private/` sub-packages and flattens the hierarchy for easier user access.

### 3.2. Implementation (`private/`)
The `private/` directory contains the actual logic and is not intended to be accessed directly by users.

- **`core/`**: Foundations of the library.
    - `model.py`: Style models (ShapeStyle, LineStyle, etc.) implemented as dataclasses.
    - `colors.py`, `fonts.py`, `theme.py`: Basic visual components.
- **`core_canvas/`**: The drawing engine.
    - `canvas.py`: Manages the drawing state and Matplotlib integration.
    - Implements basic primitives (line, rectangle, circle, text, etc.).
- **`validators/`**: Dedicated validation logic for user inputs and style attributes.
- **`dutil/`**: Low-level utilities, settings, and helper functions used across the version.
- **Feature Modules**:
    - `icons/`: Icon library integration (e.g., Phosphor icons).
    - `smartarts/`: Higher-level drawing components (e.g., flowcharts, diagrams).
    - `umls/`: Specialized UML diagram support.

## 4. Dependency Rules
- **Layered Access**: Higher-level modules (like `smartarts` or `umls`) may depend on lower-level modules (`core`, `core_canvas`), but not vice versa.
- **Private Access**: Code inside `private/` should avoid importing from other versions (e.g., `v0_2` should not depend on `v0_1`).
- **Validation**: All style model attributes must be validated using the logic in `private/validators/` via property setters.
