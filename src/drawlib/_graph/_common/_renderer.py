# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Canvas renderer for computed GraphLayout geometry."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from drawlib._core.l4_canvas import transform
from drawlib.lines import line, lines
from drawlib.shapes import circle, rectangle
from drawlib.text import text

if TYPE_CHECKING:
    from drawlib._graph._common._models import (
        ClusterLayout,
        EdgeLayout,
        GraphLayout,
        NodeLayout,
    )


def _draw_clusters(clusters: dict[str, ClusterLayout]) -> None:
    """Draw cluster boundaries and header labels in background layer."""
    for cluster in clusters.values():
        if not cluster.show:
            continue
        if cluster.shape == "circle":
            circle(
                (cluster.cx, cluster.cy),
                radius=cluster.width / 2.0,
                style=cluster.style,
            )
            if cluster.label:
                tx = cluster.cx
                ty = round(cluster.top - 2.0, 2)
                text((tx, ty), text=cluster.label, style=cluster.text_style)
        else:
            rectangle(
                (cluster.cx, cluster.cy),
                width=cluster.width,
                height=cluster.height,
                style=cluster.style,
            )
            if cluster.label:
                tx = round(cluster.left + 2.5, 2)
                ty = round(cluster.top - 2.0, 2)
                text((tx, ty), text=cluster.label, style=cluster.text_style)


def _draw_edges(edges: list[EdgeLayout], nodes: dict[str, NodeLayout]) -> None:
    """Draw connector lines and edge labels."""
    for edge in edges:
        if not edge.show:
            continue
        if (edge.src in nodes and not nodes[edge.src].show) or (edge.dst in nodes and not nodes[edge.dst].show):
            continue

        arrow: Literal["", "->", "<-", "<->"]
        if edge.arrow_head in {"", "-"}:
            arrow = ""
        else:
            arrow = edge.arrow_head

        pts = edge.points
        if len(pts) == 2:
            line(
                pts[0],
                pts[1],
                arrow_head=arrow,
                style=edge.style,
            )
        elif len(pts) > 2:
            lines(
                pts,
                arrow_head=arrow,
                style=edge.style,
            )

        if edge.label:
            mid_idx = len(pts) // 2
            if len(pts) % 2 == 0:
                p1 = pts[mid_idx - 1]
                p2 = pts[mid_idx]
                lx = round((p1[0] + p2[0]) / 2.0, 2)
                ly = round((p1[1] + p2[1]) / 2.0 + 2.0, 2)
            else:
                lx = round(pts[mid_idx][0], 2)
                ly = round(pts[mid_idx][1] + 2.0, 2)
            text((lx, ly), text=edge.label, style=edge.text_style)


def _draw_nodes(nodes: dict[str, NodeLayout]) -> None:
    """Draw nodes in foreground layer."""
    for node in nodes.values():
        if not node.show:
            continue
        n_kwargs: dict[str, Any] = {}
        if node.text_style is not None:
            n_kwargs["text_style"] = node.text_style

        if node.shape == "circle":
            circle(
                node.xy,
                radius=node.width / 2.0,
                style=node.style,
                text=node.label,
                **n_kwargs,
            )
        elif node.shape == "rounded_rectangle":
            rectangle(
                node.xy,
                width=node.width,
                height=node.height,
                r=2.0,
                style=node.style,
                text=node.label,
                **n_kwargs,
            )
        else:
            rectangle(
                node.xy,
                width=node.width,
                height=node.height,
                style=node.style,
                text=node.label,
                **n_kwargs,
            )


def render_layout(
    layout: GraphLayout,
    *,
    xy: tuple[float, float] = (0.0, 0.0),
    scale: float = 1.0,
) -> None:
    """Render a computed GraphLayout onto the active Drawlib canvas.

    Draws elements in strictly managed Z-order layers:
    1. Clusters / Grouping containers (Background)
    2. Connections and Edge paths
    3. Edge annotation labels
    4. Nodes and Node labels (Foreground)

    Args:
        layout: Complete geometrical graph layout object.
        xy: Placement offset coordinate (x, y) for the layout origin.
        scale: Proportional scale factor anchored at xy.
    """
    with transform(origin=(0.0, 0.0), scale=scale, translate=xy):
        _draw_clusters(layout.clusters)
        _draw_edges(layout.edges, layout.nodes)
        _draw_nodes(layout.nodes)
