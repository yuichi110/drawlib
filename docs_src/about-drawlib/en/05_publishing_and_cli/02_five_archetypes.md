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
# Five Built-In Project Archetypes
:::

::: block xy=(80, 130) width=1760 height=815
```drawlib file=five_archetypes_grid.svg
from drawlib.canvas import clear, save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.smartarts import Panel
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=176, height=81)

# Top unified scaffolding command banner
rectangle((88.0, 75.8), width=172.0, height=7.4, style=Styles.Neutral.patch(shape_r=2.0))
phosphor.terminal_window((10.5, 75.8), width=4.6, style=Styles.PrimaryBold)
text(
    (16.0, 75.8),
    "uv run drawlib init project <type> <dir>",
    style=Styles.PrimaryBold.patch(text_size=13.5, halign="left"),
)
text(
    (170.5, 75.8),
    "One Compiler  •  5 Purpose-Built Scaffolds  •  Web, PDF & Office",
    style=Styles.Muted.patch(text_size=12.0, halign="right"),
)

archetypes = [
    {
        "name": "site",
        "icon": phosphor.globe,
        "featured": False,
        "src": "docs_src/<lang>/",
        "use_case": "Guided narrative docs\nnavbar.md + search\nDark mode & i18n",
        "example": "e.g. www.drawlib.com",
        "outputs": ["HTML", "Search", "SVG"],
    },
    {
        "name": "catalog",
        "icon": phosphor.list_magnifying_glass,
        "featured": True,
        "src": "catalog_src/<lang>/",
        "use_case": "Two-column API ref\nAuto # H1 / ## H2\nInstant / filter",
        "example": "e.g. drawlib.com/api",
        "outputs": ["HTML", "/ Filter", "SVG"],
    },
    {
        "name": "doc",
        "icon": phosphor.file_text,
        "featured": False,
        "src": "doc_src/<lang>/",
        "use_case": "Linear whitepapers\n--generate-index\nAuto Cover & ToC",
        "example": "RFCs & Design Specs",
        "outputs": ["HTML", "PDF", "DOCX"],
    },
    {
        "name": "slide",
        "icon": phosphor.presentation_chart,
        "featured": False,
        "src": "slide_src/<lang>/",
        "use_case": "16:9 visual stage\n?presenter=1 sync\n::: note scripts",
        "example": "Keynotes & Tech Talks",
        "outputs": ["HTML", "PDF", "PPTX"],
    },
    {
        "name": "images",
        "icon": phosphor.images,
        "featured": False,
        "src": "images_src/*.py",
        "use_case": "Standalone Python\nBatch illustration\nCI asset generation",
        "example": "README & Paper Art",
        "outputs": ["SVG", "PNG", "WebP"],
    },
]

card_w = 32.4
card_h = 66.8
gap = 2.5

for idx, item in enumerate(archetypes):
    x0 = 2.0 + idx * (card_w + gap)
    cx = x0 + card_w / 2.0
    is_feat = item["featured"]

    panel = Panel(
        item["name"],
        style=(Styles.PrimaryNeutral if is_feat else Styles.White).patch(shape_r=2.2),
        header_style=Styles.PrimaryFlat if is_feat else Styles.SecondaryNeutral,
        text_style=(Styles.WhiteBold if is_feat else Styles.DarkBold).patch(text_size=15.5),
        header_variant="filled",
        header_height=9.2,
        header_align="center",
    )
    panel.draw(xy=(x0, 2.5), width=card_w, height=card_h)

    if is_feat:
        rectangle((cx, 56.8), width=18.5, height=3.8, style=Styles.AccentFlat.patch(shape_r=1.8))
        text((cx, 56.8), "NEW in v0.3.10", style=Styles.WhiteBold.patch(text_size=10.5))

    circle_y = 48.8 if is_feat else 51.0
    circle(
        (cx, circle_y),
        radius=5.0,
        style=Styles.WhiteFlat if is_feat else Styles.PrimaryNeutral,
    )
    item["icon"]((cx, circle_y), width=5.6, style=Styles.PrimaryBold)

    # Source folder badge
    src_y = 39.2
    rectangle(
        (cx, src_y),
        width=28.4,
        height=5.6,
        style=(Styles.WhiteFlat if is_feat else Styles.Neutral).patch(shape_r=1.4),
    )
    text((cx, src_y), item["src"], style=Styles.PrimaryBold.patch(text_size=11.2))

    # Primary use case lines
    text((cx, 28.0), item["use_case"], style=Styles.Dark.patch(text_size=11.6))
    text((cx, 18.8), item["example"], style=Styles.Muted.patch(text_size=10.8))

    line((x0 + 2.4, 15.6), (x0 + card_w - 2.4, 15.6), style=Styles.Muted)

    # Output format badges
    outs = item["outputs"]
    bw = 8.8
    bgap = 1.0
    start_bx = cx - (len(outs) * bw + (len(outs) - 1) * bgap) / 2.0 + bw / 2.0
    for b_idx, out_label in enumerate(outs):
        bx = start_bx + b_idx * (bw + bgap)
        is_primary_out = is_feat and b_idx == 1
        rectangle(
            (bx, 9.2),
            width=bw,
            height=5.2,
            style=(Styles.PrimaryFlat if is_primary_out else Styles.SecondaryNeutral).patch(shape_r=1.2),
        )
        text(
            (bx, 9.2),
            out_label,
            style=(Styles.WhiteBold if is_primary_out else Styles.DarkBold).patch(text_size=10.5),
        )

save()
```
:::

::: note
Drawlib provides five built-in project archetypes via `uv run drawlib init project <type> <dir>`, each tailored to a distinct engineering communication workflow while sharing the exact same Python illustration engine and `drawlib.toml` configuration model:
1. **`site`**: Multi-page documentation portals (`docs_src/<lang>/` + `navbar.md`) that compile into responsive HTML websites with client-side full-text search, dark mode, and multi-locale switching—powering `www.drawlib.com`.
2. **`catalog`** *(New in v0.3.10)*: Two-column API, schema, and rulebook reference sites (`catalog_src/<lang>/`, `1 Markdown = 1 HTML`) that automatically extract `# H1` categories and badged `## H2` entries with an instant `/` keyboard filter and zero `navbar.md` maintenance—powering `www.drawlib.com/api`.
3. **`doc`**: Linear multi-chapter specifications and whitepapers (`doc_src/<lang>/`) that compile into single-page HTML, A4 Vector PDF with `--generate-index` Cover/ToC pages, and native editable Microsoft Word (`.docx`).
4. **`slide`**: 16:9 widescreen presentation decks (`slide_src/<lang>/`) combining `1920×1080` `::: block` visuals and `::: note` speaker scripts into synchronized `?presenter=1` HTML, Vector PDF, and editable `960×540pt` PowerPoint (`.pptx`).
5. **`images`**: Standalone Python batch illustration suites (`images_src/*.py`) outputting crisp `SVG`, `PNG`, `WebP`, and `PDF` assets for papers, READMEs, and CI pipelines.
:::
