# 13. Documentation as Code & The 5 Project Archetypes

Writing standalone diagrams is only half the story. In real engineering organizations, architecture visuals live inside multi-chapter design documents, searchable API portals, RFC whitepapers, and executive slide decks that must stay synchronized across languages and output formats.

Drawlib elevates **Illustration as Code** into **Illustrated Documentation as Code**: a unified project compiler where pure-Python diagrams and Markdown prose live side-by-side in Git and compile deterministically into static HTML websites, A4 vector PDFs, editable Microsoft Word (`.docx`) specifications, 16:9 HTML/PDF slide decks, native PowerPoint (`.pptx`) files, and animated image suites.

```drawlib align=center code=fold file=five_project_archetypes.png caption="Figure 13.1: Drawlib's Single Source of Truth Compiling into the 5 Project Archetypes (v0.3.10)"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line, lines
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=158, height=74)

text(
    (79.0, 68.2),
    "Drawlib v0.3.10 — Single Source of Truth to the 5 Project Archetypes",
    style=Styles.DarkBold.patch(text_size=12.8),
)

# Left Focal Hub (1 PrimaryFlat hero node)
rectangle((24.0, 34.5), width=34.0, height=55.0, style=Styles.PrimaryFlat.patch(shape_r=2.2))
phosphor.git_branch((24.0, 55.0), width=5.6, style=Styles.WhiteBold)
text((24.0, 46.2), "Git Source\nof Truth", style=Styles.WhiteBold.patch(text_size=11.5))
line((11.0, 39.8), (37.0, 39.8), style=Styles.White)
text(
    (24.0, 23.2),
    "• drawlib.toml\n• styles.py\n• <lang>/styles.py\n• utils.py\n• _assets/\n• build.sh",
    style=Styles.White.patch(text_size=10.2),
)

# Orthogonal fan-out spine to the 3 rows
line((41.0, 34.5), (47.5, 34.5), style=Styles.DarkBold)
lines([(47.5, 34.5), (47.5, 53.5), (53.0, 53.5)], arrow_head="->", style=Styles.DarkBold)
line((47.5, 34.5), (53.0, 34.5), arrow_head="->", style=Styles.DarkBold)
lines([(47.5, 34.5), (47.5, 15.5), (53.0, 15.5)], arrow_head="->", style=Styles.DarkBold)

# Row 1: images & doc (Neutral-grounded cards)
rectangle((76.5, 53.5), width=47.0, height=16.5, style=Styles.Neutral.patch(shape_r=2.0))
phosphor.images((58.0, 57.5), width=4.6, style=Styles.PrimaryBold)
text((79.5, 57.5), "1. images — Asset Suites", style=Styles.DarkBold.patch(text_size=11.0))
text((76.5, 49.3), "*.py -> PNG / WebP / GIF / PDF / SVG", style=Styles.Dark.patch(text_size=10.0))

rectangle((128.5, 53.5), width=47.0, height=16.5, style=Styles.PrimaryNeutral.patch(shape_r=2.0))
phosphor.file_pdf((110.0, 57.5), width=4.6, style=Styles.PrimaryBold)
text((131.5, 57.5), "2. doc — Whitepapers", style=Styles.DarkBold.patch(text_size=11.0))
text((128.5, 49.3), "<lang>/*.md -> HTML / A4 PDF / DOCX", style=Styles.Dark.patch(text_size=10.0))

# Row 2: site & catalog
rectangle((76.5, 34.5), width=47.0, height=16.5, style=Styles.SecondaryNeutral.patch(shape_r=2.0))
phosphor.globe((58.0, 38.5), width=4.6, style=Styles.SecondaryBold)
text((79.5, 38.5), "3. site — Docs Portals", style=Styles.DarkBold.patch(text_size=11.0))
text((76.5, 30.3), "navbar.md -> Multi-Page HTML / PDF", style=Styles.Dark.patch(text_size=10.0))

rectangle((128.5, 34.5), width=47.0, height=16.5, style=Styles.Neutral.patch(shape_r=2.0))
phosphor.brackets_curly((110.0, 38.5), width=4.6, style=Styles.SecondaryBold)
text((131.5, 38.5), "4. catalog — API Refs", style=Styles.DarkBold.patch(text_size=11.0))
text((128.5, 30.3), "# H1 & ## GET -> Split UI + / Filter", style=Styles.Dark.patch(text_size=10.0))

# Row 3: slide (Full-span widescreen card)
rectangle((102.5, 15.5), width=99.0, height=16.5, style=Styles.PrimaryNeutral.patch(shape_r=2.0))
phosphor.presentation_chart((61.0, 19.5), width=4.8, style=Styles.PrimaryBold)
text((104.5, 19.5), "5. slide — 16:9 Widescreen Presentation Decks", style=Styles.DarkBold.patch(text_size=11.2))
text(
    (102.5, 11.3),
    "1920x1080 ::: block & ::: note -> Interactive HTML / 16:9 PDF / Editable PPTX",
    style=Styles.Dark.patch(text_size=10.2),
)

save()
```

