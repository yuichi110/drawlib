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
    Cluster,
    EdgeLayout,
    GraphLayout,
    Node,
)
from drawlib._graph._common._routing import route_grid_edge
from drawlib._graph._grid._solver import solve_grid_layout
from drawlib.styles import Style


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
        self._row_clusters: list[tuple[int, str]] = []
        self._col_clusters: list[tuple[int, str]] = []

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
        show: bool = True,
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
            show: Whether to render this cell node.

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
            show=show,
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
        show: bool = True,
    ) -> Cluster:
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
            show: Whether to render this row cluster.

        Returns:
            The registered Cluster object.

        Raises:
            ValueError: If cluster_id is already registered.
        """
        c = self.cluster(
            id=cluster_id,
            nodes=[],
            label=label,
            style=style,
            text_style=text_style,
            padding=padding,
            show=show,
        )
        self._row_clusters.append((row, cluster_id))
        return c

    def cluster_column(
        self,
        col: int,
        cluster_id: str,
        label: str | None = None,
        *,
        style: Style | None = None,
        text_style: Style | None = None,
        padding: float = 4.0,
        show: bool = True,
    ) -> Cluster:
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
            show: Whether to render this column cluster.

        Returns:
            The registered Cluster object.

        Raises:
            ValueError: If cluster_id is already registered.
        """
        c = self.cluster(
            id=cluster_id,
            nodes=[],
            label=label,
            style=style,
            text_style=text_style,
            padding=padding,
            show=show,
        )
        self._col_clusters.append((col, cluster_id))
        return c

    def calc(
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

        self._ensure_edge_nodes()

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

        nodes_layout = self._build_nodes_layout(node_coords)

        edges_layout: list[EdgeLayout] = []
        for edge in self._edges:
            src_nl = nodes_layout[edge.src]
            dst_nl = nodes_layout[edge.dst]

            src_port, waypoints, dst_port = route_grid_edge(src_nl, dst_nl, routing_style=self.edge_routing)
            edges_layout.append(self._build_edge_layout(edge, src_port, waypoints, dst_port))

        # Dynamic row/col clusters into self._clusters
        for r_idx, cid in self._row_clusters:
            row_nodes = [nid for nid, (r, _) in slot_map.items() if r == r_idx]
            if cid in self._clusters:
                self._clusters[cid].nodes = row_nodes

        for c_idx, cid in self._col_clusters:
            col_nodes = [nid for nid, (_, c) in slot_map.items() if c == c_idx]
            if cid in self._clusters:
                self._clusters[cid].nodes = col_nodes

        clusters_layout = self._build_clusters_layout(nodes_layout)

        return GraphLayout(
            nodes=nodes_layout,
            edges=edges_layout,
            clusters=clusters_layout,
            width=w,
            height=h,
        )
