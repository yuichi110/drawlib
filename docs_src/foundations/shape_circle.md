# Drawing Circle Like Shapes



## Circle-like Shapes


Functions that draw circle-like shapes include:

* `circle()`
* `donuts()`
* `fan()`
* `regularpolygon()`
* `star()`
* `wedge()`

Circle-like shapes specify `xy`, `radius`, and other shape-specific arguments.


## circle()


The `circle()` function draws a circle and takes the following arguments:

* xy : X, Y coordinates.
* radius: Radius of the circle.
* angle: Angle which affects the text inside the circle.
* style: Style of the circle.
* text: Text displayed at the center of the circle.
* textsize: The font size of the text.
* textstyle: The style of the center text

Let's explore two examples.


```python
from drawlib.canvas import config, save
from drawlib.preset_styles import get_styles
from drawlib.shapes import circle
from drawlib.text import text

styles = get_styles()
config(width=100, height=50, grid_only=True)
circle(xy=(25, 25), radius=15, style=styles.primary)
circle(xy=(75, 25), radius=20, angle=45, text="circle", style=styles.primary)
save()
```

The circle shape itself does not have an angle effect, but the text inside does.

Executing the above script generates the following output:


```drawlib 600px center
from drawlib.canvas import config, save
from drawlib.shapes import circle
from drawlib.text import text

config(width=100, height=50, grid_only=True)
circle(xy=(25, 25), radius=15, style=styles.primary)
circle(xy=(75, 25), radius=20, angle=45, text="circle", style=styles.primary)
save()
```


    circle()


## donuts()


The `donuts()` function draws a donut-like shape. 
This shape is defined by an external radius and the width of the filled area, meaning the internal radius is calculated as `external radius - width`.

This function takes these arguments.

* xy : X, Y coordinates.
* radius: Radius of the donuts.
* width: Width of donuts fill area
* angle: Angle which affects the text inside the donuts.
* style: Style of the donuts.
* text: Text displayed at the center of the donuts.
* textsize: The font size of the text.
* textstyle: The style of the center text

Let's explore two examples.


```python
from drawlib.canvas import config, save
from drawlib.preset_styles import get_styles
from drawlib.shapes import donuts
from drawlib.text import text

styles = get_styles()
config(width=100, height=50, grid_only=True)
donuts(xy=(25, 25), radius=15, width=5, style=styles.primary)
donuts(xy=(75, 25), radius=20, width=10, angle=45, text="donuts", style=styles.primary)
save()
```

By adjusting the `radius` and `width` arguments, you can control the size and thickness of the donut shape.
Executing the above script generates donut shapes with centered text, showing the usage of various arguments.


```drawlib 600px center
from drawlib.canvas import config, save
from drawlib.shapes import donuts
from drawlib.text import text

config(width=100, height=50, grid_only=True)
donuts(xy=(25, 25), radius=15, width=5, style=styles.primary)
donuts(xy=(75, 25), radius=20, width=10, angle=45, text="donuts", style=styles.primary)
save()
```


   donuts()

The `donuts()` function is essentially a simplified wrapper around the `wedge()` function, providing an easy way to draw donut shapes without needing to handle the internal radius calculations manually.



## fan()


The `fan()` function draws a fan shape, which is a sector of a circle. In other words, it creates a part of a circle from one angle to another.

* xy : X, Y coordinates.
* radius: Radius of the fan.
* from_angle: The starting angle of the fan.
* to_angle: The ending angle of the fan.
* angle: Angle of the fan.
* style: Style of the fan.
* text: Text displayed at the center of the fan.
* textsize: The font size of the text.
* textstyle: The style of the center text

There are three angle-related arguments:

* `from_angle`: Defines where the fan shape starts.
* `to_angle`: Defines where the fan shape ends.
* `angle`: Rotates the entire fan shape after it is created.

Let's explore two examples.


```python
from drawlib.canvas import config, save
from drawlib.preset_styles import get_styles
from drawlib.shapes import fan
from drawlib.text import text

styles = get_styles()
config(width=100, height=50, grid_only=True)
fan(xy=(25, 25), radius=15, angle_start=0, angle_end=135, style=styles.primary)
fan(
    xy=(75, 25),
    radius=20,
    angle_start=0,
    angle_end=135,
    angle=45,
    text="fan",
    style=styles.primary,
)
save()
```

By adjusting the from_angle, to_angle, and angle arguments, you can create and position the fan shape as desired.

First example draws fan from angle(`from_angle`) 0 to angle(`to_angle`) 135.
Second example is same, but it rotate fan via specifying `angle`. 

Executing the above script generates fan shapes with centered text, showing the usage of various arguments.


```drawlib 600px center
from drawlib.canvas import config, save
from drawlib.shapes import fan
from drawlib.text import text

config(width=100, height=50, grid_only=True)
fan(xy=(25, 25), radius=15, angle_start=0, angle_end=135, style=styles.primary)
fan(
    xy=(75, 25),
    radius=20,
    angle_start=0,
    angle_end=135,
    angle=45,
    text="fan",
    style=styles.primary,
)
save()
```


    fan()

The `fan()` function is essentially a simplified wrapper around the `wedge()` function, making it easy to draw fan shapes by specifying start and end angles, and then optionally rotating the shape.


