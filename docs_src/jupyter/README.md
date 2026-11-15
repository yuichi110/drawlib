# jupyter — Drawlib Jupyter & Google Colab Project

This directory (`jupyter_src/`) is the single source of truth for your illustrated Jupyter Notebooks (`.ipynb`) and browser HTML preview.

## Quick Commands

```bash
# Build .ipynb notebooks + HTML preview (and execute all cells via AI Dry-Run)
./jupyter_src/build.sh

# Run AI Dry-Run verification only (without writing output files)
uv run drawlib build jupyter jupyter_src/ --dry-run

# Serve the static HTML notebook preview in your browser
./jupyter_src/serve.sh
```
