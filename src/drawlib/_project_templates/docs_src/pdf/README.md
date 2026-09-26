# Drawlib PDF Report Project

This directory contains multi-chapter documents compiled into a unified PDF report.

## Directory Structure

- `__SRC_DIR__/`: Source Markdown chapters (**Source of Truth**).
  - `build.sh`: Build script to compile chapters into a single PDF document.
  - `config.py`: Global configuration script (themes, styles, canvas defaults).
  - `style.css`: PDF report stylesheet.
  - `template.html`: Jinja2 HTML layout used for PDF compilation.
  - `README.md`: This guide.
  - `00_cover.md`: Report title/cover page.
  - `01_overview.md`: Overview chapter.
  - `02_design.md`: Technical design chapter.
- `__OUT_PDF__`: Generated PDF document (**Do not edit directly**).

## Building PDF

From the project root or from inside this directory, run:

```bash
./build.sh
```

Or run drawlib directly:

```bash
drawlib build pdf __SRC_DIR__/ -o __OUT_PDF__ --generate-index
```
