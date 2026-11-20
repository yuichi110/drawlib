# __TARGET__ — Drawlib Jupyter & Google Colab Project

This directory (`__SRC_DIR__/`) is the single source of truth for your illustrated Jupyter Notebooks (`.ipynb`), browser HTML preview, and standalone diagram images.

## Quick Commands

```bash
# Build HTML preview (+ bundled .ipynb), standalone .ipynb notebooks, and extracted images
./__SRC_DIR__/build.sh

# Build standalone .ipynb notebooks only (ideal for Google Drive + Colab sharing) -> __OUT_JUPYTER_DIR__/
./__SRC_DIR__/build_jupyter.sh

# Build 2-column HTML preview site with bundled .ipynb downloads -> __OUT_HTML_DIR__/
./__SRC_DIR__/build_html.sh

# Extract rendered diagram images -> __OUT_IMAGES_DIR__/
./__SRC_DIR__/build_image.sh

# Run AI Dry-Run verification only (without writing output files)
uv run drawlib build jupyter __SRC_DIR__/ --dry-run

# Serve the static HTML notebook preview in your browser (__OUT_HTML_DIR__/)
./__SRC_DIR__/serve.sh
```
