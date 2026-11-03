# API Reference Project Guide (`drawlib init project api`)

The `api` starter template builds a dedicated, two-column **Illustrated API & SDK Reference** website (`1 Markdown = 1 HTML Page`) where each Markdown file's `# H1` becomes a sidebar category/module group and its `## H2` headings become a scannable symbol or endpoint sub-list with semantic badges, `/` quick filtering, and embedded Drawlib diagrams:

```drawlib code=fold align=center file=project_api_sidebar_architecture.png caption="How 1:1 Markdown Pages Compile into an Auto-Extracted Two-Column API Reference UI"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=128, height=62)

# Left: Source directory container (No navbar.md needed)
rectangle((21, 31), width=34, height=54, style=Styles.MutedDashed.patch(shape_r=2.0))
text((21, 54.2), "api_src/<lang>/", style=Styles.DarkBold.patch(text_size=10.8))

rectangle((21, 39.2), width=30, height=22, style=Styles.PrimaryNeutral.patch(shape_r=1.5))
phosphor.file_code((10.5, 45.8), width=4.4, style=Styles.PrimaryBold)
text((23.5, 45.8), "01_users.md", style=Styles.DarkBold.patch(text_size=10.5))
text((21, 35.0), "# H1 Category\n## `GET` /v1/users\n```drawlib Sequence", style=Styles.Dark.patch(text_size=10.0))

rectangle((21, 15.2), width=30, height=19, style=Styles.Neutral.patch(shape_r=1.5))
phosphor.gear((10.5, 20.5), width=4.4, style=Styles.PrimaryBold)
text((23.5, 20.5), "drawlib.toml", style=Styles.DarkBold.patch(text_size=10.5))
text((21, 11.8), "[api] sidebar=true\nbadge / repo / links", style=Styles.Dark.patch(text_size=10.0))

# Middle: Compiler step
line((38, 31), (53, 31), arrow_head="->", style=Styles.DarkBold)
text((45.5, 36.2), "build html", style=Styles.PrimaryBold.patch(text_size=10.5))
text((45.5, 25.5), "Auto H1 / H2", style=Styles.Muted.patch(text_size=10.0))

# Right: Compiled Two-Column API Reference UI (api_html/<lang>/)
rectangle((88, 31), width=70, height=54, style=Styles.SecondaryNeutral.patch(shape_r=2.0))
phosphor.brackets_curly((60.5, 54.2), width=4.6, style=Styles.PrimaryBold)
text((91.0, 54.2), "Compiled API Reference UI (api_html/<lang>/)", style=Styles.DarkBold.patch(text_size=10.8))

# Left Sticky Sidebar (Single divider + Default Open <details>)
rectangle((69.5, 28.0), width=27, height=44, style=Styles.Neutral.patch(shape_r=1.5))
text((69.5, 46.5), "Left API Sidebar", style=Styles.DarkBold.patch(text_size=10.5))
rectangle(
    (69.5, 40.0),
    width=23.5,
    height=5.6,
    style=Styles.SecondaryNeutral.patch(shape_r=1.0),
    text="/ Filter Symbols",
    text_style=Styles.Dark.patch(text_size=10.0),
)
rectangle(
    (69.5, 31.2),
    width=23.5,
    height=6.8,
    style=Styles.PrimaryFlat.patch(shape_r=1.0),
    text="▼ Users Service",
    text_style=Styles.WhiteBold.patch(text_size=10.0),
)
rectangle(
    (69.5, 22.0),
    width=23.5,
    height=7.2,
    style=Styles.PrimaryNeutral.patch(shape_r=1.0),
    text="[GET] /v1/users",
    text_style=Styles.PrimaryBold.patch(text_size=10.0),
)
text((69.5, 11.5), "Default Open (Ctrl+F)", style=Styles.Muted.patch(text_size=9.8))

