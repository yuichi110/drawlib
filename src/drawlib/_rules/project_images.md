# Drawlib Standalone Images Project Guidelines (`project-images`)

An **`images` project** (`drawlib init images`) is designed for authoring standalone Python illustration scripts (`images_src/*.py`) and compiling them in batch mode into raster or vector image files (`images/*.png`, `.webp`, `.svg`, `.pdf`).

*(For general project scaffolding and cache architecture, see `uv run drawlib rules show project-overview`. For the 3-stage visual verification loop, see `uv run drawlib rules show review-guide`.)*

---

## 1. When to Choose an `images` Project

Choose `drawlib init images` whenever the user wants **diagram image file(s) only** rather than a Markdown document, website, or slide deck:
- Standalone architecture diagrams for README files, pull requests, or external wikis.
- Batch generation of technical figures, charts, or visual catalogs from data scripts.
- Even when the user asks for a **single diagram image**, never create a bare `.py` file in an uninitialized folder—always scaffold `images_src/` first so `styles.py` (theme & CJK fonts), `utils.py`, `_assets/`, and `build.sh` are properly configured.

### Scaffolding & Initial Cleanup:
```bash
# 1. Scaffold an images project (pass --lang ja if Japanese/CJK labels are needed):
uv run drawlib init images [target] [-l <lang>] [-s <default|google|monochrome>]

# 2. Remove the generated starter samples so only the user's diagrams are built:
rm -f images_src/sample1.py images_src/sample2.py
```

---

## 2. Directory Structure & Compilation Pipeline

```text
.
├── images_src/                # [SOURCE OF TRUTH] Author Python scripts (*.py) here!
│   ├── _assets/               # Static logos, icons, or custom .ttf fonts
│   ├── styles.py              # Project-wide Styles & Colors (auto-loaded via -s)
│   ├── utils.py               # Shared helper functions & macros (auto-loaded via -u)
│   ├── build.sh               # Master build script (runs build_image.sh)
│   ├── build_image.sh         # Batch image compiler (images_src/ -> images/)
│   ├── README.md              # Project workflow instructions
│   ├── system_topology.py     # -> compiles to images/system_topology.png
│   └── network/               # Nested subdirectories are mirrored automatically
│       └── vpc_peering.py     # -> compiles to images/network/vpc_peering.png
└── images/                    # [GENERATED] Rendered output images (never edit manually)
    ├── system_topology.png
    └── network/
        └── vpc_peering.png
```

```drawlib center fold-code file:project_images_pipeline.png caption:"Standalone Images Project Architecture & Grid Review Loop"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=148, height=56, dpi=150)

rectangle((74, 28), width=142, height=50, style=Styles.MutedDashed.patch(shape_r=2.5))
text(
    (74, 48.5),
    "Standalone Images Workflow (images_src/*.py -> images/*.png)",
    style=Styles.DarkBold.patch(text_size=12.5),
)

# 1. Source Scripts & Shared Config
rectangle((26, 24), width=38, height=34, style=Styles.PrimaryNeutral.patch(shape_r=2.0))
phosphor.file_py((12, 35.5), width=5.0, style=Styles.PrimaryBold)
text((28, 35.5), "1. images_src/", style=Styles.PrimaryBold.patch(text_size=11.5))
text(
    (26, 20),
    "• *.py drawing scripts\n• styles.py (Fonts/Theme)\n• utils.py (Shared Macros)\n• _assets/ (Logos/TTF)",
    style=Styles.Dark.patch(text_size=10.0),
)

line((45.5, 24), (54.5, 24), arrow_head="->", style=Styles.DarkBold)

# 2. Fast Grid Review (-g)
rectangle((74, 24), width=38, height=34, style=Styles.SecondaryNeutral.patch(shape_r=2.0))
phosphor.grid_four((60, 35.5), width=5.0, style=Styles.SecondaryBold)
text((76, 35.5), "2. Grid Check (-g)", style=Styles.SecondaryBold.patch(text_size=11.5))
text(
    (74, 20),
    "• drawlib show <script.py>\n  -g -o .drawlib/scratch/\n• Inspect via view_file\n• 1-shot coord adjustment",
    style=Styles.Dark.patch(text_size=10.0),
)

line((93.5, 24), (102.5, 24), arrow_head="->", style=Styles.DarkBold)

# 3. Batch Build & AST Check
rectangle((122, 24), width=38, height=34, style=Styles.PrimaryFlat.patch(shape_r=2.0))
phosphor.images((108, 35.5), width=5.0, style=Styles.WhiteBold)
text((124, 35.5), "3. ./build.sh", style=Styles.WhiteBold.patch(text_size=11.5))
text(
    (122, 20),
    "• AST collision check\n• SQLite hash caching\n• Mirrors subdir tree\n• Outputs images/*.png",
    style=Styles.White.patch(text_size=10.0),
)

save()
```

---

## 3. Authoring Best Practices for `images_src/*.py`

