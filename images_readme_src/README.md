# Drawlib Illustration Scripts

This directory contains standalone Python scripts that generate diagram images for the README.

## Directory Structure

- `images_readme_src/`: Source Python illustration scripts (**Source of Truth**).
  - `build.sh`: Build script to execute drawing scripts and generate images.
  - `config.py`: Global configuration script (themes, styles, canvas defaults).
  - `README.md`: This guide.
  - `about/`: Scripts for the "About Drawlib" section.
  - `qs/`: Scripts for the "Quick Start" section.
- `images_readme/`: Generated images directory (**Do not edit directly**).

## Building Images

From the project root or from inside this directory, run:

```bash
./build.sh
```

Or run drawlib directly:

```bash
uv run drawlib build image images_readme_src/ -o images_readme/
```
