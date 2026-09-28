# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Package for core styles and colors base."""

from drawlib._core.l3_styles._colors import (
    BaseColors,
)
from drawlib._core.l3_styles._style_models import (
    ALL_SUPPORTS,
    Style,
    SupportType,
)

__all__ = [
    # _colors.py
    "BaseColors",
    # _style_models.py
    "ALL_SUPPORTS",
    "Style",
    "SupportType",
]
