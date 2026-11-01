::: block xy=(1700, 1010) width=140 height=30
```drawlib file=page.svg
import utils
utils.draw_page_number()
```
:::

::: block xy=(80, 40) width=1760 height=60
# Complete CLI & Workflow Cheat Sheet
:::

::: block xy=(80, 140) width=680 height=840 font_size=18px
## One Unified CLI (`drawlib`)

From initial project scaffolding to headless visual inspection and PDF / Office publishing, every workflow runs via `uv run drawlib`:

### 1. Scaffold & Author
```bash
uv run drawlib init <site|doc|slide|images>
uv run drawlib rules show overview
uv run drawlib rules show api
```

### 2. Inspect & Verify Headlessly
```bash
# Render single block with coordinate grid
uv run drawlib show page.md arch.png \
    -g -o .drawlib/scratch/preview.png

# Check links & preview in browser
uv run drawlib serve docs_html/ --check
```

### 3. Compile & Export All Targets
```bash
./docs_src/build.sh
# Or export HTML, PDF, Word & PowerPoint:
uv run drawlib build html docs_src/ -o docs_html/
uv run drawlib build pdf doc_src/ -o doc.pdf
uv run drawlib build docx doc_src/ -o doc.docx
uv run drawlib build slide slide_src/ -o slide/
uv run drawlib build pptx slide_src/ -o deck.pptx
```
:::

::: block xy=(780, 140) width=1060 height=840
```drawlib file=cli_reference_table.svg
from drawlib.canvas import clear, save, setup
from drawlib.shapes import rectangle
from drawlib.smartarts import Table
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=106, height=84)

rectangle((53, 42), width=102, height=78, style=Styles.Neutral.patch(shape_r=2.5))
text((53, 76.2), "Drawlib Command-Line Interface Reference Matrix", style=Styles.DarkBold.patch(text_size=12.0))

table = Table(
    cell_style=Styles.White,
    text_style=Styles.Dark.patch(text_size=7.9),
    header_cell_style=Styles.PrimaryFlat,
    header_text_style=Styles.WhiteBold.patch(text_size=8.6),
    border_style=Styles.MutedThin,
    has_header=True,
)

table.set_style_cell_evenodd(
    even_color=(241, 245, 249),
    even_text_style=Styles.Dark.patch(text_size=7.9),
    odd_color=(255, 255, 255),
    odd_text_style=Styles.Dark.patch(text_size=7.9),
)
table.set_style_cell(
    background_color=(30, 41, 59),
    text_style=Styles.WhiteBold.patch(text_size=8.6),
    rows=[0],
    columns=[0, 1, 2],
)
table.set_style_cell(
    background_color=(238, 242, 255),
    text_style=Styles.PrimaryBold.patch(text_size=7.9),
    rows=[1, 2, 3, 4, 5, 6, 7, 8, 9],
    columns=[0],
)

cli_data = [
    ["CLI Command", "Primary Purpose", "Key Flags & Options"],
    ["drawlib init <type>", "Scaffold site, doc, slide, or images project", "-s <theme>, -l <lang>, --force"],
    ["drawlib build html", "Compile Markdown to multi-page or doc HTML", "-o <dir>, -s styles.py, --no-cache"],
    ["drawlib build pdf", "Export A4 or 16:9 vector PDF (auto Chromium)", "-o <pdf>, --generate-index"],
    ["drawlib build docx", "Export editable MS Word (.docx) document", "-o <docx>, --generate-index"],
    ["drawlib build slide", "Compile 1920x1080 widescreen HTML slide deck", "-o <dir>, -f svg|png|webp"],
    ["drawlib build pptx", "Export editable 16:9 MS PowerPoint (.pptx)", "-o <pptx>, -t <theme>, --dpi"],
    ["drawlib build md / image", "Build GitHub Markdown or batch Python scripts", "-o <dir>, -g (grid), --no-cache"],
    ["drawlib show / serve", "Headless grid preview or HTTP + link scanner", "show -g -o, serve --check"],
    ["drawlib rules / cache", "Query AI manuals or pre-fetch assets/browser", "rules show, cache download --all"],
]

table.draw_flexible(
    xy=(6.0, 70.6),
    column_widths=[28.0, 40.0, 26.0],
    row_heights=[6.6, 6.3, 6.3, 6.3, 6.3, 6.3, 6.3, 6.3, 6.3, 6.3],
    data=cli_data,
)

save()
```
:::

::: block xy=(80, 1010) width=820 height=30 font_size=14px
*Chapter 7: AI Agent Workflow & Ecosystem — Complete CLI Cheat Sheet*
:::

::: note
- This `Table` SmartArt summarizes the entire `drawlib` CLI surface on a single slide, including optional editable MS Word (`drawlib build docx <src> -o <out.docx> --generate-index`) and 16:9 MS PowerPoint (`drawlib build pptx <src> -o <out.pptx>`) exports.
- Whether you are scaffolding a new deck (`drawlib init slide`), inspecting a single diagram with a coordinate grid (`drawlib show -g -o`), checking for broken links (`drawlib serve --check`), or pre-fetching fonts, icons, maps, and headless Chromium (`drawlib cache download --all`), everything follows a consistent, ergonomic CLI design.
:::
