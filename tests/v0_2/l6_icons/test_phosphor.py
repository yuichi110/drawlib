# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for Phosphor icons drawing."""

from drawlib.v0_2.apis import (
    Colors,
    IconStyle,
    clear,
    icon_phosphor,
    save,
)

OUTPUT_DIR = "../../../output_tests/v0_2/l6_icons/icon_phosphor/"


class TestCanvasPhosphor:
    """Tests for Phosphor icons drawing support."""

    def test_phosphor_icon_drawing(self) -> None:
        """Verify basic Phosphor icon drawing and styles (fill, thin, bold)."""
        clear()

        # Representative icon: google_logo
        icon_phosphor.google_logo(xy=(50, 50), width=20)
        save(f"{OUTPUT_DIR}test_basic.png")

        clear()
        icon_phosphor.google_logo(
            xy=(50, 50),
            width=20,
            style=IconStyle(style="fill", color=Colors.Red),
        )
        save(f"{OUTPUT_DIR}test_style.png")

    def test_phosphor_icon_angle(self) -> None:
        """Verify Phosphor icon drawing combined with a rotation angle."""
        clear()
        icon_phosphor.google_logo(
            xy=(50, 50),
            width=20,
            angle=45,
            style=IconStyle(style="thin", color=Colors.Red),
        )
        save(f"{OUTPUT_DIR}test_angle45.png")

    def test_phosphor_icon_theme(self) -> None:
        """Verify Phosphor icon drawing with theme color overrides."""
        clear()
        icon_phosphor.google_logo(xy=(25, 25), width=20, style="blue")
        icon_phosphor.google_logo(xy=(25, 75), width=20, style="green")
        icon_phosphor.google_logo(xy=(75, 25), width=20, style="red")
        save(f"{OUTPUT_DIR}test_theme.png")
