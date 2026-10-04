# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Language mapping for CSS typography and font family stacks."""

from __future__ import annotations

from drawlib._templates.langs._models import CssFontConfig

_UNIVERSAL_CJK_FALLBACK = (
    '"Hiragino Sans", "Hiragino Kaku Gothic ProN", "Noto Sans JP", "Noto Sans CJK JP", "Yu Gothic", Meiryo'
)
_UNIVERSAL_MONO_CJK_FALLBACK = '"Noto Sans Mono CJK JP"'

CSS_MAP: dict[str, CssFontConfig] = {
    "en": CssFontConfig(
        font_family=_UNIVERSAL_CJK_FALLBACK,
        mono_font_family=_UNIVERSAL_MONO_CJK_FALLBACK,
    ),
    "ja": CssFontConfig(
        font_family='"Noto Sans JP", "Hiragino Sans", "Hiragino Kaku Gothic ProN", "Yu Gothic", Meiryo',
        mono_font_family=_UNIVERSAL_MONO_CJK_FALLBACK,
    ),
    "zh-cn": CssFontConfig(
        font_family='"Noto Sans SC", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "WenQuanYi Micro Hei"',
        mono_font_family='"Noto Sans Mono CJK SC"',
    ),
    "zh-tw": CssFontConfig(
        font_family='"Noto Sans TC", "PingFang TC", "Hiragino Sans TC", "Microsoft JhengHei"',
        mono_font_family='"Noto Sans Mono CJK TC"',
    ),
    "ko": CssFontConfig(
        font_family='"Noto Sans KR", "Apple SD Gothic Neo", "Malgun Gothic", "Nanum Gothic"',
        mono_font_family='"Noto Sans Mono CJK KR"',
    ),
    "th": CssFontConfig(
        font_family='"Noto Sans Thai", "Thonburi", "Leelawadee UI", "Angsana New"',
        mono_font_family='"Noto Sans Mono"',
    ),
    "hi": CssFontConfig(
        font_family='"Noto Sans Devanagari", "Mangal", "Kokila", "Utsaah"',
        mono_font_family='"Noto Sans Mono"',
    ),
    "es": CssFontConfig(
        font_family=_UNIVERSAL_CJK_FALLBACK,
        mono_font_family=_UNIVERSAL_MONO_CJK_FALLBACK,
    ),
    "fr": CssFontConfig(
        font_family=_UNIVERSAL_CJK_FALLBACK,
        mono_font_family=_UNIVERSAL_MONO_CJK_FALLBACK,
    ),
    "de": CssFontConfig(
        font_family=_UNIVERSAL_CJK_FALLBACK,
        mono_font_family=_UNIVERSAL_MONO_CJK_FALLBACK,
    ),
    "pt": CssFontConfig(
        font_family=_UNIVERSAL_CJK_FALLBACK,
        mono_font_family=_UNIVERSAL_MONO_CJK_FALLBACK,
    ),
    "it": CssFontConfig(
        font_family=_UNIVERSAL_CJK_FALLBACK,
        mono_font_family=_UNIVERSAL_MONO_CJK_FALLBACK,
    ),
    "ru": CssFontConfig(
        font_family=_UNIVERSAL_CJK_FALLBACK,
        mono_font_family=_UNIVERSAL_MONO_CJK_FALLBACK,
    ),
    "id": CssFontConfig(
        font_family=_UNIVERSAL_CJK_FALLBACK,
        mono_font_family=_UNIVERSAL_MONO_CJK_FALLBACK,
    ),
    "vi": CssFontConfig(
        font_family=_UNIVERSAL_CJK_FALLBACK,
        mono_font_family=_UNIVERSAL_MONO_CJK_FALLBACK,
    ),
    "tr": CssFontConfig(
        font_family=_UNIVERSAL_CJK_FALLBACK,
        mono_font_family=_UNIVERSAL_MONO_CJK_FALLBACK,
    ),
}
