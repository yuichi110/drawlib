# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""NodeGroup class implementation for architecture diagrams."""

from __future__ import annotations

from typing import TYPE_CHECKING

import drawlib._diagrams.architecture._edge as _edge_module
from drawlib._diagrams.architecture._types import ArrowType, Connectable, DiagramItem, ItemT, PaddingType, RoutingType

if TYPE_CHECKING:
    from drawlib._core.l3_styles import Style
    from drawlib._diagrams.architecture._diagram import Diagram
    from drawlib._diagrams.architecture._edge import Edge


class NodeGroup:
    """Boundary container grouping nodes and nested groups in an architecture diagram."""

    def __init__(
        self,
        title: str = "",
        width: float | None = None,
        height: float | None = None,
        padding: float = 5.0,
        style: Style | None = None,
        textstyle: Style | None = None,
    ) -> None:
        """Initialize NodeGroup.

        Args:
            title: Group header title (e.g. "VPC Network", "Subnet 1").
            width: Optional fixed width. If None, auto-computed from members + padding.
            height: Optional fixed height. If None, auto-computed from members + padding.
            padding: Padding around member components when auto-calculating bounds.
            style: Style object for the boundary box (border, background color).
            textstyle: Style object for the title text.
        """
        self.title = title
        self.width = float(width) if width is not None else None
        self.height = float(height) if height is not None else None
        self.padding = float(padding)
        self.style = style
        self.textstyle = textstyle

        self._items: list[tuple[DiagramItem, tuple[float, float]]] = []
        self._local_xy: tuple[float, float] = (0.0, 0.0)
        self._diagram: Diagram | None = None
        self._parent_group: NodeGroup | None = None

    @property
    def xy(self) -> tuple[float, float]:
        """Get the relative coordinate (x, y) representing the bottom-left of the group."""
        return self._local_xy

    @property
    def items(self) -> list[DiagramItem]:
        """Get the list of direct child items in this group."""
        return [item for item, _ in self._items]

    def add(self, item: ItemT, xy: tuple[float, float]) -> ItemT:
        """Add a child Node, NodeGroup, or Junction to this group at local coordinate xy.

        Args:
            item: Child component.
            xy: Local coordinate (x, y) relative to this group's bottom-left origin.

        Returns:
            ItemT: Added component for convenient assignment.
        """
        pt = (float(xy[0]), float(xy[1]))
        item._local_xy = pt
        item._parent_group = self
        item._diagram = self._diagram
        self._items.append((item, pt))

        # Propagate diagram reference to nested elements
        if isinstance(item, NodeGroup):
            item._propagate_diagram(self._diagram)

        return item

    def _propagate_diagram(self, diagram: Diagram | None) -> None:
        """Propagate diagram reference recursively to all children."""
        self._diagram = diagram
        for item, _ in self._items:
            item._diagram = diagram
            if isinstance(item, NodeGroup):
                item._propagate_diagram(diagram)

    def get_bounds(self) -> tuple[float, float, float, float]:
        """Calculate local bounding box [min_x, min_y, max_x, max_y] of this group."""
        if self.width is not None and self.height is not None:
            return (0.0, 0.0, self.width, self.height)

        if not self._items:
            w = self.width if self.width is not None else self.padding * 4.0
            h = self.height if self.height is not None else self.padding * 4.0
            return (0.0, 0.0, w, h)

        min_xs: list[float] = []
        min_ys: list[float] = []
        max_xs: list[float] = []
        max_ys: list[float] = []

        for item, (ix, iy) in self._items:
            c_min_x, c_min_y, c_max_x, c_max_y = item.get_bounds()
            min_xs.append(ix + c_min_x)
            min_ys.append(iy + c_min_y)
            max_xs.append(ix + c_max_x)
            max_ys.append(iy + c_max_y)

        title_margin = 4.0 if self.title else 0.0

        calc_min_x = min(min_xs) - self.padding
        calc_min_y = min(min_ys) - self.padding
        calc_max_x = max(max_xs) + self.padding
        calc_max_y = max(max_ys) + self.padding + title_margin

        final_w = self.width if self.width is not None else (calc_max_x - calc_min_x)
        final_h = self.height if self.height is not None else (calc_max_y - calc_min_y)

        return (calc_min_x, calc_min_y, calc_min_x + final_w, calc_min_y + final_h)

    def get_size(self) -> tuple[float, float]:
        """Get the visual width and height of this group."""
        min_x, min_y, max_x, max_y = self.get_bounds()
        return (max_x - min_x, max_y - min_y)

    @property
    def left(self) -> tuple[float, float]:
        """Get left anchor on the group boundary."""
        min_x, min_y, _, max_y = self.get_bounds()
        return (min_x, (min_y + max_y) / 2.0)

    @property
    def right(self) -> tuple[float, float]:
        """Get right anchor on the group boundary."""
        _, min_y, max_x, max_y = self.get_bounds()
        return (max_x, (min_y + max_y) / 2.0)

    @property
    def top(self) -> tuple[float, float]:
        """Get top anchor on the group boundary."""
        min_x, _, max_x, max_y = self.get_bounds()
        return ((min_x + max_x) / 2.0, max_y)

    @property
    def bottom(self) -> tuple[float, float]:
        """Get bottom anchor on the group boundary."""
        min_x, min_y, max_x, _ = self.get_bounds()
        return ((min_x + max_x) / 2.0, min_y)

    @property
    def center(self) -> tuple[float, float]:
        """Get center coordinate of the group."""
        min_x, min_y, max_x, max_y = self.get_bounds()
        return ((min_x + max_x) / 2.0, (min_y + max_y) / 2.0)

    def connect(
        self,
        target: Connectable,
        label: str = "",
        arrow: ArrowType = "->",
        routing: RoutingType = "orthogonal",
        style: Style | None = None,
        padding: PaddingType = 0.0,
    ) -> Edge:
        """Connect this group's boundary to a target element.

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
