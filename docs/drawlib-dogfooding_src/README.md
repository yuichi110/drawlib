# Drawlib Dogfooding Whitepaper (`doc` Multi-Language Project)

This directory contains the bilingual (English & Japanese) Drawlib Dogfooding Whitepaper compiled into **HTML, A4 vector PDFs (`_en.pdf` / `_ja.pdf`), Markdown, and standalone images** (plus optional editable **MS Word `.docx`** export).

---

## 1. Directory Structure

- `drawlib-dogfooding_src/`: Source Markdown chapters and drawing code (**Source of Truth**).
  - `drawlib.toml`: Unified project manifest (`type = "doc"`, `style = "google"`, `[i18n]` `default_lang = "en"`, `langs = ["en", "ja"]`).
  - `en/`: English whitepaper chapters (`00_cover.md` .. `12_slide_presentation.md`).
  - `ja/`: Japanese whitepaper chapters (`00_cover.md` .. `12_slide_presentation.md`) and `ja/styles.py` (`FontJapanese` override).
  - `_assets/`: Shared image assets (`favicon.png`, `linux.png`) across all locales.
  - `styles.py`: Default drawing theme (`GoogleStyles` / `GoogleColors`).
  - `utils.py`: Shared drawing helper functions (`service_card`, `connect`).
  - `style.css`: Google Editorial document & A4 print stylesheet.
  - `template.html`: Jinja2 HTML layout with top-right language switcher (hidden in print/PDF).
  - `build.sh`, `build_html.sh`, `build_pdf.sh`, `build_markdown.sh`, `build_image.sh`, `serve.sh`: Build and preview scripts.
- `drawlib-dogfooding_html/`: Generated bilingual HTML whitepaper (`index.html`, `en/index.html`, `ja/index.html`).
- `drawlib-dogfooding_en.pdf` & `drawlib-dogfooding_ja.pdf`: Generated English & Japanese A4 vector PDFs.
- `drawlib-dogfooding_markdown/`: Generated Markdown chapters (`en/`, `ja/`, `images/`).
- `drawlib-dogfooding_images/`: Extracted standalone diagram images.

---

## 2. Building & Previewing

```bash
# Build via repository CLI
./dcli docs build dogfooding
./dcli docs serve dogfooding --check

# Or build individual formats via drawlib CLI
uv run drawlib build html docs/drawlib-dogfooding_src/ -o docs/drawlib-dogfooding_html/
uv run drawlib build pdf docs/drawlib-dogfooding_src/ -o docs/drawlib-dogfooding.pdf --generate-index
uv run drawlib build markdown docs/drawlib-dogfooding_src/ -o docs/drawlib-dogfooding_markdown/
uv run drawlib build image docs/drawlib-dogfooding_src/ -o docs/drawlib-dogfooding_images/
uv run drawlib build docx docs/drawlib-dogfooding_src/ -o docs/drawlib-dogfooding.docx --generate-index
```