---

## 13.1 The Project-First Rule (`drawlib init project`)

When starting any visual or documentation task—even a single architecture figure—always follow Drawlib's **Project-First Rule**: scaffold a structured `<target>_src/` workspace with `drawlib init project` rather than scattering ad-hoc standalone `.py` scripts or hand-crafting folders.

Scaffolding a project up front establishes five engineering guarantees out of the box:

- **Canonical Manifest (`drawlib.toml`)**: Declares the project archetype (`images`, `doc`, `site`, `catalog`, or `slide`), visual preset (`default`, `google`, `monochrome`), multi-language `[i18n]` routing, and `[seo]` metadata in one declarative file.
- **Centralized Theme & CJK Font Safety (`styles.py` & `<lang>/styles.py`)**: Passing `-l ja` or `-l en,ja` automatically configures `Styles` and regional font overrides (`FontJapanese`, `FontChinese`, `FontKorean`) so every diagram shares one palette without repeating font boilerplate.
- **DRY Component Macros (`utils.py`)**: Top-level helper functions defined in `utils.py` become importable everywhere via `from drawlib.utils import <helper>`, keeping recurring node cards and connectors consistent across dozens of chapters.
- **Portable Static Assets (`_assets/`)**: Provisions `_assets/favicon.png` and provides a root directory for brand logos and custom `.ttf` fonts that Drawlib resolves and SHA-256 hashes automatically.
- **Reproducible One-Command Builds (`build.sh` & `build_*.sh`)**: Generates executable build scripts (`build.sh`, `build_html.sh`, `build_pdf.sh`, `build_docx.sh`, `build_pptx.sh`, `serve.sh`) while strictly separating `<target>_src/` (your editable source of truth) from read-only compiled outputs.

Use `drawlib init project <type> [target] -l <langs> -s <style>` to initialize any of the five archetypes (and delete starter `sample*.py` files once you add your own diagrams):

```bash
# Inspect all 5 starter project templates
uv run drawlib init project list

# 1. Standalone Python diagram & animation repository (images_src/)
uv run drawlib init project images diagrams -l en -s google

# 2. Bilingual linear technical whitepaper -> HTML + A4 PDF + MS Word (.docx)
uv run drawlib init project doc whitepaper -l en,ja -s google

# 3. Multi-page documentation portal with sidebar navigation (docs_src/)
uv run drawlib init project site docs -l en,ja -s default

# 4. Searchable API / CLI / schema reference dictionary (catalog_src/)
uv run drawlib init project catalog api_ref -l en,ja -s google

# 5. Bilingual 16:9 presentation slide deck -> HTML + PDF + PowerPoint (.pptx)
uv run drawlib init project slide pitch -l en,ja -s google
```

---

## 13.2 Embedded Markdown Diagrams & 720pt Typography Parity

