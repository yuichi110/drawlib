# Drawlib Document Project

This directory contains multi-chapter specification or technical report documents compiled into static HTML, vector PDF, Markdown, and exported images using Drawlib.

---

## 1. Directory Structure

- `__SRC_DIR__/`: Source Markdown chapters and drawing code (**Source of Truth**).
  - `build.sh`: Master build script to run all builds.
  - `build_html.sh`: Fast HTML preview compiler.
  - `build_pdf.sh`: Print-ready vector PDF compiler.
  - `build_markdown.sh`: GitHub-ready Markdown compiler.
  - `build_image.sh`: Batch diagram image exporter.
  - `serve.sh`: Local preview server with live reloading.
  - `styles.py`: Global styles script (themes, styles, font presets).
  - `utils.py`: Reusable drawing helper functions, macros, and project constants.
  - `style.css`: Document stylesheet (layout, typography, paged media rules).
  - `template.html`: Jinja2 HTML layout.
  - `README.md`: This customization guide.
  - `00_cover.md`: Document title/cover page.
  - `01_overview.md`: Overview chapter.
  - `02_design.md`: Technical design chapter.
- `__OUT_MARKDOWN_DIR__/`: Generated Markdown files.
- `__OUT_HTML_DIR__/`: Generated HTML documents.
- `__OUT_PDF__`: Generated PDF document.
- `__OUT_IMAGES_DIR__/`: Generated diagram images.

---

## 2. Building Documents

### Using the Build Scripts
```bash
./build_html.sh       # Compile standalone HTML
./build_pdf.sh        # Compile vector PDF
./build_markdown.sh   # Compile Markdown
./build_image.sh      # Export diagram images
./build.sh            # Run all builds
```

### Previewing
```bash
./serve.sh            # Start local live preview server
```
