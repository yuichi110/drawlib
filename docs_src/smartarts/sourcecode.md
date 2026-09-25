# SourceCode


Drawing source code with Drawlib can be done simply using the `text()` function with `halign="left"` and a monospace font. 
For more sophisticated source code visuals, including syntax highlighting, Drawlib provides the SourceCode Smart Art feature. 
This feature leverages pygments to generate visually enhanced source code images.

Here is an example of code:


```python
from drawlib.canvas import config
from drawlib.colors import Colors140
from drawlib.fonts import FontSourceCode
from drawlib.shapes import circle
from drawlib.smartarts import SourceCode

CODE = """
from drawlib.canvas import config
from drawlib.shapes import circle

config(width=100, height=100)
circle(xy=(50, 50), radius=30, style="blue_dashed")
""".strip()

config(width=100, height=50)

sc1 = SourceCode(
    language="python",
    style="default",
)
sc1.draw((25, 25), width=40, code=CODE)

sc2 = SourceCode(
    style="monokai",
    font=FontSourceCode.ROBOTO_MONO,
    show_linenum=True,
    linenum_textcolor=Colors140.Black,
    linenum_bgcolor=Colors140.LightGray,
)
sc2.draw((75, 25), width=40, code=CODE, style="red_solid")
```

In the example above, the `SourceCode` instance is configured with options such as:

- `language`: Specifies the programming language (automatically detected if not provided).
- `style`: Defines the syntax highlighting style (e.g., `"monokai"`, `"default"`).
- `font`: Source code font (from `FontSourceCode`).
- `show_linenum`: Determines whether to display line numbers.
- `linenum_textcolor` and `linenum_bgcolor`: Customize the colors of line numbers.

After creating an instance, draw the code using the `draw()` method:

- `xy`: Coordinates `(x, y)` to center the source code block.
- `width`: Width of the source code container.
- `code`: The source code string to render.
- `style`: Container box style (border, background).

Executing the code produces:

```drawlib 600px center
from drawlib.canvas import config
from drawlib.colors import Colors140
from drawlib.fonts import FontSourceCode
from drawlib.shapes import circle
from drawlib.smartarts import SourceCode

CODE = """
from drawlib.canvas import config
from drawlib.shapes import circle

config(width=100, height=100)
circle(xy=(50, 50), radius=30, style="blue_dashed")
""".strip()

config(width=100, height=50)

sc1 = SourceCode(
    language="python",
    style="default",
)
sc1.draw((25, 25), width=40, code=CODE)

sc2 = SourceCode(
    style="monokai",
    font=FontSourceCode.ROBOTO_MONO,
    show_linenum=True,
    linenum_textcolor=Colors140.Black,
    linenum_bgcolor=Colors140.LightGray,
)
sc2.draw((75, 25), width=40, code=CODE, style="red_solid")
```



# Source Code Styles


Drawlib supports a variety of styles from Pygment's recommended list, as well as additional black and white styles. 
Here are list of supported styles:

- bw
- sas
- staroffice
- xcode
- default
- monokai
- lightbulb
- github-dark
- rrt
- algol
- algol_nu
- friendly_grayscale

Here are output of Source Code styles.


```drawlib fold-code 600px center
from drawlib.canvas import config
from drawlib.fonts import FontSourceCode
from drawlib.smartarts import SourceCode
from drawlib.text import text

CODE = """
import math

def example_function(x):
    return x * 2

print(example_function(5))
""".strip()


config(width=100, height=100, dpi=200)
xs = [17.5, 50, 82.5]
ys = [15, 37.5, 62.5, 85]
ix = 0
iy = 0
for style in [
    "bw",
    "sas",
    "staroffice",
    "xcode",
    "default",
    "monokai",
    "lightbulb",
    "github-dark",
    "rrt",
    "algol",
    "algol_nu",
    "friendly_grayscale",
]:
    sc = SourceCode(
        language="python",
        style=style,
        font=FontSourceCode.ROBOTO_MONO,
    )

    x = xs[ix]
    y = ys[iy]
    sc.draw(xy=(x, y), width=25, code=CODE, style="solid")
    text((x, y - 9), text=style)

    if ix == len(xs) - 1:
        ix = 0
        iy += 1
    else:
        ix += 1
```


# get_text()


To retrieve the text content directly from a code file, you can use the `SourceCode.get_text()` method provided by SourceCode. 
This function allows you to specify a file path relative to the code file's location.

---

<p align="center"><em>© 2026 drawlib by Yuichi Ito. Released under the Apache 2.0 License.</em></p>
