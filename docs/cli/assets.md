# `drawlib cache` & `css`

These commands manage external release assets and CSS stylesheets.

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

## 2. CSS Management (`drawlib css`)

Inspect available built-in CSS style presets. When initializing a project, use `drawlib init site --css <theme>` to choose your starting stylesheet.

```bash
drawlib css <target> <subcommand> [OPTIONS]
```

- `<target>`: `html` or `pdf`

### Subcommands

| Subcommand | Description | Example |
| :--- | :--- | :--- |
| **`list`** | Lists available CSS preset names. | `drawlib css html list` |
| **`export <preset>`** | Exports a built-in CSS preset to a stylesheet file (`style.css` by default). | `drawlib css html export google -o style.css --force` |

---

<p align="center"><em>© 2026 drawlib by Yuichi Ito. Released under the Apache 2.0 License.</em></p>
