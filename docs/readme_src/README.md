# Drawlib README Illustration Scripts

This directory contains standalone Python scripts (`images` archetype) that generate the static PNG and animated APNG illustrations embedded in the repository root `README.md`.

## Directory Structure

- `readme_src/`: Source Python illustration scripts (**Source of Truth**).
  - `drawlib.toml`: Project configuration manifest (`type = "images"`, `width = 1000`).
  - `styles.py`: Shared semantic theme and font configuration.
  - `utils.py`: Shared custom layout and card helper utilities.
  - `_assets/`: Shared raster assets (e.g., `logo_transparent.png`).
  - `build.sh` / `build_image.sh`: Batch image rendering scripts (outputs to `../readme_images/`).
  - `01_hero_ai_doc_loop.py`: Top Hero APNG animation (AI Inner Loop + Human Outer Loop).
  - `02_smartarts_showcase.py`: 18 SmartArt families visual showcase.
  - `03_anim_charts_hero.py`: Quantitative Charts progressive APNG animation.
  - `04_graph_five_solvers_hero.py`: 5 Auto-Layout Graph solvers APNG tour.
  - `05_diagrams_six_families_hero.py`: 6 Software Engineering Diagram engines showcase.
  - `06_icons_overview_hero.py`: 34 Standardized Icon Suites (`4,500+` icons) showcase.
  - `07_doc_build_pipeline.py`: Multi-locale (`drawlib.toml` + `<lang>/`) Doc & Slide build pipeline APNG.
  - `08_quickstart_five_step_workflow.py`: 5-step standalone Python drawing workflow APNG (`client_server.py`).
- `../readme_images/`: Generated PNG/APNG output directory (**Do not edit directly**).

## Building Images

From the repository root, run via `./dcli`:

```bash
./dcli docs build readme
```

Or run `drawlib` directly:

```bash
uv run drawlib build image docs/readme_src/ -o docs/readme_images/
```
