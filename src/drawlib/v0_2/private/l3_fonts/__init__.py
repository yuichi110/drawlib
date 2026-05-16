# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Package for font implementations."""

from drawlib.v0_2.private.l2_models import (
    FontBase,
    FontFile,
    FontMetadata,
    FontResource,
)
from drawlib.v0_2.private.l3_fonts._fonts import get_font_metadata
from drawlib.v0_2.private.l3_fonts._names import (
    Font,
    FontArabic,
    FontBrahmic,
    FontChinese,
    FontJapanese,
    FontKorean,
    FontMonoSpace,
    FontRoboto,
    FontSansSerif,
    FontSerif,
    FontSourceCode,
    FontThai,
)
from drawlib.v0_2.private.l3_fonts._resources import FONT_RESOURCES

__all__ = [
    # l2_models_types
    "FontBase",
    "FontFile",
    "FontMetadata",
    "FontResource",
    # _fonts.py
    "get_font_metadata",
    # _names.py
    "Font",
    "FontArabic",
    "FontBrahmic",
    "FontChinese",
    "FontJapanese",
    "FontKorean",
    "FontMonoSpace",
    "FontRoboto",
    "FontSansSerif",
    "FontSerif",
    "FontSourceCode",
    "FontThai",
    # _resources.py
    "FONT_RESOURCES",
]
