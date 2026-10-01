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

from drawlib._langs._models import HtmlLangConfig

HTML_MAP: dict[str, HtmlLangConfig] = {
    "en": HtmlLangConfig(code="en", name="English", direction="ltr"),
    "ja": HtmlLangConfig(code="ja", name="Japanese", google_font_family="Noto+Sans+JP:wght@400;500;700"),
    "zh-cn": HtmlLangConfig(
        code="zh-CN",
        name="Simplified Chinese",
        google_font_family="Noto+Sans+SC:wght@400;500;700",
    ),
    "zh-tw": HtmlLangConfig(
        code="zh-TW",
        name="Traditional Chinese",
        google_font_family="Noto+Sans+TC:wght@400;500;700",
    ),
    "ko": HtmlLangConfig(code="ko", name="Korean", google_font_family="Noto+Sans+KR:wght@400;500;700"),
    "th": HtmlLangConfig(code="th", name="Thai", google_font_family="Noto+Sans+Thai:wght@400;500;700"),
    "hi": HtmlLangConfig(code="hi", name="Hindi", google_font_family="Noto+Sans+Devanagari:wght@400;500;700"),
    "es": HtmlLangConfig(code="es", name="Spanish"),
    "fr": HtmlLangConfig(code="fr", name="French"),
    "de": HtmlLangConfig(code="de", name="German"),
    "pt": HtmlLangConfig(code="pt", name="Portuguese"),
    "it": HtmlLangConfig(code="it", name="Italian"),
    "ru": HtmlLangConfig(code="ru", name="Russian"),
    "id": HtmlLangConfig(code="id", name="Indonesian"),
    "vi": HtmlLangConfig(code="vi", name="Vietnamese"),
    "tr": HtmlLangConfig(code="tr", name="Turkish"),
}
