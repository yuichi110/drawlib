# `drawlib cache`, `template`, & `css`

These commands manage external release assets, HTML/PDF Jinja2 templates, and CSS stylesheets.

> **Tip**: If you are using `uv`, run commands with `uv run` (e.g., `uv run drawlib cache list`).

---

## 1. Asset Cache Management (`drawlib cache`)

To keep the initial Python package size lightweight, Drawlib downloads non-essential heavy assets (such as Phosphor icons, Google Cloud icons, and CJK/Arabic language fonts) dynamically from GitHub Releases on demand. Once downloaded, assets are cached locally.

```bash
drawlib cache <subcommand> [OPTIONS]
```

### Subcommands

| Subcommand | Description | Example |
| :--- | :--- | :--- |
| **`list`** | Displays all downloadable asset packages and their current local cache status. | `drawlib cache list` |
| **`download`** | Pre-downloads specific or all asset packages from GitHub Releases for offline use. | `drawlib cache download icons_phosphor` |
| **`clear`** | Clears all cached font and icon assets from local storage. | `drawlib cache clear` |

---

## 2. Template Management (`drawlib template`)

Manage built-in Jinja2 templates used when compiling HTML documentation or PDF manuals.

```bash
drawlib template <target> <subcommand> [OPTIONS]
```

- `<target>`: `html` or `pdf`

### Subcommands

| Subcommand | Description | Example |
| :--- | :--- | :--- |
| **`list`** | Lists all built-in templates available for the specified target. | `drawlib template html list` |
| **`export`** | Exports a built-in template to a local file for modification. | `drawlib template html export custom_sidebar.html.j2` |
| **`validate`** | Verifies that a custom Jinja2 template contains all required block tags and variables. | `drawlib template html validate custom_sidebar.html.j2` |

---

## 3. CSS Management (`drawlib css`)

Manage and export built-in CSS style presets.

```bash
drawlib css <target> <subcommand> [OPTIONS]
```

- `<target>`: `html` or `pdf`

### Subcommands

| Subcommand | Description | Example |
| :--- | :--- | :--- |
| **`list`** | Lists available CSS stylesheets (e.g. `default.css`, `pygments.css`). | `drawlib css html list` |
| **`export`** | Exports a built-in CSS stylesheet to a local file for customization. | `drawlib css html export my_style.css` |

---

<p align="center"><em>© 2026 drawlib by Yuichi Ito. Released under the Apache 2.0 License.</em></p>
