::: block (80, 50) (1760, 130)
# Pain Point 1: The Tool Fragmentation Problem
Why traditional technical documentation inevitably drifts out of sync with reality.
:::

::: block (80, 200) (760, 760)
### Three Disconnected Silos

1. **Source Code in Git (`src/`)**
   - Version-controlled, peer-reviewed in Pull Requests, and continuously tested in CI/CD.
2. **Diagrams in External GUI Tools (Draw.io, Visio, Figma)**
   - Drag-and-drop canvas state lives in proprietary cloud workspaces or opaque binary/XML blobs.
   - Impossible to review meaningful diffs in Git or refactor programmatically across 30 diagrams.
3. **Prose in External Wikis / Docs (Confluence, Word, Notion)**
   - Engineers manually export `.png` screenshots and paste them into external pages.

---

### The Inevitable Result: Documentation Rot
- Updating a single microservice port requires **opening a GUI tool, re-aligning boxes, exporting a PNG, and re-uploading to a wiki**.
- Under deadline pressure, engineers skip the manual handoffs—leaving architecture diagrams **months or years out of date**.
:::

::: block (880, 190) (960, 780)
```drawlib file:fragmentation.svg
from drawlib.canvas import clear, save, setup
from drawlib.icons import phosphor
from drawlib.lines import line, line_curved
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=100, height=82)

# Top Zone: Fragmented Silos (Problem)
rectangle(
    (50, 58),
    width=92,
    height=38,
    style=Styles.MutedDashed.patch(shape_r=3),
)
text((8, 73), "Traditional Fragmented Workflow (Disconnected Silos)", style=Styles.DarkBold.patch(text_size=10.5, halign="left"))

# Silo 1: Git
rectangle((20, 55), width=24, height=22, style=Styles.Neutral.patch(shape_r=2.5))
phosphor.git_branch((20, 60), width=6.5, style=Styles.DarkBold)
text((20, 50), "Git Repo\n(Source Code)", style=Styles.DarkBold.patch(text_size=8.5))

# Silo 2: GUI Tool
rectangle((50, 55), width=24, height=22, style=Styles.PrimaryNeutral.patch(shape_r=2.5))
phosphor.bounding_box((50, 60), width=6.5, style=Styles.PrimaryBold)
text((50, 50), "GUI Canvas\n(Draw.io / Visio)", style=Styles.DarkBold.patch(text_size=8.5))

# Silo 3: External Wiki
rectangle((80, 55), width=24, height=22, style=Styles.Neutral.patch(shape_r=2.5))
phosphor.file_text((80, 60), width=6.5, style=Styles.DarkBold)
text((80, 50), "External Wiki\n(Static PNGs)", style=Styles.DarkBold.patch(text_size=8.5))

# Broken handoff arrows
line((32, 55), (38, 55), arrow_head="->", style=Styles.DangerDashed.patch(line_width=2.0))
text((35, 61), "Manual\nRedraw", style=Styles.DangerBold.patch(text_size=7.5))

line((62, 55), (68, 55), arrow_head="->", style=Styles.DangerDashed.patch(line_width=2.0))
text((65, 61), "Manual\nExport", style=Styles.DangerBold.patch(text_size=7.5))

# Bottom Zone: Drawlib Unified SoT (Solution)
rectangle(
    (50, 19),
    width=92,
    height=30,
    style=Styles.SecondaryNeutral.patch(shape_r=3),
)
text((8, 30), "The Drawlib Paradigm: Single Source of Truth in Git", style=Styles.DarkBold.patch(text_size=10.5, halign="left"))

rectangle(
    (28, 16),
    width=36,
    height=15,
    style=Styles.PrimaryFlat.patch(shape_r=2.5),
    text="Git Repository\n(.py + .md + styles.py)",
    text_style=Styles.WhiteBold.patch(text_size=9.5),
)
rectangle(
    (75, 16),
    width=30,
    height=15,
    style=Styles.Neutral.patch(shape_r=2.5),
    text="Deterministic Build\n(Site / PDF / Slides)",
    text_style=Styles.DarkBold.patch(text_size=9.5),
)
line((46, 16), (60, 16), arrow_head="->", style=Styles.DarkBold.patch(line_width=2.2))
text((53, 20.5), "drawlib build", style=Styles.PrimaryBold.patch(text_size=8.5))

save()
```
:::

::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils
utils.draw_page_number()
```
:::

::: note
- Let's examine Pain Point 1: Tool Fragmentation.
- In most engineering organizations, source code lives in Git, architecture diagrams live in external GUI canvases like Draw.io, Visio, or Figma, and technical documentation lives in external wikis.
- Every architecture change requires manual redrawing and manual PNG exporting across tools. Over time, those manual handoffs break down, causing severe documentation rot.
- Drawlib eliminates these silos by bringing code, diagrams, and documentation into a single Git repository.
:::
