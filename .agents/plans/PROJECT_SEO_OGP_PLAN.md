# Project-Managed SEO, OGP & `llms.txt` via `drawlib.toml`

## 1. Background & Goal

Previously, Drawlib's HTML documentation (`site`, `doc`) and presentation (`slide`) compilers generated localized `<html lang>` and relative `hreflang` links, but lacked project-level configuration for:

- Search Engine Optimization (`<meta name="description">`, `<link rel="canonical">`, absolute `hreflang`, `sitemap.xml`, `robots.txt`)
- Social Graph / SNS Previews (`og:*` Open Graph tags and `twitter:*` Card tags for X, Slack, Discord, Zenn, Hatena, LinkedIn)
- AI Crawler & Agent Indexing (`llms.txt` following the `llmstxt.org` specification)

Instead of hardcoding metadata in Drawlib's official documentation build scripts, this plan introduces declarative `[seo]` and `[i18n.descriptions]` support in `drawlib.toml` for all web-producing archetypes (`site`, `doc`, and `slide`), and dogfoods it on the official documentation site (`https://www.drawlib.com`).

---

## 2. `drawlib.toml` Manifest Schema

### 2.1 `[seo]` Section (`site`, `doc`, `slide`)

```toml
[seo]
site_url = "https://www.drawlib.com"
og_image = "_assets/ogp.png"
twitter_card = "summary_large_image"
twitter_site = "@handle"       # optional
sitemap = true                 # generates sitemap.xml when site_url is set
robots = true                  # generates robots.txt
llms_txt = true                # generates llms.txt (llmstxt.org Markdown index)
```

- **Supported Archetypes**: `"site"`, `"doc"`, `"slide"`. Specifying `[seo]` on `"images"` raises a descriptive `ValueError`.
- **Strict Validation**:
  - Unknown keys in `[seo]` raise `ValueError` to catch configuration typos early.
  - `site_url`: Optional `http://` or `https://` URL without query/fragment or unsafe characters; normalized with trailing `/` stripped.
  - `og_image`: Either a validated `http://`/`https://` URL or a project-relative file path confined within the project root (`os.path.realpath` + `os.path.commonpath` check blocking `..` traversal, symlink escapes, absolute paths, and `file:`/`javascript:`/`data:` schemes) whose target file exists on disk.
  - `twitter_card`: `"summary_large_image"` (default) or `"summary"`.
  - `twitter_site`: Optional X handle matching `^@?[A-Za-z0-9_]{1,30}$` (normalized with leading `@`).
  - `sitemap`, `robots`, `llms_txt`: Strict booleans (`True` by default when `[seo]` table is present).

### 2.2 `[i18n.descriptions]` Section (`site`, `doc`, `slide`)

```toml
[i18n.descriptions]
en = "Pure-Python Illustration as Code and Illustrated Documentation as Code library for AI agents."
ja = "AI エージェント時代の Illustration as Code・図解ドキュメント生成 Python ライブラリ。"
```

- Optional table under `[i18n]` providing localized project summaries keyed by normalized language codes in `[i18n].langs`.
- Used for localized fallback descriptions, landing/deck summaries, and multi-locale entries in `llms.txt`.

### 2.3 Scaffolding (`drawlib init project`)

- `format_project_manifest_toml()` appends a commented `# [seo]` block on `doc`, `site`, and `slide` archetypes by default so users discover the feature immediately while keeping `manifest.seo = None` until enabled.

---

## 3. Compiler & Output Specifications

### 3.1 Canonical Public URL Resolution

When `seo.site_url` is set (e.g. `https://www.drawlib.com`):

- `index.html` (root) -> `https://www.drawlib.com/`
- `<lang>/index.html` or `<subpath>/index.html` -> `https://www.drawlib.com/<lang>/` or `https://www.drawlib.com/<subpath>/`
- `<lang>/<path>/<page>.html` -> `https://www.drawlib.com/<lang>/<path>/<page>.html`

Every canonical tag, `og:url`, `hreflang` `<link rel="alternate">`, `sitemap.xml` `<loc>`, and `llms.txt` link uses this exact resolver so `canonical` and `hreflang` URLs match 1-to-1. Meanwhile, interactive UI language switcher `<a href="...">` links remain relative so `drawlib serve` works offline.

### 3.2 HTML `<head>` Metadata Injection

When `[seo]` is configured (`manifest.seo is not None`), `render_html_document()` (`site` & `doc`), `_render_locale_index_html()` (`slide`), and `write_root_redirect_html()` (`slide` root redirect) emit:

