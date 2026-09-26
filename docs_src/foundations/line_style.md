# Line Style


Drawlib provides six functions for drawing lines and lines with arrowheads:

* `line()`
* `line_curve()`
* `line_bezier1()`
* `line_bezier2()`
* `lines()`
* `lines_bezier()`

They all share the following arguments:

- `arrowhead`: Specifies the type of arrowhead. Options are `["", "->", "<-", "<->", "-"]`.
- `width`: Specifies the line width. This should typically be configured within the style, but it is also available as an optional argument.
- `style`: Defines the line style. Requires a `Style` object (e.g., `styles.primary`).

These arguments control the line's style. 
Regarding line width, you can control it using both the `width` argument and the `style` attribute. 
We recommend using the style attribute, as it is a visual parameter. 
If you configure it in the style, you can change the line width by modifying the shared style. 
However, since many users might want to change the line width easily, the width argument is provided as a shortcut.

Additionally, we have a function called `arrow()`. 
You might think it is similar to a line with an arrowhead, but it actually draws a thick and bold arrow shape, not an arrow line.


# Style for Lines


The `Style` object has the following attributes for line styling:

* `line_width`: Line width, represented as a float value.
* `line_color`: Line color, specified in RGB (0~255, 0~255, 0~255) or RGBA (0~255, 0~255, 0~255, 0~1.0). You can use the Color classes for convenience.
* `line_alpha`: Line transparency, ranging from 0.0 (totally transparent) to 1.0 (fully opaque).
* `line_style`: Line style, which can be one of `["solid", "dashed", "dotted", "dashdot"]`. The default style is solid.
* `line_arrow_head_fill`: Arrowhead fill, indicating whether the arrowhead is filled (`True`) or not (`False`). The default is `False`.
* `line_arrow_head_scale`: Arrowhead scale, determining the size of the arrowhead. A larger value results in a larger arrowhead. The default scale is `20.0`.

The first four attributes (`line_width`, `line_color`, `line_alpha`, `line_style`) affect both lines and lines with arrowheads. 
The last two attributes (`line_arrow_head_fill`, `line_arrow_head_scale`) specifically affect lines with arrowheads.
This structure allows for precise control over the appearance of lines and their associated arrowheads within Drawlib.

It's important to note that whether the arrowhead is present or not carries logical meaning, so it is considered a function argument rather than a style attribute.



# Drawing line with style


Let's explore different line styles through examples.


```python
from drawlib.canvas import save, setup
from drawlib.colors import Colors
from drawlib.lines import line
from drawlib.text import text
from drawlib.config import styles

setup(width=100, height=40)

text((10, 5), "primary", style=styles.primary)
line((20, 5), (40, 5), style=styles.primary)
text((10, 15), "width: 5", style=styles.primary)
line((20, 15), (40, 15), style=styles.primary.patch(line_width=5))
text((10, 25), "color: Red", style=styles.primary)
line((20, 25), (40, 25), style=styles.primary.patch(line_color=Colors.Red))
text((10, 35), "alpha: 0.2", style=styles.primary)
line((20, 35), (40, 35), style=styles.primary.patch(line_alpha=0.2))

text((60, 5), "style: solid\n(default)", style=styles.primary)
line((70, 5), (90, 5), style=styles.primary.patch(line_style="solid"))
text((60, 15), "style: dashed", style=styles.primary)
line((70, 15), (90, 15), style=styles.primary.patch(line_style="dashed"))
text((60, 25), "style: dotted", style=styles.primary)
line((70, 25), (90, 25), style=styles.primary.patch(line_style="dotted"))
text((60, 35), "style: dashdot", style=styles.primary)
line((70, 35), (90, 35), style=styles.primary.patch(line_style="dashdot"))

save()
```

Running this code produces the following output:


