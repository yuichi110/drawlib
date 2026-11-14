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
# Key Takeaways & Quickstart
:::

::: block xy=(80, 130) width=1760 height=815
```drawlib file=summary_takeaways.svg
from drawlib.canvas import clear, save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.smartarts import CardList
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=176, height=81)

# Top 2x2 Grid of Takeaway Cards using two side-by-side CardList instances
left_cards = CardList(
    style=Styles.White.patch(shape_r=2.2),
    text_style=Styles.DarkBold.patch(text_size=14.6),
    description_style=Styles.Dark.patch(text_size=11.8),
    badge_shape="rounded_rect",
    badge_style=Styles.PrimaryNeutral,
    badge_text_style=Styles.PrimaryBold.patch(text_size=11.5),
    icon_style=Styles.PrimaryBold,
    direction="vertical",
    spacing=3.5,
)
left_cards.add(
    "1. Pure Python & Git Native",
    "Typed Python API, styles.py tokens & clean\nGit PR diffs — zero GUI lock-in.",
    badge_text="01",
    icon=phosphor.git_branch,
)
left_cards.add(
    "3. 5 Project Archetypes & Office Export",
    "Compile Site, Catalog, Doc, Slide & Images\nto HTML, Vector PDF, DOCX & PPTX.",
    badge_text="03",
    icon=phosphor.browsers,
)
left_cards.draw(xy=(2.0, 26.5), width=84.5, height=52.0)

right_cards = CardList(
    style=Styles.White.patch(shape_r=2.2),
    text_style=Styles.DarkBold.patch(text_size=14.6),
    description_style=Styles.Dark.patch(text_size=11.8),
    badge_shape="rounded_rect",
    badge_style=Styles.PrimaryNeutral,
    badge_text_style=Styles.PrimaryBold.patch(text_size=11.5),
    icon_style=Styles.PrimaryBold,
    direction="vertical",
    spacing=3.5,
)
right_cards.add(
    "2. Rich High-Level Components",
    "18 SmartArts, 10 Charts, 6 Diagrams, 5 Graph\nsolvers & 34 Icon Packs built in.",
    badge_text="02",
    icon=phosphor.cube,
)
right_cards.add(
    "4. Built for Autonomous AI Agents",
    "50+ drawlib rules topics, show -g grid QA &\n< 1s SQLite .drawlib/cache.db builds.",
    badge_text="04",
    icon=phosphor.robot,
    style=Styles.PrimaryNeutral.patch(shape_r=2.2),
    badge_style=Styles.PrimaryFlat,
    badge_text_style=Styles.WhiteBold.patch(text_size=11.5),
    icon_style=Styles.WhiteBold,
)
right_cards.draw(xy=(89.5, 26.5), width=84.5, height=52.0)

# Bottom Dark/Primary Quickstart Banner (height ~22)
rectangle((88.0, 12.8), width=172.0, height=21.0, style=Styles.DarkFlat.patch(shape_r=2.5))
phosphor.terminal_window((9.5, 19.2), width=4.2, style=Styles.WhiteBold)
text(
    (14.5, 19.2),
    "QUICKSTART IN 30 SECONDS",
    style=Styles.WhiteBold.patch(text_size=12.2, halign="left"),
)
text(
    (170.0, 19.2),
    "Requires Python 3.11+ & uv",
    style=Styles.White.patch(text_size=11.2, halign="right"),
)

# 3 Command Pills inside Quickstart Banner
rectangle((26.5, 9.2), width=40.0, height=9.2, style=Styles.WhiteFlat.patch(shape_r=1.6))
text((26.5, 9.2), "uv add drawlib", style=Styles.DarkBold.patch(text_size=13.0))

line((47.5, 9.2), (53.5, 9.2), arrow_head="->", style=Styles.WhiteBold)

rectangle((88.0, 9.2), width=66.0, height=9.2, style=Styles.WhiteFlat.patch(shape_r=1.6))
text(
    (88.0, 9.2),
    "uv run drawlib init project slide my-deck",
    style=Styles.DarkBold.patch(text_size=12.6),
)

line((122.0, 9.2), (128.0, 9.2), arrow_head="->", style=Styles.WhiteBold)

rectangle((149.5, 9.2), width=41.0, height=9.2, style=Styles.PrimaryFlat.patch(shape_r=1.6))
text((149.5, 9.2), "uv run drawlib serve", style=Styles.WhiteBold.patch(text_size=13.0))

save()
```
:::

::: note
Let us recap the four pillars that set Drawlib apart:
1. **Pure Python & Git Native**: Every illustration and document lives in clean, typed Python and Markdown files with shared `styles.py` design tokens and human-readable pull request diffs.
2. **Rich High-Level Components**: 18 SmartArts, 10 Charts, 6 Diagrams, 5 deterministic Graph layout solvers, and 34 icon suites let you express complex architectures without tedious box-and-line micromanagement.
3. **5 Project Archetypes & Office Export**: One compiler builds Web Docs (`site`), API Catalogs (`catalog`), Whitepapers (`doc`), 16:9 Slide Decks (`slide`), and Batch Asset Suites (`images`)—exporting HTML, Vector PDF, MS Word (`.docx`), and PowerPoint (`.pptx`).
4. **Built for Autonomous AI Agents**: 50+ `drawlib rules` topics, multimodal `show -g` coordinate grid verification, and sub-second `.drawlib/cache.db` SQLite caching turn AI agents into reliable visual authors.
Getting started takes three commands: `uv add drawlib`, `uv run drawlib init project slide my-deck`, and `uv run drawlib serve`.
:::
