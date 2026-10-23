# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Font icons internal package."""

from __future__ import annotations

import importlib
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from drawlib._icons.font_icons import phosphor
    from drawlib._icons.font_icons._font_icon import font_icon


def __getattr__(name: str) -> Any:  # noqa: ANN401
    """Lazy-load font icon symbols on first access (PEP 562)."""
    if name == "phosphor":
        module = importlib.import_module("drawlib._icons.font_icons.phosphor")
        globals()[name] = module
        return module
    if name == "font_icon":
        from drawlib._icons.font_icons._font_icon import font_icon  # noqa: PLC0415

        globals()[name] = font_icon
        return font_icon
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


def __dir__() -> list[str]:
    """Ensure lazy font icon symbols appear in dir() and autocompletion."""
    return sorted(__all__)


__all__ = [
    "font_icon",
    "phosphor",
]
