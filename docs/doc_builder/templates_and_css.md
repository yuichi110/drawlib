# Templates & Styling

Drawlib provides a flexible styling and templating pipeline based on **Jinja2** HTML templates and modular **CSS** presets. You can use Drawlib's default design out of the box or customize every aspect of the generated site and PDF.

---

## 1. Project-Level Template & CSS Architecture

When bootstrapping a documentation project with `drawlib init site`, `drawlib init simple`, or `drawlib init pdf`, Drawlib generates `template.html` and `style.css` directly in your source directory (`docs_src/` or `doc_src/`):

```text
my_docs/
├── docs_src/
│   ├── index.md
│   ├── navbar.md
│   ├── config.py
│   ├── style.css           # Project stylesheet (customizable directly)
│   ├── template.html       # Jinja2 HTML layout (customizable directly)
│   └── build.sh
├── docs/                   # GitHub-compatible Markdown output
└── docs_html/              # Compiled HTML static site
```

### 1.1 Mandatory Project Files for HTML & PDF Builds
When building HTML or PDF documentation (`drawlib build html` or `drawlib build pdf`):
- `doc_builder` **strictly requires** `template.html` and `style.css` to reside in the target directory (or parent directory of a single file).
- The previous `--css` and `--template` CLI options on build commands have been removed; styling and templating are managed cleanly and reproducibly via `style.css` and `template.html` in your project folder.
- If either file is missing, `drawlib build` halts with an informative error directing you to run `drawlib init`.
- For Markdown (`drawlib build markdown`) and image (`drawlib build images`) builds, `template.html` and `style.css` are not required and are automatically excluded from output processing.

### 1.2 Preset Selection at Initialization
You can choose a built-in theme upon project initialization using the `--css` option:

```bash
drawlib init site my_docs --css google
```

This writes the selected theme stylesheet directly to `docs_src/style.css`.

---

## 2. Template Context Variables

When rendering HTML pages, `drawlib.doc_builder` passes the following variables into the Jinja2 context:

| Variable | Type | Description |
| :--- | :--- | :--- |
| `title` | `str` | Document title (extracted from the first `# H1` heading in the Markdown file). |
| `body` | `str` | Compiled HTML body content including rendered illustrations and syntax-highlighted code. |
| `css_href` | `str \| None` | Relative URL/path to the external CSS stylesheet (`style.css`), or `None` when running in embedded mode. |
| `custom_css` | `str` | Raw CSS stylesheet content when embedded directly in `<style>` tags. |
| `nav_sections` | `list` | Nested navigation sections parsed from `navbar.md` for multi-page sidebar documentation. |
| `nav_items` | `list` | Top-level navigation items for pages and single articles. |
| `index_url` | `str` | Relative URL pointing to the root index page. |
| `site_title` | `str` | Title of the documentation site or library (defaults to `"drawlib"`). |

---

## 3. CSS Presets and Customization

Drawlib styles documents using modern, accessible typography with automatic syntax highlighting via Pygments.

### 3.1 Listing Built-in Presets
You can inspect available built-in CSS presets:

```bash
# List HTML CSS presets:
drawlib css html list

# List PDF CSS presets:
drawlib css pdf list
```

Available presets include `default`, `default-dark`, `default-auto`, `google`, `google-dark`, `google-auto`, `github`, `minimal`, and `monochrome`.

### 3.2 Modifying Styles
To customize the visual style:
- **Directly Edit `docs_src/style.css`**: Edit the scaffolded stylesheet directly. Because `build html` copies `docs_src/style.css` to `docs_html/style.css`, your edits take effect immediately on every build.
- **Exporting Presets**: Switch to or export another preset stylesheet into your project:
  ```bash
  # Export HTML Google theme to docs_src/style.css:
  drawlib css html export google -o docs_src/style.css --force

  # Export PDF dark theme to docs_src/style.css:
  drawlib css pdf export default-dark -o docs_src/style.css --force
  ```

### 3.3 CSS Embedding Modes (`--css-mode`)

| Mode | Flag | Behavior |
| :--- | :--- | :--- |
| **`auto`** (Default) | `--css-mode auto` | Embeds CSS for single-file builds; writes an external `style.css` file for multi-page directory builds. |
| **`embed`** | `--css-mode embed` | Inlines all CSS directly into `<style>` tags in every HTML file. Useful for self-contained, single-file distribution. |
| **`external`** | `--css-mode external` | Writes a shared `style.css` file and links it via `<link rel="stylesheet">`. |

---

<p align="center"><em>© 2026 drawlib by Yuichi Ito. Released under the Apache 2.0 License.</em></p>
