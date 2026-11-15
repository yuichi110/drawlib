# __TARGET__ — Drawlib Jupyter & Google Colab Project

This directory (`__SRC_DIR__/`) is the single source of truth for your illustrated Jupyter Notebooks (`.ipynb`) and browser HTML preview.

## Quick Commands

```bash
# Build .ipynb notebooks + HTML preview (and execute all cells via AI Dry-Run)
./__SRC_DIR__/build.sh

# Run AI Dry-Run verification only (without writing output files)
uv run drawlib build jupyter __SRC_DIR__/ --dry-run

# Serve the static HTML notebook preview in your browser
./__SRC_DIR__/serve.sh
```
