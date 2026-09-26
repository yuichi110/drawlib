# Drawlib Documentation Site

This directory contains the source Markdown files and configurations for the documentation site.

## Directory Structure

- `docs_src/`: Source Markdown documents and illustrations (**Source of Truth**).
  - `build.sh`: Build script to compile documents into Markdown and HTML.
  - `config.py`: Global configuration script (themes, styles, canvas defaults).
  - `template.html`: Jinja2 HTML layout template for static site generation.
  - `style.css`: Project CSS stylesheet for static site styling.
  - `README.md`: This guide.
  - `index.md`: Root landing page.
  - `navbar.md`: Navigation sidebar definition.
  - `architecture/index.md`: Architecture chapter.
  - `workflow/index.md`: Workflow chapter.
- `docs/`: Generated Markdown site (**Do not edit directly**).
- `docs_html/`: Generated static HTML website (**Do not edit directly**).

## Building Documents

From the project root or from inside this directory, run:

```bash
./build.sh
```

Or run drawlib directly:

```bash
drawlib build html docs_src/ -o docs_html/
drawlib build markdown docs_src/ -o docs/
```

## Previewing HTML Site

To serve and preview the compiled HTML website locally:

```bash
drawlib serve docs_html/
```
