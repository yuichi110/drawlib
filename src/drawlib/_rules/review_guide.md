# Drawlib Autonomous Review & Self-Correction Guide

Drawlib is engineered from the ground up to enable an **Autonomous Multimodal Self-Correction Loop** for AI coding agents.
Never deliver unverified drawing code or documentation pages to the user. Always execute the structured **3-Stage Review & Self-Correction Loop** against the **5 Quantitative Evaluation Criteria** defined in this guide before reporting task completion.

---

## 1. Why Single-Image Inspection Is Not Enough

When authoring **"Illustration as Code"** and **"Illustrated Documentation as Code"**, AI agents frequently encounter two distinct classes of visual defects:

1. **Micro-Geometry Defects (Inside the Canvas)**:
   - Overlapping shapes, labels colliding with borders, arrowheads cutting through nodes instead of connecting boundary edges, or misinterpreting `center` vs. `bottom-left` coordinate anchors.
   - **Solution**: Render with the 10-unit / 5-unit coordinate grid (`drawlib show ... -g`) and inspect the image multimodally (`view_file`) for **1-shot exact coordinate calculation**.
2. **Macro-Page & Typography Defects (Inside the HTML Document)**:
   - A diagram rendered at `1000px` width looks legible when inspected in isolation as a standalone PNG, yet becomes unreadable when embedded inside a `600px`-capped HTML figure or paired with `text_size=8.0` alongside `16px` HTML body prose.
   - Furthermore, placing the first diagram below 50 lines of text forces readers to scroll before seeing any visual summary.
   - **Solution**: Render the actual HTML page (`docs_html/*.html`) in a headless Chromium browser at desktop viewport (`1280×920`), capture a screenshot, and inspect the **above-the-fold layout and prose-to-diagram font balance** multimodally (`view_file`).

---

## 2. The 3-Stage Autonomous Self-Correction Loop

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ Stage 1: Quantitative & Static Pre-Check (Markdown & Code Audit)           │
│   • 2+ diagrams per page; Top Hero at Lines 5–15 with `fold-code`          │
│   • Zero narrow pixel caps (no `500px`/`600px` on fences); `text_size>=10` │
│   • Rich components (`phosphor`/`gcp` icons + `SmartArts`/`Diagrams`)      │
└────────────────────────────────────┬───────────────────────────────────────┘
                                     ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ Stage 2: Micro-Geometry Review (`drawlib show ... -g` + `view_file`)       │
│   • Export individual diagram with `-g` coordinate grid to `.drawlib/`     │
│   • Check anchor semantics (Center vs. Bottom-Left), margins (>= 4–6u),    │
│     text clipping, arrow routing, and 50%+ neutral color balance           │
└────────────────────────────────────┬───────────────────────────────────────┘
                                     ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ Stage 3: Macro-Page Browser HTML Review (Playwright + `view_file`)         │
│   • Build HTML (`./build.sh`) and run link check (`drawlib serve --check`) │
│   • Capture `1280×920` browser screenshot of `docs_html/<page>.html`       │
│   • Verify Top Hero is visible above the fold & diagram labels match prose │
└────────────────────────────────────────────────────────────────────────────┘
```

```drawlib center fold-code file:review_loop_pipeline.png caption:"Drawlib 3-Stage Autonomous Review & Self-Correction Pipeline"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=150, height=58, dpi=150)

# Outer subtle frame
rectangle(
    (75, 29),
    width=144,
    height=52,
    style=Styles.MutedDashed.patch(shape_r=2.5),
)
text(
    (75, 50.5),
    "Autonomous 3-Stage Multimodal Self-Correction Loop",
    style=Styles.DarkBold.patch(text_size=13.0),
)

# Stage 1 Card (Neutral)
rectangle((26, 25), width=38, height=34, style=Styles.PrimaryNeutral.patch(shape_r=2.0))
phosphor.list_checks((11.5, 36.5), width=5.0, style=Styles.PrimaryBold)
text((28, 36.5), "1. Static Audit", style=Styles.PrimaryBold.patch(text_size=11.5))
text(
    (26, 21),
    "• Hero at Lines 5–15\n• fold-code & 2+ figs\n• No narrow px width\n• text_size >= 10.0",
    style=Styles.Dark.patch(text_size=10.2),
)

# Arrow 1 -> 2
line((45.5, 25), (54.5, 25), arrow_head="->", style=Styles.DarkBold)

# Stage 2 Card (Neutral)
rectangle((75, 25), width=40, height=34, style=Styles.SecondaryNeutral.patch(shape_r=2.0))
phosphor.grid_four((60.0, 36.5), width=5.0, style=Styles.SecondaryBold)
text((77, 36.5), "2. Grid Review (-g)", style=Styles.SecondaryBold.patch(text_size=11.5))
text(
    (75, 21),
    "• drawlib show ... -g\n• 1-shot coord math\n• Anchor alignment\n• 50%+ Neutral cards",
    style=Styles.Dark.patch(text_size=10.2),
)

