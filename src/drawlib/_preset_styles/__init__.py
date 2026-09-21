# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Private preset_styles package for drawlib."""

from drawlib._preset_styles._models import PresetStyles
from drawlib._preset_styles._officials import (
    get_default_styles,
    get_essentials_styles,
    get_monochrome_styles,
    get_style,
    get_styles,
)

__all__ = [
    "PresetStyles",
    "get_default_styles",
    "get_essentials_styles",
    "get_monochrome_styles",
    "get_style",
    "get_styles",
]