# Right Main Content Pane
rectangle((103.5, 28.0), width=35, height=44, style=Styles.Neutral.patch(shape_r=1.5))
text((103.5, 46.5), "API Page + Chrome", style=Styles.DarkBold.patch(text_size=10.5))
rectangle(
    (103.5, 37.2),
    width=31,
    height=11.5,
    style=Styles.PrimaryNeutral.patch(shape_r=1.2),
    text="Architecture / Seq\nDiagram Figure",
    text_style=Styles.DarkBold.patch(text_size=10.0),
)
rectangle(
    (103.5, 19.2),
    width=31,
    height=19.0,
    style=Styles.SecondaryNeutral.patch(shape_r=1.2),
    text="## [GET] /v1/users\nParams & JSON Table\nPrev / Next Pager",
    text_style=Styles.Dark.patch(text_size=10.0),
)

save()
```

> **Note (Upcoming in v0.3.5):** The `api` project archetype (`drawlib init project api`) and `[api]` manifest section are scheduled for the upcoming **v0.3.5** release and are not yet included in the `v0.3.4` package on PyPI.

---

## 1. Why Use an `api` Project Instead of `site`?

Mixing narrative tutorials with hundreds of SDK functions or REST endpoints in a single `navbar.md` sidebar makes both hard to scan. Drawlib's `api` archetype separates dense technical references into a dedicated project while preserving full Drawlib diagram embedding:

| Capability | `site` Project (`docs_src/`) | `api` Project (`api_src/`) |
| :--- | :--- | :--- |
| **Primary Goal** | Narrative guides, tutorials, architecture portals | REST / GraphQL / gRPC endpoints, Python / TS SDKs, CLI & schema manuals |
| **Sidebar Source** | Manual `<lang>/navbar.md` curated by authors | **Zero `navbar.md`** — auto-extracted from each `.md` file's `# H1` & `## H2` |
| **Left-Pane Depth** | Page links grouped under `## Section` headings | Expandable `<details>` per `# H1` page + `## H2` `#slug` symbol anchors |
| **Symbol Badges** | Standard prose headings | Automatic color-coded badges (`def`, `class`, `GET`, `POST`, `DELETE`, `cmd`, ...) |
| **In-Browser Search** | Page-level navigation | Default-expanded categories (`Ctrl+F` friendly) + instant `/` client-side filter |

---

## 2. Scaffolding & Directory Layout

Initialize a single-locale or multi-locale `api` project with `drawlib init project api`:

```bash
# Default English API reference project (creates api_src/en/):
uv run drawlib init project api

# Custom target name + bilingual English/Japanese + Google theme (creates sdk_api_src/{en,ja}/):
uv run drawlib init project api sdk_api -l en,ja -s google

# Compile HTML, GitHub Markdown, and standalone images:
./api_src/build.sh

# Validate every internal page & anchor link headlessly:
uv run drawlib serve api_html/ --check
```

Scaffolded directory layout:

```text
api_src/
├── drawlib.toml            # Project manifest (type = "api", [i18n], [api], optional [seo])
├── styles.py               # Global Drawlib diagram palette & typography overrides
├── utils.py                # Reusable Python diagram helpers
├── style.css               # Responsive 2-column API reference stylesheet (Light/Dark)
├── template.html           # Jinja2 API layout (filter, scroll-spy, header links, pager)
├── _assets/                # Static logos & favicon.png (mirrored to api_html/_assets/)
├── en/                     # Locale Markdown pages (sorted naturally: 00_, 01_, 02_, ...)
│   ├── 00_overview.md      # Gateway topology (ArchitectureDiagram) & auth overview
│   ├── 01_users.md         # REST endpoints (`GET`/`POST`/`DELETE`) & SequenceDiagram
│   └── 02_models.md        # SDK classes/functions (`class`/`def`) & ERDiagram
├── build.sh                # Master build script (HTML + Markdown + Images)
├── build_html.sh           # Fast HTML-only rebuild -> api_html/
├── build_markdown.sh       # GitHub-Flavored Markdown export -> api_markdown/
├── build_image.sh          # Standalone PNG extraction -> api_images/
└── serve.sh                # Local preview HTTP server
```

