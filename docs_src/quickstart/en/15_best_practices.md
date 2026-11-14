# 15. Visual Design Rules & Production Checklist

Great technical diagrams communicate system architecture in under three seconds—not by adding decorative colors, but through disciplined typography scaling, calm neutral contrast, predictable coordinate anchors, and reusable component macros.

This final chapter consolidates Drawlib's engineering design laws into a single-page production cheat sheet that human authors and AI coding agents can consult before shipping any diagram, whitepaper, portal, API catalog, or 16:9 presentation deck.

```drawlib align=center code=fold file=color_do_vs_dont.png caption="Figure 15.1: Color & Contrast Discipline — DON'T (Rainbow Overload) vs. DO (50%+ Neutral Baseline + 1 Focal Highlight)"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line, lines
from drawlib.shapes import rectangle
from drawlib.smartarts import Panel
from drawlib.styles import Styles
from drawlib.text import text

setup(width=158, height=68)

# Left Panel: DON'T (Rainbow Overload & Competing Saturated Fills)
dont_panel = Panel(
    "DON'T: Rainbow Overload & Low Contrast",
    style=Styles.Neutral.patch(shape_r=2.2),
    header_style=Styles.DangerNeutral,
    text_style=Styles.DarkBold.patch(text_size=11.4),
    icon=phosphor.x_circle,
    icon_style=Styles.DangerBold,
    header_height=8.8,
)
dont_panel.draw((6.0, 6.0), width=70.0, height=56.0)

rectangle(
    (24.0, 42.5),
    width=25.0,
    height=11.5,
    style=Styles.AccentFlat.patch(shape_r=1.6),
    text="Client App",
    text_style=Styles.WhiteBold.patch(text_size=10.5),
)
rectangle(
    (57.0, 42.5),
    width=27.0,
    height=11.5,
    style=Styles.WarningFlat.patch(shape_r=1.6),
    text="API Gateway",
    text_style=Styles.WhiteBold.patch(text_size=10.5),
)
rectangle(
    (24.0, 25.5),
    width=25.0,
    height=11.5,
    style=Styles.SuccessFlat.patch(shape_r=1.6),
    text="Auth Worker",
    text_style=Styles.WhiteBold.patch(text_size=10.5),
)
rectangle(
    (57.0, 25.5),
    width=27.0,
    height=11.5,
    style=Styles.DangerFlat.patch(shape_r=1.6),
    text="Primary DB",
    text_style=Styles.WhiteBold.patch(text_size=10.5),
)

line((36.5, 42.5), (43.5, 42.5), arrow_head="->", style=Styles.AccentBold)
line((57.0, 36.7), (57.0, 31.3), arrow_head="->", style=Styles.DangerBold)
lines([(43.5, 39.5), (39.5, 39.5), (39.5, 25.5), (36.5, 25.5)], arrow_head="->", style=Styles.PrimaryBold)

rectangle((41.0, 12.2), width=62.0, height=7.4, style=Styles.White.patch(shape_r=1.4))
text(
    (41.0, 12.2),
    "4 competing saturated boxes -> Zero visual hierarchy",
    style=Styles.DangerBold.patch(text_size=10.0),
)

# Right Panel: DO (50%+ Neutral Baseline + 1 Focal PrimaryFlat Highlight)
do_panel = Panel(
    "DO: 50%+ Neutral Baseline + 1 Focal Hero",
    style=Styles.Neutral.patch(shape_r=2.2),
    header_style=Styles.PrimaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=11.4),
    icon=phosphor.check_circle,
    icon_style=Styles.PrimaryBold,
    header_height=8.8,
)
do_panel.draw((82.0, 6.0), width=70.0, height=56.0)

rectangle((117.0, 34.0), width=63.0, height=33.5, style=Styles.MutedDashed.patch(shape_r=1.8))

rectangle(
    (100.0, 42.5),
    width=25.0,
    height=11.5,
    style=Styles.White.patch(shape_r=1.6),
    text="Client App",
    text_style=Styles.DarkBold.patch(text_size=10.5),
)
rectangle(
    (133.0, 42.5),
    width=27.0,
    height=11.5,
    style=Styles.PrimaryFlat.patch(shape_r=1.6),
    text="API Gateway",
    text_style=Styles.WhiteBold.patch(text_size=10.5),
)
rectangle(
    (100.0, 25.5),
    width=25.0,
    height=11.5,
    style=Styles.SecondaryNeutral.patch(shape_r=1.6),
    text="Auth Worker",
    text_style=Styles.DarkBold.patch(text_size=10.5),
)
rectangle(
    (133.0, 25.5),
    width=27.0,
    height=11.5,
    style=Styles.PrimaryNeutral.patch(shape_r=1.6),
    text="Primary DB",
    text_style=Styles.DarkBold.patch(text_size=10.5),
)

line((112.5, 42.5), (119.5, 42.5), arrow_head="->", style=Styles.DarkBold)
line((133.0, 36.7), (133.0, 31.3), arrow_head="->", style=Styles.DarkBold)
lines([(119.5, 39.5), (115.5, 39.5), (115.5, 25.5), (112.5, 25.5)], arrow_head="->", style=Styles.DarkBold)

rectangle((117.0, 12.2), width=62.0, height=7.4, style=Styles.White.patch(shape_r=1.4))
text(
    (117.0, 12.2),
    "Calm neutral architecture + 1 crisp focal highlight",
    style=Styles.PrimaryBold.patch(text_size=10.0),
)

save()
```

