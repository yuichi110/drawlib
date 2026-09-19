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
from drawlib._core.l2_models import Dimage
from drawlib._core.l4_canvas import clear
from drawlib._core.l4_canvas_utils import (
    get_angle,
    get_center_and_size,
    get_distance,
)
from drawlib._theme import get_style


@guarded
def initialize() -> None:
    """Initialize the drawing environment by applying the official theme and clearing the image cache.

    This function performs the following steps:
    1. Clears the drawing canvas.
    2. Applies the official "default" theme using the `dtheme` module.
    3. Deletes all images in the `Dimage` cache.

    Returns:
        None

    """
    #
    # !!! Caution !!!
    # Please import modules here for avoiding exposure useless modules to user
    # Moving this code to "private.util" will make circular import.
    #

    clear()
    for name in Dimage.cache.list():
        Dimage.cache.delete(name)


__all__ = [
    "get_angle",
    "get_center_and_size",
    "get_distance",
    "initialize",
]
