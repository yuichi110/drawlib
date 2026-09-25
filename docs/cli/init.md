# `drawlib init`

The `drawlib init` command bootstraps new documentation and illustration projects using pre-configured starter templates.

> **Tip**: If you are using `uv`, run commands with `uv run` (e.g., `uv run drawlib init site my_docs`).

---

## 1. Syntax Overview

```bash
drawlib init [TYPE] [DESTINATION] [OPTIONS]
```

- `TYPE`: Starter template name (`simple`, `site`, or `pdf`).
- `DESTINATION`: Target directory path (defaults to current working directory).

---

## 2. Starter Template Types

| Template Type | Description | Included Files |
| :--- | :--- | :--- |
| **`simple`** | Minimal single-document starter project. | `document.md` (with starter diagram block), `build.sh` |
| **`site`** | Full-fledged multi-page documentation website. | `docs_src/index.md`, `docs_src/navbar.md`, `docs_src/guides/`, `config.py`, build scripts |
| **`pdf`** | Formatted technical report optimized for PDF publishing. | `report.md`, custom print styling configuration |

### Listing Available Templates
```bash
drawlib init --list
```

---

## 3. Command Options

| Option | Flag | Description |
| :--- | :--- | :--- |
| `--list` | `-l` | Lists all available starter project types and exits. |
| `--here` | | Scaffolds files directly into the current working directory without creating a subfolder. |
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
