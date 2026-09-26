# Shape Style


Drawlib uses `Style` for styling shapes and the text inside them.


# Style for Shapes


The `Style` object is used for styling shapes and configuring shape alignment.

Here are the shape-related attributes of `Style`:

* `shape_line_width`: Border line width
* `shape_line_color`: Border line color
* `shape_line_style`: Border line style ("solid", "dashed", "dotted", "dashdot")
* `shape_fill_color`: Fill color
* `shape_fill_alpha`: Transparency

All of these attributes are optional. 
If you don't specify values for them, the default preset style values are applied.


## Alignment


You can configure the alignment of shapes, except for `arrow()` and `polygon()`, which specify drawing points explicitly and therefore do not have alignment options.

The default alignment is centered both horizontally and vertically. 
You can specify `"left"`, `"center"`, or `"right"` for horizontal alignment (`text_halign`). 
Similarly, you can specify `"bottom"`, `"center"`, or `"top"` for vertical alignment (`text_valign`). 
For more details and examples, please refer to the Coordinate and Alignment page.


## Style


`Style` possesses shape styling attributes:

* Line styling: `shape_line_width`, `shape_line_color`, `shape_line_style`
* Fill styling: `shape_fill_color`
* Transparency: `shape_fill_alpha`

Here are three examples:


```python
from drawlib.canvas import save, setup
from drawlib.colors import Colors, Colors140
from drawlib.config import styles
from drawlib.shapes import circle, rectangle

setup(width=150, height=50)

# left
rectangle(xy=(25, 25), width=40, height=20, style=styles.primary)
circle(
    xy=(25, 25),
    radius=15,
    style=styles.primary.patch(
        shape_line_width=5,
        shape_line_color=Colors.Red,
        shape_line_style="dashed",
        shape_fill_color=Colors.White,
    ),
)

# center
rectangle(xy=(75, 25), width=40, height=20, style=styles.primary)
circle(
    xy=(75, 25),
    radius=15,
    style=styles.primary.patch(
        shape_line_width=5,
        shape_line_color=Colors.Red,
        shape_line_style="dashed",
        shape_fill_color=Colors.Transparent,
    ),
)

# right
rectangle(xy=(125, 25), width=40, height=20, style=styles.primary)
circle(
    xy=(125, 25),
    radius=15,
    style=styles.primary.patch(
        shape_line_width=0,
        shape_fill_color=Colors140.Orange,
        shape_fill_alpha=0.3,
    ),
)
save()
```

Left example has non transparent style.
Center has fcolor transparent.
Right has alpha value.




<div class="drawlib-image" style="text-align: center;">
  <img src="shape_style_images/1.png" alt="shape_style_1" style="width: 600px; max-width: 100%;" />
</div>




    Shapes with Style

If you don't need a shape border line, set `shape_line_width=0`. 
If you don't need a shape fill color, set `shape_fill_color=Colors.Transparent` or `shape_fill_color=Colors.White`. 
These are typical shape styling configurations.


# Styling Text Inside Shapes (textstyle)


Text drawn inside a shape via the `text` parameter is styled using a `Style` object passed to the `textstyle` parameter.

Common `Style` attributes used for shape text include:

- `text_color`: Text color
- `text_size`: Text size
- `text_font`: Text font
- `text_xy_shift`: Relative offset `(x, y)` from the shape center
- `text_angle`: Text angle (default follows the shape's angle)
- `text_halign`: Horizontal alignment
- `text_valign`: Vertical alignment

Here are three examples:


```python
from drawlib.canvas import save, setup
from drawlib.colors import Colors
from drawlib.fonts import FontSansSerif, FontSerif
from drawlib.config import styles
from drawlib.shapes import rectangle

setup(width=150, height=50)

# left
rectangle(
    xy=(25, 25),
    width=40,
    height=20,
    text="rectangle()",
    style=styles.primary,
    textstyle=styles.primary.patch(
        text_color=Colors.White,
        text_size=24,
        text_font=FontSerif.COURIER_BOLD,
    ),
)


# center
rectangle(
    xy=(75, 25),
    width=40,
    height=20,
    angle=45,
    text="rectangle()",
    style=styles.primary,
    textstyle=styles.primary.patch(
        text_color=Colors.White,
        text_size=24,
        text_font=FontSansSerif.RALEWAYS_REGULAR,
    ),
)


# right
rectangle(
    xy=(125, 25),
    width=40,
    height=20,
    angle=45,
    text="rectangle()",
    style=styles.primary,
    textstyle=styles.primary.patch(
        text_color=Colors.White,
        text_angle=0,
        text_xy_shift=(-12, -3),
    ),
)

save()
```

You can configure text styles.
But also, you can configure text positioning which you can see right example.

Below is a figure illustrating these styles:




<div class="drawlib-image" style="text-align: center;">
  <img src="shape_style_images/2.png" alt="shape_style_2" style="width: 600px; max-width: 100%;" />
</div>




    Text in shapes with Style

As you can see from the center text example, text normally follows the shape's angle. 
However, you can override it, as shown in the right example. 
In that example, we also move the text positioning via `text_xy_shift`. 
The x and y values are not absolute coordinates but are relative to the shape's dimensions.


# Pre-defined Preset Styles


Shapes use `Style` instances provided by `drawlib.config` (`from drawlib.config import styles`).

Preset styles provide pre-defined `Style` objects as attributes on `styles`, following the naming pattern `<color>_<variant>`:

- `<color>`: Default border and fill
- `<color>_flat`: Flat fill, no border
- `<color>_solid`: Outline without fill
- `<color>_dashed`: Dashed outline without fill
- `<color>_bold`: Thicker border and bold text
- `<color>_light`: Thinner border and light text

For shape text, styles can also be supplied to `textstyle`.

Here are three examples:


```python
from drawlib.canvas import save, setup
from drawlib.config import styles
from drawlib.shapes import circle

setup(width=150, height=50)

# left
circle(
    xy=(25, 25),
    radius=15,
    style=styles.red_flat,
    text="circle",
    textstyle=styles.white,
)

# center
circle(
    xy=(75, 25),
    radius=15,
    style=styles.blue_solid,
    text="circle",
    textstyle=styles.blue_bold,
)

# right
circle(
    xy=(125, 25),
    radius=15,
    style=styles.green_dashed,
    text="circle",
    textstyle=styles.green,
)
save()
```

Below is a figure illustrating these styles:




<div class="drawlib-image" style="text-align: center;">
  <img src="shape_style_images/3.png" alt="shape_style_3" style="width: 600px; max-width: 100%;" />
</div>




    Pre-defined preset styles

---

<p align="center"><em>© 2026 drawlib by Yuichi Ito. Released under the Apache 2.0 License.</em></p>
