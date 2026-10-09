::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils
utils.draw_page_number()
```
:::

::: block (80, 40) (1760, 60)
# Four Project Archetypes (`drawlib init`)
:::

::: block (80, 140) (740, 840) font:20px
## Zero-Config Project Scaffolding

Never assemble documentation directories or build scripts manually. `drawlib init` scaffolds production-ready project structures with synchronized themes (`styles.py` + `style.css`) and modular `build_*.sh` scripts:

```bash
# 1. Multi-page documentation website with sidebar
uv run drawlib init site -s default

# 2. Linear technical specification / RFC / whitepaper
uv run drawlib init doc -s google

# 3. 16:9 widescreen presentation slide deck
uv run drawlib init slide -s default

# 4. Standalone batch Python illustration repository
uv run drawlib init image -s monochrome
```

### Strict Source-of-Truth Separation
- **Edit Only `<target>_src/`**: All human- and agent-authored Markdown, `styles.py`, and `utils.py` live in `<target>_src/`.
- **Deterministic Outputs**: `./<target>_src/build.sh` compiles `<target>_html/`, `<target>.pdf`, `<target>_markdown/`, and `<target>_images/`.
:::

::: block (860, 140) (980, 840)
```drawlib file:four_archetypes.svg
from drawlib.canvas import clear, save, setup
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.smartarts import GridLayout
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=98, height=84)

rectangle((49, 42), width=94, height=78, style=Styles.Neutral.patch(shape_r=2.5))
text((49, 75), "Drawlib Project Scaffolding Matrix (drawlib init)", style=Styles.DarkBold.patch(text_size=12.0))

# Top Hero Command Banner
rectangle(
    (49, 64.5),
    width=84,
    height=9.0,
    style=Styles.PrimaryFlat.patch(shape_r=1.8),
    text="CLI Entrypoint:   uv run drawlib init <site | doc | slide | image> [target] [-s theme] [-l lang]",
    text_style=Styles.WhiteBold.patch(text_size=9.2),
)

# 2x2 GridLayout comparing the 4 archetypes
grid = GridLayout(
    num_column=2,
    num_row=2,
    style=Styles.White.patch(shape_r=2.0),
    text_style=Styles.DarkBold.patch(text_size=9.2),
)

grid.add(
    position=(0, 1),
    width=1,
    height=1,
    style=Styles.PrimaryNeutral,
    text="1. site  (docs_src/)\n• Multi-page HTML wiki + navbar.md\n• Interactive show-code / fold-code tabs\n• Outputs: docs_html/, docs_markdown/",
    text_style=Styles.DarkBold.patch(text_size=8.6),
)
grid.add(
    position=(1, 1),
    width=1,
    height=1,
    style=Styles.SecondaryNeutral,
    text="2. doc  (doc_src/)\n• Numbered chapters (00_cover.md ..)\n• Unified standalone HTML + Auto ToC\n• Outputs: doc_html/, doc.pdf (A4 Vector)",
    text_style=Styles.DarkBold.patch(text_size=8.6),
)
grid.add(
    position=(0, 0),
    width=1,
    height=1,
    style=Styles.BlueNeutral,
    text="3. slide  (slide_src/)\n• 16:9 Widescreen Stage (1920x1080)\n• ::: block (x, y) (w, h) + ::: note\n• Outputs: slide/index.html, slide.pdf",
    text_style=Styles.DarkBold.patch(text_size=8.6),
)
grid.add(
    position=(1, 0),
    width=1,
    height=1,
    style=Styles.TealNeutral,
    text="4. image  (images_src/)\n• Pure Python scripts (*.py)\n• AST duplicate output collision guard\n• Outputs: images/*.svg, *.png, *.webp",
    text_style=Styles.DarkBold.patch(text_size=8.6),
)

grid.draw(xy=(7.0, 16.0), width=84.0, height=42.0, margin=2.0)

# Bottom Shared Foundation Bar
rectangle(
    (49, 9.5),
    width=84,
    height=7.0,
    style=Styles.White.patch(shape_r=1.5),
    text="Shared Across All 4 Archetypes:   styles.py  •  utils.py  •  _assets/  •  .drawlib/cache.sqlite3",
    text_style=Styles.DarkBold.patch(text_size=8.8),
)

save()
```
:::

::: block (80, 1010) (820, 30) font:14px
*Chapter 6: Documentation & Slide Engine — Four Project Archetypes*
:::

::: note
- Drawlib provides four specialized project archetypes out of the box via `drawlib init`:
  1. `site` for multi-page technical documentation websites with a navigation sidebar (`navbar.md`).
  2. `doc` for single-page specifications, whitepapers, and RFCs with automatic Table of Contents and A4 vector PDF export.
  3. `slide` for 16:9 widescreen presentation decks (`1920x1080`).
  4. `image` (`images`) for standalone batch Python illustration scripts.
:::
