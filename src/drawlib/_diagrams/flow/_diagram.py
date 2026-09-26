# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""FlowDiagram class implementation for flow diagrams."""

from __future__ import annotations

from typing import TYPE_CHECKING

import drawlib._diagrams.flow._edge as _edge_module
import drawlib._diagrams.flow._junction as _junction_module
import drawlib._diagrams.flow._lane as _lane_module
import drawlib._diagrams.flow._renderer as _renderer_module
from drawlib._diagrams.flow._types import (
    ArrowType,
    Connectable,
    DiagramItem,
    ItemT,
    Orientation,
    PaddingType,
    RoutingType,
    Side,
)

if TYPE_CHECKING:
    from drawlib._core.types import Style
    from drawlib._diagrams.flow._edge import FlowEdge
    from drawlib._diagrams.flow._junction import Junction
    from drawlib._diagrams.flow._lane import Lane


class FlowDiagram:
    """Top-level container for flowcharts and workflow diagrams."""

    def __init__(
        self,
        title: str = "",
        width: float | None = None,
        height: float | None = None,
        style: Style | None = None,
        lane_orientation: Orientation = "vertical",
    ) -> None:
        """Initialize FlowDiagram.

        Args:
            title: Optional diagram title.
            width: Optional fixed width of the diagram canvas.
            height: Optional fixed height of the diagram canvas.
            style: Optional Style object for the diagram background.
            lane_orientation: Orientation of swimlanes ("vertical" or "horizontal"). Defaults to "vertical".
        """
        self.title = title
        self.width = float(width) if width is not None else None
        self.height = float(height) if height is not None else None
        self.style = style
        self.lane_orientation: Orientation = lane_orientation

        self._items: list[tuple[DiagramItem, tuple[float, float]]] = []
        self._edges: list[FlowEdge] = []
        self._lanes: list[Lane] = []

    @property
    def items(self) -> list[DiagramItem]:
        """Get list of top-level items (nodes, junctions) in the diagram."""
        return [item for item, _ in self._items]

    @property
    def edges(self) -> list[FlowEdge]:
        """Get list of edges in the diagram."""
        return list(self._edges)

    @property
    def lanes(self) -> list[Lane]:
        """Get list of swimlanes in the diagram."""
        return list(self._lanes)

    def add(self, item: ItemT, xy: tuple[float, float]) -> ItemT:
        """Add a FlowNode or Junction to the diagram at coordinate xy (shape center).

        Args:
            item: FlowNode or Junction instance.
            xy: Coordinate (x, y) for the center of the item.

        Returns:
            ItemT: The added item for convenient assignment or chaining.
        """
        pt = (float(xy[0]), float(xy[1]))
        item._local_xy = pt
        item._diagram = self
        self._items.append((item, pt))
        return item

    def add_edge(self, edge: FlowEdge) -> FlowEdge:
        """Register a FlowEdge connection with this diagram.

        Args:
            edge: FlowEdge instance to register.

        Returns:
            FlowEdge: The registered edge.
        """
        edge._diagram = self
        if edge not in self._edges:
            self._edges.append(edge)
        return edge

    def add_lane(
        self,
        title: str,
        size: float | None = None,
        width: float | None = None,
        height: float | None = None,
        style: Style | None = None,
        textstyle: Style | None = None,
        textsize: float | None = None,
        header_size: float = 6.0,
        header_style: Style | None = None,
    ) -> Lane:
        """Add a swimlane to the diagram.

        Args:
            title: Header title of the lane.
            size: Dimension of the lane (width for vertical, height for horizontal).
            width: Width of the lane (alternative alias when lane_orientation is vertical).
            height: Height of the lane (alternative alias when lane_orientation is horizontal).
            style: Style for the lane background fill and boundary stroke.
            textstyle: Style for the header title text.
            textsize: Font size shortcut for header text.
            header_size: Size of the header area (height for vertical, width for horizontal).
            header_style: Optional specific Style for the header card background.

        Returns:
            Lane: The created swimlane.
        """
        resolved_size = size
        if resolved_size is None:
            if self.lane_orientation == "vertical":
                resolved_size = width if width is not None else 30.0
            else:
                resolved_size = height if height is not None else 30.0

        lane = _lane_module.Lane(
            title=title,
            size=resolved_size,
            style=style,
            textstyle=textstyle,
            textsize=textsize,
            header_size=header_size,
            header_style=header_style,
        )
        self._lanes.append(lane)
        return lane

    def connect(
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
    ) -> FlowEdge:
        """Create and register an edge between two connectables.

        Args:
            start: Start FlowNode or Junction.
            end: End FlowNode or Junction.
            label: Connection label text.
            arrow: Arrowhead direction ("->", "<-", "<->", "-"). Defaults to "-" if end is Junction, else "->".
            routing: Path routing strategy ("orthogonal", "direct").
            start_side: Attachment side on start node ("left", "right", "top", "bottom", "auto").
            end_side: Attachment side on end node ("left", "right", "top", "bottom", "auto").
            style: Optional Style object for the line.
            textstyle: Optional Style object for label text.
            padding: Gap distance between nodes and line ends.

        Returns:
            FlowEdge: Newly created edge.
        """
        edge = _edge_module.FlowEdge(
            start=start,
            end=end,
            label=label,
            arrow=arrow,
            routing=routing,
            start_side=start_side,
            end_side=end_side,
            style=style,
            textstyle=textstyle,
            padding=padding,
        )
        self.add_edge(edge)
        return edge

    def junction(self, xy: tuple[float, float]) -> Junction:
        """Create and register a Junction at the given coordinate xy.

        Args:
            xy: Coordinate (x, y) in the diagram.

        Returns:
            Junction: The created and registered junction.
        """
        j = _junction_module.Junction(xy)
        self.add(j, xy)
        return j

    def get_size(self) -> tuple[float, float]:
        """Get overall width and height of the diagram."""
        if self.width is not None and self.height is not None:
            return (self.width, self.height)

        max_x = 0.0
        max_y = 0.0

        if self._lanes:
            total_lane_size = sum(lane.size for lane in self._lanes)
            if self.lane_orientation == "vertical":
                max_x = max(max_x, total_lane_size)
            else:
                max_y = max(max_y, total_lane_size)

        for item, (ix, iy) in self._items:
            min_bx, min_by, max_bx, max_by = item.get_bounds()
            max_x = max(max_x, ix + max_bx)
            max_y = max(max_y, iy + max_by)

        for edge in self._edges:
            for wx, wy in edge.waypoints:
                max_x = max(max_x, wx)
                max_y = max(max_y, wy)

        final_w = self.width if self.width is not None else (max_x if max_x > 0 else 100.0)
        final_h = self.height if self.height is not None else (max_y if max_y > 0 else 100.0)
        return (final_w, final_h)

    def draw(self, xy: tuple[float, float] = (0.0, 0.0)) -> None:
        """Render the complete flow diagram onto the canvas at base coordinate xy.

        Args:
            xy: Base canvas coordinate (x, y) where diagram's bottom-left origin is placed.
        """
        _renderer_module.draw_diagram(self, xy)
