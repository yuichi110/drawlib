---
trigger: model_decision
description: Documentation Projects and Authoring Guidelines for the drawlib repository
---

# Documentation Guidelines for drawlib

This document describes the documentation projects hosted in this repository and the mandatory workflow for authoring and updating them.

---

## 1. Documentation Projects in This Repository

All documentation, guides, slides, and README illustrations in this repository are standard Drawlib projects scaffolded via `drawlib init`:

| Build Target (`./dcli docs build <target>`) | Source Directory (`docs/*_src/`) | Template Type (`drawlib init`) | Generated Outputs (Do NOT edit directly) | Description |
| :--- | :--- | :--- | :--- | :--- |
| **`site`** | `docs/docs_src/` | `site` | `docs/docs_markdown/`, `docs/docs_html/`, `docs/docs_images/` | Official multi-page documentation website & GitHub Markdown |
| **`quickstart`** | `docs/quickstart_src/` | `doc` | `docs/quickstart_html/`, `docs/quickstart.pdf`, `docs/quickstart_markdown/`, `docs/quickstart_images/` | Linear quickstart guide & PDF |
| **`dogfooding`** | `docs/drawlib-dogfooding_src/` | `doc` | `docs/drawlib-dogfooding_html/`, `docs/drawlib-dogfooding.pdf`, `docs/drawlib-dogfooding_markdown/`, `docs/drawlib-dogfooding_images/` | Dogfooding technical whitepaper (Japanese) |
| **`dogfooding-en`** | `docs/drawlib-dogfooding-en_src/` | `doc` | `docs/drawlib-dogfooding-en_html/`, `docs/drawlib-dogfooding-en.pdf`, `docs/drawlib-dogfooding-en_markdown/`, `docs/drawlib-dogfooding-en_images/` | Dogfooding technical whitepaper (English) |
| **`slide`** | `docs/slide_about_drawlib_src/` | `slide` | `docs/slide_about_drawlib_html/`, `docs/slide_about_drawlib.pdf`, `docs/slide_about_drawlib_images/` | 16:9 presentation slide deck (HTML & PDF) |
| **`readme`** | `docs/readme_src/` | `image` | `docs/readme_images/` | Standalone Python scripts generating illustrations for `README.md` |

