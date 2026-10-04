# Drawlib Slide Presentation Project

This directory contains slide Markdown files and drawing code compiled into an interactive HTML presentation deck and print-ready PDF using Drawlib.

---

## 1. Directory Structure

- `__SRC_DIR__/`: Source slide files and configuration (**Source of Truth**).
  - `build.sh`: Master build script to run all builds.
  - `build_html.sh`: Fast interactive HTML deck compiler.
  - `build_pdf.sh`: Vector presentation PDF compiler (1 slide per page).
  - `serve.sh`: Local preview server with live reloading.
  - `styles.py`: Global styles script (themes, styles, font presets).
  - `utils.py`: Slide macro helpers (cards, tables, timelines, flows).
  - `slide.css`: Presentation styling and theme variables.
  - `01_title.md`: Title slide.
  - `02_agenda.md`: Agenda slide.
  - `03_architecture.md`: Architecture and diagram slide.
- `__OUT_DIR__/`: Generated presentation artifacts (**Do not edit directly**).

---

## 2. Building Slides

### Using the Build Scripts
```bash
./build_html.sh   # Compile interactive HTML slide deck
./build_pdf.sh    # Compile vector PDF presentation
./build.sh        # Run all builds
```

### Previewing
```bash
./serve.sh        # Start local live preview server
```
