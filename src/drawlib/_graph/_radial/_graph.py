# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""RadialGraph class for concentric ring and hub-and-spoke visualization."""

from __future__ import annotations

from typing import Literal

from drawlib._core.l4_canvas import canvas
from drawlib._graph._common._base import BaseGraph
from drawlib._graph._common._models import (
    ClusterLayout,
    EdgeLayout,
    GraphLayout,
    Node,
    NodeLayout,
)
from drawlib._graph._common._routing import route_radial_edge
from drawlib._graph._radial._solver import solve_radial_layout
from drawlib.fonts import Font
from drawlib.styles import Style, Styles


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
        draw_ring_guides: bool = False,
        ring_guide_style: Style | None = None,
        default_node_style: Style | None = None,
        default_node_text_style: Style | None = None,
        default_edge_style: Style | None = None,
        default_edge_text_style: Style | None = None,
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
            draw_ring_guides: Whether to draw subtle dashed circular guidelines for each ring.
            ring_guide_style: Custom style for the ring guideline circles.
            default_node_style: Default style for nodes.
            default_node_text_style: Default text style for node labels.
            default_edge_style: Default style for edges.
            default_edge_text_style: Default text style for edge labels.
            default_node_width: Default width for nodes.
            default_node_height: Default height for nodes.
        """
        super().__init__(
            default_node_style=default_node_style,
            default_node_text_style=default_node_text_style,
            default_edge_style=default_edge_style,
            default_edge_text_style=default_edge_text_style,
            default_node_width=default_node_width,
            default_node_height=default_node_height,
        )
        self.hub: str | None = hub
        self.center: tuple[float, float] | None = center
        self.radius_step: float | None = radius_step
        self.start_angle: float = start_angle
        self.angle_range: float = angle_range
        self.draw_ring_guides: bool = draw_ring_guides
        self.ring_guide_style: Style | None = ring_guide_style

    def spoke(
        self,
        parent: str,
        spoke_id: str,
        label: str | None = None,
        *,
        ring: int | None = None,
        style: Style | None = None,
        text_style: Style | None = None,
        shape: Literal["rectangle", "circle", "rounded_rectangle"] = "rectangle",
        icon: str | None = None,
        width: float | None = None,
        height: float | None = None,
        edge_label: str | None = None,
        edge_style: Style | None = None,
        arrow_head: Literal["->", "<-", "<->", "-"] = "->",
        show: bool = True,
        edge_show: bool = True,
    ) -> Node:
        """Convenience method to register a spoke node connected from an existing parent/hub.

        Args:
            parent: Parent or hub node ID. Will be auto-registered if not present.
            spoke_id: Unique identifier for the spoke node.
            label: Text label displayed on spoke node. Defaults to spoke_id if None.
            ring: Optional explicit concentric ring index (1, 2, ...).
            style: Shape styling for spoke node.
            text_style: Text styling for spoke node label.
            shape: Shape geometry of spoke node.
            icon: Optional icon name or path.
            width: Custom width for spoke node.
            height: Custom height for spoke node.
            edge_label: Annotation text on connecting edge.
            edge_style: Style of connecting edge.
            arrow_head: Arrowhead decoration ("->", "<-", "<->", "-").
            show: Whether to render the spoke node.
            edge_show: Whether to render the connecting edge.

        Returns:
            The registered spoke Node object.
        """
        if parent not in self._nodes:
            self.node(parent)

        n = self.node(
            id=spoke_id,
            label=label,
            style=style,
            text_style=text_style,
            shape=shape,
            icon=icon,
            width=width,
            height=height,
            ring=ring,
            show=show,
        )
        self.edge(
            src=parent,
            dst=spoke_id,
            label=edge_label,
            style=edge_style,
            arrow_head=arrow_head,
            show=edge_show,
        )
        return n

    def calc(  # noqa: C901
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

        # Auto-register nodes mentioned in edges
        for edge in self._edges:
            if edge.src not in self._nodes:
                self.node(edge.src)
            if edge.dst not in self._nodes:
                self.node(edge.dst)

        # Determine origin center
        cx, cy = self.center if self.center is not None else (round(w / 2.0, 2), round(h / 2.0, 2))

        avail_w = max(w - 2.0 * margin, 20.0)
        avail_h = max(h - 2.0 * margin, 20.0)

        node_coords, node_rings, ring_radii = solve_radial_layout(
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

        # Build NodeLayout objects
        nodes_layout: dict[str, NodeLayout] = {}
        for nid, (nx, ny) in node_coords.items():
            node = self._nodes[nid]
            nw = node.width or self.default_node_width
            nh = node.height or self.default_node_height
            nodes_layout[nid] = NodeLayout(
                id=nid,
                xy=(nx, ny),
                width=nw,
                height=nh,
                style=node.style or self.default_node_style,
                text_style=node.text_style or self.default_node_text_style,
                label=node.label or nid,
                shape=node.shape,
                icon=node.icon,
                show=node.show,
            )

        # Route Edges directly with boundary intersections
        edges_layout: list[EdgeLayout] = []
        for edge in self._edges:
            src_nl = nodes_layout[edge.src]
            dst_nl = nodes_layout[edge.dst]

            src_port, waypoints, dst_port = route_radial_edge(src_nl, dst_nl)
            edges_layout.append(
                EdgeLayout(
                    src=edge.src,
                    dst=edge.dst,
                    src_port=src_port,
                    dst_port=dst_port,
                    waypoints=waypoints,
                    label=edge.label,
                    style=self._resolve_edge_style(edge),
                    text_style=edge.text_style or self.default_edge_text_style,
                    arrow_head=edge.arrow_head,
                    show=edge.show,
                )
            )

        # Compute Clusters
        clusters_layout: dict[str, ClusterLayout] = {}
        default_cluster_text_style = Style(
            text_size=10,
            text_font=Font.SANSSERIF_BOLD,
            text_color=(100, 100, 105, 1.0),
            text_halign="left",
            text_valign="top",
        )

        # Optional Ring Guideline Circles
        if self.draw_ring_guides:
            guide_style = self.ring_guide_style or Styles.MutedDashed
            for r, radius in ring_radii.items():
                if r > 0 and radius > 0:
                    guide_id = f"__ring_guide_{r}__"
                    diam = round(radius * 2.0, 2)
                    clusters_layout[guide_id] = ClusterLayout(
                        id=guide_id,
                        label=None,
                        bbox=(cx, cy, diam, diam),
                        style=guide_style,
                        text_style=default_cluster_text_style,
                        shape="circle",
                    )

        # User-defined clusters
        for cid, cluster in self._clusters.items():
            member_nodes = [nodes_layout[nid] for nid in cluster.nodes if nid in nodes_layout]
            if member_nodes:
                top_extra = 3.5 if cluster.label else 0.0
                min_x = min(n.left for n in member_nodes) - cluster.padding
                max_x = max(n.right for n in member_nodes) + cluster.padding
                min_y = min(n.bottom for n in member_nodes) - cluster.padding
                max_y = max(n.top for n in member_nodes) + cluster.padding + top_extra
                cw = round(max_x - min_x, 2)
                ch = round(max_y - min_y, 2)
                cl_cx = round((min_x + max_x) / 2.0, 2)
                cl_cy = round((min_y + max_y) / 2.0, 2)
                c_text_style = (
                    default_cluster_text_style.patch(cluster.text_style)
                    if cluster.text_style is not None
                    else default_cluster_text_style
                )
                clusters_layout[cid] = ClusterLayout(
                    id=cid,
                    label=cluster.label,
                    bbox=(cl_cx, cl_cy, cw, ch),
                    style=cluster.style or Styles.MutedDashed,
                    text_style=c_text_style,
                    shape="rectangle",
                    show=cluster.show,
                )

        return GraphLayout(
            nodes=nodes_layout,
            edges=edges_layout,
            clusters=clusters_layout,
            width=w,
            height=h,
        )
