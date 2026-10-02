# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Common utilities for CLI visualizers."""

from __future__ import annotations

import os

from drawlib._core.l3_images import Dimage


def display_dimage(dimage: Dimage) -> None:
    """Display Dimage using PIL Image.show() unless disabled by environment.

    Args:
        dimage (Dimage): In-memory image to display.
    """
    if os.environ.get("DRAWLIB_SHOW_NO_DISPLAY") != "1":
        dimage.get_pil_image().show()
