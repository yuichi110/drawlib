# Drawlib Illustrated API & SDK Reference Project Guidelines (`project-api`)

An **`api` project** (`drawlib init project api`) compiles a locale-structured directory of Markdown files (`api_src/<lang>/**/*.md`) into a **responsive 2-column API & SDK reference website (`api_html/`)**, **GitHub-Flavored Markdown (`api_markdown/`)**, and **extracted diagram assets (`api_images/`)**.

Unlike a prose `site` project (which requires a manual `navbar.md`), an `api` project follows the **`1 Markdown = 1 HTML Page`** model with **automatic 2-tier sidebar extraction**:
- **`# H1` -> Left-Pane Category / Module Header** (`<details class="api-nav-group">`)
- **`## H2` -> Left-Pane Symbol / Endpoint Sub-list** (`#slug` anchors + semantic badges + scroll-spy)

*(For general project scaffolding, see `uv run drawlib rules show project-overview`. For prose multi-page portals, see `uv run drawlib rules show project-site`. For the 3-stage review loop, see `uv run drawlib rules show review-guide`.)*

---

## 1. When to Choose an `api` Project

Choose `drawlib init project api` when the user wants a **dedicated API, SDK, CLI, or schema reference** paired with Drawlib architecture, sequence, and ER illustrations:
- REST / GraphQL / gRPC HTTP endpoint references (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `rpc`).
- Python / TypeScript / Go / Rust library & SDK module references (`def`, `class`, `method`, `const`, `type`).
- CLI command manuals (`cmd`), webhook event catalogs (`event`), or configuration schema references.
- Keeping dense symbol lists separate from narrative guides (`site`) so neither navigation sidebar becomes cluttered.

```bash
# Scaffold an API reference project (default target 'api', creates 'api_src/'):
uv run drawlib init project api [target] [-l <lang[,lang...]>] [-s <default|google|monochrome>]

# Examples:
uv run drawlib init project api
uv run drawlib init project api sdk_ref -l en,ja -s google
```

*(Note: The canonical project type is strictly `api` — aliases such as `ref` or `reference` are intentionally not supported.)*

---

## 2. Directory Structure (`api_src/`)

Every `api` project uses the unified `<src_dir>/<lang>/` locale directory layout governed by `[i18n]` and `[api]` in `drawlib.toml`:

```text
.
├── api_src/                   # [SOURCE OF TRUTH] Edit ONLY files here!
│   ├── drawlib.toml           # [MANDATORY] Project manifest (type = "api" + [i18n] + [api])
│   ├── en/                    # Locale API pages (1 Markdown = 1 HTML page)
│   │   ├── 00_overview.md     # Landing overview (auto-aliased to en/index.html & root index.html)
│   │   ├── 01_users.md        # Category: # Users API -> ## `GET` /v1/users, ...
│   │   └── 02_models.md       # Category: # SDK & Data Models -> ## `class` User, ...
│   ├── _assets/               # Static images, logos (logo.png, logo_dark.png, favicon.png)
│   ├── styles.py              # Shared Drawlib Styles & Colors
│   ├── utils.py               # Shared Python drawing helpers
│   ├── style.css              # Wide 2-column API reference stylesheet
│   ├── template.html          # Jinja2 API sidebar + filter + scroll-spy template
│   ├── build.sh               # Master build script (HTML + Markdown + Images)
│   ├── build_html.sh          # Static HTML build (api_html/)
│   ├── build_markdown.sh      # GitHub Markdown build (api_markdown/)
│   ├── build_image.sh         # Standalone diagram extraction (api_images/)
│   └── serve.sh               # Local preview server + broken link/anchor checker
├── api_html/                  # [GENERATED] Static HTML API reference (index.html + <lang>/**)
├── api_markdown/              # [GENERATED] Rendered Markdown for GitHub
└── api_images/                # [GENERATED] Extracted diagram PNG/WebP images
```

```drawlib align=center code=fold file=project_api_architecture.png caption="API Reference Project (1 Markdown = 1 Page -> # H1 Category & ## H2 Symbol Sidebar)"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=150, height=56, dpi=150)

rectangle((75, 28), width=144, height=50, style=Styles.MutedDashed.patch(shape_r=2.5))
text(
    (75, 48.5),
    "Illustrated API Reference Architecture (api_src/<lang>/*.md -> api_html/)",
    style=Styles.DarkBold.patch(text_size=12.5),
)

# 1. Markdown Source
rectangle((26, 24), width=38, height=34, style=Styles.Neutral.patch(shape_r=2.0))
phosphor.file_md((11.5, 35.5), width=4.8, style=Styles.PrimaryBold)
text((28, 35.5), "1. Markdown Page", style=Styles.PrimaryBold.patch(text_size=11.0))
text(
    (26, 20.5),
    "# Users API (H1)\n[Top Hero Diagram]\n## `GET` /v1/users\n## `POST` /v1/users\n## `GET` /v1/users/<id>",
    style=Styles.Dark.patch(text_size=9.8),
)

line((46, 24), (54, 24), arrow_head="->", style=Styles.PrimaryBold)

# 2. Auto-Extracted Left Pane
rectangle((75, 24), width=38, height=34, style=Styles.PrimaryFlat.patch(shape_r=2.0))
phosphor.sidebar((60.5, 35.5), width=4.8, style=Styles.WhiteBold)
text((77, 35.5), "2. Left Sidebar", style=Styles.WhiteBold.patch(text_size=11.0))
text(
    (75, 20.5),
    "▼ Users API  [3]\n  [GET]  /v1/users\n  [POST] /v1/users\n  [GET]  /v1/users/<id>\n• Open by default (Ctrl+F)",
    style=Styles.White.patch(text_size=9.8),
)

line((95, 24), (103, 24), arrow_head="->", style=Styles.PrimaryBold)

# 3. Wide 2-Column Main Reference
rectangle((124, 24), width=38, height=34, style=Styles.SecondaryNeutral.patch(shape_r=2.0))
phosphor.code((109.5, 35.5), width=4.8, style=Styles.SecondaryBold)
text((126, 35.5), "3. Main Reference", style=Styles.SecondaryBold.patch(text_size=11.0))
text(
    (124, 20.5),
    "• Sequence / ER visuals\n• Badged H2 anchors\n• Parameter tables\n• Prev / Next pager",
    style=Styles.Dark.patch(text_size=9.8),
)

save()
```

