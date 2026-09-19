# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Public colors module for drawlib."""

from drawlib._core.l3_styles import (
    Colors,
    Colors140,
    ColorsThemeDefault,
    ColorsThemeEssentials,
    ColorsThemeMonochrome,
)
from drawlib._utils._color import (
    get_rgba as with_alpha,
)
from drawlib._utils._color import (
    get_rgba_from_grayscale as from_grayscale,
)
from drawlib._utils._color import (
    get_rgba_from_hexcode as from_hex,
)

__all__ = [
    # Color Classes
    "Colors",
    "Colors140",
    "ColorsThemeDefault",
    "ColorsThemeEssentials",
    "ColorsThemeMonochrome",
    # Color Utilities
    "from_hex",
    "from_grayscale",
    "with_alpha",
]
