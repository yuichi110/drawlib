---
trigger: always_on
---

# Runtime Environment Guidelines for drawlib

This document describes the runtime environment and command execution standards for the `drawlib` project.

## 1. Package Management
- **Tool**: Use `uv` for dependency management and environment isolation.
- **Environment**: Always rely on the project's virtual environment managed by `uv`.

## 2. Python Execution
- **Command**: When executing Python scripts or commands, always use `uv run python`.
- **Example**: `uv run python tasks/scripts/my_script.py`
- **Testing**: Use `uv run pytest` or `task test` for running tests.
- **Linting/Formatting**: Use `uv run ruff` or `task check:lint`.
