# 15. Best Practices & Architectural Checklist

Drawing effective architectural illustrations requires visual discipline, clear typographic hierarchy, and consistent color semantics. Follow these proven principles when designing with Drawlib.

## 1. Visual Hierarchy & Typography Scale

Establish an unambiguous reading order by adhering to a consistent text hierarchy:

| Hierarchy Level | Recommended Size | Recommended Style | Typical Placement |
| :--- | :--- | :--- | :--- |
| **Diagram Title** | `14–18` | `Styles.PrimaryBold` | Top of canvas or figure caption |
| **Container / Boundary** | `10–12` | `Styles.MutedBold` | Top-left of boundary boxes |
| **Service / Node Title** | `9–11` | `Styles.WhiteBold` (or `bold`) | Centered inside service cards |
| **Subtitle / Tech Stack** | `7.5–8.5` | `Styles.White` (or `primary`) | Below node titles (`fastapi / :8000`) |
| **Annotation / Metadata** | `7–8` | `Styles.Muted` | Connector protocols, IP subnets |

## 2. Perimeter Margins & Spacing

Never place elements flush against the edges of the canvas. Maintain at least a **5% to 10% perimeter buffer** around the canvas boundary. This ensures illustrations look polished in PDF page margins and responsive web viewports.

## 3. Semantic Color Discipline

Avoid arbitrary rainbow palettes. Use colors intentionally to communicate architectural roles:

```drawlib 640px center file:matrix.png caption:"Figure 15.1: Architectural Design Best Practices Matrix"
from drawlib.canvas import setup
from drawlib.icons import phosphor
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=120, height=48)

rules = [
    (18, phosphor.check_circle, "High Contrast", "White text on dark fill\nDark text on light fill\nNever low-contrast gray", Styles.SuccessFlat),
    (46, phosphor.arrows_out, "Perimeter Margin", "5–10% canvas buffer\nPrevent edge crowding\nBalanced whitespace", Styles.PrimaryFlat),
    (74, phosphor.palette, "Color Meaning", "Primary: Core service\nSecondary: Data store\nAccent: Entry gateway", Styles.SecondaryFlat),
    (102, phosphor.puzzle_piece, "High-Level First", "Favor SmartArts\nFavor Diagrams\nAvoid manual raw math", Styles.AccentFlat),
]

for x, icon_fn, title, desc, st in rules:
    rectangle(xy=(x, 24), width=24, height=36, r=2.5, style=Styles.MutedDashed)
    icon_fn(xy=(x, 34), width=7, style=st)
    text(xy=(x, 25), text=title, style=Styles.PrimaryBold.patch(text_size=8.5))
    text(xy=(x, 14), text=desc, style=Styles.Primary.patch(text_size=7.5))
```

## 4. Semantic Coordinates Pattern (`*_xy`)

Avoid scattering raw coordinate literals `(50, 25)` or cryptic list indices (`a[1]`) across drawing calls. Define meaningful coordinate variables (e.g. `client_xy = (25, 25)`, `gateway_xy = (65, 25)`) at the beginning of the block:
- **Refactoring Resilience**: Repositioning a node automatically updates both its shape and all incoming/outgoing connection lines.
- **Self-Documenting Flows**: Connectors read with immediate clarity: `line(client_xy, gateway_xy, arrow_head="->", style=Styles.PrimaryBold)`.

## Summary Checklist for Production Blueprints

Before merging illustrations into production documentation:

- [ ] **Explicit Imports**: Does every ````drawlib```` block explicitly import all required symbols (e.g. `from drawlib.styles import Colors, Styles`)?
- [ ] **Explicit Naming**: Does every block specify `file:<name>.png` for deterministic referencing?
- [ ] **Semantic Coordinates**: Are coordinates organized via named variables (`*_xy`) rather than raw magic literals?
- [ ] **Aspect Ratio**: Is the canvas `width` and `height` proportioned to the diagram contents without wasted letterbox space?
- [ ] **Contrast Verification**: Is text easily readable across dark and light backgrounds?
- [ ] **Connected Flows**: Do connecting lines have directional arrowheads indicating data flow direction?
- [ ] **Incremental Verification**: Has the block been tested with `uv run drawlib show <file> <name.png> -g -o .drawlib/scratch/test.png`?
