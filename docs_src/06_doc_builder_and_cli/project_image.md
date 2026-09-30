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
├── images_src/                # [SOURCE OF TRUTH] Edit Python drawing scripts here
│   ├── _assets/               # Static assets (logos, background textures)
│   ├── sample1.py             # Primitive drawing script
│   ├── sample2.py             # Advanced diagram script (utilizing styles & utils)
│   ├── styles.py              # Shared project styling themes
│   ├── utils.py               # Reusable project drawing components
│   ├── build.sh               # Executable batch build script
│   └── README.md              # Illustration workflow guide
└── images/                    # [GENERATED] Rendered PNG/WebP output images
    ├── sample1.png
    └── sample2.png
```

### Key Rules:
- **Source of Truth**: Always author drawing scripts in `images_src/`.
- **Never Edit `images/`**: The `images/` folder is an output artifact directory overwritten during builds.

---

## 3. Writing Drawing Scripts

In an image project, each `.py` file inside `images_src/` is an independent drawing script. Call `canvas.save()` at the end of the script to output the image:

```python
# images_src/architecture_overview.py
from drawlib import canvas, shapes, lines, styles

canvas.setup(width=100, height=60)

# Draw components
shapes.rectangle((30, 30), width=35, height=25, style=styles.Styles.accent_flat, text="Client")
shapes.rectangle((70, 30), width=35, height=25, style=styles.Styles.primary_flat, text="Server")
lines.line((47.5, 30), (52.5, 30), arrowhead="->", style=styles.Styles.bold)

# Save image (relative to output directory)
canvas.save("architecture_overview.png")
```

---

## 4. Building Images

### Automated Build (`./build.sh`)
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
- `--no-cache`: Forces a clean re-render of all images, bypassing the SQLite hash cache.