```drawlib 500px center
from drawlib.canvas import save, setup
from drawlib.colors import Colors
from drawlib.lines import line
from drawlib.text import text
from drawlib.config import styles

setup(width=100, height=40)

text((10, 5), "primary", style=styles.primary)
line((20, 5), (40, 5), style=styles.primary)
text((10, 15), "width: 5", style=styles.primary)
line((20, 15), (40, 15), style=styles.primary.patch(line_width=5))
text((10, 25), "color: Red", style=styles.primary)
line((20, 25), (40, 25), style=styles.primary.patch(line_color=Colors.Red))
text((10, 35), "alpha: 0.2", style=styles.primary)
line((20, 35), (40, 35), style=styles.primary.patch(line_alpha=0.2))

text((60, 5), "style: solid\n(default)", style=styles.primary)
line((70, 5), (90, 5), style=styles.primary.patch(line_style="solid"))
text((60, 15), "style: dashed", style=styles.primary)
line((70, 15), (90, 15), style=styles.primary.patch(line_style="dashed"))
text((60, 25), "style: dotted", style=styles.primary)
line((70, 25), (90, 25), style=styles.primary.patch(line_style="dotted"))
text((60, 35), "style: dashdot", style=styles.primary)
line((70, 35), (90, 35), style=styles.primary.patch(line_style="dashdot"))

save()
```


    lines with styles

This example demonstrates various line styles applied to lines using Drawlib.



# Drawing line arrow with style


All line functions in Drawlib support the `arrowhead` argument, which allows you to add arrowheads to lines.

The `arrowhead` argument accepts one of the following parameters:

- `""`: No arrowhead (default).
- `"->"`: Right arrowhead.
- `"<-"`: Left arrowhead.
- `"<->"`: Both right and left arrowheads.

You can customize the visual appearance of arrowheads using the following `Style` attributes:

* `arrow_head_fill`: Arrowhead fill. Determines whether the arrowhead is filled (`True`) or not (`False`). Default is `False`.
* `arrow_head_scale`: Arrowhead scale. Controls the size of the arrowhead. Larger values result in larger arrowheads. Default is `20.0`.

Let's see an example:


```python
from drawlib.canvas import save, setup
from drawlib.colors import Colors
from drawlib.lines import line
from drawlib.text import text
from drawlib.config import styles

setup(width=100, height=50)

text((10, 5), "arrowhead ->", style=styles.primary)
line((20, 5), (40, 5), arrowhead="->", style=styles.primary)
text((10, 13), "width: 5", style=styles.primary)
line((20, 13), (40, 13), arrowhead="->", style=styles.primary.patch(line_width=5))
text((10, 21), "color: Red", style=styles.primary)
line((20, 21), (40, 21), arrowhead="->", style=styles.primary.patch(line_color=Colors.Red))
text((10, 29), "alpha: 0.2", style=styles.primary)
line((20, 29), (40, 29), arrowhead="->", style=styles.primary.patch(line_alpha=0.2))
text((10, 37), "lstyle: dashed", style=styles.primary)
line((20, 37), (40, 37), arrowhead="->", style=styles.primary.patch(line_style="dashed"))
text((10, 45), "head_scale: 40", style=styles.primary)
line((20, 45), (40, 45), arrowhead="->", style=styles.primary.patch(line_arrow_head_scale=40))

text((60, 5), "arrowhead: ->", style=styles.primary)
line((70, 5), (90, 5), arrowhead="->", style=styles.primary)
text((60, 13), "arrowhead: <-", style=styles.primary)
line((70, 13), (90, 13), arrowhead="<-", style=styles.primary)
text((60, 21), "arrowhead: <->", style=styles.primary)
line((70, 21), (90, 21), arrowhead="<->", style=styles.primary)
text((60, 29), 'arrowhead: ""', style=styles.primary)
line((70, 29), (90, 29), arrowhead="", style=styles.primary)
text((60, 37), "head_fill: True", style=styles.primary)
line((70, 37), (90, 37), arrowhead="->", style=styles.primary.patch(line_arrow_head_fill=True))
text((60, 45), "head_scale: 10", style=styles.primary)
line((70, 45), (90, 45), arrowhead="->", style=styles.primary.patch(line_arrow_head_scale=10))

save()
```

Executing this code generates the following output:


