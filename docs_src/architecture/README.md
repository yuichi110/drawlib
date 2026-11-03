# Drawlib Software Architecture Specification (`docs_src/architecture/`)

This directory contains the source Markdown files, pure-Python UML/graph diagrams, and configuration assets for Drawlib's internal Software Architecture Specification (`https://www.drawlib.com/architecture/`).

---

## 1. Directory Structure

- `docs_src/architecture/`: Source documents and drawing code (**Source of Truth**).
  - `drawlib.toml`: Unified project manifest (`type = "site"`, `[i18n]` `langs = ["en"]`, `[seo]` `site_url = "https://www.drawlib.com/architecture"`).
  - `en/`: English specification tree (`navbar.md`, `index.md`, `01_overview/` .. `07_test_architecture/`).
  - `_assets/`: Shared favicon, OGP image, and brand assets.
  - `build.sh` / `build_html.sh`: Static HTML website build scripts (outputs to `docs/architecture/`).
  - `serve.sh`: Local preview server script (`docs/architecture/`).
  - `styles.py` / `utils.py`: Shared drawing themes and reusable helpers.
  - `style.css` / `template.html`: HTML site stylesheet and Jinja2 layout template.
- `docs/architecture/`: Generated static HTML site (`index.html`, `en/`, `images/`) (**Do not edit directly**).

---

## 2. Building & Previewing

Always prefer `./dcli` from the repository root:

```bash
./dcli docs build architecture          # Build docs_src/architecture/ -> docs/architecture/
./dcli docs serve architecture --check  # Verify zero broken links across docs/architecture/
./dcli docs serve architecture          # Launch local preview server
```

Or run the scripts directly:

```bash
./docs_src/architecture/build.sh
./docs_src/architecture/serve.sh
```

To inspect a single diagram with the coordinate grid (`-g`):

```bash
uv run drawlib show docs_src/architecture/en/index.md 1 -g -o .drawlib/scratch/preview_grid.png
```
