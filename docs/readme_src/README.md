# Drawlib Illustration Scripts

This directory contains standalone Python scripts that generate diagram images for the README.

## Directory Structure

- `readme_src/`: Source Python illustration scripts (**Source of Truth**).
  - `build.sh`: Master build script.
  - `build_image.sh`: Batch image rendering script (outputs to `readme_images/`).
  - `styles.py`: Global configuration script (themes, styles, canvas defaults).
  - `README.md`: This guide.
  - `about/`: Scripts for the "About Drawlib" section.
  - `qs/`: Scripts for the "Quick Start" section.
- `readme_images/`: Generated images directory (**Do not edit directly**).

## Building Images

From the project root or from inside this directory, run:

```bash
./build_image.sh
# or
./build.sh
```

Or run drawlib directly:

```bash
uv run drawlib build image readme_src/ -o readme_images/
```
