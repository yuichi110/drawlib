# Drawlib Illustration Scripts

This directory contains standalone Python scripts that generate diagram images.

## Directory Structure

- `__SRC_DIR__/`: Source Python illustration scripts (**Source of Truth**).
  - `build.sh`: Build script to execute drawing scripts and generate images.
  - `config.py`: Global configuration script (themes, styles, canvas defaults).
  - `README.md`: This guide.
  - `sample.py`: Example drawing script.
- `__OUT_DIR__/`: Generated images directory (**Do not edit directly**).

## Building Images

From the project root or from inside this directory, run:

```bash
./build.sh
```

Or run drawlib directly:

```bash
drawlib build image __SRC_DIR__/ -o __OUT_DIR__/
```
