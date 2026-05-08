# Lint and Type Check Workflow

This document defines the workflow for ensuring code quality through linting and static type checking.

## 1. Overview
We use `ruff` for linting and formatting, and `pyright` for static type checking. All checks are integrated into the `task` runner.

## 2. Standard Workflow

### Step 1: Run Linter
Execute the following command to check for linting issues:
```bash
task check:lint
```
- **If errors are found**:
    - For auto-fixable issues, you can run: `uv run ruff check --fix src`
    - For non-fixable issues (e.g., missing docstrings, complex logic), manually correct the code according to the [Code Style Guide](file:///.agents/rules/code-style-guide.md).

### Step 2: Run Type Checker
Execute the following command to verify type hints:
```bash
task check:type
```
- This runs `pyright` on both `src/drawlib` and `tests`.
- **Note**: Ensure all public functions have complete type hints, as required by our style guide.

### Step 3: Final Verification
Before finishing a task or submitting a change, run both checks together to ensure a clean state.

## 3. Tool Commands Reference
If you need to run tools directly (e.g., for specific files), use these patterns:

| Tool | Command |
| :--- | :--- |
| **Ruff (Check)** | `uv run ruff check --preview <path>` |
| **Ruff (Fix)** | `uv run ruff check --fix --preview <path>` |
| **Ruff (Format)** | `uv run ruff format <path>` |
| **Pyright** | `uv run pyright <path>` |

## 4. When to Run
- **During Development**: Frequently check the file you are working on.
- **After Completion**: Run the full suite (`task check:lint` and `task check:type`) to ensure no regressions or side effects.
- **Pre-Commit**: AI assistants must verify that their changes pass these checks before considering a task "done".
