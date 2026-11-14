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
# Whitepapers: HTML, Vector PDF & MS Word
:::

::: block xy=(80, 145) width=680 height=790
## Linear Specs (`type = "doc"`)

- **Numbered Chapters**: Merge `00_cover.md`, `01_intro.md` into one spec
- **Auto Cover & ToC**: `--generate-index` builds cover & clickable index
- **Triple Export**: Compile HTML, A4 Vector PDF, and editable `.docx`

```bash
# Build all 3 deliverables from doc_src/
uv run drawlib build html
uv run drawlib build pdf --generate-index
uv run drawlib build docx --generate-index
```
:::

::: block xy=(800, 140) width=1040 height=800
```drawlib file=doc_multi_export.svg
from drawlib.canvas import clear, save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.smartarts import Panel
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=104, height=80)

# Left Panel: Linear Markdown Source Repository
src_panel = Panel(
    "doc_src/{en,ja}/",
    style=Styles.Neutral.patch(shape_r=2.2),
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=16.5),
    icon=phosphor.folder_open,
    icon_style=Styles.PrimaryBold,
    header_variant="filled",
    header_height=9.2,
)
src_panel.draw(xy=(2.0, 11.0), width=33.0, height=58.0)

files = [
    ("00_cover.md", "Title & metadata"),
    ("01_intro.md", "Context & goals"),
    ("02_arch.md", "```drawlib diagrams"),
    ("03_security.md", "Threat tables"),
]
for idx, (fname, fdesc) in enumerate(files):
    fy = 52.0 - idx * 9.2
    rectangle((18.5, fy), width=28.6, height=7.4, style=Styles.White.patch(shape_r=1.4))
    phosphor.file_text((7.2, fy), width=3.8, style=Styles.PrimaryBold)
    text((10.2, fy + 1.4), fname, style=Styles.DarkBold.patch(text_size=13.5, halign="left"))
    text((10.2, fy - 1.9), fdesc, style=Styles.Muted.patch(text_size=11.8, halign="left"))

rectangle((18.5, 16.2), width=28.6, height=6.6, style=Styles.PrimaryFlat.patch(shape_r=1.4))
text((18.5, 16.2), "--generate-index", style=Styles.WhiteBold.patch(text_size=13.5))

# Routing Spine from Source to 3 Artifact Cards
line((35.0, 40.0), (40.5, 40.0), style=Styles.PrimaryBold)
line((40.5, 14.5), (40.5, 65.5), style=Styles.PrimaryBold)
circle((40.5, 40.0), radius=1.1, style=Styles.PrimaryFlat)

outputs = [
    {
        "yc": 65.5,
        "title": "Single-Page HTML",
        "badge": "WEB",
        "icon": phosphor.globe,
        "card_style": Styles.White,
        "badge_style": Styles.SecondaryNeutral,
        "badge_text_style": Styles.DarkBold,
        "desc": "Sticky ToC sidebar, dark mode\n& responsive inline SVG zoom",
    },
    {
        "yc": 40.0,
        "title": "A4 Vector PDF",
        "badge": "PRINT",
        "icon": phosphor.file_pdf,
        "card_style": Styles.PrimaryNeutral,
        "badge_style": Styles.PrimaryFlat,
        "badge_text_style": Styles.WhiteBold,
        "desc": "Auto Cover & clickable ToC\nInfinite-zoom vector diagrams",
    },
    {
        "yc": 14.5,
        "title": "Editable Word (.docx)",
        "badge": "OFFICE",
        "icon": phosphor.file_doc,
        "card_style": Styles.White,
        "badge_style": Styles.SecondaryNeutral,
        "badge_text_style": Styles.DarkBold,
        "desc": "Native Word headings, tables\n& crisp 300 DPI illustrations",
    },
]

for out in outputs:
    yc = out["yc"]
    line((40.5, yc), (46.0, yc), arrow_head="->", style=Styles.PrimaryBold)
    rectangle((74.0, yc), width=56.0, height=21.5, style=out["card_style"].patch(shape_r=2.2))

    circle((53.5, yc), radius=5.2, style=Styles.WhiteFlat if out["card_style"] == Styles.PrimaryNeutral else Styles.PrimaryNeutral)
    out["icon"]((53.5, yc), width=5.6, style=Styles.PrimaryBold)

    text((61.2, yc + 4.8), out["title"], style=Styles.DarkBold.patch(text_size=16.0, halign="left"))
    rectangle((94.8, yc + 4.8), width=10.2, height=4.4, style=out["badge_style"].patch(shape_r=1.2))
    text((94.8, yc + 4.8), out["badge"], style=out["badge_text_style"].patch(text_size=11.5))

    text((61.2, yc - 3.2), out["desc"], style=Styles.Dark.patch(text_size=13.5, halign="left"))

save()
```
:::

::: note
For formal engineering specifications, architecture RFCs, security whitepapers, and customer deliverables, `type = "doc"` merges numbered chapter files (`00_cover.md`, `01_intro.md`, `02_arch.md`) into a single cohesive linear publication.
Passing `--generate-index` automatically synthesizes a styled Cover Page and clickable multi-level Table of Contents with page numbers.
Crucially, teams never have to maintain separate Google Docs or Word files alongside their Git repository: from the exact same `doc_src/` Markdown and Python diagrams, Drawlib compiles an interactive single-page HTML reader, an A4 print-paginated Vector PDF where every diagram path stays infinitely sharp, and a native editable Microsoft Word `.docx` document for legal, executive, or external stakeholder review.
:::