### 3.1. Single-Image vs. Multi-Image Scripts (`save()` and `clear()`)
- **Single-Image Script (Recommended)**:
  When a script calls `save()` without a filename, `drawlib build image` automatically names the output image after the script stem (e.g., `images_src/architecture.py` -> `images/architecture.png`):
  ```python
  from drawlib.canvas import save, setup
  from drawlib.shapes import rectangle
  from drawlib.styles import Styles

  setup(width=140, height=70, dpi=150)
  rectangle((70, 35), width=40, height=20, style=Styles.PrimaryFlat, text="API Gateway", text_style=Styles.WhiteBold)
  save()
  ```
- **Multi-Image Batch Script (`clear()` Mandatory)**:
  If a single `.py` script generates multiple output files (`save("step1.png")`, `save("step2.png")`), **always call `clear()` between drawings** so shapes from the first canvas do not bleed into the second:
  ```python
  from drawlib.canvas import clear, save, setup
  from drawlib.shapes import rectangle
  from drawlib.styles import Styles

  setup(width=120, height=50)
  rectangle((35, 25), width=34, height=18, style=Styles.PrimaryFlat, text="Stage 1", text_style=Styles.WhiteBold)
  save("stage_1.png")

  clear()  # Reset canvas state before Stage 2!
  setup(width=120, height=50)
  rectangle((35, 25), width=34, height=18, style=Styles.Neutral, text="Stage 1")
  rectangle((85, 25), width=34, height=18, style=Styles.PrimaryFlat, text="Stage 2", text_style=Styles.WhiteBold)
  save("stage_2.png")
  ```

### 3.2. Pre-Execution AST Duplicate Output Detection
Before running any script in `images_src/`, `drawlib build image` parses all `.py` files via Python's `ast` module (ignoring `styles.py` and `utils.py`) to determine every target output filename.
- If two scripts would overwrite the same output path (e.g. `a.py` calls `save("out.png")` and `b.py` also calls `save("out.png")` in the same folder), the build **aborts immediately before executing any code**.
- Keep filenames unique or rely on bare `save()` so each `<name>.py` maps 1-to-1 to `<name>.png`.

### 3.3. Sharing Themes (`styles.py`) & Component Macros (`utils.py`)
Never duplicate boilerplate helper functions or hardcoded colors across multiple `.py` scripts:
1. **`styles.py`**: Customize palettes or fonts once in `images_src/styles.py` and import `from drawlib.styles import Colors, Styles` in every script.
2. **`utils.py`**: Define recurring node cards, legends, or header banners in `images_src/utils.py` and import `from drawlib.utils import <helper>` in your scripts.

### 3.4. Typography, Aspect Ratios & Neutral Balance
- **Typography (`text_size >= 10.0`)**: Keep body labels at `text_size = 10.5`–`12.0` and diagram titles at `12.5`–`15.0` so exported PNGs remain legible when embedded in external docs or slides.
- **50%+ Neutral Baseline**: Ground at least 50% of nodes in calm neutral cards (`Styles.Neutral`, `Styles.PrimaryNeutral`, `Styles.SecondaryNeutral`) and reserve `Styles.PrimaryFlat` / `Styles.AccentFlat` for 1–2 focal nodes.
- **Anchor Awareness**: Remember that `shapes.*`, `text.text()`, and `icons.*` use **Center `(cx, cy)`** anchors, whereas `smartarts.*`, `charts.*`, `diagrams.*`, and `graph.*` use **Bottom-Left `(x0, y0)`** anchors (`x0 = (W - width) / 2` to center horizontally).

### 3.5. Relative Asset Paths (No Absolute Paths or file:// URLs)
When loading external logos, icons, or custom fonts in illustration scripts:
- Store static assets under `images_src/_assets/` (e.g. `images_src/_assets/logo.png`).
- Reference them using relative paths (e.g. `image=image("_assets/logo.png")` or `Dimage("_assets/logo.png")`).
- Never hardcode machine-specific absolute paths (`/usr/...`, `/home/...`, `C:\...`) or `file://` URLs, which break portability across developer machines and automated build environments.

---

## 4. Verification & Build Workflow for `images` Projects

Never run `./images_src/build.sh` blindly without inspecting your diagrams with the coordinate grid:

1. **Step 1 — Rapid Single-Script Grid Preview (`-g`)**:
   ```bash
   uv run drawlib show images_src/system_topology.py \
       -s images_src/styles.py -u images_src/utils.py \
       -g -o .drawlib/scratch/preview.png
   ```
2. **Step 2 — Multimodal Self-Review (`view_file`)**:
   Inspect `.drawlib/scratch/preview.png` via `view_file`. Verify:
   - Zero overlapping labels or clipped text borders.
   - Clean `4–6` unit margins on all four canvas edges (`x=0`, `x=W`, `y=0`, `y=H`).
   - Proper `Center` vs. `Bottom-Left` component centering and `50%+` neutral color balance.
3. **Step 3 — Batch Compilation & Final Inspection**:
   ```bash
   ./images_src/build.sh
   rm -rf .drawlib/scratch/*
   ```
   Inspect the final grid-free output in `images/*.png` via `view_file` before delivering to the user.