# Arrow 2 -> 3
line((95.5, 25), (104.5, 25), arrow_head="->", style=Styles.DarkBold)

# Stage 3 Card (Primary Focal Hero)
rectangle((124, 25), width=38, height=34, style=Styles.PrimaryFlat.patch(shape_r=2.0))
phosphor.browser((110.0, 36.5), width=5.0, style=Styles.WhiteBold)
text((126, 36.5), "3. Browser HTML", style=Styles.WhiteBold.patch(text_size=11.5))
text(
    (124, 21),
    "• 1280x920 Viewport\n• Above-the-fold Hero\n• Prose vs Fig font\n• Zero broken links",
    style=Styles.White.patch(text_size=10.2),
)

save()
```

---

### 2.1. Stage 1: Quantitative & Static Pre-Check (Markdown & Code Audit)

Before or immediately after authoring `.md` files in `docs_src/` (or `doc_src/`), verify that every page satisfies these structural thresholds:

| Metric | Mandatory Standard | Common Failure Mode |
| :--- | :--- | :--- |
| **Diagrams per Page** | **`>= 2` embedded ```` ```drawlib ```` blocks** | Single-diagram or text-only pages that fail "Illustrated Documentation as Code". |
| **Top Hero Placement** | **Lines `5–15`** (immediately after `# Title` and 1–2 lead sentences) | Burying the first diagram below 40+ lines of prose or installation tables. |
| **Top Hero Visibility** | **`fold-code`** (or `hide-code` on index/landing pages) | Using `show-code` on the Top Hero, which pushes the illustration below the fold. |
| **Fence Width Attribute** | **Omit pixel widths** (let CSS fill `100%` of `.drawlib-image`) | Hardcoding `500px`, `600px`, or `680px` on fences, which shrinks the entire image and its text. |
| **In-Image `text_size`** | **`>= 10.0`** (standard `10.5`–`12.0`, titles `12.0`–`14.0`, floor `9.5` for dense code) | Using `text_size=7.5`–`8.5`, which renders at `~9px`–`10px` in HTML. |
| **Visual Richness** | Combine **`phosphor` / `gcp` / `font_icon`** with **`SmartArts` / `Diagrams` / `Graphs` / `Charts`** | Drawing barren boxes and straight lines with raw primitives only. |
| **Link & Path Hygiene** | **Strictly relative links (zero `file://` or absolute local paths)** | Writing machine-specific `file:///...` or `/home/...` links, which break on the web and trigger build errors. |

#### Automated Static Audit Snippet
Run this one-liner via `uv run python` to scan all Markdown files in a project for violations:

```bash
uv run python -c '
import glob, re
for path in sorted(glob.glob("docs_src/**/*.md", recursive=True)):
    if path.endswith("navbar.md"): continue
    text = open(path, encoding="utf-8").read()
    fences = list(re.finditer(r"^```drawlib([^\n]*)", text, re.M))
    first_line = text[:fences[0].start()].count("\n") + 1 if fences else 999
    px_caps = [m.group(1) for m in fences if re.search(r"\b[3-7]\d\dpx\b", m.group(1))]
    small_ts = re.findall(r"text_size\s*=\s*([0-9.]+)", text)
    small_ts = [v for v in small_ts if float(v) < 9.5]
    if len(fences) < 2 or first_line > 18 or px_caps or small_ts:
        print(f"{path}: blocks={len(fences)}, hero_line={first_line}, px_caps={px_caps}, small_ts={small_ts}")
'
```

---

### 2.2. Stage 2: Micro-Geometry Review with Coordinate Grid (`drawlib show ... -g`)

Do **not** rebuild the entire site just to test a single diagram, and never guess coordinates blindly.
Export individual diagrams with the `-g` (`--grid`) flag into `.drawlib/scratch/` and inspect them with `view_file`:

```bash
# Export a specific named block from a Markdown document with the coordinate grid:
uv run drawlib show docs_src/architecture/overview.md hero_arch.png \
    -s docs_src/styles.py -u docs_src/utils.py \
    -g -o .drawlib/scratch/preview_grid.png

# Export a standalone Python script from an images_src/ project with the coordinate grid:
uv run drawlib show images_src/topology.py \
    -s images_src/styles.py -u images_src/utils.py \
    -g -o .drawlib/scratch/preview_grid.png
