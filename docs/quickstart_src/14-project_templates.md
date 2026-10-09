# 14. Project Scaffolding & Standard Templates

Drawlib enforces a clean, predictable project structure for all documentation and illustration repositories. Never construct project folders manually; always scaffold them using `drawlib init`.

## The 4 Standard Project Templates

| Template | Scaffold Command | Best Suited For | Output Directory |
| :--- | :--- | :--- | :--- |
| **`doc`** | `drawlib init doc` | Linear technical document, spec, RFC, or formal report | `docs_src/` -> `doc.html`, `doc.pdf`, `doc.md` |
| **`site`** | `drawlib init site` | Complete documentation website with sidebar navigation | `docs_src/` -> `docs_html/` & `docs/` |
| **`slide`** | `drawlib init slide` | 16:9 presentation slide deck (web & vector PDF) | `slide_src/` -> `slide/index.html` & `slide.pdf` |
| **`images`** | `drawlib init images` | Standalone Python drawing batch scripts | `images_src/` -> `images/` |

```drawlib 640px center file:project_templates.png caption:"Figure 14.1: The Four Standard Drawlib Project Templates"
from drawlib.canvas import setup
from drawlib.icons import phosphor
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=120, height=48)

templates = [
    (18, phosphor.file_text, "Doc Template", "Linear docs & RFCs\nHTML, PDF, MD, img\nSingle/multi-chapter", Styles.PrimaryFlat),
    (46, phosphor.browsers, "Site Template", "Multi-page docs\nnavbar.md sidebar\nHTML + GitHub MD", Styles.SecondaryFlat),
    (74, phosphor.presentation, "Slide Template", "16:9 presentations\nInteractive HTML\n1-slide-per-page PDF", Styles.AccentFlat),
    (102, phosphor.image, "Images Template", "Python scripts only\nimages_src/*.py\nBatch PNG export", Styles.SuccessFlat),
]

for x, icon_fn, title, desc, st in templates:
    rectangle(xy=(x, 24), width=24, height=36, style=Styles.MutedDashed.patch(shape_r=2.5))
    icon_fn(xy=(x, 34), width=7, style=st)
    text(xy=(x, 25), text=title, style=Styles.DarkBold.patch(text_size=8.5))
    text(xy=(x, 14), text=desc, style=Styles.Dark.patch(text_size=7.5))
```

## Standard Project Directory Architecture

Every Drawlib documentation project adheres to strict source-of-truth isolation:

```text
my_project/
├── docs_src/               # SOURCE OF TRUTH (Always edit here)
│   ├── 00-cover.md         # Chapter 0
│   ├── 01-architecture.md  # Chapter 1
│   ├── navbar.md           # Sidebar navigation tree (for site template)
│   ├── styles.py           # Custom project design tokens (optional)
│   ├── utils.py            # Custom drawing helper macros (optional)
│   ├── template.html       # HTML layout template (optional)
│   ├── style.css           # Custom CSS styling (optional)
│   └── build.sh            # Automated build launcher script
├── docs_html/              # GENERATED: Static HTML website (do not edit directly)
└── docs/                   # GENERATED: Markdown with images for GitHub
```

## Presentations with `drawlib.slide`

The `slide` template compiles 16:9 widescreen presentation decks to both an interactive web presentation (`slide/index.html`) and an engineering PDF deck (`slide.pdf`):

```python
# slide_src/utils.py
from drawlib.slide import current_slide
from drawlib.text import text
from drawlib.styles import Styles

def draw_slide_footer():
    # Introspect page number and total count at draw time
    page_text = f"{current_slide.page_number} / {current_slide.total_pages}"
    text((1800, 45), text=page_text, style=Styles.Dark)
```

## Dynamic Animations with `drawlib.anim`

Drawlib also natively supports generating looping animated diagrams (APNG and Animated WebP) using `from drawlib.anim import Animation`:

```python
from drawlib.anim import Animation
from drawlib.canvas import setup
from drawlib.shapes import circle
from drawlib.styles import Styles

anim = Animation(file="pipeline_flow.webp", loop=0)
for step in range(3):
    with anim.frame(duration=0.5):
        setup(width=100, height=40)
        circle((25 + step * 25, 20), radius=8, style=Styles.PrimaryFlat)
```

### The Golden Rule of Source of Truth

Never edit generated output directories (`docs/`, `docs_html/`, `images/`, `slide/`). All files in these folders are automatically overwritten during compilation. Always edit files inside `<base>_src/`.
