# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Public charts package for drawlib."""

from __future__ import annotations

import importlib
from typing import TYPE_CHECKING, Any, Final

if TYPE_CHECKING:
    from drawlib._charts._common._types import DrawDirection
    from drawlib.charts import (
        area,
        bar,
        gantt,
        heatmap,
        line,
        pie,
        radar,
        scatter,
    )

_LAZY_MODULES: Final[dict[str, str]] = {
    "area": "drawlib.charts.area",
    "bar": "drawlib.charts.bar",
    "gantt": "drawlib.charts.gantt",
    "heatmap": "drawlib.charts.heatmap",
    "line": "drawlib.charts.line",
    "pie": "drawlib.charts.pie",
    "radar": "drawlib.charts.radar",
    "scatter": "drawlib.charts.scatter",
}


def __getattr__(name: str) -> Any:  # noqa: ANN401
    """Lazy-load chart submodules and types on first access (PEP 562)."""
    if name in _LAZY_MODULES:
        module = importlib.import_module(_LAZY_MODULES[name])
        globals()[name] = module
        return module
    if name == "DrawDirection":
        from drawlib._charts._common._types import DrawDirection  # noqa: PLC0415

        globals()[name] = DrawDirection
        return DrawDirection
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


def __dir__() -> list[str]:
    """Ensure lazy chart submodules appear in dir() and autocompletion."""
    return sorted(__all__)


__all__ = [
    "DrawDirection",
    "area",
    "bar",
    "gantt",
    "heatmap",
    "line",
    "pie",
    "radar",
    "scatter",
]
