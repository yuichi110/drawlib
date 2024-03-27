"""write docstring later"""

# pylint: disable=redefined-builtin
# pylint: disable=unused-import

import sys
import typing
from drawlib._pil import Pimage
from drawlib._model import (
    TextStyle,
    LineStyle,
    ShapeStyle,
    TextBackgroundStyle,
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

__help = help  # pylint: disable=used-before-assignment


def help(  # pylint: disable=redefined-builtin
    object: typing.Any,
    open_webdoc: bool = True,
) -> None:
    """getting help of drawlib
    - function
    - class
    """

    # get module objects
    module_name = (lambda x: x).__module__
    module = sys.modules[module_name]
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

    print(open_webdoc)
