# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Preset styles models module."""

from __future__ import annotations

from dataclasses import dataclass

from drawlib._core.l2_types import TypeColor
from drawlib._core.l3_fonts import FontSourceCode
from drawlib._core.l3_styles import Style


@dataclass
class PresetStyles:
    """Represents a collection of Style presets and settings."""

    primary: Style
    light: Style
    bold: Style
    flat: Style
    solid: Style
    dashed: Style
    background_color: TypeColor = (255, 255, 255, 1.0)
    sourcecode_font: FontSourceCode = FontSourceCode.SOURCECODEPRO
