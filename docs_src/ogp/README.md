# Drawlib OGP & GitHub Social Preview Scripts

This directory contains standalone Python scripts (`images` archetype) that generate the `1280 × 640 px` Open Graph Protocol (OGP) / GitHub Social Preview banner images for `drawlib`.

## Directory Structure

- `docs_src/ogp/`: Source Python illustration scripts (**Source of Truth**).
  - `drawlib.toml`: Project configuration manifest (`type = "images"`).
  - `styles.py`: Shared semantic theme and font configuration.
  - `utils.py`: Shared `1280 × 640 px` canvas setup and card/layout helper utilities.
  - `_assets/`: Shared brand logo raster assets (`logo_transparent.png`, `logo_dark_transparent.png`).
  - `build.sh` / `build_image.sh`: Batch image rendering scripts (outputs to `docs/ogp_images/`).
  - `social_preview.py`: Primary GitHub Social Preview (`Git Repo • Single Source of Truth` outer container wrapping `Source` -> `Doc Code (.md / .py)` -> `Output [Site, Doc, Slide]`).
  - `social_preview_codebase.py`: Alternative stage naming variant (`Codebase` -> `Docs as Code (.md / .py)` -> `Output [Site, Doc, Slide]`).
  - `social_preview_minimal.py`: Minimal 3-column variant without the outer repository container (`Git Repo` -> `AI Agent + Drawlib` -> `Site, Doc, Slide`).
- `docs/ogp_images/`: Generated `1280 × 640 px` PNG output directory (**Do not edit directly**).

## Building Images

From the repository root, run via `./dcli`:

```bash
./dcli docs build ogp
```

Or run `drawlib` directly:

```bash
uv run drawlib build image docs_src/ogp/ -o docs/ogp_images/
```
