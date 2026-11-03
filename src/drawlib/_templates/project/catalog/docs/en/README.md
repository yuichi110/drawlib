# Drawlib Catalog & Reference Project

This directory contains the Markdown catalog pages, embedded Drawlib diagrams, and configuration assets for an **Illustrated Catalog & Reference** website (`type = "catalog"`).

> [!TIP]
> **Need Comprehensive Rules & Deep Guides?**  
> Run the built-in Drawlib manual commands:
> - `uv run drawlib rules show project-catalog`  : Catalog project structure, `# H1` / `## H2` sidebar rules & `[catalog]` config
> - `uv run drawlib rules show overview`         : Cartesian `(0, 0)` geometry & drawing lifecycle
> - `uv run drawlib rules show style-guide`      : 50%+ neutral palette & typography guidelines
> - `uv run drawlib rules list`                  : List all specialized component & diagram manuals

---

## 1. Directory Structure

- `__SRC_DIR__/`: Source Markdown files and drawing code (**Source of Truth**).
  - `drawlib.toml`: Project manifest (`[project]`, `[i18n]`, `[catalog]`, and optional `[seo]`).
  - `__DEFAULT_LANG__/`: Catalog Markdown files (`1 Markdown = 1 HTML Page`):
    - `00_overview.md`: System overview, authentication, and topology (`# H1` category + `## H2` sections).
    - `01_users.md`: REST endpoints with semantic HTTP method badges (`GET`, `POST`, `DELETE`).
    - `02_models.md`: SDK classes, helper functions, and relational data schemas (`class`, `def`).
  - `_assets/`: Shared static assets (`favicon.png`, `logo.png`, `logo_dark.png`).
  - `styles.py` / `utils.py`: Shared Drawlib theme tokens and reusable diagram helpers.
  - `style.css` / `template.html`: Responsive 2-column catalog stylesheet and Jinja2 layout template.
  - `build.sh`, `build_html.sh`, `build_markdown.sh`, `build_image.sh`, `serve.sh`: Build & preview scripts.
- `__OUT_HTML_DIR__/`: Generated static HTML catalog (`index.html`, `<lang>/...`) (**Do not edit directly**).
- `__OUT_MARKDOWN_DIR__/`: Generated Markdown catalog (**Do not edit directly**).
- `__OUT_IMAGES_DIR__/`: Extracted standalone diagram images (**Do not edit directly**).

---

## 2. How the Left Navigation Pane Works (`1 MD = 1 Page`)

Each `.md` file under `__SRC_DIR__/<lang>/` compiles into one HTML page:
1. **`# H1` Heading -> Category / Domain Header**: Displayed as an accordion group in the left sidebar.
2. **`## H2` Headings -> Item / Symbol / Endpoint Sub-list**: Displayed beneath its `# H1` category and linked via `#slug` anchors with automatic scroll-spy highlighting.
3. **Semantic Badges**: Prefixing an `## H2` heading with a backtick token automatically renders a color-coded badge in both the sidebar and main page:
   - **Code / SDK / CLI**: `` ## `def` verify_signature(payload, header, secret) ``, `` ## `class` User ``, `` ## `method` client.send(req) ``, `` ## `const` DEFAULT_TIMEOUT ``, `` ## `type` UserRole ``, `` ## `cmd` sync ``
   - **REST HTTP**: `` ## `GET` /v1/users ``, `` ## `POST` /v1/users ``, `` ## `PUT` /v1/users/<id> ``, `` ## `PATCH` /v1/users/<id> ``, `` ## `DELETE` /v1/users/<id> ``
   - **General Catalogs (Services, Data, Config, Rules, Ops)**: `` ## `service` billing-api ``, `` ## `table` users ``, `` ## `schema` OrderEvent ``, `` ## `config` server.port ``, `` ## `env` LOG_LEVEL ``, `` ## `rule` DL001 ``, `` ## `error` E1004 ``, `` ## `token` PrimaryFlat ``, `` ## `adr` ADR-004 ``

---

## 3. Customizing `[catalog]` in `drawlib.toml`

Configure sidebar expansion, breadcrumb root label, version badge, repository icon, and top-right links in `drawlib.toml`:

```toml
[catalog]
# Expand all sidebar categories by default so browser Ctrl+F / Cmd+F finds every item immediately
sidebar_expanded = true

# Optional custom root label in the page breadcrumb (defaults to "Catalog" / "カタログ")
breadcrumb_root = "Catalog"

# Optional version pill badge & GitHub repository icon beneath the top-left logo
badge_text = "Catalog · v1.0"
repo_url = "https://github.com/example/my-catalog"

# Optional navigation links on the right side of the top header bar
header_links = [
  { label = { en = "Guides", ja = "ガイド" }, url = "https://docs.example.com" },
]
```

---

## 4. Building & Previewing

```bash
./__SRC_DIR__/build.sh          # Build HTML, Markdown, and standalone images
./__SRC_DIR__/serve.sh          # Start local preview server with live reload
./__SRC_DIR__/serve.sh --check  # Validate all internal links and #slug anchors
```
