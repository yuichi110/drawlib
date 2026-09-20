# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for custom icon drawing."""

import os

from drawlib.canvas import clear, save
from drawlib.colors import Colors
from drawlib.icons import icon
from drawlib.types import Style

FONT_AWESOME_FREE = os.path.normpath(os.path.join(os.path.dirname(__file__), "../assets/fontawesome-free/brands.ttf"))
OUTPUT_DIR = "../../output_tests/l6_icons/icon/"


class TestCanvasIcon:
    """Tests for the custom icon drawing method."""

    def test_icon(self) -> None:
        """Verify custom icon drawing with font path, color, and center alignment."""
        clear()
        icon(
            xy=(50, 50),
            width=20,
            code="\uf1a0",
            file=FONT_AWESOME_FREE,
            style=Style(
                text_color=Colors.Red,
                text_halign="center",
                text_valign="center",
            ),
        )
        save(f"{OUTPUT_DIR}test_icon.png")
