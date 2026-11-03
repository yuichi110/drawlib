# Illustrated API Reference Project (`api`) Design & Implementation Plan

## 1. Background & Goal

Drawlib currently provides four project archetypes via `drawlib init project`:

- **`images`**: Standalone Python illustration scripts compiled into raster/vector images.
- **`doc`**: Linear specification or report merged into HTML, A4 PDF, and MS Word (`.docx`).
- **`site`**: Multi-page narrative documentation website (`2-column` layout, story-driven prose, Top Hero diagram conventions).
- **`slide`**: `16:9` presentation deck compiled into HTML slides, PDF, and MS PowerPoint (`.pptx`).

While `site` excels at narrative guides and tutorials, forcing high-density **API References** (REST/GraphQL/gRPC/MCP endpoints, CLI command references, or Python/SDK module dictionaries) into `site` creates layout and authoring friction:

1. Narrative `site` pages rely on manually curated `navbar.md` page links without exposing per-endpoint/per-function `## H2` symbols in the left sidebar.
2. `site` AI authoring rules (`project-site`) enforce narrative patterns (such as placing a Top Hero diagram at lines 5–15 and `2+` diagrams on every page) that conflict with reference dictionary pages.
3. Mechanical API doc generators (Sphinx, Swagger UI, pdoc) lack Drawlib's signature capability: **embedding declarative illustrations (`ArchitectureDiagram`, `SequenceDiagram`, `ERDiagram`, coordinate anatomy diagrams) directly alongside API specifications**.

This plan introduces a dedicated **5th project archetype: `api`** (`drawlib init project api [target]`) for **"Illustrated API Reference as Code"**.

---

## 2. Core User Experience & Structural Model

### 2.1. `1 Markdown File = 1 HTML Page` with Automatic `H1` / `H2` Left-Pane Hierarchy

- Each Markdown file under `<target>_src/<lang>/**/*.md` compiles into **1 standalone HTML page** (preserving the familiar multi-page mental model of `site`).
- **Automatic Left-Pane Construction (No `navbar.md` Required)**:
  - Files are discovered automatically in deterministic path/filename order (e.g. `00_overview.md`, `01_authentication.md`, `02_users.md`, `03_orders.md`, or `index.md` first when present).
  - If subdirectories exist (e.g. `01_rest/01_users.md`, `02_webhooks/01_events.md`), normalized directory names render as top-level group labels in the left sidebar.
  - For every Markdown file:
    - **`# H1`** becomes the **Category / Page Header** in the left pane (linking to `<page>.html`).
    - **`## H2`** headings inside that file are automatically extracted (ignoring fenced code blocks and HTML comments) and rendered in document order as the **API Item List** under that `H1` (linking to `<page>.html#<slug>`).
    - **`### H3` / `#### H4`** (e.g. `### Parameters`, `### Request Body`, `### Returns`, `### Example`) receive deterministic `id="..."` attributes in the HTML body for deep linking, **without** cluttering the left-pane list.
  - Optional override: If a locale directory explicitly provides `navbar.md`, its file order and optional `## Group` headings determine page ordering while still auto-populating each page's `H2` symbol list.

### 2.2. Wide 2-Column Layout Optimized for Diagrams & Signatures

- Because every page's `## H2` endpoints/functions are already listed directly in the left pane (with scroll-spy highlighting), a redundant 3rd right-hand "On this page" column is unnecessary.
- Keeping a clean **2-column layout** (`Left Reference Tree` + `Wide Main Content` up to `1000px`) gives ample horizontal room for:
  - Embedded ````drawlib```` illustrations (auth sequence flows, webhook state machines, geometry anchor diagrams, ER schemas),
  - Wide monospace function/endpoint signatures, and
  - Multi-column `Parameter | Type | Required | Default | Description` tables.

### 2.3. Browser `Ctrl+F` Compatibility & Configurable Sidebar Expansion (`[api]`)

Developers frequently use native browser search (`Ctrl+F` / `Cmd+F`) to jump directly to an endpoint or function across the entire API surface. Collapsing inactive sections by default hides off-page `H2` items from browser find-in-page.

- **`drawlib.toml` `[api]` Configuration**:
  ```toml
  [api]
  sidebar_expanded = true  # true (default): expand all H1 sections | false: collapse inactive sections
  ```