Inside `doc`, `site`, `catalog`, and `slide` Markdown files (`<target>_src/<lang>/**/*.md`), Python illustrations are embedded directly inline using fenced `drawlib` blocks. During compilation, Drawlib executes each block in an isolated canvas state, caches the rendered output in `.drawlib/cache.db`, and replaces the fence with responsive figure markup.

````markdown
```drawlib align=center code=fold file=gateway_flow.png caption="Figure 13.3: Regional API Gateway Topology"
from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles

setup(width=136, height=44)

rectangle((28, 22), width=32, height=18, style=Styles.Neutral, text="Client App")
rectangle(
    (68, 22),
    width=32,
    height=18,
    style=Styles.PrimaryFlat,
    text="API Gateway",
    text_style=Styles.WhiteBold,
)
rectangle((108, 22), width=32, height=18, style=Styles.SecondaryNeutral, text="Auth Service")

line((44, 22), (52, 22), arrow_head="->", style=Styles.DarkBold)
line((84, 22), (92, 22), arrow_head="->", style=Styles.DarkBold)
save()
```
````

Every embedded `drawlib` fence supports four header attributes that govern file naming, layout, and code disclosure:

| Fence Attribute | Supported Values | Recommended Usage |
| :--- | :--- | :--- |
| **`file=`** | `<stem>.png` / `.webp` / `.svg` | **Mandatory.** Assigns a deterministic filename (`file=arch.png` for shared diagrams, or `file=arch_ja.png` for localized CJK diagrams) so `drawlib show <md> <file>` can target it by name. |
| **`caption=`** | `"Figure X.Y: ..."` | **Mandatory on docs.** Renders an accessible `<figcaption>` in HTML/PDF and figure caption paragraph in `.docx`. |
| **`align=`** | `center` \| `left` \| `right` | Controls horizontal figure alignment inside the document column (`align=center` standard). |
| **`code=`** | `hide` \| `fold` \| `show` | `code=hide` (default) emits only the figure for clean whitepapers; `code=fold` renders the figure first with a collapsible `<details>` code drawer (**mandatory for Top Hero diagrams at Lines 5–15**); `code=show` displays syntax-highlighted Python above the figure for API tutorials. |

### Why Omitting Pixel `width=` Caps Preserves `720pt` Typography

Drawlib's rendering engine normalizes every canvas (`setup(width=W, height=H)`) to a physical width of **`10 inches = 720 points`** regardless of whether `W=100` or `W=160`. When that image is displayed inside an HTML column of width $W_{\text{HTML}}$ (typically `~880px–960px`), an in-diagram `text_size` (in points) appears on screen at:

$$\text{Rendered CSS Font Size (px)} = \text{text\_size} \times \frac{W_{\text{HTML}}}{720}$$

- **Without pixel caps (`100%` column width, `~900px`)**: `text_size=11.0` renders at `11.0 × 900 / 720 = 13.75px`, harmonizing naturally with `16px` HTML body prose and A4 PDF text.
- **With hardcoded narrow caps (`width=500px` or `600px` — Forbidden)**: Shrinking the image container to `500px` crushes `text_size=11.0` down to `7.6px`, making labels unreadable even when the standalone PNG looked fine in isolation. Always omit pixel `width=` caps on fences and keep `text_size >= 10.0`.

---

## 13.3 Comparing the 5 Project Archetypes

Drawlib `v0.3.10` provides five purpose-built project archetypes. All four Markdown-driven archetypes (`doc`, `site`, `catalog`, `slide`) use the exact same `<target>_src/<lang>/` locale directory convention so teams can add new languages at any time without moving existing files.

