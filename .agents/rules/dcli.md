---
trigger: model_decision
description: dcli commands for development (testing, building doc, pypi management etc.)
---

# Development CLI (dcli) for drawlib

Routine development tasks, such as linting, testing, document building, and publishing, are managed using the `./dcli` launcher script backed by Python + Typer + Rich (`tools/dcli/`). Always prefer using these predefined CLI toolsets to ensure consistency.

## Available Toolsets

Execute `./dcli` with no arguments to print all available toolsets:

```text
* assets:   Release asset management for GitHub Releases
  - ./dcli assets list
  - ./dcli assets sync [--tag VER] [--check]
  - ./dcli assets build [PACKAGE] [--tag VER]
  - ./dcli assets remote [--tag VER]
  - ./dcli assets upload [PACKAGE] [--tag VER] [--force] [--dry-run]
  - ./dcli assets remove [PACKAGE] [--all] [--tag VER] [--yes] [--dry-run]
* check:    Code quality and static analysis (Ruff, Ty, docstrings)
  - ./dcli check lint [--fix]
  - ./dcli check type
  - ./dcli check docstring
  - ./dcli check lines
  - ./dcli check all
* codegen:  Code generation utilities for icons and bindings
  - ./dcli codegen icon-phosphor
  - ./dcli codegen icon-gcp [--output-dir DIR]
* docker:   Docker test container management
  - ./dcli docker status
  - ./dcli docker build-image --version <VER> [--python VER] [--repo pypi|test-pypi]
  - ./dcli docker list-images / prune-images
* docs:     Documentation generation and local preview
  - ./dcli docs build [TARGET] [--all] [--clean]
  - ./dcli docs serve [TARGET] [-p PORT]
* pypi:     PyPI publishing, version verification, and dependency management
  - ./dcli pypi deps
  - ./dcli pypi dep-releases <package> [--from YEAR]
  - ./dcli pypi list-versions [--test-pypi]
  - ./dcli pypi latest [--test-pypi]
  - ./dcli pypi check-version [--allow-jump] [--test-pypi]
  - ./dcli pypi update-pyproject
  - ./dcli pypi publish [--allow-jump] [--test-pypi]
* test:     Test execution and coverage via pytest
  - ./dcli test all [--cov] [--parallel]
  - ./dcli test drawlib
  - ./dcli test dcli
  - ./dcli test target <path_or_shortcut> (shortcuts: canvas, smartarts, core, etc.)
```

## Shell Autocompletion

Enable dynamic shell autocompletion and the `dcli` command alias in your current terminal session:

```bash
source ./dcli
```