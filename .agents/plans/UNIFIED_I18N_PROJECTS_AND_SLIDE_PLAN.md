# Unified i18n-Native Project Architecture (`doc`, `site`, `slide`) Implementation Plan

## 1. Objective & Core Design Decisions

Unify all Markdown-based project archetypes (`doc`, `site`, `slide`) onto the **`i18n`-native `<src_dir>/<lang>/` architecture** ($N \ge 1$ locales), eliminating the legacy flat single-language directory layout and dual compiler code paths:

1. **Unified Locale Layout (`doc`, `site`, `slide`)**:
   - Every `doc`, `site`, and `slide` project places its Markdown sources under `<src_dir>/<lang>/` (even for single-language projects such as `-l en` -> `<src_dir>/en/` or `-l ja` -> `<src_dir>/ja/`).
   - Adding a second language later requires zero file moves (`git mv`) or script changes: simply add `<src_dir>/<new_lang>/` and append `"<new_lang>"` to `langs` in `drawlib.toml`.
   - `images` remains a flat standalone Python script archetype (`images_src/*.py`) with `lang` under `[project]`.
2. **Unified `drawlib.toml` Schema**:
   - For `doc`, `site`, and `slide`: `[i18n]` (`default_lang`, `langs` with `len(langs) >= 1`, and optional `[i18n.labels]`) is **required**, and `lang` under `[project]` is disallowed (preventing duplicate/conflicting language definitions).
   - For `images`: `[project]` includes `lang = "en"` (default) and `[i18n]` is disallowed.
3. **Consistent Locale-Suffixed Document/Deck Deliverables (`Option A`)**:
   - Even when `len(langs) == 1` (e.g., `langs = ["en"]`), compiled file deliverables always use `<base>_<lang>.<ext>`:
     - `doc`: `<base>_<lang>.pdf`, `<base>_<lang>.docx`, `<base>_html/<lang>/index.html` (+ root `<base>_html/index.html`), `<base>_markdown/<lang>/...`
     - `site`: `<base>_html/<lang>/...` (+ root `<base>_html/index.html`), `<base>_markdown/<lang>/...` (+ root `<base>_markdown/index.md`)
     - `slide`: `<base>_<lang>.pdf`, `<base>_<lang>.pptx`, `<base>_html/<lang>/index.html` (+ root `<base>_html/index.html` redirect preserving `?presenter=1` and `#N`)
   - Language switcher UI is automatically hidden when `len(langs) == 1` and automatically displayed when `len(langs) >= 2` (and hidden in `@media print`).
4. **Clean Removal of Legacy Flat Directory Builders**:
   - Remove legacy flat-directory compilation branches from `doc_builder` (`html.py`, `markdown.py`, `pdf.py`, `docx.py`), `image_builder.py`, and `_slide` (`compiler.py`, `compiler_pptx.py`). Directory builds for `doc`, `site`, and `slide` strictly require `drawlib.toml` with `[i18n]`.
   - Preserve standalone single-file `build_pdf("file.md")` / `build_docx("file.md")` / `build_image("file.py" | "file.md")` workflows.

---

## 2. Phase Breakdown

### Phase 1: Manifest Schema, `i18nslide` Engine & Compiler Unification
1. **`src/drawlib/_builder/_common/manifest.py`**:
   - Update `ProjectMetadata.lang` (`str | None = None`): allowed on `images` (default `"en"`), rejected on `doc` / `site` / `slide`.
   - Extend `I18nConfig` with `labels: dict[str, str] = Field(default_factory=dict)` for `[i18n.labels]`.
   - Require `[i18n]` (`len(langs) >= 1`) when `project.type in {"doc", "site", "slide"}`; reject `[i18n]` when `project.type == "images"`.
   - Update `format_project_manifest_toml()` accordingly.
2. **`src/drawlib/_builder/doc_builder/i18n.py`**:
   - Support `project_type: Literal["site", "doc", "slide"]` in `validate_i18n_project()`:
     - For `"slide"`: forbid `navbar.md`, require `>= 1` slide `.md` per locale, strip `::: note ... :::` via `extract_slide_notes()` before `extract_markdown_skeleton()`, and pass `require_file=False` when checking shared `drawlib` code blocks.
   - Honor `config.labels.get(lang_key)` in `build_language_switcher_context()`.
3. **`src/drawlib/_slide/` (`compiler.py`, `compiler_pptx.py`, `_assets.py`) & Slide Assets (`slide.js`, `slide.css`)**:
   - Refactor `build_slide()` to compile `<src_dir>/<lang>/...` for all `lang in manifest.i18n.langs`:
     - Default `output_dir` to `<parent>/<base>_html`.
     - Shared `<out_dir>/images/<slide_stem>/...` (deduplicating identical diagrams across locales via `BuildCacheManager`), shared `<out_dir>/_assets/`, and shared `<out_dir>/slide.js` (preferring local `<src_dir>/slide.js` if present, else `get_slide_js()`).
     - Per-locale `<lang>/styles.py` & `<lang>/utils.py` overrides falling back to root `<src_dir>/styles.py` & `<src_dir>/utils.py`.
     - Per-locale `<out_dir>/<lang>/style.css` (localized via `localize_css_for_language` + `bundle_svg_fonts`) and `<out_dir>/<lang>/index.html` (`<html lang="..." dir="...">`, `font_link_html`, `../slide.js`, `../images/...`, `../_assets/...`).
     - Multi-locale switcher dropdown in `.slide-controls` (when `len(langs) > 1`), updating `slide.js` so switching locales preserves the current `#N` slide hash, and hiding `.slide-controls` in `@media print`.
     - Root `<out_dir>/index.html` redirector forwarding to `<default_lang>/index.html` while preserving `window.location.search + window.location.hash`.
   - Refactor `build_pptx()` (`compiler_pptx.py`) and `build_pdf()` slide branch (`doc_builder/compiler/pdf.py`) to emit `<base>_<lang>.pptx` and `<base>_<lang>.pdf` for every locale in `manifest.i18n.langs`.
