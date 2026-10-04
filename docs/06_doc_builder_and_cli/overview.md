# Documentation as Code: The Drawlib Build Engine

Drawlib unifies technical documentation and architectural illustrations under a single **"Documentation as Code"** pipeline. Instead of managing out-of-sync vector files, manually exporting diagrams from third-party tools, or checking in opaque binary assets, you author declarative Python drawing blocks directly inside standard Markdown documents.

---

## 1. Core Principles

```text
Markdown Source (docs_src/)                  Drawlib Compilation Pipeline                Publishing Targets
┌───────────────────────────┐                 ┌───────────────────────────┐               ┌───────────────────────────┐
│ # Architecture Guide      │                 │  Markdown Parser          │               │ docs_html/ (Static Site)  │
│                           │                 │          │                │               │                           │
│ ```drawlib 600px center   │ ──────────────► │  Python Execution Sandbox │ ────────────► │ docs/ (GitHub Markdown)   │
│ from drawlib.shapes...    │                 │          │                │               │                           │
│ ```                       │                 │  SQLite Image Cache       │               │ docs.pdf (Vector Report)  │
└───────────────────────────┘                 └───────────────────────────┘               └───────────────────────────┘
```

1. **Source of Truth (`<name>_src/`)**: You author content exclusively in source directories (e.g. `docs_src/` or `images_src/`). Output folders (`docs/`, `docs_html/`, `images/`) are build artifacts and should never be manually modified.
2. **Deterministic Build Cache**: Drawlib computes a SHA-256 hash of each embedded code block. Unaltered diagrams are restored instantly from `.drawlib/cache.db`, enabling sub-second incremental builds across massive multi-page sites.
3. **Execution Sandbox & Isolation**: The canvas lifecycle automatically clears between separate code blocks, ensuring zero visual side effects between adjacent diagrams.
4. **Target Portability**: The same Markdown source document can compile simultaneously to:
   - A responsive static HTML documentation site (`drawlib build html`).
   - GitHub-flavored Markdown with companion images (`drawlib build markdown`).
   - A publication-grade vector PDF with table of contents and cover page (`drawlib build pdf`).

---

## 2. Project Starter Templates

Never construct documentation directories manually. Scaffolding them with `drawlib init` guarantees the correct directory layout and configuration scripts:

| Template | Primary Output | Typical Use Case |
|---|---|---|
| **`doc`** | `doc.html`, `doc.pdf`, `doc.md`, `images/` | Linear technical documents, RFCs, specifications, whitepapers, and formal reports. |
| **`site`** | `docs_html/` & `docs/` | Multi-page documentation websites with sidebar navigation (`navbar.md`). |
| **`slide`** | `slide/index.html` & `slide.pdf` | 16:9 presentation slide decks (interactive web deck + printable vector PDF). |
| **`image`** | `images/*.png` | Batch rendering standalone Python drawing scripts to image assets. |

---

## 3. Chapter Structure

Dive deeper into each builder subsystem:
- [Embedded Code Blocks](./code_blocks.md): Code fence syntax, display modes (`show-code`, `fold-code`), alignment, and captions.
- [CLI Reference](./cli_reference.md): Complete guide to `build`, `serve`, `show`, `init`, `cache`, `css`, `colors`, `styles`, and `rules`.
- [Linear Document Project Guide](./project_doc.md): Linear document RFCs, specifications, whitepapers, and dual HTML/PDF publishing.
- [Doc Site Project Guide](./project_site.md): Multi-page website authoring, sidebar categories, and link validation.
- [Slide Deck Project Guide](./project_slide.md): 16:9 presentation slide decks with interactive web deck and vector PDF export.
- [Image Project Guide](./project_image.md): Standalone script automation (`images_src/` ➔ `images/`).
- [Customization & Theming](./customization.md): Customizing `template.html`, `style.css`, and injecting project `styles.py` and `utils.py`.
