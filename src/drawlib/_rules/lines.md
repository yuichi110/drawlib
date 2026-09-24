# Drawlib Lines Guidelines

Draw straight, curved, or multi-point lines with arrowheads and annotations.

## 1. Imports
```python
from drawlib.lines import line, line_curved, lines, lines_curved
from drawlib.types import Style
```

## 2. Core Functions
- `line(start, end, arrowhead=None, width=None, style=None, text="", textstyle=None)`
  - `start`, `end`: Endpoints `(x, y)`.
  - `arrowhead`: Arrowhead direction (`"->"`, `"<-"`, `"<->"`, or `None`).
  - `width`: Line thickness (overrides style line width).
- `line_curved(start, end, bend=0.0, arrowhead=None, width=None, style=None, text="", textstyle=None)`
  - `bend`: Curvature from -1.0 to 1.0 (0.0 is straight).
- `lines(points, arrowhead=None, width=None, style=None)`
  - `points`: Chained polyline vertices `[(x1, y1), (x2, y2), ...]`.
- `lines_curved(points, arrowhead=None, width=None, style=None)`
  - Smooth Bezier curve connecting coordinates.

## 3. Styling & Options
- `style`: Preset style string (e.g. `"blue"`, `"red_dashed"`, `"bold"`) or `Style(line_color=..., line_width=..., line_style=...)`.
- `text`: Centered label text along the line.
- `textstyle`: Style applied to label text.

## 4. Minimal Example
```python
from drawlib.canvas import config, save
from drawlib.lines import line, line_curved

config(width=100, height=50)
line((10, 25), (45, 25), arrowhead="->", style="blue_bold", text="request")
line_curved((55, 35), (90, 15), bend=0.3, arrowhead="->", style="green_dashed", text="response")
save()
```
