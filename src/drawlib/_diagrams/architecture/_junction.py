# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Junction class implementation for architecture diagrams."""

from __future__ import annotations

from typing import TYPE_CHECKING

import drawlib._diagrams.architecture._edge as _edge_module
from drawlib._diagrams.architecture._types import ArrowType, Connectable, PaddingType, RoutingType

if TYPE_CHECKING:
    from drawlib._core.l3_styles import Style
    from drawlib._diagrams.architecture._diagram import ArchitectureDiagram
    from drawlib._diagrams.architecture._edge import Edge
    from drawlib._diagrams.architecture._group import NodeGroup


class Junction:
    """Lightweight connectable waypoint / branch point in an architecture diagram."""

    def __init__(self, xy: tuple[float, float]) -> None:
        """Initialize Junction.

        Args:
            xy: Local coordinate (x, y) of the junction point.
        """
        self._local_xy = (float(xy[0]), float(xy[1]))
        self._diagram: ArchitectureDiagram | None = None
        self._parent_group: NodeGroup | None = None

    @property
    def xy(self) -> tuple[float, float]:
        """Get the relative coordinate (x, y) of this junction."""
        return self._local_xy

    @property
    def center(self) -> tuple[float, float]:
        """Get the center coordinate of this junction."""
        return self._local_xy

    @property
    def top(self) -> tuple[float, float]:
        """Get the top anchor coordinate of this junction."""
        return self._local_xy

    @property
    def bottom(self) -> tuple[float, float]:
        """Get the bottom anchor coordinate of this junction."""
        return self._local_xy

    @property
    def left(self) -> tuple[float, float]:
        """Get the left anchor coordinate of this junction."""
        return self._local_xy

    @property
    def right(self) -> tuple[float, float]:
        """Get the right anchor coordinate of this junction."""
        return self._local_xy

    def get_bounds(self) -> tuple[float, float, float, float]:  # noqa: PLR6301
        """Get visual bounding box [min_x, min_y, max_x, max_y] of the junction (always 0, 0, 0, 0)."""
        return (0.0, 0.0, 0.0, 0.0)

    def get_size(self) -> tuple[float, float]:  # noqa: PLR6301
        """Get visual size of the junction (always 0, 0)."""
        return (0.0, 0.0)

    def connect(
        self,
        target: Connectable,
        label: str = "",
        arrow: ArrowType = "->",
        routing: RoutingType = "orthogonal",
        style: Style | None = None,
        padding: PaddingType = 0.0,
    ) -> Edge:
        """Connect this junction to a target element.

        Args:
            target: Target Node, NodeGroup, or Junction.
            label: Connection label text.
            arrow: Arrowhead direction ("->", "<-", "<->", "-").
            routing: Path routing strategy ("orthogonal", "direct", "curved").
            style: Optional Style object for the line.
            padding: Gap distance between nodes and line ends (float or (start, end) tuple).

        Returns:
            Edge: Created connection object.
        """
        edge = _edge_module.Edge(
            start=self,
            end=target,
            label=label,
            arrow=arrow,
            routing=routing,
            style=style,
            padding=padding,
        )
        if self._diagram is not None:
            self._diagram.add_edge(edge)
        elif hasattr(target, "_diagram") and target._diagram is not None:
            target._diagram.add_edge(edge)
        return edge
