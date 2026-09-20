# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

# ruff: noqa: PLC0415

"""Canvas related utilities."""

from drawlib._core.l1_core import guarded
from drawlib._core.l4_canvas import clear
from drawlib._core.l4_canvas_utils import (
    get_angle,
    get_center_and_size,
    get_distance,
)


@guarded
def initialize() -> None:
    """Initialize the drawing environment by clearing the drawing canvas.

    Returns:
        None

    """
    clear()


__all__ = [
    "get_angle",
    "get_center_and_size",
    "get_distance",
    "initialize",
]
