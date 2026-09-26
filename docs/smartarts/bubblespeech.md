# Bubblespeech


The Bubblespeech feature in Drawlib allows you to create irregular bubble-shaped speech graphics, often used in illustrations. 
It's implemented within the `smartarts` module as part of the Smart Art functions, offering advanced shape drawing capabilities.

Here's an example of using Bubblespeech in Drawlib:


```python
from drawlib.canvas import setup
from drawlib.config import styles
from drawlib.smartarts import bubblespeech

setup(width=95, height=52)
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




<div class="drawlib-image" style="text-align: center;">
  <img src="bubblespeech_images/1.png" alt="bubblespeech_1" style="width: 600px; max-width: 100%;" />
</div>



In the example above, the options for drawing Bubblespeech are specified. The key parameters include:

- `xy`: Coordinates `(x, y)` specifying the position of the bottom-left corner of the bubble box.
- `width`, `height`: Dimensions of the rectangular bubble area.
- `tail_edge`: Specifies the edge from which the tail extends (`"left"`, `"right"`, `"bottom"`, `"top"`).
- `tail_start_ratio`: Determines where the tail begins along the specified edge (`0.0` to `1.0`).
- `tail_vertex_xy`: Coordinates `(x, y)` specifying the tip/vertex location of the tail.
- `tail_end_ratio`: Specifies where the tail ends along the specified edge (`tail_start_ratio` < `tail_end_ratio`).

The diagram below illustrates how each parameter controls the geometry:



<div class="drawlib-image" style="text-align: center;">
  <img src="bubblespeech_images/2.png" alt="bubblespeech_2" style="width: 600px; max-width: 100%;" />
</div>



Ellipse-like bubblespeech can also be approximated or customized using shapes and lines.

---

<p align="center"><em>© 2026 drawlib by Yuichi Ito. Released under the Apache 2.0 License.</em></p>
