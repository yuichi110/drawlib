---
trigger: model_decision
description: Documentation Projects and Authoring Guidelines for the drawlib repository
---

# Documentation Guidelines for drawlib

This document describes the documentation projects hosted in this repository and the mandatory workflow for authoring and updating them.

---

## 1. Documentation Projects in This Repository

All documentation, guides, slides, and README illustrations in this repository are standard Drawlib projects scaffolded via `drawlib init project`:

| Build Target (`./dcli docs build <target>`) | Source Directory (`docs/*_src/`) | Template Type (`drawlib init project`) | Generated Outputs (Do NOT edit directly) | Description |
| :--- | :--- | :--- | :--- | :--- |
| **`site`** | `docs/docs_src/` (`drawlib.toml`: `en/`, `ja/`) | `site` | `docs/docs_markdown/`, `docs/docs_html/`, `docs/docs_images/` | Official multi-language (`en`/`ja`) documentation website & GitHub Markdown |
| **`architecture`** | `docs/architecture_src/` (`drawlib.toml`: `en/`) | `site` | `docs/architecture_markdown/`, `docs/architecture_html/`, `docs/architecture_images/` | Software architecture specification site |
| **`quickstart`** | `docs/quickstart_src/` (`drawlib.toml`: `en/`) | `doc` | `docs/quickstart_html/`, `docs/quickstart_en.pdf`, `docs/quickstart_markdown/`, `docs/quickstart_images/` | Linear quickstart guide & PDF |
| **`dogfooding`** | `docs/drawlib-dogfooding_src/` (`drawlib.toml`: `en/`, `ja/`) | `doc` | `docs/drawlib-dogfooding_html/`, `docs/drawlib-dogfooding_en.pdf`, `docs/drawlib-dogfooding_ja.pdf`, `docs/drawlib-dogfooding_markdown/`, `docs/drawlib-dogfooding_images/` | Bilingual (`en`/`ja`) Dogfooding technical whitepaper |
| **`slide`** | `docs/slide_about_drawlib_src/` (`drawlib.toml`: `en/`) | `slide` | `docs/slide_about_drawlib_html/`, `docs/slide_about_drawlib_en.pdf`, `docs/slide_about_drawlib_images/` | 16:9 presentation slide deck (About Drawlib) |
| **`slide-ddos`** | `docs/slide_ddos_incident_response_src/` (`drawlib.toml`: `en/`) | `slide` | `docs/slide_ddos_incident_response_html/`, `docs/slide_ddos_incident_response_en.pdf`, `docs/slide_ddos_incident_response_images/` | 16:9 presentation slide deck (DDoS Incident Response) |
| **`readme`** | `docs/readme_src/` | `images` | `docs/readme_images/` | Standalone Python scripts generating illustrations for `README.md` |
| **`logo`** | `docs/logo_src/` | `images` | `docs/logo_images/` | Drawlib brand logo & favicon asset generator scripts |
| **`ogp`** | `docs/ogp_src/` | `images` | `docs/ogp_images/` | GitHub Social Preview & OGP banner generator scripts (`1280×640`) |

- **Source of Truth**: Always edit files inside `docs/<name>_src/` (and `drawlib.toml`, `build.sh`, `<lang>/navbar.md` within it). Never manually edit generated output folders or PDFs.
- **Unified `<src_dir>/<lang>/` Locale Architecture (`doc`, `site`, `slide`)**: Every `doc`, `site`, and `slide` project declares `[i18n]` (`default_lang`, `langs`, optional `[i18n.labels]`; no `[project].lang`) in `drawlib.toml` and places Markdown sources inside `<src_dir>/<lang>/` (even single-language `en/` projects), emitting locale-suffixed document/deck deliverables (`<base>_<lang>.pdf`, `<base>_<lang>.docx`, `<base>_<lang>.pptx`). Standalone `images` projects (`readme_src/`, `logo_src/`, `ogp_src/`) remain flat (`*.py`) with `lang = "en"` under `[project]`.
- **Multi-Language Parity in `docs/docs_src/` & `docs/drawlib-dogfooding_src/` (`en/` & `ja/`)**: Multi-language projects declare `langs = ["en", "ja"]` with shared `styles.py` (optional per-locale `<lang>/styles.py` override), `utils.py`, `_assets/`, `style.css`, and `template.html` at root and localized Markdown trees in `en/` and `ja/`. Whenever adding, renaming, or editing a page/chapter or `drawlib` block in `en/`, apply the corresponding update to `ja/` so file paths, `navbar.md` structure (for `site`), `H1`–`H3` skeleton sequence, and `drawlib` code blocks remain 100% in parity (`caption="..."` and prose localized per language; localized diagram labels use `file=<stem>_<lang>.png`).
- **Build & Preview**:
  ```bash
  ./dcli docs build <target>          # e.g. ./dcli docs build site (or --all)
  ./dcli docs serve <target> --check  # Verify links and HTML output headlessly
  ```

