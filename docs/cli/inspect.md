# `drawlib show`

During documentation authoring, rebuilding an entire site to test an individual diagram is slow. The `show` command lets you extract, execute, inspect, and export a single drawing block or standalone Python script instantaneously.

> **Tip**: If you are using `uv`, run commands with `uv run` (e.g., `uv run drawlib show doc.md 1 -o diagram.png`).

---

## 1. Fast Development Iteration

- **Desktop GUI Mode (default)**: Renders the illustration and displays it in a local GUI preview window.
- **Headless Export Mode (`-o <path>`)**: Renders the illustration and writes it directly to an image file without opening GUI windows (ideal for CI/CD, terminal sessions, and automated testing).

---

## 2. Syntax & Arguments

```bash
drawlib show {file} [target] [OPTIONS]
```

### Arguments:
- `file` (Required): Target Markdown file (`.md`), HTML file (`.html`), or standalone Python script (`.py`).
- `target` (Optional):
  - **1-based Block Index**: An integer (e.g. `1`, `2`, `3`) selecting the $N$-th code block in the document.
  - **Target Image Filename**: The target filename specified in the block header (e.g. `file:arch.png` ➔ target `arch.png`).
  - *If omitted*, the CLI lists all available blocks in the document without executing them.

---

## 3. Options Reference

| Option | Flag | Description |
| :--- | :--- | :--- |
| `--output` | `-o <path>` | Destination path for the rendered image file. Specifying `-o` suppresses the GUI window and operates in headless export mode. |
| `--grid` | `-g` | Overlays Cartesian coordinate grid lines and center axis markers on top of the illustration for precise coordinate tuning. |
| `--styles` | `-s <path>` | Path to a Python styles script (e.g. `styles.py`) to execute with custom styles. |
| `--utils` | `-u <path>` | Path to a Python utility script (e.g. `utils.py`) to execute with custom helpers. |

---

## 4. Usage Examples

### Listing All Blocks in a Document
```bash
drawlib show docs_src/diagrams/sequence.md
```
Output:
```text
Available drawlib code blocks in 'docs_src/diagrams/sequence.md':
Index   Line    File Target                               Header Options
-----------------------------------------------------------------
1       L29     sequence_images/1.png                     Basic Request-Reply Flow
2       L68     sequence_images/sync_async.png            Message Types and Synchronicity
```

### Previewing in Desktop Window
```bash
drawlib show docs_src/diagrams/sequence.md 1
```

### Previewing with Coordinate Grid Overlay
```bash
drawlib show docs_src/diagrams/sequence.md 1 --grid
```

### Exporting Single Block to File in Headless Mode
```bash
drawlib show docs_src/diagrams/sequence.md 1 -o scratch/test_diagram.png
```

### Exporting by Filename Target
```bash
drawlib show docs_src/architecture.md arch.png -o scratch/arch.png
```

### Exporting with Coordinate Grid
```bash
drawlib show docs_src/architecture.md 1 -g -o scratch/preview_grid.png
```

### Previewing or Exporting a Standalone Python Script
```bash
# Preview in window:
drawlib show my_drawing.py

# Export directly to image file:
drawlib show my_drawing.py -o scratch/my_drawing.png
```

---

<p align="center"><em>© 2026 drawlib by Yuichi Ito. Released under the Apache 2.0 License.</em></p>
