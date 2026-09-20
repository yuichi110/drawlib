===============

# Drawing Icons


If you're looking to enhance your illustrations with icons, drawlib offers several methods to achieve this. 
You can utilize the `image()` function by providing an icon image file of your choice. 
Alternatively, you can use `icon()` along with dedicated `Icon Modules` for drawing icons directly.


# Icon Modules


We've curated a selection of icons for your convenience, available in drawlib now.

* `icon_phosphor`: Derived from Phosphor Icons (https://phosphoricons.com)

Each icon within these modules is defined as a function, allowing you to draw specific icons by simply calling their respective function. 
Let's explore with examples:


```drawlib
from drawlib.canvas import config, save
from drawlib.icons import icon_phosphor
from drawlib.text import text

width = 100
height = 50
config(width=width, height=height)

x = width / 7
y = height / 2
icon_phosphor.airplane_taxiing(xy=(x, y), width=10)
icon_phosphor.airplane_takeoff(xy=(x * 2, y), width=10)
icon_phosphor.airplane_in_flight(xy=(x * 3, y), width=10)
icon_phosphor.airplane_tilt(xy=(x * 4, y), width=10)
icon_phosphor.airplane(xy=(x * 5, y), width=10, angle=270)
text(xy=(x * 5, y - 10), text="angle 270")
icon_phosphor.airplane_landing(xy=(x * 6, y), width=10)

save()
```

All functions have these args.

- `xy` : coordinate
- `width` : icon width
- `angle` : angle 0.0~360.0
- `style` : Accepts string style name or `IconStyle` object.

Executing this code yields the following image:


```drawlib 600px center
from drawlib.canvas import config, save
from drawlib.icons import icon_phosphor
from drawlib.text import text

width = 100
height = 50
config(width=width, height=height)

x = width / 7
y = height / 2
icon_phosphor.airplane_taxiing(xy=(x, y), width=10)
icon_phosphor.airplane_takeoff(xy=(x * 2, y), width=10)
icon_phosphor.airplane_in_flight(xy=(x * 3, y), width=10)
icon_phosphor.airplane_tilt(xy=(x * 4, y), width=10)
icon_phosphor.airplane(xy=(x * 5, y), width=10, angle=270)
text(xy=(x * 5, y - 10), text="angle 270")
icon_phosphor.airplane_landing(xy=(x * 6, y), width=10)

save()
```


    icon_phosphor's icons

You see lots of variation of only airplane.
`icon_phosphor` has around 1500 icons.


# icon()


`icon()` is a versatile function for displaying font icons. 
Internally, icon modules utilize icon().

The function arguments are:

* `xy`: Coordinates for positioning the icon.
* `width`: Width of the icon.
* `code`: Font code representing the icon.
* `file`: Font file used for rendering the icon.
* `angle`: Angle for rotating the icon (optional).
* `style`: Additional style configurations (optional).

Let's explore its usage with FontAwesome Free:


```drawlib
from drawlib.canvas import config, save
from drawlib.icons import icon
from drawlib.text import text

width = 100
height = 50
config(width=width, height=height)

file_brand = "fontawesome-free/brands.ttf"
file_regular = "fontawesome-free/regular.ttf"
file_solid = "fontawesome-free/solid.ttf"

google = "\uf1a0"
gmail = "\uf0e0"
google_map = "\uf3c5"
google_drive = "\uf3aa"
google_play = "\uf3ab"
google_pay = "\ue079"

x = width / 7
y = height / 2
icon(xy=(x, y), width=10, code=google, file=file_brand)
icon(xy=(x * 2, y), width=10, code=gmail, file=file_regular)
icon(xy=(x * 3, y), width=10, code=google_map, file=file_solid, angle=270)
text(xy=(x * 3, y - 10), text="angle 270")
icon(
    xy=(x * 4, y),
    width=10,
    code=google_drive,
    file=file_brand,
)
icon(
    xy=(x * 5, y),
    width=10,
    code=google_play,
    file=file_brand,
)


save()
```

Executing this code generates the following image:


```drawlib 600px center
from drawlib.canvas import config, save
from drawlib.icons import icon
from drawlib.text import text

width = 100
height = 50
config(width=width, height=height)

file_brand = "fontawesome-free/brands.ttf"
file_regular = "fontawesome-free/regular.ttf"
file_solid = "fontawesome-free/solid.ttf"

google = "\uf1a0"
gmail = "\uf0e0"
google_map = "\uf3c5"
google_drive = "\uf3aa"
google_play = "\uf3ab"
google_pay = "\ue079"

x = width / 7
y = height / 2
icon(xy=(x, y), width=10, code=google, file=file_brand)
icon(xy=(x * 2, y), width=10, code=gmail, file=file_regular)
icon(xy=(x * 3, y), width=10, code=google_map, file=file_solid, angle=270)
text(xy=(x * 3, y - 10), text="angle 270")
icon(
    xy=(x * 4, y),
    width=10,
    code=google_drive,
    file=file_brand,
)
icon(
    xy=(x * 5, y),
    width=10,
    code=google_play,
    file=file_brand,
)


save()
```


    FontAwesome-Free icons

While FontAwesome is widely recognized, its full usage requires a commercial license. 
The free version may lack variation and style consistency. 
Therefore, drawlib does not currently provide an icon module for it.



# IconStyle


Similar to other drawing elements, the appearance of icons can be customized using the `IconStyle` class, which allows you to control:

`IconStyle` encompasses these attributes

* `halign`: Horizontal alignment
* `valign`: Vertical alignment
* `style`: Icon style, Supports `"thin"`, `"light"`, `"regular"`, `"bold"`, or `"fill"`. The availability of styles depends on the icon modules.
* `color`: Icon color, specified in RGB (0255, 0255, 0255) or RGBA (0255, 0255, 0255, 0.0~1.0). You can utilize helpers like `Colors` and `Colors140`.
* `alpha`: Icon transparency, ranging from 0.0 to 1.0, where 0.0 represents total transparency.

Let's illustrate this with an example:


```drawlib
from drawlib.canvas import config, save
from drawlib.colors import Colors
from drawlib.icons import icon_phosphor
from drawlib.shapes import circle
from drawlib.text import text
from drawlib.types import IconStyle, ShapeStyle

width = 100
height = 50
config(width=width, height=height)

x = width / 7
y = height / 2
icon_phosphor.airplane_taxiing(xy=(x, y), width=10, style=IconStyle(text_color=Colors.Red))
icon_phosphor.airplane_takeoff(xy=(x * 2, y), width=10, style=IconStyle(icon_style="thin"))
icon_phosphor.airplane_in_flight(xy=(x * 3, y), width=10, style=IconStyle(icon_style="bold"))
icon_phosphor.airplane_tilt(xy=(x * 4, y), width=10, style=IconStyle(icon_style="fill"))
icon_phosphor.airplane(xy=(x * 5, y), width=10, style=IconStyle(text_halign="left", text_valign="bottom"))
circle(xy=(x * 5, y), radius=0.5, style=ShapeStyle(fill_color=Colors.Red, line_color=Colors.Red))
text(xy=(x * 5 + 5, y - 10), text="align left,bottom")

save()
```

Executing this code generates the following image:


```drawlib 600px center
from drawlib.canvas import config, save
from drawlib.colors import Colors
from drawlib.icons import icon_phosphor
from drawlib.shapes import circle
from drawlib.text import text
from drawlib.types import IconStyle, ShapeStyle

width = 100
height = 50
config(width=width, height=height)

x = width / 7
y = height / 2
icon_phosphor.airplane_taxiing(xy=(x, y), width=10, style=IconStyle(text_color=Colors.Red))
icon_phosphor.airplane_takeoff(xy=(x * 2, y), width=10, style=IconStyle(icon_style="thin"))
icon_phosphor.airplane_in_flight(xy=(x * 3, y), width=10, style=IconStyle(icon_style="bold"))
icon_phosphor.airplane_tilt(xy=(x * 4, y), width=10, style=IconStyle(icon_style="fill"))
icon_phosphor.airplane(xy=(x * 5, y), width=10, style=IconStyle(text_halign="left", text_valign="bottom"))
circle(xy=(x * 5, y), radius=0.5, style=ShapeStyle(fill_color=Colors.Red, line_color=Colors.Red))
text(xy=(x * 5 + 5, y - 10), text="align left,bottom")

save()
```


    icons with IconStyle.



# Pre-defined icon styles


Drawlib's theme provides pre-defined icon styles.
You can specify them by names.

Here is an examples.


```drawlib
from drawlib.canvas import config, save
from drawlib.icons import icon_phosphor

width = 100
height = 50
config(width=width, height=height)

x = width / 7
y = height / 2
icon_phosphor.airplane_taxiing(xy=(x, y), width=10, style="green")
icon_phosphor.airplane_takeoff(xy=(x * 2, y), width=10, style="red_light")
icon_phosphor.airplane_in_flight(xy=(x * 3, y), width=10, style="blue_bold")
icon_phosphor.airplane_tilt(xy=(x * 4, y), width=10, style="green_flat")
save()
```

Icon supports the following styles exclusively:

- weight of icon: `light` and `bold`
- fill color: `flat`
- color of icon

Line style solid and dashed are not supported.


```drawlib 600px center
from drawlib.canvas import config, save
from drawlib.icons import icon_phosphor

width = 100
height = 50
config(width=width, height=height)

x = width / 7
y = height / 2
icon_phosphor.airplane_taxiing(xy=(x, y), width=10, style="green")
icon_phosphor.airplane_takeoff(xy=(x * 2, y), width=10, style="red_light")
icon_phosphor.airplane_in_flight(xy=(x * 3, y), width=10, style="blue_bold")
icon_phosphor.airplane_tilt(xy=(x * 4, y), width=10, style="green_flat")
save()
```


    icon with theme's style



