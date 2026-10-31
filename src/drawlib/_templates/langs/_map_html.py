# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Language mapping for HTML attributes, text direction, and Google Fonts."""

from __future__ import annotations

from drawlib._templates.langs._models import HtmlLangConfig

HTML_MAP: dict[str, HtmlLangConfig] = {
    "en": HtmlLangConfig(code="en", name="English", native_name="English", direction="ltr"),
    "ja": HtmlLangConfig(
        code="ja",
        name="Japanese",
        native_name="日本語",
        google_font_family="Noto+Sans+JP:wght@400;500;700",
    ),
    "zh-cn": HtmlLangConfig(
        code="zh-CN",
        name="Simplified Chinese",
        native_name="简体中文",
        google_font_family="Noto+Sans+SC:wght@400;500;700",
    ),
    "zh-tw": HtmlLangConfig(
        code="zh-TW",
        name="Traditional Chinese",
        native_name="繁體中文",
        google_font_family="Noto+Sans+TC:wght@400;500;700",
    ),
    "ko": HtmlLangConfig(
        code="ko",
        name="Korean",
        native_name="한국어",
        google_font_family="Noto+Sans+KR:wght@400;500;700",
    ),
    "th": HtmlLangConfig(
        code="th",
        name="Thai",
        native_name="ไทย",
        google_font_family="Noto+Sans+Thai:wght@400;500;700",
    ),
    "hi": HtmlLangConfig(
        code="hi",
        name="Hindi",
        native_name="हिन्दी",
        google_font_family="Noto+Sans+Devanagari:wght@400;500;700",
    ),
    "es": HtmlLangConfig(code="es", name="Spanish", native_name="Español"),
    "fr": HtmlLangConfig(code="fr", name="French", native_name="Français"),
    "de": HtmlLangConfig(code="de", name="German", native_name="Deutsch"),
    "pt": HtmlLangConfig(code="pt", name="Portuguese", native_name="Português"),
    "it": HtmlLangConfig(code="it", name="Italian", native_name="Italiano"),
    "ru": HtmlLangConfig(code="ru", name="Russian", native_name="Русский"),
    "id": HtmlLangConfig(code="id", name="Indonesian", native_name="Bahasa Indonesia"),
    "vi": HtmlLangConfig(code="vi", name="Vietnamese", native_name="Tiếng Việt"),
    "tr": HtmlLangConfig(code="tr", name="Turkish", native_name="Türkçe"),
}
