# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Edge class implementation for architecture diagrams."""

from __future__ import annotations

from typing import TYPE_CHECKING

import drawlib._diagrams.architecture._junction as _junction_module
from drawlib._diagrams.architecture._types import ArrowType, Connectable, PaddingType, RoutingType

if TYPE_CHECKING:
    from drawlib._core.types import Style
    from drawlib._diagrams.architecture._diagram import ArchitectureDiagram
    from drawlib._diagrams.architecture._junction import Junction


class Edge:
    """Connection line between elements in an architecture diagram."""

    def __init__(
        self,
        start: Connectable,
        end: Connectable,
        label: str = "",
        arrow: ArrowType = "->",
        routing: RoutingType = "orthogonal",
        style: Style | None = None,
        textstyle: Style | None = None,
        padding: PaddingType = 0.0,
    ) -> None:
        """Initialize Edge.

        Args:
            start: Start Node, NodeGroup, or Junction.
            end: End Node, NodeGroup, or Junction.
            label: Text label along the connection.
            arrow: Arrowhead configuration ("->", "<-", "<->", "-").
            routing: Line path routing style ("orthogonal", "direct", "curved").
            style: Style object for the line (color, width, dash style).
            textstyle: Style object for the label text.
            padding: Gap distance between nodes and line ends (float or (start, end) tuple).
        """
        self.start = start
        self.end = end
        self.label = label
        self.label_pos = 0.5
        self.arrow = arrow
        self.routing = routing
        self.style = style
        self.textstyle = textstyle
        self.padding = padding
        self._waypoints: list[tuple[float, float]] = []
        self._diagram: ArchitectureDiagram | None = None

    @property
    def waypoints(self) -> list[tuple[float, float]]:
        """Get the list of intermediate waypoints."""
        return list(self._waypoints)

    def points(self, waypoints: list[tuple[float, float]]) -> Edge:
        """Set explicit intermediate waypoints for this edge.

        Args:
            waypoints: List of (x, y) coordinate tuples relative to the diagram.

        Returns:
            Edge: self for method chaining.
        """
        self._waypoints = [(float(pt[0]), float(pt[1])) for pt in waypoints]
        return self

    def via(self, *waypoints: tuple[float, float]) -> Edge:
        """Set explicit intermediate waypoints for this edge (unpacked argument version).

        Args:
            *waypoints: Variable number of (x, y) coordinate tuples.

        Returns:
            Edge: self for method chaining.
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

    def set_label(self, text: str, pos: float = 0.5) -> Edge:
        """Set edge label text and position.

        Args:
            text: Label text.
            pos: Fractional position along the edge (0.0=start, 1.0=end). Defaults to 0.5.

        Returns:
            Edge: self for method chaining.
        """
        self.label = text
        self.label_pos = float(pos)
        return self

    def set_arrow(self, arrow: ArrowType) -> Edge:
        """Set edge arrowhead.

        Args:
            arrow: Arrowhead style ("->", "<-", "<->", "-").

        Returns:
            Edge: self for method chaining.
        """
        self.arrow = arrow
        return self

    def set_style(self, style: Style) -> Edge:
        """Set edge line style.

        Args:
            style: Style object for the line.

        Returns:
            Edge: self for method chaining.
        """
        self.style = style
        return self

    def set_textstyle(self, textstyle: Style) -> Edge:
        """Set edge label text style.

        Args:
            textstyle: Style object for the label text.

        Returns:
            Edge: self for method chaining.
        """
        self.textstyle = textstyle
        return self

    def set_padding(self, padding: PaddingType) -> Edge:
        """Set gap padding between nodes and line ends.

        Args:
            padding: Gap distance (float for both ends, or (start, end) tuple).

        Returns:
            Edge: self for method chaining.
        """
        self.padding = padding
        return self
