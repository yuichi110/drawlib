# Drawlib PDF Document Project

This is a multi-chapter report project compiled into a single PDF document with an automated Table of Contents.

## Project Structure

- `docs_src/`: Source Markdown chapters compiled in alphanumeric order.
  - `00_cover.md`: Document cover page.
  - `01_overview.md`: Chapter 1 with system overview diagram.
  - `02_design.md`: Chapter 2 with data flow diagram.
- `docs_config.py`: Global configuration script for Drawlib illustrations.
- `docs_build.sh`: Shell script to compile all chapters into `document.pdf`.

## Building the PDF

Run the build script:

```bash
./docs_build.sh
```

Or build manually via the CLI:

```bash
drawlib build pdf docs_src/ -o document.pdf --generate-index -c docs_config.py
```

*Note: Generating PDF requires a Chromium-based browser (Chrome, Chromium, Edge) installed on the system.*
