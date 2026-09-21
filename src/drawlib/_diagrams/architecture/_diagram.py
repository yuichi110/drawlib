# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Diagram class implementation for architecture diagrams."""

from __future__ import annotations

from typing import TYPE_CHECKING

import drawlib._diagrams.architecture._edge as _edge_module
import drawlib._diagrams.architecture._group as _group_module
import drawlib._diagrams.architecture._junction as _junction_module
import drawlib._diagrams.architecture._renderer as _renderer_module
from drawlib._diagrams.architecture._types import ArrowType, Connectable, DiagramItem, ItemT, PaddingType, RoutingType

if TYPE_CHECKING:
    from drawlib._core.l3_styles import Style
    from drawlib._diagrams.architecture._edge import Edge
    from drawlib._diagrams.architecture._junction import Junction


class Diagram:
    """Top-level container for architecture diagrams."""

    def __init__(
        self,
        title: str = "",
        width: float | None = None,
        height: float | None = None,
        style: Style | None = None,
    ) -> None:
        """Initialize Diagram.

        Args:
            title: Optional diagram title.
            width: Optional fixed width of the diagram.
            height: Optional fixed height of the diagram.
            style: Optional Style object for the diagram background.
        """
        self.title = title
        self.width = float(width) if width is not None else None
        self.height = float(height) if height is not None else None
        self.style = style

        self._items: list[tuple[DiagramItem, tuple[float, float]]] = []
        self._edges: list[Edge] = []

    @property
    def items(self) -> list[DiagramItem]:
        """Get list of top-level items in the diagram."""
        return [item for item, _ in self._items]

    @property
    def edges(self) -> list[Edge]:
        """Get list of edges in the diagram."""
        return list(self._edges)

    def add(self, item: ItemT, xy: tuple[float, float]) -> ItemT:
        """Add a Node, NodeGroup, or Junction to the diagram at local relative coordinate xy.

        Args:
            item: Node, NodeGroup, or Junction instance.
            xy: Local coordinate (x, y) relative to the diagram.

        Returns:
            ItemT: The added item for convenient assignment or chaining.
        """
        pt = (float(xy[0]), float(xy[1]))
        item._local_xy = pt
        item._diagram = self
        self._items.append((item, pt))

        if isinstance(item, _group_module.NodeGroup):
            item._propagate_diagram(self)

        return item

    def add_edge(self, edge: Edge) -> Edge:
        """Register an Edge connection with this diagram.

        Args:
            edge: Edge instance to register.

        Returns:
            Edge: The registered edge.
        """
        edge._diagram = self
        if edge not in self._edges:
            self._edges.append(edge)
        return edge

    def connect(
        self,
        start: Connectable,
        end: Connectable,
        label: str = "",
        arrow: ArrowType = "->",
        routing: RoutingType = "orthogonal",
        style: Style | None = None,
        padding: PaddingType = 0.0,
    ) -> Edge:
        """Create and register an edge between two connectables.

        Args:
            start: Start Node, NodeGroup, or Junction.
            end: End Node, NodeGroup, or Junction.
            label: Connection label text.
            arrow: Arrowhead direction ("->", "<-", "<->", "-").
            routing: Path routing strategy ("orthogonal", "direct", "curved").
            style: Optional Style object for the line.
            padding: Gap distance between nodes and line ends (float or (start, end) tuple).

        Returns:
            Edge: Newly created edge.
        """
        edge = _edge_module.Edge(
            start=start,
            end=end,
            label=label,
            arrow=arrow,
            routing=routing,
            style=style,
            padding=padding,
        )
        self.add_edge(edge)
        return edge

    def junction(self, xy: tuple[float, float]) -> Junction:
        """Create and register a Junction at the given relative coordinate xy.

        Args:
            xy: Relative coordinate (x, y) in the diagram.

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

        if not self._items:
            return (100.0, 100.0)

        max_x = 0.0
        max_y = 0.0
        for item, (ix, iy) in self._items:
            _, _, c_max_x, c_max_y = item.get_bounds()
            max_x = max(max_x, ix + c_max_x)
            max_y = max(max_y, iy + c_max_y)

        final_w = self.width if self.width is not None else max_x
        final_h = self.height if self.height is not None else max_y
        return (final_w, final_h)

    def draw(self, xy: tuple[float, float] = (0.0, 0.0)) -> None:
        """Render the complete diagram onto the canvas at base coordinate xy.

        Args:
            xy: Base canvas coordinate (x, y) where diagram's bottom-left origin is placed.
        """
        _renderer_module.draw_diagram(self, xy)
