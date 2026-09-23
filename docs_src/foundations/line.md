# Drawing line


Drawlib provides six functions for drawing lines:

* `line()`
* `line_curve()`
* `line_bezier1()`
* `line_bezier2()`
* `lines()`
* `lines_bezier()`

We will explain each of these functions in detail. 
They all share the following optional arguments:

- `arrowhead`: Specifies the type of arrowhead. Options are `["", "->", "<-", "<->"]`.
- `width`: Specifies the line width. This should typically be configured within the style, but it is also available as an optional argument.
- `style`: Defines the line style. Accepts a Style object or a string (style name).

Details on these options will be covered in the next section on line styles (see the following page).


# line()


The `line()` function is the most basic function for drawing lines. 
It requires two mandatory arguments and accepts three optional arguments.

* xy1: The start point of the line
* xy2: The end point of the line
* (optional) arrowhead: Specifies the type of arrow head
* (optional) width: The width of the line
* (optional) style: The style of the line

Let's look at an example:


```drawlib
from drawlib.canvas import config, save
from drawlib.lines import line

config(width=100, height=50)
line(xy1=(10, 10), xy2=(90, 40))
save()
```

In this example, we draw a line from (10, 10) to (90, 40) without specifying a style. 
This generates the following output:


```drawlib 600px center
from drawlib.canvas import config, save
from drawlib.lines import line

config(width=100, height=50)
line(xy1=(10, 10), xy2=(90, 40))
save()
```


    straight line from xy1 to xy2



# line_curved()


The `line_curved()` function makes it easy to draw curved lines. 
While `line_bezier1()` and `line_bezier2()` can also draw curved lines, they require more complex curve control compared to `line_curved()`.

It requires three mandatory arguments and accepts three optional arguments.

* xy1: The start point of the line
* xy2: The end point of the line
* bend: The additional length beyond a direct connection, controlling the curvature.
* (optional) arrowhead: Specifies the type of arrow head
* (optional) width: The width of the line
* (optional) style: The style of the line

For example, suppose xy1 is (10, 10) and xy2 is (10, 20). 
The distance between these points is 10 units.

- When `bend` is set to 0.2, the line is drawn from (10, 10) to (10, 20) with a length of 12 units (10 x 1.2).
- When `bend` is set to 0.4, the length is 14 units (10 x 1.4).

Negative values can also be used for bend, which maintains the length but reverses the bending direction. 
Let's check some examples:


```drawlib
from drawlib.canvas import config, save
from drawlib.lines import line_curved
from drawlib.text import text

config(width=100, height=50)
line_curved(xy1=(10, 20), xy2=(90, 20), bend=0.4)
text((50, 7), "0.4")
line_curved(xy1=(10, 23), xy2=(90, 23), bend=0.2)
text((50, 18), "0.2")
line_curved(xy1=(10, 27), xy2=(90, 27), bend=-0.2)
text((50, 32), "-0.2")
line_curved(xy1=(10, 30), xy2=(90, 30), bend=-0.4)
text((50, 43), "-0.4")
save()
```

This code generates the following output:


```drawlib 600px center
from drawlib.canvas import config, save
from drawlib.lines import line_curved
from drawlib.text import text

config(width=100, height=50)
line_curved(xy1=(10, 20), xy2=(90, 20), bend=0.4)
text((50, 7), "0.4")
line_curved(xy1=(10, 23), xy2=(90, 23), bend=0.2)
text((50, 18), "0.2")
line_curved(xy1=(10, 27), xy2=(90, 27), bend=-0.2)
text((50, 32), "-0.2")
line_curved(xy1=(10, 30), xy2=(90, 30), bend=-0.4)
text((50, 43), "-0.4")
save()
```


    curved line from xy1 to xy2



# line_bezier1()


The `line_bezier1()` function draws a Bézier curve with one control point. 
It requires three mandatory arguments and accepts three optional arguments.

* xy1: The start point of the line
* cp: The Bézier control point.
* xy2: The end point of the line
* bend: The additional length beyond a direct connection, controlling the curvature.
* (optional) arrowhead: Specifies the type of arrow head
* (optional) width: The width of the line
* (optional) style: The style of the line

Bézier curves are a popular method for drawing smooth, curved lines. 
If you are not familiar with Bézier curves, it is recommended to research and understand the concept first. 

This code generates the following output:


