# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Public preset_styles module for drawlib."""

from __future__ import annotations

import importlib
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from drawlib._core.l3_styles import Style
    from drawlib._preset_styles import (
        DefaultStyles,
        DefaultStyles1,
        DefaultStyles2,
        DefaultStyles3,
        DefaultStyles4,
        DefaultStyles5,
        DefaultStyles6,
        GoogleStyles,
        MonochromeStyles,
    )

_LAZY_ATTRS: dict[str, tuple[str, str]] = {
    "Style": ("drawlib._core.l3_styles", "Style"),
    "DefaultStyles": ("drawlib._preset_styles", "DefaultStyles"),
    "DefaultStyles1": ("drawlib._preset_styles", "DefaultStyles1"),
    "DefaultStyles2": ("drawlib._preset_styles", "DefaultStyles2"),
    "DefaultStyles3": ("drawlib._preset_styles", "DefaultStyles3"),
    "DefaultStyles4": ("drawlib._preset_styles", "DefaultStyles4"),
    "DefaultStyles5": ("drawlib._preset_styles", "DefaultStyles5"),
    "DefaultStyles6": ("drawlib._preset_styles", "DefaultStyles6"),
    "GoogleStyles": ("drawlib._preset_styles", "GoogleStyles"),
    "MonochromeStyles": ("drawlib._preset_styles", "MonochromeStyles"),
}

__all__ = [
    "DefaultStyles",
    "DefaultStyles1",
    "DefaultStyles2",
    "DefaultStyles3",
    "DefaultStyles4",
    "DefaultStyles5",
    "DefaultStyles6",
    "GoogleStyles",
    "MonochromeStyles",
    "Style",
]


def __getattr__(name: str) -> Any:  # noqa: ANN401
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