> **Note:** Like `site`, multi-page `api` projects compile to `html`, `markdown`, and `image` targets (`drawlib build pdf` and `drawlib build docx` target linear `doc` or `slide` projects).

---

## 3. Heading Mapping & Semantic Badges (`# H1` / `## H2`)

Every Markdown file under `api_src/<lang>/` maps `1:1` to an HTML page and populates the left navigation tree automatically:

1. **`# H1` (Category / Module Header)**: Becomes the `<details class="api-nav-group">` summary title in the left pane and the `<h1 class="api-page-title">` header on the page. Dotted module names (such as `# drawlib.shapes`) automatically render in monospace font.
2. **`## H2` (Symbol / Endpoint Sub-list)**: Prefixing an `## H2` heading with a leading inline-code token `` `BADGE` `` renders a semantic pill badge in **both** the left sidebar and the main content heading, plus a deterministic `#slug` permalink anchor.
3. **`### H3` / `#### H4` (Parameter Sub-sections)**: Receive deterministic `id="..."` anchors in the page body (e.g., `### Parameters`, `### Response Codes`) without cluttering the left sidebar.

```drawlib code=fold align=center file=project_api_badge_taxonomy.png caption="Supported Semantic H2 Badges Across SDK Modules, HTTP APIs, RPC Services, and CLI Manuals"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.shapes import rectangle
from drawlib.smartarts import Table
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=128, height=56)

rectangle((64, 50.5), width=120, height=7.2, style=Styles.PrimaryNeutral.patch(shape_r=1.5))
phosphor.tag((11.5, 50.5), width=4.4, style=Styles.PrimaryBold)
text(
    (66.0, 50.5),
    "Markdown Pattern:  ## `<BADGE>` <signature_or_endpoint_path>",
    style=Styles.DarkBold.patch(text_size=11.2),
)

tbl = Table(
    cell_style=Styles.White,
    text_style=Styles.Dark.patch(text_size=10.2),
    header_cell_style=Styles.PrimaryFlat,
    header_text_style=Styles.WhiteBold.patch(text_size=10.8),
    border_style=Styles.MutedThin,
    has_header=True,
)
tbl.set_style_cell_evenodd(
    even_color=Colors.White,
    even_text_style=Styles.Dark.patch(text_size=10.2),
    odd_color=Styles.SecondaryNeutral.shape_fill_color or Colors.White,
    odd_text_style=Styles.Dark.patch(text_size=10.2),
)
tbl.set_style_cell_header(
    background_color=Styles.PrimaryFlat.shape_fill_color or Colors.Primary,
    text_style=Styles.WhiteBold.patch(text_size=10.8),
)
tbl.draw_flexible(
    xy=(4, 44.5),
    column_widths=[27.0, 36.0, 57.0],
    row_heights=[8.2, 8.0, 8.0, 8.0, 8.0],
    data=[
        ["API Domain", "Recognized Badges", "Markdown Authoring Example"],
        ["SDK & Libraries", "def, async, class, method", "## `def` build_html(src, out)"],
        ["Types & Constants", "type, enum, const, prop", "## `class` ProjectManifest"],
        ["REST / HTTP APIs", "GET, POST, PUT, PATCH, DELETE", "## `GET` /v1/users/<id>"],
        ["CLI, Events & RPC", "cmd, rpc, event", "## `cmd` drawlib init project api"],
    ],
)

save()
```

### Markdown Authoring Example (`01_users.md`):

````markdown
# Users Service

Provision, query, and revoke workspace user accounts over HTTPS.

