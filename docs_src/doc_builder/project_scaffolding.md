# Project Scaffolding with `drawlib init`

To get started quickly, Drawlib provides built-in starter project templates that scaffold complete documentation trees, sample diagrams, configuration scripts, and build tasks.

---

## 1. Starter Project Templates

Drawlib includes four official starter project types:

| Template | Command | Best For | Included Artifacts |
| :--- | :--- | :--- | :--- |
| **`site`** | `drawlib init site` | Complete documentation websites, project manuals, API references | `docs_src/` hierarchy, `navbar.md`, `config.py`, `style.css`, `template.html`, `build.sh` |
| **`simple`** | `drawlib init simple` | Single articles, README diagrams, standalone blog posts | `document.md`, `config.py`, `style.css`, `template.html`, `build.sh` |
| **`pdf`** | `drawlib init pdf` | Technical specifications, whitepapers, executive reports | `doc_src/` chapters (`00_cover.md`...), `config.py`, `style.css`, `template.html`, `build.sh` |
| **`image`** | `drawlib init image` | Standalone Python diagram/illustration scripts | Python script scaffolding, configuration, and image export tasks |

---

## 2. Using `drawlib init`

### 2.1 List Available Templates
```bash
drawlib init --list
```

### 2.2 Scaffolding a New Project Directory
Specify the template type and target directory name:

```bash
drawlib init site my_docs/
```

This creates a new folder `my_docs/` populated with the starter website structure and automatically compiles the initial Markdown (`docs/`) and HTML (`docs_html/`) outputs.

### 2.3 Choosing Language and CSS Theme
You can specify the document language and starting CSS theme:

```bash
# Bootstrap a Japanese documentation website with the Google theme:
drawlib init site my_docs/ --lang ja --css google
```

When `--lang ja` is selected, Drawlib configures Japanese font patching (`FontJapanese.SANSSERIF_REGULAR`) in `config.py` out of the box.

### 2.4 Scaffolding in the Current Directory
Use the `--here` flag to bootstrap directly into an existing empty directory:

```bash
mkdir documentation && cd documentation
drawlib init site --here
```

### 2.5 Overwriting Existing Files
By default, `drawlib init` prevents accidental overwriting. Pass `--force` (`-f`) if you explicitly intend to overwrite existing files:

```bash
drawlib init simple my_docs/ --force
```

---

## 3. End-to-End Workflow After Scaffolding

Once your project is scaffolded, typical development follows this cycle:

```bash
# 1. Inspect a specific diagram block while writing:
drawlib show docs_src/index.md 1

# 2. Compile the static documentation site:
drawlib build html docs_src/ -o docs_html/

# 3. Start a local preview server with auto-reload and broken link checks:
drawlib serve docs_html/
```

---

<p align="center"><em>© 2026 drawlib by Yuichi Ito. Released under the Apache 2.0 License.</em></p>
