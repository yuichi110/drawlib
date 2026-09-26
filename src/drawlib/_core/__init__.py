# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Drawlib core drawing engine facade.

This module re-exports domain facades of the core drawing engine.
External packages should import from `drawlib._core.<domain>` (e.g. shapes, lines, types, canvas, etc.)
rather than accessing lower-level implementation details directly.
"""

from drawlib._core import (
    canvas,
    colors,
    fonts,
    images,
    lines,
    shapes,
    text,
    types,
    utils,
)

__all__ = [
    "canvas",
    "colors",
    "fonts",
    "images",
    "lines",
    "shapes",
    "text",
    "types",
    "utils",
]