- **Default Behavior (`sidebar_expanded = true`)**:
  - When `[api]` or `sidebar_expanded` is omitted in `drawlib.toml`, **`sidebar_expanded` defaults to `True`**.
  - `drawlib init project api` explicitly writes `[api]\nsidebar_expanded = true` into the scaffolded `drawlib.toml` AND sets the starter `template.html` default to open.
  - All `<details class="api-nav-group" open>` elements render open in static HTML so native browser `Ctrl+F` / `Cmd+F` immediately matches every `H2` across all pages.
- **Collapsed Mode (`sidebar_expanded = false`)**:
  - Inactive pages render collapsed (`<details class="api-nav-group">`), while the **currently active page's `<details>` always renders `open`** so the reader can see and jump within the current page's `H2` items.
- **Interactive Controls & Scroll Preservation**:
  - **Sidebar Scroll Persistence**: Navigating between pages preserves the left sidebar's `scrollTop` in `sessionStorage` (`drawlib-api-sidebar-scroll`) with an automatic `scrollIntoView({ block: "nearest" })` fallback on the active item so clicking lower items never resets the sidebar back to the top.
  - **Expand All / Collapse All Toggle + Quick Filter Input**: A compact toolbar at the top of the left sidebar lets readers filter `H1`/`H2` items by substring in real time or toggle all sections open/closed with one click.
  - **Scroll-Spy Active Highlight**: An `IntersectionObserver` highlights the currently visible `H2` item in the left sidebar as the user scrolls down a page.

### 2.4. API-Tailored Markdown Presentation (Zero Proprietary Syntax Lock-In)

Standard GFM Markdown automatically receives clean API styling via heading post-processing and `targets/api.css`:

- **Semantic Method / Kind Badges on `H2`**:
  - Writing leading inline code in an `H2`—such as:
    - HTTP endpoints: `` ## `GET` /v1/users ``, `` ## `POST` /v1/users ``, `` ## `PUT` /v1/users/{id} ``, `` ## `PATCH` ... ``, `` ## `DELETE` ... ``
    - Code / CLI symbols: `` ## `def` rectangle(xy, width, height, ...) ``, `` ## `class` ArchitectureDiagram ``, `` ## `async` run_task(...) ``, `` ## `cmd` drawlib build html ``
  - Automatically renders the leading token as a color-coded semantic badge (`GET` blue, `POST` green, `PUT`/`PATCH` amber, `DELETE` red, `class`/`def`/`async`/`cmd` indigo/neutral) paired with a crisp monospace signature bar and a hover `#` permalink button.
  - Standard headings without backticks (e.g. `## Authentication`, `## Error Codes`) render cleanly as standard reference section headers with `#` permalinks.
- **Collapsible Schemas & Payloads**:
  - Native `<details><summary>Response Schema (200 OK)</summary>...</details>` blocks receive polished card styling matching Light/Dark themes.
- **`llms.txt` Integration**:
  - When `[seo]` is enabled (`llms_txt = true`), `llms.txt` automatically indexes all API pages and summaries so AI coding agents can ingest the reference directly.

---

## 3. Detailed Technical Specifications

### 3.1. Manifest Schema (`src/drawlib/_builder/_common/manifest.py`)

- Extend `ProjectArchetype`:
  ```python
  ProjectArchetype = Literal["images", "doc", "site", "slide", "api"]
  ```
- Update `_VALID_ARCHETYPES`:
  - Map `"api": "api"` strictly (no `ref` or `reference` aliases).
- Add `"api"` to `_I18N_ARCHETYPES` (`frozenset({"doc", "site", "slide", "api"})`) so `[i18n]` and `[seo]` work identically on `api` projects (single-locale `langs = ["en"]` or multi-locale `langs = ["en", "ja"]`).
- Add `ApiConfig` model:
  ```python
  class ApiConfig(BaseModel):
      """Parsed configuration from the ``[api]`` section of ``drawlib.toml``."""

      model_config = ConfigDict(frozen=True)

      sidebar_expanded: bool = True
  ```
- Attach `api: ApiConfig | None = None` to `ProjectManifest` (populated with `ApiConfig(sidebar_expanded=True)` by default whenever `project.type == "api"`):
  - Reject `[api]` on non-`api` project types (`images`, `doc`, `site`, `slide`) with a descriptive `ValueError`.
  - Reject unknown keys in `[api]` and non-boolean `sidebar_expanded` values with a `ValueError`.
