# Documentation as Code: The Drawlib Build Engine

Drawlib unifies technical documentation and architectural illustrations under a single **"Documentation as Code"** pipeline. Instead of managing out-of-sync vector files, manually exporting diagrams from third-party tools, or checking in opaque binary assets, you author declarative Python drawing blocks directly inside standard Markdown documents.

---

## 1. Core Principles

```drawlib fold-code 650px center file:doc_builder_overview_pipeline.png caption:"The Drawlib Documentation Compilation Pipeline and Publishing Targets"
from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=150, height=62)

# Left: Markdown Source
rectangle(
    (22, 31),
    width=32,
    height=42,
    style=Styles.Neutral.patch(shape_r=2.0),
    text="Markdown Source\n(docs_src/*.md +\nstyles.py)\n\n• Embedded drawlib blocks\n• utils.py & _assets/*",
    text_style=Styles.Dark.patch(text_size=8.0),
)

# Center: Drawlib Compilation Pipeline Container
rectangle((75, 31), width=44, height=50, style=Styles.MutedDashed.patch(shape_r=2.5))
text((75, 51.5), "Drawlib Compilation Pipeline", style=Styles.DarkBold.patch(text_size=8.5))

rectangle(
    (75, 41),
    width=38,
    height=9,
    style=Styles.PrimaryNeutral.patch(shape_r=1.5),
    text="1. Markdown Parser",
    text_style=Styles.DarkBold.patch(text_size=8.0),
)
line((75, 36.5), (75, 32.5), arrow_head="->", style=Styles.DarkBold)

rectangle(
    (75, 28),
    width=38,
    height=9,
    style=Styles.PrimaryFlat.patch(shape_r=1.5),
    text="2. Python Sandbox",
    text_style=Styles.WhiteBold.patch(text_size=8.0),
)
line((75, 23.5), (75, 19.5), arrow_head="->", style=Styles.DarkBold)

rectangle(
    (75, 15),
    width=38,
    height=9,
    style=Styles.SecondaryNeutral.patch(shape_r=1.5),
    text="3. SQLite Cache (.drawlib/cache.db)",
    text_style=Styles.DarkBold.patch(text_size=7.5),
)

# Right: 4 Publishing Targets
targets = [
    (49.5, "docs_html/ (Web Site)", Styles.PrimaryNeutral),
    (37.2, "docs_markdown/ (GitHub MD)", Styles.Neutral),
    (24.8, "docs.pdf (Print PDF)", Styles.SecondaryNeutral),
    (12.5, "docs_images/ (Extracted Assets)", Styles.Neutral),
]
for ty, label, st in targets:
    rectangle(
        (127, ty),
        width=34,
        height=9.5,
        style=st.patch(shape_r=1.5),
        text=label,
        text_style=Styles.DarkBold.patch(text_size=7.8),
    )

# Connectors: Source -> Pipeline -> 4 Publishing Targets
line((38, 31), (53, 31), arrow_head="->", style=Styles.DarkBold)
line((97, 28), (103, 28), style=Styles.DarkBold)
line((103, 12.5), (103, 49.5), style=Styles.DarkBold)
for ty, _, _ in targets:
    line((103, ty), (110, ty), arrow_head="->", style=Styles.DarkBold)

save()
```

1. **Source of Truth (`<name>_src/`)**: You author content exclusively in source directories (e.g. `docs_src/`, `doc_src/`, `slide_src/`, or `images_src/`). Output folders (`docs_html/`, `docs_markdown/`, `docs_images/`, `images/`, etc.) are build artifacts and should never be manually modified.
2. **Deterministic Build Cache**: Drawlib computes a SHA-256 hash of each embedded code block (`styles.py`, `utils.py`, and referenced local assets included). Unaltered diagrams are restored instantly from `.drawlib/cache.db`, enabling sub-second incremental builds across massive multi-page sites.
3. **Execution Sandbox & Isolation**: The canvas lifecycle automatically clears between separate code blocks, ensuring zero visual side effects between adjacent diagrams.
4. **Target Portability**: The same Markdown source document can compile simultaneously to:
   - A responsive static HTML documentation site (`drawlib build html`).
   - GitHub-flavored Markdown with companion images (`drawlib build markdown`).
   - A publication-grade vector PDF with table of contents and cover page (`drawlib build pdf`).
   - Extracted standalone diagram images (`drawlib build image`).

---

## 2. Project Starter Templates

Never construct documentation directories manually. Scaffolding them with `drawlib init` guarantees the correct directory layout and configuration scripts:

