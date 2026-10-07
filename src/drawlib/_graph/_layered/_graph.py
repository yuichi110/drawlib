# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""LayerGraph class for declarative hierarchical DAG and pipeline visualization."""

from __future__ import annotations

from typing import Literal

from drawlib._core.l4_canvas import canvas
from drawlib._graph._common._base import BaseGraph
from drawlib._graph._common._models import EdgeLayout, GraphLayout
from drawlib._graph._common._routing import route_orthogonal_edge, route_straight_edge
from drawlib._graph._layered._solver import solve_layered_layout
from drawlib.styles import Style


class LayerGraph(BaseGraph):
    """Declarative layered hierarchical graph layout solver.

    Uses the Sugiyama framework (cycle breaking, longest-path layering, barycenter
    crossing reduction) to arrange nodes into tidy sequential tiers with minimal line crossings.
    Ideal for CI/CD pipelines, data lineage (ETL / dbt / Airflow), task scheduling DAGs,
    and module dependency graphs.
    """

    def __init__(
        self,
        *,
        direction: Literal["LR", "TB"] = "LR",
        rank_sep: float | None = None,
        node_sep: float | None = None,
        edge_routing: Literal["orthogonal", "straight"] = "orthogonal",
        default_node_style: Style | None = None,
        default_node_text_style: Style | None = None,
        default_edge_style: Style | None = None,
        default_edge_text_style: Style | None = None,
        default_node_width: float = 22.0,
        default_node_height: float = 12.0,
    ) -> None:
        """Initialize LayerGraph solver.

        Args:
            direction: Layout flow direction ("LR" for Left-to-Right, "TB" for Top-to-Bottom).
            rank_sep: Fixed distance between successive layers. If None, auto-scales.
            node_sep: Fixed minimum distance between nodes in the same layer. If None, auto-scales.
            edge_routing: Edge routing style ("orthogonal" for Manhattan right-angles, or "straight").
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
        self.direction: Literal["LR", "TB"] = direction
        self.rank_sep: float | None = rank_sep
        self.node_sep: float | None = node_sep
        self.edge_routing: Literal["orthogonal", "straight"] = edge_routing

    def tier(
        self,
        name: str,
        nodes: list[str],
        *,
        layer: int | None = None,
    ) -> None:
        """Explicitly assign multiple nodes to a specific layer/rank.

        Args:
            name: Semantic tier name (for identification/documentation).
            nodes: List of node IDs assigned to this tier.
            layer: Optional explicit integer layer index (0, 1, 2...).
        """
        for nid in nodes:
            if nid not in self._nodes:
                self.node(nid)
            if layer is not None:
                self._nodes[nid].layer = layer

    def calc(
        self,
        *,
        width: float | None = None,
        height: float | None = None,
        margin: float = 10.0,
    ) -> GraphLayout:
        """Compute tidy hierarchical layered coordinates without rendering.

        Args:
            width: Target canvas width. Defaults to canvas._width or 120.0.
            height: Target canvas height. Defaults to canvas._height or 70.0 (LR) / 90.0 (TB).
            margin: Outer margin surrounding the diagram.

        Returns:
            A GraphLayout containing all computed node, edge, and cluster geometries.
        """
        fallback_h = 70.0 if self.direction == "LR" else 90.0
        w = width if width is not None else float(getattr(canvas, "_width", 120.0))
        h = height if height is not None else float(getattr(canvas, "_height", fallback_h))

        if not self._nodes and not self._edges:
            return GraphLayout(width=w, height=h)

        self._ensure_edge_nodes()

        node_coords, _ = solve_layered_layout(
            nodes=self._nodes,
            edges=self._edges,
            direction=self.direction,
            rank_sep=self.rank_sep,
            node_sep=self.node_sep,
            width=w,
            height=h,
            margin=margin,
            default_node_width=self.default_node_width,
            default_node_height=self.default_node_height,
        )

        nodes_layout = self._build_nodes_layout(node_coords)

        edges_layout: list[EdgeLayout] = []
        for edge in self._edges:
            src_nl = nodes_layout[edge.src]
            dst_nl = nodes_layout[edge.dst]

            if self.edge_routing == "orthogonal":
                src_port, waypoints, dst_port = route_orthogonal_edge(src_nl, dst_nl, direction=self.direction)
            else:
                src_port, waypoints, dst_port = route_straight_edge(src_nl, dst_nl, direction=self.direction)

            edges_layout.append(self._build_edge_layout(edge, src_port, waypoints, dst_port))

        clusters_layout = self._build_clusters_layout(nodes_layout)

        return GraphLayout(
            nodes=nodes_layout,
            edges=edges_layout,
            clusters=clusters_layout,
            width=w,
            height=h,
        )
