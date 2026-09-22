# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GanttChart container class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from drawlib._charts._common._types import ColorType
from drawlib._charts.gantt_chart import _renderer as _renderer_module
from drawlib._charts.gantt_chart._item import (
    GanttDependency,
    GanttMarker,
    GanttMilestone,
    GanttSection,
    GanttTask,
)

if TYPE_CHECKING:
    from drawlib._core.l3_styles import Style


class GanttChart:
    """Represents a 2D Gantt project schedule chart."""

    def __init__(
        self,
        columns: list[str],
        width: float = 90.0,
        height: float | None = None,
        row_height: float = 4.5,
        header_height: float = 5.5,
        label_width: float = 24.0,
        title: str = "",
        title_style: Style | None = None,
        header_style: Style | None = None,
        grid_style: Style | None = None,
        task_style: Style | None = None,
        section_style: Style | None = None,
        show_vertical_grid: bool = True,
        show_zebra: bool = True,
        bar_radius: float = 0.8,
    ) -> None:
        """Initialize GanttChart.

        Args:
            columns: Ordered sequence of timeline interval names (e.g. months, weeks, sprints).
            width: Overall chart bounding box width. Defaults to 90.0.
            height: Overall chart bounding box height. If None, calculated from row count.
            row_height: Vertical height per task or section row. Defaults to 4.5.
            header_height: Height of the column header band. Defaults to 5.5.
            label_width: Horizontal width allocated for the left task label column. Defaults to 24.0.
            title: Title text displayed at the top. Defaults to "".
            title_style: Optional Style overriding title typography.
            header_style: Optional Style overriding header cells.
            grid_style: Optional Style overriding vertical grid divider lines.
            task_style: Optional default Style for task bars.
            section_style: Optional default Style for section divider rows.
            show_vertical_grid: Whether to draw vertical column boundary lines. Defaults to True.
            show_zebra: Whether to alternate row background colors. Defaults to True.
            bar_radius: Corner rounding radius for task bars. Defaults to 0.8.

        Raises:
            ValueError: If columns list is empty.
        """
        if not columns:
            raise ValueError("GanttChart requires at least 1 column.")

        self._columns = list(columns)
        self.width = float(width)
        self.height = float(height) if height is not None else None
        self.row_height = float(row_height)
        self.header_height = float(header_height)
        self.label_width = float(label_width)
        self.title = title
        self.title_style: Style | None = title_style
        self.header_style: Style | None = header_style
        self.grid_style: Style | None = grid_style
        self.task_style: Style | None = task_style
        self.section_style: Style | None = section_style
        self.show_vertical_grid = show_vertical_grid
        self.show_zebra = show_zebra
        self.bar_radius = float(bar_radius)

        self._items: list[GanttTask | GanttSection | GanttMilestone] = []
        self._markers: list[GanttMarker] = []
        self._dependencies: list[GanttDependency] = []

    @property
    def columns(self) -> list[str]:
        """List of timeline column labels."""
        return list(self._columns)

    @property
    def items(self) -> list[GanttTask | GanttSection | GanttMilestone]:
        """List of registered rows (tasks, sections, milestones)."""
        return list(self._items)

    @property
    def markers(self) -> list[GanttMarker]:
        """List of vertical marker lines."""
        return list(self._markers)

    @property
    def dependencies(self) -> list[GanttDependency]:
        """List of task dependency arrows."""
        return list(self._dependencies)

    def add_task(
        self,
        name: str,
        start: str | float,
        end: str | float,
        progress: float = 0.0,
        color: ColorType | None = None,
        style: Style | None = None,
        show_progress_text: bool = True,
    ) -> GanttTask:
        """Add a scheduled task to the chart.

        Args:
            name: Task name displayed in the left label column.
            start: Start column name or numerical index.
            end: End column name or numerical index.
            progress: Progress ratio from 0.0 to 1.0. Defaults to 0.0.
            color: Task bar fill color.
            style: Optional Style overriding task bar appearance.
            show_progress_text: Whether to print progress percentage. Defaults to True.

        Returns:
            GanttTask: The newly registered task item.
        """
        task = GanttTask(
            name=name,
            start=start,
            end=end,
            progress=progress,
            color=color,
            style=style or self.task_style,
            show_progress_text=show_progress_text,
        )
        self._items.append(task)
        return task

    def add_section(
        self,
        name: str,
        style: Style | None = None,
    ) -> GanttSection:
        """Add a category section divider row.

        Args:
            name: Section label text.
            style: Optional Style overriding section banner appearance.

        Returns:
            GanttSection: The newly registered section item.
        """
        section = GanttSection(
            name=name,
            style=style or self.section_style,
        )
        self._items.append(section)
        return section

    def add_milestone(
        self,
        name: str,
        at: str | float,
        color: ColorType | None = None,
        style: Style | None = None,
    ) -> GanttMilestone:
        """Add a milestone marker event.

        Args:
            name: Milestone title displayed in the label column.
            at: Column name or numerical index where the diamond is anchored.
            color: Diamond marker color.
            style: Optional Style overriding diamond appearance.

        Returns:
            GanttMilestone: The newly registered milestone item.
        """
        milestone = GanttMilestone(
            name=name,
            at=at,
            color=color,
            style=style,
        )
        self._items.append(milestone)
        return milestone

    def add_marker(
        self,
        at: str | float,
        label: str = "",
        color: ColorType | None = None,
        style: Style | None = None,
    ) -> GanttMarker:
        """Add a vertical reference highlight line (e.g. today).

        Args:
            at: Column name or numerical index where the line is anchored.
            label: Badge text displayed above the line. Defaults to "".
            color: Line color.
            style: Optional Style overriding line appearance.

        Returns:
            GanttMarker: The newly registered marker item.
        """
        marker = GanttMarker(
            at=at,
            label=label,
            color=color,
            style=style,
        )
        self._markers.append(marker)
        return marker

    def add_dependency(
        self,
        from_task: GanttTask,
        to_task: GanttTask,
        color: ColorType | None = None,
        style: Style | None = None,
    ) -> GanttDependency:
        """Add an orthogonal dependency arrow connecting two tasks.

        Args:
            from_task: Source task.
            to_task: Target task.
            color: Arrow line color.
            style: Optional Style overriding arrow appearance.

        Returns:
            GanttDependency: The newly registered dependency.
        """
        dep = GanttDependency(
            from_task=from_task,
            to_task=to_task,
            color=color,
            style=style,
        )
        self._dependencies.append(dep)
        return dep

    def get_size(self) -> tuple[float, float]:
        """Compute the total dimensions (width, height) of this chart."""
        if self.height is not None:
            return (self.width, self.height)

        title_h = 7.0 if self.title else 0.0
        padding_y = 6.0
        calculated_h = title_h + self.header_height + len(self._items) * self.row_height + padding_y
        return (self.width, max(20.0, calculated_h))

    def draw(self, xy: tuple[float, float] = (0.0, 0.0)) -> None:
        """Render this Gantt chart onto the canvas anchored at bottom-left coordinate xy.

        Args:
            xy: Base canvas placement coordinate (x, y) where the bottom-left corner is anchored.
        """
        _renderer_module.draw_gantt_chart(self, xy)
