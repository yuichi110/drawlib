---
trigger: always_on
---

# Automation Tasks for drawlib

Routine development tasks, such as linting, testing, and publishing, are managed using the `task` command. Always prefer using these predefined tasks over manual commands to ensure consistency.

## Available Tasks

Below is the list of available tasks in the project:

```text
* default:                                      Print available tasks
* agent:gen:GEMINI.md:                          Aggregate all agent rules into a single GEMINI.md file
* check:default:                                Run all checks (lint, type, and docstring)      (aliases: check)
* check:docstring:                              Check if forbidden type aliases appear in @guarded function docstrings
* check:lines:                                  Count lines of code
* check:lint:                                   Run linter (ruff)
* check:type:                                   Run type checker (ty)
* check:type-ty:                                Run type checker (ty)
* dependency:list:                              List all dependencies in pyproject.toml
* dependency:releases:                          List available releases for a package
* docker:daemon:start:                          Start Docker Desktop app (macOS only)
* docker:daemon:status:                         Check Docker daemon status (macOS only)
* docker:daemon:stop:                           Quit Docker Desktop app (macOS only)
* docker:test-images:build:                     Build drawlib Docker image for testing
* docker:test-images:list:                      List all drawlib test images
* docker:test-images:prune:                     Remove all drawlib test images
* gen:code:icon:                                Generate icon phosphor code
* gen:code:theme-style:                         Generate theme style classes
* pypi-test:check-new-version:                  Check if the new version is valid compared to TestPyPI
* pypi-test:check-new-version:allow_jump:       Check if the new version is valid compared to TestPyPI
* pypi-test:get-latest-version:                 Get the latest version of drawlib from TestPyPI
* pypi-test:list-versions:                      List all versions of drawlib from TestPyPI
* pypi-test:publish:                            Publish the package to TestPyPI
* pypi-test:publish:allow_jump:                 Publish the package to TestPyPI - Allow Version Jump
* pypi-test:pyproject:update:                   Update pyproject.toml metadata from src/drawlib/__init__.py
* pypi:check-new-version:                       Check if the new version is valid compared to PyPI
* pypi:check-new-version:allow_jump:            Check if the new version is valid compared to PyPI
* pypi:get-latest-version:                      Get the latest version of drawlib from PyPI
* pypi:list-versions:                           List all versions of drawlib from PyPI
* pypi:publish:                                 Publish the package to PyPI (Production)
* pypi:publish:allow_jump:                      Publish the package to PyPI (Production) - Allow Version Jump
* pypi:pyproject:update:                        Update pyproject.toml metadata from src/drawlib/__init__.py
* pyproject:update:                             Update pyproject.toml metadata from src/drawlib/__init__.py
* setup:docker:install:                         Install Docker (macOS only)
* setup:docker:update:                          Update Docker (macOS only)
* setup:gemini-cli:install:                     Install gemini-cli (macOS only)
* setup:gemini-cli:update:                      Update gemini-cli (macOS only)
* setup:uv:install:                             Install uv package manager
* setup:uv:self-update:                         Update uv package manager to the latest version
* setup:uv:sync:                                Sync project dependencies using uv
* utest:all:                                    Run all version tests
* utest:dependency:matrix:                      Run all combinations of the test matrix
* utest:docker:default:                         Run unit tests in a Docker container      (aliases: utest:docker)
* utest:docker:docker:daemon:start:             Start Docker Desktop app (macOS only)
* utest:docker:docker:daemon:status:            Check Docker daemon status (macOS only)
* utest:docker:docker:daemon:stop:              Quit Docker Desktop app (macOS only)
* utest:docker:docker:test-images:build:        Build drawlib Docker image for testing
* utest:docker:docker:test-images:list:         List all drawlib test images
* utest:docker:docker:test-images:prune:        Remove all drawlib test images
* utest:v0.2:all:                               Run all tests for v0.2
* utest:v0.2:core:                              Run core tests for v0.2
* utest:v0.2:dsarts:                            Run dsarts tests for v0.2
* utest:v0.2:fonts:                             Run fonts tests for v0.2
* utest:v0.2:icons:                             Run icons tests for v0.2
* utest:v0.2:model:                             Run model tests for v0.2
* utest:v0.2:original:                          Run original tests for v0.2
* utest:v0.2:others:                            Run other tests for v0.2
* utest:v0.2:patches:                           Run patches tests for v0.2
* utest:v0.2:theme:                             Run theme tests for v0.2
```

## Usage
- Use `task <task_name>` to execute a specific task.
- Use `task --list` to see the current list of available tasks.
- If a task involves Python code, ensure the environment is synced with `task setup:uv:sync` if necessary.
