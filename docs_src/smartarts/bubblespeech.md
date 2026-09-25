# Bubblespeech


The Bubblespeech feature in Drawlib allows you to create irregular bubble-shaped speech graphics, often used in illustrations. 
It's implemented within the `smartarts` module as part of the Smart Art functions, offering advanced shape drawing capabilities.

Here's an example of using Bubblespeech in Drawlib:


```python
from drawlib.canvas import config
from drawlib.preset_styles import get_styles
from drawlib.smartarts import bubblespeech

styles = get_styles()
config(width=95, height=52)
bubblespeech(
    xy=(36, 11),
    width=50,
    height=30,
    tail_edge="left",
    tail_start_ratio=0.2,
    tail_vertex_xy=(16, 26),
    tail_end_ratio=0.6,
    style=styles.blue_flat,
    text="Hello Drawlib!",
    textstyle=styles.white,
)
```

This function call draws a speech bubble with a pointed tail extending from the left edge.


```drawlib 600px center
from drawlib.canvas import config
from drawlib.smartarts import bubblespeech

config(width=95, height=52)
bubblespeech(
    xy=(36, 11),
    width=50,
    height=30,
    tail_edge="left",
    tail_start_ratio=0.2,
    tail_vertex_xy=(16, 26),
    tail_end_ratio=0.6,
    style=styles.blue_flat,
    text="Hello Drawlib!",
    textstyle=styles.white,
)
```

In the example above, the options for drawing Bubblespeech are specified. The key parameters include:

- `xy`: Coordinates `(x, y)` specifying the position of the bottom-left corner of the bubble box.
- `width`, `height`: Dimensions of the rectangular bubble area.
- `tail_edge`: Specifies the edge from which the tail extends (`"left"`, `"right"`, `"bottom"`, `"top"`).
- `tail_start_ratio`: Determines where the tail begins along the specified edge (`0.0` to `1.0`).
- `tail_vertex_xy`: Coordinates `(x, y)` specifying the tip/vertex location of the tail.
- `tail_end_ratio`: Specifies where the tail ends along the specified edge (`tail_start_ratio` < `tail_end_ratio`).

The diagram below illustrates how each parameter controls the geometry:

```drawlib 600px center
from drawlib.canvas import config
from drawlib.lines import line
from drawlib.shapes import circle
from drawlib.smartarts import bubblespeech
from drawlib.text import text

config(width=95, height=52)

# Bubble shape with neutral style for annotation
bubblespeech(
    xy=(36, 11),
    width=50,
    height=30,
    tail_edge="left",
    tail_start_ratio=0.2,
    tail_vertex_xy=(16, 26),
    tail_end_ratio=0.6,
    style=styles.light,
    text="Hello Drawlib!",
    textstyle=styles.bold,
)

# Reference edge
line((36, 11), (36, 41), style=styles.blue_dashed)
text((36, 45), 'tail_edge = "left"', style=styles.blue)

# Bottom-left corner xy
circle(xy=(36, 11), radius=1, style=styles.red_flat)
text((36, 7), "xy = (36, 11)", style=styles.red)

# Tail start ratio (0.2 * 30 = 6 above bottom -> y=17)
line((33, 11), (33, 17), arrowhead="<->", style=styles.blue)
text((19, 14), "tail_start_ratio = 0.2", style=styles.blue)

# Tail vertex
circle(xy=(16, 26), radius=1, style=styles.red_flat)
text((20, 30), "tail_vertex_xy = (16, 26)", style=styles.red)

# Tail end ratio (0.6 * 30 = 18 above bottom -> y=29)
line((39, 11), (39, 29), arrowhead="<->", style=styles.blue)
text((53, 14), "tail_end_ratio = 0.6", style=styles.blue)
```

Ellipse-like bubblespeech can also be approximated or customized using shapes and lines.

---

<p align="center"><em>© 2026 drawlib by Yuichi Ito. Released under the Apache 2.0 License.</em></p>
