# Drawlib Quickstart Document Project

This directory contains multi-chapter specification and tutorial documents compiled into static HTML, vector PDF, Markdown, and exported images using Drawlib (with optional editable MS Word `.docx` export).

---

## 1. Directory Structure

- `quickstart_src/`: Source Markdown chapters and drawing code (**Source of Truth**).
  - `drawlib.toml`: Unified project manifest (`type = "doc"`, `style = "google"`, `[i18n]` `default_lang = "en"`, `langs = ["en"]`).
  - `en/`: English tutorial and guide chapters (`00-cover.md` ... `15-best_practices.md`).
  - `_assets/`: Shared image assets across locales.
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
- `quickstart_markdown/`: Generated Markdown documentation (`en/`, `images/`).
- `quickstart_html/`: Generated standalone HTML documents (`index.html`, `en/index.html`).
- `quickstart_en.pdf`: Generated vector PDF document.
- `quickstart_images/`: Generated standalone diagram images.

---

## 2. Building Documents

### Using the Build Scripts
```bash
./build_html.sh       # Compile standalone HTML (quickstart_html/)
./build_pdf.sh        # Compile vector PDF (quickstart_en.pdf)
./build_markdown.sh   # Compile Markdown (quickstart_markdown/)
./build_image.sh      # Export diagram images (quickstart_images/)
./build.sh            # Run all builds sequentially
```

### Optional Editable MS Word (`.docx`) Export
```bash
uv run drawlib build docx quickstart_src/ -o quickstart.docx --generate-index   # -> quickstart_en.docx
```

### Previewing
```bash
./serve.sh            # Start local live preview server for quickstart_html/
```
