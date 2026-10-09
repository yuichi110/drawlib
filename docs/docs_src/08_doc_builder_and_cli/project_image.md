# Images Project Guide (`drawlib init images`)

The `images` starter template (CLI alias: `image`) is designed for generating standalone illustration assets, presentation diagrams, article hero banners, and social preview cards directly from batch Python scripts.

---

## 1. Project Initialization

Scaffold a new images project using `drawlib init`:

```bash
# Scaffold standard images project in current directory (creates 'images_src/'):
drawlib init images

# Or with custom target name, theme, and language (creates 'my_assets_src/'):
drawlib init images my_assets -s google -l en
```

---

## 2. Directory Layout & Anatomy

```drawlib fold-code 600px center file:project_image_directory_tree.png caption:"Directory Structure of a Standalone Batch Image (images) Project"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.smartarts import TreeNode
from drawlib.styles import Styles

setup(width=100, height=62)

TreeNode.register_drawing_item(
    name="folder",
    location="before",
    padding_width=3.8,
    function=phosphor.folder,
    style=Styles.PrimaryFlat,
    args={"width": 2.8},
)
TreeNode.register_drawing_item(
    name="folder_out",
    location="before",
    padding_width=3.8,
    function=phosphor.folder,
    style=Styles.Secondary,
    args={"width": 2.8},
)
TreeNode.register_drawing_item(
    name="py",
    location="before",
    padding_width=3.8,
    function=phosphor.file_py,
    style=Styles.PrimaryBold,
    args={"width": 2.8},
)
TreeNode.register_drawing_item(
    name="code",
    location="before",
    padding_width=3.8,
    function=phosphor.file_code,
    style=Styles.Dark,
    args={"width": 2.8},
)
TreeNode.register_drawing_item(
    name="img",
    location="before",
    padding_width=3.8,
    function=phosphor.file_text,
    style=Styles.Dark,
    args={"width": 2.8},
)

root = TreeNode(
    "my_assets/",
    text_style=Styles.DarkBold.patch(text_size=9.5),
    line_style=Styles.DarkThin,
    line_horizontal_margin=3.2,
    line_horizontal_length=3.2,
    line_vertical_margin=5.5,
).set_drawing_item("folder")

src = root.add(
    "images_src/  — [SOURCE OF TRUTH] Edit Python drawing scripts here",
    text_style=Styles.DarkBold.patch(text_size=9.0),
).set_drawing_item("folder")
src.add(
    "_assets/  — Static assets (logos, background textures)",
    text_style=Styles.Dark.patch(text_size=8.5),
).set_drawing_item("folder")
src.add(
    "sample1.py & sample2.py  — Starter Python drawing scripts",
    text_style=Styles.Dark.patch(text_size=8.5),
).set_drawing_item("py")
src.add(
    "styles.py & utils.py  — Shared styling themes & reusable components",
    text_style=Styles.Dark.patch(text_size=8.5),
).set_drawing_item("py")
src.add(
    "build.sh, build_image.sh, README.md  — Batch build scripts",
    text_style=Styles.Dark.patch(text_size=8.5),
).set_drawing_item("code")

out = root.add(
    "images/  — [GENERATED] Rendered PNG/WebP output images",
    text_style=Styles.DarkBold.patch(text_size=8.8),
).set_drawing_item("folder_out")
out.add(
    "sample1.png & sample2.png  — Compiled image artifacts",
    text_style=Styles.Dark.patch(text_size=8.5),
).set_drawing_item("img")

root.draw(xy=(8, 54))
save()
```

### Key Rules:
- **Source of Truth**: Always author drawing scripts in `images_src/`. After scaffolding, replace or remove the starter `sample1.py` and `sample2.py` files so only your desired diagrams are built.
- **Never Edit `images/`**: The `images/` folder is an output artifact directory overwritten during builds.

---

## 3. Writing Drawing Scripts

In an `images` project, each `.py` file inside `images_src/` is an independent drawing script. Call `save()` at the end of the script to output the image:

```drawlib show-code 600px center file:project_image_architecture_overview.png caption:"Rendered Output of images_src/architecture_overview.py"
# images_src/architecture_overview.py
from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles

setup(width=100, height=50)

# Draw components (50%+ neutral baseline + 1 primary focal point)
rectangle((28, 25), width=32, height=22, style=Styles.Neutral, text="Client")
rectangle(
    (72, 25),
    width=32,
    height=22,
    style=Styles.PrimaryFlat,
    text="Server",
    text_style=Styles.WhiteBold,
)
line((44, 25), (56, 25), arrow_head="->", style=Styles.DarkBold)

# Save image (defaults to <script_stem>.png or save("architecture_overview.png") in scripts)
save()
```

### How `save()` Interacts with `drawlib build image -o images/`:
- **Automatic Output Redirection**: When executed via `drawlib build image images_src/ -o images/`, relative paths passed to `save("architecture_overview.png")` (or `save()` with no filename, which defaults to `<script_stem>.png`) are automatically written inside the `-o images/` directory, preserving any nested subdirectory hierarchy under `images_src/`.
- **Pre-Execution AST Duplicate Collision Check**: Before running any scripts in a batch, Drawlib parses the Python AST of all target `.py` files to inspect their `save(...)` targets. If two scripts would write to the exact same output file path, the build aborts immediately before modifying disk state.

---

## 4. Building Images

### Automated Build (`./build_image.sh` or `./build.sh`)
Execute the provided build script:

```bash
./images_src/build.sh
```

### Direct CLI Command
Alternatively, invoke the builder directly:

```bash
drawlib build image images_src/ -o images/ -s images_src/styles.py -u images_src/utils.py
```

### Useful Build Flags:
- `--grid` (`-g`): Automatically generates companion `*_grid.png` images overlaid with coordinate grid lines for visual debugging.
- `-f webp`: Overrides output format across all scripts to modern WebP.
- `--no-cache`: Forces a clean re-render of all images, bypassing the SQLite hash cache (`.drawlib/cache.db`).
