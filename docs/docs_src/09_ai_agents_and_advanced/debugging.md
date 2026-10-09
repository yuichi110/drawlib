# Troubleshooting & Debugging

This guide provides solutions for common rendering errors, coordinate clipping, missing fonts, broken links, and cache anomalies when working with Drawlib.

---

## 1. Visual Geometry & Boundary Clipping

### Symptom: Shapes or Text Clipped at Canvas Edges
- **Cause**: In Drawlib's Cartesian coordinate system, `(0, 0)` is at the bottom-left. Elements placed with coordinates or radii extending beyond `width` or `height` are cropped.
- **Diagnosis**: List the blocks in your document or run `drawlib show` with the `-g` / `--grid` flag targeting the block's `file:` name:
  ```bash
  # List all drawlib blocks in the Markdown file:
  uv run drawlib show docs_src/doc.md

  # Render a specific block with the coordinate grid overlay:
  uv run drawlib show docs_src/doc.md arch.png -g -o .drawlib/scratch/debug_grid.png
  ```
  The coordinate grid reveals immediately if coordinates exceed `setup(width=..., height=...)`.
- **Solution**:
  1. Increase canvas dimensions in `setup(width=..., height=...)`.
  2. Or shift shapes inward, leaving at least 5–10 units of breathing room along all perimeter edges.

```drawlib fold-code 650px center file:debugging_boundary_clipping_fix.png caption:"Boundary Clipping Defect vs. Safe 5%–10% Perimeter Margin with Grid (-g)"
from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=154, height=58)

# Left Panel: Bad (Boundary Clipping at x=100)
text((40, 52), "Bad: Node at x=95 Overflows width=100 Boundary", style=Styles.DangerBold.patch(text_size=8.2))
rectangle((40, 26), width=64, height=40, style=Styles.MutedDashed.patch(shape_r=1.5))
text((11, 42.5), "setup(width=100, height=60)", style=Styles.Muted.patch(text_size=7.2, halign="left"))

rectangle((26, 24), width=22, height=14, style=Styles.Neutral.patch(shape_r=1.5), text="API", text_style=Styles.DarkBold.patch(text_size=8.0))
# Simulated clipped box at right canvas edge (x=72)
rectangle((63, 24), width=18, height=14, style=Styles.SecondaryNeutral.patch(shape_r=1.0), text="Worker...", text_style=Styles.DarkBold.patch(text_size=8.0))
line((72, 6), (72, 46), style=Styles.DangerBold)
text((72, 10), "Clipped at x=100!", style=Styles.DangerBold.patch(text_size=7.5, halign="right"))
line((37, 24), (54, 24), arrow_head="->", style=Styles.DarkBold)

# Center Transition Arrow
line((75, 26), (81, 26), arrow_head="->", style=Styles.DarkBold)

# Right Panel: Good (Safe 10-Unit Perimeter Margin Inspected with -g)
text((115, 52), "Good: Safe 10-Unit Perimeter Margin Inspected with -g", style=Styles.DarkBold.patch(text_size=8.2))
rectangle((115, 26), width=64, height=40, style=Styles.MutedDashed.patch(shape_r=1.5))
# Inner safe-zone guide (10-unit margin)
rectangle((115, 26), width=54, height=30, style=Styles.PrimaryNeutral.patch(shape_r=1.5))
text((115, 37.5), "Safe Content Zone (8–10 Unit Margin)", style=Styles.Muted.patch(text_size=7.2))

rectangle((101, 23), width=20, height=13, style=Styles.Neutral.patch(shape_r=1.5), text="API", text_style=Styles.DarkBold.patch(text_size=8.0))
rectangle(
    (129, 23),
    width=20,
    height=13,
    style=Styles.PrimaryFlat.patch(shape_r=1.5),
    text="Worker",
    text_style=Styles.WhiteBold.patch(text_size=8.0),
)
line((111, 23), (119, 23), arrow_head="->", style=Styles.DarkBold)

save()
```

### Symptom: Label Overflow or Connector Line Cutting Across Node Text
- **Cause**:
  1. Single-line labels that are wider than the enclosing rectangle's `width` spill past the left and right borders.
  2. Drawlib uses the **Painter's Algorithm** (elements are rendered in the exact order they are called). Calling `line()` between two node centers *after* calling `rectangle()` draws the line right on top of the intermediate node's label.
- **Solution**:
  1. Insert explicit `\n` line breaks (`"Authentication\nService"`) and widen the card (e.g. `width=32`).
  2. Anchor connectors to shape perimeter edges (`cx ± width/2`) or draw background connectors *before* foreground nodes.

