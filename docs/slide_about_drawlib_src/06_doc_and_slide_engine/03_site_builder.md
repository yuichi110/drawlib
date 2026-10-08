::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils
utils.draw_page_number()
```
:::

::: block (80, 40) (1760, 60)
# Multi-Page Documentation Sites (`site`)
:::

::: block (80, 140) (740, 840) font:20px
## Technical Portals & GitHub Mirrors

A `site` project (`docs_src/`) compiles nested Markdown folders into both a responsive HTML documentation portal (`docs_html/`) and a GitHub-browsable Markdown mirror (`docs_markdown/`).

### Core `site` Capabilities
- **Declarative Sidebar (`navbar.md`)**:
  - `# Brand Title` sets the top-left header; `## Section` groups links into collapsible categories; every internal `.md` link is validated at build time.
- **Interactive Code Tabs (`show-code` / `fold-code`)**:
  - Adding `show-code` to a ```` ```drawlib ```` fence renders an interactive UI card allowing readers to toggle between the **Rendered Diagram** and **Copyable Python Source**.
- **Pre-Flight Link & Asset Scanner (`drawlib serve --check`)**:
  - `scan_broken_links()` verifies all internal `<a href>` links, section anchors, and `<img src>` assets before launching the live preview server.
:::

::: block (860, 140) (980, 840)
```drawlib file:site_architecture.svg
from drawlib.canvas import clear, save, setup
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=98, height=84)

rectangle((49, 42), width=94, height=78, r=2.5, style=Styles.Neutral)
text((49, 75), "Multi-Page Site Compiler & Interactive Page Anatomy", style=Styles.DarkBold.patch(text_size=11.8))

# Top Pipeline: Source -> Compiler -> Dual Targets
rectangle(
    (19.0, 62.5),
    width=24.0,
    height=13.0,
    r=1.5,
    style=Styles.PrimaryNeutral,
    text="docs_src/\n• index.md & navbar.md\n• Nested */*.md pages",
    text_style=Styles.DarkBold.patch(text_size=8.2),
)
rectangle(
    (49.0, 62.5),
    width=22.0,
    height=13.0,
    r=1.5,
    style=Styles.PrimaryFlat,
    text="Site Compiler\ndrawlib build html\ndrawlib build md",
    text_style=Styles.WhiteBold.patch(text_size=8.5),
)
rectangle(
    (78.5, 66.0),
    width=24.0,
    height=6.0,
    r=1.2,
    style=Styles.SecondaryNeutral,
    text="docs_html/ (Web Portal)",
    text_style=Styles.DarkBold.patch(text_size=8.2),
)
rectangle(
    (78.5, 59.0),
    width=24.0,
    height=6.0,
    r=1.2,
    style=Styles.BlueNeutral,
    text="docs_markdown/ (GitHub)",
    text_style=Styles.DarkBold.patch(text_size=8.2),
)
line((31.0, 62.5), (38.0, 62.5), arrow_head="->", style=Styles.DarkBold)
line((60.0, 64.5), (66.5, 66.0), arrow_head="->", style=Styles.DarkBold)
line((60.0, 60.5), (66.5, 59.0), arrow_head="->", style=Styles.DarkBold)

# Bottom Mockup: Compiled docs_html/ Browser Window
rectangle((49.0, 29.0), width=86.0, height=44.0, r=2.0, style=Styles.White)
rectangle(
    (49.0, 48.0),
    width=86.0,
    height=6.0,
    r=1.0,
    style=Styles.DarkFlat,
    text="Browser Preview:  http://localhost:8000/architecture/index.html   [drawlib serve --check: 0 broken links]",
    text_style=Styles.WhiteBold.patch(text_size=8.2),
)

# Left Sidebar from navbar.md
rectangle((19.5, 26.0), width=23.0, height=34.0, r=1.2, style=Styles.PrimaryNeutral)
text((19.5, 39.5), "navbar.md Sidebar", style=Styles.PrimaryBold.patch(text_size=8.5))
rectangle((19.5, 34.0), width=19.5, height=4.2, r=0.8, style=Styles.White, text="Home (index.md)", text_style=Styles.Dark.patch(text_size=7.8))
rectangle((19.5, 28.5), width=19.5, height=4.2, r=0.8, style=Styles.PrimaryFlat, text="• Cloud Architecture", text_style=Styles.WhiteBold.patch(text_size=7.8))
rectangle((19.5, 23.0), width=19.5, height=4.2, r=0.8, style=Styles.White, text="API Sequence Flows", text_style=Styles.Dark.patch(text_size=7.8))
rectangle((19.5, 17.5), width=19.5, height=4.2, r=0.8, style=Styles.White, text="Database ER Models", text_style=Styles.Dark.patch(text_size=7.8))
text((19.5, 12.0), "Active Page Highlighted", style=Styles.MutedBold.patch(text_size=7.5))

# Right Content Pane with show-code Interactive Card
rectangle((61.5, 26.0), width=55.0, height=34.0, r=1.2, style=Styles.Neutral)
text((37.0, 39.5), "# Cloud Architecture Specification", style=Styles.DarkBold.patch(text_size=9.2, halign="left"))

# Interactive show-code container inside page
rectangle((61.5, 23.5), width=49.0, height=23.0, r=1.5, style=Styles.White)
rectangle((47.0, 32.5), width=18.0, height=4.0, r=0.8, style=Styles.PrimaryFlat, text="[Tab 1] Diagram", text_style=Styles.WhiteBold.patch(text_size=7.5))
rectangle((66.5, 32.5), width=18.0, height=4.0, r=0.8, style=Styles.PrimaryNeutral, text="[Tab 2] Python Code", text_style=Styles.DarkBold.patch(text_size=7.5))
rectangle(
    (61.5, 20.5),
    width=44.0,
    height=15.0,
    r=1.0,
    style=Styles.SecondaryNeutral,
    text="Rendered Vector SVG / PNG Illustration\n+ Synchronized Python Source Code (show-code)",
    text_style=Styles.DarkBold.patch(text_size=8.2),
)

save()
```
:::

::: block (80, 1010) (820, 30) font:14px
*Chapter 6: Documentation & Slide Engine — Multi-Page Documentation Sites (site)*
:::

::: note
- Drawlib's own official documentation (`docs/docs_src/`) uses the `site` archetype.
- `navbar.md` controls the hierarchical sidebar on the left and validates every linked Markdown file at compile time.
- With `show-code`, readers can inspect the rendered diagram alongside the exact Python code that produced it, and `drawlib serve --check` verifies that zero broken links or missing images exist across the entire site.
:::