---

## 15.1 The `720pt` Typography Scale & Width Discipline

Because Drawlib maps every canvas width (`setup(width=W, height=H)`) to **`10 inches = 720 points`**, rendered font size in HTML or PDF depends strictly on `text_size × ContainerWidth / 720`. Hardcoding narrow pixel caps like `width=500px` or `width=600px` on a Markdown fence shrinks the container below `720pt`, breaking visual parity with `16px` HTML prose. Always omit pixel `width=` caps on documentation fences and follow this typography scale:

| Hierarchy Role | Recommended `text_size` | Recommended `Styles` Token | Rendered Size in `~900px` Column |
| :--- | :--- | :--- | :--- |
| **Canvas Title** | **`14.0 – 16.0`** | `Styles.DarkBold.patch(text_size=14.5)` | `~17.5px – 20.0px` (Clear banner lead) |
| **Section / Group Header** | **`12.0 – 13.5`** | `Styles.DarkBold.patch(text_size=12.5)` | `~15.0px – 16.9px` (Matches subheadings) |
| **Node / Card Body** | **`10.5 – 12.0`** | `Styles.DarkBold` (light) / `Styles.WhiteBold` (`*Flat`) | `~13.1px – 15.0px` (Matches `16px` prose) |
| **Edge / Axis Labels** | **`10.0`** | `Styles.Dark` or `Styles.Muted` | `~12.5px` (Clean protocol/unit caption) |
| **Strict Floor (Ticks / Code)** | **`9.5` (Never `< 9.5`)** | `Styles.Dark` / `SourceCode` | `~11.9px` (Minimum legible threshold) |

> **16:9 Slide Deck Adjustment (`1920×1080` Stage)**: Slide prose defaults to `26px`—much larger than `16px` web docs. When placing a diagram inside a half-width 2-column `::: block` (`width=960..1040`), raise node/axis `text_size` to **`13.5 – 15.5`** (and titles to `16.0 – 18.5`) while widening boxes by `25%–40%` so labels match adjacent slide bullets.

---

## 15.2 The `50%+` Neutral Baseline & Contrast Discipline

Human-crafted architecture diagrams use color sparingly to direct attention rather than decorate every box:

