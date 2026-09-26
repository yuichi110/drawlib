# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Core canvas facade module."""

from drawlib._core.l4_canvas import (
    canvas,
    clear,
    config,
    get_dimage,
    get_image_zoom_from_width,
    get_image_zoom_original,
    save,
    setup,
    show,
)
from drawlib._core.l4_canvas._canvas import Canvas

__all__ = [
    "Canvas",
    "canvas",
    "clear",
    "config",
    "get_dimage",
    "get_image_zoom_from_width",
    "get_image_zoom_original",
    "save",
    "setup",
    "show",
]
