# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""ArchitectureGraph class for declarative system and cloud architecture visualization."""

from __future__ import annotations

from typing import Literal

from drawlib._core.l4_canvas import canvas
from drawlib._graph._architecture._solver import solve_architecture_layout
from drawlib._graph._common._base import BaseGraph
from drawlib._graph._common._models import (
    ClusterLayout,
    EdgeLayout,
    GraphLayout,
    NodeLayout,
)
from drawlib._graph._common._routing import route_orthogonal_edge, route_straight_edge
from drawlib.fonts import Font
from drawlib.styles import Style, Styles


class ArchitectureGraph(BaseGraph):
    """Declarative 2-level macro/micro architecture graph layout solver.

    Lays out top-level architectural containers (VPCs, clusters, client zones,
    external SaaS) along the macro flow direction while automatically ordering
    internal services, subnets, and databases within their respective boundaries.
    """

    def __init__(
        self,
        *,
        direction: Literal["LR", "TB"] = "LR",
        container_sep: float | None = None,
        edge_routing: Literal["orthogonal", "straight"] = "orthogonal",
        default_node_style: Style | None = None,
        default_node_text_style: Style | None = None,
        default_edge_style: Style | None = None,
        default_edge_text_style: Style | None = None,
        default_container_style: Style | None = None,
        default_node_width: float = 24.0,
        default_node_height: float = 12.0,
    ) -> None:
        """Initialize ArchitectureGraph solver.

        Args:
            direction: Macro flow direction ("LR" for Left-to-Right, "TB" for Top-to-Bottom).
            container_sep: Distance between adjacent top-level containers. If None, auto-scales.
            edge_routing: Edge path style ("orthogonal" for Manhattan right angles, or "straight").
            default_node_style: Default style for nodes.
            default_node_text_style: Default text style for node labels.
            default_edge_style: Default style for edges.
            default_edge_text_style: Default text style for edge labels.
            default_container_style: Default style for container boundaries.
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
        self.direction: Literal["LR", "TB"] = direction
        self.container_sep: float | None = container_sep
        self.edge_routing: Literal["orthogonal", "straight"] = edge_routing
        self.default_container_style: Style = default_container_style or Styles.MutedDashed

    def calc(  # noqa: C901
        self,
        *,
        width: float | None = None,
        height: float | None = None,
        margin: float = 10.0,
    ) -> GraphLayout:
        """Compute compound macro/micro architecture coordinates without rendering.

        Args:
            width: Target canvas width. Defaults to canvas._width or 160.0.
            height: Target canvas height. Defaults to canvas._height or 90.0.
            margin: Outer margin surrounding the diagram.

        Returns:
            A GraphLayout containing all computed node, edge, and container geometries.
        """
        w = width if width is not None else float(getattr(canvas, "_width", 160.0))
        h = height if height is not None else float(getattr(canvas, "_height", 90.0))

        if not self._nodes and not self._edges and not self._clusters:
            return GraphLayout(width=w, height=h)

        # Auto-register nodes mentioned in edges
        for edge in self._edges:
            if edge.src not in self._nodes:
                self.node(edge.src)
            if edge.dst not in self._nodes:
                self.node(edge.dst)

        # Auto-register nodes mentioned in clusters
        for cluster in self._clusters.values():
            for nid in cluster.nodes:
                if nid not in self._nodes:
                    self.node(nid)

        # Auto-register clusters mentioned in node group/subgroup attributes
        for node in self._nodes.values():
            if node.group and node.group not in self._clusters:
                self.cluster(id=node.group, nodes=[], label=node.group)
            if node.subgroup and node.subgroup not in self._clusters:
                self.cluster(id=node.subgroup, nodes=[], label=node.subgroup, parent=node.group)
            elif node.subgroup and node.group and not self._clusters[node.subgroup].parent:
                self._clusters[node.subgroup].parent = node.group

        node_coords, cluster_boxes = solve_architecture_layout(
            nodes=self._nodes,
            edges=self._edges,
            clusters=self._clusters,
            direction=self.direction,
            container_sep=self.container_sep,
            width=w,
            height=h,
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

        # Route Edges
        is_compass = any(c.pos is not None for c in self._clusters.values())
        edges_layout: list[EdgeLayout] = []
        for edge in self._edges:
            src_nl = nodes_layout[edge.src]
            dst_nl = nodes_layout[edge.dst]

            if is_compass:
                dx = dst_nl.x - src_nl.x
                dy = dst_nl.y - src_nl.y
                if abs(dx) >= abs(dy):
                    edge_dir: Literal["TB", "BT", "LR", "RL"] = "LR" if dx >= 0 else "RL"
                else:
                    edge_dir = "BT" if dy >= 0 else "TB"
            else:
                edge_dir = self.direction

            if self.edge_routing == "orthogonal":
                src_port, waypoints, dst_port = route_orthogonal_edge(src_nl, dst_nl, direction=edge_dir)
            else:
                src_port, waypoints, dst_port = route_straight_edge(src_nl, dst_nl, direction=edge_dir)

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

        # Build ClusterLayout objects for containers
        clusters_layout: dict[str, ClusterLayout] = {}
        default_cluster_text_style = Style(
            text_size=10,
            text_font=Font.SANSSERIF_BOLD,
            text_color=(100, 100, 105, 1.0),
            text_halign="left",
            text_valign="top",
        )

        for cid, (cx, cy, cw, ch) in cluster_boxes.items():
            cluster_meta = self._clusters.get(cid)
            lbl = cluster_meta.label if cluster_meta else cid
            style = (cluster_meta.style if cluster_meta and cluster_meta.style else self.default_container_style)
            t_style = (
                default_cluster_text_style.patch(cluster_meta.text_style)
                if cluster_meta and cluster_meta.text_style
                else default_cluster_text_style
            )
            c_show = cluster_meta.show if cluster_meta is not None else True
            clusters_layout[cid] = ClusterLayout(
                id=cid,
                label=lbl,
                bbox=(cx, cy, cw, ch),
                style=style,
                text_style=t_style,
                shape="rectangle",
                show=c_show,
            )

        return GraphLayout(
            nodes=nodes_layout,
            edges=edges_layout,
            clusters=clusters_layout,
            width=w,
            height=h,
        )
