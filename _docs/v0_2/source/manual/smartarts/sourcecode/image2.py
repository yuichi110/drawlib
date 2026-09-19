from drawlib.apis import *

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
    sc = dsart.SourceCode(
        language="python",
        style=style,
        font=FontSourceCode.ROBOTO_MONO,
    )

    x = xs[ix]
    y = ys[iy]
    sc.draw(xy=(x, y), width=25, code=CODE, style=ImageStyle(lwidth=1))
    text((x, y - 9), text=style)

    if ix == len(xs) - 1:
        ix = 0
        iy += 1
    else:
        ix += 1

save()
