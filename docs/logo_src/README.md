# Drawlib Logo Project

This directory contains the standalone Python scripts that generate the official Drawlib brand logos (`docs/logo/`).

---

## 1. Directory Structure

- `logo_src/`: Source Python illustration scripts (**Source of Truth**).
  - `build.sh` / `build_image.sh`: Build scripts to execute drawing scripts and generate images in `docs/logo/`.
  - `styles.py`: Global styles script (`DefaultColors` & `DefaultStyles`).
  - `utils.py`: Reusable logo drawing functions (`draw_logo`, `draw_logo_icon`, `draw_logo_text`).
  - `logo.py` / `logo_transparent.py`: Official horizontal brand logo (`docs/logo/logo.png`, `docs/logo/logo_transparent.png`).
  - `logo_icon.py` / `logo_icon_transparent.py`: Standalone square icon mark (`docs/logo/logo_icon.png`, `docs/logo/logo_icon_transparent.png`).
  - `logo_text.py` / `logo_text_transparent.py`: Standalone wordmark (`docs/logo/logo_text.png`, `docs/logo/logo_text_transparent.png`).
- `logo/`: Generated logo images directory (**Do not edit directly**).

---

## 2. Building Logo Images

Run the build script from `docs/` or inside `docs/logo_src/`:

```bash
./docs/logo_src/build.sh
```
