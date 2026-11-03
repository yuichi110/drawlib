# Drawlib API Reference Project

This directory contains the Markdown reference pages, embedded Drawlib diagrams, and configuration assets for an **Illustrated API Reference** website (`type = "api"`).

> [!TIP]
> **Need Comprehensive Rules & Deep Guides?**  
> Run the built-in Drawlib manual commands:
> - `uv run drawlib rules show project-api`      : API project structure, `# H1` / `## H2` sidebar rules & `[api]` config
> - `uv run drawlib rules show overview`         : Cartesian `(0, 0)` geometry & drawing lifecycle
> - `uv run drawlib rules show style-guide`      : 50%+ neutral palette & typography guidelines
> - `uv run drawlib rules list`                  : List all specialized component & diagram manuals

---

## 1. Directory Structure

- `__SRC_DIR__/`: Source Markdown files and drawing code (**Source of Truth**).
  - `drawlib.toml`: Project manifest (`[project]`, `[i18n]`, `[api]`, and optional `[seo]`).
  - `__DEFAULT_LANG__/`: API reference Markdown files (`1 Markdown = 1 HTML Page`):
    - `00_overview.md`: API Overview, authentication, and system topology (`# H1` category + `## H2` sections).
    - `01_users.md`: REST endpoints with semantic HTTP method badges (`GET`, `POST`, `DELETE`).
    - `02_models.md`: SDK classes, helper functions, and relational data schemas (`class`, `def`).
  - `_assets/`: Shared static assets (`favicon.png`, `logo.png`, `logo_dark.png`).
  - `styles.py` / `utils.py`: Shared Drawlib theme tokens and reusable diagram helpers.
  - `style.css` / `template.html`: Responsive 2-column API stylesheet and Jinja2 layout template.
  - `build.sh`, `build_html.sh`, `build_markdown.sh`, `build_image.sh`, `serve.sh`: Build & preview scripts.
- `__OUT_HTML_DIR__/`: Generated static HTML reference (`index.html`, `<lang>/...`) (**Do not edit directly**).
- `__OUT_MARKDOWN_DIR__/`: Generated Markdown reference (**Do not edit directly**).
- `__OUT_IMAGES_DIR__/`: Extracted standalone diagram images (**Do not edit directly**).

---

## 2. How the Left Navigation Pane Works (`1 MD = 1 Page`)

Each `.md` file under `__SRC_DIR__/<lang>/` compiles into one HTML page:
1. **`# H1` Heading -> Category / Module Header**: Displayed as an accordion group in the left sidebar.
2. **`## H2` Headings -> Symbol / Endpoint Sub-list**: Displayed beneath its `# H1` category and linked via `#slug` anchors with automatic scroll-spy highlighting.
3. **Semantic Badges**: Prefixing an `## H2` heading with a backtick token automatically renders a color-coded badge in both the sidebar and main page:
   - **Code / SDK**: `` ## `def` verify_signature(payload, header, secret) ``, `` ## `class` User ``, `` ## `method` client.send(req) ``, `` ## `const` DEFAULT_TIMEOUT ``, `` ## `type` UserRole ``, `` ## `cmd` sync ``
   - **REST HTTP**: `` ## `GET` /v1/users ``, `` ## `POST` /v1/users ``, `` ## `PUT` /v1/users/<id> ``, `` ## `PATCH` /v1/users/<id> ``, `` ## `DELETE` /v1/users/<id> ``

---

## 3. Customizing `[api]` in `drawlib.toml`

Configure sidebar expansion, version badge, repository icon, and top-right links in `drawlib.toml`:

```toml
[api]
# Expand all sidebar categories by default so browser Ctrl+F / Cmd+F finds every symbol immediately
sidebar_expanded = true

# Optional version pill badge & GitHub repository icon beneath the top-left logo
badge_text = "v1.0"
repo_url = "https://github.com/example/my-api"

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