| Archetype | Source Layout | Navigation & Structure | Compiled Deliverables | Primary Engineering Use Cases |
| :--- | :--- | :--- | :--- | :--- |
| **`images`** | `images_src/*.py` | Flat or nested Python scripts; AST duplicate output check | `.png` (incl. `APNG`), `.webp`, `.gif`, `.pdf`, `.svg` | Architecture asset libraries, README figures, CI-generated charts, multi-frame protocol animations |
| **`doc`** | `doc_src/<lang>/*.md` (`00_cover.md`, `01_*`...) | Lexicographical chapter merge + `--generate-index` TOC (`no navbar.md`) | Single-page `HTML` book, A4 vector `PDF`, editable Word `.docx`, GitHub `MD` | Engineering RFCs, architecture whitepapers, onboarding manuals, printable specs & stakeholder redlining |
| **`site`** | `docs_src/<lang>/**/*.md` + `<lang>/navbar.md` | Persistent multi-section sidebar (`navbar.md`), dark mode, search | Multi-page `HTML` portal, per-page `PDF`, GitHub `MD`, `llms.txt` | Product documentation portals, developer guides, multi-team architecture wikis |
| **`catalog`** | `catalog_src/<lang>/*.md` *(auto-indexed)* | Sticky 2-column split/outline UI from `# H1` & `## H2` + instant `/` live filter | Interactive 2-column `HTML` dictionary, GitHub `MD`, `llms.txt` | REST/gRPC API references, CLI flag manuals, event/metric catalogs, database schema dictionaries |
| **`slide`** | `slide_src/<lang>/*.md` (`01_title.md`...) | `1920×1080` `::: block` stage + `::: note` speaker script + Presenter View | `16:9` interactive `HTML` deck, `16:9` vector `PDF`, editable PowerPoint `.pptx` | Technical keynotes, architecture review decks, sprint demos, customer executive briefings |

Key capabilities distinguishing each archetype in daily workflows:

1. **`images` (Standalone Diagrams & Animations)**: Each `*.py` script calling `save()` automatically emits `<script_stem>.png` (or `.webp`/`.gif` for `Animation()` loops). Before running any script, `drawlib build image` parses all files via Python's `ast` module and aborts immediately if two scripts would collide on the same output filename. When writing multiple files inside one script, call `clear()` before each subsequent `setup()`.
2. **`doc` (Linear Multi-Chapter Books, PDF & Word `.docx`)**: Merges numbered chapters (`00_cover.md`, `01_overview.md`, ...) in sorted order, injecting CSS/Word page breaks (`--page-break`) and a localized Table of Contents (`--generate-index`) right after `00_cover.md`. Alongside `./doc_src/build.sh` (`HTML` + A4 `PDF`), run `./doc_src/build_docx.sh` (`drawlib build docx`) whenever stakeholders need a native editable `.docx` file.
3. **`site` (Multi-Page Documentation Portals)**: Driven by `<lang>/navbar.md`, compiling nested Markdown trees into responsive static portals with light/dark theme switching, localized sidebars, syntax highlighting, and cross-page link rewriting (`.md` -> `.html`).
4. **`catalog` (Searchable Reference Dictionaries)**: Eliminates manual sidebar maintenance (`1 Markdown = 1 HTML Page`). Each file's `# H1` becomes a collapsible sidebar category, while every `## H2` becomes a scroll-spied `#slug` entry supporting instant `/` keyboard live filtering and color-coded semantic prefix badges—including HTTP verbs (`` ## `GET` /v1/users/<id> ``, `` ## `POST` /v1/orders ``), code symbols (`` ## `def` setup() ``, `` ## `class` BarChart ``), and infrastructure entities (`` ## `service` auth-api ``, `` ## `table` accounts ``, `` ## `cmd` drawlib build ``).
5. **`slide` (`16:9` Widescreen Decks & Editable `.pptx`)**: Separates concise visual slides (`::: block xy=(x, y) width=W height=H` on a `1920×1080` canvas) from rich presenter scripts (`::: note`). In addition to dual-screen HTML Presenter View and `16:9` vector PDFs, `./slide_src/build_pptx.sh` (`drawlib build pptx`) measures the live Chromium DOM to emit native editable PowerPoint shapes, text boxes, tables, speaker notes, and `240 DPI` diagrams.

