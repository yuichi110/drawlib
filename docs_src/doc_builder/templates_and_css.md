# Templates & Styling

Drawlib provides a flexible styling and templating pipeline based on **Jinja2** HTML templates and modular **CSS** presets. You can use Drawlib's default design out of the box or customize every aspect of the generated site and PDF.

---

## 1. Built-in HTML Templates

Drawlib ships with two production-ready Jinja2 HTML templates:

1. **`sidebar.html.j2`** (Default for directories): Complete static site template featuring a collapsible sidebar, document hierarchy tree, table of contents, breadcrumbs, search-ready markup, and responsive mobile layout.
2. **`simple.html.j2`** (Default for single files): Clean, centered, standalone article layout without navigation sidebars.

### 1.1 Exporting a Template for Customization
To inspect or customize the default sidebar template, export it to your project:

```bash
drawlib template html export my_sidebar.html.j2
```

### 1.2 Validating Custom Templates
Before running a build, verify that your modified Jinja2 template contains all necessary placeholders:

```bash
drawlib template html validate my_sidebar.html.j2
```

### 1.3 Applying a Custom Template
Pass the template file path with `-t` or `--template`:

```bash
drawlib build html docs_src/ -o docs_html/ -t my_sidebar.html.j2
```

---

## 2. Template Context Variables

When rendering HTML pages, `drawlib.doc_builder` passes the following variables into the Jinja2 context:

| Variable | Type | Description |
| :--- | :--- | :--- |
| `title` | `str` | Document title (extracted from the first `# H1` heading in the Markdown file). |
| `content` | `str` | Compiled HTML body content including rendered illustrations and syntax-highlighted code. |
| `nav_items` | `list` | Nested navigation hierarchy for generating the sidebar. Each item contains `title`, `href`, and `is_active`. |
| `css_content` | `str` | Combined CSS styling content when running in embedded CSS mode. |
| `has_sidebar` | `bool` | `True` when compiling multi-document directories; `False` for standalone articles. |
| `page_depth` | `int` | Directory nesting depth of the current page relative to the documentation root. |

---

## 3. CSS Presets and Customization

Drawlib styles documents using modern, accessible typography with automatic syntax highlighting via Pygments.

### 3.1 Exporting Built-in CSS Presets
```bash
# List available CSS presets:
drawlib css html list

# Export the default stylesheet:
drawlib css html export custom_theme.css
```

### 3.2 Applying Custom CSS
You can provide custom CSS to override or augment default styles using the `--css` option:

```bash
drawlib build html docs_src/ -o docs_html/ --css brand_overrides.css
```

### 3.3 CSS Embedding Modes (`--css-mode`)

| Mode | Flag | Behavior |
| :--- | :--- | :--- |
| **`auto`** (Default) | `--css-mode auto` | Embeds CSS in single files; writes an external `style.css` file for multi-page directory builds. |
| **`embed`** | `--css-mode embed` | Inlines all CSS directly into `<style>` tags in every HTML file. Useful for self-contained, single-file distribution. |
| **`external`** | `--css-mode external` | Writes a shared `style.css` file and links it via `<link rel="stylesheet">`. |

---

<p align="center"><em>© 2026 drawlib by Yuichi Ito. Released under the Apache 2.0 License.</em></p>
