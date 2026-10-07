# Drawlib Slide Presentation Project

This directory contains slide Markdown files and drawing code compiled into an interactive HTML presentation deck and print-ready vector PDF using Drawlib.

---

## 1. Directory Structure

- `slide_about_drawlib_src/`: Source slide files and configuration (**Source of Truth**).
  - `build.sh`: Master build script to run all builds (HTML + PDF + Images).
  - `build_html.sh`: Fast interactive HTML deck compiler.
  - `build_pdf.sh`: Vector presentation PDF compiler (1 slide per page).
  - `build_image.sh`: Standalone diagram image extractor.
  - `serve.sh`: Local preview server.
  - `styles.py`: Global styles script (themes, styles, font presets).
  - `utils.py`: Slide macro helpers (cards, tables, timelines, flows).
  - `slide.css`: Presentation styling and theme variables.
  - `01_title.md` ... `09_ecosystem.md`: Slide Markdown files.
  - `_assets/`: Static image assets (logos, mascots).
- `slide_about_drawlib_html/`: Generated interactive HTML slide deck (`slide_about_drawlib_html/index.html`).
- `slide_about_drawlib.pdf`: Generated vector PDF presentation.
- `slide_about_drawlib_images/`: Generated standalone diagram images.

---

## 2. Building Slides

### Using the Build Scripts
```bash
./build_html.sh   # Compile interactive HTML slide deck (slide_about_drawlib_html/)
./build_pdf.sh    # Compile vector PDF presentation (slide_about_drawlib.pdf)
./build_image.sh  # Extract standalone diagram images (slide_about_drawlib_images/)
./build.sh        # Run HTML, PDF, and image builds sequentially
```

### Previewing
```bash
./serve.sh        # Start local preview server at http://localhost:8000
```

### Using the Drawlib CLI Directly
```bash
drawlib build slide slide_about_drawlib_src/ -o slide_about_drawlib_html/
drawlib build pdf slide_about_drawlib_src/ -o slide_about_drawlib.pdf
drawlib build image slide_about_drawlib_src/ -o slide_about_drawlib_images/
```
