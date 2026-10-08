::: block (80, 50) (1760, 130)
# Single Source of Truth (SoT) in Git
Code, diagrams, and prose evolve together in atomic Pull Requests and compile deterministically.
:::

::: block (80, 190) (720, 770)
### Software Engineering Rigor for Documentation

1. **Atomic Pull Requests**
   - When an engineer adds a new gRPC service or database table in `src/`, they update the `drawlib` diagram block in `docs_src/` in the **exact same commit**.
2. **Code Review & Static Verification**
   - Reviewers inspect clean Python diffs instead of binary `.png` blobs.
   - CI validates every diagram block, checks internal hyperlinks (`drawlib check`), and verifies zero syntax or type errors.
3. **Deterministic Multi-Target Compilation**
   - One command (`drawlib build`) compiles `.md` + `.py` sources into HTML documentation sites, GitHub-flavored Markdown, 1920×1080 slides, and vector PDFs.
4. **Content-Addressable SQLite Caching**
   - Unchanged diagrams are restored from `.drawlib/cache.db` in **< 1ms**, making incremental rebuilds instantaneous.
:::

::: block (840, 180) (1000, 780)
```drawlib file:sot_workflow.svg
from drawlib.canvas import clear, save, setup
from drawlib.diagrams.architecture import ArchitectureDiagram, Node, NodeGroup, PhosphorIcon
from drawlib.smartarts import ChevronProcess
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=110, height=84)

# Top Section: CI/CD Workflow Pipeline via ChevronProcess
text((8, 78), "1. Git-Native Authoring & CI/CD Lifecycle", style=Styles.DarkBold.patch(text_size=11, halign="left"))

pipeline = ChevronProcess(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=9.0),
    description_style=Styles.Muted.patch(text_size=7.5),
    corner_angle=60.0,
    spacing=1.8,
    flat_left_end=True,
)
pipeline.add("1. Edit Source", description=".md & .py in Git")
pipeline.add("2. Pull Request", description="Review Python Diff", style=Styles.PrimaryNeutral)
pipeline.add(
    "3. Drawlib Build",
    description="SQLite Cache + Render",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=9.0),
    description_style=Styles.White.patch(text_size=7.5),
)
pipeline.add("4. Publish", description="Site / PDF / Slides", style=Styles.SecondaryNeutral)
pipeline.draw(xy=(6, 57), width=98.0, height=16.0)

# Bottom Section: ArchitectureDiagram showing SoT fan-out
text((8, 49), "2. One Source Directory -> Four Publishing Targets", style=Styles.DarkBold.patch(text_size=11, halign="left"))

d = ArchitectureDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=9.0),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=8.0),
    node_card_style=Styles.White,
)

sot = d.add(
    NodeGroup(title="Git SoT (*_src/)", padding=5.5, style=Styles.PrimaryNeutral),
    xy=(4.0, 4.0),
)
src_md = sot.add(Node((20, 15), "Markdown +\ndrawlib Blocks", icon=PhosphorIcon.FILE_CODE, icon_size=7.5), xy=(13.0, 26.0))
theme_py = sot.add(Node((20, 15), "styles.py &\nutils.py", icon=PhosphorIcon.PALETTE, icon_size=7.5), xy=(13.0, 9.0))

compiler = d.add(
    Node(
        (20, 15),
        "drawlib build",
        icon=PhosphorIcon.CPU,
        icon_size=8.5,
        style=Styles.White,
        card_style=Styles.PrimaryFlat,
        text_style=Styles.WhiteBold.patch(text_size=9.0),
    ),
    xy=(48.0, 21.0),
)

out_site = d.add(Node((20, 14), "HTML Docs Site", icon=PhosphorIcon.GLOBE, icon_size=7.5, card_style=Styles.SecondaryNeutral), xy=(84.0, 36.0))
out_pdf = d.add(Node((20, 14), "Vector PDF Spec", icon=PhosphorIcon.FILE_PDF, icon_size=7.5, card_style=Styles.Neutral), xy=(84.0, 21.0))
out_slide = d.add(Node((20, 14), "16:9 Slide Deck", icon=PhosphorIcon.PRESENTATION_CHART, icon_size=7.5, card_style=Styles.BlueNeutral), xy=(84.0, 6.0))

d.connect(src_md, compiler, padding=1.2)
d.connect(theme_py, compiler, padding=1.2)
compiler.fork([out_site, out_pdf, out_slide], at_x=64.0, padding=1.2)

d.draw(xy=(4.0, 2.0))
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
- When diagrams and documentation live in Git alongside application code, we achieve a true Single Source of Truth.
- On the right, we combine two Drawlib components on a single canvas—a `ChevronProcess` at the top and an `ArchitectureDiagram` at the bottom—to illustrate how `.md` files, `styles.py`, and `utils.py` flow through PR code review and `drawlib build` to produce HTML sites, vector PDFs, and 16:9 slide decks.
:::
