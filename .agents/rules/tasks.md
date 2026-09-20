---
trigger: always_on
---

# Development CLI (dcli) for drawlib

Routine development tasks, such as linting, testing, document building, and publishing, are managed using the `./dcli` launcher script backed by Python + Typer + Rich (`tools/dcli/`). Always prefer using these predefined CLI toolsets to ensure consistency.

## Available Toolsets

Execute `./dcli` with no arguments to print all available toolsets:

```text
* assets:   Release asset management for GitHub Releases
  - ./dcli assets list
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
* test:     Test execution and coverage via pytest
  - ./dcli test all [--cov]
  - ./dcli test target <path>
  - ./dcli test cli
  - ./dcli test core / models / types / styles / fonts / theme / canvas / icons / smartarts / doc-builder
* docs:     Documentation generation and local preview
  - ./dcli docs build
  - ./dcli docs serve [-p PORT]
* gen:      Code generation utilities
  - ./dcli gen icon
* pypi:     PyPI publishing and version management
  - ./dcli pypi list-versions [--test-pypi]
  - ./dcli pypi latest [--test-pypi]
  - ./dcli pypi check-version [--allow-jump] [--test-pypi]
  - ./dcli pypi update-pyproject
  - ./dcli pypi publish [--allow-jump] [--test-pypi]
* dep:      Project dependency inspection and PyPI releases
  - ./dcli dep list
  - ./dcli dep releases <package> [--from YEAR]
* docker:   Docker test container management
  - ./dcli docker daemon-status / daemon-start / daemon-stop
  - ./dcli docker build-image --version <VER> [--python VER] [--repo pypi|test-pypi]
  - ./dcli docker list-images / prune-images
```

## Shell Autocompletion

Enable dynamic shell autocompletion and the `dcli` command alias in your current terminal session:

```bash
source ./dcli
```
