# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GridGraph class for declarative matrix and layered grid visualization."""

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
from drawlib._graph._common._routing import route_grid_edge
from drawlib._graph._grid._solver import solve_grid_layout
from drawlib.fonts import Font
from drawlib.styles import Style, Styles


class GridGraph(BaseGraph):
    """Declarative matrix grid graph layout solver.

    Tiles nodes in a regular matrix grid with customizable column count, ordering
    ("row-major" or "column-major"), and spacing. Supports explicit (row, col) slot pinning
    for arbitrary architecture topologies, microservice matrixes, and layered tier diagrams.
    """

    def __init__(
        self,
        columns: int = 3,
        *,
        rows: int | None = None,
        order: Literal["row-major", "column-major"] = "row-major",
        col_sep: float | None = None,
        row_sep: float | None = None,
        edge_routing: Literal["smart", "orthogonal", "straight"] = "smart",
        default_node_style: Style | None = None,
        default_node_text_style: Style | None = None,
        default_edge_style: Style | None = None,
        default_edge_text_style: Style | None = None,
        default_node_width: float = 20.0,
        default_node_height: float = 12.0,
    ) -> None:
        """Initialize GridGraph solver.

        Args:
            columns: Number of grid columns (defaults to 3).
            rows: Optional fixed number of rows (used primarily in column-major order).
            order: Flow ordering for unpinned nodes ("row-major" or "column-major").
            col_sep: Fixed horizontal separation between columns. If None, auto-scales to canvas.
            row_sep: Fixed vertical separation between rows. If None, auto-scales to canvas.
            edge_routing: Routing algorithm ("smart", "orthogonal", "straight").
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
        self.columns: int = max(1, columns)
        self.rows: int | None = rows
        self.order: Literal["row-major", "column-major"] = order
        self.col_sep: float | None = col_sep
        self.row_sep: float | None = row_sep
        self.edge_routing: Literal["smart", "orthogonal", "straight"] = edge_routing
        self._row_clusters: list[tuple[int, str, str | None, Style | None, Style | None, float]] = []
        self._col_clusters: list[tuple[int, str, str | None, Style | None, Style | None, float]] = []

    def cell(
        self,
        cell_id: str,
        row: int | None = None,
        col: int | None = None,
        label: str | None = None,
        *,
        style: Style | None = None,
        text_style: Style | None = None,
        shape: Literal["rectangle", "circle", "rounded_rectangle"] = "rectangle",
        icon: str | None = None,
        width: float | None = None,
        height: float | None = None,
    ) -> Node:
        """Convenience method to register a grid cell node at an optional (row, col) position.

        Args:
            cell_id: Unique identifier for the node.
            row: Optional row index (0-based, top row is 0).
            col: Optional column index (0-based, leftmost column is 0).
            label: Text label displayed on the node. Defaults to cell_id if None.
            style: Shape styling for this node.
            text_style: Text styling for the node label.
            shape: Shape geometry ("rectangle", "circle", "rounded_rectangle").
            icon: Optional icon name or path.
            width: Custom width for this node.
            height: Custom height for this node.

        Returns:
            The registered Node object.
        """
        return self.node(
            id=cell_id,
            label=label,
            style=style,
            text_style=text_style,
            shape=shape,
            icon=icon,
            width=width,
            height=height,
            row=row,
            col=col,
        )

    def cluster_row(
        self,
        row: int,
        cluster_id: str,
        label: str | None = None,
        *,
        style: Style | None = None,
        text_style: Style | None = None,
        padding: float = 4.0,
    ) -> None:
        """Register a cluster grouping all nodes in a specific row.

        The actual member nodes are dynamically resolved during calc() based on
        their final row assignment.

        Args:
            row: Row index (0-based).
            cluster_id: Unique identifier for the cluster.
            label: Optional title displayed on the cluster.
            style: Box and border style for the cluster boundary.
            text_style: Text style for the cluster label.
            padding: Margin surrounding the member nodes.

        Raises:
            ValueError: If cluster_id is already registered.
        """
        if cluster_id in self._clusters or any(cid == cluster_id for _, cid, _, _, _, _ in self._row_clusters):
            raise ValueError(f"Cluster '{cluster_id}' is already registered in the graph.")
        self._row_clusters.append((row, cluster_id, label, style, text_style, padding))

    def cluster_column(
        self,
        col: int,
        cluster_id: str,
        label: str | None = None,
        *,
        style: Style | None = None,
        text_style: Style | None = None,
        padding: float = 4.0,
    ) -> None:
        """Register a cluster grouping all nodes in a specific column.

        The actual member nodes are dynamically resolved during calc() based on
        their final column assignment.

        Args:
            col: Column index (0-based).
            cluster_id: Unique identifier for the cluster.
            label: Optional title displayed on the cluster.
            style: Box and border style for the cluster boundary.
            text_style: Text style for the cluster label.
            padding: Margin surrounding the member nodes.

        Raises:
            ValueError: If cluster_id is already registered.
        """
        if cluster_id in self._clusters or any(cid == cluster_id for _, cid, _, _, _, _ in self._col_clusters):
            raise ValueError(f"Cluster '{cluster_id}' is already registered in the graph.")
        self._col_clusters.append((col, cluster_id, label, style, text_style, padding))

    def calc(  # noqa: C901
        self,
        *,
        width: float | None = None,
        height: float | None = None,
        margin: float = 10.0,
    ) -> GraphLayout:
        """Compute matrix grid coordinates and edge paths without rendering.

        Args:
            width: Target canvas width. Defaults to canvas._width or 120.0.
            height: Target canvas height. Defaults to canvas._height or 80.0.
            margin: Outer margin surrounding the grid diagram.

        Returns:
            A GraphLayout containing all computed node, edge, and cluster geometries.
        """
        w = width if width is not None else float(getattr(canvas, "_width", 120.0))
        h = height if height is not None else float(getattr(canvas, "_height", 80.0))

        if not self._nodes and not self._edges:
            return GraphLayout(width=w, height=h)

        # Auto-register nodes mentioned in edges
        for edge in self._edges:
            if edge.src not in self._nodes:
                self.node(edge.src)
            if edge.dst not in self._nodes:
                self.node(edge.dst)

        node_coords, slot_map = solve_grid_layout(
            nodes=self._nodes,
            columns=self.columns,
            rows=self.rows,
            order=self.order,
            col_sep=self.col_sep,
            row_sep=self.row_sep,
            width=w,
            height=h,
            margin=margin,
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
            )

        # Route Edges
        edges_layout: list[EdgeLayout] = []
        for edge in self._edges:
            src_nl = nodes_layout[edge.src]
            dst_nl = nodes_layout[edge.dst]

            src_port, waypoints, dst_port = route_grid_edge(src_nl, dst_nl, routing_style=self.edge_routing)
            edges_layout.append(
                EdgeLayout(
                    src=edge.src,
                    dst=edge.dst,
                    src_port=src_port,
                    dst_port=dst_port,
                    waypoints=waypoints,
                    label=edge.label,
                    style=edge.style or self.default_edge_style,
                    text_style=edge.text_style or self.default_edge_text_style,
                    arrow_head=edge.arrow_head,
                )
            )

        # Dynamic row/col clusters into self._clusters
        for r_idx, cid, lbl, st, t_st, pad in self._row_clusters:
            row_nodes = [nid for nid, (r, _) in slot_map.items() if r == r_idx]
            if row_nodes and cid not in self._clusters:
                self.cluster(cid, nodes=row_nodes, label=lbl, style=st, text_style=t_st, padding=pad)

        for c_idx, cid, lbl, st, t_st, pad in self._col_clusters:
            col_nodes = [nid for nid, (_, c) in slot_map.items() if c == c_idx]
            if col_nodes and cid not in self._clusters:
                self.cluster(cid, nodes=col_nodes, label=lbl, style=st, text_style=t_st, padding=pad)

        # Compute Clusters
        clusters_layout: dict[str, ClusterLayout] = {}
        default_cluster_text_style = Style(
            text_size=10,
            text_font=Font.SANSSERIF_BOLD,
            text_color=(100, 100, 105, 1.0),
            text_halign="left",
            text_valign="top",
        )
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
                )

        return GraphLayout(
            nodes=nodes_layout,
            edges=edges_layout,
            clusters=clusters_layout,
            width=w,
            height=h,
        )
