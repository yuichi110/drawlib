# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Junction class implementation for flow diagrams."""

from __future__ import annotations

from typing import TYPE_CHECKING

import drawlib._diagrams.flow._edge as _edge_module
from drawlib._diagrams.flow._types import ArrowType, Connectable, PaddingType, RoutingType, Side

if TYPE_CHECKING:
    from drawlib._core.types import Style
    from drawlib._diagrams.flow._diagram import FlowDiagram
    from drawlib._diagrams.flow._edge import FlowEdge


class Junction:
    """Lightweight connectable waypoint / branch point in a flow diagram."""

    def __init__(self, xy: tuple[float, float]) -> None:
        """Initialize Junction.

        Args:
            xy: Local coordinate (x, y) of the junction point.
        """
        self._local_xy = (float(xy[0]), float(xy[1]))
        self._diagram: FlowDiagram | None = None

    @property
    def xy(self) -> tuple[float, float]:
        """Get relative coordinate (x, y) of this junction."""
        return self._local_xy

    @property
    def center(self) -> tuple[float, float]:
        """Get center coordinate of this junction."""
        return self._local_xy

    @property
    def top(self) -> tuple[float, float]:
        """Get top anchor coordinate of this junction."""
        return self._local_xy

    @property
    def bottom(self) -> tuple[float, float]:
        """Get bottom anchor coordinate of this junction."""
        return self._local_xy

    @property
    def left(self) -> tuple[float, float]:
        """Get left anchor coordinate of this junction."""
        return self._local_xy

    @property
    def right(self) -> tuple[float, float]:
        """Get right anchor coordinate of this junction."""
        return self._local_xy

    def get_anchor(self, side: Side = "auto") -> tuple[float, float]:  # noqa: ARG002
        """Get anchor coordinate for this junction (always returns xy)."""
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
        arrow: ArrowType | None = None,
        routing: RoutingType = "orthogonal",
        start_side: Side = "auto",
        end_side: Side = "auto",
        style: Style | None = None,
        textstyle: Style | None = None,
        padding: PaddingType = 0.0,
    ) -> FlowEdge:
        """Connect this junction to a target element.

        Args:
            target: Target FlowNode or Junction.
            label: Connection label text.
            arrow: Arrowhead direction ("->", "<-", "<->", "-"). Defaults to "-" if target is Junction, else "->".
            routing: Path routing strategy ("orthogonal" or "direct").
            start_side: Exit side on junction.
            end_side: Entry side on target.
            style: Optional Style object for the line.
            textstyle: Optional Style object for label text.
            padding: Gap distance between elements and line ends.

        Returns:
            FlowEdge: Created connection object.
        """
        edge = _edge_module.FlowEdge(
            start=self,
            end=target,
            label=label,
            arrow=arrow,
            routing=routing,
            start_side=start_side,
            end_side=end_side,
            style=style,
            textstyle=textstyle,
            padding=padding,
        )
        if self._diagram is not None:
            self._diagram.add_edge(edge)
        elif hasattr(target, "_diagram") and target._diagram is not None:
            target._diagram.add_edge(edge)
        return edge
