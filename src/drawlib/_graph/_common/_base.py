# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Abstract base class and core contract for declarative graph coordinate solvers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Literal

from drawlib._graph._common._models import (
    Cluster,
    ClusterLayout,
    Edge,
    EdgeLayout,
    GraphLayout,
    Node,
    NodeLayout,
)


class BaseGraph(ABC):
    """Abstract base class for all declarative graph coordinate solvers.

    Provides node/edge/cluster registration methods and a uniform `get_layout()`
    interface for calculating topology coordinates without rendering.
    """

    def __init__(
        self,
        *,
        default_node_width: float = 20.0,
        default_node_height: float = 12.0,
    ) -> None:
        """Initialize base graph properties and defaults.

        Args:
            default_node_width: Default width for nodes when not explicitly specified.
            default_node_height: Default height for nodes when not explicitly specified.
        """
        self.default_node_width: float = default_node_width
        self.default_node_height: float = default_node_height

        self._nodes: dict[str, Node] = {}
        self._edges: list[Edge] = []
        self._clusters: dict[str, Cluster] = {}

    def _ensure_edge_nodes(self) -> None:
        """Auto-register any nodes referenced by edges that have not been explicitly registered."""
        for edge in self._edges:
            if edge.src not in self._nodes:
                self.node(edge.src)
            if edge.dst not in self._nodes:
                self.node(edge.dst)

    def _build_nodes_layout(
        self,
        node_coords: dict[str, tuple[float, float]],
    ) -> dict[str, NodeLayout]:
        """Build NodeLayout dictionary from computed (x, y) coordinates."""
        nodes_layout: dict[str, NodeLayout] = {}
        for nid, (nx, ny) in node_coords.items():
            node = self._nodes[nid]
            nw = node.width if node.width is not None else self.default_node_width
            nh = node.height if node.height is not None else self.default_node_height
            nodes_layout[nid] = NodeLayout(
                id=nid,
                xy=(nx, ny),
                width=nw,
                height=nh,
            )
        return nodes_layout

    @staticmethod
    def _build_edge_layout(
        edge: Edge,
        src_port: tuple[float, float],
        waypoints: list[tuple[float, float]],
        dst_port: tuple[float, float],
    ) -> EdgeLayout:
        """Construct an EdgeLayout from an Edge and routed port/waypoint coordinates."""
        return EdgeLayout(
            src=edge.src,
            dst=edge.dst,
            src_port=src_port,
            dst_port=dst_port,
            waypoints=waypoints,
        )

    def _build_clusters_layout(
        self,
        nodes_layout: dict[str, NodeLayout],
    ) -> dict[str, ClusterLayout]:
        """Compute bounding-box ClusterLayout dictionary from member NodeLayouts."""
        clusters_layout: dict[str, ClusterLayout] = {}
        for cid, cluster in self._clusters.items():
            member_nodes = [nodes_layout[nid] for nid in cluster.nodes if nid in nodes_layout]
            if member_nodes:
                min_x = min(n.left for n in member_nodes) - cluster.padding
                max_x = max(n.right for n in member_nodes) + cluster.padding
                min_y = min(n.bottom for n in member_nodes) - cluster.padding
                max_y = max(n.top for n in member_nodes) + cluster.padding + cluster.header_height
                cw = round(max_x - min_x, 2)
                ch = round(max_y - min_y, 2)
                cl_cx = round((min_x + max_x) / 2.0, 2)
                cl_cy = round((min_y + max_y) / 2.0, 2)
                clusters_layout[cid] = ClusterLayout(
                    id=cid,
                    bbox=(cl_cx, cl_cy, cw, ch),
                    parent_id=cluster.parent,
                )
        self._finalize_hierarchy_coords(nodes_layout, clusters_layout)
        return clusters_layout

    def _resolve_node_parent_cluster(
        self,
        nid: str,
        clusters_layout: dict[str, ClusterLayout],
        node_to_cluster: dict[str, str],
    ) -> str | None:
        """Determine the immediate parent cluster ID for a node."""
        node_meta = self._nodes.get(nid)
        if node_meta is not None:
            if node_meta.subgroup and node_meta.subgroup in clusters_layout:
                return node_meta.subgroup
            if node_meta.group and node_meta.group in clusters_layout:
                return node_meta.group
        return node_to_cluster.get(nid)

    def _finalize_hierarchy_coords(
        self,
        nodes_layout: dict[str, NodeLayout],
        clusters_layout: dict[str, ClusterLayout],
    ) -> None:
        """Populate parent_id, local_bottom_left on ClusterLayout and local_xy on NodeLayout."""
        for cid, cl in clusters_layout.items():
            cluster_meta = self._clusters.get(cid)
            parent_cid = cluster_meta.parent if cluster_meta is not None else cl.parent_id
            if parent_cid and parent_cid in clusters_layout:
                parent_cl = clusters_layout[parent_cid]
                cl.parent_id = parent_cid
                cl.local_bottom_left = (
                    round(cl.left - parent_cl.left, 2),
                    round(cl.bottom - parent_cl.bottom, 2),
                )
            else:
                cl.parent_id = None
                cl.local_bottom_left = cl.bottom_left

        node_to_cluster: dict[str, str] = {}
        for cid, cluster in self._clusters.items():
            if cid in clusters_layout:
                for nid in cluster.nodes:
                    if nid not in node_to_cluster or cluster.parent is not None:
                        node_to_cluster[nid] = cid

        for nid, nl in nodes_layout.items():
            parent_cid = self._resolve_node_parent_cluster(nid, clusters_layout, node_to_cluster)
            if parent_cid and parent_cid in clusters_layout:
                parent_cl = clusters_layout[parent_cid]
                nl.parent_id = parent_cid
                nl.local_xy = (
                    round(nl.x - parent_cl.left, 2),
                    round(nl.y - parent_cl.bottom, 2),
                )
            else:
                nl.parent_id = None
                nl.local_xy = nl.xy

    def node(
        self,
        id: str,
        *,
        width: float | None = None,
        height: float | None = None,
        ring: int | None = None,
        row: int | None = None,
        col: int | None = None,
        layer: int | None = None,
        group: str | None = None,
        subgroup: str | None = None,
    ) -> Node:
        """Register a node in the graph topology.

        Args:
            id: Unique identifier string for the node.
            width: Custom width for this node.
            height: Custom height for this node.
            ring: Optional concentric ring number (for radial layouts).
            row: Optional row index (for grid layouts).
            col: Optional column index (for grid layouts).
            layer: Optional layer/rank index (for layered layouts).
            group: Optional container/group ID (for architecture layouts).
            subgroup: Optional nested subgroup ID (for architecture layouts).

        Returns:
            The registered Node object.

        Raises:
            ValueError: If a node with the same id is already registered.
        """
        if id in self._nodes:
            raise ValueError(f"Node '{id}' is already registered in the graph.")

        n = Node(
            id=id,
            width=width,
            height=height,
            ring=ring,
            row=row,
            col=col,
            layer=layer,
            group=group,
            subgroup=subgroup,
        )
        self._nodes[id] = n
        return n

    def edge(
        self,
        src: str,
        dst: str,
    ) -> Edge:
        """Register a connection between two nodes.

        Args:
            src: Source node ID.
            dst: Destination node ID.

        Returns:
            The registered Edge object.
        """
        e = Edge(src=src, dst=dst)
        self._edges.append(e)
        return e

    def cluster(
        self,
        id: str,
        nodes: list[str] | None = None,
        *,
        padding: float = 4.0,
        header_height: float = 3.5,
        parent: str | None = None,
        order: int | None = None,
        pos: Literal["top", "bottom", "left", "right", "center"] | None = None,
    ) -> Cluster:
        """Register a grouping boundary surrounding a subset of nodes.

        Args:
            id: Unique identifier string for the cluster.
            nodes: Optional list of node IDs contained within this cluster.
            padding: Margin padding surrounding the member nodes.
            header_height: Extra top space reserved for a container header title. Defaults to 3.5.
            parent: Optional parent group/cluster ID for nested boundaries.
            order: Optional sequence index among peer containers.
            pos: Optional 2D macro spatial position ("top", "bottom", "left", "right", "center").

        Returns:
            The registered Cluster object.

        Raises:
            ValueError: If a cluster with the same id is already registered.
        """
        if id in self._clusters:
            raise ValueError(f"Cluster '{id}' is already registered in the graph.")

        c = Cluster(
            id=id,
            nodes=list(nodes) if nodes is not None else [],
            padding=padding,
            header_height=header_height,
            parent=parent,
            order=order,
            pos=pos,
        )
        self._clusters[id] = c
        return c

    def group(
        self,
        id: str,
        *,
        nodes: list[str] | None = None,
        padding: float = 4.0,
        header_height: float = 3.5,
        parent: str | None = None,
        order: int | None = None,
        pos: Literal["top", "bottom", "left", "right", "center"] | None = None,
    ) -> Cluster:
        """Register an architectural container / group (e.g. VPC, subnet, zone).

        Args:
            id: Unique identifier string for the container.
            nodes: Optional initial list of member node IDs.
            padding: Margin padding surrounding member elements.
            header_height: Extra top space reserved for a container header title. Defaults to 3.5.
            parent: Optional parent container ID (e.g. Subnet in VPC).
            order: Optional ordering rank among peer containers.
            pos: Optional 2D macro spatial position ("top", "bottom", "left", "right", "center").

        Returns:
            The registered Cluster object.
        """
        return self.cluster(
            id=id,
            nodes=nodes,
            padding=padding,
            header_height=header_height,
            parent=parent,
            order=order,
            pos=pos,
        )

    @abstractmethod
    def get_layout(
        self,
        *,
        width: float | None = None,
        height: float | None = None,
        margin: float = 10.0,
    ) -> GraphLayout:
        """Compute node, edge, and cluster geometries without drawing.

        Args:
            width: Target layout width.
            height: Target layout height.
            margin: Outer margin surrounding the diagram.

        Returns:
            A GraphLayout containing all computed geometries.
        """
