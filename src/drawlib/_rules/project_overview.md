# Drawlib Project Architecture & Overview Guidelines

Drawlib provides a complete project scaffolding and multi-target build engine. It compiles Python drawing scripts and Markdown documents containing embedded ````drawlib```` blocks into publication-ready static HTML websites, linear vector PDFs, 16:9 presentation slide decks, GitHub-Flavored Markdown, and standalone image assets.

This document covers the **universal project architecture, template selection, shared configuration files (`styles.py`, `utils.py`), and caching system**. For deep authoring best practices on a specific project type, consult its dedicated rule guide:
- **Standalone Images (`images`)**: `uv run drawlib rules show project-images`
- **Linear Document & PDF (`doc`)**: `uv run drawlib rules show project-doc`
- **Multi-Page Website (`site`)**: `uv run drawlib rules show project-site`
- **16:9 Slide Deck (`slide`)**: `uv run drawlib rules show project-slide`
- **3-Stage Review & Self-Correction Loop**: `uv run drawlib rules show review-guide`

---

## 1. Project-First Rule (`drawlib init` — No Bare `.py` Files)

> **CRITICAL for AI Agents & Developers**: Never create standalone `.py` drawing scripts directly in an uninitialized directory, and never construct project folders from scratch manually.  
> Before writing any drawing code, check if a Drawlib project (`*_src/`) already exists in the workspace. If not, **always scaffold a project first using `drawlib init`** (or guide the user to choose one) so that `styles.py` (theme & language fonts), `utils.py`, `_assets/`, and `build.sh` are properly configured:
> - **Diagram image(s) only** -> Scaffold an **`images`** project (`uv run drawlib init images [-l <lang>] [-s <style>]`).
> - **Linear technical spec / whitepaper / PDF** -> Scaffold a **`doc`** project (`uv run drawlib init doc [-l <lang>] [-s <style>]`).
> - **Multi-page documentation website** -> Scaffold a **`site`** project (`uv run drawlib init site [-l <lang>] [-s <style>]`).
> - **16:9 presentation slide deck** -> Scaffold a **`slide`** project (`uv run drawlib init slide [-l <lang>] [-s <style>]`).
> - **Pass `--lang` for Non-English Labels**: When the user prompts in Japanese (or requires CJK/multilingual typography), pass `--lang ja` (or target language code) to `drawlib init` so `styles.py` automatically configures CJK-safe fonts.
> - **Clean Up Starter Samples**: After scaffolding, replace or delete the generated starter sample files (`sample1.py`, `sample2.py`, etc.) so only the user's requested diagrams are built.

### Scaffolding CLI Syntax & Options:
```bash
# List available starter templates:
uv run drawlib init list

# Scaffold a project in the current directory:
uv run drawlib init <images|doc|site|slide> [target] [-l <lang>] [-s <style>] [-f]

# Examples:
uv run drawlib init images --lang ja -s google
uv run drawlib init doc rbac -s google
uv run drawlib init site docs -s default
uv run drawlib init slide pitch -l ja -s google
```

| Option | Shorthand | Type | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `--style` | `-s` | `<theme>` | `default` | Style preset theme (`default`, `google`, `monochrome`) or custom CSS path. Synchronously configures both `style.css` and `styles.py`. |
| `--lang` | `-l` | `<lang>` | `en` | Starter template language code (`en`, `ja`, `zh-cn`, `ko`, `th`, `hi`, etc.). Configures regional font fallbacks in `styles.py`. |
| `--force` | `-f` | flag | `False` | Overwrite existing files if the destination directory is not empty. |

> **Pure Scaffolding Principle**: `drawlib init` only creates template and configuration files; it never runs compilation automatically. To compile your project, run `./<target>_src/build.sh` (or `./<target>_src/build_*.sh`).

---

## 2. Choosing Among the 4 Project Archetypes

Drawlib features 4 project starter templates tailored to distinct authoring and publishing workflows:

