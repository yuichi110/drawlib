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

from drawlib._core.l2_models import StaticContainer
from drawlib.colors import (
    DefaultStyleColors,
    EssentialsStyleColors,
    GoogleStyleColors,
    MonochromeStyleColors,
)
from drawlib.preset_styles import (
    BasePresetStyles,
    DefaultStyles,
    EssentialsStyles,
    GoogleStyles,
    MonochromeStyles,
    essentials_styles,
)

# Active styles (default: essentials_styles)
styles: EssentialsStyles = essentials_styles

# Active colors matching the active theme
colors: type[EssentialsStyleColors] = EssentialsStyleColors

_STYLE_TO_COLOR_MAP: dict[type[BasePresetStyles], type[StaticContainer]] = {
    EssentialsStyles: EssentialsStyleColors,
    DefaultStyles: DefaultStyleColors,
    GoogleStyles: GoogleStyleColors,
    MonochromeStyles: MonochromeStyleColors,
}


def _resolve_colors(style_obj: BasePresetStyles) -> type[StaticContainer]:
    """Resolve corresponding color class for a given style object.

    Args:
        style_obj (BasePresetStyles): The style instance to inspect.

    Returns:
        type[StaticContainer]: The corresponding style color class.
    """
    for style_cls, color_cls in _STYLE_TO_COLOR_MAP.items():
        if isinstance(style_obj, style_cls):
            return color_cls
    return EssentialsStyleColors


def _set_active_styles(new_styles: BasePresetStyles, new_colors: type[StaticContainer] | None = None) -> None:
    """Set the active styles and colors.

    Args:
        new_styles (BasePresetStyles): The new preset style instance.
        new_colors (type[StaticContainer] | None): Optional specific color class.
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
    setattr(mod, "styles", essentials_styles)
    setattr(mod, "colors", EssentialsStyleColors)


__all__ = [
    "colors",
    "styles",
]
