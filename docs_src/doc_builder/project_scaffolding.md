# Project Scaffolding with `drawlib init`

To get started quickly, Drawlib provides built-in starter project templates that scaffold complete documentation trees, sample diagrams, configuration scripts, and build tasks.

---

## 1. Starter Project Templates

Drawlib includes three official starter project types:

| Template | Command | Best For | Included Artifacts |
| :--- | :--- | :--- | :--- |
| **`simple`** | `drawlib init simple` | Single articles, README diagrams, standalone blog posts | `document.md`, `build.sh`, sample architecture illustration block |
| **`site`** | `drawlib init site` | Complete documentation websites, project manuals, API references | `docs_src/` hierarchy, `navbar.md`, multiple chapters, custom configuration |
| **`pdf`** | `drawlib init pdf` | Technical specifications, whitepapers, executive reports | Structured multi-section report configured for high-fidelity PDF output |

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

This creates a new folder `my_docs/` populated with the starter website structure.

### 2.3 Scaffolding in the Current Directory
Use the `--here` flag to bootstrap directly into an existing empty directory:

```bash
mkdir documentation && cd documentation
drawlib init site --here
```

### 2.4 Overwriting Existing Files
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