| Project Type | Source Folder | Generated Deliverables | When AI Agents Should Choose This | Dedicated Guide |
| :--- | :--- | :--- | :--- | :--- |
| **`images`** | `images_src/*.py` | `images/*.png` (or `.webp`) | User wants **diagram image(s) only** (architecture figures, README illustrations, standalone assets). | `project-images` |
| **`doc`** | `doc_src/*.md` | `doc_html/` (Web preview)<br>`doc.pdf` (A4 vector PDF)<br>`doc_markdown/` (GitHub MD)<br>`doc_images/` (Extracted PNGs) | User wants a **single linear technical document** (RFCs, design specs, whitepapers, quickstarts, printable PDF reports). | `project-doc` |
| **`site`** | `docs_src/**/*.md`<br>+ `navbar.md` | `docs_html/` (Multi-page site)<br>`docs_markdown/` (GitHub MD)<br>`docs_images/` (Extracted PNGs) | User wants a **multi-page documentation website** with a persistent navigation sidebar (portals, guides, wikis). | `project-site` |
| **`slide`** | `slide_src/*.md` | `slide_html/index.html` (Deck)<br>`slide.pdf` (16:9 vector PDF)<br>`slide_images/` (Extracted SVGs) | User wants a **16:9 widescreen presentation deck** with `1920×1080` stage blocks, speaker notes, and Presenter View. | `project-slide` |

```drawlib center fold-code file:project_archetypes_overview.png caption:"Drawlib's Four Project Archetypes & Compilation Deliverables"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=152, height=62, dpi=150)

rectangle((76, 31), width=146, height=56, style=Styles.MutedDashed.patch(shape_r=2.5))
text(
    (76, 53.5),
    "Four Drawlib Project Archetypes (drawlib init <type>)",
    style=Styles.DarkBold.patch(text_size=13.0),
)

cards = [
    (22.5, "images", "images_src/*.py", "• Batch Python scripts\n• Standalone PNG/WebP\n• Rule: project-images", Styles.Neutral, Styles.PrimaryBold, phosphor.image),
    (58.2, "doc", "doc_src/*.md", "• Linear chapters + ToC\n• A4 Vector PDF & HTML\n• Rule: project-doc", Styles.PrimaryNeutral, Styles.PrimaryBold, phosphor.file_pdf),
    (93.8, "site", "docs_src/**/*.md", "• Multi-page + navbar.md\n• Static Website & Search\n• Rule: project-site", Styles.PrimaryFlat, Styles.WhiteBold, phosphor.globe),
    (129.5, "slide", "slide_src/*.md", "• 1920x1080 ::: block\n• Web Deck & 16:9 PDF\n• Rule: project-slide", Styles.SecondaryNeutral, Styles.SecondaryBold, phosphor.presentation_chart),
]

for cx, title, sub, body, card_st, hdr_st, icon_fn in cards:
    rectangle((cx, 25.5), width=32.5, height=38, style=card_st.patch(shape_r=2.0))
    icon_fn((cx - 9.5, 38.5), width=4.8, style=hdr_st)
    text((cx + 2.5, 38.5), title, style=hdr_st.patch(text_size=12.0))
    sub_st = Styles.White.patch(text_size=9.8) if card_st == Styles.PrimaryFlat else Styles.Muted.patch(text_size=9.8)
    body_st = Styles.White.patch(text_size=9.8) if card_st == Styles.PrimaryFlat else Styles.Dark.patch(text_size=9.8)
    text((cx, 31.5), sub, style=sub_st)
    line((cx - 13, 28.2), (cx + 13, 28.2), style=Styles.White if card_st == Styles.PrimaryFlat else Styles.Muted)
    text((cx, 17.5), body, style=body_st)

save()
```

---

## 3. Shared Project Architecture (`styles.py`, `utils.py`, `_assets/`, `build.sh`)

Every scaffolded `<target>_src/` directory shares four foundational mechanisms:

### 3.1. Golden Rule: `<target>_src/` Is the Single Source of Truth
- **Author & Edit Strictly Inside `<target>_src/`**: All Markdown documents, Python scripts, stylesheets, and assets live inside `images_src/`, `doc_src/`, `docs_src/`, or `slide_src/`.
- **Never Manually Edit Output Directories**: Generated folders (`images/`, `doc_html/`, `docs_html/`, `docs_markdown/`, `slide_html/`, `*.pdf`) are overwritten on every build.
- **Overwrite Protection**: `drawlib build` strictly refuses to execute if the source and destination paths resolve to the same directory (`src_abs == dest_abs`).

