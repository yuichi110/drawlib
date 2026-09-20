---
description: Lint and Type Check
---

# Lint and Type Check Workflow

This document defines the workflow for ensuring code quality through linting and static type checking.

## 1. Overview
We use `ruff` for linting and formatting, and `ty` for static type checking. All checks are integrated into `./dcli check`.

## 2. Standard Workflow

### Step 1: Run All Checks
Execute the following command to check linting, types, and docstrings together:
```bash
./dcli check all
```

### Step 2: Individual Checks
- **Linter**:
  ```bash
  ./dcli check lint
  # Or with automatic fixes:
  ./dcli check lint --fix
  ```
- **Type Checker**:
  ```bash
  ./dcli check type
  ```
- **Docstring Validator**:
  ```bash
  ./dcli check docstring
  ```

## 3. Tool Commands Reference
If you need to run tools directly for specific files or targets:

| Tool | Command |
| :--- | :--- |
| **Ruff (Check)** | `uv run ruff check --preview <path>` |
| **Ruff (Fix)** | `uv run ruff check --fix --preview <path>` |
| **Ruff (Format)** | `uv run ruff format <path>` |
| **Ty** | `uv run ty check <path>` |

## 4. When to Run
- **During Development**: Frequently check the file you are working on.
- **After Completion**: Run the full suite (`./dcli check all`) to ensure no regressions or side effects.
- **Pre-Commit**: AI assistants must verify that their changes pass `./dcli check all` before considering a task "done".