```drawlib
from drawlib.canvas import config, save
from drawlib.colors import Colors
from drawlib.lines import line, line_bezier1
from drawlib.shapes import circle
from drawlib.types import Style

config(width=100, height=50)
line_bezier1(xy1=(10, 10), cp=(10, 40), xy2=(40, 40))
line(xy1=(10, 10), xy2=(10, 40), style=Style(line_style="dashed", line_color=Colors.Red))
line(xy1=(10, 40), xy2=(40, 40), style=Style(line_style="dashed", line_color=Colors.Red))
circle(xy=(10, 10), radius=0.5, style=Style(fill_color=Colors.White, line_color=Colors.Red))
circle(xy=(10, 40), radius=0.5, style=Style(fill_color=Colors.White, line_color=Colors.Red))
circle(xy=(40, 40), radius=0.5, style=Style(fill_color=Colors.White, line_color=Colors.Red))

line_bezier1(xy1=(60, 40), cp=(90, 40), xy2=(90, 10))
line(xy1=(60, 40), xy2=(90, 40), style=Style(line_style="dashed", line_color=Colors.Red))
line(xy1=(90, 40), xy2=(90, 10), style=Style(line_style="dashed", line_color=Colors.Red))
circle(xy=(60, 40), radius=0.5, style=Style(fill_color=Colors.White, line_color=Colors.Red))
circle(xy=(90, 40), radius=0.5, style=Style(fill_color=Colors.White, line_color=Colors.Red))
circle(xy=(90, 10), radius=0.5, style=Style(fill_color=Colors.White, line_color=Colors.Red))

save()
```

It generate this output.


```drawlib 600px center
from drawlib.canvas import config, save
from drawlib.colors import Colors
from drawlib.lines import line, line_bezier1
from drawlib.shapes import circle
from drawlib.types import Style

config(width=100, height=50)
line_bezier1(xy1=(10, 10), cp=(10, 40), xy2=(40, 40))
line(xy1=(10, 10), xy2=(10, 40), style=Style(line_style="dashed", line_color=Colors.Red))
line(xy1=(10, 40), xy2=(40, 40), style=Style(line_style="dashed", line_color=Colors.Red))
circle(xy=(10, 10), radius=0.5, style=Style(fill_color=Colors.White, line_color=Colors.Red))
circle(xy=(10, 40), radius=0.5, style=Style(fill_color=Colors.White, line_color=Colors.Red))
circle(xy=(40, 40), radius=0.5, style=Style(fill_color=Colors.White, line_color=Colors.Red))

line_bezier1(xy1=(60, 40), cp=(90, 40), xy2=(90, 10))
line(xy1=(60, 40), xy2=(90, 40), style=Style(line_style="dashed", line_color=Colors.Red))
line(xy1=(90, 40), xy2=(90, 10), style=Style(line_style="dashed", line_color=Colors.Red))
circle(xy=(60, 40), radius=0.5, style=Style(fill_color=Colors.White, line_color=Colors.Red))
circle(xy=(90, 40), radius=0.5, style=Style(fill_color=Colors.White, line_color=Colors.Red))
circle(xy=(90, 10), radius=0.5, style=Style(fill_color=Colors.White, line_color=Colors.Red))

save()
```


    Bézier curves from xy1 to xy2


# line_bezier2()


The `line_bezier2()` function draws a Bézier curve with two control points. 
It requires four mandatory arguments and accepts three optional arguments.

* xy1: The start point of the line
* cp1: The first Bézier control point.
* cp2: The seconde Bézier control point.
* xy2: The end point of the line
* bend: The additional length beyond a direct connection, controlling the curvature.
* (optional) arrowhead: Specifies the type of arrow head
* (optional) width: The width of the line
* (optional) style: The style of the line

Drawing a Bézier curve with two control points is a popular method for creating smooth, curved lines. 
If you are not familiar with Bézier curves, it is recommended to research and understand the concept first.

Here is an example code:


