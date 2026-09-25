# Drawlib PDF Document Project

This is a multi-chapter report and technical specification project created with [Drawlib](https://github.com/yuichi110/drawlib), compiled into a single publication-ready vector PDF document.

It is ideal for formal architecture reports, technical specifications, system design proposals, and whitepapers requiring high visual fidelity and automated page numbering.

## 1. Project Structure & Chapter Organization

Drawlib compiles Markdown files in `docs_src/` in **alphanumeric order** into a single continuous PDF document:

- `docs_src/`: Source Markdown chapters (**Source of Truth**).
  - `00_cover.md`: Document title, author metadata, and abstract.
  - `01_overview.md`: Chapter 1 covering executive summary and system context.
  - `02_design.md`: Chapter 2 covering architecture and data flows.
- `docs_config.py`: Global configuration script for Drawlib illustrations (themes, canvas defaults, fonts).
- `docs_build.sh`: Automated shell script to compile chapters into `document.pdf`.
- `document.pdf`: Final compiled PDF output (**Never edit directly!**).

### Naming Convention for Chapters:
Use zero-padded numerical prefixes (`00_`, `01_`, `02_`, ..., `10_`) to guarantee consistent chapter sequencing across different operating systems and file systems.

Each Markdown file starts on a fresh page automatically during PDF compilation.

## 2. Headless PDF Compilation Engine

Drawlib generates vector PDFs using a local headless Chromium-based browser (Google Chrome, Chromium, or Microsoft Edge). This ensures crisp vector graphics, modern CSS layout, and font rendering without requiring heavyweight third-party PDF generators.

- Ensure Chrome, Chromium, or Edge is installed on your system.
- If your browser is installed in a non-standard location, set the `DRAWLIB_CHROME_PATH` environment variable:
  ```bash
  export DRAWLIB_CHROME_PATH="/path/to/chrome"
  ```

## 3. Embedding Illustrations in PDF Documents

Drawlib illustration code blocks are embedded using standard ````drawlib```` blocks:

````markdown
# Chapter 1: System Overview

```drawlib 600px center caption:"Figure 1: High-Level Architecture"
config(width=100, height=50)

rectangle((25, 25), width=30, height=20, style="blue_flat", text="Client App", textstyle="white_bold")
rectangle((75, 25), width=30, height=20, style="green_flat", text="Cloud Backend", textstyle="white_bold")

line((40, 25), (60, 25), arrowhead="<->", style="bold")
text((50, 28), "TLS / HTTPS")
```
````

### PDF Authoring Tips:
- **Image Width**: Set explicit widths (e.g. `600px` or `100%`) to fit neatly within standard printable page margins.
- **Code Visibility**: In PDF export mode, code blocks marked with `fold-code` (<details> dropdowns) are automatically omitted or rendered cleanly for static print layouts. Use `show-code` if you want Python code printed alongside the diagram.
- **Table of Contents**: When `--generate-index` (or `--toc`) is passed, Drawlib automatically collects `# Heading 1` and `## Heading 2` headers into a formatted Table of Contents with page references.

## 4. Building the PDF

Compile the document using the automated build script:

```bash
./docs_build.sh
```

Or build manually via the Drawlib CLI:

```bash
# Build PDF with automatic Table of Contents:
drawlib build pdf docs_src/ -o document.pdf --generate-index -c docs_config.py

# Build without Table of Contents:
drawlib build pdf docs_src/ -o document.pdf -c docs_config.py

# Build with a specific style theme (e.g. google, minimal, book):
drawlib build pdf docs_src/ -o document.pdf --generate-index --css google -c docs_config.py
```

## 5. Rapid Illustration Development

Rebuilding an entire multi-chapter PDF during illustration tweaking is slow. Use `drawlib export` or `drawlib show` to quickly test individual diagrams:

```bash
# Rapidly export Chapter 1's first diagram with coordinate grid:
drawlib export docs_src/01_overview.md 1 -g -o scratch/test.png

# Preview in a local desktop GUI window:
drawlib show docs_src/01_overview.md 1 --grid
```

## 6. Learning & Guidelines

For comprehensive syntax rules, component references, and styling guides, use the built-in CLI rules browser:

```bash
# List all available rule topics:
drawlib rules list

# View guidelines for specific topics:
drawlib rules show overview
drawlib rules show shapes
drawlib rules show lines
drawlib rules show docs_build
```
