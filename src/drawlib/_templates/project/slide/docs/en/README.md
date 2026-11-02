# Drawlib Slide Presentation Project

This directory contains slide Markdown files and drawing code compiled into an interactive HTML presentation deck and print-ready PDF using Drawlib.

---

## 1. Directory Structure

- `__SRC_DIR__/`: Source slide files and configuration (**Source of Truth**).
  - `drawlib.toml`: Project manifest (`[project]` metadata and `[i18n]` locale configuration).
  - `__DEFAULT_LANG__/`: Slide Markdown files for the default locale (add `<lang>/` directories and append to `langs` in `drawlib.toml` for multi-language decks):
    - `01_title.md`: Title slide.
    - `02_agenda.md`: Agenda slide.
    - `03_architecture.md`: Architecture and diagram slide.
  - `_assets/`: Shared image assets across locales (`favicon.png`, `linux.png`).
  - `build.sh`: Master build script to run standard builds (HTML, PDF, Images).
  - `build_html.sh`: Fast interactive HTML deck compiler.
  - `build_pdf.sh`: Vector presentation PDF compiler (1 slide per page).
  - `build_pptx.sh`: On-demand editable 16:9 MS PowerPoint (`.pptx`) exporter.
  - `build_image.sh`: Standalone diagram image extractor.
  - `serve.sh`: Local preview server with live reloading.
  - `styles.py`: Global styles script (themes, styles, font presets; optional `<lang>/styles.py` override).
  - `utils.py`: Slide macro helpers (cards, tables, timelines, flows).
  - `style.css`: Presentation styling and theme variables.
  - `README.md`: This customization guide.
- `__OUT_HTML_DIR__/`: Generated interactive HTML slide deck (`__OUT_HTML_DIR__/index.html`, `__OUT_HTML_DIR__/<lang>/index.html`).
- `__TARGET___<lang>.pdf` (e.g. `__TARGET_____DEFAULT_LANG__.pdf`): Generated vector PDF presentation(s) per locale.
- `__TARGET___<lang>.pptx` (e.g. `__TARGET_____DEFAULT_LANG__.pptx`): On-demand editable 16:9 MS PowerPoint presentation(s) per locale.
- `__OUT_IMAGES_DIR__/`: Generated standalone diagram images.

---

## 2. Building Slides

### Using the Build Scripts
```bash
./build_html.sh   # Compile interactive HTML slide deck
./build_pdf.sh    # Compile vector PDF presentation (<base>_<lang>.pdf)
./build_pptx.sh   # Export editable 16:9 MS PowerPoint (<base>_<lang>.pptx, on-demand)
./build_image.sh  # Extract standalone diagram images
./build.sh        # Run standard builds sequentially (HTML + PDF + Images)
```

### Previewing
```bash
./serve.sh        # Start local live preview server
```
