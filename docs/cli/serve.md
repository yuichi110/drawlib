# `drawlib serve`

The `drawlib serve` command launches a local HTTP development server to preview compiled HTML documentation sites directly in your web browser.

> **Tip**: If you are using `uv`, run commands with `uv run` (e.g., `uv run drawlib serve`).

---

## 1. Basic Usage

```bash
# Serve default compiled output (auto-detects docs_html/, docs/, or current directory):
drawlib serve

# Explicitly specify target directory to serve:
drawlib serve docs_html/
```

When started, `drawlib serve`:
1. Scans the target directory for broken relative hyperlinks and missing image assets.
2. Starts a lightweight Python HTTP server on `http://localhost:8000`.
3. Automatically opens your default system web browser.

---

## 2. Command Options

| Option | Flag | Default | Description |
| :--- | :--- | :--- | :--- |
| `--port` | `-p <int>` | `8000` | Port number to bind the HTTP server to. |
| `--no-browser` | | `False` | Prevents automatically launching the web browser upon startup. Ideal for remote SSH sessions, Docker containers, and CI. |
| `--check` | `--check-only` | `False` | Scans the target directory for broken links and missing image assets, prints a report, and exits without starting the server. |
| `--skip-check` | | `False` | Skips the pre-scan integrity checks and starts the server immediately. |

---

## 3. Pre-Flight Asset & Link Checking (`--check`)

Broken links and missing images disrupt documentation quality. The built-in scanner parses all `.html` files in the served directory to ensure:
- All `<a href="...">` links resolve to existing local HTML files or anchor tags.
- All `<img src="...">` paths point to existing image files.
- Static assets like `style.css` are present.

### Running Integrity Checks in CI:
```bash
# Run integrity check and fail if broken references are detected:
drawlib serve docs_html/ --check
```

---

## 4. Typical Development Workflow

```bash
# 1. Compile docs in terminal 1:
drawlib build html docs_src/ -o docs_html/

# 2. Start server in terminal 2 (or background):
drawlib serve docs_html/ -p 8080 --no-browser
```

---

<p align="center"><em>© 2026 drawlib by Yuichi Ito. Released under the Apache 2.0 License.</em></p>
