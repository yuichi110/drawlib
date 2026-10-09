::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils
utils.draw_page_number()
```
:::

::: block (80, 40) (1760, 60)
# Single-Page Technical Docs & Vector PDFs (`doc` & `pdf`)
:::

::: block (80, 140) (740, 840) font:20px
## Chapter-Merged Whitepapers & RFCs

The `doc` archetype (`doc_src/`) is purpose-built for linear technical documents—such as architecture RFCs, whitepapers, and quickstart manuals:

```text
doc_src/
├── 00_cover.md          # Title, subtitle, author metadata
├── 01_introduction.md   # Chapter 1
├── 02_architecture.md   # Chapter 2 (with ```drawlib blocks)
└── 03_benchmarks.md     # Chapter 3
```

### Dual Publication Outputs from One Source
1. **Unified Standalone Web Document (`doc_html/index.html`)**:
   - Merges all numbered `.md` chapters in sorted order into a single `index.html` with an auto-generated **Table of Contents**, a centered **900px reading container**, and full `file://` portability.
2. **Print-Ready Vector PDF (`doc.pdf`)**:
   - `drawlib build pdf --toc --page-break` launches headless **Playwright / Chromium** (`page.pdf()`) to render crisp vector diagrams, web fonts, and A4 page breaks with deterministic metadata.
:::

::: block (860, 140) (980, 840)
```drawlib file:doc_pdf_pipeline.svg
from drawlib.canvas import clear, save, setup
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=98, height=84)

rectangle((49, 42), width=94, height=78, style=Styles.Neutral.patch(shape_r=2.5))
text((49, 75), "Linear Document & Headless Vector PDF Pipeline", style=Styles.DarkBold.patch(text_size=12.0))

# Left Column: Ordered Markdown Chapters
rectangle((18.5, 42.0), width=23.0, height=54.0, style=Styles.PrimaryNeutral.patch(shape_r=2.0))
text((18.5, 64.5), "doc_src/ Chapters", style=Styles.PrimaryBold.patch(text_size=9.5))

ch_files = [
    ("00_cover.md", "Cover & Metadata"),
    ("01_overview.md", "Executive Summary"),
    ("02_design.md", "Architecture + Diagrams"),
    ("03_metrics.md", "Charts & Benchmarks"),
]
for i, (fname, desc) in enumerate(ch_files):
    cy = 55.0 - i * 11.5
    rectangle(
        (18.5, cy),
        width=19.5,
        height=8.8,
        style=Styles.White.patch(shape_r=1.2),
        text=f"{fname}\n{desc}",
        text_style=Styles.DarkBold.patch(text_size=7.8),
    )

# Center: Document Merger & Auto-ToC Engine
rectangle(
    (48.0, 42.0),
    width=21.0,
    height=28.0,
    style=Styles.PrimaryFlat.patch(shape_r=2.0),
    text="Document Merger\n& Block Processor\n\n• Sort 00..03\n• Render Diagrams\n• Generate ToC\n• Inject Page Breaks",
    text_style=Styles.WhiteBold.patch(text_size=8.2),
)
line((30.0, 42.0), (37.5, 42.0), arrow_head="->", style=Styles.DarkBold)

# Right Top: Standalone index.html (900px centered reading view)
rectangle((78.5, 56.5), width=25.0, height=25.0, style=Styles.SecondaryNeutral.patch(shape_r=2.0))
text((78.5, 65.5), "1. Standalone Web Doc", style=Styles.DarkBold.patch(text_size=9.0))
rectangle(
    (78.5, 53.5),
    width=21.0,
    height=15.0,
    style=Styles.White.patch(shape_r=1.2),
    text="doc_html/index.html\n• Centered 900px layout\n• Interactive ToC links\n• Works via file://",
    text_style=Styles.Dark.patch(text_size=7.8),
)

# Right Bottom: Headless Chromium Vector PDF
rectangle((78.5, 25.5), width=25.0, height=27.0, style=Styles.BlueNeutral.patch(shape_r=2.0))
text((78.5, 35.5), "2. Vector PDF Export", style=Styles.DarkBold.patch(text_size=9.0))
rectangle(
    (78.5, 22.5),
    width=21.0,
    height=16.5,
    style=Styles.AccentFlat.patch(shape_r=1.2),
    text="Playwright + Chromium\n--> doc.pdf (A4)\n• Crisp Vector Graphics\n• CSS @page Breaks",
    text_style=Styles.WhiteBold.patch(text_size=7.8),
)

line((58.5, 48.0), (66.0, 56.5), arrow_head="->", style=Styles.DarkBold)
line((58.5, 36.0), (66.0, 25.5), arrow_head="->", style=Styles.DarkBold)

save()
```
:::

::: block (80, 1010) (820, 30) font:14px
*Chapter 6: Documentation & Slide Engine — Single-Page Technical Docs & Vector PDFs*
:::

::: note
- In Drawlib's own repository, both the Quickstart Guide (`docs/quickstart_src/`) and the Dogfooding Whitepapers (`docs/drawlib-dogfooding_src/`) use the `doc` archetype.
- Authors write modular chapter files (`00_cover.md`, `01_overview.md`, ...), and Drawlib compiles them into both a single-page `index.html` and a print-ready A4 vector PDF via headless Chromium.
:::
