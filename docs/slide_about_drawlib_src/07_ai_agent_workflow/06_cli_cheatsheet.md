::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils
utils.draw_page_number()
```
:::

::: block (80, 40) (1760, 60)
# Complete CLI & Workflow Cheat Sheet
:::

::: block (80, 140) (680, 840) font:19px
## One Unified CLI (`drawlib`)

From initial project scaffolding to headless visual inspection and vector PDF publishing, every workflow is accessible through `uv run drawlib`:

### 1. Scaffold & Author
```bash
uv run drawlib init <site|doc|slide|image>
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
# Or invoke subcommands directly:
uv run drawlib build html docs_src/ -o docs_html/
uv run drawlib build pdf doc_src/ -o doc.pdf --toc
uv run drawlib build slide slide_src/ -o slide/
```
:::

::: block (780, 140) (1060, 840)
```drawlib file:cli_reference_table.svg
from drawlib.canvas import clear, save, setup
from drawlib.shapes import rectangle
from drawlib.smartarts import Table
from drawlib.styles import Colors, Styles
from drawlib.text import text

clear()
setup(width=106, height=84)

rectangle((53, 42), width=102, height=78, r=2.5, style=Styles.Neutral)
text((53, 75.5), "Drawlib Command-Line Interface Reference Matrix", style=Styles.DarkBold.patch(text_size=12.0))

table = Table(
    cell_style=Styles.White,
    text_style=Styles.Dark.patch(text_size=8.2),
    header_cell_style=Styles.PrimaryFlat,
    header_text_style=Styles.WhiteBold.patch(text_size=8.8),
    border_style=Styles.MutedThin,
    has_header=True,
)

table.set_style_cell_evenodd(
    even_color=(241, 245, 249),
    even_text_style=Styles.Dark.patch(text_size=8.2),
    odd_color=(255, 255, 255),
    odd_text_style=Styles.Dark.patch(text_size=8.2),
)
table.set_style_cell(
    background_color=(238, 242, 255),
    text_style=Styles.PrimaryBold.patch(text_size=8.2),
    rows=[1, 2, 3, 4, 5, 6, 7, 8],
    columns=[0],
)

cli_data = [
    ["CLI Command", "Primary Purpose", "Key Flags & Options"],
    ["drawlib init <type>", "Scaffold site, doc, slide, or image project", "-s <theme>, -l <lang>, --force"],
    ["drawlib build html", "Compile Markdown to multi-page or standalone HTML", "-o <dir>, -s styles.py, --no-cache"],
    ["drawlib build pdf", "Export A4 or 16:9 vector PDF via Chromium", "-o <pdf>, --toc, --page-break"],
    ["drawlib build slide", "Compile 1920x1080 widescreen HTML slide deck", "-o <dir>, -f svg|png|webp"],
    ["drawlib build md / image", "Build GitHub Markdown or batch Python scripts", "-o <dir>, -g (grid), --no-cache"],
    ["drawlib show <file> [id]", "Render single block/script (headless with -o)", "-g (coordinate grid), -o <img_path>"],
    ["drawlib serve <dir>", "Local HTTP preview server + broken link scanner", "-p 8000, --check, --no-browser"],
    ["drawlib rules / cache", "Query AI agent manuals or manage asset cache", "rules show <topic>, cache download --all"],
]

table.draw_flexible(
    xy=(6.0, 69.5),
    column_widths=[28.0, 40.0, 26.0],
    row_heights=[7.2, 6.8, 6.8, 6.8, 6.8, 6.8, 6.8, 6.8, 6.8],
    data=cli_data,
)

save()
```
:::

::: block (80, 1010) (820, 30) font:14px
*Chapter 7: AI Agent Workflow & Ecosystem — Complete CLI Cheat Sheet*
:::

::: note
- This `Table` SmartArt summarizes the entire `drawlib` CLI surface on a single slide.
- Whether you are scaffolding a new deck (`drawlib init slide`), inspecting a single diagram with a coordinate grid (`drawlib show -g -o`), checking for broken links (`drawlib serve --check`), or querying built-in agent rules (`drawlib rules show`), everything follows a consistent, ergonomic CLI design.
:::
