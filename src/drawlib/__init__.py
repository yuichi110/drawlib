# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Root package."""

from __future__ import annotations

import importlib
from typing import TYPE_CHECKING, Any, Final

from drawlib._core.l1_core._const import LIB_NAME, LIB_VERSION

__version__: Final[str] = LIB_VERSION

if TYPE_CHECKING:
    from drawlib import (
        anim,
        canvas,
        charts,
        diagrams,
        fonts,
        graph,
        icons,
        images,
        lines,
        math,
        preset_colors,
        preset_styles,
        shapes,
        slide,
        smartarts,
        styles,
        text,
        tools,
        types,
        utils,
    )

_LAZY_MODULES: Final[dict[str, str]] = {
    "anim": "drawlib.anim",
    "canvas": "drawlib.canvas",
    "charts": "drawlib.charts",
    "diagrams": "drawlib.diagrams",
    "fonts": "drawlib.fonts",
    "graph": "drawlib.graph",
    "icons": "drawlib.icons",
    "images": "drawlib.images",
    "lines": "drawlib.lines",
    "math": "drawlib.math",
    "preset_colors": "drawlib.preset_colors",
    "preset_styles": "drawlib.preset_styles",
    "shapes": "drawlib.shapes",
    "slide": "drawlib.slide",
    "smartarts": "drawlib.smartarts",
    "styles": "drawlib.styles",
    "text": "drawlib.text",
    "tools": "drawlib.tools",
    "types": "drawlib.types",
    "utils": "drawlib.utils",
}


def __getattr__(name: str) -> Any:  # noqa: ANN401
    """Lazy-load submodules on first attribute access (PEP 562)."""
    if name in _LAZY_MODULES:
        module = importlib.import_module(_LAZY_MODULES[name])
        globals()[name] = module
        return module
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


def __dir__() -> list[str]:
    """Ensure lazy modules appear in dir() and REPL autocompletion."""
    return sorted(__all__)


__all__ = [
    "LIB_NAME",
    "LIB_VERSION",
    "__version__",
    "anim",
    "canvas",
    "charts",
    "diagrams",
    "fonts",
    "graph",
    "icons",
    "images",
    "lines",
    "math",
    "preset_colors",
    "preset_styles",
    "shapes",
    "slide",
    "smartarts",
    "styles",
    "text",
    "tools",
    "types",
    "utils",
]