- `<meta name="description" content="...">` (extracted from the page's first Markdown prose paragraph, with fallback to `[i18n.descriptions][lang]` -> `[project].description`)
- `<link rel="canonical" href="...">` (when `site_url` is set; on `slide` root redirect, points to `<site_url>/<default_lang>/`)
- `<meta property="og:type" content="website">`
- `<meta property="og:site_name" content="...">`
- `<meta property="og:title" content="...">` (`<Page Title> — <Site Title>` when distinct)
- `<meta property="og:description" content="...">`
- `<meta property="og:url" content="...">` (when `site_url` is set)
- `<meta property="og:image" content="...">` (absolute URL when `site_url` is set, else relative path; asset automatically copied to `<out_dir>`)
- `<meta property="og:locale" content="...">` and `<meta property="og:locale:alternate" content="...">`
- `<meta name="twitter:card" content="...">`, `twitter:site` (optional), `twitter:title`, `twitter:description`, `twitter:image`

PDF compilation (`render_pdf_document`) is unaffected. Templates (`site/template.html.template`, `doc/template.html.template`, `docs/docs_src/template.html`) render `{{ seo_meta_html | default('') | safe }}`, with idempotent fallback injection in `_ensure_i18n_head_metadata()` for custom legacy templates.

### 3.3 `sitemap.xml`, `robots.txt`, and `llms.txt`

- **`sitemap.xml`** (generated when `seo.sitemap` is `True` and `seo.site_url` is non-empty):
  - Valid UTF-8 Sitemap 0.9 XML with `xmlns:xhtml="http://www.w3.org/1999/xhtml"` alternate links across multi-locale page clusters.
  - Excludes client-side redirect shells (`slide` root `index.html`).
- **`robots.txt`** (generated when `seo.robots` is `True`):
  - `User-agent: *\nAllow: /\n`, plus `Sitemap: <site_url>/sitemap.xml` when `sitemap` and `site_url` are active.
- **`llms.txt`** (generated when `seo.llms_txt` is `True`):
  - Follows `llmstxt.org` format (`# <Title>`, `> <Summary>`, categorized `## <Section>` link lists with extracted 1-sentence page/chapter/slide summaries, plus `## Locales` when 2+ locales are configured).

---

## 4. Implementation Steps

1. **Manifest & Shared SEO Engine**:
   - Update `src/drawlib/_builder/_common/manifest.py` (`SeoConfig`, `I18nConfig.descriptions`, `ProjectManifest.seo`, `format_project_manifest_toml`).
   - Create `src/drawlib/_builder/_common/seo.py` and export public helpers in `src/drawlib/_builder/_common/__init__.py`.
2. **Compilers & Templates**:
   - Integrate into `src/drawlib/_builder/doc_builder/exporter_html.py`, `src/drawlib/_builder/doc_builder/compiler/html.py`, `src/drawlib/_builder/doc_builder/compiler/base.py`, and `src/drawlib/_slide/compiler.py`.
   - Update `src/drawlib/_templates/project/site/template.html.template` and `src/drawlib/_templates/project/doc/template.html.template`.
3. **Unit & Security Tests**:
   - Add `tests/drawlib/doc_builder/test_seo.py` covering manifest validation, XSS/XML injection escaping, path traversal prevention on `og_image`, `site`/`doc`/`slide` OGP & canonical/hreflang output, `sitemap.xml`, `robots.txt`, `llms.txt`, and `scan_broken_links` compatibility.
4. **Dogfooding & Official Site (`www.drawlib.com`)**:
   - Sync `docs/ogp_images/social_preview.png` -> `docs/docs_src/_assets/ogp.png` (and update `docs/ogp_src/build_image.sh`).
   - Configure `[seo]` and `[i18n.descriptions]` in `docs/docs_src/drawlib.toml` and update `docs/docs_src/template.html`.
   - Document `[seo]` in `src/drawlib/_rules/` (`project_overview.md`, `project_site.md`, `project_doc.md`, `project_slide.md`) and `docs/docs_src/{en,ja}/09_doc_builder_and_cli/project_site.md` (with 100% EN/JA parity).
   - Run `./dcli code-check all`, `./dcli test target doc-builder`, `./dcli test target slide`, `./dcli test target cli`, `./dcli docs build site`, and `./dcli docs serve site --check`.

---

## Verification Plan

### Automated Security Check

- **Security Scanner**: Run a scan on all newly created files to identify common
  vulnerabilities (e.g., XSS, SQL injection). If findings are detected, auto-apply
  the fix and document the results.
- **Security Audit**: Audit the new code for design-level security issues (input
  validation, secrets handling, auth checks). Document findings and remediations
  in the `walkthrough.md` artifact using the `generate_security_audit_report`
  skill.
