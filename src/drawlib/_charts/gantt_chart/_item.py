# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Item models for GanttChart (tasks, sections, milestones, markers, dependencies)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from drawlib._charts._common._types import ColorType

if TYPE_CHECKING:
    from drawlib._core.l3_styles import Style


class GanttTask:
    """Represents a scheduled task spanning a start and end time interval."""

    def __init__(
        self,
        name: str,
        start: str | float,
        end: str | float,
        progress: float = 0.0,
        color: ColorType | None = None,
        style: Style | None = None,
        show_progress_text: bool = True,
    ) -> None:
        """Initialize GanttTask.

        Args:
            name: Label displayed on the left column.
            start: Start column name or numerical time index.
            end: End column name or numerical time index.
            progress: Completion ratio from 0.0 to 1.0. Defaults to 0.0.
            color: Base color for task bar fill.
            style: Optional Style overriding task bar appearance.
            show_progress_text: Whether to print progress percentage on bar. Defaults to True.
        """
        self.name = name
        self.start = start
        self.end = end
        self.progress = max(0.0, min(1.0, float(progress)))
        self.color: ColorType | None = color
        self.style: Style | None = style
        self.show_progress_text = show_progress_text

        # Layout cache populated during rendering
        self._cached_start_x: float = 0.0
        self._cached_end_x: float = 0.0
        self._cached_row_y: float = 0.0


class GanttSection:
    """Represents a category section divider row in the Gantt chart."""

    def __init__(
        self,
        name: str,
        style: Style | None = None,
    ) -> None:
        """Initialize GanttSection.

        Args:
            name: Section title displayed across the row.
            style: Optional Style overriding section banner appearance.
        """
        self.name = name
        self.style: Style | None = style

        # Layout cache
        self._cached_row_y: float = 0.0


class GanttMilestone:
    """Represents a zero-duration milestone event in time."""

    def __init__(
        self,
        name: str,
        at: str | float,
        color: ColorType | None = None,
        style: Style | None = None,
    ) -> None:
        """Initialize GanttMilestone.

        Args:
            name: Milestone title displayed in the label column.
            at: Column name or numerical time index where diamond is placed.
            color: Marker color.
            style: Optional Style overriding diamond appearance.
        """
        self.name = name
        self.at = at
        self.color: ColorType | None = color
        self.style: Style | None = style

        # Layout cache
        self._cached_at_x: float = 0.0
        self._cached_row_y: float = 0.0


class GanttMarker:
    """Represents a vertical reference line across all rows (e.g. today)."""

    def __init__(
        self,
        at: str | float,
        label: str = "",
        color: ColorType | None = None,
        style: Style | None = None,
    ) -> None:
        """Initialize GanttMarker.

        Args:
            at: Column name or numerical time index where line is placed.
            label: Text badge rendered above or next to the line.
            color: Vertical line color.
            style: Optional Style overriding marker appearance.
        """
        self.at = at
        self.label = label
        self.color: ColorType | None = color
        self.style: Style | None = style


class GanttDependency:
    """Represents an orthogonal arrow linking two dependent tasks."""

    def __init__(
        self,
        from_task: GanttTask,
        to_task: GanttTask,
        color: ColorType | None = None,
        style: Style | None = None,
    ) -> None:
        """Initialize GanttDependency.

        Args:
            from_task: Predecessor task whose completion triggers to_task.
            to_task: Successor task whose start depends on from_task.
            color: Arrow line stroke color.
            style: Optional Style overriding link appearance.
        """
        self.from_task = from_task
        self.to_task = to_task
        self.color: ColorType | None = color
        self.style: Style | None = style
