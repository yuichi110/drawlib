# Multi-Language Documentation Showcase

Welcome to the multi-language documentation showcase built with [Drawlib](https://github.com/yuichi110/drawlib). Driven by a single `i18n.toml` manifest, this site compiles English (`en/`) and Japanese (`ja/`) Markdown trees into a unified static portal with shared diagram assets, automatic link rebasing, and a built-in language switcher.

```drawlib align=center code=fold file=i18n_site_hero.png caption="Multi-Language Site Build Pipeline: From Locale Trees and Parity Checks to Unified Static Output"
from drawlib.canvas import setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=152, height=74)

# Layer 1: Outer structural boundary (6.0-unit perimeter margin)
rectangle((76.0, 37.0), width=140.0, height=62.0, style=Styles.MutedDashed.patch(shape_r=2.5))
text(
    (76.0, 63.0),
    "Multi-Language Site Build Architecture (i18n.toml)",
    style=Styles.DarkBold.patch(text_size=13.0),
)

# Layer 2: Inter-stage pipeline connectors (snapped to card boundary ports)
line((49.0, 34.0), (58.0, 34.0), arrow_head="->", style=Styles.DarkBold)
line((94.0, 34.0), (103.0, 34.0), arrow_head="->", style=Styles.DarkBold)

# Layer 3A: Stage 1 — Locale Source Tree (Neutral container + tinted-neutral sub-cards)
rectangle((30.0, 34.0), width=38.0, height=47.0, style=Styles.Neutral.patch(shape_r=2.0))
phosphor.folder_open((16.2, 52.5), width=4.2, style=Styles.PrimaryBold)
text((19.8, 52.5), "1. Source Tree", style=Styles.DarkBold.patch(text_size=11.5, halign="left"))

rectangle((30.0, 41.0), width=33.5, height=12.5, style=Styles.PrimaryNeutral.patch(shape_r=1.5))
phosphor.gear((17.4, 41.0), width=4.0, style=Styles.PrimaryBold)
text((21.0, 43.2), "i18n.toml + Shared", style=Styles.DarkBold.patch(text_size=10.5, halign="left"))
text((21.0, 38.6), "styles.py / utils.py", style=Styles.Dark.patch(text_size=10.5, halign="left"))

rectangle((30.0, 22.8), width=33.5, height=19.0, style=Styles.SecondaryNeutral.patch(shape_r=1.5))
phosphor.globe((17.4, 28.0), width=4.0, style=Styles.SecondaryBold)
text((21.0, 28.0), "en/ & ja/ Locales", style=Styles.DarkBold.patch(text_size=10.5, halign="left"))
text((15.8, 22.0), "• navbar.md + *.md", style=Styles.Dark.patch(text_size=10.5, halign="left"))
text((15.8, 17.2), "• Shared drawlib code", style=Styles.Dark.patch(text_size=10.5, halign="left"))

# Layer 3B: Stage 2 — Single PrimaryFlat Focal Card (4 Pre-Flight Parity Checks)
rectangle((76.0, 34.0), width=36.0, height=47.0, style=Styles.PrimaryFlat.patch(shape_r=2.0))
phosphor.shield_check((63.2, 52.0), width=4.4, style=Styles.WhiteBold)
text((66.9, 52.0), "4 Parity Checks", style=Styles.WhiteBold.patch(text_size=11.5, halign="left"))
line((61.5, 47.5), (90.5, 47.5), style=Styles.White.patch(line_width=1.0))

checks = [
    (42.2, "1. File Set"),
    (35.2, "2. navbar.md"),
    (28.2, "3. Skeleton Sequence"),
    (21.2, "4. Drawlib Code"),
]
for cy, label in checks:
    phosphor.check_circle((62.6, cy), width=3.4, style=Styles.WhiteBold)
    text((65.8, cy), label, style=Styles.WhiteBold.patch(text_size=10.5, halign="left"))

text((76.0, 14.2), "Fail-Fast Pre-Flight", style=Styles.White.patch(text_size=10.5))

# Layer 3C: Stage 3 — Compiled Multi-Locale Output (Neutral container + neutral sub-cards)
rectangle((122.0, 34.0), width=38.0, height=47.0, style=Styles.Neutral.patch(shape_r=2.0))
phosphor.browser((108.2, 52.5), width=4.2, style=Styles.PrimaryBold)
text((111.8, 52.5), "3. Unified Output", style=Styles.DarkBold.patch(text_size=11.5, halign="left"))

rectangle((122.0, 42.3), width=33.5, height=10.2, style=Styles.PrimaryNeutral.patch(shape_r=1.5))
phosphor.package((109.2, 42.3), width=3.8, style=Styles.PrimaryBold)
text((112.8, 44.4), "Shared images/", style=Styles.DarkBold.patch(text_size=10.5, halign="left"))
text((112.8, 40.0), "Rendered once total", style=Styles.Dark.patch(text_size=10.5, halign="left"))

rectangle((122.0, 30.3), width=33.5, height=10.2, style=Styles.SecondaryNeutral.patch(shape_r=1.5))
phosphor.file_code((109.2, 30.3), width=3.8, style=Styles.SecondaryBold)
text((112.8, 32.4), "Root index.html", style=Styles.DarkBold.patch(text_size=10.5, halign="left"))
text((112.8, 28.0), "Auto-rebased links", style=Styles.Dark.patch(text_size=10.5, halign="left"))

rectangle((122.0, 18.3), width=33.5, height=10.2, style=Styles.PrimaryNeutral.patch(shape_r=1.5))
phosphor.globe((109.2, 18.3), width=3.8, style=Styles.PrimaryBold)
text((112.8, 20.4), "en/ & ja/ Locales", style=Styles.DarkBold.patch(text_size=10.5, halign="left"))
text((112.8, 16.0), "hreflang + Switcher", style=Styles.Dark.patch(text_size=10.5, halign="left"))
```

## 1. Mechanical Parity & Single-Render Architecture

Multi-language documentation sites frequently suffer from silent translation drift when new pages, sidebar links, or architectural diagrams are updated in one language but forgotten in another. Drawlib eliminates structural drift before rendering a single pixel by validating every locale directory against `default_lang` (`en/`) through four automated pre-flight checks:

- **1. File Set Parity**: Every locale directory (`en/`, `ja/`) must contain the exact same set of relative `.md` and `.html` document paths.
- **2. Sidebar Navigation Parity (`navbar.md`)**: Category section counts, heading presence, item counts, and normalized link targets must match across all locales while allowing natural localized labels.
- **3. Markdown Skeleton Sequence Parity**: The ordered structural sequence of `Heading(H1..H3)`, `MarkdownText`, `DrawlibBlock`, and `CodeBlock` tokens must match `default_lang`. Consecutive paragraphs, bullet lists, tables, and blockquotes collapse into a single `MarkdownText` token so translators retain full phrasing freedom.
- **4. Shared vs. Localized Drawlib Code Parity**: Shared diagrams (`file=<name>.png`) keep identical Python code across locales and are rendered **once** into `images/`, while intentionally localized diagrams opt in explicitly via `file=<stem>_<lang>.png`.

```drawlib align=center code=fold file=i18n_parity_matrix.png caption="Four Pre-Flight Mechanical Parity Checks Enforced Across All Locales"
from drawlib.canvas import setup
from drawlib.icons import phosphor
from drawlib.smartarts import Table
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=156, height=62)

phosphor.shield_check((39.0, 54.2), width=4.4, style=Styles.PrimaryBold)
text(
    (43.0, 54.2),
    "4 Pre-Flight Mechanical Parity Checks (Enforced on Build)",
    style=Styles.DarkBold.patch(text_size=12.5, halign="left"),
)

table = Table(
    cell_style=Styles.White,
    text_style=Styles.Dark.patch(text_size=10.5),
    header_cell_style=Styles.PrimaryFlat,
    header_text_style=Styles.WhiteBold.patch(text_size=11.0),
    border_style=Styles.MutedThin,
)

table.set_style_cell_evenodd(
    even_color=Colors.PrimaryNeutral,
    even_text_style=Styles.Dark.patch(text_size=10.5),
    odd_color=Colors.White,
    odd_text_style=Styles.Dark.patch(text_size=10.5),
)
table.set_style_cell(
    background_color=Colors.White,
    text_style=Styles.DarkBold.patch(text_size=10.5),
    rows=[1, 3],
    columns=[0],
)
table.set_style_cell(
    background_color=Colors.PrimaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=10.5),
    rows=[2, 4],
    columns=[0],
)
table.set_style_cell_header(
    background_color=Colors.Primary,
    text_style=Styles.WhiteBold.patch(text_size=11.0),
)

table.set_style_border(
    top=Styles.Dark.patch(line_width=1.5),
    top2=Styles.Dark.patch(line_width=1.2),
    bottom=Styles.Dark.patch(line_width=1.5),
    left=Styles.MutedThin,
    left2=Styles.Muted,
    right=Styles.MutedThin,
    between_columns=Styles.MutedThin,
    between_rows=Styles.MutedThin,
)

parity_rows = [
    ["Parity Check", "Target Scope", "Enforced Invariant (vs. default_lang)", "Allowed Localization"],
    ["1. File Set", "<lang>/**/*.md", "Identical relative page paths", "Localized page prose"],
    ["2. navbar.md", "<lang>/navbar.md", "Same sections, counts & link targets", "Localized nav labels"],
    ["3. Skeleton Sequence", "H1-H3, Prose, Blocks", "Same ordered structural token list", "Free paragraphs & lists"],
    ["4. Drawlib Code", "file=<name>.png", "Identical Python code (or _<lang>.png)", "Localized captions"],
]

table.draw_flexible(
    xy=(6.0, 48.0),
    column_widths=[31.0, 29.0, 53.0, 31.0],
    row_heights=[8.8, 8.2, 8.2, 8.2, 8.2],
    data=parity_rows,
    align="top_left",
)
```

## 2. Explore the Showcase Chapters

Once all parity checks pass, Drawlib compiles localized pages (`en/**/*.html`, `ja/**/*.html`) with `<html lang="...">`, Google Fonts stylesheets, `hreflang` metadata, and a top-right language switcher, while generating the root landing page (`index.html`) directly from `default_lang` with automatically rebased relative URLs. Explore the chapters below to see multi-language diagramming in action:

- **[System Architecture](architecture/index.md)**: Cloud microservice topology, shared project-wide theming via `styles.py` and `utils.py`, and single-render architecture diagrams shared across locales.
- **[Localization Workflow](workflow/index.md)**: Step-by-step multi-locale authoring workflow, skeleton token collapsing behavior, and opt-in localized CJK diagrams (`file=<stem>_<lang>.png`).