| Template | Source Directory | Primary Output | Typical Use Case |
|---|---|---|---|
| **`doc`** | `doc_src/` | `doc_html/`, `doc.pdf`, `doc_markdown/`, `doc_images/` | Linear technical documents, RFCs, specifications, whitepapers, and formal reports. |
| **`site`** | `docs_src/` | `docs_html/`, `docs_markdown/` (or `docs/`), `docs_images/` | Multi-page documentation websites with sidebar navigation (`navbar.md`). |
| **`slide`** | `slide_src/` | `slide_html/`, `slide.pdf`, `slide_images/` | 16:9 presentation slide decks (interactive web deck + printable vector PDF). |
| **`images`** *(alias: `image`)* | `images_src/` | `images/*.png` (or `.webp`) | Batch rendering standalone Python drawing scripts to image assets. |

```drawlib fold-code 650px center file:doc_builder_four_templates_matrix.png caption:"Overview of the Four Drawlib Project Starter Templates and Their Outputs"
from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles

setup(width=140, height=58)

cards = [
    (
        36,
        43,
        "1. doc (Linear Spec / RFC)",
        Styles.SecondaryNeutral,
        Styles.DarkBold,
        "doc_src/*.md\n(00_cover, 01_...)",
        "doc.pdf & doc_html/\ndoc_markdown/\ndoc_images/",
    ),
    (
        104,
        43,
        "2. site (Documentation Website)",
        Styles.PrimaryFlat,
        Styles.WhiteBold,
        "docs_src/**/*.md\n+ navbar.md",
        "docs_html/ (Web)\ndocs_markdown/\ndocs_images/",
    ),
    (
        36,
        15,
        "3. slide (16:9 Presentation Deck)",
        Styles.PrimaryNeutral,
        Styles.DarkBold,
        "slide_src/*.md\n(1920x1080 stage)",
        "slide_html/ (?presenter=1)\nslide.pdf\nslide_images/",
    ),
    (
        104,
        15,
        "4. images (Batch Python Scripts)",
        Styles.SecondaryNeutral,
        Styles.DarkBold,
        "images_src/*.py\n+ styles.py",
        "images/*.png\n*.webp / *.svg",
    ),
]

for cx, cy, title, hdr_style, hdr_text_style, src_text, out_text in cards:
    # Outer card container
    rectangle(
        (cx, cy),
        width=64,
        height=24,
        style=Styles.Neutral.patch(shape_r=2.0),
    )
    # Header banner
    rectangle(
        (cx, cy + 8.2),
        width=61,
        height=5.6,
        style=hdr_style.patch(shape_r=1.2),
        text=title,
        text_style=hdr_text_style.patch(text_size=8.0),
    )
    # Source box (left)
    rectangle(
        (cx - 17.5, cy - 2.5),
        width=25,
        height=12.5,
        style=Styles.PrimaryNeutral.patch(shape_r=1.2),
        text=src_text,
        text_style=Styles.DarkBold.patch(text_size=7.4),
    )
    # Arrow
    line((cx - 5.0, cy - 2.5), (cx - 0.5, cy - 2.5), arrow_head="->", style=Styles.DarkBold)
    # Output box (right)
    rectangle(
        (cx + 15.0, cy - 2.5),
        width=31,
        height=12.5,
        style=Styles.SecondaryNeutral.patch(shape_r=1.2),
        text=out_text,
        text_style=Styles.Dark.patch(text_size=7.3),
    )

save()
```

---

## 3. Chapter Structure

Dive deeper into each builder subsystem:
- [Embedded Code Blocks](./code_blocks.md): Code fence syntax, display modes (`show-code`, `fold-code`), alignment, and captions.
- [CLI Reference](./cli_reference.md): Complete guide to `build`, `serve`, `show`, `init`, `cache`, `css`, `colors`, `styles`, and `rules`.
- [Linear Document Project Guide](./project_doc.md): Linear document RFCs, specifications, whitepapers, and dual HTML/PDF publishing.
- [Doc Site Project Guide](./project_site.md): Multi-page website authoring, sidebar categories, and link validation.
- [Slide Deck Project Guide](./project_slide.md): 16:9 presentation slide decks with interactive web deck and vector PDF export.
- [Slide Stage Layout & API](./slide_layout_and_api.md): `1920x1080` virtual stage coordinates, `::: block` / `::: note` syntax, templates, and `drawlib.slide` Python API.
- [Image Project Guide](./project_image.md): Standalone script automation (`images_src/` ➔ `images/`).
- [Customization & Theming](./customization.md): Customizing `template.html`, `style.css`, and injecting project `styles.py` and `utils.py`.
- [Caching Architecture & CI/CD](./caching_and_cicd.md): Two-tier caching (`.drawlib/cache.db` & `drawlib cache`) and headless CI/CD pipelines.
