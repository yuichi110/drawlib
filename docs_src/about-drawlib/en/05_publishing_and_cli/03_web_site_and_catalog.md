::: block xy=(1700, 1008) width=140 height=32
```drawlib file=page.svg
import utils
utils.draw_page_number()
```
:::

::: block xy=(80, 1010) width=900 height=30 font_size=15px
*Drawlib — Illustration & Documentation as Code*
:::

::: block xy=(80, 36) width=1760 height=72
# Web Publishing: Docs Site & API Catalog
:::

::: block xy=(80, 130) width=1760 height=115
- **`type = "site"` (Narrative Docs)**: Guided chapter navigation via `navbar.md`, full-text search, dark mode & `i18n` (`www.drawlib.com`).
- **`type = "catalog"` (API Reference)**: Zero-`navbar.md` `1 MD = 1 HTML` dictionary extracting `# H1` / badged `## H2` items with `/` instant filter (`www.drawlib.com/api`).
:::

::: block xy=(80, 260) width=1760 height=685
```drawlib file=site_vs_catalog_ui.svg
from drawlib.canvas import clear, save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.smartarts import Panel
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=176, height=68)

dots = (Styles.DangerFlat, Styles.WarningFlat, Styles.SuccessFlat)

# ==============================================================================
# Left Window: type = "site" (www.drawlib.com)
# ==============================================================================
site_win = Panel(
    'www.drawlib.com — type = "site"',
    style=Styles.White.patch(shape_r=2.2),
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=13.0),
    dot_styles=dots,
    header_variant="window",
    header_height=8.2,
)
site_win.draw(xy=(2.0, 2.5), width=83.5, height=63.5)

# Top Navigation Bar
rectangle((43.75, 53.5), width=79.5, height=6.4, style=Styles.Neutral.patch(shape_r=1.2))
phosphor.globe((7.5, 53.5), width=3.8, style=Styles.PrimaryBold)
text((11.0, 53.5), "Docs   Guide   SmartArts   CLI", style=Styles.DarkBold.patch(text_size=11.2, halign="left"))
rectangle((68.2, 53.5), width=11.0, height=4.2, style=Styles.WhiteFlat.patch(shape_r=1.0))
text((68.2, 53.5), "Search", style=Styles.Muted.patch(text_size=10.2))
rectangle((78.8, 53.5), width=7.2, height=4.2, style=Styles.PrimaryNeutral.patch(shape_r=1.0))
text((78.8, 53.5), "EN/JA", style=Styles.PrimaryBold.patch(text_size=10.0))

# Left Sidebar (navbar.md chapters)
rectangle((15.5, 26.8), width=23.0, height=43.6, style=Styles.Neutral.patch(shape_r=1.5))
text((6.0, 45.2), "navbar.md", style=Styles.Muted.patch(text_size=10.8, halign="left"))
chapters = [
    ("01 Overview", False),
    ("02 Primitives", False),
    ("03 SmartArts", True),
    ("04 Diagrams", False),
    ("05 Publishing", False),
]
for idx, (label, active) in enumerate(chapters):
    cy = 40.2 - idx * 6.4
    if active:
        rectangle((15.5, cy), width=20.6, height=5.0, style=Styles.PrimaryFlat.patch(shape_r=1.0))
        text((6.5, cy), label, style=Styles.WhiteBold.patch(text_size=11.0, halign="left"))
    else:
        text((6.5, cy), label, style=Styles.Dark.patch(text_size=11.0, halign="left"))

# Right Narrative Content Area
rectangle((56.2, 26.8), width=54.6, height=43.6, style=Styles.White.patch(shape_r=1.5))
text((31.5, 44.5), "Chapter 3  •  SmartArt Guide", style=Styles.PrimaryBold.patch(text_size=11.0, halign="left"))
text((31.5, 39.8), "Architecture & Panel Layouts", style=Styles.DarkBold.patch(text_size=13.5, halign="left"))

# Embedded Hero Diagram Preview inside site page
rectangle((56.2, 27.5), width=49.5, height=16.5, style=Styles.PrimaryNeutral.patch(shape_r=1.5))
for nx, nlabel, nicon in [(39.8, "MD Src", phosphor.file_text), (56.2, "Build", phosphor.cube), (72.6, "Web SVG", phosphor.globe)]:
    rectangle((nx, 27.5), width=12.8, height=10.5, style=Styles.WhiteFlat.patch(shape_r=1.2))
    nicon((nx, 29.6), width=3.6, style=Styles.PrimaryBold)
    text((nx, 24.4), nlabel, style=Styles.DarkBold.patch(text_size=10.2))
line((46.4, 27.5), (49.6, 27.5), arrow_head="->", style=Styles.PrimaryBold)
line((62.8, 27.5), (66.0, 27.5), arrow_head="->", style=Styles.PrimaryBold)

text(
    (31.5, 15.2),
    "Guided narrative prose, dark mode,\nand Prev / Next chapter navigation.",
    style=Styles.Dark.patch(text_size=11.0, halign="left"),
)
rectangle((40.8, 8.2), width=18.2, height=4.2, style=Styles.Neutral.patch(shape_r=1.0))
text((40.8, 8.2), "← Primitives", style=Styles.Muted.patch(text_size=10.2))
rectangle((71.8, 8.2), width=18.2, height=4.2, style=Styles.PrimaryNeutral.patch(shape_r=1.0))
text((71.8, 8.2), "Diagrams →", style=Styles.PrimaryBold.patch(text_size=10.2))

# ==============================================================================
# Right Window: type = "catalog" (www.drawlib.com/api)
# ==============================================================================
cat_win = Panel(
    'www.drawlib.com/api — type = "catalog"',
    style=Styles.PrimaryNeutral.patch(shape_r=2.2),
    header_style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=13.0),
    dot_styles=dots,
    header_variant="window",
    header_height=8.2,
)
cat_win.draw(xy=(90.5, 2.5), width=83.5, height=63.5)

# Left Sticky Filter & Auto-Extracted Index Sidebar
rectangle((107.0, 30.2), width=29.0, height=50.5, style=Styles.White.patch(shape_r=1.5))

# Instant '/' Filter Input
rectangle((107.0, 51.2), width=25.8, height=5.8, style=Styles.PrimaryNeutral.patch(shape_r=1.2))
phosphor.magnifying_glass((96.8, 51.2), width=3.4, style=Styles.PrimaryBold)
text((99.5, 51.2), "panel", style=Styles.DarkBold.patch(text_size=11.5, halign="left"))
rectangle((117.2, 51.2), width=3.6, height=3.8, style=Styles.PrimaryFlat.patch(shape_r=0.8))
text((117.2, 51.2), "/", style=Styles.WhiteBold.patch(text_size=10.5))

text((94.5, 45.2), "# SmartArts (H1)", style=Styles.Muted.patch(text_size=10.8, halign="left"))

cat_items = [
    ("CLASS", "CardList", False),
    ("CLASS", "Panel", True),
    ("FUNC", "sourcecode", False),
]
for idx, (badge, name, active) in enumerate(cat_items):
    cy = 40.2 - idx * 6.2
    if active:
        rectangle((107.0, cy), width=25.8, height=5.2, style=Styles.PrimaryFlat.patch(shape_r=1.0))
    rectangle(
        (98.2, cy),
        width=7.2,
        height=3.6,
        style=(Styles.WhiteFlat if active else Styles.SecondaryNeutral).patch(shape_r=0.8),
    )
    text(
        (98.2, cy),
        badge,
        style=(Styles.PrimaryBold if active else Styles.DarkBold).patch(text_size=9.5),
    )
    text(
        (103.0, cy),
        name,
        style=(Styles.WhiteBold if active else Styles.Dark).patch(text_size=11.2, halign="left"),
    )

text((94.5, 21.5), "# HTTP API (H1)", style=Styles.Muted.patch(text_size=10.8, halign="left"))
for idx, (badge, name) in enumerate([("GET", "/v1/rules"), ("POST", "/v1/build")]):
    cy = 16.5 - idx * 6.0
    rectangle((98.2, cy), width=7.2, height=3.6, style=Styles.PrimaryNeutral.patch(shape_r=0.8))
    text((98.2, cy), badge, style=Styles.PrimaryBold.patch(text_size=9.5))
    text((103.0, cy), name, style=Styles.Dark.patch(text_size=11.0, halign="left"))

# Right API Detail & Schema Reference Pane
rectangle((147.2, 30.2), width=48.0, height=50.5, style=Styles.White.patch(shape_r=1.5))
rectangle((129.5, 50.8), width=8.6, height=4.2, style=Styles.PrimaryFlat.patch(shape_r=1.0))
text((129.5, 50.8), "CLASS", style=Styles.WhiteBold.patch(text_size=10.2))
text((135.2, 50.8), "Panel (## H2)", style=Styles.DarkBold.patch(text_size=13.2, halign="left"))
text(
    (125.5, 45.0),
    "1 MD = 1 HTML • Zero navbar.md",
    style=Styles.Muted.patch(text_size=10.8, halign="left"),
)

# Embedded Sequence / Class Diagram Preview inside catalog item
rectangle((147.2, 31.2), width=43.6, height=18.5, style=Styles.Neutral.patch(shape_r=1.5))
rectangle((135.5, 36.2), width=16.5, height=5.0, style=Styles.PrimaryNeutral.patch(shape_r=1.0))
text((135.5, 36.2), "Caller", style=Styles.PrimaryBold.patch(text_size=10.8))
rectangle((158.8, 36.2), width=17.5, height=5.0, style=Styles.PrimaryFlat.patch(shape_r=1.0))
text((158.8, 36.2), "Panel", style=Styles.WhiteBold.patch(text_size=10.8))
line((135.5, 33.6), (135.5, 23.5), style=Styles.MutedDashed)
line((158.8, 33.6), (158.8, 23.5), style=Styles.MutedDashed)
line((135.5, 29.0), (158.8, 29.0), arrow_head="->", style=Styles.PrimaryBold)
text((147.2, 31.6), "draw() / content_box()", style=Styles.DarkBold.patch(text_size=9.6))
line((158.8, 25.0), (135.5, 25.0), arrow_head="->", style=Styles.SecondaryBold)

# Signature & Args rows
rectangle((147.2, 13.5), width=43.6, height=11.5, style=Styles.PrimaryNeutral.patch(shape_r=1.2))
text(
    (127.0, 15.8),
    "variant: 'filled' | 'window'",
    style=Styles.DarkBold.patch(text_size=10.6, halign="left"),
)
text(
    (127.0, 10.8),
    "get_content_box() -> Inner Box",
    style=Styles.PrimaryBold.patch(text_size=10.6, halign="left"),
)

save()
```
:::

::: note
When publishing technical knowledge to the web, Drawlib offers two complementary website archetypes optimized for different reader journeys:
- On the left, **`type = "site"`** powers guided narrative documentation like `www.drawlib.com`. Authors curate a deliberate learning path in `navbar.md` with numbered chapters, tutorials, full-text search, dark mode, and Prev/Next links.
- On the right, **`type = "catalog"`** (in Drawlib v0.3.10) powers high-density lookup portals like `www.drawlib.com/api`. Every Markdown file maps `1:1` to an HTML page with **zero `navbar.md` maintenance**—Drawlib automatically extracts `# H1` categories and badged `## H2` entries (`[CLASS]`, `[FUNC]`, `[GET]`, `[POST]`) into a sticky sidebar with an instant `/` keyboard filter, while keeping full support for inline Class, Sequence, and ER diagrams.
:::