```drawlib align=center code=fold file=project_directory_anatomy.png caption="Figure 13.2: Multi-Locale Project Directory Anatomy (TreeNode Source Layout Compiling into docs/ Deliverables)"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.smartarts import CardList, Panel, TreeNode
from drawlib.styles import Colors, Styles

setup(width=158, height=74)

# Left Panel: Source of Truth Directory Tree
src_panel = Panel(
    "Source of Truth (docs_src/)",
    style=Styles.Neutral.patch(shape_r=2.2),
    header_style=Styles.PrimaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=12.0),
    icon=phosphor.folder,
    icon_style=Styles.PrimaryBold,
    header_height=8.8,
)
src_panel.draw((6.0, 6.0), width=76.0, height=62.0)

TreeNode.register_drawing_item(
    name="dir_item",
    location="before",
    padding_width=4.4,
    function=phosphor.folder,
    style=Styles.Primary.patch(icon_color=Colors.Primary),
    args={"width": 3.0},
)
TreeNode.register_drawing_item(
    name="py_item",
    location="before",
    padding_width=4.4,
    function=phosphor.file_py,
    style=Styles.Secondary.patch(icon_color=Colors.Secondary),
    args={"width": 3.0},
)
TreeNode.register_drawing_item(
    name="cfg_item",
    location="before",
    padding_width=4.4,
    function=phosphor.file_code,
    style=Styles.Dark.patch(icon_color=Colors.Dark),
    args={"width": 3.0},
)

root = TreeNode(
    "docs_src/",
    text_style=Styles.DarkBold.patch(text_size=10.5),
    line_style=Styles.MutedBold.patch(line_width=1.2),
    line_horizontal_margin=2.8,
    line_horizontal_length=2.8,
    line_vertical_margin=4.8,
    children=[
        TreeNode("drawlib.toml  ([project], [i18n], [seo])", text_style=Styles.Dark.patch(text_size=10.2)).set_drawing_item("cfg_item"),
        TreeNode("styles.py & utils.py  (Shared Theme)", text_style=Styles.Dark.patch(text_size=10.2)).set_drawing_item("py_item"),
        TreeNode("_assets/  (favicon.png, brand logos)", text_style=Styles.Dark.patch(text_size=10.2)).set_drawing_item("dir_item"),
        TreeNode(
            "en/  (Default Locale)",
            children=[
                TreeNode("navbar.md & index.md", text_style=Styles.Dark.patch(text_size=10.0)).set_drawing_item("cfg_item"),
            ],
        ).set_drawing_item("dir_item"),
        TreeNode(
            "ja/  (Japanese Locale)",
            children=[
                TreeNode("styles.py, navbar.md & index.md", text_style=Styles.Dark.patch(text_size=10.0)).set_drawing_item("py_item"),
            ],
        ).set_drawing_item("dir_item"),
        TreeNode("build.sh & serve.sh", text_style=Styles.Dark.patch(text_size=10.2)).set_drawing_item("cfg_item"),
    ],
).set_drawing_item("dir_item")
root.draw(xy=(10.5, 54.5))

# Compiler Connector
line((83.2, 37.0), (89.8, 37.0), arrow_head="->", style=Styles.DarkBold)

# Right Panel: Compiled Deliverables
out_panel = Panel(
    "Compiled Deliverables (docs/)",
    style=Styles.PrimaryNeutral.patch(shape_r=2.2),
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=12.0),
    icon=phosphor.globe,
    icon_style=Styles.PrimaryBold,
    header_height=8.8,
)
out_panel.draw((91.0, 6.0), width=61.0, height=62.0)

outputs = CardList(
    style=Styles.White.patch(shape_r=1.6),
    text_style=Styles.DarkBold.patch(text_size=10.8),
    description_style=Styles.Dark.patch(text_size=10.0),
    badge_shape="none",
    icon_style=Styles.DarkBold,
    spacing=2.2,
)
outputs.add(
    "docs/ (or docs_html/)",
    "en/, ja/, shared images/, switcher",
    icon=phosphor.globe,
    style=Styles.PrimaryFlat.patch(shape_r=1.6),
    text_style=Styles.WhiteBold.patch(text_size=10.8),
    description_style=Styles.White.patch(text_size=10.0),
    icon_style=Styles.WhiteBold,
)
outputs.add(
    "PDF & Office Deliverables",
    "*_<lang>.pdf, .docx & .pptx",
    icon=phosphor.file_pdf,
)
outputs.add(
    "SEO & AI Agent Index",
    "sitemap.xml, robots.txt & llms.txt",
    icon=phosphor.brackets_curly,
)
outputs.add(
    "Incremental Cache (.drawlib/)",
    "SHA-256 SQLite cache.db (<1ms hit)",
    icon=phosphor.database,
    style=Styles.SecondaryNeutral.patch(shape_r=1.6),
)
outputs.draw((94.5, 9.0), width=54.0, height=46.5)

save()
```

