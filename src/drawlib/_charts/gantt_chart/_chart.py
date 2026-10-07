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

from pydantic import validate_call

from drawlib._charts._common._base import draw_with_box_overrides
from drawlib._charts._common._types import DrawDirection
from drawlib._charts.gantt_chart import _renderer as _renderer_module
from drawlib._charts.gantt_chart._item import (
    Dependency,
    Marker,
    Milestone,
    Section,
    Task,
)
from drawlib._core.l3_styles import Style


class GanttChart:
    """Represents a 2D Gantt project schedule chart."""

    @validate_call
    def __init__(
        self,
        *,
        columns: list[str],
        axis_line_style: Style,
        axis_text_style: Style | None = None,
        header_style: Style | None = None,
        grid_style: Style | None = None,
        zebra_style: Style | None = None,
        progress_text_style: Style | None = None,
        background_style: Style | None = None,
        title: str = "",
        title_style: Style | None = None,
        width: float = 90.0,
        height: float | None = None,
        row_height: float = 4.5,
        header_height: float = 5.5,
        label_width: float = 24.0,
        bar_radius: float = 0.8,
    ) -> None:
        """Initialize GanttChart.

        Args:
            columns: Ordered sequence of timeline interval names (e.g. months, weeks, sprints).
            axis_line_style: Required Style for header dividing lines and table axis lines.
            axis_text_style: Optional Style for column header and task label typography.
            header_style: Optional Style overriding header row background card.
            grid_style: Optional Style for vertical timeline gridlines. If None, vertical lines are omitted.
            zebra_style: Optional Style for alternating row backgrounds. If None, zebra striping is omitted.
            progress_text_style: Optional Style for progress percentage text on task bars.
            background_style: Optional Style for chart background card.
            title: Title text displayed at the top. Defaults to "".
            title_style: Optional Style overriding title typography.
            width: Overall chart bounding box width. Defaults to 90.0.
            height: Overall chart bounding box height. If None, calculated from row count.
            row_height: Vertical height per task or section row. Defaults to 4.5.
            header_height: Height of the column header band. Defaults to 5.5.
            label_width: Horizontal width allocated for the left task label column. Defaults to 24.0.
            bar_radius: Corner rounding radius for task bars. Defaults to 0.8.

        Raises:
            ValueError: If columns list is empty.
        """
        if not columns:
            raise ValueError("GanttChart requires at least 1 column.")

        self._columns = list(columns)
        self.axis_line_style: Style = axis_line_style
        self.axis_text_style: Style | None = axis_text_style
        self.header_style: Style | None = header_style
        self.grid_style: Style | None = grid_style
        self.zebra_style: Style | None = zebra_style
        self.progress_text_style: Style | None = progress_text_style
        self.background_style: Style | None = background_style
        self.title = title
        self.title_style: Style | None = title_style

        self.width = float(width)
        self.height = float(height) if height is not None else None
        self.row_height = float(row_height)
        self.header_height = float(header_height)
        self.label_width = float(label_width)
        self.bar_radius = float(bar_radius)

        self._items: list[Task | Section | Milestone] = []
        self._markers: list[Marker] = []
        self._dependencies: list[Dependency] = []

    @property
    def columns(self) -> list[str]:
        """List of timeline column labels."""
        return list(self._columns)

    @property
    def items(self) -> list[Task | Section | Milestone]:
        """List of registered rows (tasks, sections, milestones)."""
        return list(self._items)

    @property
    def markers(self) -> list[Marker]:
        """List of vertical marker lines."""
        return list(self._markers)

    @property
    def dependencies(self) -> list[Dependency]:
        """List of task dependency arrows."""
        return list(self._dependencies)

    def add_task(
        self,
        name: str,
        start: str | float,
        end: str | float,
        style: Style,
        progress: float = 0.0,
        progress_text_style: Style | None = None,
        *,
        show: bool = True,
        draw_ratio: float = 1.0,
        draw_direction: DrawDirection = "left_to_right",
    ) -> Task:
        """Add a scheduled task to the chart.

        Args:
            name: Task name displayed in the left label column.
            start: Start column name or numerical index.
            end: End column name or numerical index.
            style: Style defining task bar appearance.
            progress: Progress ratio from 0.0 to 1.0. Defaults to 0.0.
            progress_text_style: Optional Style for progress percentage text.
            show: Whether this task is rendered. Defaults to True.
            draw_ratio: Spatial rendering progress ratio in [0.0, 1.0]. Defaults to 1.0.
            draw_direction: Direction of partial rendering ("left_to_right" or "bottom_to_top").

        Returns:
            Task: The newly registered task item.
        """
        task = Task(
            name=name,
            start=start,
            end=end,
            style=style,
            progress=progress,
            progress_text_style=progress_text_style,
            show=show,
            draw_ratio=draw_ratio,
            draw_direction=draw_direction,
        )
        self._items.append(task)
        return task

    def add_section(
        self,
        name: str,
        style: Style | None = None,
        text_style: Style | None = None,
        *,
        show: bool = True,
    ) -> Section:
        """Add a category section divider row.

        Args:
            name: Section label text.
            style: Optional Style overriding section banner appearance.
            text_style: Optional Style overriding section text typography.
            show: Whether this section is rendered. Defaults to True.

        Returns:
            Section: The newly registered section item.
        """
        section = Section(
            name=name,
            style=style,
            text_style=text_style,
            show=show,
        )
        self._items.append(section)
        return section

    def add_milestone(
        self,
        name: str,
        at: str | float,
        style: Style,
        *,
        show: bool = True,
    ) -> Milestone:
        """Add a milestone marker event.

        Args:
            name: Milestone title displayed in the label column.
            at: Column name or numerical index where the diamond is anchored.
            style: Style defining diamond marker appearance.
            show: Whether this milestone is rendered. Defaults to True.

        Returns:
            Milestone: The newly registered milestone item.
        """
        milestone = Milestone(
            name=name,
            at=at,
            style=style,
            show=show,
        )
        self._items.append(milestone)
        return milestone

    def add_marker(
        self,
        at: str | float,
        style: Style,
        label: str = "",
        label_style: Style | None = None,
        *,
        show: bool = True,
    ) -> Marker:
        """Add a vertical reference highlight line (e.g. today).

        Args:
            at: Column name or numerical index where the line is anchored.
            style: Style defining line appearance.
            label: Badge text displayed above the line. Defaults to "".
            label_style: Optional Style for marker label text.
            show: Whether this marker is rendered. Defaults to True.

        Returns:
            Marker: The newly registered marker item.
        """
        marker = Marker(
            at=at,
            style=style,
            label=label,
            label_style=label_style,
            show=show,
        )
        self._markers.append(marker)
        return marker

    def add_dependency(
        self,
        from_task: Task,
        to_task: Task,
        style: Style | None = None,
        *,
        show: bool = True,
    ) -> Dependency:
        """Add an orthogonal dependency arrow connecting two tasks.

        Args:
            from_task: Source task.
            to_task: Target task.
            style: Optional Style overriding arrow appearance.
            show: Whether this dependency arrow is rendered. Defaults to True.

        Returns:
            Dependency: The newly registered dependency.
        """
        dep = Dependency(
            from_task=from_task,
            to_task=to_task,
            style=style,
            show=show,
        )
        self._dependencies.append(dep)
        return dep

    def get_size(self) -> tuple[float, float]:
        """Compute the total dimensions (width, height) of this chart."""
        if self.height is not None:
            return (self.width, self.height)

        title_h = 7.0 if (self.title and self.title_style is not None) else 0.0
        padding_y = 6.0
        calculated_h = title_h + self.header_height + len(self._items) * self.row_height + padding_y
        return (self.width, max(20.0, calculated_h))

    def draw(
        self,
        xy: tuple[float, float] = (0.0, 0.0),
        *,
        width: float | None = None,
        height: float | None = None,
        scale: float = 1.0,
    ) -> None:
        """Render this Gantt chart onto the canvas anchored at bottom-left coordinate xy.

        Args:
            xy: Base canvas placement coordinate (x, y) where the bottom-left corner is anchored.
            width: Optional temporary override for chart container width.
            height: Optional temporary override for chart container height.
            scale: Uniform scaling factor applied around xy. Defaults to 1.0.
        """
        draw_with_box_overrides(
            self,
            _renderer_module.draw_gantt_chart,
            xy,
            width=width,
            height=height,
            scale=scale,
        )
