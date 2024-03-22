import sys
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
from drawlib._state import (
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
from drawlib._pil import Pimage
from drawlib._util import (
    get_angle,
    warning_suppress,
    get_function_name,
)

VERSION = 0.1

if "-v" in sys.argv or "--version" in sys.argv:
    print(VERSION)
    exit(0)

if "-h" in sys.argv or "--help" in sys.argv:
    print("drawlib. illustration as code(python).")
    print("options")
    print("  -h:         show help")
    print("  --help:     show help")
    print("  -v:         show version")
    print("  --version:  show version")
    print("  --debug:    show verbose error message")
    print("  --devdebug: disable error handler. show native error message")
    exit(0)
