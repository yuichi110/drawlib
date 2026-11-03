# Drawlib Illustrated Catalog & Reference Project Guidelines (`project-catalog`)

A **`catalog` project** (`drawlib init project catalog`) compiles a locale-structured directory of Markdown files (`catalog_src/<lang>/**/*.md`) into a **responsive 2-column catalog & reference website (`catalog_html/`)**, **GitHub-Flavored Markdown (`catalog_markdown/`)**, and **extracted diagram assets (`catalog_images/`)**.

Unlike a prose `site` project (which requires a manual `navbar.md`), a `catalog` project follows the **`1 Markdown = 1 HTML Page`** model with **automatic 2-tier sidebar extraction**:
- **`# H1` -> Left-Pane Category / Group Header** (`<details class="catalog-nav-group">`)
- **`## H2` -> Left-Pane Item / Symbol Sub-list** (`#slug` anchors + semantic badges + scroll-spy)

*(For general project scaffolding, see `uv run drawlib rules show project-overview`. For prose multi-page portals, see `uv run drawlib rules show project-site`. For the 3-stage review loop, see `uv run drawlib rules show review-guide`.)*

---

## 1. When to Choose a `catalog` Project

Choose `drawlib init project catalog` whenever the user wants an **enumerated, searchable 2-column catalog, dictionary, or technical reference** paired with Drawlib diagrams:
- **REST / GraphQL / gRPC & SDK API References**: HTTP endpoints (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `rpc`) and Python / TypeScript / Go / Rust modules (`def`, `class`, `method`, `const`, `type`).
- **CLI, Config & Flag Dictionaries**: CLI subcommands (`cmd`, `cli`), environment variables (`env`, `config`), feature flags (`flag`), and schema options (`option`, `param`).
- **Data, Event & Service Catalogs**: Database tables/views (`table`, `view`, `schema`, `entity`), webhook/Kafka events (`event`), microservices & batch pipelines (`service`, `component`, `job`, `pipeline`), and metrics (`metric`).
- **Governance, Runbook & Design System Catalogs**: Lint/security policies (`rule`, `policy`, `check`), error codes & incident runbooks (`error`, `warn`, `alert`, `critical`), ADRs (`adr`), and design/icon tokens (`token`, `style`, `color`, `icon`, `asset`).

```bash
# Scaffold a catalog / reference project (default target 'catalog', creates 'catalog_src/'):
uv run drawlib init project catalog [target] [-l <lang[,lang...]>] [-s <default|google|monochrome>]

# Examples:
uv run drawlib init project catalog
uv run drawlib init project catalog api -l en,ja -s google
uv run drawlib init project catalog services -l en,ja -s default
```

*(Note: Pass a custom `[target]` such as `api`, `services`, or `runbook` to name the source folder `api_src/`, `services_src/`, etc. while keeping `type = "catalog"` in `drawlib.toml`.)*

---

## 2. Directory Structure (`catalog_src/`)

Every `catalog` project uses the unified `<src_dir>/<lang>/` locale directory layout governed by `[i18n]` and `[catalog]` in `drawlib.toml`:

```text
.
├── catalog_src/               # [SOURCE OF TRUTH] Edit ONLY files here!
│   ├── drawlib.toml           # [MANDATORY] Project manifest (type = "catalog" + [i18n] + [catalog])
│   ├── en/                    # Locale catalog pages (1 Markdown = 1 HTML page)
│   │   ├── 00_overview.md     # Landing overview (auto-aliased to en/index.html & root index.html)
│   │   ├── 01_users.md        # Category: # Users API -> ## `GET` /v1/users, ...
│   │   └── 02_models.md       # Category: # Data & Models -> ## `class` User, ## `table` users, ...
│   ├── _assets/               # Static images, logos (logo.png, logo_dark.png, favicon.png)
│   ├── styles.py              # Shared Drawlib Styles & Colors
│   ├── utils.py               # Shared Python drawing helpers
│   ├── style.css              # Wide 2-column catalog stylesheet (drawlib css show catalog <preset>)
│   ├── template.html          # Jinja2 catalog sidebar + filter + scroll-spy template
│   ├── build.sh               # Master build script (HTML + Markdown + Images)
│   ├── build_html.sh          # Static HTML build (catalog_html/)
│   ├── build_markdown.sh      # GitHub Markdown build (catalog_markdown/)
│   ├── build_image.sh         # Standalone diagram extraction (catalog_images/)
│   └── serve.sh               # Local preview server + broken link/anchor checker
├── catalog_html/              # [GENERATED] Static HTML catalog site (index.html + <lang>/**)
├── catalog_markdown/          # [GENERATED] Rendered Markdown for GitHub
└── catalog_images/            # [GENERATED] Extracted diagram PNG/WebP images
```

