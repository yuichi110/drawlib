# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""FlowNode base class implementation for flow diagrams."""

from __future__ import annotations

from typing import TYPE_CHECKING, Union

import drawlib._diagrams.flow._edge as _edge_module
import drawlib._diagrams.flow._junction as _junction_module
from drawlib._diagrams.flow._types import ArrowType, Connectable, PaddingType, RoutingType, ShapeType, Side

if TYPE_CHECKING:
    from drawlib._core.types import Style
    from drawlib._diagrams.flow._diagram import FlowDiagram
    from drawlib._diagrams.flow._edge import FlowEdge


class FlowNode:
    """Vertex component representing a process, decision, terminal, or data shape in a flow diagram."""

    def __init__(
        self,
        text: str = "",
        width: float = 24.0,
        height: float = 12.0,
        r: float = 0.0,
        angle: float = 0.0,
        style: Style | None = None,
        textstyle: Style | None = None,
        textsize: float | None = None,
        shape_type: ShapeType = "process",
    ) -> None:
        """Initialize FlowNode.

        Args:
            text: Text content to display centered inside the shape.
            width: Width of the shape. Defaults to 24.0.
            height: Height of the shape. Defaults to 12.0.
            r: Corner radius for rounded corners. Defaults to 0.0.
            angle: Rotation angle in degrees. Defaults to 0.0.
            style: Style object for the shape (fill color, border color/width).
            textstyle: Style object for the label text.
            textsize: Font size shortcut for label text.
            shape_type: Shape type ("process", "decision", "start", "end", "data").
        """
        self.text = text
        self.width = float(width)
        self.height = float(height)
        self.r = float(r)
        self.angle = float(angle)
        self.style = style
        self.textstyle = textstyle
        self.textsize = float(textsize) if textsize is not None else None
        self.shape_type: ShapeType = shape_type

        self._local_xy: tuple[float, float] = (0.0, 0.0)
        self._diagram: FlowDiagram | None = None

    @property
    def xy(self) -> tuple[float, float]:
        """Get relative coordinate (x, y) representing the center of this node."""
        return self._local_xy

    @property
    def center(self) -> tuple[float, float]:
        """Get center coordinate (x, y) of this node."""
        return self._local_xy

    @property
    def top(self) -> tuple[float, float]:
        """Get top anchor coordinate."""
        return self.get_anchor("top")

    @property
    def bottom(self) -> tuple[float, float]:
        """Get bottom anchor coordinate."""
        return self.get_anchor("bottom")

    @property
    def left(self) -> tuple[float, float]:
        """Get left anchor coordinate."""
        return self.get_anchor("left")

    @property
    def right(self) -> tuple[float, float]:
        """Get right anchor coordinate."""
        return self.get_anchor("right")

    def get_anchor(self, side: Side = "auto") -> tuple[float, float]:
        """Get anchor coordinate on the node boundary.

        Args:
            side: Side to get anchor point ("top", "bottom", "left", "right", "auto").

        Returns:
            Absolute or local coordinate (x, y) of the anchor.
        """
        cx, cy = self._local_xy
        half_w = self.width / 2.0
        half_h = self.height / 2.0

        if side == "top":
            return (cx, cy + half_h)
        if side == "bottom":
            return (cx, cy - half_h)
        if side == "left":
            return (cx - half_w, cy)
        if side == "right":
            return (cx + half_w, cy)

        # "auto" defaults to center
        return (cx, cy)

    def get_bounds(self) -> tuple[float, float, float, float]:
        """Get visual bounding box [min_x, min_y, max_x, max_y] relative to center (0, 0)."""
        half_w = self.width / 2.0
        half_h = self.height / 2.0
        return (-half_w, -half_h, half_w, half_h)

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
        """Connect this node to a target element.

        Args:
            target: Target FlowNode or Junction.
            label: Connection label text (e.g. "Yes", "No", "Success").
            arrow: Arrowhead direction ("->", "<-", "<->", "-"). Defaults to "-" if target is Junction, else "->".
            routing: Path routing strategy ("orthogonal" or "direct").
            start_side: Attachment side on start node ("left", "right", "top", "bottom", "auto").
            end_side: Attachment side on end element ("left", "right", "top", "bottom", "auto").
            style: Optional Style object for the line.
            textstyle: Optional Style object for the label text.
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

    def fork(
        self,
        targets: list[Connectable],
        at_x: float | None = None,
        at_y: float | None = None,
        style: Style | None = None,
        padding: PaddingType = 0.0,
    ) -> list[FlowEdge]:
        """Branch from this node to multiple targets via an intermediate junction.

        Args:
            targets: List of target elements (FlowNode, Junction).
            at_x: Optional X coordinate for branch junction.
            at_y: Optional Y coordinate for branch junction.
            style: Optional Style object for all connections.
            padding: Gap distance between elements and line ends.

        Returns:
            list[FlowEdge]: Created edges connecting this node to targets via junction.
        """
        cx, cy = self._local_xy
        jx = float(at_x) if at_x is not None else cx + self.width
        jy = float(at_y) if at_y is not None else cy
        j = _junction_module.Junction((jx, jy))

        if self._diagram is not None:
            self._diagram.add(j, (jx, jy))

        start_pad = padding if isinstance(padding, (int, float)) else padding[0]
        end_pad = padding if isinstance(padding, (int, float)) else padding[1]
        edges = [self.connect(j, arrow="-", style=style, padding=(start_pad, 0.0))]
        for tgt in targets:
            edges.append(j.connect(tgt, style=style, padding=(0.0, end_pad)))
        return edges
