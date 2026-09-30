# 14. Project Scaffolding & Standard Templates

Drawlib enforces a clean, predictable project structure for all documentation and illustration repositories. Never construct project folders manually; always scaffold them using `drawlib init`.

## The 4 Standard Project Templates

| Template | Scaffold Command | Best Suited For | Output Directory |
| :--- | :--- | :--- | :--- |
| **`site`** | `drawlib init site` | Complete documentation website with sidebar navigation | `docs_src/` -> `docs_html/` & `docs/` |
| **`simple`** | `drawlib init simple` | Single technical specification, RFC, or design memo | `docs_src/` -> `doc.html` & `doc.md` |
| **`pdf`** | `drawlib init pdf` | Multi-chapter formal technical book or engineering report | `docs_src/` -> `document.pdf` |
| **`image`** | `drawlib init image` | Standalone Python drawing batch scripts | `images_src/` -> `images/` |

```drawlib 640px center caption:"Figure 14.1: The Four Standard Drawlib Project Templates"
from drawlib.canvas import setup
from drawlib.icons import phosphor
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=120, height=48)

templates = [
    (18, phosphor.browsers, "Site Template", "Multi-page docs\nnavbar.md sidebar\nHTML + GitHub MD", Styles.primary_flat),
    (46, phosphor.file_text, "Simple Template", "Single RFC / Spec\ndoc.md -> doc.html\nStandalone memo", Styles.secondary_flat),
    (74, phosphor.book, "PDF Template", "Multi-chapter book\n00-cover, 01-intro\nAuto-index page", Styles.accent_flat),
    (102, phosphor.image, "Image Template", "Python scripts only\nimages_src/*.py\nBatch PNG export", Styles.success_flat),
]

for x, icon_fn, title, desc, st in templates:
    rectangle(xy=(x, 24), width=24, height=36, r=2.5, style=Styles.muted_dashed)
    icon_fn(xy=(x, 34), width=7, style=st)
    text(xy=(x, 25), text=title, style=Styles.bold, size=8.5)
    text(xy=(x, 14), text=desc, style=Styles.primary, size=7.5)
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

### The Golden Rule of Source of Truth

Never edit generated output directories (`docs/`, `docs_html/`, `images/`). All files in these folders are automatically overwritten during compilation. Always edit files inside `<base>_src/`.
