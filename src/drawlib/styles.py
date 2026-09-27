# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Public styles module for drawlib.

Provides the active preset styles and corresponding theme colors for drawings.
"""

from __future__ import annotations

import sys as _sys

from drawlib._core.types import Color, Style
from drawlib.preset_colors import (
    BaseColors,
    DefaultColors,
    GoogleColors,
    MonochromeColors,
    default_colors,
    google_colors,
    monochrome_colors,
)
from drawlib.preset_styles import (
    BasePresetStyles,
    DefaultStyles,
    GoogleStyles,
    MonochromeStyles,
    default_styles,
)

# Active styles (default: default_styles)
styles: DefaultStyles = default_styles

# Active colors matching the active theme (default: default_colors)
colors: DefaultColors = default_colors

_STYLE_TO_COLOR_MAP: dict[type[BasePresetStyles], BaseColors] = {
    DefaultStyles: default_colors,
    GoogleStyles: google_colors,
    MonochromeStyles: monochrome_colors,
}


def _resolve_colors(style_obj: BasePresetStyles) -> BaseColors:
    """Resolve corresponding color instance for a given style object.

    Args:
        style_obj (BasePresetStyles): The style instance to inspect.

    Returns:
        BaseColors: The corresponding style color instance.
    """
    for style_cls, color_obj in _STYLE_TO_COLOR_MAP.items():
        if isinstance(style_obj, style_cls):
            return color_obj
    return default_colors


def _set_active_styles(new_styles: BasePresetStyles, new_colors: BaseColors | None = None) -> None:
    """Set the active styles and colors.

    Args:
        new_styles (BasePresetStyles): The new preset style instance.
        new_colors (BaseColors | None): Optional specific color instance.
    """
    mod = _sys.modules.get(__name__)
    if mod is None:
        return
    setattr(mod, "styles", new_styles)
    if new_colors is not None:
        setattr(mod, "colors", new_colors)
    else:
        setattr(mod, "colors", _resolve_colors(new_styles))


def _reset_styles() -> None:
    """Reset styles and colors to defaults."""
    mod = _sys.modules.get(__name__)
    if mod is None:
        return
    setattr(mod, "styles", default_styles)
    setattr(mod, "colors", default_colors)


__all__ = [
    "Color",
    "Style",
    "colors",
    "styles",
]
