# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Package for smart arts modules."""

from __future__ import annotations

import importlib
from typing import TYPE_CHECKING, Any, Final

if TYPE_CHECKING:
    from drawlib._smartarts._boxlist import BoxList, BoxListItem
    from drawlib._smartarts._bulletpoints import BulletPointItem, BulletPoints
    from drawlib._smartarts._calendar import (
        CalendarItem,
        DayCalendar,
        MonthCalendar,
        WeekCalendar,
    )
    from drawlib._smartarts._cardlist import CardList, CardListItem
    from drawlib._smartarts._chevronprocess import ChevronItem, ChevronProcess
    from drawlib._smartarts._cycle import Cycle, CycleCenter, CycleItem
    from drawlib._smartarts._geomap import GeoMap
    from drawlib._smartarts._gridlayout import GridItem, GridLayout
    from drawlib._smartarts._kpicards import KpiCard, KpiCardItem, KpiCards
    from drawlib._smartarts._mindmap import MindMapNode
    from drawlib._smartarts._panel import Panel
    from drawlib._smartarts._pyramid import Pyramid, PyramidItem
    from drawlib._smartarts._roadmap import Roadmap, RoadmapItem
    from drawlib._smartarts._sourcecode import (
        SourceCode,
        SourceCodeStyles,
        get_source_code_styles,
        sourcecode,
    )
    from drawlib._smartarts._table import Table
    from drawlib._smartarts._tree import TreeNode

_LAZY_ATTRS: Final[dict[str, str]] = {
    "BoxList": "drawlib._smartarts._boxlist",
    "BoxListItem": "drawlib._smartarts._boxlist",
    "BulletPointItem": "drawlib._smartarts._bulletpoints",
    "BulletPoints": "drawlib._smartarts._bulletpoints",
    "CalendarItem": "drawlib._smartarts._calendar",
    "DayCalendar": "drawlib._smartarts._calendar",
    "MonthCalendar": "drawlib._smartarts._calendar",
    "WeekCalendar": "drawlib._smartarts._calendar",
    "CardList": "drawlib._smartarts._cardlist",
    "CardListItem": "drawlib._smartarts._cardlist",
    "ChevronItem": "drawlib._smartarts._chevronprocess",
    "ChevronProcess": "drawlib._smartarts._chevronprocess",
    "Cycle": "drawlib._smartarts._cycle",
    "CycleCenter": "drawlib._smartarts._cycle",
    "CycleItem": "drawlib._smartarts._cycle",
    "GeoMap": "drawlib._smartarts._geomap",
    "GridItem": "drawlib._smartarts._gridlayout",
    "GridLayout": "drawlib._smartarts._gridlayout",
    "KpiCard": "drawlib._smartarts._kpicards",
    "KpiCardItem": "drawlib._smartarts._kpicards",
    "KpiCards": "drawlib._smartarts._kpicards",
    "MindMapNode": "drawlib._smartarts._mindmap",
    "Panel": "drawlib._smartarts._panel",
    "Pyramid": "drawlib._smartarts._pyramid",
    "PyramidItem": "drawlib._smartarts._pyramid",
    "Roadmap": "drawlib._smartarts._roadmap",
    "RoadmapItem": "drawlib._smartarts._roadmap",
    "SourceCode": "drawlib._smartarts._sourcecode",
    "SourceCodeStyles": "drawlib._smartarts._sourcecode",
    "get_source_code_styles": "drawlib._smartarts._sourcecode",
    "sourcecode": "drawlib._smartarts._sourcecode",
    "Table": "drawlib._smartarts._table",
    "TreeNode": "drawlib._smartarts._tree",
}


def __getattr__(name: str) -> Any:  # noqa: ANN401
    """Lazy-load SmartArt classes and helpers on first access (PEP 562)."""
    if name in _LAZY_ATTRS:
        module = importlib.import_module(_LAZY_ATTRS[name])
        value = getattr(module, name)
        globals()[name] = value
        return value
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


def __dir__() -> list[str]:
    """Ensure lazy SmartArt attributes appear in dir() and autocompletion."""
    return sorted(__all__)


__all__ = [
    "BoxList",
    "BoxListItem",
    "BulletPointItem",
    "BulletPoints",
    "CalendarItem",
    "CardList",
    "CardListItem",
    "ChevronItem",
    "ChevronProcess",
    "Cycle",
    "CycleCenter",
    "CycleItem",
    "DayCalendar",
    "GeoMap",
    "GridItem",
    "GridLayout",
    "KpiCard",
    "KpiCardItem",
    "KpiCards",
    "MindMapNode",
    "MonthCalendar",
    "Panel",
    "Pyramid",
    "PyramidItem",
    "Roadmap",
    "RoadmapItem",
    "SourceCode",
    "SourceCodeStyles",
    "Table",
    "TreeNode",
    "WeekCalendar",
    "get_source_code_styles",
    "sourcecode",
]
