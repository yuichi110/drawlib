# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Public fonts module for drawlib."""

from drawlib._core.l3_fonts import (
    Font,
    FontArabic,
    FontBase,
    FontBrahmic,
    FontChinese,
    FontFile,
    FontJapanese,
    FontKorean,
    FontMonoSpace,
    FontRoboto,
    FontSansSerif,
    FontSerif,
    FontSourceCode,
    FontThai,
)

__all__ = [
    "FontBase",
    "FontFile",
    "Font",
    "FontSansSerif",
    "FontSerif",
    "FontMonoSpace",
    "FontRoboto",
    "FontSourceCode",
    "FontJapanese",
    "FontChinese",
    "FontKorean",
    "FontArabic",
    "FontThai",
    "FontBrahmic",
]
