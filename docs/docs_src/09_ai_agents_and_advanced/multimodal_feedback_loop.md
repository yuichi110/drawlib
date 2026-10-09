# The Autonomous Multimodal Visual Feedback Loop

A key strength of modern AI coding assistants equipped with vision tools (such as Claude 3.5 Sonnet, Gemini 1.5 Pro, and GPT-4o) is the ability to visually inspect their own drawings before presenting them to the user.

Drawlib is engineered specifically to empower this autonomous self-correction loop.

---

## 1. The Autonomous Feedback Cycle

```drawlib fold-code 650px center file:multimodal_feedback_cycle.png caption:"The Autonomous Multimodal AI Visual Self-Correction Loop"
from drawlib.canvas import save, setup
from drawlib.lines import line, lines
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=160, height=58)

# Top Row: Stages 1 to 4
rectangle(
    (19, 43),
    width=26,
    height=13,
    style=Styles.Neutral.patch(shape_r=2.0),
    text="1. Inspect Context\n& Rules",
    text_style=Styles.DarkBold.patch(text_size=8.0),
)
rectangle(
    (52, 43),
    width=26,
    height=13,
    style=Styles.PrimaryNeutral.patch(shape_r=2.0),
    text="2. Author\nDrawlib Code",
    text_style=Styles.DarkBold.patch(text_size=8.0),
)
rectangle(
    (85, 43),
    width=26,
    height=13,
    style=Styles.SecondaryNeutral.patch(shape_r=2.0),
    text="3. Render with\nGrid (-g)",
    text_style=Styles.DarkBold.patch(text_size=8.0),
)
rectangle(
    (122, 43),
    width=32,
    height=13,
    style=Styles.PrimaryFlat.patch(shape_r=2.0),
    text="4. Multimodal\nVision Review",
    text_style=Styles.WhiteBold.patch(text_size=8.0),
)

# Forward Connectors (1 -> 2 -> 3 -> 4)
line((32, 43), (39, 43), arrow_head="->", style=Styles.DarkBold)
line((65, 43), (72, 43), arrow_head="->", style=Styles.DarkBold)
line((98, 43), (106, 43), arrow_head="->", style=Styles.DarkBold)

# Decision Branch A: Defects Found -> Loop Back to Step 2
rectangle(
    (78, 14),
    width=44,
    height=11,
    style=Styles.SecondaryNeutral.patch(shape_r=1.5),
    text="Defects Found:\nSelf-Correct Coordinates & Retry",
    text_style=Styles.DarkBold.patch(text_size=7.8),
)
lines([(113, 36.5), (113, 14), (100, 14)], arrow_head="->", style=Styles.DarkBold)
lines([(56, 14), (46, 14), (46, 36.5)], arrow_head="->", style=Styles.DarkBold)

# Decision Branch B: Pass -> Step 5 Final Deliverable
rectangle(
    (136, 14),
    width=34,
    height=11,
    style=Styles.PrimaryNeutral.patch(shape_r=1.5),
    text="5. Final Deliverable\n(Clean Layout & 50%+ Neutral)",
    text_style=Styles.DarkBold.patch(text_size=7.5),
)
line((131, 36.5), (131, 19.5), arrow_head="->", style=Styles.DarkBold)
text((133.5, 28), "Pass", style=Styles.DarkBold.patch(text_size=8.0, halign="left"))

save()
```

### Stage 1: Inspect Context
Rather than imagining an architecture from thin air, the agent inspects real repository source code (`models.py`, API routes, microservice configurations).

### Stage 2: Prototype in Isolated Scratch Space (`.drawlib/scratch/`)
The agent drafts the drawing prototype code in an isolated scratch file (`.drawlib/scratch/test_diagram.py`) or tests a specific block instead of altering production assets blindly. Do NOT pollute the project root; ensure `.drawlib/` is in `.gitignore`.

### Stage 3: Headless Render with Coordinate Grid (`-g`)
The agent executes `drawlib show` with the `-g` flag to render the diagram overlaid with coordinate axes, tick marks, and numeric coordinate labels (targeting embedded Markdown blocks by their explicit `file:` name rather than fragile numeric index):

```bash
# Render an embedded Markdown block by explicit filename with coordinate grid (Recommended):
uv run drawlib show docs_src/architecture.md service_mesh.png -g -o .drawlib/scratch/preview.png

# Or render a standalone Python script with coordinate grid:
uv run drawlib show .drawlib/scratch/test_diagram.py -g -o .drawlib/scratch/test_diagram.png
```

### Stage 4: Multimodal Inspection
Using vision inspection tools (such as `view_file` or an image viewer), the agent examines the rendered output for five common visual defects:
1. **Text Overflow & Clipping**: Did a long service name or method label spill outside its enclosing box?
2. **Line & Arrow Overlaps**: Are orthogonal lines colliding awkwardly, or are arrowheads obscured by shapes?
3. **Canvas Margin Starvation**: Are outermost elements pushed right up against the canvas boundary with zero padding?
4. **Color Contrast**: Is dark text placed over dark shape fills, or light text on pale backgrounds?
5. **Color Overuse (Rainbow Chaos)**: Are all boxes colored with saturated fills? Ground 50%+ of nodes in calm neutral or tinted-neutral styles (`Styles.Neutral`, `Styles.NeutralFlat`, `Styles.PrimaryNeutral`, `Styles.SecondaryNeutral`) and reserve saturated hero fills (`Styles.PrimaryFlat`) for 1–2 key focal points.

### Stage 5: Iterative Refinement
Because the coordinate grid directly reveals the exact `(x, y)` location of every visual defect, the agent can adjust coordinates deterministically (e.g. "Move box X from 45.0 to 52.0 to eliminate overlap") rather than guessing.

