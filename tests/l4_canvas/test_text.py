# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for CanvasTextFeature text layouts."""

import os

from drawlib.canvas import clear, save
from drawlib.colors import Colors
from drawlib.fonts import FontFile
from drawlib.preset_styles import default_styles
from drawlib.text import text, text_vertical

# ruff: noqa: F403, F405

FONT_AVENGER = os.path.normpath(os.path.join(os.path.dirname(__file__), "../assets/avenger/regular.ttf"))
FONT_MPLUS1P = os.path.normpath(os.path.join(os.path.dirname(__file__), "../assets/mplus1p/regular.ttf"))
OUTPUT_DIR = "../../output_tests/l4_canvas/text/"


class TestCanvasText:
    """Tests for the CanvasTextFeature class, including horizontal and vertical text styles."""

    def test_text(self) -> None:
        """Verify horizontal text rendering, size overrides, background blocks, and custom fonts."""
        clear()
        styles = default_styles
        s_def = styles.primary

        # Simple text
        text((30, 30), "Hello World", style=s_def)

        # Size settings & overrides
        text((30, 30), "Hello World", style=s_def.patch(text_size=12))
        text((30, 30), "Hello World", size=36, style=s_def.patch(text_size=12))

        # Background bounding box settings
        text(
            (30, 30),
            "Hello World",
            angle=90,
            style=s_def.patch(
                text_bg_line_color=Colors.Blue,
                text_bg_fill_color=Colors.Yellow,
                text_bg_line_style="dotted",
                text_bg_line_width=2,
            ),
        )

        # Custom TTF fonts
        text(
            (20, 30),
            "Hello World. あいうえお",
            style=s_def.patch(text_font=FontFile(FONT_MPLUS1P)),
        )
        text(
            (20, 70),
            "Hello World. あいうえお",
            style=s_def.patch(text_font=FontFile(FONT_AVENGER)),
        )

        save(f"{OUTPUT_DIR}test_text.png")

    def test_text_vertical(self) -> None:
        """Verify vertical text layout rendering with custom fonts, sizes, and borders."""
        clear()
        styles = default_styles
        s_def = styles.primary

        # Standard vertical text
        text_vertical((30, 30), "Hello World. あいうえお", style=s_def)

        # Custom sizes
        text_vertical((30, 30), "Hello World", style=s_def.patch(text_size=12))

        # Bounding box & angles
        text_vertical(
            (30, 30),
            "Hello World",
            angle=90,
            style=s_def.patch(
                text_bg_line_color=Colors.Blue,
                text_bg_fill_color=Colors.Yellow,
                text_bg_line_style="dotted",
                text_bg_line_width=2,
            ),
        )

        # Custom TTF fonts in vertical mode
        text_vertical(
            (20, 30),
            "Hello World. あいうえお",
            style=s_def.patch(text_font=FontFile(FONT_MPLUS1P)),
        )
        text_vertical(
            (50, 30),
            "Hello World. あいうえお",
            style=s_def.patch(text_font=FontFile(FONT_AVENGER)),
        )

        save(f"{OUTPUT_DIR}test_text_vertical.png")
