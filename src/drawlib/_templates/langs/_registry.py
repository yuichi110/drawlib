# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Supported languages registry and alias definitions."""

from __future__ import annotations

from drawlib._templates.langs._map_css import CSS_MAP
from drawlib._templates.langs._map_html import HTML_MAP
from drawlib._templates.langs._map_style_font import STYLE_FONT_MAP
from drawlib._templates.langs._models import LanguageConfig


def _build_languages() -> dict[str, LanguageConfig]:
    """Assemble unified LanguageConfig instances from HTML, CSS, and style font maps."""
    languages: dict[str, LanguageConfig] = {}
    for key, html_cfg in HTML_MAP.items():
        css_cfg = CSS_MAP[key]
        style_cfg = STYLE_FONT_MAP[key]
        languages[key] = LanguageConfig(
            code=html_cfg.code,
            name=html_cfg.name,
            direction=html_cfg.direction,
            google_font_family=html_cfg.google_font_family,
            font_family=css_cfg.font_family,
            mono_font_family=css_cfg.mono_font_family,
            drawlib_font_module=style_cfg.drawlib_font_module,
            font_regular_attr=style_cfg.font_regular_attr,
            font_bold_attr=style_cfg.font_bold_attr,
            font_thin_attr=style_cfg.font_thin_attr,
            activate_patch=style_cfg.activate_patch,
        )
    return languages


LANGUAGES: dict[str, LanguageConfig] = _build_languages()

# Aliases mapping alternative names / BCP-47 variations to canonical keys in LANGUAGES
LANGUAGE_ALIASES: dict[str, str] = {
    "zh": "zh-cn",
    "zh-hans": "zh-cn",
    "zh-sg": "zh-cn",
    "zh-hant": "zh-tw",
    "zh-hk": "zh-tw",
    "jp": "ja",
    "jpn": "ja",
    "kr": "ko",
    "kor": "ko",
    "in": "id",
}