```drawlib fold-code 650px center file:multimodal_before_after_comparison.png caption:"Before vs. After Multimodal Self-Correction Using the Coordinate Grid (-g)"
from drawlib.canvas import save, setup
from drawlib.lines import line, lines
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=142, height=58)

# Left Panel: Draft 1 with Visual Defects
text((36, 52.5), "Draft 1: Visual Defects Detected with -g", style=Styles.DangerBold.patch(text_size=8.0))
rectangle((36, 26.5), width=60, height=44, style=Styles.SecondaryNeutral.patch(shape_r=2.0))

# Narrow box (width=16) causing label overflow
rectangle(
    (36, 40.5),
    width=16,
    height=9,
    style=Styles.Neutral.patch(shape_r=1.2),
    text="OrderPaymentGateway",
    text_style=Styles.DarkBold.patch(text_size=8.0),
)
# Intermediate node
rectangle(
    (36, 27.0),
    width=18,
    height=8.5,
    style=Styles.Neutral.patch(shape_r=1.2),
    text="Auth Cache",
    text_style=Styles.DarkBold.patch(text_size=7.4),
)
# Bottom node
rectangle(
    (36, 15.0),
    width=18,
    height=8.0,
    style=Styles.Neutral.patch(shape_r=1.2),
    text="Database",
    text_style=Styles.DarkBold.patch(text_size=7.4),
)
# Colliding arrow cutting straight through intermediate node
line((36, 36.0), (36, 19.0), arrow_head="->", style=Styles.DangerBold)

# Red callout badge with high-contrast white text
rectangle(
    (36, 7.8),
    width=52,
    height=4.8,
    style=Styles.DangerFlat.patch(shape_r=1.0),
    text="Defects: Text overflow & arrow collision",
    text_style=Styles.WhiteBold.patch(text_size=6.9),
)

# Center Transition Arrow
line((67.5, 26.5), (74.5, 26.5), arrow_head="->", style=Styles.DarkBold)

# Right Panel: Draft 2 Self-Corrected
text((106, 52.5), "Draft 2: Self-Corrected After Grid Inspection", style=Styles.DarkBold.patch(text_size=8.0))
rectangle((106, 26.5), width=60, height=44, style=Styles.Neutral.patch(shape_r=2.0))

# Widened focal box (width=28) with wrapped label
rectangle(
    (102, 40.5),
    width=28,
    height=9.5,
    style=Styles.PrimaryFlat.patch(shape_r=1.5),
    text="Order Payment\nGateway",
    text_style=Styles.WhiteBold.patch(text_size=7.4),
)
rectangle(
    (102, 27.0),
    width=28,
    height=8.5,
    style=Styles.PrimaryNeutral.patch(shape_r=1.5),
    text="Auth Cache",
    text_style=Styles.DarkBold.patch(text_size=7.4),
)
rectangle(
    (102, 15.0),
    width=28,
    height=8.0,
    style=Styles.SecondaryNeutral.patch(shape_r=1.5),
    text="Database",
    text_style=Styles.DarkBold.patch(text_size=7.4),
)

# Clean step connectors & orthogonal detour routing around intermediate node
line((102, 35.75), (102, 31.25), arrow_head="->", style=Styles.DarkBold)
line((102, 22.75), (102, 19.0), arrow_head="->", style=Styles.DarkBold)
lines([(116, 40.5), (126, 40.5), (126, 15.0), (116, 15.0)], arrow_head="->", style=Styles.DarkBold)

text((106, 7.8), "Fixed: Widened boxes (w=28) & orthogonal detour", style=Styles.DarkBold.patch(text_size=6.9))

save()
```

### Stage 6: Deliver Final Asset
The agent compiles the clean, verified drawing into the document or commits the Python script with 100% confidence.

---

## 2. Visual Self-Repair Checklist

When performing a multimodal self-review, check off each item in this matrix:

| Verification Area | Common Visual Flaw | Deterministic Fix |
|---|---|---|
| **Canvas Padding** | Outer nodes or labels touching canvas perimeter | Increase canvas dimensions in `setup(width=..., height=...)` or inset outer shapes by at least `8–12` units from all edges. |
| **Node Alignment** | Jagged, slightly crooked horizontal or vertical connection lines | Ensure horizontally aligned nodes share the exact same `y` coordinate and vertically stacked nodes share the exact same `x` coordinate. |
| **Label Breathing Room** | Multi-line text touching or overflowing card borders | Increase box `width` / `height`, insert explicit `\n` line breaks, or lower `text_size` via `.patch(text_size=...)`. |
| **Arrowheads & Edge Labels** | Arrowhead clipped inside target node, or parallel edge labels colliding | Add `padding=1.5` or `2.0` on connectors, route return paths onto distinct sides (`from_side="bottom"`, `to_side="bottom"`), or use `label_offset=(dx, dy)`. |
| **50%+ Neutral Baseline** | Confusing multi-color "rainbow" diagram where every node competes for attention | Ground 50%+ of shapes in calm neutral styles (`Styles.Neutral`, `Styles.PrimaryNeutral`, `Styles.SecondaryNeutral`), use `Styles.MutedDashed` for boundary containers, and reserve saturated hero fills (`Styles.PrimaryFlat`) for 1–2 focal components. |
| **Text Luminance Contrast** | Dark text over dark `Flat` fill or white text over light `Neutral` fill | Always pair saturated `Flat` fills (`Styles.PrimaryFlat`, `Styles.DangerFlat`) with `text_style=Styles.WhiteBold`, and light `Neutral` fills with `Styles.DarkBold` or `Styles.Dark`. |
