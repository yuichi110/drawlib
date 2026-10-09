# Quick Start Guide

Drawlib makes creating publication-ready technical diagrams intuitive and reproducible. 
You can author diagrams either as **standalone Python scripts** (`.py`) or as **embedded Markdown blocks** (` ```drawlib `).

---

## The Standard 5-Step Drawing Workflow

Every Drawlib illustration follows a clean, predictable lifecycle:

1. **Import APIs**: Import canvas management, drawing primitives, and styling presets.
2. **Setup Canvas**: Initialize canvas dimensions (`width`, `height`) via `setup()`.
3. **Draw Structural Containers**: Create boundary boxes, cloud regions, or background grids.
4. **Draw Entities & Connectors**: Add shapes, icons, and lines with semantic styles and labels.
5. **Save / Export**: Save the drawing to an image file via `save()`, or let the Document Builder render it inline automatically.

```drawlib fold-code 650px center file:quickstart_five_step_workflow.png caption:"The Standard 5-Step Drawlib Drawing Workflow"
from drawlib.canvas import save, setup
from drawlib.smartarts import ChevronProcess
from drawlib.styles import Styles

setup(width=136, height=32)

workflow = ChevronProcess(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=8.8),
    description_style=Styles.Muted,
    corner_angle=60.0,
    spacing=2.0,
    flat_left_end=True,
)
workflow.add("1. Import\nAPIs")
workflow.add("2. Setup\nCanvas")
workflow.add("3. Draw\nContainers")
workflow.add("4. Entities &\nConnectors")
workflow.add(
    "5. Save /\nExport",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=8.8),
)
workflow.draw(xy=(8, 8), width=120.0, height=16.0)
save()
```

---

## 1. Standalone Python Script (`images` Project)

> [!IMPORTANT]
> **Project-First Rule (`drawlib init`)**:  
> Rather than creating bare `.py` files in an uninitialized directory, always scaffold a Drawlib project first so `styles.py` (theme & language fonts), `utils.py`, `_assets/`, and `build.sh` are properly configured:
> ```bash
> # Scaffold a standalone illustration project (creates images_src/ -> images/)
> $ uv run drawlib init images
> ```

Create a Python script named `images_src/client_server.py`:

```python
from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.styles import Styles
from drawlib.text import text

# Step 2: Setup canvas dimensions (Cartesian space: 100 wide x 50 high)
setup(width=100, height=50)

# Step 3: Draw background boundary container
rectangle((50, 25), width=90, height=40, style=Styles.MutedDashed)

# Step 4: Draw main entities and connectors (50%+ Neutral-Grounded)
circle((25, 25), radius=12, style=Styles.Neutral, text="Client")
rectangle((75, 25), width=24, height=20, style=Styles.PrimaryFlat, text="Server", text_style=Styles.WhiteBold)

# Connection line with arrowhead
line((37, 25), (63, 25), arrow_head="->", style=Styles.DarkBold)
text((50, 30), "REST API", style=Styles.DarkBold)

# Step 5: Save image (defaults to client_server.png)
save()
```

### Running and Previewing

Build all scripts in `images_src/` using the generated build script, or run a single script directly:

```bash
# Batch-compile all scripts in images_src/ to images/
$ ./images_src/build.sh

# Or run a single script directly with Python
$ uv run python images_src/client_server.py
```

Use the unified `drawlib show` CLI command to export headless previews or inspect coordinate overlays:

```bash
# Export directly to a specified output file
$ uv run drawlib show images_src/client_server.py -o .drawlib/scratch/output.png

# Overlay a visual coordinate grid (-g) to check element spacing
$ uv run drawlib show images_src/client_server.py -g -o .drawlib/scratch/output_grid.png
```

---

## 2. Embedded Markdown Document

Inside any Markdown document (such as `doc.md` in a `doc` or `site` project), simply embed the code block with ````drawlib````:

````markdown
# Architecture Overview

Here is our primary service flow:

```drawlib 600px center file:client_server_communication.png caption:"Client-Server REST Communication"
from drawlib.canvas import save, setup
from drawlib.shapes import rectangle, circle
from drawlib.lines import line
from drawlib.text import text
from drawlib.styles import Styles

setup(width=100, height=50)

rectangle((50, 25), width=90, height=40, style=Styles.MutedDashed)
circle((25, 25), radius=12, style=Styles.Neutral, text="Client")
rectangle((75, 25), width=24, height=20, style=Styles.PrimaryFlat, text="Server", text_style=Styles.WhiteBold)
line((37, 25), (63, 25), arrow_head="->", style=Styles.DarkBold)
text((50, 30), "REST API", style=Styles.DarkBold)
save()
```
````

You can preview a specific named block inside a Markdown file with a coordinate grid before building the full site:

```bash
# Preview a specific named diagram block with a coordinate grid (-g)
$ uv run drawlib show doc.md client_server_communication.png -g -o .drawlib/scratch/preview.png
```

When compiled with `drawlib build html` or `drawlib build markdown`, the code fence is executed and replaced with the rendered image:

```drawlib fold-code 600px center file:client_server_communication_styled.png caption:"Client-Server REST Communication"
from drawlib.canvas import save, setup
from drawlib.shapes import rectangle, circle
from drawlib.lines import line
from drawlib.text import text
from drawlib.styles import Styles

setup(width=100, height=50)

rectangle((50, 25), width=90, height=40, style=Styles.MutedDashed)
circle((25, 25), radius=12, style=Styles.Neutral, text="Client")
rectangle((75, 25), width=24, height=20, style=Styles.PrimaryFlat, text="Server", text_style=Styles.WhiteBold)
line((37, 25), (63, 25), arrow_head="->", style=Styles.DarkBold)
text((50, 30), "REST API", style=Styles.DarkBold)
save()
```

---

## 3. Key Rules for Smooth Drawing

1. **`setup()` is Mandatory**: Always call `setup(width=..., height=...)` at the start of your drawing block.
2. **Handling `save()` in Markdown Blocks**: In Markdown embedded blocks, calling `save()` is optional because Drawlib captures the canvas automatically (and calls to `save()` are safely treated as no-ops). However, writing `save()` (without arguments) in complete examples is recommended for 100% copy-paste compatibility with standalone `.py` scripts.
3. **Color Discipline (50%+ Neutral-Grounded Architecture)**: Avoid rainbow chaos. Ground 50% or more of nodes in calm neutral cards (`Styles.Neutral`, `Styles.PrimaryNeutral`, `Styles.SecondaryNeutral`), reserve saturated hero styles (`Styles.PrimaryFlat`) for 1–2 primary focal points, and use `Styles.DarkBold` for connectors.
