# Drawlib Slide Presentation Project

This directory contains slide Markdown files and drawing code compiled into an interactive HTML presentation deck and print-ready vector PDF (plus optional editable 16:9 MS PowerPoint `.pptx` export) using Drawlib.

---

## 1. Directory Structure

- `slide_about_drawlib_src/`: Source slide files and configuration (**Source of Truth**).
  - `drawlib.toml`: Unified project manifest (`type = "slide"`, `style = "default"`, `[i18n]` `default_lang = "en"`, `langs = ["en"]`).
  - `en/`: English slide deck chapters (`00_opening/` ... `07_ai_agent_workflow/`).
  - `_assets/`: Static image assets (logos, mascots) shared across locales.
  - `build.sh`: Master build script to run all builds (HTML + PDF + Images).
  - `build_html.sh`: Fast interactive HTML deck compiler.
  - `build_pdf.sh`: Vector presentation PDF compiler (1 slide per page).
  - `build_image.sh`: Standalone diagram image extractor.
  - `serve.sh`: Local preview server.
  - `styles.py`: Global styles script (themes, styles, font presets).
  - `utils.py`: Slide macro helpers (cards, tables, timelines, flows).
  - `style.css`: Presentation styling and theme variables.
- `slide_about_drawlib_html/`: Generated interactive HTML slide deck (`index.html`, `en/index.html`).
- `slide_about_drawlib_en.pdf`: Generated vector PDF presentation.
- `slide_about_drawlib_images/`: Generated standalone diagram images.

---

## 2. Building Slides

### Using the Build Scripts
```bash
./build_html.sh   # Compile interactive HTML slide deck (slide_about_drawlib_html/)
./build_pdf.sh    # Compile vector PDF presentation (slide_about_drawlib_en.pdf)
./build_image.sh  # Extract standalone diagram images (slide_about_drawlib_images/)
./build.sh        # Run HTML, PDF, and image builds sequentially
```

### Previewing
```bash
./serve.sh        # Start local preview server at http://localhost:8000
```

### Using the Drawlib CLI Directly
```bash
uv run drawlib build slide slide_about_drawlib_src/ -o slide_about_drawlib_html/
uv run drawlib build pdf slide_about_drawlib_src/ -o slide_about_drawlib.pdf     # -> slide_about_drawlib_en.pdf
uv run drawlib build image slide_about_drawlib_src/ -o slide_about_drawlib_images/

# Optional: Export an editable 16:9 MS PowerPoint (.pptx) presentation
uv run drawlib build pptx slide_about_drawlib_src/ -o slide_about_drawlib.pptx   # -> slide_about_drawlib_en.pptx
```
