# Drawlib Agent Drawing Guidelines

Drawlib is a Python diagramming library ("Illustration as Code").
Follow these principles to write robust, maintainable drawing scripts.

## 1. Canvas Lifecycle & Core Rules
1. **Canvas Lifecycle**:
   - `config(width=..., height=...)` to set dimensions (default: 100x100).
   - Draw shapes, lines, text, icons, smartarts, or charts.
   - `save()` to finalize and write the image file.
2. **Coordinate System**:
   - Origin `(0, 0)` is at the **bottom-left** corner of the canvas.
   - X-axis increases to the right; Y-axis increases upward.
3. **Module Import Convention**:
   - Always import symbols from public domain modules:
     ```python
     from drawlib.canvas import clear, config, save
     from drawlib.shapes import circle, ellipse, polygon, rectangle
     from drawlib.lines import line, line_curved
     from drawlib.text import text
     from drawlib.colors import Colors, ColorsDefault
     from drawlib.types import Style
     ```

## 2. Minimal Example
```python
from drawlib.canvas import config, save
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.text import text

config(width=100, height=50)
rectangle((25, 25), width=30, height=20, style="blue_flat", text="Service A", textstyle="white_bold")
line((40, 25), (60, 25), arrowhead="->", style="bold")
rectangle((75, 25), width=30, height=20, style="green_flat", text="Service B", textstyle="white_bold")
save()
```

## 3. Verification & Rules Commands
Execute these commands in the terminal as needed during drawing or verification:
- `python <script>.py` : Run script and generate image.
- `drawlib export <script>.py -g -o scratch/check.png` : Export image with coordinate grid overlay.
- `drawlib rules list` : List all available rule topics.
- `drawlib rules show <topic>` : Fetch detailed specifications and examples for a topic.

Available topics: `cli`, `shapes`, `lines`, `text`, `icons`, `preset_styles`, `smartarts`, `charts`, `diagrams`.
