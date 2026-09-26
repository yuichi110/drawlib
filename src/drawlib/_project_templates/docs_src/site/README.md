# Drawlib Documentation Site

This directory contains the source Markdown files and configurations for the documentation site.

## Directory Structure

- `__SRC_DIR__/`: Source Markdown documents and illustrations (**Source of Truth**).
  - `build.sh`: Build script to compile documents into Markdown and HTML.
  - `config.py`: Global configuration script (themes, styles, canvas defaults).
  - `README.md`: This guide.
  - `index.md`: Root landing page.
  - `navbar.md`: Navigation sidebar definition.
  - `architecture/index.md`: Architecture chapter.
  - `workflow/index.md`: Workflow chapter.
- `__OUT_DIR__/`: Generated Markdown site (**Do not edit directly**).
- `__OUT_HTML_DIR__/`: Generated static HTML website (**Do not edit directly**).

## Building Documents

From the project root or from inside this directory, run:

```bash
./build.sh
```

Or run drawlib directly:

```bash
drawlib build html __SRC_DIR__/ -o __OUT_HTML_DIR__/
drawlib build markdown __SRC_DIR__/ -o __OUT_DIR__/
```

## Previewing HTML Site

To serve and preview the compiled HTML website locally:

```bash
drawlib serve __OUT_HTML_DIR__/
```
