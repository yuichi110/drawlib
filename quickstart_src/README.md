# Drawlib Quickstart PDF Project

This directory contains multi-chapter documents compiled into the unified `quickstart.pdf` guide.

## Directory Structure

- `quickstart_src/`: Source Markdown chapters (**Source of Truth**).
  - `build.sh`: Build script to compile chapters into a single PDF document.
  - `config.py`: Global configuration script (themes, styles, canvas defaults).
  - `style.css`: PDF report stylesheet.
  - `template.html`: Jinja2 HTML layout used for PDF compilation.
  - `README.md`: This guide.
  - `00-cover.md`: Cover page.
  - `01-about.md` ... `09-diagrams.md`: Guide chapters.
- `quickstart.pdf`: Generated PDF document (**Do not edit directly**).

## Building PDF

From the project root or from inside this directory, run:

```bash
./build.sh
```

Or run drawlib directly:

```bash
uv run drawlib build pdf quickstart_src/ -o quickstart.pdf --generate-index
```
