# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Node class implementation for architecture diagrams."""

from __future__ import annotations

from typing import TYPE_CHECKING

import drawlib._diagrams.architecture._edge as _edge_module
import drawlib._diagrams.architecture._junction as _junction_module
from drawlib._diagrams.architecture._types import (
    ArrowType,
    Connectable,
    IconType,
    PaddingType,
    RoutingType,
)

if TYPE_CHECKING:
    from drawlib._core.l3_styles import Style
    from drawlib._diagrams.architecture._diagram import ArchitectureDiagram
    from drawlib._diagrams.architecture._edge import Edge
    from drawlib._diagrams.architecture._group import NodeGroup


class Node:
    """Vertex component representing an entity in an architecture diagram."""

    def __init__(
        self,
        card_size: tuple[float, float],
        text: str = "",
        icon: IconType = None,
        icon_size: float = 8.0,
        style: Style | None = None,
        text_style: Style | None = None,
        card_style: Style | None = None,
        show: bool = True,
    ) -> None:
        """Initialize Node.

        Args:
            card_size: (width, height) dimensions of the node card bounding box.
            text: Label text for this node.
            icon: Icon enumeration, CustomIcon, Dimage, PIL Image, file path, or drawing function.
            icon_size: Width/size of the icon. Defaults to 8.0.
            style: Optional Style object for the icon or image.
            text_style: Optional Style object for the label text.
            card_style: Optional Style object for the node card background/border.
            show: Whether to render this node. Defaults to True.
        """
        self.card_size: tuple[float, float] = (float(card_size[0]), float(card_size[1]))
        self.text = text
        self.icon = icon
        self.icon_size = float(icon_size)
        self.style = style
        self.text_style = text_style
        self.card_style = card_style
        self.show = bool(show)

        self._local_xy: tuple[float, float] = (0.0, 0.0)
        self._diagram: ArchitectureDiagram | None = None
        self._parent_group: NodeGroup | None = None

    @property
    def xy(self) -> tuple[float, float]:
        """Get the relative coordinate (x, y) of the node card center."""
        return self._local_xy

    @property
    def center(self) -> tuple[float, float]:
        """Get the center coordinate of the node card."""
        return self._local_xy

    def get_bounds(self) -> tuple[float, float, float, float]:
        """Get visual bounding box [min_x, min_y, max_x, max_y] relative to node center (0, 0)."""
        half_w = self.card_size[0] / 2.0
        half_h = self.card_size[1] / 2.0
        return (-half_w, -half_h, half_w, half_h)

    def get_size(self) -> tuple[float, float]:
        """Get the overall card bounding box (width, height)."""
        return self.card_size

    @property
    def left(self) -> tuple[float, float]:
        """Get left anchor coordinate on the card boundary."""
        x, y = self._local_xy
        return (x - self.card_size[0] / 2.0, y)

    @property
    def right(self) -> tuple[float, float]:
        """Get right anchor coordinate on the card boundary."""
        x, y = self._local_xy
        return (x + self.card_size[0] / 2.0, y)

    @property
    def top(self) -> tuple[float, float]:
        """Get top anchor coordinate on the card boundary."""
        x, y = self._local_xy
        return (x, y + self.card_size[1] / 2.0)

    @property
    def bottom(self) -> tuple[float, float]:
        """Get bottom anchor coordinate on the card boundary."""
        x, y = self._local_xy
        return (x, y - self.card_size[1] / 2.0)

    def connect(
        self,
        target: Connectable,
        label: str = "",
        arrow: ArrowType = "->",
        routing: RoutingType = "orthogonal",
        style: Style | None = None,
        padding: PaddingType = 0.0,
        show: bool = True,
    ) -> Edge:
        """Connect this node to a target element.

        Args:
            target: Target Node, NodeGroup, or Junction.
            label: Connection label text.
            arrow: Arrowhead direction ("->", "<-", "<->", "-").
            routing: Path routing strategy ("orthogonal", "direct", "curved").
            style: Optional Style object for the line.
            padding: Gap distance between nodes and line ends (float or (start, end) tuple).
            show: Whether to render this edge. Defaults to True.

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
            show=show,
        )
        if self._diagram is not None:
            self._diagram.add_edge(edge)
        elif hasattr(target, "_diagram") and target._diagram is not None:
            target._diagram.add_edge(edge)
        return edge

    def get_absolute_xy(self) -> tuple[float, float]:
        """Compute absolute coordinate relative to diagram root.

        Returns:
            Tuple of (x, y) coordinates relative to the root diagram origin.
        """
        x, y = self._local_xy
        curr = self._parent_group
        while curr is not None:
            cx, cy = curr._local_xy
            x += cx
            y += cy
            curr = curr._parent_group
        return (x, y)

    def fork(
        self,
        targets: list[Connectable],
        at_x: float | None = None,
        at_y: float | None = None,
        style: Style | None = None,
        padding: PaddingType = 0.0,
        show: bool = True,
    ) -> list[Edge]:
        """Branch from this node to multiple targets via an intermediate junction.

        Args:
            targets: List of target elements (Node, NodeGroup, Junction).
            at_x: Optional X coordinate for the branch junction.
            at_y: Optional Y coordinate for the branch junction.
            style: Optional Style object for all connections.
            padding: Gap distance between nodes and line ends.
            show: Whether to render the created edges. Defaults to True.

        Returns:
            list[Edge]: Created edges connecting this node to targets via the junction.
        """
        ax, ay = self.get_absolute_xy()
        jx = float(at_x) if at_x is not None else ax + self.card_size[0]
        jy = float(at_y) if at_y is not None else ay
        j = _junction_module.Junction((jx, jy), show=show)

        if self._diagram is not None:
            self._diagram.add(j, (jx, jy))

        start_pad = padding if isinstance(padding, (int, float)) else padding[0]
        end_pad = padding if isinstance(padding, (int, float)) else padding[1]
        edges = [self.connect(j, arrow="-", style=style, padding=(start_pad, 0.0), show=show)]
        for tgt in targets:
            edges.append(j.connect(tgt, style=style, padding=(0.0, end_pad), show=show))
        return edges