## regularpolygon()


The `regularpolygon()` function draws a regular polygon with a specified number of vertices.

This function takes these arguments.

* xy : X, Y coordinates.
* radius: Radius of the regularpolygon.
* num_vertices: Number of vertices of the polygon (must be 3 or more).
* angle: Angle of the regularpolygon.
* style: Style of the regularpolygon.
* text: Text displayed at the center of the regularpolygon.
* textsize: The font size of the text.
* textstyle: The style of the center text

Here are two examples demonstrating the use of `regularpolygon()`:


```python
from drawlib.canvas import config, save
from drawlib.preset_styles import get_styles
from drawlib.shapes import polygon, regularpolygon
from drawlib.text import text

styles = get_styles()
config(width=100, height=50, grid_only=True)
regularpolygon(xy=(25, 25), radius=15, num_vertex=5, style=styles.primary)
regularpolygon(xy=(75, 25), radius=20, num_vertex=6, angle=45, text="regular polygon", style=styles.primary)
save()
```

Executing the above script generates regular polygons with centered text, demonstrating the usage of various arguments.


```drawlib 600px center
from drawlib.canvas import config, save
from drawlib.shapes import polygon, regularpolygon
from drawlib.text import text

config(width=100, height=50, grid_only=True)
regularpolygon(xy=(25, 25), radius=15, num_vertex=5, style=styles.primary)
regularpolygon(xy=(75, 25), radius=20, num_vertex=6, angle=45, text="regular polygon", style=styles.primary)
save()
```


    regularpolygon()

The `regularpolygon()` function allows you to specify the number of vertices from 3 upwards to create polygons of various shapes.



## star()


The `star()` function draws a star shape with a specified number of external vertices.

This function takes these arguments.

* xy : X, Y coordinates.
* radius_ext: Radius of the circle circumscribing the outermost vertices of the star.
* radius_int: Radius of the circle circumscribing the innermost vertices of the star.
* num_vertices: Number of external vertices of the star (must be 3 or more).
* angle: Angle of the star.
* style: Style of the star.
* text: Text displayed at the center of the star.
* textsize: The font size of the text.
* textstyle: The style of the center text

Here are two examples demonstrating the use of `star()`:


```python
from drawlib.canvas import config, save
from drawlib.preset_styles import get_styles
from drawlib.shapes import star
from drawlib.text import text

styles = get_styles()
config(width=100, height=50, grid_only=True)
star(xy=(25, 25), num_vertex=5, radius_ext=15, radius_int=5, style=styles.primary)
star(xy=(75, 25), num_vertex=9, radius_ext=20, radius_int=7.5, angle=45, text="star", style=styles.primary)
save()
```

The `star()` function allows you to specify the number of external vertices to create stars of different shapes and sizes.
Executing the above script generates stars with centered text, demonstrating the usage of various arguments.


```drawlib 600px center
from drawlib.canvas import config, save
from drawlib.shapes import star
from drawlib.text import text

config(width=100, height=50, grid_only=True)
star(xy=(25, 25), num_vertex=5, radius_ext=15, radius_int=5, style=styles.primary)
star(xy=(75, 25), num_vertex=9, radius_ext=20, radius_int=7.5, angle=45, text="star", style=styles.primary)
save()
```


    star()


## wedge()


The `wedge()` function draws a wedge shape, which is a combination of a donut (ring) and a fan (sector of a circle).

This function takes these arguments.

* xy : X, Y coordinates.
* radius: Radius of the wedge.
* width : width of donuts fill area
* from_angle: Starting angle of the wedge.
* to_angle: Ending angle of the wedge.
* angle: Angle of the wedge.
* style: Style of the wedge.
* text: Text displayed at the center of the wedge.
* textsize: The font size of the text.
* textstyle: The style of the center text

Here is an example demonstrating the use of `wedge()`:


```python
from drawlib.canvas import config, save
from drawlib.preset_styles import get_styles
from drawlib.shapes import wedge
from drawlib.text import text

styles = get_styles()
config(width=100, height=50, grid_only=True)
wedge(xy=(25, 25), radius=15, width=5, angle_start=0, angle_end=135, style=styles.primary)
wedge(
    xy=(75, 25),
    radius=20,
    width=10,
    angle_start=0,
    angle_end=135,
    angle=45,
    text="wedge",
    style=styles.primary,
)
save()
```

Executing the above script generates a wedge shape with centered text, demonstrating the usage of various arguments.


```drawlib 600px center
from drawlib.canvas import config, save
from drawlib.shapes import wedge
from drawlib.text import text

config(width=100, height=50, grid_only=True)
wedge(xy=(25, 25), radius=15, width=5, angle_start=0, angle_end=135, style=styles.primary)
wedge(
    xy=(75, 25),
    radius=20,
    width=10,
    angle_start=0,
    angle_end=135,
    angle=45,
    text="wedge",
    style=styles.primary,
)
save()
```


    wedge()

The `wedge()` function allows you to specify the radius, width, starting angle, and ending angle to create wedge shapes, which are useful for visualizing segments of circles with customizable styles and text.

---

<p align="center"><em>© 2026 drawlib by Yuichi Ito. Released under the Apache 2.0 License.</em></p>