- **Ground `>= 50%` of Shapes in Calm Neutrals**: Build the majority of service cards, worker nodes, and containers with `Styles.Neutral`, `Styles.PrimaryNeutral`, `Styles.SecondaryNeutral`, or `Styles.White` (and `Styles.MutedDashed` for VPC/cluster boundaries).
- **Reserve Saturated `*Flat` Fills for `1–2` Focal Nodes**: Use `Styles.PrimaryFlat` or `Styles.AccentFlat` exclusively on the core system under discussion so the reader's eye locks onto the focal component immediately.
- **Strict Luminance Contrast Pairing**:
  - On saturated solid fills (`Styles.PrimaryFlat`, `Styles.AccentFlat`, `Styles.DangerFlat`), **always** pair `Styles.WhiteBold` (titles) and `Styles.White` (subtitles/icons).
  - On neutral or light fills (`Styles.Neutral`, `Styles.PrimaryNeutral`, `Styles.SecondaryNeutral`, `Styles.White`), **always** pair `Styles.DarkBold` and `Styles.Dark` (avoid chromatic blue/purple body text on white cards).
- **Neutral Connectors by Default**: Use `Styles.DarkBold` (or `Styles.Dark`) for standard sequential and structural arrows, reserving `Styles.DangerBold` (errors/rollbacks), `Styles.SuccessBold` (verified commits), and `Styles.PrimaryBold` (highlighted critical path) for intentional semantic contrast.
- **PascalCase Token Imports**: Always write `from drawlib.styles import Colors, Styles`—never lowercase `styles` or `colors`, which shadows module namespaces and bypasses `styles.py` overrides.

---

## 15.3 Master Coordinate Anchor Cheat Sheet

Every Drawlib canvas uses Cartesian coordinates with `(0, 0)` at the **bottom-left** (`+X` right, `+Y` up), but individual component families interpret their `xy` placement parameter using one of three anchor conventions. Memorizing—or verifying—this table prevents 100% of off-by-half layout shifts:

| Anchor Convention | Drawlib Families & Classes | How `xy` Behaves | Horizontal / Vertical Span |
| :--- | :--- | :--- | :--- |
| **Center `(cx, cy)`** | `shapes.*` (`rectangle`, `circle`, `cylinder`, ...)<br>`text.text()`, `icons.*` (`phosphor`, `gcp`, `aws`, `azure`, ...)<br>`images.image()`<br>`smartarts.Cycle`, `smartarts.MindMapNode`<br>`diagrams.*` `Node(..., xy=(cx, cy))` | Geometric **center** of the element | `x: [cx - w/2, cx + w/2]`<br>`y: [cy - h/2, cy + h/2]` |
| **Bottom-Left `(x0, y0)`** | `charts.*` (all 10 quantitative charts)<br>`diagrams.*` `d.draw(xy=(x0, y0))` & `NodeGroup(..., xy=(x0, y0))`<br>Most `smartarts.*` (`BoxList`, `CardList`, `ChevronProcess`, `GridLayout`, `Pyramid`, `KpiCards`, `Roadmap`, `Panel`, `GeoMap`, `*Calendar`) | **Bottom-left corner** (`+x` right, `+y` up); center on canvas `W` via `x0 = (W - width) / 2` | `x: [x0, x0 + width]`<br>`y: [y0, y0 + height]` |
| **Top-Left `(x0, y_top)`** | `smartarts.Table`<br>`smartarts.TreeNode`<br>`smartarts.BulletPoints`<br>`smartarts.SourceCode` | **Top-left corner** (`+x` right, rows/branches grow **downward** toward `y = 0`) | `x: [x0, x0 + width]`<br>`y: [y_top - height, y_top]` |
| **Dual Solver (`get_layout()`)** | `graph.*` (`ArchitectureGraph`, `LayerGraph`, `TreeGraph`, `RadialGraph`, `GridGraph`) | Exposes both center and corner coordinates on computed layout objects | `.xy` / `.local_xy` (Center)<br>`.bottom_left` / `.local_bottom_left` |

