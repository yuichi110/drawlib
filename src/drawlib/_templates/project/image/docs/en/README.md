# Drawlib Illustration Scripts

This directory contains standalone Python scripts that generate diagram images in batch mode using Drawlib.

> [!TIP]
> **Need Comprehensive Rules & Deep Guides?**  
> For complete architectural guidelines, drawing syntax, and developer APIs, run:
> - `uv run drawlib rules show overview` : Full drawing manual & workflow feedback loop
> - `uv run drawlib rules show styles`    : Dynamic theming, `styles.py`, and `utils.py`
> - `uv run drawlib rules show canvas`    : Canvas sizing, coordinate origin & clear/save
> - `uv run drawlib rules show cli`       : CLI commands & export options
> - `uv run drawlib rules list`          : List all available rule topics

---

## 1. Directory Structure

- `__SRC_DIR__/`: Source Python illustration scripts (**Source of Truth**).
  - `build.sh`: Build script to execute drawing scripts and generate images.
  - `styles.py`: Global styles script (themes, styles, font presets).
  - `utils.py`: Reusable drawing helper functions, macros, and project constants.
  - `README.md`: This customization guide.
  - `sample1.py`: Basic architecture diagram using Drawlib core primitives.
  - `sample2.py`: Advanced architecture diagram using `utils.py` and local assets (`_assets/`).
- `__OUT_IMAGES_DIR__/`: Generated images directory (**Do not edit directly**).

---

## 2. Building Images

### Using the Build Script
Run the automated build script from the project root or inside this directory:
```bash
./build.sh
```

### Using the Drawlib CLI Directly
```bash
# Execute all Python scripts in the directory and generate image files
drawlib build image __SRC_DIR__/ -o __OUT_IMAGES_DIR__/
```

---

## 3. Customization Guide

### 3.1. Themes & Global Styles (`styles.py`)
Configure drawing styles, color palettes, and fonts for all standalone scripts:
```python
from drawlib.fonts import FontRoboto
from drawlib.styles import Styles

Styles = Styles.patch_font(
    regular=FontRoboto.REGULAR,
    bold=FontRoboto.BOLD,
)
```

### 3.2. Reusable Helpers & Macros (`utils.py`)
Define reusable drawing functions and constants in `utils.py`:
```python
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

BRAND_COLOR = "#0055ff"

def component_box(xy: tuple[float, float], label: str) -> None:
    rectangle(xy, width=28, height=16, r=2, style=Styles.BlueFlat)
    text(xy, label, style=Styles.WhiteBold)
```
Consume inside standalone scripts:
```python
from drawlib.utils import BRAND_COLOR, component_box
component_box((50, 30), "Service Worker")
```

### 3.3. Drawing Script Best Practices
- **Coordinate Origin**: `(0, 0)` is strictly at the bottom-left corner.
- **Center Anchored**: Default coordinates define the geometric center of shapes.
- **Canvas Sizing**: Use `setup(width=..., height=...)` at the start of each drawing. Recommended canvas sizes:
  - `80x40` (badges, small cards)
  - `140x70` (architecture, flows, sequence diagrams)
  - `160x90` (16:9 widescreen slides)
- **Multi-Image Scripts**: Call `clear()` before starting subsequent diagrams in the same script.

### 3.4. Fast Developer Verification
Test an individual drawing script with alignment grid (`-g`):
```bash
drawlib show __SRC_DIR__/sample1.py -g -o preview.png
```
Rebuild without cache:
```bash
drawlib build image __SRC_DIR__/ -o __OUT_DIR__/ --no-cache
```
