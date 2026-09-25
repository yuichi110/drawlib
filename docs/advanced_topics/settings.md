# Library Settings & Environment Variables

This guide describes how to configure Drawlib's execution environment, build caching, external tool paths, and canvas defaults.

---

## 1. Environment Variables

Drawlib respects several environment variables for controlling headless browser printing and compilation behavior:

| Variable | Default | Purpose |
| :--- | :--- | :--- |
| `DRAWLIB_CHROME_PATH` | *(auto-detected)* | Path to a Chromium-compatible executable (Chrome, Chromium, Brave, Edge) for headless PDF compilation. |
| `DRAWLIB_DISABLE_CACHE` | *(unset)* | Set to `1` or `true` to force recompilation of all illustration code blocks, bypassing SQLite image build caches. |

### Example: Setting Chromium Path
```bash
export DRAWLIB_CHROME_PATH="/usr/bin/chromium-browser"
drawlib build pdf docs_src/ -o docs.pdf
```

---

## 2. Global Setup Scripts (`--config`)

Rather than repeating canvas configurations, font choices, or themes across dozens of illustrations, provide a Python setup script using the `--config` (`-c`) option during build:

```bash
drawlib build html docs_src/ -o docs_html/ --config setup.py
```

### Example `setup.py`:
```python
from drawlib.canvas import config
from drawlib.preset_styles import MonochromeStyles, set_default_styles

# 1. Canvas coordinate space defaults:
config(width=120, height=80)

# 2. Preset styles theme:
set_default_styles(MonochromeStyles())
```

All functions, styles, and variables declared in this script are injected into the global namespace of every `drawlib` code block.

---

## 3. Logging & Verbosity Flags

Logging levels are controlled directly via the CLI:

- `--quiet`: Suppress all informational and progress outputs, showing only critical errors.
- `--verbose` / `--debug`: Print detailed step-by-step diagnostic output including asset downloads, font resolution, and cache hits.
- `--developer`: Disable internal error masking, showing full Python stack traces when an error occurs.

---

<p align="center"><em>© 2026 drawlib by Yuichi Ito. Released under the Apache 2.0 License.</em></p>