```

Then call `view_file` on `.drawlib/scratch/preview_grid.png`:
- **Read Exact Coordinates from the Grid**: The `-g` overlay draws **10-unit major lines** with numeric labels and **5-unit minor dashed lines**. If a label at `y=42` overlaps a box top edge at `y=40`, you can read off the exact target coordinate (`y=45`) in a single iteration.
- **Check All 4 Perimeter Margins**: Ensure no shape, shadow, or text label comes within `4–6` virtual coordinate units of `x=0`, `x=width`, `y=0`, or `y=height`.
- **Check Arrow Routing & Label Clearance**: Ensure connectors terminate cleanly on shape boundaries (`cx ± w/2`, `cy ± h/2`) and edge labels do not sit directly on top of arrowheads or borders.

---

### 2.3. Stage 3: Macro-Page Browser HTML Verification (Headless Playwright + `view_file`)

After individual diagrams pass Stage 2, compile the HTML documentation and verify both **site integrity** and **real browser rendering**:

```bash
# 1. Build the project and verify zero broken links or missing assets:
./docs_src/build.sh
uv run drawlib serve docs_html/ --check
```

```bash
# 2. Capture a 1280x920 desktop browser screenshot of the rendered HTML page:
uv run python -c '
from pathlib import Path
from playwright.sync_api import sync_playwright

html_file = Path("docs_html/index.html").resolve()
out_png = Path(".drawlib/scratch/browser_check.png").resolve()
out_png.parent.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 920})
    page.goto(html_file.as_uri(), wait_until="networkidle")
    page.screenshot(path=str(out_png), full_page=False)
    browser.close()
'
```

Inspect `.drawlib/scratch/browser_check.png` using `view_file` and verify:
1. **Above-the-Fold Hero Visibility**: Within the `1280×920` viewport (zero scrolling), the page `# Title`, lead paragraph, and the complete **Top Hero illustration** are immediately visible.
2. **Prose-to-Diagram Typography Harmony**: Compare the HTML body text (`16px`) right above the diagram against the labels inside the diagram image. Diagram labels must appear crisp and comparable in visual size (`~13.5px`–`18px` rendered CSS height)—never microscopic.
3. **Clean Up Scratch Files**: Remove temporary preview images (`rm -rf .drawlib/scratch/*`) once verification is complete.

---

## 3. The 5 Core Quantitative Evaluation Criteria

### Criterion 1: Mathematical Typography Scaling (`720pt` Canvas Law)

Drawlib's internal rendering engine maps the **full canvas width (`setup(width=W)`) to exactly `10 inches = 720 points`** regardless of whether `W=100` or `W=160`.
When the resulting image is displayed inside an HTML page at width $W_{\text{HTML}}$ (in CSS `px`), any in-image `text_size` (in `pt`) scales according to:

$$\text{Rendered CSS Font Size (px)} = \text{text\_size} \times \frac{W_{\text{HTML}}}{720}$$

| Fence Width Setting | Displayed $W_{\text{HTML}}$ | `text_size=8.0` Renders As | `text_size=11.0` Renders As | Visual Verdict vs. `16px` HTML Prose |
| :--- | :--- | :--- | :--- | :--- |
| `500px` (Narrow Cap — **Forbidden**) | `500px` | `5.5px` (Unreadable) | `7.6px` (Too small) | **Fails**: Entire figure & text look tiny. |
| `600px` (Old Cap — **Avoid**) | `600px` | `6.7px` (Tiny) | `9.2px` (Cramped) | **Fails**: Noticeably smaller than prose. |
| **Omitted (`100%` Container — Mandatory)** | **`~880px–960px`** | `9.8px–10.6px` (Marginal) | **`13.4px–14.7px` (Ideal)** | **Passes**: Matches `14px–16px` HTML prose! |

- **Rule 1A (Full Container Width)**: Never restrict standard documentation diagrams with narrow pixel widths (`500px`, `600px`, `680px`). Omit the width token on the ```` ```drawlib ```` fence so the `.drawlib-image` container expands to `100%` of the content column (`max-width: 1000px`).
- **Rule 1B (`text_size >= 10.0`)**:
  - **Standard Node / Body Labels**: `text_size = 10.5` – `12.0`
  - **Section Headers / Banner Titles**: `text_size = 12.0` – `15.0`
  - **Dense Code Listings (`SourceCode`) / Secondary Badges**: `text_size >= 9.5` (strict floor)
- **Rule 1C (Widen Boxes When Raising `text_size`)**: Whenever you increase `text_size` (e.g., from `8.5` to `11.0`), proportionally increase container widths (`width += 20%–30%`), `Table` `col_widths`, or `FlowDiagram` node widths so enlarged text never clips or wraps awkwardly.

---

### Criterion 2: Above-the-Fold Top Hero & Eye-Catcher Richness

Every documentation page must hook the reader visually at first glance:
1. **Top Hero Position (`Lines 5–15`)**: Place the first ```` ```drawlib ```` block immediately after `# Page Title` and a concise 1–2 sentence executive summary.
2. **Collapsed Source Code (`fold-code`)**: Always use `fold-code` on the Top Hero diagram (or `hide-code` on landing pages). Putting a 50-line `show-code` block at the top of a page pushes the rendered diagram completely off-screen.
3. **High-Level Component + Icon Synergy**: Top Hero diagrams should combine official iconography (`phosphor.*`, `gcp.*`, `font_icon`) with high-level layout components (`SmartArts`, `ArchitectureDiagram`, `FlowDiagram`, `SequenceDiagram`, `ArchitectureGraph`, `BarChart`, etc.) rather than plain geometric boxes.

