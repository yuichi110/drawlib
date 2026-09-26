# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Core fonts facade module."""

from drawlib._core.l2_models import (
    FontBase,
    FontFile,
    FontMetadata,
    FontResource,
)
from drawlib._core.l3_fonts import (
    FONT_RESOURCES,
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
    get_font_metadata,
)

__all__ = [
    "FONT_RESOURCES",
    "Font",
    "FontArabic",
    "FontBase",
    "FontBrahmic",
    "FontChinese",
    "FontFile",
    "FontJapanese",
    "FontKorean",
    "FontMetadata",
    "FontMonoSpace",
    "FontResource",
    "FontRoboto",
    "FontSansSerif",
    "FontSerif",
    "FontSourceCode",
    "FontThai",
    "get_font_metadata",
]
