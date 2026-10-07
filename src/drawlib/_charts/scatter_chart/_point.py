# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Point and series data containers for ScatterChart."""

from __future__ import annotations

from drawlib._charts._common._types import DrawDirection, PointShape
from drawlib._core.l3_styles import Style


class Point:
    """Represents a single data point in a ScatterChart."""

    def __init__(
        self,
        xy: tuple[float, float],
        style: Style,
        radius: float = 1.0,
        shape: PointShape = "circle",
        label: str = "",
        label_style: Style | None = None,
        *,
        show: bool = True,
    ) -> None:
        """Initialize Point.

        Args:
            xy: Numerical data coordinate tuple (x, y).
            style: Style defining marker outline and fill.
            radius: Visual radius of the point marker. Defaults to 1.0.
            shape: Marker shape ("circle", "square", "rhombus", "triangle"). Defaults to "circle".
            label: Optional text label displayed next to the point.
            label_style: Optional Style for the label text.
            show: Whether to render this point on the canvas. Defaults to True.
        """
        self.xy: tuple[float, float] = (float(xy[0]), float(xy[1]))
        self.style: Style = style
        self.radius: float = float(radius)
        self.shape: PointShape = shape
        self.label: str = label
        self.label_style: Style | None = label_style
        self.show: bool = bool(show)


class Series:
    """Represents a named group of scatter points."""

    def __init__(
        self,
        name: str,
        points: list[Point],
        style: Style,
        radius: float = 1.0,
        shape: PointShape = "circle",
        legend_text_style: Style | None = None,
        *,
        show: bool = True,
        draw_ratio: float = 1.0,
        draw_direction: DrawDirection = "left_to_right",
    ) -> None:
        """Initialize Series.

        Args:
            name: Group name displayed in chart legend.
            points: List of Point instances belonging to this series.
            style: Style applied to points in this series.
            radius: Default radius for points in this series. Defaults to 1.0.
            shape: Default shape for points in this series. Defaults to "circle".
            legend_text_style: Optional custom text style for this series in legend.
            show: Whether to render this series on the canvas. Defaults to True.
            draw_ratio: Spatial rendering ratio from 0.0 to 1.0. Defaults to 1.0.
            draw_direction: Partial rendering direction ("left_to_right" or "bottom_to_top").
        """
        self.name: str = name
        self.points: list[Point] = points
        self.style: Style = style
        self.radius: float = float(radius)
        self.shape: PointShape = shape
        self.legend_text_style: Style | None = legend_text_style
        self.show: bool = bool(show)
        self.draw_ratio: float = float(draw_ratio)
        self.draw_direction: DrawDirection = draw_direction