```drawlib align=center code=fold file=users_provisioning_sequence.png caption="POST /v1/users Provisioning Sequence"
from drawlib.canvas import save, setup
from drawlib.diagrams.sequence import Participant, PhosphorIcon, SequenceDiagram
from drawlib.styles import Styles

setup(width=120, height=62)
sd = SequenceDiagram(
    node_style=Styles.Dark,
    node_text_style=Styles.DarkBold.patch(text_size=10.5),
    edge_style=Styles.Dark.patch(line_width=1.4),
    edge_text_style=Styles.Dark.patch(text_size=10.0),
    node_card_style=Styles.Neutral,
    col_width=34.0,
    step_y=7.5,
)
client = sd.add(Participant("SDK Client", icon=PhosphorIcon.LAPTOP, width=22, card_style=Styles.PrimaryNeutral))
api = sd.add(
    Participant(
        "Users API",
        icon=PhosphorIcon.SHIELD_CHECK,
        width=22,
        style=Styles.White,
        text_style=Styles.WhiteBold.patch(text_size=10.5),
        card_style=Styles.PrimaryFlat,
    )
)
db = sd.add(Participant("PostgreSQL", icon=PhosphorIcon.DATABASE, width=22, card_style=Styles.Neutral))
client.request(api, "POST /v1/users")
api.request(db, "INSERT INTO users")
db.reply(api, "201 Created")
api.reply(client, "User JSON")
sd.draw(xy=(60, 31), align="center")
save()
```

## `GET` /v1/users/<id>

Retrieve a single user profile by unique identifier `<id>`.

| Parameter | Location | Type | Description |
| :--- | :--- | :--- | :--- |
| `id` | `path` | `string` | Unique user ID (`usr_...`). |

## `POST` /v1/users

Create a new user account and dispatch an invitation token.
````

> **Angle-Bracket Safety (`<id>`, `<T>`):** Route placeholders such as `/v1/users/<id>` and generic type parameters such as `Result<T>` are preserved verbatim as visible escaped text in both the sidebar and `<h2>` headings without being stripped as HTML tags.

---

## 4. Configuring `[api]` in `drawlib.toml`

Customize sidebar expansion defaults, version badges, source repository icon links, and top-right navigation links directly in `api_src/drawlib.toml` without editing `template.html`:

```toml
[project]
name = "cloud_api"
type = "api"
title = "Cloud API Reference"
description = "REST endpoints, authentication flows, and Python SDK models."
style = "google"

[i18n]
default_lang = "en"
langs = ["en", "ja"]

[api]
# Expand all sidebar categories by default so browser Ctrl+F / Cmd+F finds every symbol immediately:
sidebar_expanded = true

# Optional version/status pill rendered in the sidebar subbar (plain string or per-locale table):
badge_text = { en = "v2.4 · Stable", ja = "v2.4 · 安定版" }
badge_url = "00_overview.html"

# Optional GitHub / GitLab source repository icon in the sidebar subbar (http:// or https://):
repo_url = "https://github.com/example/cloud-sdk"

# Optional navigation links rendered in the top-right header bar (plain or localized labels):
header_links = [
    { label = { en = "User Guide", ja = "利用ガイド" }, url = "https://docs.example.com" },
    { label = "Data Models", url = "02_models.html" },
]
```

### `[api]` Reference Table:

| Key | Type | Default | Behavior |
| :--- | :--- | :--- | :--- |
| `sidebar_expanded` | `bool` | `true` | When `true` *(default and omitted fallback)*, all category `<details>` render open so native browser find (`Ctrl+F` / `Cmd+F`) matches every symbol across the reference. When `false`, inactive categories start collapsed while the current page's category remains open. |
| `badge_text` | `str \| dict[lang, str]` | `None` | Renders a version/release pill below the brand header. When both `badge_text` and `repo_url` are omitted, the subbar hides cleanly while preserving a single crisp horizontal divider beneath the brand title. |
| `badge_url` | `str` | `None` | Optional `http(s)://` or locale-relative link target when clicking the version pill. |
| `repo_url` | `str` | `None` | Optional `http://` or `https://` repository URL rendered as a source icon next to the badge. |
| `header_links` | `list[{label, url}]` | `[]` | Links displayed in the top-right bar alongside the multi-locale switcher (`http(s)://` links open in a new tab with an `↗` indicator; relative links rebase automatically across nested subdirectories). |
