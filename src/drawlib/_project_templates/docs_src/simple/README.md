# Drawlib Simple Document

This directory contains simple Markdown documents with embedded Drawlib illustrations.

## Directory Structure

- `__SRC_DIR__/`: Source Markdown documents (**Source of Truth**).
  - `build.sh`: Build script to compile documents into Markdown and HTML.
  - `config.py`: Global configuration script (themes, styles, canvas defaults).
  - `README.md`: This guide.
  - `doc.md`: Sample document with embedded illustrations.
- `__OUT_DIR__/`: Compiled Markdown output (**Do not edit directly**).
- `__OUT_HTML_DIR__/`: Compiled HTML output (**Do not edit directly**).

## Building Documents

From the project root or from inside this directory, run:

```bash
./build.sh
```

Or run drawlib directly:

```bash
drawlib build markdown __SRC_DIR__/doc.md -o __OUT_DIR__/doc.md
drawlib build html __SRC_DIR__/doc.md -o __OUT_HTML_DIR__/doc.html
```
