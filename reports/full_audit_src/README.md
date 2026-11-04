# Drawlib Document Project

This directory contains multi-chapter specification or technical report documents compiled into static HTML, vector PDF, Markdown, and exported images using Drawlib.

---

## 1. Directory Structure

- `full_audit_src/`: Source Markdown chapters and drawing code (**Source of Truth**).
  - `drawlib.toml`: Project manifest (`[project]` metadata and `[i18n]` locale configuration).
  - `en/`: Markdown chapters for the default locale (add `<lang>/` directories and append to `langs` in `drawlib.toml` for multi-language builds):
    - `00_cover.md`: Document title/cover page.
    - `01_overview.md`: Overview chapter.
    - `02_design.md`: Technical design chapter.
  - `_assets/`: Shared image assets across locales (`favicon.png`, `linux.png`).
  - `build.sh`: Master build script to run standard builds (HTML, PDF, Markdown, Images).
  - `build_html.sh`: Fast HTML preview compiler.
  - `build_pdf.sh`: Print-ready vector PDF compiler.
  - `build_docx.sh`: On-demand editable MS Word (`.docx`) exporter.
  - `build_markdown.sh`: GitHub-ready Markdown compiler.
  - `build_image.sh`: Batch diagram image exporter.
  - `serve.sh`: Local preview server with live reloading.
  - `styles.py`: Global styles script (themes, styles, font presets; optional `<lang>/styles.py` override).
  - `utils.py`: Reusable drawing helper functions, macros, and project constants.
  - `style.css`: Document stylesheet (layout, typography, paged media rules).
  - `template.html`: Jinja2 HTML layout.
  - `README.md`: This customization guide.
- `full_audit_markdown/`: Generated Markdown files (`<lang>/...`).
- `full_audit_html/`: Generated HTML documents (`index.html`, `<lang>/index.html`).
- `full_audit_<lang>.pdf` (e.g. `full_audit_en.pdf`): Generated vector PDF document(s) per locale.
- `full_audit_<lang>.docx` (e.g. `full_audit_en.docx`): On-demand editable MS Word document(s) per locale.
- `full_audit_images/`: Generated diagram images.

---

## 2. Building Documents

### Using the Build Scripts
```bash
./build_html.sh       # Compile standalone HTML
./build_pdf.sh        # Compile vector PDF (<base>_<lang>.pdf)
./build_docx.sh       # Export editable MS Word (<base>_<lang>.docx, on-demand)
./build_markdown.sh   # Compile Markdown
./build_image.sh      # Export diagram images
./build.sh            # Run standard builds (HTML + PDF + Markdown + Images)
```

### Previewing
```bash
./serve.sh            # Start local live preview server
```
