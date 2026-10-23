# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Private preset colors package for drawlib."""

from __future__ import annotations

import importlib
from typing import TYPE_CHECKING, Any, Final

if TYPE_CHECKING:
    from drawlib._core.l3_colors import BaseColors
    from drawlib._preset_colors._color_css import CssColors
    from drawlib._preset_colors._color_default import (
        DefaultColors,
        DefaultColors1,
        DefaultColors2,
        DefaultColors3,
        DefaultColors4,
        DefaultColors5,
        DefaultColors6,
    )
    from drawlib._preset_colors._color_google import GoogleColors
    from drawlib._preset_colors._color_monochrome import MonochromeColors

_LAZY_ATTRS: Final[dict[str, str]] = {
    "BaseColors": "drawlib._core.l3_colors",
    "CssColors": "drawlib._preset_colors._color_css",
    "DefaultColors": "drawlib._preset_colors._color_default",
    "DefaultColors1": "drawlib._preset_colors._color_default",
    "DefaultColors2": "drawlib._preset_colors._color_default",
    "DefaultColors3": "drawlib._preset_colors._color_default",
    "DefaultColors4": "drawlib._preset_colors._color_default",
    "DefaultColors5": "drawlib._preset_colors._color_default",
    "DefaultColors6": "drawlib._preset_colors._color_default",
    "GoogleColors": "drawlib._preset_colors._color_google",
    "MonochromeColors": "drawlib._preset_colors._color_monochrome",
}


def __getattr__(name: str) -> Any:  # noqa: ANN401
    """Lazy-load preset color palettes on first access (PEP 562)."""
    if name in _LAZY_ATTRS:
        module = importlib.import_module(_LAZY_ATTRS[name])
        value = getattr(module, name)
        globals()[name] = value
        return value
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


def __dir__() -> list[str]:
    """Ensure lazy color palettes appear in dir() and autocompletion."""
    return sorted(__all__)


__all__ = [
    "BaseColors",
    "CssColors",
    "DefaultColors",
    "DefaultColors1",
    "DefaultColors2",
    "DefaultColors3",
    "DefaultColors4",
    "DefaultColors5",
    "DefaultColors6",
    "GoogleColors",
    "MonochromeColors",
]
