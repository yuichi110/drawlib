# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Language normalization, font replacements, and styles font patch code generator."""

from __future__ import annotations

from drawlib._langs._models import LanguageConfig
from drawlib._langs._registry import LANGUAGE_ALIASES, LANGUAGES


def list_supported_languages() -> list[str]:
    """Return sorted list of supported language code keys.

    Returns:
        list[str]: Supported canonical language codes.
    """
    return sorted(LANGUAGES.keys())


def normalize_language(lang: str) -> str:
    """Normalize input language code string to canonical registered language key.

    Args:
        lang: Input language code (e.g. 'JA', 'zh-Hans', 'jp', 'th').

    Returns:
        str: Canonical key in LANGUAGES (e.g. 'ja', 'zh-cn', 'th').

    Raises:
        ValueError: If input language code is unknown or unsupported.
    """
    clean = lang.strip().lower().replace("_", "-")
    resolved = LANGUAGE_ALIASES.get(clean, clean)
    if resolved in LANGUAGES:
        return resolved
    supported = ", ".join(sorted(LANGUAGES.keys()))
    raise ValueError(f"Unsupported language '{lang}'. Supported languages: {supported}")


def get_language_config(lang: str) -> LanguageConfig:
    """Get LanguageConfig for a language code or alias.

    Args:
        lang: Language code or alias (e.g. 'en', 'ja', 'zh', 'jp', 'th').

    Returns:
        LanguageConfig: Metadata configuration for the language.

    Raises:
        ValueError: If the language is not supported.
    """
    canonical_key = normalize_language(lang)
    return LANGUAGES[canonical_key]


def get_styles_font_imports(lang: str) -> str:
    """Generate Python import statements for styles.py.

    Args:
        lang: Language code or alias.

    Returns:
        str: Python import statements or empty string if no patch is needed.
    """
    cfg = get_language_config(lang)
    if cfg.activate_patch:
        return f"from drawlib.fonts import {cfg.drawlib_font_module}\nfrom drawlib.preset_styles import DefaultStyles\n"
    return ""


def get_styles_font_patch(lang: str) -> str:
    """Generate Python code snippet for styles.py to patch DefaultStyles font.

    Args:
        lang: Language code or alias.

    Returns:
        str: Python code snippet configuring Styles.
    """
    cfg = get_language_config(lang)
    if cfg.activate_patch:
        return (
            f"# Apply {cfg.name} fonts to default drawing styles\n"
            "Styles = DefaultStyles().patch_font(\n"
            f"    regular={cfg.font_regular_attr},\n"
            f"    bold={cfg.font_bold_attr},\n"
            f"    light={cfg.font_light_attr},\n"
            ")"
        )

    return (
        "# To customize default drawing fonts, uncomment and configure:\n"
        "#\n"
        f"# from drawlib.fonts import {cfg.drawlib_font_module}\n"
        "# from drawlib.preset_styles import DefaultStyles\n"
        "#\n"
        "# Styles = DefaultStyles().patch_font(\n"
        f"#     regular={cfg.font_regular_attr},\n"
        f"#     bold={cfg.font_bold_attr},\n"
        f"#     light={cfg.font_light_attr},\n"
        "# )"
    )


def get_font_replacements(lang_code: str) -> dict[str, str]:
    """Generate substitution mapping for templates and stylesheets based on language.

    Args:
        lang_code: Language code or alias (e.g. 'en', 'ja', 'th').

    Returns:
        dict[str, str]: Placeholder replacements dictionary.
    """
    cfg = get_language_config(lang_code)
    return {
        "__RTD_FONT_LINK__": cfg.font_link_html,
        "__RTD_FONT_FAMILY__": f"{cfg.font_family}, " if cfg.font_family else "",
        "__RTD_MONO_FONT_FAMILY__": f"{cfg.mono_font_family}, " if cfg.mono_font_family else "",
        "__RTD_HTML_LANG__": cfg.code,
        "__RTD_HTML_DIR__": cfg.direction,
        "__RTD_STYLES_IMPORTS__": get_styles_font_imports(lang_code),
        "__RTD_STYLES_FONT_PATCH__": get_styles_font_patch(lang_code),
    }
