# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""RadialGraph class for concentric ring and hub-and-spoke layout calculation."""

from __future__ import annotations

from drawlib._core.l4_canvas import canvas
from drawlib._graph._common._base import BaseGraph
from drawlib._graph._common._models import (
    EdgeLayout,
    GraphLayout,
    Node,
)
from drawlib._graph._common._routing import route_radial_edge
from drawlib._graph._radial._solver import solve_radial_layout


class RadialGraph(BaseGraph):
    """Declarative radial and concentric-ring graph layout solver.

    Places a central hub node at the origin and distributes connected or tiered
    spoke nodes across concentric orbital rings with even angular separation.
    Ideal for event-driven architectures, Pub/Sub topologies, Hub-and-Spoke networks,
    and mindmaps.
    """

    def __init__(
        self,
        hub: str | None = None,
        *,
        center: tuple[float, float] | None = None,
        radius_step: float | None = None,
        start_angle: float = 0.0,
        angle_range: float = 360.0,
        default_node_width: float = 20.0,
        default_node_height: float = 12.0,
    ) -> None:
        """Initialize RadialGraph solver.

        Args:
            hub: Optional ID of the central hub node. If omitted, automatically selects
                the node with the highest connectivity.
            center: Origin (cx, cy) of the concentric rings. Defaults to canvas center.
            radius_step: Fixed radial distance between successive rings. If None, auto-scales.
            start_angle: Angular starting position in degrees (0.0 is right/east, 90.0 is top/north).
            angle_range: Total sweep angle in degrees (e.g. 360.0 for full circle, 180.0 for semicircle).
            default_node_width: Default width for nodes.
            default_node_height: Default height for nodes.
        """
        super().__init__(
            default_node_width=default_node_width,
            default_node_height=default_node_height,
        )
        self.hub: str | None = hub
        self.center: tuple[float, float] | None = center
        self.radius_step: float | None = radius_step
        self.start_angle: float = start_angle
        self.angle_range: float = angle_range

    def spoke(
        self,
        parent: str,
        spoke_id: str,
        *,
        ring: int | None = None,
        width: float | None = None,
        height: float | None = None,
    ) -> Node:
        """Convenience method to register a spoke node connected from an existing parent/hub.

        Args:
            parent: Parent or hub node ID. Will be auto-registered if not present.
            spoke_id: Unique identifier for the spoke node.
            ring: Optional explicit concentric ring index (1, 2, ...).
            width: Custom width for spoke node.
            height: Custom height for spoke node.

        Returns:
            The registered spoke Node object.
        """
        if parent not in self._nodes:
            self.node(parent)

        n = self.node(
            id=spoke_id,
            ring=ring,
            width=width,
            height=height,
        )
        self.edge(src=parent, dst=spoke_id)
        return n

    def get_layout(
        self,
        *,
        width: float | None = None,
        height: float | None = None,
        margin: float = 10.0,
    ) -> GraphLayout:
        """Compute radial and concentric coordinates without rendering.

        Args:
            width: Target canvas width. Defaults to canvas._width or 120.0.
            height: Target canvas height. Defaults to canvas._height or 120.0.
            margin: Outer margin surrounding the radial diagram.

        Returns:
            A GraphLayout containing all computed node, edge, and cluster geometries.
        """
        w = width if width is not None else float(getattr(canvas, "_width", 120.0))
        h = height if height is not None else float(getattr(canvas, "_height", 120.0))

        if not self._nodes and not self._edges:
            return GraphLayout(width=w, height=h)

        self._ensure_edge_nodes()

        # Determine origin center
        cx, cy = self.center if self.center is not None else (round(w / 2.0, 2), round(h / 2.0, 2))

        avail_w = max(w - 2.0 * margin, 20.0)
        avail_h = max(h - 2.0 * margin, 20.0)

        node_coords, _node_rings, ring_radii = solve_radial_layout(
            nodes=self._nodes,
            edges=self._edges,
            hub_id=self.hub,
            center=(cx, cy),
            radius_step=self.radius_step,
            start_angle=self.start_angle,
            angle_range=self.angle_range,
            avail_w=avail_w,
            avail_h=avail_h,
            default_node_width=self.default_node_width,
            default_node_height=self.default_node_height,
        )

        nodes_layout = self._build_nodes_layout(node_coords)

        # Route Edges directly with boundary intersections
        edges_layout: list[EdgeLayout] = []
        for edge in self._edges:
            src_nl = nodes_layout[edge.src]
            dst_nl = nodes_layout[edge.dst]

            src_port, waypoints, dst_port = route_radial_edge(src_nl, dst_nl)
            edges_layout.append(self._build_edge_layout(edge, src_port, waypoints, dst_port))

        clusters_layout = self._build_clusters_layout(nodes_layout)

        return GraphLayout(
            nodes=nodes_layout,
            edges=edges_layout,
            clusters=clusters_layout,
            width=w,
            height=h,
            ring_radii=ring_radii,
        )
