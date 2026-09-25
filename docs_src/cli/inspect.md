# `drawlib show` & `drawlib export`

During documentation authoring, rebuilding an entire site to test an individual diagram is slow. The `show` and `export` commands let you extract, execute, and inspect a single drawing block or standalone Python script instantaneously.

> **Tip**: If you are using `uv`, run commands with `uv run` (e.g., `uv run drawlib export doc.md 1 -o diagram.png`).

---

## 1. Fast Development Iteration

- **`drawlib show`**: Renders the illustration and displays it in a local GUI preview window (supports `--output` for headless environments).
- **`drawlib export`**: Renders the illustration and writes it directly to an image file without GUI displays (ideal for CI, terminal sessions, and automated testing).

---

## 2. Syntax & Arguments

Both commands share identical argument formats:

```bash
drawlib show {file} [target] [OPTIONS]
drawlib export {file} [target] [OPTIONS]
```

### Arguments:
- `file` (Required): Target Markdown file (`.md`), HTML file (`.html`), or standalone Python script (`.py`).
- `target` (Optional):
  - **1-based Block Index**: An integer (e.g. `1`, `2`, `3`) selecting the $N$-th code block in the document.
  - **Target Image Filename**: The target filename specified in the block header (e.g. `file:arch.png` ➔ target `arch.png`).
  - *If omitted*, the CLI lists all available blocks in the document.

---

## 3. Options Reference

| Option | Flag | Description |
| :--- | :--- | :--- |
| `--output` | `-o <path>` | Destination path for the rendered image file. In `drawlib show`, specifying `-o` suppresses the GUI window and operates in headless mode. |
| `--grid` | `-g` | Overlays Cartesian coordinate grid lines and center axis markers on top of the illustration for precise coordinate tuning. |
| `--config` | `-c <path>` | Path to a Python setup/configuration script (e.g. `config.py`) to execute before rendering. |

---

## 4. Usage Examples

### Listing All Blocks in a Document
```bash
drawlib export docs_src/diagrams/sequence.md
```
Output:
```text
Available drawlib blocks in docs_src/diagrams/sequence.md:
  [1] line 29: format=png, width=650px, align=center, caption='Basic Request-Reply Flow'
  [2] line 68: format=png, width=650px, align=center, caption='Message Types and Synchronicity'
```

### Previewing with Coordinate Grid Overlay
```bash
drawlib show docs_src/diagrams/sequence.md 1 --grid
```

### Exporting Single Block to File in Headless Mode
```bash
drawlib export docs_src/diagrams/sequence.md 1 -o scratch/test_diagram.png
```

### Exporting by Filename Target
```bash
drawlib export docs_src/architecture.md arch.png -o scratch/arch.png
```

### Applying a Custom Theme Configuration
```bash
drawlib export docs_src/index.md 1 -c config.py -o scratch/preview.png
```

---

<p align="center"><em>© 2026 drawlib by Yuichi Ito. Released under the Apache 2.0 License.</em></p>
