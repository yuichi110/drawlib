# Image Project Guide (`drawlib init image`)

The `image` starter template is designed for generating standalone illustration assets, presentation slides, article hero banners, and social preview cards directly from batch Python scripts.

---

## 1. Project Initialization

Scaffold a new image project using `drawlib init`:

```bash
# Create in a new subdirectory:
drawlib init image my_assets/

# Or scaffold directly in current working directory:
drawlib init image --here
```

---

## 2. Directory Layout & Anatomy

```text
my_assets/
├── image_src/                 # [SOURCE OF TRUTH] Edit Python drawing scripts here
│   ├── _assets/               # Static assets (logos, background textures)
│   ├── sample1.py             # Primitive drawing script
│   ├── sample2.py             # Advanced diagram script (utilizing styles & utils)
│   ├── styles.py              # Shared project styling themes
│   ├── utils.py               # Reusable project drawing components
│   ├── build.sh               # Executable batch build script
│   ├── build_image.sh         # Batch image rendering script (image_images/)
│   └── README.md              # Illustration workflow guide
└── image_images/              # [GENERATED] Rendered PNG/WebP output images
    ├── sample1.png
    └── sample2.png
```

### Key Rules:
- **Source of Truth**: Always author drawing scripts in `image_src/`.
- **Never Edit `image_images/`**: The `image_images/` folder is an output artifact directory overwritten during builds.

---

## 3. Writing Drawing Scripts

In an image project, each `.py` file inside `image_src/` is an independent drawing script. Call `canvas.save()` at the end of the script to output the image:

```python
# image_src/architecture_overview.py
from drawlib import canvas, shapes, lines, styles

canvas.setup(width=100, height=60)

# Draw components
shapes.rectangle((30, 30), width=35, height=25, style=styles.Styles.AccentFlat, text="Client")
shapes.rectangle((70, 30), width=35, height=25, style=styles.Styles.PrimaryFlat, text="Server")
lines.line((47.5, 30), (52.5, 30), arrow_head="->", style=styles.Styles.PrimaryBold)

# Save image (relative to output directory)
canvas.save("architecture_overview.png")
```

---

## 4. Building Images

### Automated Build (`./build_image.sh` or `./build.sh`)
Execute the provided build script:

```bash
./image_src/build_image.sh
```

### Direct CLI Command
Alternatively, invoke the builder directly:

```bash
drawlib build image image_src/ -o image_images/ -s image_src/styles.py -u image_src/utils.py
```

### Useful Build Flags:
- `--grid` (`-g`): Automatically generates companion `*_grid.png` images overlaid with coordinate grid lines for visual debugging.
- `-f webp`: Overrides output format across all scripts to modern WebP.
- `--no-cache`: Forces a clean re-render of all images, bypassing the SQLite hash cache.
