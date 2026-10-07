# Developer Guide for drawlib

This document provides essential setup instructions and workflows for developers working on the `drawlib` codebase.

---

## 1. Prerequisites & Environment Setup

`drawlib` targets **Python 3.11+** and relies on [`uv`](https://github.com/astral-sh/uv) for fast, reproducible dependency management and environment isolation.

```bash
# 1. Clone the repository
git clone https://github.com/yuichi110/drawlib.git
cd drawlib

# 2. Install dependencies into virtual environment
uv sync

# 3. (Recommended) Register shell autocompletion and the `dcli` command alias
source ./dcli
```

*(Optional: [Docker](https://www.docker.com/) is only required if you plan to build clean-room verification images for release packages).*

---

## 2. Daily Development Workflow (`./dcli`)

All routine development operations—linting, static analysis, testing, document building, and publishing—are orchestrated through the unified developer CLI `./dcli`:

### Code Quality & Static Analysis
```bash
./dcli code-check all        # Run Ruff linter/formatter, Ty static type checker, and docstring checks
./dcli code-check lint --fix # Automatically fix autofixable Ruff lint issues
./dcli code-check type       # Run Ty static type checker only
./dcli code-check docstring  # Validate public docstring type annotation rules
./dcli code-check lines      # Print source and test code line counts
```

### Testing via Pytest
```bash
./dcli test all           # Run complete test suite with coverage and parallel workers
./dcli test drawlib       # Run unit and integration tests for drawlib package
./dcli test dcli          # Run test suite for dcli developer CLI tools
./dcli test target <name> # Run targeting a module shortcut (e.g. canvas, smartarts, core) or path
```

### Documentation & Preview
```bash
./dcli docs build         # Build documentation website (docs/docs_src -> docs/docs_html & docs/docs_markdown)
./dcli docs serve         # Launch local preview server for documentation website
```

---

## 3. Detailed Specifications & AI Pair Programming

In `drawlib`, detailed technical rules and tool specifications are centralized inside [`.agents/rules/`](../.agents/rules/) as **Living Documentation (Single Source of Truth)**.

### Ask the AI Agent
When working with an AI coding assistant (Antigravity, Gemini, Claude, etc.), the agent automatically reads and enforces these rules. You don't need to memorize every option or flag—simply ask your AI agent:
- *"Which dcli command should I run to build and test release assets?"*
- *"How do I add a new shape primitive following drawlib's layer architecture?"*
- *"Run checks and tests on the changes."*

### Specification References
If you prefer browsing the rule specifications directly:
- **Developer CLI (`dcli`)**: [`.agents/rules/dcli.md`](../.agents/rules/dcli.md) — Exhaustive command reference for `code-check`, `codegen`, `docker`, `docs`, `pypi`, `release-assets`, and `test`.
- **Development Workflow**: [`.agents/rules/workflow.md`](../.agents/rules/workflow.md) — Lifecycles for code changes, doc sync, asset management, and releases.
- **System Architecture**: [`.agents/rules/architecture.md`](../.agents/rules/architecture.md) — Package hierarchy, public facades, and internal layered engine (`l1` ~ `l4`).
- **Coding & Style Guidelines**: [`.agents/rules/code-style-guide.md`](../.agents/rules/code-style-guide.md) — Python 3.11+ standards, naming conventions, type hints, and docstrings.
- **Testing Standards**: [`.agents/rules/testing.md`](../.agents/rules/testing.md) — Pytest fixtures, naming conventions, and mock standards.
- **Documentation Authoring**: [`.agents/rules/docs.md`](../.agents/rules/docs.md) — Writing and building repository docs (`docs/`, `navbar.md`, `./dcli docs`).
- **Drawlib Diagramming Instructions**: [`.agents/rules/drawlib.md`](../.agents/rules/drawlib.md) — AI agent instructions for creating architectural illustrations as code.
- **Runtime Environment**: [`.agents/rules/runtime.md`](../.agents/rules/runtime.md) — Python versions, package management rules, and execution standards.

---

## 4. Repository Structure Overview

```text
drawlib/
├── src/drawlib/        # Main library source code (public facades & _core engine)
├── tests/              # Test suite (tests/drawlib and tests/dcli)
├── tools/dcli/         # Developer CLI implementation (Python + Typer + Rich)
├── dcli                # Shell launcher & autocompletion wrapper
├── docs/               # Documentation projects (*_src/), outputs, README_DEV.md & README_PYPI.md
├── release_assets/     # Font and icon asset source files for GitHub Releases
├── .agents/rules/      # Living developer guidelines and AI instructions
└── pyproject.toml      # Project metadata, dependencies, and tool configs
```