```drawlib align=center code=fold file=project_catalog_architecture.png caption="Catalog Project Architecture (1 Markdown = 1 Page -> # H1 Category & ## H2 Item Sidebar)"
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
    "Illustrated Catalog Architecture (catalog_src/<lang>/*.md -> catalog_html/)",
    style=Styles.DarkBold.patch(text_size=12.5),
)

# 1. Markdown Source
rectangle((26, 24), width=38, height=34, style=Styles.Neutral.patch(shape_r=2.0))
phosphor.file_md((11.5, 35.5), width=4.8, style=Styles.PrimaryBold)
text((28, 35.5), "1. Markdown Page", style=Styles.PrimaryBold.patch(text_size=11.0))
text(
    (26, 20.5),
    "# Core Catalog (H1)\n[Top Hero Diagram]\n## `service` auth-api\n## `GET` /v1/users\n## `table` users",
    style=Styles.Dark.patch(text_size=9.8),
)

line((46, 24), (54, 24), arrow_head="->", style=Styles.PrimaryBold)

# 2. Auto-Extracted Left Pane
rectangle((75, 24), width=38, height=34, style=Styles.PrimaryFlat.patch(shape_r=2.0))
phosphor.sidebar((60.5, 35.5), width=4.8, style=Styles.WhiteBold)
text((77, 35.5), "2. Left Sidebar", style=Styles.WhiteBold.patch(text_size=11.0))
text(
    (75, 20.5),
    "▼ Core Catalog  [3]\n  [service] auth-api\n  [GET]     /v1/users\n  [table]   users\n• Open + `/` Quick Filter",
    style=Styles.White.patch(text_size=9.8),
)

line((95, 24), (103, 24), arrow_head="->", style=Styles.PrimaryBold)

# 3. Wide 2-Column Main View
rectangle((124, 24), width=38, height=34, style=Styles.SecondaryNeutral.patch(shape_r=2.0))
phosphor.code((109.5, 35.5), width=4.8, style=Styles.SecondaryBold)
text((126, 35.5), "3. Main Catalog", style=Styles.SecondaryBold.patch(text_size=11.0))
text(
    (124, 20.5),
    "• Architecture / ER visuals\n• Badged H2 anchors\n• Spec & schema tables\n• Prev / Next pager",
    style=Styles.Dark.patch(text_size=9.8),
)

save()
```

---

## 3. Heading Hierarchy & Semantic Badges (`# H1` / `## H2`)

### 3.1. `1 Markdown = 1 Page` Mapping Rules
1. **`# H1` (Category / Group Title)**: The first `# H1` in each `.md` file names the accordion group in the left sidebar (and falls back to a humanized filename stem if omitted). Dotted or lowercase module names (e.g. `# drawlib.shapes`) automatically style in monospace.
2. **`## H2` (Catalog Item / Symbol Entries)**: Every `## H2` outside fenced code blocks becomes a clickable sub-item under its `# H1` category (`#slug`) with automatic scroll-spy highlighting.
3. **`### H3` / `#### H4` (Sub-sections)**: Receive deterministic `id="..."` anchors in the main body (for `Parameters`, `Schema`, `Remediation`, `Examples`) without cluttering the left sidebar.
4. **Angle-Bracket Safety**: Placeholders like `` ## `GET` /v1/users/<id> `` or `Result<T>` are preserved and HTML-escaped automatically — never stripped as raw HTML tags.
5. **Optional Subdirectory Grouping or `navbar.md`**: Numbered root files (`00_overview.md`, `01_users.md`) sort deterministically (`index.md` or `00_*` becomes `index.html`). Placing files in subdirectories (`rest/01_users.md`, `data/01_tables.md`) or adding an optional `<lang>/navbar.md` adds uppercase group labels above the `# H1` categories.

### 3.2. Supported Semantic Badges
Prefix an `## H2` heading with a backtick token to render a color-coded badge in both the sidebar and main page:

