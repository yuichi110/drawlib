=======================

# Release Notes



# Version 0.3.0

## Release date: 2026/09/21

## New features

- **Modern Flat Package Architecture**:
  - Refactored library layout from legacy version-namespaced structure to standard flat package (`drawlib`).
  - Unified public interface via `drawlib.apis` facade.
- **Built-in Document Builder**:
  - Added native Markdown / HTML document compiler (`drawlib doc-builder` and `build_document()`).
  - Automatically compiles markdown with `drawlib` code blocks into responsive HTML, rendered Markdown, or PDF.
- **ER Diagrams (`drawlib.diagrams.er`)**:
  - Declarative Entity-Relationship diagrams with full support for IE (Crow's Foot) notation.
  - Automatic right-angled orthogonal routing, column-level anchoring, and custom styling.
- **Headless PDF Export**:
  - PDF generation uses existing system Chromium-based browsers (Chrome, Chromium, Edge) without requiring Playwright.
- **On-Demand Release Assets**:
  - Assets such as icon sets and fonts are downloaded dynamically from GitHub Releases (`v0.3`), significantly reducing the PyPI package footprint.
- **Unified Developer CLI (`dcli`)**:
  - Integrated CLI tooling for linting (`ruff`), type checking (`ty`), asset management, and documentation builds.

## Requirements & Breaking changes

- Python >= 3.11 is now required.
- Package modules are directly accessible (e.g. `drawlib.canvas`, `drawlib.shapes`, `drawlib.smartarts`).
- The legacy `dsart` facade is removed in favor of direct imports from `drawlib.smartarts` (e.g., `from drawlib.smartarts import Table, SourceCode, bubblespeech`).



# Version 0.2.3



## Release data: 2024/09/08



## Commit: `4cc6e6e <https://github.com/yuichi110/drawlib/commit/4cc6e6ef2a72baeaf7e5405988d20f551e2eae3a>`_



## New features


Adding shape arrow functions.

- `arrow_polyline()`
- `arrow_l()`
- `arrow_u()`
- `arrow_arc()`

Adding smart arts.

- `dsart.BoxList`
- `dsart.BulletPoints`
- `dsart.GridLayout`
- `dsart.Pyramid`
- `dsart.Table`
- `dsart.Tree`

Adding style model attribute.

- `ShapeTextStyle.xy_abs_shift`



## Breaking changes


Change arg names 

- From `from_angle` to `angle_start`
- From `to_angle` to `angle_end`

At these functions.

- `arc()`
- `fan()`
- `wedge()`

Change arg names at function `dsart.bubblespeech()`.

- From `tail_from_ratio` to `tail_start_ratio`
- From `tail_to_ratio` to `tail_end_ratio`


# 0.2.2



## Release data: 2024/07/02



## Commit: `fa1d90a <https://github.com/yuichi110/drawlib/commit/fa1d90a4a45fb3edab2cbafddfa04ef23d6a5691>`_


First release of Drawlib `0.2`.

---

<p align="center"><em>© 2026 drawlib by Yuichi Ito. Released under the Apache 2.0 License.</em></p>
