# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Public preset colors module for drawlib."""

from __future__ import annotations

import importlib
from typing import TYPE_CHECKING, Any, Final

if TYPE_CHECKING:
    from drawlib._core.l3_colors import (
        Color,
        get_intermediate_color,
        get_intermediate_colors,
    )
    from drawlib._preset_colors import (
        CssColors,
        DefaultColors,
        DefaultColors1,
        DefaultColors2,
        DefaultColors3,
        DefaultColors4,
        DefaultColors5,
        DefaultColors6,
        GoogleColors,
        MonochromeColors,
    )

_LAZY_ATTRS: Final[dict[str, str]] = {
    "Color": "drawlib._core.l3_colors",
    "get_intermediate_color": "drawlib._core.l3_colors",
    "get_intermediate_colors": "drawlib._core.l3_colors",
    "CssColors": "drawlib._preset_colors",
    "DefaultColors": "drawlib._preset_colors",
    "DefaultColors1": "drawlib._preset_colors",
    "DefaultColors2": "drawlib._preset_colors",
    "DefaultColors3": "drawlib._preset_colors",
    "DefaultColors4": "drawlib._preset_colors",
    "DefaultColors5": "drawlib._preset_colors",
    "DefaultColors6": "drawlib._preset_colors",
    "GoogleColors": "drawlib._preset_colors",
    "MonochromeColors": "drawlib._preset_colors",
}


def __getattr__(name: str) -> Any:  # noqa: ANN401
    """Lazy-load color symbols on first access (PEP 562)."""
    if name in _LAZY_ATTRS:
        module = importlib.import_module(_LAZY_ATTRS[name])
        value = getattr(module, name)
        globals()[name] = value
        return value
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


def __dir__() -> list[str]:
    """Ensure lazy color symbols appear in dir() and autocompletion."""
    return sorted(__all__)


__all__ = [
    "Color",
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
    "get_intermediate_color",
    "get_intermediate_colors",
]