```drawlib
from drawlib.canvas import config, save
from drawlib.colors import Colors
from drawlib.lines import line, line_bezier2
from drawlib.shapes import circle
from drawlib.types import Style

config(width=100, height=50)
line_bezier2(xy1=(10, 10), cp1=(10, 40), cp2=(40, 40), xy2=(40, 10))
line(xy1=(10, 10), xy2=(10, 40), style=Style(line_style="dashed", line_color=Colors.Red))
line(xy1=(10, 40), xy2=(40, 40), style=Style(line_style="dashed", line_color=Colors.Red))
line(xy1=(40, 40), xy2=(40, 10), style=Style(line_style="dashed", line_color=Colors.Red))
circle(xy=(10, 10), radius=0.5, style=Style(fill_color=Colors.White, line_color=Colors.Red))
circle(xy=(10, 40), radius=0.5, style=Style(fill_color=Colors.White, line_color=Colors.Red))
circle(xy=(40, 40), radius=0.5, style=Style(fill_color=Colors.White, line_color=Colors.Red))
circle(xy=(40, 10), radius=0.5, style=Style(fill_color=Colors.White, line_color=Colors.Red))

line_bezier2(xy1=(60, 40), cp1=(60, 10), cp2=(90, 10), xy2=(90, 40))
line(xy1=(60, 40), xy2=(60, 10), style=Style(line_style="dashed", line_color=Colors.Red))
line(xy1=(60, 10), xy2=(90, 10), style=Style(line_style="dashed", line_color=Colors.Red))
line(xy1=(90, 10), xy2=(90, 40), style=Style(line_style="dashed", line_color=Colors.Red))
circle(xy=(60, 40), radius=0.5, style=Style(fill_color=Colors.White, line_color=Colors.Red))
circle(xy=(60, 10), radius=0.5, style=Style(fill_color=Colors.White, line_color=Colors.Red))
circle(xy=(90, 10), radius=0.5, style=Style(fill_color=Colors.White, line_color=Colors.Red))
circle(xy=(90, 40), radius=0.5, style=Style(fill_color=Colors.White, line_color=Colors.Red))

save()
```

Executing this code generates the following output:


```drawlib 600px center
from drawlib.canvas import config, save
from drawlib.colors import Colors
from drawlib.lines import line, line_bezier2
from drawlib.shapes import circle
from drawlib.types import Style

config(width=100, height=50)
line_bezier2(xy1=(10, 10), cp1=(10, 40), cp2=(40, 40), xy2=(40, 10))
line(xy1=(10, 10), xy2=(10, 40), style=Style(line_style="dashed", line_color=Colors.Red))
line(xy1=(10, 40), xy2=(40, 40), style=Style(line_style="dashed", line_color=Colors.Red))
line(xy1=(40, 40), xy2=(40, 10), style=Style(line_style="dashed", line_color=Colors.Red))
circle(xy=(10, 10), radius=0.5, style=Style(fill_color=Colors.White, line_color=Colors.Red))
circle(xy=(10, 40), radius=0.5, style=Style(fill_color=Colors.White, line_color=Colors.Red))
circle(xy=(40, 40), radius=0.5, style=Style(fill_color=Colors.White, line_color=Colors.Red))
circle(xy=(40, 10), radius=0.5, style=Style(fill_color=Colors.White, line_color=Colors.Red))

line_bezier2(xy1=(60, 40), cp1=(60, 10), cp2=(90, 10), xy2=(90, 40))
line(xy1=(60, 40), xy2=(60, 10), style=Style(line_style="dashed", line_color=Colors.Red))
line(xy1=(60, 10), xy2=(90, 10), style=Style(line_style="dashed", line_color=Colors.Red))
line(xy1=(90, 10), xy2=(90, 40), style=Style(line_style="dashed", line_color=Colors.Red))
circle(xy=(60, 40), radius=0.5, style=Style(fill_color=Colors.White, line_color=Colors.Red))
circle(xy=(60, 10), radius=0.5, style=Style(fill_color=Colors.White, line_color=Colors.Red))
circle(xy=(90, 10), radius=0.5, style=Style(fill_color=Colors.White, line_color=Colors.Red))
circle(xy=(90, 40), radius=0.5, style=Style(fill_color=Colors.White, line_color=Colors.Red))

save()
```


    Bézier curves from xy1 to xy2


# line_arc()


The `line_arc()` function draws a line on the ellipse arc. If the width and height of the ellipse are same, line will be drawn on circle arc.



# lines()


The `lines()` function draws a line that passes through a series of provided points
It requires one mandatory arguments and accepts three optional arguments.

* xys: A list of (x, y) tuples representing the points the line should pass through.
* (optional) arrowhead: Specifies the type of arrow head
* (optional) width: The width of the line
* (optional) style: The style of the line

The `xys` argument differs from the previous functions, but it is simply a list of (x, y) coordinates, such as `[(10, 10), (20, 40), (30, 10), (40, 40)]`.

Here is an example code:


```drawlib
from drawlib.canvas import config, save
from drawlib.lines import lines

config(width=100, height=50)
lines(
    xys=[
        (10, 10),
        (10, 20),
        (40, 30),
        (40, 40),
        (60, 40),
        (90, 10),
    ]
)
save()
```