```drawlib align=center code=fold file=anchor_cheatsheet_visual.png caption="Figure 15.2: Visual Coordinate Anchor Cheat Sheet — Center (cx, cy), Bottom-Left (x0, y0), and Top-Left (x0, y_top)"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.smartarts import Panel
from drawlib.styles import Styles
from drawlib.text import text

setup(width=158, height=70)

# Card 1: Center (cx, cy)
p1 = Panel(
    "1. Center (cx, cy)",
    style=Styles.Neutral.patch(shape_r=2.0),
    header_style=Styles.PrimaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=11.2),
    icon=phosphor.crosshair,
    icon_style=Styles.PrimaryBold,
    header_height=8.5,
)
p1.draw((6.0, 6.0), width=46.0, height=58.0)

text((29.0, 51.5), "Anchor: (cx, cy)", style=Styles.PrimaryBold.patch(text_size=10.2))
rectangle((29.0, 41.0), width=28.0, height=13.0, style=Styles.White.patch(shape_r=1.5))
line((15.0, 41.0), (43.0, 41.0), style=Styles.MutedDashed)
line((29.0, 34.5), (29.0, 47.5), style=Styles.MutedDashed)
circle((29.0, 41.0), radius=2.3, style=Styles.PrimaryOutlineBold)
circle((29.0, 41.0), radius=1.3, style=Styles.PrimaryFlat)

line((10.5, 29.0), (47.5, 29.0), style=Styles.Muted)
text(
    (29.0, 17.5),
    "• shapes.* & text()\n• icons.* & images.*\n• Cycle & MindMapNode\n• Diagram Node(xy=...)",
    style=Styles.Dark.patch(text_size=10.0),
)

# Card 2: Bottom-Left (x0, y0)
p2 = Panel(
    "2. Bottom-Left (x0, y0)",
    style=Styles.PrimaryNeutral.patch(shape_r=2.0),
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=11.2),
    icon=phosphor.corners_out,
    icon_style=Styles.PrimaryBold,
    header_height=8.5,
)
p2.draw((56.0, 6.0), width=46.0, height=58.0)

rectangle((79.0, 43.5), width=28.0, height=13.0, style=Styles.White.patch(shape_r=1.5))
rectangle((71.5, 40.5), width=4.2, height=5.0, style=Styles.SecondaryNeutral)
rectangle((79.0, 42.5), width=4.2, height=9.0, style=Styles.PrimaryNeutral)
rectangle((86.5, 41.5), width=4.2, height=7.0, style=Styles.SecondaryNeutral)
line((65.0, 37.0), (94.8, 37.0), arrow_head="->", style=Styles.DarkBold)
line((65.0, 37.0), (65.0, 51.8), arrow_head="->", style=Styles.DarkBold)
circle((65.0, 37.0), radius=1.6, style=Styles.AccentFlat)
text((79.0, 32.5), "Anchor: (x0, y0)", style=Styles.DarkBold.patch(text_size=10.2))

line((60.5, 29.0), (97.5, 29.0), style=Styles.Muted)
text(
    (79.0, 17.5),
    "• All 10 Charts\n• Diagrams draw(xy=...)\n• ChevronProcess, Panel\n• CardList, KpiCards",
    style=Styles.Dark.patch(text_size=10.0),
)

# Card 3: Top-Left (x0, y_top)
p3 = Panel(
    "3. Top-Left (x0, y_top)",
    style=Styles.Neutral.patch(shape_r=2.0),
    header_style=Styles.PrimaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=11.2),
    icon=phosphor.squares_four,
    icon_style=Styles.PrimaryBold,
    header_height=8.5,
)
p3.draw((106.0, 6.0), width=46.0, height=58.0)

text((129.0, 51.5), "Anchor: (x0, y_top)", style=Styles.PrimaryBold.patch(text_size=10.2))
rectangle((129.0, 40.0), width=28.0, height=13.0, style=Styles.White.patch(shape_r=1.5))
rectangle((129.0, 44.5), width=28.0, height=4.0, style=Styles.PrimaryNeutral)
line((115.0, 38.0), (143.0, 38.0), style=Styles.Muted)
line((115.0, 46.5), (144.8, 46.5), arrow_head="->", style=Styles.DarkBold)
line((115.0, 46.5), (115.0, 32.0), arrow_head="->", style=Styles.DarkBold)
circle((115.0, 46.5), radius=1.6, style=Styles.PrimaryFlat)

line((110.5, 29.0), (147.5, 29.0), style=Styles.Muted)
text(
    (129.0, 17.5),
    "• Table\n• TreeNode\n• BulletPoints\n• SourceCode",
    style=Styles.Dark.patch(text_size=10.0),
)

save()
```

