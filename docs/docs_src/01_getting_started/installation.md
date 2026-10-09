# Installation Guide

Drawlib is published on PyPI and can be installed using `uv` (recommended) or standard `pip`.

---

## Requirements

- **Python**: Version 3.11 or higher.
- **Operating System**: Linux, macOS, or Windows.

---

## 1. Using `uv` (Recommended)

Add Drawlib to your current project dependencies:

```bash
# Add to active project
$ uv add drawlib

# Verify installation and CLI version
$ uv run drawlib --version
```

### Standalone CLI Execution (`uvx`)
If you want to run the Drawlib CLI tool without adding it to a project:

```bash
$ uvx drawlib --version
$ uvx drawlib init site
```

---

## 2. Using `pip`

Install Drawlib into your virtual environment:

```bash
$ pip install drawlib

# Verify installation
$ drawlib --version
```

---

## 3. Optional PDF Export Support

Drawlib includes built-in support for compiling Markdown documents into standalone PDF publications via headless Chromium.

To enable PDF generation (`drawlib build pdf`):

```bash
# When using uv:
$ uv add "drawlib[pdf]"
$ uv run playwright install chromium

# When using pip:
$ pip install "drawlib[pdf]"
$ playwright install chromium
```

```drawlib fold-code 650px center file:installation_setup_workflow.png caption:"Three-Step Drawlib Environment Setup Workflow"
from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles

setup(width=138, height=44)

# Step 1: Core Package (Hero focal origin)
rectangle(
    (23, 22),
    width=38,
    height=32,
    style=Styles.PrimaryFlat.patch(shape_r=2),
    text="Step 1: Core Package\n\nuv add drawlib\npip install drawlib\n(Python 3.11+ • Zero heavy deps)",
    text_style=Styles.WhiteBold.patch(text_size=8.0),
)

# Step 2: Optional PDF Engine (Neutral card)
rectangle(
    (69, 22),
    width=38,
    height=32,
    style=Styles.Neutral.patch(shape_r=2),
    text='Step 2: Optional PDF Engine\n\nuv add "drawlib[pdf]"\nplaywright install chromium\n(Headless vector PDF export)',
    text_style=Styles.Dark.patch(text_size=8.0),
)

# Step 3: Offline Asset Pre-fetch (SecondaryNeutral card)
rectangle(
    (115, 22),
    width=38,
    height=32,
    style=Styles.SecondaryNeutral.patch(shape_r=2),
    text="Step 3: Offline Asset Pre-fetch\n\ndrawlib cache download --all\n(Pre-cache fonts, icons & maps\nfor CI / air-gapped builds)",
    text_style=Styles.Dark.patch(text_size=8.0),
)

# Connectors
line((42, 22), (50, 22), arrow_head="->", style=Styles.DarkBold)
line((88, 22), (96, 22), arrow_head="->", style=Styles.DarkBold)

save()
```

---

## 4. Asset & Build Cache Management (`drawlib cache`)

To maintain a minimal PyPI package size, high-resolution icon sets (Phosphor, FontAwesome, and official Google Cloud icons), multilingual fonts, and geographic map datasets are downloaded on demand upon first use and cached inside `drawlib/_cached_assets/` (managed via `drawlib cache`). Meanwhile, project-local incremental diagram builds are cached separately in `.drawlib/cache.db`.

```drawlib fold-code 650px center file:installation_two_tier_cache.png caption:"Two-Tier Asset and Incremental Build Cache Architecture"
from drawlib.canvas import save, setup
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=136, height=58)

# Left container: Tier 1 Global Asset Cache
rectangle((36, 29), width=58, height=46, style=Styles.SecondaryNeutral.patch(shape_r=2.5))
rectangle(
    (36, 46.5),
    width=54,
    height=7,
    style=Styles.PrimaryFlat.patch(shape_r=1.5),
    text="Tier 1: Global Asset Cache",
    text_style=Styles.WhiteBold.patch(text_size=9.5),
)
text((36, 39.5), "drawlib/_cached_assets/", style=Styles.DarkBold.patch(text_size=8.8))
rectangle((36, 32.5), width=52, height=5.5, style=Styles.Neutral.patch(shape_r=1), text="Fonts (Roboto, Noto CJK, Source Code)", text_style=Styles.Dark.patch(text_size=8.2))
rectangle((36, 25.5), width=52, height=5.5, style=Styles.Neutral.patch(shape_r=1), text="Icons (phosphor, fontawesome, gcp)", text_style=Styles.Dark.patch(text_size=8.2))
rectangle((36, 18.5), width=52, height=5.5, style=Styles.Neutral.patch(shape_r=1), text="GeoMap Vector Datasets (world & regional)", text_style=Styles.Dark.patch(text_size=8.2))
rectangle(
    (36, 10.5),
    width=52,
    height=6,
    style=Styles.PrimaryNeutral.patch(shape_r=1),
    text="drawlib cache download --all\nclear --fonts | --icons | --maps",
    text_style=Styles.DarkBold.patch(text_size=7.8),
)

# Right container: Tier 2 Project Incremental Build Cache
rectangle((100, 29), width=58, height=46, style=Styles.Neutral.patch(shape_r=2.5))
rectangle(
    (100, 46.5),
    width=54,
    height=7,
    style=Styles.DarkFlat.patch(shape_r=1.5),
    text="Tier 2: Incremental Build Cache",
    text_style=Styles.WhiteBold.patch(text_size=9.5),
)
text((100, 39.5), ".drawlib/cache.db (SQLite)", style=Styles.DarkBold.patch(text_size=8.8))
rectangle((100, 32.5), width=52, height=5.5, style=Styles.SecondaryNeutral.patch(shape_r=1), text="SHA-256 Digest (Code + styles.py + utils.py)", text_style=Styles.Dark.patch(text_size=8.2))
rectangle((100, 25.5), width=52, height=5.5, style=Styles.SecondaryNeutral.patch(shape_r=1), text="Hashed Diagram Renders (PNG / WebP / SVG)", text_style=Styles.Dark.patch(text_size=8.2))
rectangle((100, 18.5), width=52, height=5.5, style=Styles.SecondaryNeutral.patch(shape_r=1), text="Instant Cache Hit on Unchanged Blocks", text_style=Styles.Dark.patch(text_size=8.2))
rectangle(
    (100, 10.5),
    width=52,
    height=6,
    style=Styles.PrimaryNeutral.patch(shape_r=1),
    text="drawlib build [--no-cache]\ndrawlib cache clear --images",
    text_style=Styles.DarkBold.patch(text_size=7.8),
)

save()
```

You can inspect, pre-fetch (e.g. for offline builds, Docker images, or CI/CD pipelines), and clear both caches via `drawlib cache`:

```bash
# Inspect cached font, icon, and map packages
$ uv run drawlib cache list

# Pre-download all font, icon, and map packages
$ uv run drawlib cache download --all

# Or pre-download specific asset categories selectively
$ uv run drawlib cache download --fonts
$ uv run drawlib cache download --icons
$ uv run drawlib cache download --maps

# Clear project-local incremental diagram build cache (.drawlib/cache.db)
$ uv run drawlib cache clear --images

# Clear all caches (downloaded font/icon/map assets + SQLite image build cache)
$ uv run drawlib cache clear --all
```

---

## 5. Verifying Installation

Verify that the Drawlib CLI commands and rule guides are accessible:

```bash
$ uv run drawlib --help
$ uv run drawlib rules list
```
