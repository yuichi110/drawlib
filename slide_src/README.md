# Drawlib Slide Presentation Project

This directory contains slide Markdown files and drawing code compiled into an interactive HTML presentation deck and print-ready vector PDF using Drawlib.

---

## 1. Directory Structure

- `slide_src/`: Source slide files and configuration (**Source of Truth**).
  - `build.sh`: Master build script to run all builds (HTML + PDF).
  - `build_html.sh`: Fast interactive HTML deck compiler.
  - `build_pdf.sh`: Vector presentation PDF compiler (1 slide per page).
  - `serve.sh`: Local preview server.
  - `styles.py`: Global styles script (themes, styles, font presets).
  - `utils.py`: Slide macro helpers (cards, tables, timelines, flows).
  - `slide.css`: Presentation styling and theme variables.
  - `01_title.md` ... `09_ecosystem.md`: Slide Markdown files.
  - `_assets/`: Static image assets (logos, mascots).
- `slide/`: Generated interactive HTML slide deck (`slide/index.html`).
- `slide.pdf`: Generated vector PDF presentation.

---

## 2. Building Slides

### Using the Build Scripts
```bash
./build_html.sh   # Compile interactive HTML slide deck (slide/)
./build_pdf.sh    # Compile vector PDF presentation (slide.pdf)
./build.sh        # Run HTML and PDF builds sequentially
```

### Previewing
```bash
./serve.sh        # Start local preview server at http://localhost:8000
```

### Using the Drawlib CLI Directly
```bash
drawlib build slide slide_src/ -o slide/
drawlib build pdf slide_src/ -o slide.pdf
```
