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

from typing import TYPE_CHECKING

from drawlib._charts._common._types import PointShape

if TYPE_CHECKING:
    from drawlib._core.l3_styles import Style


class ScatterPoint:
    """Represents a single data point in a ScatterChart."""

    def __init__(
        self,
        xy: tuple[float, float],
        radius: float = 1.0,
        style: Style | None = None,
        shape: PointShape = "circle",
        label: str = "",
        label_style: Style | None = None,
    ) -> None:
        """Initialize ScatterPoint.

        Args:
            xy: Numerical data coordinate tuple (x, y).
            radius: Visual radius of the point marker. Defaults to 1.0.
            style: Optional Style overriding marker appearance.
            shape: Marker shape ("circle", "square", "rhombus", "triangle"). Defaults to "circle".
            label: Optional text label displayed next to the point.
            label_style: Optional Style for the label text.
        """
        self.xy: tuple[float, float] = (float(xy[0]), float(xy[1]))
        self.radius: float = float(radius)
        self.style: Style | None = style
        self.shape: PointShape = shape
        self.label: str = label
        self.label_style: Style | None = label_style


class ScatterSeries:
    """Represents a named group of scatter points."""

    def __init__(
        self,
        name: str,
        points: list[ScatterPoint],
        style: Style | None = None,
        radius: float = 1.0,
        shape: PointShape = "circle",
    ) -> None:
        """Initialize ScatterSeries.

        Args:
            name: Group name displayed in chart legend.
            points: List of ScatterPoint instances belonging to this series.
            style: Optional Style applied to points in this series.
            radius: Default radius for points in this series. Defaults to 1.0.
            shape: Default shape for points in this series. Defaults to "circle".
        """
        self.name: str = name
        self.points: list[ScatterPoint] = points
        self.style: Style | None = style
        self.radius: float = float(radius)
        self.shape: PointShape = shape
