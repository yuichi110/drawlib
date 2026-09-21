# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

import dataclasses

from drawlib._core.l3_fonts import FontSourceCode
from drawlib._core.l3_styles import Style
from drawlib._preset_styles._models import PresetStyles


class TestPresetStyles:
    """Unit tests for the PresetStyles dataclass."""

    def test_preset_styles_instantiation(self) -> None:
        """Verifies successful instantiation of PresetStyles with valid arguments."""
        primary = Style(fill_color=(0, 0, 255, 1.0))
        light = Style(fill_color=(100, 100, 255, 1.0))
        bold = Style(fill_color=(0, 0, 150, 1.0))
        flat = Style(line_width=0)
        solid = Style(line_style="solid")
        dashed = Style(line_style="dashed")

        preset = PresetStyles(
            primary=primary,
            light=light,
            bold=bold,
            flat=flat,
            solid=solid,
            dashed=dashed,
            background_color=(255, 255, 255, 1.0),
            sourcecode_font=FontSourceCode.ROBOTO_MONO,
        )

        assert dataclasses.is_dataclass(preset)
        assert preset.primary == primary
        assert preset.light == light
        assert preset.bold == bold
        assert preset.flat == flat
        assert preset.solid == solid
        assert preset.dashed == dashed
        assert preset.background_color == (255, 255, 255, 1.0)
        assert preset.sourcecode_font == FontSourceCode.ROBOTO_MONO