---

## 2. Follow `drawlib rules` & Style Guide

Because all documentation projects are built with `drawlib init project`, always inspect and follow the embedded Drawlib rules before authoring content or diagrams:

```bash
uv run drawlib rules show project-overview # Project structure, drawlib.toml, navbar.md, code fence attributes
uv run drawlib rules show overview         # Coordinate space (origin (0,0) at bottom-left) & lifecycle
uv run drawlib rules show style-guide      # Visual design rules, typography, and color discipline
```

- **Strict Style Guide Compliance**:
  - **50%+ Neutral Baseline**: Ground 50% or more of diagram nodes in calm neutral styles (`Styles.Neutral`, `Styles.PrimaryNeutral`, `Styles.SecondaryNeutral`). Never create rainbow diagrams.
  - **Focal Hierarchy**: Reserve saturated fills (`Styles.PrimaryFlat`, `Styles.AccentFlat` with `text_style=Styles.WhiteBold`) strictly for 1–2 hero components.
  - **PascalCase Tokens**: Always import `from drawlib.styles import Colors, Styles`.
  - **Deterministic Code Blocks**: Always specify `file=<name>.png` (or `.webp` for animations) and `caption="..."` on every ````drawlib```` block in Markdown.
  - **Code Visibility in `docs/docs_src/` (`code=show` / `code=fold` / Animation GitHub Link)**:
    - **Static Diagrams**: Use **`code=show`** for primary API tutorials and feature implementation examples, and use **`code=fold`** for static Top Hero illustrations (~60 lines), conceptual overview diagrams, or multi-item catalog showcase banners.
    - **Multi-Frame `Animation` Blocks Outside `08_animations/`**: Because multi-frame `Animation(...)` scripts (e.g. Top Hero animations and Section 1 `*_tour.png` parameter tours, ~250–1,150 lines) bloat HTML size and dilute page SEO even inside `<details>`, **omit `code=fold` / `code=show`** on `Animation(...)` fences outside `08_animations/` and place a `<div class="drawlib-source-link">` link to the GitHub `.md` source (`en/` or `ja/`) immediately below the fence. In `08_animations/` (which teaches the animation API directly), keep `code=fold` / `code=show` as usual.
  - **Top Hero Illustration Rule (Above-the-Fold Eye-Catcher)**:
    - Every page in `docs/docs_src/` (excluding `01_getting_started/release_notes.md`) **must** begin with a **Hero illustration** placed right at the top of the page (**Lines 6–15**, immediately after `# Page Title` and a 1–2 sentence introductory paragraph, **before** any `python`/`bash` code blocks, Markdown tables, or long bullet lists).
    - Because `code=show` renders the Python source block *above* the image in HTML, the 1st ````drawlib```` block on a page **must never use `code=show`**: use **`code=fold`** for static Hero diagrams so the illustration is immediately visible above the fold (`▶ Source Code` underneath), or omit `code=` + add `<div class="drawlib-source-link">` if the Hero is a multi-frame `Animation` outside `08_animations/`.
    - **Eye-Catching Design with Icons & High-Level Components**: Because the Hero illustration serves as the visual eye-catcher for the page, **never build Hero diagrams out of plain `rectangle()` + `line()` + `text()` alone** (except on `02_drawing_primitives/` pages specifically documenting those primitives). Actively combine **standardized icons (`drawlib.icons.phosphor` / `gcp`)** and **high-level components (`SmartArts` such as `ChevronProcess`, `Cycle`, `BoxList`, `GridLayout`, `TreeNode`, `Table`, `SourceCode`, or `Diagrams`, `Graphs`, `Charts`)**.
    - **Hero Scope**: A Hero illustration should visually summarize the page's core concept, component variants, or architecture at a glance, and **does not need to serve as a detailed code tutorial** (detailed step-by-step tutorials belong in `## 1.`, `## 2.`, etc. using `code=show`).
  - **HTML Image Width & In-Image Typography Size Rules (No Tiny Images or Tiny Text)**:
    1. **Do Not Shrink HTML Images (`No 600px/650px Cap`)**: Omit narrow pixel widths (`width=500px`–`width=650px`) from ````drawlib```` code fence headers (use ```` ```drawlib code=fold align=center file=... ```` or `width=100%`) so the rendered illustration fills the `.drawlib-image` container (`~822px` in `site`, `~746px` in `doc`) without wasted side margins inside the card.
    2. **Do Not Make In-Image Text Too Small (`text_size >= 10.0`)**:
       - Drawlib fixes Matplotlib's figure width at `10.0 inches` (`720 pt`), so browser font size in CSS pixels is `text_size * (displayed_width_px / 720)`.
       - Keep canvas dimensions compact (`setup(width=100..125)`) with tight perimeter margins (3–6 units) so the diagram fills the canvas.
       - **Standard Node / Body Text**: Use **`text_size = 10.5` to `12.0`** (Drawlib default is `12.0`).
       - **Card Headers / Section Titles**: Use **`text_size = 12.0` to `14.0`**.
       - **Secondary Annotations / Subtitles**: **Minimum `text_size >= 9.5`–`10.0`**. **Never use `text_size < 9.5`** (ban `6.5`–`8.5`), and avoid `canvas.transform(scale < 0.8)` unless inner font sizes are scaled up proportionally to compensate.
  - **No Absolute Paths or `file://` URLs in Documentation (Relative Links Only)**:
    - **Never** write local filesystem absolute paths (e.g. `/usr/...`, `/home/...`, `/Users/...`, `C:\...`) or `file:///` URLs inside documentation Markdown source files (`docs/*_src/**/*.md`). All links must use relative paths (e.g. `../08_doc_builder_and_cli/customization.md` or `../../.agents/rules/drawlib.md`) or inline code format (e.g. `` `drawlib.md` (`.agents/rules/drawlib.md`) ``).
    - **Distinction from Agent Chat**: While the AI assistant uses `file:///` links when conversing with the user in chat responses for clickable IDE navigation, repository documentation files published on the web or GitHub must **never** contain `file:///` or machine-specific absolute paths.
    - Violations are automatically caught and will fail the build (`drawlib build` / `validate_markdown_links`).
  - **Unreleased / Upcoming Features Notice (`Note (Upcoming in vX.Y.Z)`)**:
    - **During Development (Before Release)**: When documenting a new module, component, or feature that is currently in development (e.g. `0.3.1.dev1` in `pyproject.toml`) and not yet published in the latest stable PyPI release, add a blockquote callout at the top of the feature page (and an inline `*(Upcoming in vX.Y.Z)*` badge in overview/index tables):
      ```markdown
      > **Note (Upcoming in vX.Y.Z):** `<module_or_feature>` is scheduled for the upcoming **vX.Y.Z** release and is not yet included in the `vA.B.C` package on PyPI.
      ```
    - **At Release Time (Before Publishing `vX.Y.Z`)**: When preparing the official `vX.Y.Z` release (`pyproject.toml` bumped to `X.Y.Z`), **remove** all `> **Note (Upcoming in vX.Y.Z):**` callouts and `*(Upcoming in vX.Y.Z)*` badges across `docs/*_src/`, move the feature summary into `01_getting_started/release_notes.md`, and rebuild the documentation (`./dcli docs build --all`).

---

## 3. Visual Inspection & Browser HTML Self-Correction Loop (Mandatory)

Never consider a documentation or diagram update complete after only writing code or viewing the raw `.png` in isolation. You **must** render the images, verify geometry with `-g`, and **verify the rendered HTML page in a browser** to compare diagram text against the `16px` HTML body text:

1. **Render with Grid (`-g`)**:
   ```bash
   # Preview a specific embedded diagram block or standalone script
   uv run drawlib show docs/docs_src/en/path/to/page.md <diagram_file.png> -g -o .drawlib/scratch/preview.png
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

