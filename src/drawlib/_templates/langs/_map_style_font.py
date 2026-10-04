# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Language mapping for Drawlib drawing style fonts and patch configuration."""

from __future__ import annotations

from drawlib._templates.langs._models import StyleFontConfig

STYLE_FONT_MAP: dict[str, StyleFontConfig] = {
    "en": StyleFontConfig(
        drawlib_font_module="FontRoboto",
        font_regular_attr="FontRoboto.REGULAR",
        font_bold_attr="FontRoboto.BOLD",
        font_light_attr="FontRoboto.LIGHT",
        activate_patch=False,
    ),
    "ja": StyleFontConfig(
        drawlib_font_module="FontJapanese",
        font_regular_attr="FontJapanese.SANSSERIF_REGULAR",
        font_bold_attr="FontJapanese.SANSSERIF_BOLD",
        font_light_attr="FontJapanese.SANSSERIF_LIGHT",
        activate_patch=True,
    ),
    "zh-cn": StyleFontConfig(
        drawlib_font_module="FontChinese",
        font_regular_attr="FontChinese.SIMPLIFIED_SANSSERIF_REGULAR",
        font_bold_attr="FontChinese.SIMPLIFIED_SANSSERIF_BOLD",
        font_light_attr="FontChinese.SIMPLIFIED_SANSSERIF_LIGHT",
        activate_patch=True,
    ),
    "zh-tw": StyleFontConfig(
        drawlib_font_module="FontChinese",
        font_regular_attr="FontChinese.TRADITIONAL_SANSSERIF_REGULAR",
        font_bold_attr="FontChinese.TRADITIONAL_SANSSERIF_BOLD",
        font_light_attr="FontChinese.TRADITIONAL_SANSSERIF_LIGHT",
        activate_patch=True,
    ),
    "ko": StyleFontConfig(
        drawlib_font_module="FontKorean",
        font_regular_attr="FontKorean.SANSSERIF_REGULAR",
        font_bold_attr="FontKorean.SANSSERIF_BOLD",
        font_light_attr="FontKorean.SANSSERIF_LIGHT",
        activate_patch=True,
    ),
    "th": StyleFontConfig(
        drawlib_font_module="FontThai",
        font_regular_attr="FontThai.SANSSERIF_REGULAR",
        font_bold_attr="FontThai.SANSSERIF_BOLD",
        font_light_attr="FontThai.SANSSERIF_LIGHT",
        activate_patch=True,
    ),
    "hi": StyleFontConfig(
        drawlib_font_module="FontBrahmic",
        font_regular_attr="FontBrahmic.DEVANAGARI_SANSSERIF_REGULAR",
        font_bold_attr="FontBrahmic.DEVANAGARI_SANSSERIF_BOLD",
        font_light_attr="FontBrahmic.DEVANAGARI_SANSSERIF_LIGHT",
        activate_patch=True,
    ),
    "es": StyleFontConfig(
        drawlib_font_module="FontRoboto",
        font_regular_attr="FontRoboto.REGULAR",
        font_bold_attr="FontRoboto.BOLD",
        font_light_attr="FontRoboto.LIGHT",
        activate_patch=False,
    ),
    "fr": StyleFontConfig(
        drawlib_font_module="FontRoboto",
        font_regular_attr="FontRoboto.REGULAR",
        font_bold_attr="FontRoboto.BOLD",
        font_light_attr="FontRoboto.LIGHT",
        activate_patch=False,
    ),
    "de": StyleFontConfig(
        drawlib_font_module="FontRoboto",
        font_regular_attr="FontRoboto.REGULAR",
        font_bold_attr="FontRoboto.BOLD",
        font_light_attr="FontRoboto.LIGHT",
        activate_patch=False,
    ),
    "pt": StyleFontConfig(
        drawlib_font_module="FontRoboto",
        font_regular_attr="FontRoboto.REGULAR",
        font_bold_attr="FontRoboto.BOLD",
        font_light_attr="FontRoboto.LIGHT",
        activate_patch=False,
    ),
    "it": StyleFontConfig(
        drawlib_font_module="FontRoboto",
        font_regular_attr="FontRoboto.REGULAR",
        font_bold_attr="FontRoboto.BOLD",
        font_light_attr="FontRoboto.LIGHT",
        activate_patch=False,
    ),
    "ru": StyleFontConfig(
        drawlib_font_module="FontRoboto",
        font_regular_attr="FontRoboto.REGULAR",
        font_bold_attr="FontRoboto.BOLD",
        font_light_attr="FontRoboto.LIGHT",
        activate_patch=False,
    ),
    "id": StyleFontConfig(
        drawlib_font_module="FontRoboto",
        font_regular_attr="FontRoboto.REGULAR",
        font_bold_attr="FontRoboto.BOLD",
        font_light_attr="FontRoboto.LIGHT",
        activate_patch=False,
    ),
    "vi": StyleFontConfig(
        drawlib_font_module="FontRoboto",
        font_regular_attr="FontRoboto.REGULAR",
        font_bold_attr="FontRoboto.BOLD",
        font_light_attr="FontRoboto.LIGHT",
        activate_patch=False,
    ),
    "tr": StyleFontConfig(
        drawlib_font_module="FontRoboto",
        font_regular_attr="FontRoboto.REGULAR",
        font_bold_attr="FontRoboto.BOLD",
        font_light_attr="FontRoboto.LIGHT",
        activate_patch=False,
    ),
}
