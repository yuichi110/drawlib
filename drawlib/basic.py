"""doc of drawlib"""

from drawlib._pil import Pimage
from drawlib._model import (
    TextStyle,
    LineStyle,
    ShapeStyle,
    TextBackgroundStyle,
)
from drawlib._tools import (
    help,
)
from drawlib._canvas import (
    # basics
    clear,
    config,
    save,
    plot,
    title,
    # image
    image,
    # line
    line,
    lines,
    line_bezier,
    # patches
    circle,
    rectangle,
    rectangle_rounded,
    # text
    text,
)
