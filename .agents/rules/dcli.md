---
trigger: always_on
---

# Development CLI (dcli) for drawlib

All routine development operations—static analysis, testing, document building, code generation, release asset management, and PyPI publishing—are managed via `./dcli` (`tools/dcli/`, built with Python + Typer + Rich).

Always use `./dcli` instead of running raw tool commands manually.

---

## 1. Quick Overview & Shell Setup

Run `./dcli` with no arguments to display the summary table of all 7 toolsets:

```bash
./dcli                    # Display available toolsets table
source ./dcli             # Register 'dcli' alias and dynamic Tab autocompletion in current shell
```

| Toolset | Module (`tools/dcli/`) | Primary Purpose |
| :--- | :--- | :--- |
| **`code-check`** | `code_check/` | Code quality & static analysis (Ruff lint/format, Ty type check, docstring check, line count) |
| **`test`** | `test.py` | Unit & integration test execution via pytest + coverage + xdist parallelization |
| **`docs`** | `docs/` | Building documentation projects (`site`, `quickstart`, `dogfooding`, `slide`, `readme`) & preview server |
| **`codegen`** | `codegen/` | Code generation utilities for Phosphor and GCP icon Python bindings |
| **`release-assets`**| `release_assets/` | Building, verifying, uploading, and syncing font/icon archives on GitHub Releases |
| **`pypi`** | `pypi/` | Dependency auditing, version checks, `pyproject.toml` updates, and TestPyPI/PyPI publishing |
| **`docker`** | `docker.py` | Clean-room Linux container image building and testing for published releases |

---

## 2. Toolset Reference

### 2.1. `code-check` — Code Quality & Static Analysis
```bash
./dcli code-check all [--fix]       # Run lint, type, and docstring checks in sequence
./dcli code-check lint [--fix]      # Run Ruff linter & formatter on src/, tests/, tools/
./dcli code-check type              # Run Ty static type checker on src/drawlib, tests/, tools/
./dcli code-check docstring         # Verify @validate_call functions do not use internal type aliases in docstrings
./dcli code-check lines             # Count and display source and test code lines
```

### 2.2. `test` — Test Execution & Coverage
```bash
./dcli test all [--cov/--no-cov] [--cov-report] [--parallel/--no-parallel]
./dcli test drawlib [--cov/--no-cov] [--cov-report] [--parallel/--no-parallel]
./dcli test dcli [--cov/--no-cov]
./dcli test target <shortcut_or_path> [--cov] [--cov-report] [--parallel]
```
- **Available `<shortcut>` names for `./dcli test target`**:
  - Core & Engine: `core`, `types`, `styles`, `fonts`, `images`, `canvas`, `preset-styles`
  - Domain Modules: `icons`, `smartarts`, `charts`, `diagrams`, `graph`, `slide`, `anim`
  - Builders & CLI: `cli`, `doc-builder`, `drawlib`, `dcli`
  - Or pass any file/directory path directly (e.g. `./dcli test target tests/drawlib/shapes/test_basic.py`).

### 2.3. `docs` — Documentation Build & Preview Server
```bash
./dcli docs build [TARGET] [--all/-a] [--clean/--no-clean]
./dcli docs serve [TARGET] [--port/-p 8000] [--no-browser] [--skip-check] [--check]
```
- **Available `TARGET` names**:
  - `site` *(default)*: Main documentation site (`docs/docs_src/` -> `docs/docs_html/`, `docs/docs_markdown/`)
  - `quickstart`: Quickstart guide & PDF (`docs/quickstart_src/`)
  - `dogfooding`: Dogfooding whitepaper JP (`docs/drawlib-dogfooding_src/`)
  - `dogfooding-en`: Dogfooding whitepaper EN (`docs/drawlib-dogfooding-en_src/`)
  - `slide` (`slide_about_drawlib`): 16:9 presentation slide deck (`docs/slide_about_drawlib_src/`)
  - `readme`: Standalone README illustration scripts (`docs/readme_src/`)
  - `all`: Build all targets sequentially

### 2.4. `codegen` — Icon & Binding Code Generation
```bash
./dcli codegen icon-phosphor                 # Generate Phosphor icon enum/methods from phosphor_data.json
./dcli codegen icon-gcp [--output-dir DIR]   # Sanitize GCP icons and generate GCP icon bindings
```

### 2.5. `release-assets` — GitHub Release Asset Management
Manages external binary packages (fonts & icons) stored in `release_assets/<tag>/` and hosted on GitHub Releases:
```bash
./dcli release-assets list [--tag VER]
./dcli release-assets sync [--tag VER] [--check]
./dcli release-assets build [PACKAGE] [--tag VER] [--output-dir DIR]
./dcli release-assets remote [--tag VER] [--token TOKEN]
./dcli release-assets upload [PACKAGE] [--tag VER] [--force] [--dry-run] [--token TOKEN]
./dcli release-assets remove [PACKAGE] [--all] [--tag VER] [--yes] [--dry-run] [--token TOKEN]
```

### 2.6. `pypi` — Dependency & PyPI Release Management
```bash
./dcli pypi deps                                     # Show dependency tree and outdated packages
./dcli pypi dep-releases <package> [--from YEAR]     # Query PyPI release history & Python version requirements
./dcli pypi list-versions [--test-pypi]              # List all published drawlib versions
./dcli pypi latest [--test-pypi]                     # Show latest published version
./dcli pypi check-version [--allow-jump] [--test-pypi]
./dcli pypi update-pyproject                         # Sync README_PYPI.md and metadata for release
./dcli pypi publish [--allow-jump] [--test-pypi]     # Build and publish package to TestPyPI or PyPI
```

### 2.7. `docker` — Production Image Build & Clean-Room Container Testing
```bash
./dcli docker status                                 # Verify Docker CLI & daemon availability
./dcli docker build [--pdf] [--assets] [--full] [--python 3.12] [--pypi VER] [--tag TAG]
./dcli docker test [--pypi VER | --test-pypi VER] [--python 3.12]
./dcli docker list                                   # List drawlib & test-drawlib container images
./dcli docker prune                                  # Remove all drawlib & test-drawlib container images
```
- **`./dcli docker build` variants**:
  - Default (`drawlib:slim`): Minimal `drawlib` installation.
  - `--pdf` (`drawlib:pdf`): Includes Playwright & Chromium for PDF export.
  - `--assets` (`drawlib:assets`): Pre-downloads all font and icon packages (`drawlib cache download --all`).
  - `--full` (`drawlib:full`): Full offline/air-gapped image (`--pdf` + `--assets`).
- **`./dcli docker test` modes**:
  - Default (no flags): Builds local source into a clean container and runs `pytest tests/drawlib/`.
  - `--pypi <VER>` / `--test-pypi <VER>`: Installs the published package from PyPI/TestPyPI and runs `pytest tests/drawlib/`.