It generate this output.


```drawlib 600px center
from drawlib.canvas import config, save
from drawlib.lines import lines

config(width=100, height=50)
lines(
    xys=[
        (10, 10),
        (10, 20),
        (40, 30),
        (40, 40),
        (60, 40),
        (90, 10),
    ]
)
save()
```


    lines which passes list of xy


# lines_bezier()


The `lines_bezier()` function is similar to `lines()`, but it can draw multiple straight lines, 
Bézier curves with one control point (bezier1), or Bézier curves with two control points (bezier2) from point to point. 

It takes two mandatory arguments and three optional arguments.

* xy: The starting point.
* path_points: A list of tuples defining the path.
* (optional) arrowhead: Specifies the type of arrow head
* (optional) width: The width of the line
* (optional) style: The style of the line

The `path_points` argument can be complex, as it accepts three types of tuples:

* (x, y): Draws a straight line from the last point to (x, y).
* ((cp_x, cp_y), (x, y)): Draws a bezier1 line from the last point to (x, y) with one control point (cp_x, cp_y).
* ((cp1_x, cp1_y), (cp2_x, cp2_y), (x, y)): Draws a bezier2 line from the last point to (x, y) with two control points (cp1_x, cp1_y) and (cp2_x, cp2_y).

Element of `path_points` are very similar to the previous functions line(), line_bezier1(), and line_bezier2(). 
We set almost the same arguments for elements of the path_points.

Let's see how it works with an example:


```drawlib
from drawlib.canvas import config, save
from drawlib.colors import Colors
from drawlib.lines import line, lines_bezier
from drawlib.shapes import circle
from drawlib.types import Style

config(width=100, height=50)

points = [
    ((10, 20), (30, 20)),
    (60, 10),
    ((60, 40), (90, 40), (90, 10)),
]
lines_bezier(xy=(10, 40), path_points=points)

# bezier1 help line
line(xy1=(10, 40), xy2=(10, 20), style=Style(line_style="dashed", line_color=Colors.Red))
line(xy1=(10, 20), xy2=(30, 20), style=Style(line_style="dashed", line_color=Colors.Red))
circle(xy=(10, 40), radius=0.5, style=Style(fill_color=Colors.White, line_color=Colors.Red))
circle(xy=(10, 20), radius=0.5, style=Style(fill_color=Colors.White, line_color=Colors.Red))
circle(xy=(30, 20), radius=0.5, style=Style(fill_color=Colors.White, line_color=Colors.Red))

# bezier2 help line
line(xy1=(60, 10), xy2=(60, 40), style=Style(line_style="dashed", line_color=Colors.Red))
line(xy1=(60, 40), xy2=(90, 40), style=Style(line_style="dashed", line_color=Colors.Red))
line(xy1=(90, 40), xy2=(90, 10), style=Style(line_style="dashed", line_color=Colors.Red))
circle(xy=(60, 10), radius=0.5, style=Style(fill_color=Colors.White, line_color=Colors.Red))
circle(xy=(60, 40), radius=0.5, style=Style(fill_color=Colors.White, line_color=Colors.Red))
circle(xy=(90, 40), radius=0.5, style=Style(fill_color=Colors.White, line_color=Colors.Red))
circle(xy=(90, 10), radius=0.5, style=Style(fill_color=Colors.White, line_color=Colors.Red))

save()
```

In this example, we use all three types of tuples as elements of path_points. 
They will create a straight line, a bezier1 line, and a bezier2 line. 

Executing this code generates the following output:


```drawlib 600px center
from drawlib.canvas import config, save
from drawlib.colors import Colors
from drawlib.lines import line, lines_bezier
from drawlib.shapes import circle
from drawlib.types import Style

config(width=100, height=50)

points = [
    ((10, 20), (30, 20)),
    (60, 10),
    ((60, 40), (90, 40), (90, 10)),
]
lines_bezier(xy=(10, 40), path_points=points)

# bezier1 help line
line(xy1=(10, 40), xy2=(10, 20), style=Style(line_style="dashed", line_color=Colors.Red))
line(xy1=(10, 20), xy2=(30, 20), style=Style(line_style="dashed", line_color=Colors.Red))
circle(xy=(10, 40), radius=0.5, style=Style(fill_color=Colors.White, line_color=Colors.Red))
circle(xy=(10, 20), radius=0.5, style=Style(fill_color=Colors.White, line_color=Colors.Red))
circle(xy=(30, 20), radius=0.5, style=Style(fill_color=Colors.White, line_color=Colors.Red))

# bezier2 help line
line(xy1=(60, 10), xy2=(60, 40), style=Style(line_style="dashed", line_color=Colors.Red))
line(xy1=(60, 40), xy2=(90, 40), style=Style(line_style="dashed", line_color=Colors.Red))
line(xy1=(90, 40), xy2=(90, 10), style=Style(line_style="dashed", line_color=Colors.Red))
circle(xy=(60, 10), radius=0.5, style=Style(fill_color=Colors.White, line_color=Colors.Red))
circle(xy=(60, 40), radius=0.5, style=Style(fill_color=Colors.White, line_color=Colors.Red))
circle(xy=(90, 40), radius=0.5, style=Style(fill_color=Colors.White, line_color=Colors.Red))
circle(xy=(90, 10), radius=0.5, style=Style(fill_color=Colors.White, line_color=Colors.Red))

save()
```


    image6.png

