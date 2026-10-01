# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for drawlib._langs module."""

from __future__ import annotations

import pytest

from drawlib._langs import (
    CSS_MAP,
    HTML_MAP,
    LANGUAGES,
    STYLE_FONT_MAP,
    get_font_replacements,
    get_language_config,
    get_styles_font_imports,
    get_styles_font_patch,
    list_supported_languages,
    normalize_language,
)


def test_list_supported_languages() -> None:
    """Test list_supported_languages returns 16 supported languages."""
    langs = list_supported_languages()
    assert len(langs) == 16
    expected = [
        "de",
        "en",
        "es",
        "fr",
        "hi",
        "id",
        "it",
        "ja",
        "ko",
        "pt",
        "ru",
        "th",
        "tr",
        "vi",
        "zh-cn",
        "zh-tw",
    ]
    assert sorted(langs) == expected


def test_normalize_language() -> None:
    """Test normalize_language handles valid codes, aliases, and case insensitivity."""
    assert normalize_language("en") == "en"
    assert normalize_language("EN") == "en"
    assert normalize_language("ja") == "ja"
    assert normalize_language("JP") == "ja"
    assert normalize_language("jpn") == "ja"
    assert normalize_language("zh") == "zh-cn"
    assert normalize_language("zh-hans") == "zh-cn"
    assert normalize_language("zh-hant") == "zh-tw"
    assert normalize_language("zh-tw") == "zh-tw"
    assert normalize_language("ko") == "ko"
    assert normalize_language("kr") == "ko"
    assert normalize_language("kor") == "ko"
    assert normalize_language("th") == "th"
    assert normalize_language("hi") == "hi"

    with pytest.raises(ValueError, match="Unsupported language 'xx'"):
        normalize_language("xx")


def test_get_language_config() -> None:
    """Test get_language_config returns correct LanguageConfig metadata."""
    cfg_th = get_language_config("th")
    assert cfg_th.code == "th"
    assert cfg_th.name == "Thai"
    assert cfg_th.direction == "ltr"
    assert "Noto Sans Thai" in cfg_th.font_family
    assert "Noto+Sans+Thai" in cfg_th.google_font_family
    assert '<link href="https://fonts.googleapis.com' in cfg_th.font_link_html

    cfg_ja = get_language_config("ja")
    assert cfg_ja.code == "ja"
    assert "Noto Sans JP" in cfg_ja.font_family

    cfg_en = get_language_config("en")
    assert cfg_en.code == "en"
    assert cfg_en.google_font_family == ""
    assert cfg_en.font_link_html == ""

    with pytest.raises(ValueError, match="Unsupported language 'invalid'"):
        get_language_config("invalid")


def test_get_font_replacements() -> None:
    """Test get_font_replacements builds proper placeholder dictionary."""
    rep_th = get_font_replacements("th")
    assert rep_th["__RTD_HTML_LANG__"] == "th"
    assert rep_th["__RTD_HTML_DIR__"] == "ltr"
    assert '<link href="https://fonts.googleapis.com' in rep_th["__RTD_FONT_LINK__"]
    assert '"Noto Sans Thai"' in rep_th["__RTD_FONT_FAMILY__"]
    assert rep_th["__RTD_FONT_FAMILY__"].endswith(", ")
    assert '"Noto Sans Mono"' in rep_th["__RTD_MONO_FONT_FAMILY__"]
    assert rep_th["__RTD_MONO_FONT_FAMILY__"].endswith(", ")

    rep_en = get_font_replacements("en")
    assert rep_en["__RTD_HTML_LANG__"] == "en"
    assert rep_en["__RTD_FONT_LINK__"] == ""


def test_get_styles_font_patch() -> None:
    """Test get_styles_font_patch and get_styles_font_imports generate expected Python code."""
    # English needs no active patch, returns commented guidance
    assert get_styles_font_imports("en") == ""
    patch_en = get_styles_font_patch("en")
    assert "# To customize default drawing fonts, uncomment and configure:" in patch_en
    assert "# from drawlib.fonts import FontRoboto" in patch_en
    assert "# Styles = DefaultStyles().patch_font(" in patch_en

    # Japanese needs FontJapanese imports and patch
    imports_ja = get_styles_font_imports("ja")
    assert "from drawlib.fonts import FontJapanese" in imports_ja
    assert "from drawlib.preset_styles import DefaultStyles" in imports_ja
    patch_ja = get_styles_font_patch("ja")
    assert "Styles = DefaultStyles().patch_font(" in patch_ja
    assert "regular=FontJapanese.SANSSERIF_REGULAR," in patch_ja
    assert "bold=FontJapanese.SANSSERIF_BOLD," in patch_ja

    # Thai needs FontThai imports and patch
    imports_th = get_styles_font_imports("th")
    assert "from drawlib.fonts import FontThai" in imports_th
    patch_th = get_styles_font_patch("th")
    assert "regular=FontThai.SANSSERIF_REGULAR," in patch_th


def test_maps_consistency() -> None:
    """Test HTML_MAP, CSS_MAP, and STYLE_FONT_MAP have consistent keys with LANGUAGES."""
    expected_keys = set(LANGUAGES.keys())
    assert set(HTML_MAP.keys()) == expected_keys
    assert set(CSS_MAP.keys()) == expected_keys
    assert set(STYLE_FONT_MAP.keys()) == expected_keys

    for key, cfg in LANGUAGES.items():
        html_cfg = HTML_MAP[key]
        css_cfg = CSS_MAP[key]
        style_cfg = STYLE_FONT_MAP[key]

        assert cfg.code == html_cfg.code
        assert cfg.name == html_cfg.name
        assert cfg.direction == html_cfg.direction
        assert cfg.google_font_family == html_cfg.google_font_family

        assert cfg.font_family == css_cfg.font_family
        assert cfg.mono_font_family == css_cfg.mono_font_family

        assert cfg.drawlib_font_module == style_cfg.drawlib_font_module
        assert cfg.font_regular_attr == style_cfg.font_regular_attr
        assert cfg.font_bold_attr == style_cfg.font_bold_attr
        assert cfg.font_light_attr == style_cfg.font_light_attr
        assert cfg.activate_patch == style_cfg.activate_patch