---

## 3. Heading Hierarchy & Semantic Badges (`# H1` / `## H2`)

### 3.1. `1 Markdown = 1 Page` Mapping Rules
1. **`# H1` (Category / Module Title)**: The first `# H1` in each `.md` file names the accordion group in the left sidebar (and falls back to a humanized filename stem if omitted). Dotted or lowercase module names (e.g. `# drawlib.shapes`) automatically style in monospace.
2. **`## H2` (Symbol / Endpoint Entries)**: Every `## H2` outside fenced code blocks becomes a clickable sub-item under its `# H1` category (`#slug`) with automatic scroll-spy highlighting.
3. **`### H3` / `#### H4` (Sub-sections)**: Receive deterministic `id="..."` anchors in the main body (for `Parameters`, `Returns`, `Responses`) without cluttering the left sidebar.
4. **Angle-Bracket Safety**: Placeholders like `` ## `GET` /v1/users/<id> `` or `Result<T>` are preserved and HTML-escaped automatically — never stripped as raw HTML tags.
5. **Optional Subdirectory Grouping or `navbar.md`**: Numbered root files (`00_overview.md`, `01_users.md`) sort deterministically (`index.md` or `00_*` becomes `index.html`). Placing files in subdirectories (`rest/01_users.md`, `sdk/01_client.md`) or adding an optional `<lang>/navbar.md` adds uppercase group labels above the `# H1` categories.

### 3.2. Supported Semantic Badges
Prefix an `## H2` heading with a backtick token to render a color-coded badge in both the sidebar and main page:

| Category | Backtick Prefix Tokens | Example Markdown Heading | Generated `#slug` |
| :--- | :--- | :--- | :--- |
| **Functions** | `` `def` ``, `` `fn` ``, `` `func` ``, `` `function` ``, `` `async` `` | `` ## `def` rectangle(xy, width, height) `` | `#rectangle` |
| **Classes / Types** | `` `class` ``, `` `interface` ``, `` `struct` `` | `` ## `class` BarChart `` | `#barchart` |
| **Methods / RPCs** | `` `method` ``, `` `rpc` `` | `` ## `method` BarChart.draw(xy) `` | `#barchart-draw` |
| **Constants / Events** | `` `const` ``, `` `attr` ``, `` `prop` ``, `` `event` `` | `` ## `const` Styles.Neutral `` | `#styles-neutral` |
| **Types / Enums** | `` `type` ``, `` `enum` `` | `` ## `enum` PhosphorIcon `` | `#phosphoricon` |
| **CLI Commands** | `` `cmd` ``, `` `cli` `` | `` ## `cmd` drawlib init project api `` | `#drawlib-init-project-api` |
| **HTTP Endpoints** | `` `GET` ``, `` `POST` ``, `` `PUT` ``, `` `PATCH` ``, `` `DELETE` ``, `` `HEAD` `` | `` ## `GET` /v1/users/<id> `` | `#v1-users-id` |

---

## 4. Configuring `[api]` in `drawlib.toml`

All sidebar expansion defaults, version badges, repository links, and top-right navigation links are controlled declaratively in `drawlib.toml`:

```toml
[project]
name = "my_api"
type = "api"
title = "My Platform API"
style = "default"

[i18n]
default_lang = "en"
langs = ["en", "ja"]

[api]
# Expand all sidebar categories by default so browser Ctrl+F / Cmd+F finds every symbol immediately.
# Set to false to collapse inactive categories while keeping the active page expanded.
sidebar_expanded = true

# Optional pill badge & GitHub icon beneath the top-left brand logo (plain string or per-locale table):
badge_text = { en = "v2.0 Stable", ja = "v2.0 安定版" }
badge_url = "https://github.com/example/my-api/releases"
repo_url = "https://github.com/example/my-api"

# Optional navigation links on the right side of the top header bar (left of language switcher):
header_links = [
  { label = { en = "Docs Site", ja = "ドキュメント" }, url = "https://docs.example.com" },
  { label = "GitHub", url = "https://github.com/example/my-api" },
]
```

---

## 5. Authoring & Review Checklist for `api` Projects

1. **Illustrate Every Category Page**: Place a concise `ArchitectureDiagram`, `SequenceDiagram`, `FlowDiagram`, `ClassDiagram`, or `ERDiagram` near the top of each `.md` page (`code=fold`, `text_size >= 10.0`, `50%+` neutral palette) so developers grasp request flows and data models before reading parameter tables.
2. **Keep `sidebar_expanded = true` Unless Requested Otherwise**: Leaving categories open ensures native browser `Ctrl+F` / `Cmd+F` searches across the entire API surface work out of the box, complemented by the built-in `/` quick filter and `Collapse All` button.
3. **Verify Links & `#slug` Anchors**: Always run `./<target>_src/build.sh` followed by `uv run drawlib serve <target>_html/ --check` and inspect `-g` coordinate grids + rendered HTML pages before delivery.
