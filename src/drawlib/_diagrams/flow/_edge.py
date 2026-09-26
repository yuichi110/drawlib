# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""FlowEdge connection line implementation for flow diagrams."""

from __future__ import annotations

from typing import TYPE_CHECKING, Union

import drawlib._diagrams.flow._junction as _junction_module
from drawlib._diagrams.flow._types import ArrowType, Connectable, PaddingType, RoutingType, Side

if TYPE_CHECKING:
    from drawlib._core.types import Style
    from drawlib._diagrams.flow._diagram import FlowDiagram
    from drawlib._diagrams.flow._junction import Junction


class FlowEdge:
    """Connection line between elements in a flow diagram."""

    def __init__(
        self,
        start: Connectable,
        end: Connectable,
        label: str = "",
        arrow: ArrowType | None = None,
        routing: RoutingType = "orthogonal",
        start_side: Side = "auto",
        end_side: Side = "auto",
        style: Style | None = None,
        textstyle: Style | None = None,
        padding: PaddingType = 0.0,
    ) -> None:
        """Initialize FlowEdge.

        Args:
            start: Start FlowNode or Junction.
            end: End FlowNode or Junction.
            label: Text label along the connection.
            arrow: Arrowhead configuration ("->", "<-", "<->", "-"). Defaults to "-" if end is Junction, else "->".
            routing: Line path routing style ("orthogonal", "direct").
            start_side: Attachment side on start element ("left", "right", "top", "bottom", "auto").
            end_side: Attachment side on end element ("left", "right", "top", "bottom", "auto").
            style: Style object for the line (color, width, dash style).
            textstyle: Style object for the label text.
            padding: Gap distance between elements and line ends (float or (start, end) tuple).
        """
        if arrow is None:
            resolved_arrow = "-" if isinstance(end, _junction_module.Junction) else "->"
        else:
            resolved_arrow = arrow

        valid_arrows = {"->", "<-", "<->", "-"}
        if resolved_arrow not in valid_arrows:
            raise ValueError(f"Invalid arrow: {resolved_arrow!r}. Must be one of {sorted(valid_arrows)}.")

        valid_routings = {"orthogonal", "direct"}
        if routing not in valid_routings:
            raise ValueError(f"Invalid routing: {routing!r}. Must be one of {sorted(valid_routings)}.")

        valid_sides = {"left", "right", "top", "bottom", "auto"}
        if start_side not in valid_sides:
            raise ValueError(f"Invalid start_side: {start_side!r}. Must be one of {sorted(valid_sides)}.")
        if end_side not in valid_sides:
            raise ValueError(f"Invalid end_side: {end_side!r}. Must be one of {sorted(valid_sides)}.")

        self.start = start
        self.end = end
        self.label = label
        self.arrow = resolved_arrow
        self.routing = routing
        self.start_side = start_side
        self.end_side = end_side
        self.style = style
        self.textstyle = textstyle
        self.padding = padding
        self._waypoints: list[tuple[float, float]] = []
        self._diagram: FlowDiagram | None = None

    @property
    def waypoints(self) -> list[tuple[float, float]]:
        """Get list of intermediate waypoints."""
        return list(self._waypoints)

    def points(self, waypoints: list[tuple[float, float]]) -> FlowEdge:
        """Set explicit intermediate waypoints for this edge.

        Args:
            waypoints: List of (x, y) coordinate tuples relative to the diagram.

        Returns:
            FlowEdge: self for method chaining.
        """
        self._waypoints = [(float(pt[0]), float(pt[1])) for pt in waypoints]
        return self

    def via(self, *waypoints: tuple[float, float]) -> FlowEdge:
        """Set explicit intermediate waypoints for this edge (unpacked argument version).

        Args:
            *waypoints: Variable number of (x, y) coordinate tuples.

        Returns:
            FlowEdge: self for method chaining.
        """
        return self.points(list(waypoints))

    def add_point(self, xy: tuple[float, float]) -> Junction:
        """Add a waypoint to this edge and return it as a branching Junction.

        Args:
            xy: (x, y) coordinates for the waypoint / branch point.

        Returns:
            Junction: Newly created Junction at xy that can be connected to other elements.
        """
        pt = (float(xy[0]), float(xy[1]))
        if pt not in self._waypoints:
            self._waypoints.append(pt)

        junction = _junction_module.Junction(pt)
        junction._diagram = self._diagram
        if self._diagram is not None:
            self._diagram.add(junction, pt)
        return junction
