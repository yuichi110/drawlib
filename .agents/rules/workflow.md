---
trigger: always_on
---

# Development Workflow & Lifecycle for drawlib

This repository is the main development repository for the `drawlib` library, and simultaneously serves as a **live dogfooding environment** where the repository's own documentation projects (`docs_src/`, `quickstart_src/`, `drawlib-dogfooding_src/`, `slide_src/`, `readme_src/`) test and validate `drawlib` in real-world scenarios.

---

## 1. Core Development & Dogfooding Loop

Whenever adding features, modifying drawing logic, or fixing bugs in `src/drawlib/`, follow this end-to-end lifecycle:

```text
1. Implement & Unit Test ──> 2. Code Check (code-check all) ──> 3. Update Docs & Rules (Dogfooding)
                                                                                 │
   6. Complete <── 5. Visual Review & Self-Repair Loop <── 4. Build Docs & Render Images
```

### Step 1: Planning, Implementation & Unit Tests
- **Design & Implementation Plans**: When creating or updating feature/architecture design plans in the repository, always place them under `.agents/plans/` (e.g., `.agents/plans/<feature_name>.md`). Do not create a root-level `plans/` directory.
- Respect the internal layer hierarchy (`l1_core` -> `l2_types` -> `l3_*` -> `l4_canvas` -> domain modules -> public facades).
- Write or update code in `src/drawlib/` (or `tools/dcli/`) and add unit tests in `tests/`.
- Run targeted unit tests:
  ```bash
  ./dcli test target <shortcut_or_path>
  ```

### Step 2: Code Quality Verification (Mandatory)
- Run the full static analysis suite and resolve all lint, type, and docstring issues:
  ```bash
  ./dcli code-check all
  ```

### Step 3: Dogfooding via Documentation & Rules Update
- If public APIs, parameters, styles, or visual behaviors change:
  1. Update embedded agent rules in `src/drawlib/_rules/` (`api.md`, `lib_*.md`, etc.).
  2. Update or add real usage examples in the repository's documentation sources (`docs_src/`, `quickstart_src/`, `drawlib-dogfooding_src/`, `slide_src/`, or `readme_src/`).

### Step 4: Build Documentation & Render Images
- Test your library changes against the documentation projects to verify that real-world builds succeed:
  ```bash
  ./dcli docs build site          # Or quickstart, dogfooding, slide, readme, --all
  ./dcli docs serve site --check  # Verify links and HTML integrity
  ```
- Or render specific diagrams with the coordinate grid (`-g`) for close inspection:
  ```bash
  uv run drawlib show docs_src/path/to/page.md <diagram.png> -g -o .drawlib/scratch/preview.png
  ```

### Step 5: Visual Inspection & Self-Healing Iteration
- **Inspect Output Images (`view_file`)**: Always visually inspect the newly rendered images using `view_file`. Unit tests alone cannot catch visual regressions.
- **Check for Visual Defects**:
  - Text clipping, overlapping labels, or misaligned arrowheads.
  - Unbalanced margins, cramped layouts, or awkward spacing.
  - Style guide violations (ensure 50%+ neutral baseline, high text contrast).
- **Self-Heal & Iterate**: If the rendered illustration looks broken or suboptimal, fix either the library rendering logic (`src/drawlib/`) or the diagram code (`*_src/`), re-render, and re-inspect until the visual output is clean.

---

## 2. Assets & Code Generation Lifecycle

When updating icon sets, fonts, or external binary assets:

1. **Code Generation**:
   ```bash
   ./dcli codegen icon-phosphor
   ./dcli codegen icon-gcp
   ```
2. **Asset Archiving & Sync**:
   ```bash
   ./dcli release-assets build
   ./dcli release-assets upload --dry-run
   ./dcli release-assets sync --check
   ```

---

## 3. Release & Publishing Lifecycle

When preparing a new release version of `drawlib`:

1. **Dependency & Version Audit**:
   ```bash
   ./dcli pypi deps
   ./dcli pypi check-version
   ```
2. **Full Regression & Dogfooding Build**:
   ```bash
   ./dcli code-check all
   ./dcli test all
   ./dcli docs build --all
   ```
3. **Publish & Clean-Room Verification**:
   ```bash
   ./dcli pypi publish --test-pypi
   ./dcli docker test --test-pypi <VER>
   ./dcli pypi publish
   ./dcli docker test --pypi <VER>
   ```