```drawlib fold-code 650px center file:debugging_text_overflow_and_z_order.png caption:"Common Visual Bugs and Fixes: Text Box Sizing and Painter's Algorithm Z-Order"
from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=142, height=58)

# Left Panel: Common Visual Bugs (Anti-Patterns)
text((36, 52.5), "Common Visual Bugs (Anti-Patterns)", style=Styles.DangerBold.patch(text_size=8.0))
rectangle((36, 26.5), width=60, height=44, style=Styles.SecondaryNeutral.patch(shape_r=2.0))

# Bug 1: Narrow box where "Authentication Service" overflows borders
text((36, 44.5), "1. Single-Line Label Overflows Narrow Box (w=16)", style=Styles.DangerBold.patch(text_size=6.9))
rectangle(
    (36, 36.0),
    width=16,
    height=10,
    style=Styles.Neutral.patch(shape_r=1.2),
    text="Authentication Service",
    text_style=Styles.DarkBold.patch(text_size=7.6),
)

# Bug 2: Connector line drawn after node cuts across text label
text((36, 24.5), "2. line() Drawn After rectangle() Cuts Across Label", style=Styles.DangerBold.patch(text_size=6.9))
rectangle((15, 14.0), width=12, height=9, style=Styles.Neutral.patch(shape_r=1.2), text="Client", text_style=Styles.DarkBold.patch(text_size=7.2))
rectangle((36, 14.0), width=18, height=10, style=Styles.Neutral.patch(shape_r=1.2), text="API Node", text_style=Styles.DarkBold.patch(text_size=7.4))
rectangle((57, 14.0), width=12, height=9, style=Styles.Neutral.patch(shape_r=1.2), text="DB", text_style=Styles.DarkBold.patch(text_size=7.2))
# Anti-pattern: line drawn after middle node cuts right over "API Node"
line((21, 14.0), (51, 14.0), arrow_head="->", style=Styles.DangerBold)

# Center Transition Arrow
line((67.5, 26.5), (74.5, 26.5), arrow_head="->", style=Styles.DarkBold)

# Right Panel: Recommended Fixes (Best Practices)
text((106, 52.5), "Recommended Fixes (Best Practices)", style=Styles.DarkBold.patch(text_size=8.0))
rectangle((106, 26.5), width=60, height=44, style=Styles.Neutral.patch(shape_r=2.0))

# Fix 1: Multi-line wrap + widened card (width=32)
text((106, 44.5), "1. Multi-Line Wrap (\\n) + Widened Card (w=32)", style=Styles.DarkBold.patch(text_size=6.9))
rectangle(
    (106, 36.0),
    width=32,
    height=10.5,
    style=Styles.PrimaryFlat.patch(shape_r=1.5),
    text="Authentication\nService",
    text_style=Styles.WhiteBold.patch(text_size=7.6),
)

# Fix 2: Perimeter-anchored connectors (cx ± w/2) & clean Z-order
text((106, 24.5), "2. Anchor Connectors to Perimeter Edges (cx ± w/2)", style=Styles.DarkBold.patch(text_size=6.9))
rectangle((85, 14.0), width=12, height=9, style=Styles.PrimaryNeutral.patch(shape_r=1.2), text="Client", text_style=Styles.DarkBold.patch(text_size=7.2))
rectangle((106, 14.0), width=18, height=10, style=Styles.PrimaryNeutral.patch(shape_r=1.2), text="API Node", text_style=Styles.DarkBold.patch(text_size=7.4))
rectangle((127, 14.0), width=12, height=9, style=Styles.PrimaryNeutral.patch(shape_r=1.2), text="DB", text_style=Styles.DarkBold.patch(text_size=7.2))
line((91, 14.0), (97, 14.0), arrow_head="->", style=Styles.DarkBold)
line((115, 14.0), (121, 14.0), arrow_head="->", style=Styles.DarkBold)

save()
```

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
  1. Configure a CJK-capable font family (or scaffold with `drawlib init <type> --lang ja`):
     ```python
     from drawlib.fonts import FontJapanese
     from drawlib.types import Style
     
     jp_style = Style(text_font=FontJapanese.SANSSERIF_REGULAR)
     ```
  2. Ensure font assets are pre-cached:
     ```bash
     uv run drawlib cache download --fonts
     ```

---

## 4. Cache Anomalies & Stale Images

### Symptom: Changes to External Python Helper Modules Do Not Reflect in Output
- **Cause**: The SQLite diagram cache (`.drawlib/cache.db`) hashes the block's Python code, `styles.py`, `utils.py`, and string-literal local asset files. However, if a block imports an external custom Python module *outside* `styles.py` and `utils.py`, editing that external module will not automatically alter the block's SHA-256 cache key.
- **Solution**:
  1. Force clean re-rendering during build or preview:
     ```bash
     uv run drawlib build html docs_src/ -o docs_html/ --no-cache
     uv run drawlib show docs_src/doc.md arch.png -g -o .drawlib/scratch/preview.png --no-cache
     ```
  2. Or purge the SQLite image cache via the CLI (see [Caching Architecture & CI/CD](../08_doc_builder_and_cli/caching_and_cicd.md)):
     ```bash
     uv run drawlib cache clear --images
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
- Any orphaned or broken references are reported with exact file locations (exiting with status code `1`).

---

## 6. Common Build Error Messages & Fixes

| Error Message | Root Cause | Solution |
| :--- | :--- | :--- |
| **`Missing required 'file:...' option in drawlib code block`** | An embedded ````drawlib```` block in a `doc`, `site`, or `slide` Markdown file omitted the `file:<name>` attribute. | Add an explicit filename to the opening code fence (e.g. ```` ```drawlib 600px center file:service_arch.png caption:"..." ````). |
| **`Directory build requires "index.md" / "navbar.md"`** | Running `drawlib build html` on a `site` directory missing mandatory root files, or missing `template.html` / `style.css`. | Ensure `index.md`, `navbar.md`, `template.html`, and `style.css` exist in `docs_src/`, or scaffold with `drawlib init site`. |
| **`Refusing to overwrite input source directory / file`** | The `-o` output path points to the exact same path as the source input (`src_abs == dest_abs`). | Specify a separate output directory (e.g. `drawlib build markdown docs_src/ -o docs_markdown/`). |
| **`Duplicate output image file detected`** | Two embedded blocks in the same Markdown file share the same `file:<name>`, or two `.py` scripts in `images_src/` call `save()` with the same target path. | Assign a unique `file:<name>.png` to each block or script. |
| **`Playwright or Chromium not found`** | Running `drawlib build pdf` without Playwright or the headless Chromium binary installed. | Run `uv add "drawlib[pdf]"` (or `pip install "drawlib[pdf]"`) followed by `uv run playwright install chromium`. |