---

### Criterion 3: Coordinate Anchor Semantics (`Center` vs. `Bottom-Left`)

One of the most frequent sources of off-by-half layout bugs is confusing **center-anchored primitives** with **bottom-left-anchored composite components**. Always verify which anchor convention a component uses:

| Anchor Type | Drawlib Modules & Functions | How `(x, y)` Is Interpreted | Bounding Box Span |
| :--- | :--- | :--- | :--- |
| **Center `(cx, cy)`** | `shapes.*` (`rectangle`, `circle`, `cylinder`, `chevron`, ...)<br>`text.text()` *(default `halign="center"`, `valign="center"`)*<br>`icons.*` (`phosphor.*`, `gcp.*`, `font_icon`)<br>`images.image()` | Geometric **center** of the element | Horizontal: `[cx - w/2, cx + w/2]`<br>Vertical: `[cy - h/2, cy + h/2]` |
| **Bottom-Left `(x0, y0)`** | `smartarts.*` (`BoxList`, `Table`, `ChevronProcess`, `CardGrid`, `SourceCode`, `BulletPoints`, `TreeNode`, ...)<br>`charts.*` (`BarChart`, `LineChart`, `PieChart`, `RadarChart`, `GanttChart`, ...)<br>`diagrams.*` (`FlowDiagram`, `SequenceDiagram`, `ArchitectureDiagram`, `StateDiagram`, `ClassDiagram`, `ERDiagram`)<br>`graph.*` (`ArchitectureGraph`, `LayerGraph`, `TreeGraph`, ...) | **Bottom-left corner** of the component's bounding area | Horizontal: `[x0, x0 + width]`<br>Vertical: `[y0, y0 + height]` |

> **Centering a Bottom-Left Component on a Canvas of Width `W`**:
> Set `x0 = (W - component_width) / 2`. Never pass `x0 = W / 2` to `chart.draw((x0, y0))` or `table.draw((x0, y0))`, or the component will extend from the middle of the canvas off the right edge!

---

### Criterion 4: 50%+ Neutral Baseline & 1–2 Focal Points

Avoid **"Rainbow Color Chaos"** (assigning a different saturated fill to every node):
- **50%+ Neutral Cards**: Ground at least half of all shapes in calm neutral styles (`Styles.Neutral`, `Styles.PrimaryNeutral`, `Styles.SecondaryNeutral`, `Styles.BlueNeutral`, `Styles.TealNeutral`).
- **1–2 Saturated Focal Nodes**: Reserve `Styles.PrimaryFlat` or `Styles.AccentFlat` (with `text_style=Styles.WhiteBold`) strictly for the primary hero element or entrypoint.
- **Subtle Containers**: Use `Styles.MutedDashed` or `Styles.PrimaryDashed` for outer subsystem or VPC boundaries.

---

### Criterion 5: Perimeter Margins (`>= 4–6` Units) & Vertical Breathing Room

- **Outer Canvas Margin**: Maintain at least `4` to `6` virtual coordinate units of clear whitespace between outermost elements (including top titles, bottom legends, and drop shadows) and the canvas edges (`0`, `width`, `0`, `height`).
- **Header-to-Body Clearance**: Leave at least `4` to `6` units of vertical gap between top banner/section titles and the top edge of cards or containers below them.

---

## 4. Quick Self-Correction Checklist for AI Agents

- [ ] **Stage 1 (Static Check)**: Does every page have `>= 2` diagrams, a Top Hero at `Lines 5–15` with `fold-code`, no narrow `px` width caps on fences, and `text_size >= 10.0`?
- [ ] **Stage 2 (Grid Check `-g`)**: Did you export each new/modified diagram with `drawlib show ... -g -o .drawlib/scratch/preview.png` and inspect it via `view_file` to verify zero overlapping labels, accurate `Center` vs. `Bottom-Left` anchors, and `50%+` neutral color balance?
- [ ] **Stage 3 (Browser HTML Check)**: Did you build the HTML (`./build.sh`), pass `drawlib serve --check`, and inspect a `1280×920` Playwright browser screenshot via `view_file` to confirm above-the-fold Hero visibility and prose-to-diagram font size parity?
- [ ] **Cleanup**: Did you remove temporary files in `.drawlib/scratch/` before finishing?