| Category | Backtick Prefix Tokens | Example Markdown Heading | Generated `#slug` |
| :--- | :--- | :--- | :--- |
| **Functions & Pipelines** | `` `def` ``, `` `fn` ``, `` `func` ``, `` `function` ``, `` `async` ``, `` `job` ``, `` `pipeline` `` | `` ## `def` rectangle(xy, width, height) `` | `#rectangle` |
| **Classes, Services & Tables** | `` `class` ``, `` `interface` ``, `` `struct` ``, `` `service` ``, `` `svc` ``, `` `component` ``, `` `module` ``, `` `package` ``, `` `table` ``, `` `view` `` | `` ## `service` billing-worker `` | `#billing-worker` |
| **Methods & RPCs** | `` `method` ``, `` `rpc` `` | `` ## `method` BarChart.draw(xy) `` | `#barchart-draw` |
| **Config, Constants & Metrics** | `` `const` ``, `` `attr` ``, `` `prop` ``, `` `event` ``, `` `config` ``, `` `cfg` ``, `` `env` ``, `` `flag` ``, `` `option` ``, `` `param` ``, `` `metric` `` | `` ## `env` DRAWLIB_CACHE_DIR `` | `#drawlib-cache-dir` |
| **Schemas, Types & Design Tokens** | `` `type` ``, `` `enum` ``, `` `schema` ``, `` `entity` ``, `` `model` ``, `` `token` ``, `` `style` ``, `` `color` ``, `` `font` ``, `` `icon` ``, `` `asset` ``, `` `template` `` | `` ## `table` user_accounts `` | `#user-accounts` |
| **CLI, Rules & ADRs** | `` `cmd` ``, `` `cli` ``, `` `rule` ``, `` `policy` ``, `` `check` ``, `` `adr` `` | `` ## `cmd` drawlib init project catalog `` | `#drawlib-init-project-catalog` |
| **HTTP Endpoints** | `` `GET` ``, `` `POST` ``, `` `PUT` ``, `` `PATCH` ``, `` `DELETE` ``, `` `HEAD` `` | `` ## `GET` /v1/users/<id> `` | `#v1-users-id` |
| **Status & Severity** | `` `ok` ``, `` `active` ``, `` `stable` ``, `` `warn` ``, `` `warning` ``, `` `error` ``, `` `err` ``, `` `alert` ``, `` `critical` ``, `` `deprecated` `` | `` ## `error` E1042: Connection Pool Exhausted `` | `#e1042-connection-pool-exhausted` |

---

## 4. Configuring `[catalog]` in `drawlib.toml`

All sidebar expansion defaults, breadcrumb root labels, version badges, repository links, and top-right navigation links are controlled declaratively in `drawlib.toml`:

```toml
[project]
name = "platform_catalog"
type = "catalog"
title = "Platform Service & API Catalog"
style = "default"

[i18n]
default_lang = "en"
langs = ["en", "ja"]

[catalog]
# Expand all sidebar categories by default so browser Ctrl+F / Cmd+F finds every item immediately.
# Set to false to collapse inactive categories while keeping the active page expanded.
sidebar_expanded = true

# Optional custom root label in the top sub-bar breadcrumb (defaults to "Catalog" / "カタログ"):
breadcrumb_root = { en = "API Reference", ja = "API リファレンス" }

# Optional pill badge & GitHub icon beneath the top-left brand logo (plain string or per-locale table):
badge_text = { en = "v2.0 Stable", ja = "v2.0 安定版" }
badge_url = "https://github.com/example/platform/releases"
repo_url = "https://github.com/example/platform"

# Optional navigation links on the right side of the top header bar (left of language switcher):
header_links = [
  { label = { en = "Docs Site", ja = "ドキュメント" }, url = "https://docs.example.com" },
  { label = "GitHub", url = "https://github.com/example/platform" },
]
```

---

## 5. Authoring & Review Checklist for `catalog` Projects

1. **Illustrate Every Category Page**: Place a concise `ArchitectureDiagram`, `SequenceDiagram`, `FlowDiagram`, `ClassDiagram`, `ERDiagram`, or `SmartArt` near the top of each `.md` page (`code=fold`, `text_size >= 10.0`, `50%+` neutral palette) so readers grasp topologies, data flows, and relationships before scanning individual items.
2. **Keep `sidebar_expanded = true` Unless Requested Otherwise**: Leaving categories open ensures native browser `Ctrl+F` / `Cmd+F` searches across the entire catalog work out of the box, complemented by the built-in `/` quick filter and `Collapse All` button.
3. **Verify Links & `#slug` Anchors**: Always run `./<target>_src/build.sh` followed by `uv run drawlib serve <target>_html/ --check` and inspect `-g` coordinate grids + rendered HTML pages before delivery.