---

## 13.4 Configuring `drawlib.toml`: `[project]`, `[i18n]`, and `[seo]`

Every Markdown-based Drawlib project (`doc`, `site`, `catalog`, `slide`) is governed by `drawlib.toml` at the root of `<target>_src/`. Centralizing metadata in `drawlib.toml` eliminates fragile CLI flag duplication across shell scripts and CI workflows:

```toml
[project]
name = "platform_docs"
type = "site"                 # "images" | "doc" | "site" | "catalog" | "slide"
title = "Cloud Platform Architecture"
description = "Unified architecture portal and API guide."
style = "google"              # "default" | "google" | "monochrome"

[i18n]
default_lang = "en"
langs = ["en", "ja"]          # Always present on doc/site/catalog/slide (even ["en"])

[i18n.labels]
en = "English"
ja = "日本語"

[i18n.descriptions]
en = "Cloud Platform architecture documentation and operational runbooks."
ja = "クラウドプラットフォームのアーキテクチャ設計書および運用ガイド。"

[seo]
site_url = "https://docs.example.com"
og_image = "_assets/ogp.png"
twitter_card = "summary_large_image"
sitemap = true
robots = true
llms_txt = true
```

### Multi-Language Skeleton Parity (`[i18n]`) & AI Discoverability (`[seo]`)

When `langs` contains two or more locales (such as `["en", "ja"]`), Drawlib runs **four mechanical pre-flight parity checks** before rendering any page, catching translation drift at build time rather than in production:

- **1. File Set & `navbar.md` Parity**: Every locale folder (`en/`, `ja/`) must contain the exact same relative `.md` file paths, and (for `site` projects) `navbar.md` must have identical section counts and normalized link targets.
- **2. Structural Skeleton Parity**: Each translated page must match `default_lang` in its ordered sequence of `#`/`##`/`###` headings (`H1`–`H3`), prose/table/list slots (`MarkdownText`), non-drawlib fenced code block languages (`CodeBlock`), and `drawlib` block attributes (`align`, `code`, `caption` presence). Consecutive paragraphs, lists, and tables collapse into a single `MarkdownText` slot so translators can write natural prose freely.
- **3. Shared vs. Localized Diagram Routing**: If `ja/` reuses the same filename (`file=arch.png`), Drawlib verifies that the Python code is byte-for-byte identical and renders the image **once** across all locales. When diagram labels are translated into Japanese, pair a locale-suffixed filename (`file=arch_ja.png`) with `ja/styles.py` (`FontJapanese`).
- **4. Automated SEO & `llms.txt` Generation (`[seo]`)**: Setting `[seo]` injects `<link rel="canonical">`, `hreflang` cross-locale tags, Open Graph (`og:*`), and Twitter Card metadata into every HTML page, while emitting `sitemap.xml`, `robots.txt`, and an `llmstxt.org`-compliant **`llms.txt`** index at the HTML root so AI coding assistants and search crawlers can index your documentation structure immediately.
