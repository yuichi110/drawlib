---
trigger: model_decision
description: Documentation Projects and Authoring Guidelines for the drawlib repository
---

# Documentation Guidelines for drawlib

This document describes the documentation projects hosted in this repository and the mandatory workflow for authoring and updating them.

---

## 1. Documentation Projects in This Repository

All documentation, guides, slides, and README illustrations in this repository are standard Drawlib projects scaffolded via `drawlib init`:

| Build Target (`./dcli docs build <target>`) | Source Directory (`*_src/`) | Template Type (`drawlib init`) | Generated Outputs (Do NOT edit directly) | Description |
| :--- | :--- | :--- | :--- | :--- |
| **`site`** | `docs_src/` | `site` | `docs/`, `docs_html/`, `docs_images/` | Official multi-page documentation website & GitHub Markdown |
| **`quickstart`** | `quickstart_src/` | `doc` | `quickstart_html/`, `quickstart.pdf`, `quickstart_markdown/`, `quickstart_images/` | Linear quickstart guide & PDF |
| **`dogfooding`** | `drawlib-dogfooding_src/` | `doc` | `drawlib-dogfooding_html/`, `drawlib-dogfooding.pdf`, `drawlib-dogfooding_markdown/`, `drawlib-dogfooding_images/` | Dogfooding technical whitepaper (Japanese) |
| **`dogfooding-en`** | `drawlib-dogfooding-en_src/` | `doc` | `drawlib-dogfooding-en_html/`, `drawlib-dogfooding-en.pdf`, `drawlib-dogfooding-en_markdown/`, `drawlib-dogfooding-en_images/` | Dogfooding technical whitepaper (English) |
| **`slide`** | `slide_about_drawlib_src/` | `slide` | `slide_about_drawlib_html/`, `slide_about_drawlib.pdf` | 16:9 presentation slide deck (HTML & PDF) |
| **`readme`** | `readme_src/` | `image` | `readme_images/` | Standalone Python scripts generating illustrations for `README.md` |

- **Source of Truth**: Always edit files inside `<name>_src/` (and `build.sh` / `navbar.md` within it). Never manually edit generated output folders or PDFs.
- **Build & Preview**:
  ```bash
  ./dcli docs build <target>          # e.g. ./dcli docs build site (or --all)
  ./dcli docs serve <target> --check  # Verify links and HTML output headlessly
  ```

---

## 2. Follow `drawlib rules` & Style Guide

Because all documentation projects are built with `drawlib init`, always inspect and follow the embedded Drawlib rules before authoring content or diagrams:

```bash
uv run drawlib rules show project       # Project structure, navbar.md, code fence attributes
uv run drawlib rules show overview      # Coordinate space (origin (0,0) at bottom-left) & lifecycle
uv run drawlib rules show style-guide   # Visual design rules, typography, and color discipline
```

- **Strict Style Guide Compliance**:
  - **50%+ Neutral Baseline**: Ground 50% or more of diagram nodes in calm neutral styles (`Styles.Neutral`, `Styles.PrimaryNeutral`, `Styles.SecondaryNeutral`). Never create rainbow diagrams.
  - **Focal Hierarchy**: Reserve saturated fills (`Styles.PrimaryFlat`, `Styles.AccentFlat` with `text_style=Styles.WhiteBold`) strictly for 1–2 hero components.
  - **PascalCase Tokens**: Always import `from drawlib.styles import Colors, Styles`.
  - **Deterministic Code Blocks**: Always specify `file:<name>.png` and `caption:"..."` on every ````drawlib```` block in Markdown.

---

## 3. Visual Inspection & Self-Correction Loop (Mandatory)

Never consider a documentation or diagram update complete after only writing code. You **must** render the images, visually inspect them, and self-correct:

1. **Render with Grid (`-g`)**:
   ```bash
   # Preview a specific embedded diagram block or standalone script
   uv run drawlib show docs_src/path/to/page.md <diagram_file.png> -g -o .drawlib/scratch/preview.png
   ```
2. **Multimodal Visual Review (`view_file`)**:
   Open the generated image using `view_file` and verify:
   - No text clipping, overlapping labels, or overflowing boxes.
   - Balanced margins and proper alignment across coordinates.
   - Arrows and connectors attach cleanly to shape edges without crossing through unrelated nodes.
   - Strict adherence to the 50%+ neutral style guide and high text contrast.
3. **Self-Correct & Rebuild**:
   If any visual flaw is detected, adjust coordinates/styles, re-render, and re-inspect until clean, then run `./dcli docs build <target>` to update the project outputs.
