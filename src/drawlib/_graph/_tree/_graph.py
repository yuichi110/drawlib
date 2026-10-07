# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""TreeGraph class for declarative tree hierarchy visualization."""

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
from drawlib._graph._common._routing import route_orthogonal_edge, route_straight_edge
from drawlib._graph._tree._solver import solve_buchheim_tree
from drawlib.fonts import Font
from drawlib.styles import Style, Styles


class TreeGraph(BaseGraph):
    """Declarative tree graph layout solver using the Reingold-Tilford / Buchheim algorithm.

    Arranges nodes into a tidy, symmetrical hierarchy where parents are centered
    above (or beside) their children, with guaranteed overlap-free subtrees.
    """

    def __init__(
        self,
        *,
        root: str | None = None,
        direction: Literal["TB", "LR"] = "TB",
        level_sep: float | None = None,
        sibling_sep: float | None = None,
        default_node_style: Style | None = None,
        default_node_text_style: Style | None = None,
        default_edge_style: Style | None = None,
        default_edge_text_style: Style | None = None,
        default_node_width: float = 22.0,
        default_node_height: float = 12.0,
        edge_routing: Literal["orthogonal", "straight"] = "orthogonal",
    ) -> None:
        """Initialize TreeGraph solver.

        Args:
            root: Optional explicit root node ID. If omitted, automatically detects
                nodes with in-degree 0.
            direction: Layout flow direction ("TB" for Top-to-Bottom, "LR" for Left-to-Right).
            level_sep: Fixed distance between generational levels. If None, auto-scales to canvas.
            sibling_sep: Fixed minimum distance between siblings. If None, auto-scales to canvas.
            default_node_style: Default style for nodes.
            default_node_text_style: Default text style for node labels.
            default_edge_style: Default style for edges.
            default_edge_text_style: Default text style for edge labels.
            default_node_width: Default width for nodes.
            default_node_height: Default height for nodes.
            edge_routing: Edge path style ("orthogonal" for Manhattan right-angles, or "straight").
        """
        super().__init__(
            default_node_style=default_node_style,
            default_node_text_style=default_node_text_style,
            default_edge_style=default_edge_style,
            default_edge_text_style=default_edge_text_style,
            default_node_width=default_node_width,
            default_node_height=default_node_height,
        )
        self.root: str | None = root
        self.direction: Literal["TB", "LR"] = direction
        self.level_sep: float | None = level_sep
        self.sibling_sep: float | None = sibling_sep
        self.edge_routing: Literal["orthogonal", "straight"] = edge_routing

    def child(
        self,
        parent: str,
        child_id: str,
        label: str | None = None,
        *,
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
        """Convenience method to register a child node and connect it from its parent.

        Args:
            parent: Parent node ID. Will be auto-registered if not present.
            child_id: Child node ID.
            label: Text label displayed on child node. Defaults to child_id if None.
            style: Shape styling for child node.
            text_style: Text styling for child node label.
            shape: Shape geometry of child node.
            icon: Optional icon name or path.
            width: Custom width for child node.
            height: Custom height for child node.
            edge_label: Annotation text on connecting edge.
            edge_style: Style of connecting edge.
            arrow_head: Arrowhead decoration ("->", "<-", "<->", "-").
            show: Whether to render the child node.
            edge_show: Whether to render the connecting edge.

        Returns:
            The registered child Node object.
        """
        if parent not in self._nodes:
            self.node(parent)

        n = self.node(
            id=child_id,
            label=label,
            style=style,
            text_style=text_style,
            shape=shape,
            icon=icon,
            width=width,
            height=height,
            show=show,
        )
        self.edge(
            src=parent,
            dst=child_id,
            label=edge_label,
            style=edge_style,
            arrow_head=arrow_head,
            show=edge_show,
        )
        return n

    def _build_tree_hierarchy(self) -> tuple[list[str], dict[str, list[str]]]:  # noqa: C901
        """Validate tree structure and build adjacency list.

        Returns:
            tuple of (root_ids, children_map).

        Raises:
            ValueError: If cycles or multiple parents are detected.
        """
        for edge in self._edges:
            if edge.src not in self._nodes:
                self.node(edge.src)
            if edge.dst not in self._nodes:
                self.node(edge.dst)

        parent_map: dict[str, str] = {}
        children_map: dict[str, list[str]] = {nid: [] for nid in self._nodes}

        for edge in self._edges:
            if edge.dst in parent_map:
                raise ValueError(
                    f"Node '{edge.dst}' has multiple parents ('{parent_map[edge.dst]}' and '{edge.src}'). "
                    "TreeGraph requires a strict tree structure (nodes must have at most one parent). "
                    "For general directed graphs with multiple parents or DAGs, use ArchitectureGraph."
                )
            parent_map[edge.dst] = edge.src
            children_map[edge.src].append(edge.dst)

        visited: dict[str, int] = {}  # 0: unvisited, 1: visiting, 2: visited

        def dfs(u: str) -> None:
            visited[u] = 1
            for v in children_map[u]:
                if visited.get(v, 0) == 1:
                    raise ValueError(
                        f"Cycle detected in TreeGraph at node '{v}'. Trees must be strictly acyclic. "
                        "For general cyclic graphs, use ArchitectureGraph."
                    )
                if visited.get(v, 0) == 0:
                    dfs(v)
            visited[u] = 2

        for nid in self._nodes:
            if visited.get(nid, 0) == 0:
                dfs(nid)

        if self.root:
            if self.root not in self._nodes:
                raise ValueError(f"Specified root '{self.root}' was not registered in the graph.")
            roots = [self.root]
        else:
            roots = [nid for nid in self._nodes if nid not in parent_map]
            if not roots and self._nodes:
                roots = [next(iter(self._nodes))]

        return roots, children_map

    def calc(  # noqa: C901
        self,
        *,
        width: float | None = None,
        height: float | None = None,
        margin: float = 10.0,
    ) -> GraphLayout:
        """Compute tidy tree coordinates without rendering.

        Args:
            width: Target canvas width. Defaults to canvas._width or 120.0.
            height: Target canvas height. Defaults to canvas._height or 60.0.
            margin: Outer margin surrounding the tree diagram.

        Returns:
            A GraphLayout containing all computed node, edge, and cluster geometries.
        """
        w = width if width is not None else float(getattr(canvas, "_width", 120.0))
        h = height if height is not None else float(getattr(canvas, "_height", 60.0))

        if not self._nodes and not self._edges:
            return GraphLayout(width=w, height=h)

        roots, children_map = self._build_tree_hierarchy()
        logical_coords = solve_buchheim_tree(roots, children_map)

        all_x = [coords[0] for coords in logical_coords.values()]
        all_d = [coords[1] for coords in logical_coords.values()]
        min_lx, max_lx = min(all_x), max(all_x)
        max_d = max(all_d) if all_d else 0

        max_nw = max(n.width or self.default_node_width for n in self._nodes.values())
        max_nh = max(n.height or self.default_node_height for n in self._nodes.values())

        avail_w = max(w - 2.0 * margin, max_nw)
        avail_h = max(h - 2.0 * margin, max_nh)

        nodes_layout: dict[str, NodeLayout] = {}

        if self.direction == "TB":
            min_step_x = max_nw + 4.0
            span_x = max_lx - min_lx
            if self.sibling_sep is not None:
                step_x = max_nw + self.sibling_sep
            elif span_x > 0:
                ideal_step = (avail_w - max_nw) / span_x
                step_x = max(min_step_x, ideal_step)
                if step_x * span_x + max_nw > avail_w:
                    step_x = max(min_step_x, (avail_w - max_nw) / span_x)
            else:
                step_x = max_nw + 10.0

            min_step_y = max_nh + 6.0
            if self.level_sep is not None:
                step_y = max_nh + self.level_sep
            elif max_d > 0:
                ideal_step_y = (avail_h - max_nh) / max_d
                step_y = max(min_step_y, ideal_step_y)
                if step_y * max_d + max_nh > avail_h:
                    step_y = max(min_step_y, (avail_h - max_nh) / max_d)
            else:
                step_y = max_nh + 15.0

            tree_width = span_x * step_x + max_nw
            tree_height = max_d * step_y + max_nh

            origin_x = (w - tree_width) / 2.0 + max_nw / 2.0
            top_y = (h + tree_height) / 2.0 - max_nh / 2.0

            for nid, node in self._nodes.items():
                lx, ld = logical_coords[nid]
                nw = node.width or self.default_node_width
                nh = node.height or self.default_node_height
                cx = origin_x + (lx - min_lx) * step_x
                cy = top_y - ld * step_y
                nodes_layout[nid] = NodeLayout(
                    id=nid,
                    xy=(round(cx, 2), round(cy, 2)),
                    width=nw,
                    height=nh,
                    style=node.style or self.default_node_style,
                    text_style=node.text_style or self.default_node_text_style,
                    label=node.label or nid,
                    shape=node.shape,
                    icon=node.icon,
                    show=node.show,
                )

        else:  # "LR"
            min_step_x = max_nw + 6.0
            span_y = max_lx - min_lx
            if self.level_sep is not None:
                step_x = max_nw + self.level_sep
            elif max_d > 0:
                ideal_step_x = (avail_w - max_nw) / max_d
                step_x = max(min_step_x, ideal_step_x)
                if step_x * max_d + max_nw > avail_w:
                    step_x = max(min_step_x, (avail_w - max_nw) / max_d)
            else:
                step_x = max_nw + 15.0

            min_step_y = max_nh + 4.0
            if self.sibling_sep is not None:
                step_y = max_nh + self.sibling_sep
            elif span_y > 0:
                ideal_step_y = (avail_h - max_nh) / span_y
                step_y = max(min_step_y, ideal_step_y)
                if step_y * span_y + max_nh > avail_h:
                    step_y = max(min_step_y, (avail_h - max_nh) / span_y)
            else:
                step_y = max_nh + 10.0

            tree_width = max_d * step_x + max_nw
            tree_height = span_y * step_y + max_nh

            origin_x = (w - tree_width) / 2.0 + max_nw / 2.0
            top_y = (h + tree_height) / 2.0 - max_nh / 2.0

            for nid, node in self._nodes.items():
                lx, ld = logical_coords[nid]
                nw = node.width or self.default_node_width
                nh = node.height or self.default_node_height
                cx = origin_x + ld * step_x
                cy = top_y - (lx - min_lx) * step_y
                nodes_layout[nid] = NodeLayout(
                    id=nid,
                    xy=(round(cx, 2), round(cy, 2)),
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
        edges_layout: list[EdgeLayout] = []
        for edge in self._edges:
            src_nl = nodes_layout[edge.src]
            dst_nl = nodes_layout[edge.dst]

            if self.edge_routing == "orthogonal":
                src_port, waypoints, dst_port = route_orthogonal_edge(src_nl, dst_nl, direction=self.direction)
            else:
                src_port, waypoints, dst_port = route_straight_edge(src_nl, dst_nl, direction=self.direction)

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
                cx = round((min_x + max_x) / 2.0, 2)
                cy = round((min_y + max_y) / 2.0, 2)
                c_text_style = (
                    default_cluster_text_style.patch(cluster.text_style)
                    if cluster.text_style is not None
                    else default_cluster_text_style
                )
                clusters_layout[cid] = ClusterLayout(
                    id=cid,
                    label=cluster.label,
                    bbox=(cx, cy, cw, ch),
                    style=cluster.style or Styles.MutedDashed,
                    text_style=c_text_style,
                    show=cluster.show,
                )

        return GraphLayout(
            nodes=nodes_layout,
            edges=edges_layout,
            clusters=clusters_layout,
            width=w,
            height=h,
        )
