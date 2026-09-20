=============

# BulletPoints


Class `dsart.BulletPoints` is used for drawing bullet points.


```drawlib 600px center
from drawlib.canvas import config, save
from drawlib.lines import line
from drawlib.smartarts import BulletPoints, dsart
from drawlib.text import text

config(width=100, height=50, grid=True)


def center():
    bp = dsart.BulletPoints(vertical_margin=4, indent_width=4)
    bp.add("Type of Drawlib shapes")
    bp.set_indent(1)
    bp.add("Circle Like Shapes")
    bp.set_indent(2)
    bp.add("Circle")
    bp.add("Start etc.")
    bp.set_indent(1)
    bp.add("Rectangle Like Shapes")
    bp.set_indent(2)
    bp.add("Rectangle")
    bp.add("Ellipse etc.")
    bp.draw(xy=(42, 40))


def left():
    x1 = 17
    x2 = 27
    x3 = 37

    text((x1, 40), "Indent Level 0", style="light")
    line((x2, 40), (x3, 40), style="dashed_light", arrowhead="->")
    text((x1, 36), "Indent Level 1", style="light")
    line((x2, 36), (x3, 36), style="dashed_light", arrowhead="->")
    text((x1, 32), "Indent Level 2", style="light")
    line((x2, 32), (x3, 32), style="dashed_light", arrowhead="->")

    line((x2, 21), (42, 24), style="dashed_light", arrowhead="->")
    line((x2, 19), (46, 16), style="dashed_light", arrowhead="->")
    text((x1, 20), "indent_style", style="light")


def others():
    line((70, 40), (70, 36), style="dashed_light", arrowhead="<->")
    text((82, 38), "vertical_margin", style="light")
    line((42, 12), (46, 12), style="dashed_light", arrowhead="<->")
    text((44, 9), "indent_width", style="light")


center()
left()
others()
save()
```


    image1.png

As you can see, you can control text style and bullet point styles.


# API Specification



## ``dsart.BulletPoints()``


Args:

- vertical_margin (float): The vertical space between bullet points.
- indent_width (float): The width of the indentation for each level.
- default_style (Union[str, Style, None]): The default text style for the bullet points.


## ``set_indent()``


Sets the indentation level for the next bullet point.

Args:

- level (int): The indentation level.


## ``set_bullet_style()``


Sets the style and function for drawing bullets at a specific indentation level.

Args:

- indent_level (int): The indentation level to apply the style to.
- function (Callable): The function to draw the bullet shape.
- style (Union[str, Style]): The style to apply to the bullet shape.
- args (dict): Additional arguments to pass to the drawing function.


## ``add()``


Adds a bullet point with the specified text and style.

Args:

- text (str): The text for the bullet point.
- style (Union[str, Style, None]): The text style for the bullet point.


## ``draw()``


Draws the list of bullet points starting from the specified location.

Args:

xy (Tuple[float, float]): The starting point (x, y) to draw the bullet points.
