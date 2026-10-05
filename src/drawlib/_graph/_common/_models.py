# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Graph and Layout data models for declarative graph solving."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from drawlib._graph._common._code_generator import generate_code
from drawlib._graph._common._renderer import render_layout
from drawlib.styles import Style, Styles


@dataclass
class Node:
    """User-registered node in a graph."""

    id: str
    label: str | None = None
    style: Style | None = None
    text_style: Style | None = None
    shape: Literal["rectangle", "circle", "rounded_rectangle"] = "rectangle"
    icon: str | None = None
    width: float | None = None
    height: float | None = None
    ring: int | None = None
    row: int | None = None
    col: int | None = None
    layer: int | None = None


@dataclass
class Edge:
    """User-registered directed or undirected edge between two nodes."""

    src: str
    dst: str
    label: str | None = None
    style: Style | None = None
    text_style: Style | None = None
    arrow_head: Literal["->", "<-", "<->", "-"] = "->"
    line_style: Literal["solid", "dashed", "dotted"] | None = None


@dataclass
class Cluster:
    """User-registered grouping cluster of nodes."""

    id: str
    nodes: list[str] = field(default_factory=list)
    label: str | None = None
    style: Style | None = None
    text_style: Style | None = None
    padding: float = 4.0


@dataclass
class NodeLayout:
    """Calculated position and dimensions for a node."""

    id: str
    xy: tuple[float, float]
    width: float
    height: float
    style: Style
    label: str
    text_style: Style | None = None
    shape: str = "rectangle"
    icon: str | None = None

    @property
    def x(self) -> float:
        """Center X coordinate."""
        return self.xy[0]

    @property
    def y(self) -> float:
        """Center Y coordinate."""
        return self.xy[1]

    @property
    def left(self) -> float:
        """Left edge X coordinate."""
        return self.xy[0] - self.width / 2.0

    @property
    def right(self) -> float:
        """Right edge X coordinate."""
        return self.xy[0] + self.width / 2.0

    @property
    def bottom(self) -> float:
        """Bottom edge Y coordinate."""
        return self.xy[1] - self.height / 2.0

    @property
    def top(self) -> float:
        """Top edge Y coordinate."""
        return self.xy[1] + self.height / 2.0


@dataclass
class EdgeLayout:
    """Calculated routing path and styling for an edge."""

    src: str
    dst: str
    src_port: tuple[float, float]
    dst_port: tuple[float, float]
    waypoints: list[tuple[float, float]] = field(default_factory=list)
    label: str | None = None
    style: Style = field(default_factory=lambda: Styles.DarkBold)
    text_style: Style = field(default_factory=lambda: Styles.Dark)
    arrow_head: Literal["", "->", "<-", "<->", "-"] = "->"

    @property
    def points(self) -> list[tuple[float, float]]:
        """All consecutive points defining the edge path."""
        return [self.src_port] + self.waypoints + [self.dst_port]


@dataclass
class ClusterLayout:
    """Calculated bounding box and styling for a cluster."""

    id: str
    label: str | None
    bbox: tuple[float, float, float, float]  # (cx, cy, width, height)
    style: Style
    text_style: Style
    shape: Literal["rectangle", "circle"] = "rectangle"

    @property
    def cx(self) -> float:
        """Cluster center X coordinate."""
        return self.bbox[0]

    @property
    def cy(self) -> float:
        """Cluster center Y coordinate."""
        return self.bbox[1]

    @property
    def width(self) -> float:
        """Cluster width."""
        return self.bbox[2]

    @property
    def height(self) -> float:
        """Cluster height."""
        return self.bbox[3]

    @property
    def left(self) -> float:
        """Left edge X coordinate."""
        return self.bbox[0] - self.bbox[2] / 2.0

    @property
    def right(self) -> float:
        """Right edge X coordinate."""
        return self.bbox[0] + self.bbox[2] / 2.0

    @property
    def top(self) -> float:
        """Top edge Y coordinate."""
        return self.bbox[1] + self.bbox[3] / 2.0

    @property
    def bottom(self) -> float:
        """Bottom edge Y coordinate."""
        return self.bbox[1] - self.bbox[3] / 2.0


@dataclass
class GraphLayout:
    """Complete geometrical result calculated by graph solvers."""

    nodes: dict[str, NodeLayout] = field(default_factory=dict)
    edges: list[EdgeLayout] = field(default_factory=list)
    clusters: dict[str, ClusterLayout] = field(default_factory=dict)
    width: float = 100.0
    height: float = 100.0

    def offset(self, node_id: str, dx: float = 0.0, dy: float = 0.0) -> None:
        """Shift a specific node and recalculate incident edge ports.

        Args:
            node_id: ID of the node to move.
            dx: Horizontal delta to shift.
            dy: Vertical delta to shift.

        Raises:
            KeyError: If node_id does not exist in the layout.
        """
        if node_id not in self.nodes:
            raise KeyError(f"Node '{node_id}' not found in layout.")

        nl = self.nodes[node_id]
        new_xy = (round(nl.xy[0] + dx, 2), round(nl.xy[1] + dy, 2))
        self.nodes[node_id] = NodeLayout(
            id=nl.id,
            xy=new_xy,
            width=nl.width,
            height=nl.height,
            style=nl.style,
            text_style=nl.text_style,
            label=nl.label,
            shape=nl.shape,
            icon=nl.icon,
        )

        # Shift incident edge ports
        for edge in self.edges:
            if edge.src == node_id:
                edge.src_port = (round(edge.src_port[0] + dx, 2), round(edge.src_port[1] + dy, 2))
            if edge.dst == node_id:
                edge.dst_port = (round(edge.dst_port[0] + dx, 2), round(edge.dst_port[1] + dy, 2))

    def draw(self) -> None:
        """Render this layout directly onto the active Drawlib canvas."""
        render_layout(self)

    def to_code(self) -> str:
        """Export this layout as standalone executable Drawlib Python source code.

        Returns:
            Formatted Python source code string.
        """
        return generate_code(self)
