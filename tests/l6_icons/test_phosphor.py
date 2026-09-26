# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for Phosphor icons drawing."""

import importlib

from drawlib import icons
from drawlib._icons.font_icons import phosphor as phosphor_internal
from drawlib.canvas import clear, save
from drawlib.colors import Colors
from drawlib.icons import phosphor
from drawlib.preset_styles import default_styles, essentials_styles
from drawlib.types import Style

OUTPUT_DIR = "../../output_tests/l6_icons/icon_phosphor/"


class TestCanvasPhosphor:
    """Tests for Phosphor icons drawing support."""

    def test_phosphor_icon_drawing(self) -> None:
        """Verify basic Phosphor icon drawing and styles (fill, thin, bold)."""
        clear()

        # Representative icon: google_logo
        s_def = default_styles.primary.patch(icon_style="thin")
        phosphor.google_logo(xy=(50, 50), width=20, style=s_def)
        save(f"{OUTPUT_DIR}test_basic.png")

        clear()
        phosphor.google_logo(
            xy=(50, 50),
            width=20,
            style=Style(icon_style="fill", icon_color=Colors.Red),
        )
        save(f"{OUTPUT_DIR}test_style.png")

    def test_phosphor_icon_angle(self) -> None:
        """Verify Phosphor icon drawing combined with a rotation angle."""
        clear()
        phosphor.google_logo(
            xy=(50, 50),
            width=20,
            angle=45,
            style=Style(icon_style="thin", icon_color=Colors.Red),
        )
        save(f"{OUTPUT_DIR}test_angle45.png")

    def test_phosphor_icon_theme(self) -> None:
        """Verify Phosphor icon drawing with theme color overrides."""
        clear()
        styles = essentials_styles
        phosphor.google_logo(xy=(25, 25), width=20, style=styles.blue.patch(icon_style="thin"))
        phosphor.google_logo(xy=(25, 75), width=20, style=styles.green.patch(icon_style="thin"))
        phosphor.google_logo(xy=(75, 25), width=20, style=styles.red.patch(icon_style="thin"))
        save(f"{OUTPUT_DIR}test_theme.png")

    def test_phosphor_flat_import(self) -> None:
        """Verify Phosphor icon drawing via flat drawlib.icons.phosphor import."""
        s_def = default_styles.primary.patch(icon_style="thin")
        phosphor.google_logo(xy=(50, 50), width=20, style=s_def)
        phosphor_submodule = importlib.import_module("drawlib.icons.phosphor")

        assert phosphor.google_logo == phosphor_submodule.google_logo
        assert phosphor.google_logo == phosphor_internal.google_logo
        assert not hasattr(icons, "icon_phosphor")
