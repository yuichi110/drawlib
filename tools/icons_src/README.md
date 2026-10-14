# Drawlib Native Icons Source (`tools/icons_src/`)

This directory is a Drawlib `images` project that defines all native architecture icons as declarative Python scripts (`1 icon variant = 1 .py file`).

## Naming Convention (`<icon_name>_<variant>.py`)

Every icon script must include its `variant` as the filename suffix:
- **Default variant**: `<icon_name>_default.py` $\rightarrow$ `<icon_name>_default.png`
  - For `original_cloud/`: Refined pastel 3-color style (`compute_default.py`, `database_default.py`, `ai_agent_default.py`, etc.).
  - For `gcp/`: Unified 3-tone blue (`legacy`) style (`compute_engine_default.py`, `bigquery_default.py`, `gke_default.py`, etc.).
- **Alternative variants**: `<icon_name>_<variant>.py` $\rightarrow$ `<icon_name>_<variant>.png`
  - For `gcp/`: 4-color multicolor (`modern`) style (`compute_engine_modern.py`, `bigquery_modern.py`, etc.).

## Building Icons

Run `./tools/icons_src/build.sh` from the repository root:

```bash
./tools/icons_src/build.sh
```

This executes:
1. `uv run drawlib build image tools/icons_src/ -o tools/release_assets/v0.3/icons/` (with incremental SQLite caching via `tools/icons_src/.drawlib/cache.db`).
2. `uv run python -m tools.dcli.codegen.icons_build` to normalize rendered PNGs to `512 × 512 px` (`460 × 460 px` inner bounding box) and update `manifest.json`.

## Previewing a Single Icon with Grid

```bash
uv run drawlib show tools/icons_src/original_cloud/compute_default.py -g -o .drawlib/scratch/preview.png
```