### 3.2. Global Theme & Font Configuration (`styles.py`)
`styles.py` defines project-wide `Styles` and `Colors` overrides (including regional CJK font patching when initialized with `--lang`).
Inside any drawing script or embedded ````drawlib```` block, always import uppercase `Styles` and `Colors`:
```python
from drawlib.styles import Colors, Styles
```
Never import lowercase `styles` or `colors`, which shadows the module namespace.

### 3.3. Reusable Drawing Macros (`utils.py`)
`utils.py` holds project-specific helper functions, recurring diagram sub-components (e.g., `draw_service_card()`, `draw_page_number()`), and layout constants. Any top-level function or constant in `utils.py` can be imported via:
```python
from drawlib.utils import draw_service_card
```

### 3.4. Local Static Assets (`_assets/`)
Place static logos, custom `.ttf`/`.otf` font files, or reference screenshots inside `<target>_src/_assets/`.
- During HTML/Markdown/Slide builds, `_assets/` is automatically copied to the output directory.
- Inside drawing code, reference files as `"_assets/logo.png"` or `FontFile("_assets/brand.ttf")`—Drawlib automatically resolves paths relative to the document or project root and hashes them in `.drawlib/cache.db`.

### 3.5. Modular Build Scripts (`build_*.sh`)
Each project scaffolds focused shell scripts alongside the master `build.sh`:
- **`build_html.sh`**: Fast HTML compilation for rapid browser verification.
- **`build_pdf.sh`**: Headless Chromium print to vector PDF (`doc` and `slide`).
- **`build_markdown.sh`**: GitHub-Flavored Markdown compilation (`doc` and `site`).
- **`build_image.sh`**: Standalone diagram image compilation/extraction.
- **`build.sh`**: Master script that runs all target builds for the project sequentially.
- **`serve.sh`**: Local preview HTTP server (`drawlib serve`).

---

## 4. Build Cache (`.drawlib/cache.db`) & Asset Cache (`drawlib cache`)

### 4.1. SQLite Incremental Build Cache (`.drawlib/cache.db`)
- **Automatic Hashing**: Before executing any ````drawlib```` block or `.py` script, Drawlib computes a SHA-256 key over:
  1. The Python drawing code block.
  2. Global `styles.py` (`-s`) and `utils.py` (`-u`) contents.
  3. Local asset files referenced as string literals (e.g. `_assets/*`).
  4. Source/target file paths, image format (`png` / `webp` / `svg`), and slide count.
- **Auto-Ignore & Eviction**: Automatically creates `.drawlib/.gitignore` (`*`), invalidates on `drawlib`/`matplotlib` version upgrades, and evicts the oldest 50% of blobs when exceeding 1 GiB.
- **When to Bypass Cache (`--no-cache`)**: If your drawing code imports an external custom `.py` file outside `styles.py` and `utils.py`, pass `--no-cache` or clear the image cache:
  ```bash
  uv run drawlib build html docs_src/ -o docs_html/ --no-cache
  uv run drawlib cache clear --images
  ```

### 4.2. Font & Icon Release Asset Cache (`drawlib cache`)
Font families and icon packs (`icon-phosphor`, `icon-fontawesome`, `icon-gcp`) are downloaded on demand into `drawlib/_cached_assets/`:
```bash
uv run drawlib cache list              # Inspect cached packages and disk size
uv run drawlib cache download --all    # Pre-download all fonts & icons for offline/CI builds
uv run drawlib cache clear --all       # Purge all font, icon, and SQLite image caches
```

---

## 5. Dedicated Project Rule Guides

Query the specific project manual matching your target deliverable:
- **`uv run drawlib rules show project-images`**: Standalone `.py` illustration scripts (`images_src/`).
- **`uv run drawlib rules show project-doc`**: Linear technical documents, whitepapers & A4 vector PDFs (`doc_src/`).
- **`uv run drawlib rules show project-site`**: Multi-page documentation websites & `navbar.md` (`docs_src/`).
- **`uv run drawlib rules show project-slide`**: 16:9 widescreen presentation decks & `::: block` stage layouts (`slide_src/`).
- **`uv run drawlib rules show review-guide`**: 3-Stage Autonomous Multimodal Review & Self-Correction Loop.