- **Source of Truth**: Always edit files inside `docs/<name>_src/` (and `build.sh` / `navbar.md` within it). Never manually edit generated output folders or PDFs.
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
  - **Deterministic Code Blocks**: Always specify `file:<name>.png` (or `.webp` for animations) and `caption:"..."` on every ````drawlib```` block in Markdown.
  - **Code Visibility in `docs/docs_src/` (`show-code` / `fold-code`)**: Because `docs/docs_src/` is Drawlib's official reference documentation, never hide drawing code (never omit both `show-code` and `fold-code`). Use **`show-code`** for primary API tutorials and feature implementation examples, and use **`fold-code`** for Top Hero illustrations, conceptual overview diagrams, or multi-item catalog showcase banners.
  - **Top Hero Illustration Rule (Above-the-Fold `fold-code` Eye-Catcher)**:
    - Every page in `docs/docs_src/` (excluding `01_getting_started/release_notes.md`) **must** begin with a **`fold-code` Hero illustration** placed right at the top of the page (**Lines 6–15**, immediately after `# Page Title` and a 1–2 sentence introductory paragraph, **before** any `python`/`bash` code blocks, Markdown tables, or long bullet lists).
    - Because `show-code` renders the Python source block *above* the image in HTML, the 1st ````drawlib```` block on a page **must always use `fold-code`** so the rendered illustration is immediately visible above the fold without scrolling, with its source code expandable directly underneath (`▶ Source Code`).
    - **Eye-Catching Design with Icons & High-Level Components**: Because the Hero illustration serves as the visual eye-catcher for the page, **never build Hero diagrams out of plain `rectangle()` + `line()` + `text()` alone** (except on `02_drawing_primitives/` pages specifically documenting those primitives). Actively combine **standardized icons (`drawlib.icons.phosphor` / `gcp`)** and **high-level components (`SmartArts` such as `ChevronProcess`, `Cycle`, `BoxList`, `GridLayout`, `TreeNode`, `Table`, `SourceCode`, or `Diagrams`, `Graphs`, `Charts`)**.
    - **Hero Scope**: A Hero illustration should visually summarize the page's core concept, component variants, or architecture at a glance, and **does not need to serve as a detailed code tutorial** (detailed step-by-step tutorials belong in `## 1.`, `## 2.`, etc. using `show-code`).
  - **HTML Image Width & In-Image Typography Size Rules (No Tiny Images or Tiny Text)**:
    1. **Do Not Shrink HTML Images (`No 600px/650px Cap`)**: Omit narrow pixel widths (`500px`–`650px`) from ````drawlib```` code fence headers (use ```` ```drawlib fold-code center file:... ```` or `100%`) so the rendered illustration fills the `.drawlib-image` container (`~822px` in `site`, `~746px` in `doc`) without wasted side margins inside the card.
    2. **Do Not Make In-Image Text Too Small (`text_size >= 10.0`)**:
       - Drawlib fixes Matplotlib's figure width at `10.0 inches` (`720 pt`), so browser font size in CSS pixels is `text_size * (displayed_width_px / 720)`.
       - Keep canvas dimensions compact (`setup(width=100..125)`) with tight perimeter margins (3–6 units) so the diagram fills the canvas.
       - **Standard Node / Body Text**: Use **`text_size = 10.5` to `12.0`** (Drawlib default is `12.0`).
       - **Card Headers / Section Titles**: Use **`text_size = 12.0` to `14.0`**.
       - **Secondary Annotations / Subtitles**: **Minimum `text_size >= 9.5`–`10.0`**. **Never use `text_size < 9.5`** (ban `6.5`–`8.5`), and avoid `canvas.transform(scale < 0.8)` unless inner font sizes are scaled up proportionally to compensate.
  - **Minimum 2 Illustrations Per Page & No ASCII Art**:
    - Every documentation page in `docs/docs_src/` (excluding `01_getting_started/release_notes.md`) **must contain at least 2 `drawlib` illustrations** (`1` `fold-code` Top Hero + `>= 1` `show-code` tutorial or `fold-code` architectural/reference diagram).
    - **Never use ASCII art diagrams** (`+---+`, `--->`, `[Box]`) or **ASCII directory trees** (`├──`, `└──`) in documentation prose; always render workflows, coordinate geometry, and directory trees (`TreeNode`) using `drawlib`.

---

## 3. Visual Inspection & Browser HTML Self-Correction Loop (Mandatory)

Never consider a documentation or diagram update complete after only writing code or viewing the raw `.png` in isolation. You **must** render the images, verify geometry with `-g`, and **verify the rendered HTML page in a browser** to compare diagram text against the `16px` HTML body text:

1. **Render with Grid (`-g`)**:
   ```bash
   # Preview a specific embedded diagram block or standalone script
   uv run drawlib show docs/docs_src/path/to/page.md <diagram_file.png> -g -o .drawlib/scratch/preview.png
   ```
2. **Multimodal Visual Review (`view_file`)**:
   Open the generated image using `view_file` and verify:
   - No text clipping, overlapping labels, or overflowing boxes.
   - Tight, balanced perimeter margins (no excessive empty whitespace around the drawing).
   - Arrows and connectors attach cleanly to shape edges without crossing through unrelated nodes.
   - Strict adherence to the 50%+ neutral style guide, high text contrast, and readable `text_size >= 10.0`.
3. **Browser HTML Verification (Compare Against `16px` Body Text)**:
   - Build the HTML output (`./dcli docs build site --no-clean`) and inspect the rendered HTML page in a browser (or capture a `1280x900` headless Playwright screenshot of `docs/docs_html/.../*.html` and view it via `view_file`).
   - Verify that:
     - The image fills the `.drawlib-image` card cleanly without large empty side margins.
     - The text inside the illustration is clearly legible and visually balanced next to the surrounding `16px` HTML body text.
   - If the image or its internal text appears too small compared to the body text, reduce `setup(width=...)`, increase `text_size` (`10.5`–`13.0`), remove any narrow width cap on the ````drawlib```` fence, re-render, and re-verify in the browser.

