# Drawlib Slide Presentation Project

This directory contains slide Markdown files and drawing code compiled into an interactive HTML presentation deck and print-ready PDF (plus optional editable 16:9 MS PowerPoint `.pptx` export) using Drawlib.

---

## 1. Directory Structure

- `docs/slide_ddos_incident_response_src/`: Source slide files and configuration (**Source of Truth**).
  - `drawlib.toml`: Unified project manifest (`type = "slide"`, `style = "google"`, `[i18n]` `default_lang = "en"`, `langs = ["en"]`).
  - `en/`: English slide deck chapters (`00_opening/` ... `05_closing/`).
  - `_CONTENTS_PLANNING.md`: Underscore-prefixed slide deck blueprint (automatically excluded from compilation).
  - `_assets/`: Shared static image assets across locales.
  - `build.sh`: Master build script to run all builds.
  - `build_html.sh`: Fast interactive HTML deck compiler.
  - `build_pdf.sh`: Vector presentation PDF compiler (1 slide per page).
  - `build_image.sh`: Standalone diagram image extractor.
  - `serve.sh`: Local preview server with live reloading.
  - `styles.py`: Global styles script (themes, styles, font presets).
  - `utils.py`: Slide macro helpers (cards, tables, timelines, flows).
  - `style.css`: Presentation styling and theme variables.
- `docs/slide_ddos_incident_response_html/`: Generated interactive HTML slide deck (`index.html`, `en/index.html`).
- `docs/slide_ddos_incident_response_en.pdf`: Generated vector PDF presentation.
- `docs/slide_ddos_incident_response_images/`: Generated standalone diagram images.

---

## 2. Building Slides

### Using the Build Scripts
```bash
./build_html.sh   # Compile interactive HTML slide deck
./build_pdf.sh    # Compile vector PDF presentation (slide_ddos_incident_response_en.pdf)
./build_image.sh  # Extract standalone diagram images
./build.sh        # Run all builds sequentially
```

### Previewing
```bash
./serve.sh        # Start local live preview server
```

### Using the Drawlib CLI Directly
```bash
uv run drawlib build slide docs/slide_ddos_incident_response_src/ -o docs/slide_ddos_incident_response_html/
uv run drawlib build pdf docs/slide_ddos_incident_response_src/ -o docs/slide_ddos_incident_response.pdf     # -> docs/slide_ddos_incident_response_en.pdf
uv run drawlib build image docs/slide_ddos_incident_response_src/ -o docs/slide_ddos_incident_response_images/

# Optional: Export an editable 16:9 MS PowerPoint (.pptx) presentation
uv run drawlib build pptx docs/slide_ddos_incident_response_src/ -o docs/slide_ddos_incident_response.pptx   # -> docs/slide_ddos_incident_response_en.pptx
```
