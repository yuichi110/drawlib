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

import importlib
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from drawlib.preset_colors import (
        Color,
        DefaultColors,
        get_intermediate_color,
        get_intermediate_colors,
    )
    from drawlib.preset_styles import DefaultStyles, Style

    Colors: DefaultColors
    Styles: DefaultStyles

_LAZY_ATTRS: dict[str, tuple[str, str]] = {
    "Color": ("drawlib.preset_colors", "Color"),
    "Style": ("drawlib.preset_styles", "Style"),
    "get_intermediate_color": ("drawlib.preset_colors", "get_intermediate_color"),
    "get_intermediate_colors": ("drawlib.preset_colors", "get_intermediate_colors"),
}

__all__ = [
    "Color",
    "Colors",
    "Style",
    "Styles",
    "get_intermediate_color",
    "get_intermediate_colors",
]


def __getattr__(name: str) -> Any:  # noqa: ANN401
    if name == "Colors":
        from drawlib.preset_colors import DefaultColors  # noqa: PLC0415

        val = DefaultColors()
        globals()["Colors"] = val
        return val
    if name == "Styles":
        from drawlib.preset_styles import DefaultStyles  # noqa: PLC0415

        val = DefaultStyles()
        globals()["Styles"] = val
        return val
    target = _LAZY_ATTRS.get(name)
    if target is not None:
        mod_path, attr_name = target
        mod = importlib.import_module(mod_path)
        val = getattr(mod, attr_name)
        globals()[name] = val
        return val
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(__all__))