- Update `format_project_manifest_toml()`:
  - When `project_type == "api"`, emit:
    ```toml
    [api]
    sidebar_expanded = true
    ```
    plus the commented `# [seo]` discovery template (unless active `seo` is provided).

### 3.2. Heading Extractor, Anchor Injection & Navigation Builder (`src/drawlib/_builder/doc_builder/`)

Create a dedicated module `src/drawlib/_builder/doc_builder/api_nav.py` (keeping `html.py` modular):

1. **Heading & Slug Extraction (`extract_api_headings`)**:
   - Masks fenced code blocks (```` ``` ````, ```` ```` ````, `~~~`) and HTML comments before scanning ATX headings (`#`–`####`).
   - Extracts:
     - `h1_title`: First `# H1` text (plain text stripped of inline Markdown formatting for sidebar display; falls back to humanized filename stem if absent).
     - `h2_items`: Ordered list of `ApiNavAnchor(title, badge, signature, anchor_id)` for every `## H2` in the file.
   - **Deterministic Slug Generator (`slugify_heading`)**:
     - Normalizes heading text into deterministic, URL-safe slugs (preserving word characters including CJK/Unicode letters/digits or clean ASCII hyphenation, collapsing punctuation/whitespace to `-`), deduplicating collisions within the same page via `-2`, `-3` suffixes.
2. **HTML Heading Post-Processor (`inject_api_heading_ids_and_badges`)**:
   - Runs on rendered HTML `<h2>`–`<h4>` elements (outside `<pre>`/`<code>`):
     - Injects exact matching `id="<anchor_id>"` attributes so every sidebar link and deep link resolves 1-to-1.
     - Detects leading `<code>METHOD</code>Rest` inside `<h2>` when matching known semantic badges (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `HEAD`, `OPTIONS`, `def`, `fn`, `func`, `class`, `type`, `interface`, `enum`, `const`, `prop`, `event`, `async`, `cmd`, `rpc`) and wraps them in `<span class="api-badge api-badge-<kind>">...</span><code class="api-sig">...</code>`.
     - Appends `<a class="api-heading-anchor" href="#<anchor_id>" aria-label="Permalink">#</a>` to `<h2>` and `<h3>`.
3. **Locale API Tree Resolution (`build_api_sidebar_tree`)**:
   - Collects all `.md` files in `<input_abs>/<lang>` (or follows optional `navbar.md` file order if present).
   - Determines landing index source:
     - Uses `index.md` if present; otherwise uses the first sorted `.md` file (e.g. `00_overview.md`) to populate `<lang>/index.html` and root `/index.html` (rebasing relative URLs cleanly so there is never a missing `index.html`).
   - Produces template-ready `api_nav_groups` / `api_pages` structures:
     - Optional directory section heading (when files live in subdirectories like `01_core/...`)
     - Page entry: `title` (`H1`), `url`, `active` (`bool`), `expanded` (`True` if `sidebar_expanded` is `True` OR `active` is `True`), and `items` (list of `{ title, badge, url, anchor }`).

### 3.3. Compiler & Builder Dispatch Updates

1. **`src/drawlib/_builder/doc_builder/compiler/html.py`**:
   - In `build_html()`, dispatch `manifest.project.type == "api"` to `_build_i18n_api_html(...)`.
   - Reuse `BuildImageCache`, `DrawlibBlockProcessor`, per-locale `style.css` font localization, language switcher context (`2+` locales), root `index.html` generation, `bundle_svg_fonts()`, and SEO/OGP/`sitemap.xml`/`robots.txt`/`llms.txt` generation.
2. **`src/drawlib/_builder/doc_builder/i18n.py`**:
   - Support `project_type="api"` in `validate_i18n_project()` (multi-locale file-set parity + skeleton parity across locales, without requiring `navbar.md` or `index.md`).
3. **`src/drawlib/_builder/doc_builder/compiler/markdown.py` & `src/drawlib/_builder/image_builder.py`**:
   - Allow `drawlib build markdown <api_src>` and `drawlib build image <api_src>` on `type = "api"` projects (sharing diagram deduplication just like `site`/`doc`).
4. **`src/drawlib/_builder/doc_builder/compiler/pdf.py`, `docx.py`, `src/drawlib/_slide/compiler.py`**:
   - Add explicit guard clauses for `manifest.project.type == "api"` raising clear, actionable `ValueError` messages directing users to `drawlib build html`.

### 3.4. CSS Target & Starter Template (`src/drawlib/_templates/`)

1. **CSS Architecture (`src/drawlib/_templates/css/targets/api.css` & `_css.py`)**:
   - Add `"api"` to `list_css()`, `get_css()`, and `export_css()` (`Layer 1 Theme Tokens` + `code.css` + `markdown.css` + `targets/api.css`).
   - `targets/api.css` defines:
     - Wide 2-column responsive layout (`--sidebar-width: 300px`, wide content container `max-width: 1000px`).
     - Sidebar filter toolbar (`input.api-filter-input` + Expand/Collapse toggle button).
     - Collapsible `<details class="api-nav-group">` + `<summary>` chevron styling + nested `.api-nav-h2-list` items with compact monospace/badge pills and active scroll-spy indicator.
     - Semantic `.api-badge-*` colors (harmonized for both Light and Dark themes) and `.api-heading-anchor` hover permalinks.
2. **Project Template (`src/drawlib/_templates/project/api/`)**:
   - `build.sh.template`, `build_html.sh.template`, `build_image.sh.template`, `build_markdown.sh.template`, `serve.sh.template`
   - `template.html.template` (with `sidebar_expanded | default(true)` handling, filter input, Expand/Collapse All button, `sessionStorage` scroll persistence, and `IntersectionObserver` scroll-spy)
   - Starter content in `docs/en/` and `docs/ja/` (plus `docs_i18n/ja/`):
     - `00_overview.md` — Service overview, base URL / auth summary, and an architecture ````drawlib```` diagram.
     - `01_users.md` — `GET /v1/users`, `POST /v1/users`, `DELETE /v1/users/{id}` with parameter tables, collapsible JSON response schema, and an auth/create ````drawlib```` sequence diagram.
     - `02_models.md` — Core resource models / SDK types with an ER/schema ````drawlib```` diagram.
3. **Scaffolding & CLI (`src/drawlib/_templates/_project.py` & `src/drawlib/_cli/commands/init.py`)**:
   - Register `"api"` in `PROJECT_TYPES`, `_CANONICAL_TYPE_MAP` (`"api": "api"`), `_I18N_PROJECT_TYPES`, and `default_names` (`"api": "api"` -> `api_src/`, `api_html/`, `api_images/`).
   - Add `drawlib init project api [target] [-s/--style] [-l/--lang] [-f/--force]` in `src/drawlib/_cli/commands/init.py` and include `./<target>_src/serve.sh` in `_print_init_success()`.

### 3.5. Link Scanner Enhancement (`src/drawlib/_http_server/_link_scanner.py`)

- Verify that `drawlib serve <api_html> --check` validates all generated cross-page and intra-page links cleanly, and add unit test assertions ensuring every sidebar `<a href="...#slug">` matches an existing `id="slug"` in the target HTML file.

### 3.6. Embedded AI Rules & Official Documentation Dogfooding

1. **Embedded Agent Rules (`src/drawlib/_rules/`)**:
   - Create `src/drawlib/_rules/project_api.md` documenting `drawlib init project api`, `[api] sidebar_expanded`, `H1`/`H2` heading structure, semantic badges (`` `GET` ``, `` `POST` ``, `` `def` ``, `` `class` ``), and purposeful diagram placement guidelines.
   - Register `"project-api": ("project_api.md",)` in `src/drawlib/_builder/rules_builder.py`.
   - Update `project_overview.md`, `cli.md`, `agent_instruction.md`, and `.agents/rules/drawlib.md` to list the 5 project archetypes (`images`, `doc`, `site`, `api`, `slide`).
2. **Official Documentation Site (`docs_src/site/`)**:
   - Add `docs_src/site/en/09_doc_builder_and_cli/project_api.md` and `docs_src/site/ja/09_doc_builder_and_cli/project_api.md` (with 100% EN/JA skeleton parity and visual diagrams).
   - Update `docs_src/site/{en,ja}/navbar.md`, `09_doc_builder_and_cli/overview.md`, and `09_doc_builder_and_cli/cli_reference.md`.

---

## 4. Phased Implementation Steps

1. **Phase 1 — Manifest & CSS Foundation**:
   - Implement `ApiConfig` and `"api"` archetype support in `manifest.py` and `_templates/_css.py` + `css/targets/api.css`.
2. **Phase 2 — `api_nav.py` & HTML/Markdown/Image Compiler Integration**:
   - Implement heading extraction, deterministic slugging, badge/anchor HTML post-processing, landing `index.html` resolution, and `_build_i18n_api_html()` in `doc_builder`.
3. **Phase 3 — Starter Templates & CLI `drawlib init project api`**:
   - Create `src/drawlib/_templates/project/api/` (`template.html.template`, scripts, EN/JA starter `.md` files) and wire up `_project.py` + `_cli/commands/init.py` + `css.py`.
4. **Phase 4 — Unit & Integration Tests**:
   - Add comprehensive tests covering `[api]` manifest validation, `sidebar_expanded = true` vs `false` HTML output, `H1`/`H2` extraction (including fenced code block masking & duplicate heading deduplication), multi-locale `en,ja` builds, SEO/`llms.txt` generation, CLI `drawlib init project api` -> `build html` -> `serve --check`, and XSS escaping.
5. **Phase 5 — Rules, Docs Dogfooding & Visual Inspection**:
   - Add `project_api.md` rule and official EN/JA docs page, run `./dcli code-check all` and `./dcli test all`, build docs, and visually inspect rendered `api` starter pages (Light & Dark modes, expanded vs collapsed sidebar, `Ctrl+F` behavior, and diagram rendering) via Playwright/grid review.

---

## 5. Verification Plan

### 5.1. Functional & Regression Verification

- Run targeted unit tests during development:
  - `./dcli test target doc-builder`
  - `./dcli test target cli`
- Run full quality and test suites:
  - `./dcli code-check all` (Ruff lint/format, Ty static type check, `@validate_call` docstring check)
  - `./dcli test drawlib`
- End-to-end scaffold & build smoke test in `.drawlib/scratch/`:
  - Scaffold single-locale (`en`), Japanese (`ja`), and multi-locale (`en,ja`) `api` projects via `uv run drawlib init project api`.
  - Test both `sidebar_expanded = true` (default) and `sidebar_expanded = false`, verifying `<details open>` attributes, landing `index.html` generation, `drawlib serve --check`, and Playwright visual screenshots in Light/Dark modes.
- Official documentation build & link check:
  - `./dcli docs build site`
  - `./dcli docs serve site --check`

### 5.2. Security Verification Plan

- **XSS & Output Encoding (`api_nav.py`, `exporter_html.py`, `api/template.html.template`)**:
  - Verify all extracted `H1`/`H2` titles, badge labels, generated `id`/`href` attributes, and SEO tags are strictly HTML-escaped (`html.escape(..., quote=True)`) and all Jinja2 template attributes are double-quoted.
  - Add dedicated unit tests with malicious headings (e.g. `# <script>alert(1)</script>`, `` ## `GET` "><img src=x onerror=alert(1)> ``) asserting zero unescaped tags or attribute breakouts in compiled HTML.
- **Safe Vanilla JavaScript DOM Manipulation (`api/template.html.template`)**:
  - Strictly prohibit `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write`, `eval`, and `alert()` in template scripts.
  - Implement sidebar filtering, expand/collapse toggling, scroll-spy highlighting, and scroll restoration exclusively via `textContent`, `hidden` / `classList`, `details.open`, and validated numeric `scrollTop`.
- **Client Storage & Local Server Safety**:
  - `localStorage` (`drawlib-theme`) and `sessionStorage` (`drawlib-api-sidebar-scroll`) store only non-sensitive UI preferences (`"light"`/`"dark"` and finite scroll offsets), never credentials or PII.
  - Local preview server (`drawlib serve`) binds strictly to `127.0.0.1` by default.
  - *Note on non-applicable web-backend controls*: Drawlib's `api` project compiler is an offline static-site generator with no user authentication, session cookies, CSRF endpoints, file upload endpoints, or application SQL user database (build cache uses local parameterized SQLite only); any future server-side extensions will document `TODO(security)` items accordingly.
- **Path Traversal & Input Validation (`manifest.py`, `_project.py`)**:
  - Validate `[api]` keys against a strict allow-list (`{"sidebar_expanded"}`) and enforce existing `realpath` + `commonpath` confinement on all project assets and `[seo].og_image`.
