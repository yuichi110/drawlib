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

if TYPE_CHECKING:
    from drawlib._core.l3_styles import Style


class Task:
    """Represents a scheduled task spanning a start and end time interval."""

    def __init__(
        self,
        name: str,
        start: str | float,
        end: str | float,
        style: Style,
        progress: float = 0.0,
        progress_text_style: Style | None = None,
    ) -> None:
        """Initialize Task.

        Args:
            name: Label displayed on the left column.
            start: Start column name or numerical time index.
            end: End column name or numerical time index.
            style: Style defining task bar appearance.
            progress: Completion ratio from 0.0 to 1.0. Defaults to 0.0.
            progress_text_style: Optional Style for progress percentage text.
        """
        self.name = name
        self.start = start
        self.end = end
        self.style: Style = style
        self.progress = max(0.0, min(1.0, float(progress)))
        self.progress_text_style: Style | None = progress_text_style

        # Layout cache populated during rendering
        self._cached_start_x: float = 0.0
        self._cached_end_x: float = 0.0
        self._cached_row_y: float = 0.0


class Section:
    """Represents a category section divider row in the Gantt chart."""

    def __init__(
        self,
        name: str,
        style: Style | None = None,
        text_style: Style | None = None,
    ) -> None:
        """Initialize Section.

        Args:
            name: Section title displayed across the row.
            style: Optional Style overriding section banner appearance.
            text_style: Optional Style overriding section text typography.
        """
        self.name = name
        self.style: Style | None = style
        self.text_style: Style | None = text_style

        # Layout cache
        self._cached_row_y: float = 0.0


class Milestone:
    """Represents a zero-duration milestone event in time."""

    def __init__(
        self,
        name: str,
        at: str | float,
        style: Style,
    ) -> None:
        """Initialize Milestone.

        Args:
            name: Milestone title displayed in the label column.
            at: Column name or numerical time index where diamond is placed.
            style: Style defining diamond marker appearance.
        """
        self.name = name
        self.at = at
        self.style: Style = style

        # Layout cache
        self._cached_at_x: float = 0.0
        self._cached_row_y: float = 0.0


class Marker:
    """Represents a vertical reference line across all rows (e.g. today)."""

    def __init__(
        self,
        at: str | float,
        style: Style,
        label: str = "",
        label_style: Style | None = None,
    ) -> None:
        """Initialize Marker.

        Args:
            at: Column name or numerical time index where line is placed.
            style: Style defining marker line appearance.
            label: Text badge rendered above or next to the line. Defaults to "".
            label_style: Optional Style for marker label text.
        """
        self.at = at
        self.style: Style = style
        self.label = label
        self.label_style: Style | None = label_style


class Dependency:
    """Represents an orthogonal arrow linking two dependent tasks."""

    def __init__(
        self,
        from_task: Task,
        to_task: Task,
        style: Style | None = None,
    ) -> None:
        """Initialize Dependency.

        Args:
            from_task: Predecessor task whose completion triggers to_task.
            to_task: Successor task whose start depends on from_task.
            style: Optional Style overriding link appearance.
        """
        self.from_task = from_task
        self.to_task = to_task
        self.style: Style | None = style