---

## 15.4 Reusable Project Macros (`utils.py` & `styles.py`)

When a project grows past five diagrams, copy-pasting custom card dimensions, subtitle offsets, or CJK font declarations across Markdown blocks invites visual drift. Keep diagrams **DRY (Don't Repeat Yourself)** by separating concerns across two shared files:

- **`styles.py` & `<lang>/styles.py` (Theme & Locale Fonts)**: Configure `Colors = GoogleColors()` and `Styles = GoogleStyles()` in root `styles.py`, and place locale-specific font overrides (such as `Styles = GoogleStyles().patch_font(regular=FontJapanese.SANSSERIF_REGULAR, bold=FontJapanese.SANSSERIF_BOLD)`) inside `ja/styles.py`. Drawlib hashes `styles.py` into `.drawlib/cache.db` automatically so any palette update invalidates and rebuilds dependent figures.
- **`utils.py` (Team-Wide Component Macros)**: Encapsulate recurring domain shapes—such as a standardized `service_card()` or labeled `connect()` helper—inside `utils.py` and import them via `from drawlib.utils import connect, service_card` in every chapter:

```python
# Inside any chapter block or script — reusing macros from utils.py & styles.py
from drawlib.canvas import save, setup
from drawlib.styles import Styles
from drawlib.utils import connect, service_card

setup(width=128, height=42)

# Neutral supporting nodes + 1 focal PrimaryFlat hero using shared macros
service_card((26, 21), "Ingress Proxy", "Envoy :443", width=32, height=18, style=Styles.PrimaryFlat)
service_card((96, 21), "Billing API", "Python / gRPC", width=32, height=18, style=Styles.SecondaryNeutral)
connect((42, 21), (80, 21), label="mTLS gRPC", style=Styles.DarkBold)

save()
```

---

## 15.5 Production Pre-Flight Checklist

Before merging a documentation pull request or publishing release deliverables, run through this five-point production pre-flight checklist:

- [ ] **1. Relative Link & Asset Path Hygiene**: Every cross-page Markdown link (`02_architecture.md`, `../01_intro/index.md`) and asset path (`../_assets/logo.png` in Markdown prose; `"_assets/logo.png"` inside Python `drawlib` blocks) uses portable relative paths. Confirm zero local URI schemes or machine-specific roots such as `/abs/local/path` or `C:\local\path`, which `drawlib build` rejects at compile time.
- [ ] **2. Canvas Margins (`>= 4–6` Units) & Grid Verification (`-g`)**: Every modified diagram has been rendered with `drawlib show ... -g --no-cache` and inspected visually to verify `>= 4–6` coordinate units of outer margin on all four edges, zero text-border collisions, and `text_size >= 10.0`.
- [ ] **3. `50%+` Neutral Palette & Top Hero Placement**: At least half of all cards/nodes rest on calm neutral styles (`Neutral`, `PrimaryNeutral`, `SecondaryNeutral`, `White`), `WhiteBold` is paired with `*Flat` focal nodes, and each chapter/page places a `code=fold` Top Hero diagram at **Lines 5–15** with `2+` diagrams overall.
- [ ] **4. `i18n` Multi-Locale Skeleton Parity**: In bilingual/multilingual projects (`langs = ["en", "ja"]`), every locale contains the identical relative file set, matching `#`/`##`/`###` heading hierarchy, matching fenced code block sequence, and `<stem>_<lang>.png` filenames for localized diagrams.
- [ ] **5. Automated Link Gate & Multi-Target Export Check**: `./<target>_src/build.sh` and `uv run drawlib serve <target>_html/ --check` exit with code `0`, `1280×920` browser views confirm above-the-fold typography harmony, compiled `PDF` / `.docx` / `.pptx` deliverables have clean page breaks, and temporary `.drawlib/scratch/` files are removed.
