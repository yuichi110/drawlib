# The Autonomous Multimodal Visual Feedback Loop

A key strength of modern AI coding assistants equipped with vision tools (such as Claude 3.5 Sonnet, Gemini 1.5 Pro, and GPT-4o) is the ability to visually inspect their own drawings before presenting them to the user.

Drawlib is engineered specifically to empower this autonomous self-correction loop.

---

## 1. The Autonomous Feedback Cycle

```text
1. Inspect Context ──► 2. Prototype in Scratch ──► 3. Render with Grid (-g) ──► 4. Multimodal Review
                                ▲                                                        │
                                └─────────── 5. Issues Found? Adjust & Retry ────────────┘
                                                         │ (Pass)
                                                         ▼
                                                 6. Present to User
```

### Stage 1: Inspect Context
Rather than imagining an architecture from thin air, the agent inspects real repository source code (`models.py`, API routes, microservice configurations).

### Stage 2: Prototype in Isolated Scratch Space (`.drawlib/scratch/`)
The agent drafts the drawing prototype code in an isolated scratch file (`.drawlib/scratch/test_diagram.py`) or tests a specific block instead of altering production assets blindly. Do NOT pollute the project root; ensure `.drawlib/` is in `.gitignore`.

### Stage 3: Headless Render with Coordinate Grid (`-g`)
The agent executes `drawlib show` with the `-g` flag to render the image overlaid with coordinate axes, millimeter tick marks, and numeric coordinate labels:

```bash
uv run drawlib show .drawlib/scratch/test_diagram.py -g -o .drawlib/scratch/test_diagram.png
```

### Stage 4: Multimodal Inspection
Using vision inspection tools (such as `view_file` or image viewer), the agent examines the rendered output for five common visual defects:
1. **Text Overflow & Clipping**: Did a long service name or method label spill outside its enclosing box?
2. **Line & Arrow Overlaps**: Are orthogonal lines colliding awkwardly, or are arrowheads obscured by shapes?
3. **Canvas Margin Starvation**: Are outermost elements pushed right up against the canvas boundary with zero padding?
4. **Color Contrast**: Is dark text placed over dark shape fills, or light text on pale backgrounds?
5. **Color Overuse (Rainbow Chaos)**: Are all boxes colored with saturated fills? Ground 50%+ of nodes in calm neutral or tinted-neutral styles (`Styles.Neutral`, `Styles.NeutralFlat`, `Styles.PrimaryNeutral`, `Styles.SecondaryNeutral`) and reserve saturated hero fills (`Styles.PrimaryFlat`) for 1–2 key focal points.

### Stage 5: Iterative Refinement
Because the coordinate grid directly reveals the exact `(x, y)` location of every visual defect, the agent can adjust coordinates deterministically (e.g. "Move box X from 45.0 to 52.0 to eliminate overlap") rather than guessing.

### Stage 6: Deliver Final Asset
The agent compiles the clean, verified drawing into the document or commits the Python script with 100% confidence.

---

## 2. Visual Inspection Checklist

When performing a multimodal self-review, check off each item in this matrix:

| Verification Area | Common Flaw | Automated Fix |
|---|---|---|
| **Canvas Padding** | Outer nodes touching canvas perimeter | Increase canvas dimensions or add 10–15 units of margin (`setup(width=..., height=...)`). |
| **Node Alignment** | Jagged, misaligned connection lines | Ensure horizontally aligned nodes share the exact same `y` coordinate. |
| **Label Breathing Room** | Text touching card borders | Increase box `width` / `height` or adjust `text_size` via `text_style`. |
| **Arrowhead Visibility** | Arrowhead clipped inside target node | Add `padding=1.5` or `padding=2.0` on connection edge calls. |
| **Color Semantic Roles** | Confusing multi-color rainbow chaos | Follow the 50%+ Neutral-Grounded Architecture rule: ground 50%+ of nodes in calm neutral styles (`Styles.Neutral`, `Styles.PrimaryNeutral`, `Styles.SecondaryNeutral`), use `Styles.MutedDashed` for boundary containers, and reserve saturated hero fills (`Styles.PrimaryFlat`) for 1–2 focal components. |
