# Troubleshooting & Debugging

This guide provides solutions for common rendering errors, coordinate clipping, missing fonts, broken links, and cache anomalies when working with Drawlib.

---

## 1. Visual Geometry & Boundary Clipping

### Symptom: Shapes or Text Clipped at Canvas Edges
- **Cause**: In Drawlib's Cartesian coordinate system, `(0, 0)` is at the bottom-left. Elements placed with coordinates or radii extending beyond `width` or `height` are cropped.
- **Diagnosis**: Run `drawlib show` with the `-g` / `--grid` flag:
  ```bash
  uv run drawlib show docs_src/doc.md 1 -g -o .drawlib/scratch/debug_grid.png
  ```
  The coordinate grid reveals immediately if coordinates exceed `setup(width=..., height=...)`.
- **Solution**:
  1. Increase canvas dimensions in `setup(width=..., height=...)`.
  2. Or shift shapes inward, leaving at least 5–10 units of breathing room along all perimeter edges.

---

## 2. CLI Diagnostics & Developer Mode

By default, Drawlib formats exceptions into concise, user-friendly error summaries. When debugging deep issues or library internals:

### Enable Full Python Tracebacks (`--developer`)
```bash
uv run drawlib --developer build html docs_src/ -o docs_html/
```
Disables error suppression and prints full Python stack traces with exact file names and line numbers.

### Enable Diagnostic Logging (`--verbose` / `--debug`)
```bash
uv run drawlib --verbose build html docs_src/ -o docs_html/
```
Outputs timing metrics, image cache hits/misses, and document parsing phases.

---

## 3. Font Fallbacks & Missing Glyphs

### Symptom: Box Glyphs ("Tofu" `□`) in CJK or Non-Latin Text
- **Cause**: The active font does not contain glyphs for Chinese, Japanese, Korean, or specialized Unicode characters.
- **Solution**:
  1. Switch to universal CJK typography:
     ```python
     from drawlib.fonts import FontSourceHanSans
     from drawlib.types import Style
     
     jp_style = Style(font=FontSourceHanSans.Regular)
     ```
  2. Ensure font assets are pre-cached:
     ```bash
     uv run drawlib cache download --fonts
     ```

---

## 4. Cache Anomalies & Stale Images

### Symptom: Changes to External Assets or Helpers Do Not Reflect in Output
- **Cause**: The SQLite diagram cache (`.drawlib/cache.db`) hashes the code block text. If an external file imported by the block (e.g. `styles.py` or a local PNG) changes, the block hash may still match the cache.
- **Solution**:
  1. Force clean re-rendering during build:
     ```bash
     uv run drawlib build html docs_src/ -o docs_html/ --no-cache
     ```
  2. Or purge the local build cache directory:
     ```bash
     rm -rf .drawlib/
     ```

---

## 5. Broken Link & Missing Asset Auditing

### Pre-Flight Verification
Run `drawlib serve --check` before publishing your documentation site:

```bash
uv run drawlib serve docs_html/ --check
```

Drawlib scans all compiled HTML pages and verifies:
- Every `<a href="...">` internal link points to an existing file.
- Every `<img>` source points to an existing image.
- Any orphaned or broken references are reported with exact line locations.
