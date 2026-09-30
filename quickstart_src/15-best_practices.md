# 15. Best Practices & Architectural Checklist

Drawing effective architectural illustrations requires visual discipline, clear typographic hierarchy, and consistent color semantics. Follow these proven principles when designing with Drawlib.

## 1. Visual Hierarchy & Typography Scale

Establish an unambiguous reading order by adhering to a consistent text hierarchy:

| Hierarchy Level | Recommended Size | Recommended Style | Typical Placement |
| :--- | :--- | :--- | :--- |
| **Diagram Title** | `14–18` | `Styles.bold` | Top of canvas or figure caption |
| **Container / Boundary** | `10–12` | `Styles.muted_bold` | Top-left of boundary boxes |
| **Service / Node Title** | `9–11` | `Styles.white_bold` (or `bold`) | Centered inside service cards |
| **Subtitle / Tech Stack** | `7.5–8.5` | `Styles.white` (or `primary`) | Below node titles (`fastapi / :8000`) |
| **Annotation / Metadata** | `7–8` | `Styles.muted` | Connector protocols, IP subnets |

## 2. Perimeter Margins & Spacing

Never place elements flush against the edges of the canvas. Maintain at least a **5% to 10% perimeter buffer** around the canvas boundary. This ensures illustrations look polished in PDF page margins and responsive web viewports.

## 3. Semantic Color Discipline

Avoid arbitrary rainbow palettes. Use colors intentionally to communicate architectural roles:

```drawlib 640px center caption:"Figure 15.1: Architectural Design Best Practices Matrix"
from drawlib.canvas import setup
from drawlib.icons import phosphor
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=120, height=48)

rules = [
    (18, phosphor.check_circle, "High Contrast", "White text on dark fill\nDark text on light fill\nNever low-contrast gray", Styles.success_flat),
    (46, phosphor.arrows_out, "Perimeter Margin", "5–10% canvas buffer\nPrevent edge crowding\nBalanced whitespace", Styles.primary_flat),
    (74, phosphor.palette, "Color Meaning", "Primary: Core service\nSecondary: Data store\nAccent: Entry gateway", Styles.secondary_flat),
    (102, phosphor.puzzle_piece, "High-Level First", "Favor SmartArts\nFavor Diagrams\nAvoid manual raw math", Styles.accent_flat),
]

for x, icon_fn, title, desc, st in rules:
    rectangle(xy=(x, 24), width=24, height=36, r=2.5, style=Styles.muted_dashed)
    icon_fn(xy=(x, 34), width=7, style=st)
    text(xy=(x, 25), text=title, style=Styles.bold, size=8.5)
    text(xy=(x, 14), text=desc, style=Styles.primary, size=7.5)
```

## Summary Checklist for Production Blueprints

Before merging illustrations into production documentation:

- [ ] **Explicit Imports**: Does every ````drawlib```` block explicitly import all required symbols?
- [ ] **Aspect Ratio**: Is the canvas `width` and `height` proportioned to the diagram contents without wasted letterbox space?
- [ ] **Contrast Verification**: Is text easily readable across dark and light backgrounds?
- [ ] **Connected Flows**: Do connecting lines have directional arrowheads indicating data flow direction?
- [ ] **Incremental Verification**: Has the block been tested with `uv run drawlib show <file> <index> -g`?
