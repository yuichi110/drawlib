# Drawlib Official Documentation Site (`docs_src/site/`)

This directory contains the source Markdown files, embedded pure-Python drawing blocks, and theme assets for the official Drawlib website (`https://www.drawlib.com/`).

---

## 1. Directory Structure

- `docs_src/site/`: Source documents and drawing code (**Source of Truth**).
  - `drawlib.toml`: Project manifest (`type = "site"`, `[i18n]` `langs = ["en", "ja"]`, `[seo]` `site_url = "https://www.drawlib.com"`).
  - `en/`: English documentation pages (`navbar.md`, `index.md`, `01_getting_started/` .. `10_ai_agents_and_advanced/`).
  - `ja/`: Japanese documentation pages (`navbar.md`, `index.md`, `01_getting_started/` .. `10_ai_agents_and_advanced/`).
  - `pypi/`: Standalone PyPI showcase illustration scripts (`docs/pypi_images/`).
  - `_assets/`: Shared logos, favicons, OGP banner, GeoJSON, and custom assets across locales.
  - `build.sh` / `build_html.sh`: Static HTML website build scripts (outputs to `docs/`).
  - `serve.sh`: Local preview server script (`docs/`).
  - `styles.py` / `utils.py`: Shared drawing themes and reusable helpers.
  - `style.css` / `template.html`: HTML site stylesheet and Jinja2 layout template.
- `docs/`: Generated public static HTML site (`index.html`, `en/`, `ja/`, `images/`, `CNAME`, `.nojekyll`) (**Do not edit directly**).

---

## 2. Building & Previewing

Always prefer `./dcli` from the repository root:

```bash
./dcli docs build site          # Build docs_src/site/ -> docs/ (and PyPI images)
./dcli docs serve site --check  # Verify zero broken links across docs/
./dcli docs serve site          # Launch local preview server on http://localhost:8000
```

Or run the scripts directly:

```bash
./docs_src/site/build.sh
./docs_src/site/serve.sh
```

To inspect a single diagram with the coordinate grid (`-g`):

```bash
uv run drawlib show docs_src/site/en/index.md 1 -g -o .drawlib/scratch/preview_grid.png
```
