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

from typing import Final, Optional

from drawlib._templates.langs._models import LanguageConfig
from drawlib._templates.langs._registry import LANGUAGE_ALIASES, LANGUAGES

THEME_PRESET_MAP: Final[dict[str, tuple[str, str]]] = {
    "default": ("DefaultStyles", "DefaultColors"),
    "default-dark": ("DefaultStyles", "DefaultColors"),
    "default-auto": ("DefaultStyles", "DefaultColors"),
    "google": ("GoogleStyles", "GoogleColors"),
    "google-dark": ("GoogleStyles", "GoogleColors"),
    "google-auto": ("GoogleStyles", "GoogleColors"),
    "monochrome": ("MonochromeStyles", "MonochromeColors"),
    "github": ("DefaultStyles", "DefaultColors"),
    "minimal": ("DefaultStyles", "DefaultColors"),
    "default1": ("DefaultStyles1", "DefaultColors1"),
    "default2": ("DefaultStyles2", "DefaultColors2"),
    "default3": ("DefaultStyles3", "DefaultColors3"),
    "default4": ("DefaultStyles4", "DefaultColors4"),
    "default5": ("DefaultStyles5", "DefaultColors5"),
    "default6": ("DefaultStyles6", "DefaultColors6"),
}


def resolve_style_preset(style_theme: Optional[str]) -> tuple[str, str]:
    """Resolve style theme name to (styles_class_name, colors_class_name).

    Args:
        style_theme: Style preset name (e.g. 'default', 'google', 'monochrome').

    Returns:
        tuple[str, str]: Tuple of (StyleClassName, ColorClassName).
    """
    if not style_theme:
        return ("DefaultStyles", "DefaultColors")
    clean = style_theme.strip().lower()
    return THEME_PRESET_MAP.get(clean, ("DefaultStyles", "DefaultColors"))


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


def get_styles_font_imports(lang: str, style_theme: str = "default") -> str:
    """Generate Python import statements for styles.py.

    Args:
        lang: Language code or alias.
        style_theme: Style preset name ('default', 'google', 'monochrome', etc.).

    Returns:
        str: Python import statements.
    """
    cfg = get_language_config(lang)
    style_cls, color_cls = resolve_style_preset(style_theme)

    lines: list[str] = []
    if cfg.activate_patch:
        lines.append(f"from drawlib.fonts import {cfg.drawlib_font_module}")
    lines.append(f"from drawlib.preset_colors import {color_cls}")
    lines.append(f"from drawlib.preset_styles import {style_cls}")
    return "\n".join(lines) + "\n"


def get_styles_font_patch(lang: str, style_theme: str = "default") -> str:
    """Generate Python code snippet for styles.py to configure Styles and Colors.

    Args:
        lang: Language code or alias.
        style_theme: Style preset name ('default', 'google', 'monochrome', etc.).

    Returns:
        str: Python code snippet configuring Styles and Colors.
    """
    cfg = get_language_config(lang)
    style_cls, color_cls = resolve_style_preset(style_theme)

    if cfg.activate_patch:
        theme_name = "default" if style_theme in {"default", ""} else style_theme
        return (
            f"Colors = {color_cls}()\n"
            f"# Apply {cfg.name} fonts to {theme_name} drawing styles\n"
            f"Styles = {style_cls}().patch_font(\n"
            f"    regular={cfg.font_regular_attr},\n"
            f"    bold={cfg.font_bold_attr},\n"
            f"    light={cfg.font_light_attr},\n"
            ")"
        )

    return f"Colors = {color_cls}()\nStyles = {style_cls}()"


def get_font_replacements(lang_code: str, style_theme: str = "default") -> dict[str, str]:
    """Generate substitution mapping for templates and stylesheets based on language and style.

    Args:
        lang_code: Language code or alias (e.g. 'en', 'ja', 'th').
        style_theme: Style preset name (e.g. 'default', 'google', 'monochrome').

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
        "__RTD_STYLES_IMPORTS__": get_styles_font_imports(lang_code, style_theme=style_theme),
        "__RTD_STYLES_FONT_PATCH__": get_styles_font_patch(lang_code, style_theme=style_theme),
    }
