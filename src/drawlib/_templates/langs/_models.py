# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Language configuration model definitions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class HtmlLangConfig:
    """HTML-specific language configuration.

    Attributes:
        code: Normalized ISO 639 / BCP-47 language tag (e.g. 'en', 'ja', 'th', 'zh-CN').
        name: Human-readable English name of the language (e.g. 'English', 'Japanese').
        direction: Writing direction ('ltr' or 'rtl').
        google_font_family: Google Fonts family query parameter.
    """

    code: str
    name: str
    direction: Literal["ltr", "rtl"] = "ltr"
    google_font_family: str = ""


@dataclass(frozen=True)
class CssFontConfig:
    """CSS font-family stacks for HTML and PDF stylesheets.

    Attributes:
        font_family: Primary font-family stack.
        mono_font_family: Monospace font-family stack.
    """

    font_family: str
    mono_font_family: str


@dataclass(frozen=True)
class StyleFontConfig:
    """Drawlib Python drawing style font configuration.

    Attributes:
        drawlib_font_module: Drawlib font class name (e.g. 'FontJapanese', 'FontThai', 'FontRoboto').
        font_regular_attr: Regular font attribute name.
        font_bold_attr: Bold font attribute name.
        font_thin_attr: Thin font attribute name.
        activate_patch: Whether to activate Styles.patch_font by default in styles.py.
    """

    drawlib_font_module: str = "FontRoboto"
    font_regular_attr: str = "FontRoboto.REGULAR"
    font_bold_attr: str = "FontRoboto.BOLD"
    font_thin_attr: str = "FontRoboto.THIN"
    activate_patch: bool = False


@dataclass(frozen=True)
class LanguageConfig:
    """Configuration metadata and font stacks for a supported language.

    Attributes:
        code: Normalized ISO 639 / BCP-47 language tag (e.g. 'en', 'ja', 'th', 'zh-CN').
        name: Human-readable English name of the language (e.g. 'English', 'Japanese').
        direction: Writing direction ('ltr' or 'rtl').
        google_font_family: Google Fonts family query parameter (e.g. 'Noto+Sans+JP:wght@400;500;700').
        font_family: Primary CSS font-family stack for HTML/PDF stylesheets.
        mono_font_family: Primary monospace CSS font-family stack for HTML/PDF stylesheets.
        drawlib_font_module: Drawlib font class name (e.g. 'FontJapanese', 'FontThai', 'FontRoboto').
        font_regular_attr: Drawlib font regular constant (e.g. 'FontJapanese.SANSSERIF_REGULAR').
        font_bold_attr: Drawlib font bold constant (e.g. 'FontJapanese.SANSSERIF_BOLD').
        font_thin_attr: Drawlib font thin constant (e.g. 'FontJapanese.SANSSERIF_THIN').
        activate_patch: Whether to activate Styles.patch_font by default in styles.py.
    """

    code: str
    name: str
    direction: Literal["ltr", "rtl"] = "ltr"
    google_font_family: str = ""
    font_family: str = ""
    mono_font_family: str = ""
    drawlib_font_module: str = "FontRoboto"
    font_regular_attr: str = "FontRoboto.REGULAR"
    font_bold_attr: str = "FontRoboto.BOLD"
    font_thin_attr: str = "FontRoboto.THIN"
    activate_patch: bool = False

    @property
    def font_link_html(self) -> str:
        """Generate HTML preconnect and link tags for Google Fonts if needed.

        Returns:
            str: HTML snippet with preconnect and stylesheet link, or empty string.
        """
        if not self.google_font_family:
            return ""
        return (
            '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
            '    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            f'    <link href="https://fonts.googleapis.com/css2?family={self.google_font_family}&display=swap" '
            'rel="stylesheet">'
        )
