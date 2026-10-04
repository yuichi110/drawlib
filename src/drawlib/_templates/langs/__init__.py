# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Multilingual typography and language configuration registry for drawlib."""

from __future__ import annotations

from drawlib._templates.langs._map_css import CSS_MAP
from drawlib._templates.langs._map_html import HTML_MAP
from drawlib._templates.langs._map_style_font import STYLE_FONT_MAP
from drawlib._templates.langs._models import (
    CssFontConfig,
    HtmlLangConfig,
    LanguageConfig,
    StyleFontConfig,
)
from drawlib._templates.langs._patch import (
    THEME_PRESET_MAP,
    get_font_replacements,
    get_language_config,
    get_styles_font_imports,
    get_styles_font_patch,
    list_supported_languages,
    normalize_language,
    resolve_style_preset,
)
from drawlib._templates.langs._registry import LANGUAGE_ALIASES, LANGUAGES

__all__ = [
    "CSS_MAP",
    "CssFontConfig",
    "HTML_MAP",
    "HtmlLangConfig",
    "LANGUAGE_ALIASES",
    "LANGUAGES",
    "LanguageConfig",
    "STYLE_FONT_MAP",
    "StyleFontConfig",
    "THEME_PRESET_MAP",
    "get_font_replacements",
    "get_language_config",
    "get_styles_font_imports",
    "get_styles_font_patch",
    "list_supported_languages",
    "normalize_language",
    "resolve_style_preset",
]
