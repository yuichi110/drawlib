# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

# ruff: noqa: F401, PLC0415

"""Canvas related utilities."""

import drawlib.v0_2.private.util
from drawlib.v0_2.private.util import (
    get_angle,
    get_center_and_size,
    get_distance,
)


@drawlib.v0_2.private.util.error_handler
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

    from drawlib.v0_2.private.core.dimage import Dimage
    from drawlib.v0_2.private.core.theme import dtheme
    from drawlib.v0_2.private.core_canvas.canvas import clear

    clear()
    dtheme.apply_official_theme("default")
    for name in Dimage.cache.list():
        Dimage.cache.delete(name)
