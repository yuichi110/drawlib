# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Package for core styles base and models."""

from __future__ import annotations

from drawlib._core.l3_styles._base_styles import (
    DEFAULT_FONT,
    DEFAULT_FONT_BOLD,
    DEFAULT_FONT_THIN,
    DEFAULT_TEXT_SIZE,
    BaseStyles,
)
from drawlib._core.l3_styles._style import (
    Style,
    _construct_preset_style,
)

__all__ = [
    # _base_styles.py
    "DEFAULT_FONT",
    "DEFAULT_FONT_BOLD",
    "DEFAULT_FONT_THIN",
    "DEFAULT_TEXT_SIZE",
    "BaseStyles",
    # _style.py
    "Style",
    "_construct_preset_style",
]
