---
trigger: always_on
---

# Runtime Environment Guidelines for drawlib

This document describes the runtime environment and command execution standards for the `drawlib` project.

## 1. Package Management
- **Tool**: Use `uv` for dependency management and environment isolation.
- **Environment**: Always rely on the project's virtual environment managed by `uv`.

## 2. Python Execution
- **Command**: When executing Python scripts or commands, always use `uv run python` or `./dcli`.
- **Example**: `uv run python tools/scripts/my_script.py`
- **Testing**: Use `./dcli test all` or `./dcli test <target>`.
- **Linting/Formatting**: Use `./dcli check lint` or `./dcli check all`.