```drawlib 500px center
from drawlib.canvas import save, setup
from drawlib.colors import Colors
from drawlib.lines import line
from drawlib.text import text
from drawlib.config import styles

setup(width=100, height=50)

text((10, 5), "arrowhead ->", style=styles.primary)
line((20, 5), (40, 5), arrowhead="->", style=styles.primary)
text((10, 13), "width: 5", style=styles.primary)
line((20, 13), (40, 13), arrowhead="->", style=styles.primary.patch(line_width=5))
text((10, 21), "color: Red", style=styles.primary)
line((20, 21), (40, 21), arrowhead="->", style=styles.primary.patch(line_color=Colors.Red))
text((10, 29), "alpha: 0.2", style=styles.primary)
line((20, 29), (40, 29), arrowhead="->", style=styles.primary.patch(line_alpha=0.2))
text((10, 37), "lstyle: dashed", style=styles.primary)
line((20, 37), (40, 37), arrowhead="->", style=styles.primary.patch(line_style="dashed"))
text((10, 45), "head_scale: 40", style=styles.primary)
line((20, 45), (40, 45), arrowhead="->", style=styles.primary.patch(line_arrow_head_scale=40))

text((60, 5), "arrowhead: ->", style=styles.primary)
line((70, 5), (90, 5), arrowhead="->", style=styles.primary)
text((60, 13), "arrowhead: <-", style=styles.primary)
line((70, 13), (90, 13), arrowhead="<-", style=styles.primary)
text((60, 21), "arrowhead: <->", style=styles.primary)
line((70, 21), (90, 21), arrowhead="<->", style=styles.primary)
text((60, 29), 'arrowhead: ""', style=styles.primary)
line((70, 29), (90, 29), arrowhead="", style=styles.primary)
text((60, 37), "head_fill: True", style=styles.primary)
line((70, 37), (90, 37), arrowhead="->", style=styles.primary.patch(line_arrow_head_fill=True))
text((60, 45), "head_scale: 10", style=styles.primary)
line((70, 45), (90, 45), arrowhead="->", style=styles.primary.patch(line_arrow_head_scale=10))

save()
```


    arrow lines with styles

This example demonstrates lines with different arrowhead styles and visual configurations using Drawlib.



# Pre-defined Line Styles


Drawlib provides pre-defined line styles on the `styles` object.
You can access them as attributes (e.g. `styles.red`, `styles.red_solid`, `styles.red_dashed`, `styles.bold`).

Let's look at an example:


```python
from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.text import text
from drawlib.config import styles

setup(width=100, height=40)

text((12, 5), "styles.primary", style=styles.primary)
line((25, 5), (40, 5), style=styles.primary)
text((12, 15), "styles.red", style=styles.primary)
line((25, 15), (40, 15), style=styles.red)
text((12, 25), "styles.red_solid", style=styles.primary)
line((25, 25), (40, 25), style=styles.red_solid)
text((12, 35), "styles.red_dashed", style=styles.primary)
line((25, 35), (40, 35), style=styles.red_dashed)

text((60, 5), "styles.red_bold", style=styles.primary)
line((75, 5), (90, 5), arrowhead="->", style=styles.red_bold)
text((60, 15), "styles.blue_flat", style=styles.primary)
line((75, 15), (90, 15), arrowhead="->", style=styles.blue_flat)
text((60, 25), "styles.dashed", style=styles.primary)
line((75, 25), (90, 25), arrowhead="->", style=styles.dashed)
text((60, 35), "styles.bold", style=styles.primary)
line((75, 35), (90, 35), arrowhead="->", style=styles.bold)

save()
```

Executing this code generates the following output:


```drawlib 500px center
from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.text import text
from drawlib.config import styles

setup(width=100, height=40)

text((12, 5), "styles.primary", style=styles.primary)
line((25, 5), (40, 5), style=styles.primary)
text((12, 15), "styles.red", style=styles.primary)
line((25, 15), (40, 15), style=styles.red)
text((12, 25), "styles.red_solid", style=styles.primary)
line((25, 25), (40, 25), style=styles.red_solid)
text((12, 35), "styles.red_dashed", style=styles.primary)
line((25, 35), (40, 35), style=styles.red_dashed)

text((60, 5), "styles.red_bold", style=styles.primary)
line((75, 5), (90, 5), arrowhead="->", style=styles.red_bold)
text((60, 15), "styles.blue_flat", style=styles.primary)
line((75, 15), (90, 15), arrowhead="->", style=styles.blue_flat)
text((60, 25), "styles.dashed", style=styles.primary)
line((75, 25), (90, 25), arrowhead="->", style=styles.dashed)
text((60, 35), "styles.bold", style=styles.primary)
line((75, 35), (90, 35), arrowhead="->", style=styles.bold)

save()
```


    lines with pre-defined style names

This example demonstrates lines drawn using pre-defined style names in Drawlib, showcasing different colors, line types, and thicknesses based on the specified styles.

---

<p align="center"><em>© 2026 drawlib by Yuichi Ito. Released under the Apache 2.0 License.</em></p>