This function can be used to draw curved lines from shape to shape like this:


```drawlib 600px center
from drawlib.canvas import config, save
from drawlib.colors import Colors
from drawlib.lines import line, lines_bezier
from drawlib.shapes import circle
from drawlib.types import Style

config(width=100, height=50)

circle((10, 40), radius=5)
lines_bezier(
    (20, 40),
    path_points=[
        (75, 40),
        ((90, 40), (90, 25)),
        (90, 20),
    ],
    arrowhead="->",
)
circle((90, 10), radius=5)

# bezier1 help line
line(xy1=(75, 40), xy2=(90, 40), style=Style(line_style="dashed", line_color=Colors.Red))
line(xy1=(90, 40), xy2=(90, 25), style=Style(line_style="dashed", line_color=Colors.Red))
circle(xy=(75, 40), radius=0.5, style=Style(fill_color=Colors.White, line_color=Colors.Red))
circle(xy=(90, 40), radius=0.5, style=Style(fill_color=Colors.White, line_color=Colors.Red))
circle(xy=(90, 25), radius=0.5, style=Style(fill_color=Colors.White, line_color=Colors.Red))

save()
```


    image7.png

For precise control, use this function. 
However, if you want to draw a simple curved line, we recommend using `lines_curved()` instead.



# lines_curved()


The `lines_curved()` function is a simplified syntax for `lines_bezier()`.

From an argument perspective, this function is almost the same as `lines()`, but it includes an additional argument `r` which specifies the length of the curve.
This automatically applies a bezier1 curve effect to lines with the specified length `r`. 
If you want to add related curves to all vertices, this function is very useful.

It takes two mandatory arguments and three optional arguments.

* xys: A list of (x, y) tuples representing the points the line should pass through.
* r: The length of the curve.
* (optional) arrowhead: Specifies the type of arrow head
* (optional) width: The width of the line
* (optional) style: The style of the line

Here is an example code:


```drawlib
from drawlib.canvas import config, save
from drawlib.colors import Colors
from drawlib.lines import lines, lines_curved
from drawlib.shapes import circle
from drawlib.types import Style

config(width=100, height=50)

circle((10, 40), radius=5)
lines(
    [(20, 40), (30, 40), (30, 10), (90, 40), (90, 22)],
    style=Style(line_color=Colors.Red, line_style="dashed", line_width=1.5),
)
lines_curved(
    [(20, 40), (30, 40), (30, 10), (90, 40), (90, 20)],
    r=8,
    width=2.5,
    arrowhead="->",
)
circle((90, 10), radius=5)
save()
```

Executing this code generates the following output:


```drawlib 600px center
from drawlib.canvas import config, save
from drawlib.colors import Colors
from drawlib.lines import lines, lines_curved
from drawlib.shapes import circle
from drawlib.types import Style

config(width=100, height=50)

circle((10, 40), radius=5)
lines(
    [(20, 40), (30, 40), (30, 10), (90, 40), (90, 22)],
    style=Style(line_color=Colors.Red, line_style="dashed", line_width=1.5),
)
lines_curved(
    [(20, 40), (30, 40), (30, 10), (90, 40), (90, 20)],
    r=8,
    width=2.5,
    arrowhead="->",
)
circle((90, 10), radius=5)
save()
```


    lines_curve()

The red dashed support line length is the value of `r`. 
If you set a large value, the curve becomes bigger. 
However, be careful: `r` should be smaller than the distance between points.

---

<p align="center"><em>© 2026 drawlib by Yuichi Ito. Released under the Apache 2.0 License.</em></p>
