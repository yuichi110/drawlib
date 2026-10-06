---
trigger: model_decision
description: Testing Guidelines for drawlib
---

# Testing Guidelines for drawlib

This document defines the standards and best practices for writing tests in the `drawlib` project.

## 1. General Principles
- **Test Framework**: Use `pytest`.
- **Target Architecture**: Tests are located in `tests/` and mirror the package structure of `src/drawlib/`.
- **Isolation**: Tests should be isolated and not depend on external network or specific local file paths (unless in `tests/assets/`).
- **Reproducibility**: Use fixed seeds or constant values for any pseudo-random operations to ensure consistent results.

## 2. Test Structure and Organization
- **Top-Level Package Separation**:
  - `tests/drawlib/`: Mirrors `src/drawlib/` 1:1 for the published library package.
    - `tests/drawlib/_core/`: Mirrors `src/drawlib/_core/` (`l1_core/`, `l2_types/`, `l3_colors/`, `l3_external/`, `l3_fonts/`, `l3_images/`, `l3_math/`, `l3_styles/`, `l4_canvas/`).
    - Domain packages: `tests/drawlib/charts/`, `tests/drawlib/diagrams/`, `tests/drawlib/smartarts/`, `tests/drawlib/graph/`, `tests/drawlib/slide/`, `tests/drawlib/anim/`, `tests/drawlib/icons/`, `tests/drawlib/preset_styles/`.
    - Builders & CLI: `tests/drawlib/doc_builder/`, `tests/drawlib/cli/`, `tests/drawlib/http_server/`.
    - Release assets: `tests/drawlib/release_assets/`.
  - `tests/dcli/`: Mirrors `tools/dcli/` for internal developer tools and scripts.
- **File Names**: All test files must be prefixed with `test_` (e.g., `test_validator.py`, `test_bar_chart.py`).
- **Function Names**: All test functions must start with `test_` (e.g., `test_icon_style()`).
- **Conftest**: Use `conftest.py` for shared fixtures within root or subdirectories.

## 3. Writing Tests
- **Assertions**: Use standard Python `assert` statements.
- **Exception Testing**: Use `pytest.raises(ExceptionClass)` to verify that specific errors are raised for invalid inputs.
- **Data Comparison**: For style models, use `dataclasses.asdict()` to compare the state of objects against expected dictionaries.
- **Public API usage**: In domain and end-to-end tests, use public facades (`from drawlib import ...` or `from drawlib.shapes import ...`).

## 4. Specific Test Types
### 4.1. Model & Validation Tests
- Verify that dataclasses correctly store attributes.
- Verify that property setters correctly validate inputs and raise `ValueError` for invalid data.
- Test `copy()` and `merge()` methods for consistency and deep copying.

### 4.2. Drawing Tests (Functional)
- For functions that generate Matplotlib patches or shapes, verify that the resulting objects have the expected properties (coordinates, colors, z-order).
- Avoid checking the exact visual rendering pixel-by-pixel unless specifically required (e.g., regression testing for image output with reference answer images).

## 5. Mocking and Patching
- Use `unittest.mock` (or `pytest-mock` if preferred) to isolate components.
- Mock the Matplotlib backend or figure/axes objects when testing drawing logic without wanting to display a window.

## 6. Execution
- Run tests using `./dcli test`:
    - `./dcli test all`: Runs the entire test suite (`tests/` across both `drawlib` and `dcli`).
    - `./dcli test drawlib`: Runs all tests under `tests/drawlib/`.
    - `./dcli test dcli`: Runs tests under `tests/dcli/`.
    - `./dcli test target <path_or_shortcut>`: Runs a specific test file, directory, or target shortcut (e.g., `core`, `charts`, `diagrams`, `smartarts`, `graph`, `slide`, `anim`, `icons`, `canvas`, `types`, `styles`, `fonts`, `images`, `cli`, `doc-builder`, `preset-styles`).