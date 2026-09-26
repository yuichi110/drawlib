# `drawlib init`

The `drawlib init` command bootstraps new documentation and illustration projects using pre-configured starter templates.

> **Tip**: If you are using `uv`, run commands with `uv run` (e.g., `uv run drawlib init site my_docs`).

---

## 1. Syntax Overview

```bash
drawlib init [TYPE] [DESTINATION] [OPTIONS]
```

- `TYPE`: Starter template name (`site`, `simple`, `pdf`, or `image`).
- `DESTINATION`: Target directory path (defaults to current working directory).

---

## 2. Starter Template Types

| Template Type | Description | Included Files |
| :--- | :--- | :--- |
| **`site`** | Full-fledged multi-page documentation website. | `docs_src/` (`index.md`, `navbar.md`, sections, `config.py`, `style.css`, `template.html`, `build.sh`, `README.md`) |
| **`simple`** | Minimal single-document starter project. | `docs_src/` (`doc.md`, `config.py`, `style.css`, `template.html`, `build.sh`, `README.md`) |
| **`pdf`** | Formatted multi-chapter technical report for PDF publishing. | `doc_src/` (`00_cover.md`, `01_overview.md`, `02_design.md`, `config.py`, `style.css`, `template.html`, `build.sh`, `README.md`) |
| **`image`** | Standalone illustration/diagram generation project. | `images_src/` (`sample.py`, `config.py`, `build.sh`, `README.md`) |

### Listing Available Templates
```bash
drawlib init --list
```

---

## 3. Command Options

| Option | Flag | Description |
| :--- | :--- | :--- |
| `--list` | `-l` | Lists all available starter project types and exits. |
| `--lang` | | Target language for starter content and font configuration (`en` [default] or `ja`). |
| `--css` | | Built-in CSS theme preset (`google`, `github`, `minimal`, `monochrome`, etc.) or stylesheet path. |
| `--output` | `-o` | Base project/artifact name (e.g. `-o mybook` produces `mybook_src/`, `mybook.pdf`, etc.). |
| `--here` | | Scaffolds files directly into the current working directory without creating a subfolder. |
| `--no-build` | | Skips the automatic initial build step upon project creation. |
| `--force` | `-f` | Overwrites existing files if destination files already exist. |

---

## 4. Examples

### Create a Complete Documentation Website
```bash
drawlib init site my_docs/
cd my_docs/
drawlib build html docs_src/ -o docs_html/
```

### Initialize a Standalone Article in the Current Directory
```bash
mkdir article && cd article
drawlib init simple --here
```

### Bootstrap a PDF Report with Force Overwrite
```bash
drawlib init pdf whitepaper/ --force
```

---

<p align="center"><em>© 2026 drawlib by Yuichi Ito. Released under the Apache 2.0 License.</em></p>
