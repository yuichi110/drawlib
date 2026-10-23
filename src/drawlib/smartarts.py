# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Public smartarts module for drawlib."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from drawlib._smartarts import (
        BoxList,
        BoxListItem,
        BulletPointItem,
        BulletPoints,
        CalendarItem,
        CardList,
        CardListItem,
        ChevronItem,
        ChevronProcess,
        Cycle,
        CycleCenter,
        CycleItem,
        DayCalendar,
        GeoMap,
        GridItem,
        GridLayout,
        KpiCard,
        KpiCardItem,
        KpiCards,
        MindMapNode,
        MonthCalendar,
        Panel,
        Pyramid,
        PyramidItem,
        Roadmap,
        RoadmapItem,
        SourceCode,
        SourceCodeStyles,
        Table,
        TreeNode,
        WeekCalendar,
        get_source_code_styles,
        sourcecode,
    )


def __getattr__(name: str) -> Any:  # noqa: ANN401
    """Lazy-load SmartArt components on first access (PEP 562)."""
    if name in __all__:
        from drawlib import _smartarts  # noqa: PLC0415

        value = getattr(_smartarts, name)
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
