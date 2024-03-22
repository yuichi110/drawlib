import sys as _sys
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
import drawlib._util as _util

if "-v" in _sys.argv or "--version" in _sys.argv:
    print("0.1")
    exit(0)

if "-h" in _sys.argv or "--help" in _sys.argv:
    print("python drawlib. illustration as code.")
    print("options")
    print("  -h:         show help")
    print("  --help:     show help")
    print("  -v:         show version")
    print("  --version:  show version")
    print("  --debug:    show stacktrace(verbose error message)")
    print("  --devdebug: show native error message")
    exit(0)

# escape native help command
__help = help


@_util.error_handler
def help(object, open_webdoc=True):
    """getting help of drawlib
    - function
    - class
    """

    # get module objects
    module_name = (lambda x: x).__module__
    module = _sys.modules[module_name]
    module_objects = set()
    g = globals()
    for object_name in dir(module):
        if object_name.startswith("_"):
            continue
        if object_name == "help":
            continue
        module_objects.add(g[object_name])

    # show document
    if object in module_objects:
        print(object.__doc__)
    else:
        __help(object)
