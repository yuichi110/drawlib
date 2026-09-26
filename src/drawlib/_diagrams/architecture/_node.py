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
    TextPosition,
)

if TYPE_CHECKING:
    from drawlib._core.types import Style
    from drawlib._diagrams.architecture._diagram import ArchitectureDiagram
    from drawlib._diagrams.architecture._edge import Edge
    from drawlib._diagrams.architecture._group import NodeGroup


class Node:
    """Vertex component representing an entity in an architecture diagram."""

    def __init__(
        self,
        text: str = "",
        icon: IconType = None,
        icon_size: float = 8.0,
        icon_style: Style | None = None,
        style: Style | None = None,
        text_position: TextPosition = "bottom",
        text_margin: float = 1.5,
        text_angle: float = 0.0,
        text_size: float | None = None,
        textstyle: Style | None = None,
    ) -> None:
        """Initialize Node.

        Args:
            text: Label text for this node.
            icon: Icon enumeration, CustomIcon, Dimage, file path, or drawing function.
            icon_size: Width/size of the icon.
            icon_style: Optional Style object for the icon.
            style: Optional Style object for the node background/card.
            text_position: Alignment of label relative to the icon ("bottom", "top", "left", "right").
            text_margin: Margin between icon and label.
            text_angle: Rotation angle in degrees for the label text.
            text_size: Font size for the label.
            textstyle: Optional Style object for the label text.
        """
        self.text = text
        self.icon = icon
        self.icon_size = float(icon_size)
        self.icon_style = icon_style
        self.style = style
        self.text_position = text_position
        self.text_margin = float(text_margin)
        self.text_angle = float(text_angle)
        self.text_size = text_size
        self.textstyle = textstyle

        self._local_xy: tuple[float, float] = (0.0, 0.0)
        self._diagram: ArchitectureDiagram | None = None
        self._parent_group: NodeGroup | None = None

    @property
    def xy(self) -> tuple[float, float]:
        """Get the relative coordinate (x, y) of the icon center."""
        return self._local_xy

    @property
    def center(self) -> tuple[float, float]:
        """Get the center coordinate of the icon."""
        return self._local_xy

    def _estimate_text_dimensions(self) -> tuple[float, float]:
        """Estimate text width and height based on font size and lines."""
        if not self.text:
            return (0.0, 0.0)
        lines = self.text.split("\n")
        num_lines = len(lines)
        max_len = max(len(line) for line in lines) if lines else 0

        font_size = 14.0
        if self.text_size is not None:
            font_size = float(self.text_size)
        elif self.textstyle is not None and self.textstyle.text_size is not None:
            font_size = float(self.textstyle.text_size)

        line_height = font_size * 0.18
        char_width = font_size * 0.065
        text_w = max_len * char_width
        text_h = num_lines * line_height
        return (text_w, text_h)

    def get_bounds(self) -> tuple[float, float, float, float]:
        """Get visual bounding box [min_x, min_y, max_x, max_y] relative to icon center (0, 0)."""
        half = self.icon_size / 2.0
        min_x = -half
        max_x = half
        min_y = -half
        max_y = half

        if not self.text:
            return (min_x, min_y, max_x, max_y)

        text_w, text_h = self._estimate_text_dimensions()
        half_tw = text_w / 2.0

        if self.text_position == "bottom":
            min_y = -half - self.text_margin - text_h
            min_x = min(min_x, -half_tw)
            max_x = max(max_x, half_tw)
        elif self.text_position == "top":
            max_y = half + self.text_margin + text_h
            min_x = min(min_x, -half_tw)
            max_x = max(max_x, half_tw)
        elif self.text_position == "left":
            min_x = -half - self.text_margin - text_w
            min_y = min(min_y, -text_h / 2.0)
            max_y = max(max_y, text_h / 2.0)
        elif self.text_position == "right":
            max_x = half + self.text_margin + text_w
            min_y = min(min_y, -text_h / 2.0)
            max_y = max(max_y, text_h / 2.0)

        return (min_x, min_y, max_x, max_y)

    def get_size(self) -> tuple[float, float]:
        """Get the overall visual bounding box (width, height) including icon and label."""
        min_x, min_y, max_x, max_y = self.get_bounds()
        return (max_x - min_x, max_y - min_y)

    @property
    def left(self) -> tuple[float, float]:
        """Get left anchor coordinate on the icon horizontal axis."""
        x, y = self._local_xy
        return (x - self.icon_size / 2.0, y)

    @property
    def right(self) -> tuple[float, float]:
        """Get right anchor coordinate on the icon horizontal axis."""
        x, y = self._local_xy
        return (x + self.icon_size / 2.0, y)

    @property
    def top(self) -> tuple[float, float]:
        """Get top anchor coordinate avoiding text collisions."""
        x, y = self._local_xy
        _, text_h = self._estimate_text_dimensions()
        if self.text and self.text_position == "top":
            return (x, y + self.icon_size / 2.0 + self.text_margin + text_h)
        return (x, y + self.icon_size / 2.0)

    @property
    def bottom(self) -> tuple[float, float]:
        """Get bottom anchor coordinate avoiding text collisions."""
        x, y = self._local_xy
        _, text_h = self._estimate_text_dimensions()
        if self.text and self.text_position == "bottom":
            return (x, y - self.icon_size / 2.0 - self.text_margin - text_h)
        return (x, y - self.icon_size / 2.0)

    def connect(
        self,
        target: Connectable,
        label: str = "",
        arrow: ArrowType = "->",
        routing: RoutingType = "orthogonal",
        style: Style | None = None,
        padding: PaddingType = 0.0,
    ) -> Edge:
        """Connect this node to a target element.

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

    def fork(
        self,
        targets: list[Connectable],
        at_x: float | None = None,
        at_y: float | None = None,
        style: Style | None = None,
        padding: PaddingType = 0.0,
    ) -> list[Edge]:
        """Branch from this node to multiple targets via an intermediate junction.

        Args:
            targets: List of target elements (Node, NodeGroup, Junction).
            at_x: Optional X coordinate for the branch junction.
            at_y: Optional Y coordinate for the branch junction.
            style: Optional Style object for all connections.
            padding: Gap distance between nodes and line ends.

        Returns:
            list[Edge]: Created edges connecting this node to targets via the junction.
        """
        x, y = self._local_xy
        jx = float(at_x) if at_x is not None else x + self.icon_size * 2.0
        jy = float(at_y) if at_y is not None else y
        j = _junction_module.Junction((jx, jy))

        if self._diagram is not None:
            self._diagram.add(j, (jx, jy))

        start_pad = padding if isinstance(padding, (int, float)) else padding[0]
        end_pad = padding if isinstance(padding, (int, float)) else padding[1]
        edges = [self.connect(j, arrow="-", style=style, padding=(start_pad, 0.0))]
        for tgt in targets:
            edges.append(j.connect(tgt, style=style, padding=(0.0, end_pad)))
        return edges
