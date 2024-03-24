"""doc of drawlib"""

import drawlib._args
from drawlib._core.image import (
    get_image,
)
from drawlib._core.line import (
    get_line,
    get_lines,
    get_line_bezier,
)
from drawlib._core.patches import (
    get_circle,
    get_rectangle,
    get_rectangle_rounded,
)
from drawlib._core.text import (
    get_text,
)
from drawlib._model import (
    TextStyle,
    LineStyle,
    ShapeStyle,
    TextBackgroundStyle,
)
from drawlib._draw import (
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
from drawlib._cache import (
    # line style
    has_cache_linestyle,
    set_cache_linestyle,
    get_cache_linestyle,
    # shape style
    has_cache_shapestyle,
    set_cache_shapestyle,
    get_cache_shapestyle,
    # text style
    has_cache_textstyle,
    set_cache_textstyle,
    get_cache_textstyle,
    # text background style
    has_cache_textbackgroundstyle,
    set_cache_textbackgroundstyle,
    get_cache_textbackgroundstyle,
    # pimage
    has_cache_image,
    set_cache_image,
    get_cache_image,
)
from drawlib._pil import Pimage
from drawlib._util import (
    run,
    help,
    get_angle,
    get_script_relative_path,
)
from drawlib import debug
