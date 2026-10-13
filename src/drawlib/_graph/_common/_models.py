# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Graph and Layout data models for declarative graph coordinate solving."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Self


@dataclass
class Node:
    """User-registered node in a graph topology."""

    id: str
    width: float | None = None
    height: float | None = None
    ring: int | None = None
    row: int | None = None
    col: int | None = None
    layer: int | None = None
    group: str | None = None
    subgroup: str | None = None


@dataclass
class Edge:
    """User-registered connection between two nodes."""

    src: str
    dst: str


@dataclass
class Cluster:
    """User-registered grouping boundary of nodes."""

    id: str
    nodes: list[str] = field(default_factory=list)
    padding: float = 4.0
    header_height: float = 3.5
    parent: str | None = None
    order: int | None = None
    pos: Literal["top", "bottom", "left", "right", "center"] | None = None


@dataclass
class NodeLayout:
    """Calculated position and dimensions for a node."""

    id: str
    xy: tuple[float, float]
    width: float
    height: float
    parent_id: str | None = None
    local_xy: tuple[float, float] = (0.0, 0.0)

    def __post_init__(self) -> None:
        if self.parent_id is None and self.local_xy == (0.0, 0.0):
            self.local_xy = self.xy

    @property
    def x(self) -> float:
        """Center X coordinate."""
        return self.xy[0]

    @property
    def y(self) -> float:
        """Center Y coordinate."""
        return self.xy[1]

    @property
    def center(self) -> tuple[float, float]:
        """Center (cx, cy) coordinate."""
        return self.xy

    @property
    def size(self) -> tuple[float, float]:
        """Node dimensions (width, height)."""
        return (self.width, self.height)

    @property
    def left(self) -> float:
        """Left edge X coordinate."""
        return round(self.xy[0] - self.width / 2.0, 2)

    @property
    def right(self) -> float:
        """Right edge X coordinate."""
        return round(self.xy[0] + self.width / 2.0, 2)

    @property
    def bottom(self) -> float:
        """Bottom edge Y coordinate."""
        return round(self.xy[1] - self.height / 2.0, 2)

    @property
    def top(self) -> float:
        """Top edge Y coordinate."""
        return round(self.xy[1] + self.height / 2.0, 2)

    @property
    def bottom_left(self) -> tuple[float, float]:
        """Bottom-left (left, bottom) coordinate."""
        return (self.left, self.bottom)

    @property
    def local_bottom_left(self) -> tuple[float, float]:
        """Bottom-left coordinate relative to the parent cluster's bottom-left origin."""
        lx, ly = self.local_xy
        return (round(lx - self.width / 2.0, 2), round(ly - self.height / 2.0, 2))


@dataclass
class EdgeLayout:
    """Calculated routing path for an edge."""

    src: str
    dst: str
    src_port: tuple[float, float]
    dst_port: tuple[float, float]
    waypoints: list[tuple[float, float]] = field(default_factory=list)

    @property
    def points(self) -> list[tuple[float, float]]:
        """All consecutive points defining the edge path."""
        return [self.src_port, *self.waypoints, self.dst_port]

    @property
    def mid_xy(self) -> tuple[float, float]:
        """Midpoint coordinate along the routed path."""
        pts = self.points
        if len(pts) == 2:
            return (
                round((pts[0][0] + pts[1][0]) / 2.0, 2),
                round((pts[0][1] + pts[1][1]) / 2.0, 2),
            )
        mid_idx = len(pts) // 2
        p1 = pts[mid_idx - 1]
        p2 = pts[mid_idx]
        return (
            round((p1[0] + p2[0]) / 2.0, 2),
            round((p1[1] + p2[1]) / 2.0, 2),
        )


@dataclass
class ClusterLayout:
    """Calculated bounding box and hierarchy coordinates for a cluster."""

    id: str
    bbox: tuple[float, float, float, float]  # (cx, cy, width, height)
    parent_id: str | None = None
    local_bottom_left: tuple[float, float] = (0.0, 0.0)

    def __post_init__(self) -> None:
        if self.parent_id is None and self.local_bottom_left == (0.0, 0.0):
            self.local_bottom_left = self.bottom_left

    @property
    def cx(self) -> float:
        """Cluster center X coordinate."""
        return self.bbox[0]

    @property
    def cy(self) -> float:
        """Cluster center Y coordinate."""
        return self.bbox[1]

    @property
    def xy(self) -> tuple[float, float]:
        """Cluster center (cx, cy) coordinate."""
        return (self.bbox[0], self.bbox[1])

    @property
    def center(self) -> tuple[float, float]:
        """Cluster center (cx, cy) coordinate."""
        return (self.bbox[0], self.bbox[1])

    @property
    def width(self) -> float:
        """Cluster width."""
        return self.bbox[2]

    @property
    def height(self) -> float:
        """Cluster height."""
        return self.bbox[3]

    @property
    def size(self) -> tuple[float, float]:
        """Cluster dimensions (width, height)."""
        return (self.bbox[2], self.bbox[3])

    @property
    def left(self) -> float:
        """Left edge X coordinate."""
        return round(self.bbox[0] - self.bbox[2] / 2.0, 2)

    @property
    def right(self) -> float:
        """Right edge X coordinate."""
        return round(self.bbox[0] + self.bbox[2] / 2.0, 2)

    @property
    def top(self) -> float:
        """Top edge Y coordinate."""
        return round(self.bbox[1] + self.bbox[3] / 2.0, 2)

    @property
    def bottom(self) -> float:
        """Bottom edge Y coordinate."""
        return round(self.bbox[1] - self.bbox[3] / 2.0, 2)

    @property
    def bottom_left(self) -> tuple[float, float]:
        """Bottom-left (left, bottom) coordinate."""
        return (self.left, self.bottom)