4. **Remove Legacy Flat Directory Paths in `doc_builder` & `image_builder`**:
   - `compiler/html.py`: Require `manifest` (`doc` or `site`) on directories; delete legacy flat-directory compilation functions.
   - `compiler/markdown.py`: Require `manifest` (`doc` or `site`); delete legacy flat-directory walk.
   - `compiler/pdf.py` & `compiler/docx.py`: Delete heuristic slide sniffing and flat directory compilation; dispatch strictly via `manifest.project.type` (`doc` / `slide`).
   - `image_builder.py` & `_image_ast.py`: Support `project.type == "slide"` (with `SlideContext(idx, total)` and default `.svg` for unnamed slide blocks), resolve ancestor `drawlib.toml` for single `.md` files inside `<lang>/...`, prune `.` / `_` directories, and reject manifest-less `.md` directories.
   - `_cli/commands/build.py`: Format multi-locale output summaries across `pdf`, `docx`, and `pptx`.

### Phase 2: Scaffolding Templates (`drawlib init`)
1. **`src/drawlib/_templates/_project.py` & `_cli/commands/init.py`**:
   - Allow `-l en,ja` on `doc`, `site`, and `slide` (reject multi-lang only on `images`).
   - Always scaffold `<src_dir>/<lang>/...` and `[i18n]` in `drawlib.toml` for `doc`, `site`, and `slide` (using `docs/<lang>/` when `len(langs) == 1` so `-l ja` keeps localized Japanese sample diagrams, and `docs_i18n/<lang>/` when `len(langs) > 1` for out-of-the-box parity).
2. **Template Files (`src/drawlib/_templates/project/{doc,site,slide}/`)**:
   - Add `slide/docs_i18n/ja/` matching `slide/docs/en/` skeleton and shared diagram filenames.
   - Update `slide/docs/{en,ja}/01_title.md` asset path `_assets/linux.png` -> `../_assets/linux.png` (and verify `doc` / `site` starter templates).
   - Use Jinja `{{ html_lang | default('en') }}`, `{{ html_dir | default('ltr') }}`, and `{{ font_link_html | default('') | safe }}` directly in `doc/template.html.template` and `site/template.html.template`.
   - Update `build_pdf.sh.template`, `build.sh.template`, `serve.sh.template`, and `README.md` across `doc`, `site`, and `slide` for `<base>_<lang>.pdf` and `<src_dir>/<lang>/`.

### Phase 3: Unit/Integration Tests & Repository Dogfooding Migration (`docs/` + `dcli`)
1. **Migrate Remaining Single-Locale Projects in `docs/`**:
   - `docs/quickstart_src/`: Move `00-cover.md`..`15-best_practices.md` -> `en/` (updating any `_assets/` relative refs if present), update `drawlib.toml` to `[i18n] default_lang = "en", langs = ["en"]`, update `template.html` & `build_pdf.sh` (`docs/quickstart_en.pdf`), remove stale `docs/quickstart.pdf`.
   - `docs/architecture_src/`: Move `index.md`, `navbar.md`, `01_overview/`..`07_test_architecture/` -> `en/`, update `drawlib.toml` & `template.html`.
   - `docs/slide_about_drawlib_src/`: Move `00_opening/`..`07_ai_agent_workflow/` -> `en/`, update `drawlib.toml`, `slide.js`, `style.css`, `build_pdf.sh` (`docs/slide_about_drawlib_en.pdf`), remove stale `docs/slide_about_drawlib.pdf`.
   - `docs/slide_ddos_incident_response_src/`: Move `00_opening/`..`05_closing/` -> `en/` (fixing any `_assets/` refs in `.md` prose to `../_assets/`), update `drawlib.toml`, `slide.js`, `style.css`, `build_pdf.sh` (`docs/slide_ddos_incident_response_en.pdf`), remove stale `docs/slide_ddos_incident_response.pdf`.
   - Update `tools/dcli/docs/builder.py`, `README.md`, `docs/README_PYPI.md` for `*_en.pdf` paths.
2. **Update All 12 Affected Test Modules in `tests/`**:
   - `tests/drawlib/doc_builder/` (`test_auto_styles_and_exclusions.py`, `test_build_cache.py`, `test_compiler.py`, `test_css.py`, `test_doc_i18n.py`, `test_docx.py`, `test_site_i18n.py`)
   - `tests/drawlib/cli/` (`test_cli_build.py`, `test_cli_css.py`, `test_cli_init.py`)
   - `tests/drawlib/slide/` (`test_slide.py`, `test_pptx.py` — including new multi-locale `en,ja` HTML, PDF, and PPTX tests!)

### Phase 4: Agent Rules, Documentation, Full Verification & Stage 3 Visual Review
1. Update `src/drawlib/_rules/` (`project_overview.md`, `project_doc.md`, `project_site.md`, `project_slide.md`, `cli.md`), `.agents/rules/docs.md`, and `docs/docs_src/{en,ja}/09_doc_builder_and_cli/{project_overview,project_doc,project_site,project_slide}.md`.
2. Run `./dcli code-check all`, `./dcli test all --no-cov`, `./dcli docs build --all`, and `./dcli docs serve <target> --check` across all HTML targets.
3. Perform Stage 3 multimodal inspection (`view_file`) on compiled slides, multi-locale slide language switcher, and generated `*_en.pdf` deliverables.
