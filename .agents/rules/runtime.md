---
trigger: always_on
---

# Runtime Environment Guidelines for drawlib

This document describes the runtime environment, Python versions, and command execution standards for the `drawlib` project.

## 1. Python Versions

- **Development Environment**: **Python 3.12**
  - The primary local development and CI quality check environment uses **Python 3.12** (managed via `uv`).
- **Supported Library Runtime**: **Python 3.11, 3.12, 3.13** (`>=3.11`)
  - Specified in `pyproject.toml` as `requires-python = ">=3.11"`.
  - The published library code (`src/drawlib/`) **must maintain strict compatibility with Python 3.11+**.
  - Do not introduce Python 3.12+-only syntax or standard library features into `src/drawlib/` without compatibility fallbacks.
  - Cross-version and cross-platform compatibility is verified in CI across Linux, Windows, and macOS for Python 3.11, 3.12, and 3.13.

## 2. Package Management
- **Tool**: Use `uv` for dependency management and environment isolation.
- **Environment**: Always rely on the project's virtual environment managed by `uv`.

## 3. Command Execution Standards
- **Python Execution**: Always execute scripts or modules via `uv run python` or `./dcli`.
- **Examples**:
  - `./dcli code-check all` or `uv run python -m drawlib`
  - `./dcli test all` or `./dcli test target <path_or_shortcut>`
  - `./dcli code-check lint` or `./dcli code-check type`
