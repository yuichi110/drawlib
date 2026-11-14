# About Drawlib — Official Bilingual 16:9 Showcase Deck (`slide`)

This directory contains bilingual (`en` / `ja`) slide Markdown files and embedded Drawlib Python diagrams compiled into an interactive HTML presentation deck (with Presenter View and live locale switching), print-ready vector PDFs, and editable 16:9 MS PowerPoint (`.pptx`) decks.

---

## 1. Directory Structure

- `drawlib.toml`: Unified project manifest (`type = "slide"`, `style = "default"`, `[i18n]` `default_lang = "en"`, `langs = ["en", "ja"]`).
- `en/` & `ja/`: Symmetric 39-slide English and Japanese chapters (`00_opening/` ... `07_closing/`).
- `_assets/`: Static image assets shared across locales.
- `styles.py`: Global styles script (`DefaultStyles` / `DefaultColors`).
- `utils.py`: Slide-calibrated macro helpers (`draw_page_number`, `draw_chapter_divider`, `draw_curved_agenda`, `draw_kpi_cards`).
- `style.css` / `slide.js`: Presentation styling and runtime interactivity.
- `build.sh`, `build_html.sh`, `build_pdf.sh`, `build_pptx.sh`, `serve.sh`: Build and preview scripts (outputs to `docs/about-drawlib/`).

---

## 2. Building & Previewing

```bash
./dcli docs build about-drawlib   # Build HTML slides, PDF, PPTX, and preview.png into docs/about-drawlib/
./dcli docs serve about-drawlib   # Start local preview server at http://localhost:8000
```