@dataclass
class GraphLayout:
    """Complete geometrical result calculated by graph solvers."""

    nodes: dict[str, NodeLayout] = field(default_factory=dict)
    edges: list[EdgeLayout] = field(default_factory=list)
    clusters: dict[str, ClusterLayout] = field(default_factory=dict)
    width: float = 100.0
    height: float = 100.0
    ring_radii: dict[int, float] = field(default_factory=dict)

    def __getitem__(self, key: str) -> NodeLayout | ClusterLayout:
        """Look up a NodeLayout or ClusterLayout by ID."""
        if key in self.nodes:
            return self.nodes[key]
        if key in self.clusters:
            return self.clusters[key]
        raise KeyError(f"'{key}' not found in nodes or clusters of GraphLayout.")

    def offset(self, node_id: str, dx: float = 0.0, dy: float = 0.0) -> Self:
        """Shift a specific node and recalculate incident edge ports.

        Args:
            node_id: ID of the node to move.
            dx: Horizontal delta to shift.
            dy: Vertical delta to shift.

        Returns:
            Self: This GraphLayout instance for method chaining.

        Raises:
            KeyError: If node_id does not exist in the layout.
        """
        if node_id not in self.nodes:
            raise KeyError(f"Node '{node_id}' not found in layout.")

        nl = self.nodes[node_id]
        new_xy = (round(nl.xy[0] + dx, 2), round(nl.xy[1] + dy, 2))
        old_local = nl.local_xy if nl.local_xy is not None else nl.xy
        new_local_xy = (round(old_local[0] + dx, 2), round(old_local[1] + dy, 2))
        self.nodes[node_id] = NodeLayout(
            id=nl.id,
            xy=new_xy,
            width=nl.width,
            height=nl.height,
            parent_id=nl.parent_id,
            local_xy=new_local_xy,
        )

        # Shift incident edge ports
        for edge in self.edges:
            if edge.src == node_id:
                edge.src_port = (round(edge.src_port[0] + dx, 2), round(edge.src_port[1] + dy, 2))
            if edge.dst == node_id:
                edge.dst_port = (round(edge.dst_port[0] + dx, 2), round(edge.dst_port[1] + dy, 2))

        return self

    def _format_clusters(self) -> list[str]:
        if not self.clusters:
            return []
        max_cid = max(len(cid) for cid in self.clusters)
        out = ["Clusters:"]
        for cid, cl in self.clusters.items():
            line = f"  {cid:<{max_cid}} : bottom_left={cl.bottom_left}, center={cl.center}, size={cl.size}"
            if cl.parent_id is not None:
                line += f", parent={cl.parent_id!r}, local_bottom_left={cl.local_bottom_left}"
            out.append(line)
        return out

    def _format_nodes(self) -> list[str]:
        if not self.nodes:
            return []
        max_nid = max(len(nid) for nid in self.nodes)
        out = ["Nodes:"]
        for nid, nl in self.nodes.items():
            line = f"  {nid:<{max_nid}} : xy={nl.xy}, bottom_left={nl.bottom_left}, size={nl.size}"
            if nl.parent_id is not None:
                line += f", parent={nl.parent_id!r}, local_xy={nl.local_xy}"
            out.append(line)
        return out

    def __str__(self) -> str:
        """Format a human- and AI-readable coordinate table for layout inspection."""
        lines: list[str] = [f"GraphLayout(width={self.width:.1f}, height={self.height:.1f})"]

        rings_str = ", ".join(f"ring {r}: r={rad:.1f}" for r, rad in sorted(self.ring_radii.items()) if r > 0)
        if rings_str:
            lines.append(f"Ring Radii: {rings_str}")

        lines.extend(self._format_clusters())
        lines.extend(self._format_nodes())

        if self.edges:
            lines.append("Edges:")
            lines.extend(f"  {el.src} -> {el.dst} : points={el.points}, mid_xy={el.mid_xy}" for el in self.edges)

        return "\n".join(lines)
