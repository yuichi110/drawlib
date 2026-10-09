# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Edge routing utilities for graph layouts."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from drawlib._graph._common._models import NodeLayout


def route_orthogonal_edge(
    src: NodeLayout,
    dst: NodeLayout,
    direction: Literal["TB", "BT", "LR", "RL"] = "TB",
) -> tuple[tuple[float, float], list[tuple[float, float]], tuple[float, float]]:
    """Route an edge between two nodes with right-angle (Manhattan) waypoints.

    Args:
        src: Source node layout.
        dst: Destination node layout.
        direction: Flow direction of the layout.

    Returns:
        tuple containing (src_port, waypoints, dst_port).
    """
    if direction in {"TB", "BT"}:
        if direction == "TB":
            src_port = (round(src.x, 2), round(src.bottom, 2))
            dst_port = (round(dst.x, 2), round(dst.top, 2))
        else:  # "BT"
            src_port = (round(src.x, 2), round(src.top, 2))
            dst_port = (round(dst.x, 2), round(dst.bottom, 2))

        if abs(src.x - dst.x) > 0.5:
            mid_y = round((src_port[1] + dst_port[1]) / 2.0, 2)
            waypoints = [(src_port[0], mid_y), (dst_port[0], mid_y)]
        else:
            waypoints = []
    else:  # "LR", "RL"
        if direction == "LR":
            src_port = (round(src.right, 2), round(src.y, 2))
            dst_port = (round(dst.left, 2), round(dst.y, 2))
        else:  # "RL"
            src_port = (round(src.left, 2), round(src.y, 2))
            dst_port = (round(dst.right, 2), round(dst.y, 2))

        if abs(src.y - dst.y) > 0.5:
            mid_x = round((src_port[0] + dst_port[0]) / 2.0, 2)
            waypoints = [(mid_x, src_port[1]), (mid_x, dst_port[1])]
        else:
            waypoints = []

    return src_port, waypoints, dst_port


def route_straight_edge(
    src: NodeLayout,
    dst: NodeLayout,
    direction: Literal["TB", "BT", "LR", "RL"] = "TB",
) -> tuple[tuple[float, float], list[tuple[float, float]], tuple[float, float]]:
    """Route a direct straight edge connecting corresponding node boundary ports.

    Args:
        src: Source node layout.
        dst: Destination node layout.
        direction: Flow direction of the layout.

    Returns:
        tuple containing (src_port, waypoints=[], dst_port).
    """
    if direction == "TB":
        src_port = (round(src.x, 2), round(src.bottom, 2))
        dst_port = (round(dst.x, 2), round(dst.top, 2))
    elif direction == "BT":
        src_port = (round(src.x, 2), round(src.top, 2))
        dst_port = (round(dst.x, 2), round(dst.bottom, 2))
    elif direction == "LR":
        src_port = (round(src.right, 2), round(src.y, 2))
        dst_port = (round(dst.left, 2), round(dst.y, 2))
    else:  # "RL"
        src_port = (round(src.left, 2), round(src.y, 2))
        dst_port = (round(dst.right, 2), round(dst.y, 2))
    return src_port, [], dst_port


def compute_boundary_intersection(
    node: NodeLayout,
    target_xy: tuple[float, float],
) -> tuple[float, float]:
    """Compute the intersection point between a node's perimeter and a line toward target_xy.

    Accurately calculates intersections for circle and rectangle geometries.

    Args:
        node: NodeLayout of the shape.
        target_xy: Target coordinate (e.g. another node center).

    Returns:
        Exact boundary point (x, y) on the node's perimeter.
    """
    dx = target_xy[0] - node.x
    dy = target_xy[1] - node.y
    dist = (dx**2 + dy**2) ** 0.5
    if dist < 1e-6:
        return (node.x, node.y)

    u_x = dx / dist
    u_y = dy / dist

    if node.shape == "circle":
        r = node.width / 2.0
        return (round(node.x + r * u_x, 2), round(node.y + r * u_y, 2))

    # Rectangle / Rounded Rectangle (Ray-Box Intersection)
    half_w = node.width / 2.0
    half_h = node.height / 2.0

    t_x = half_w / abs(u_x) if abs(u_x) > 1e-6 else float("inf")
    t_y = half_h / abs(u_y) if abs(u_y) > 1e-6 else float("inf")
    t = min(t_x, t_y)

    return (round(node.x + t * u_x, 2), round(node.y + t * u_y, 2))


def route_radial_edge(
    src: NodeLayout,
    dst: NodeLayout,
) -> tuple[tuple[float, float], list[tuple[float, float]], tuple[float, float]]:
    """Route a direct radial edge between two nodes connecting their exact boundaries.

    Args:
        src: Source node layout.
        dst: Destination node layout.

    Returns:
        tuple containing (src_port, waypoints=[], dst_port).
    """
    src_port = compute_boundary_intersection(src, (dst.x, dst.y))
    dst_port = compute_boundary_intersection(dst, (src.x, src.y))
    return src_port, [], dst_port


def route_grid_edge(
    src: NodeLayout,
    dst: NodeLayout,
    routing_style: Literal["smart", "orthogonal", "straight"] = "smart",
) -> tuple[tuple[float, float], list[tuple[float, float]], tuple[float, float]]:
    """Route an edge between two nodes in a grid layout.

    - "smart": Straight line for adjacent horizontal/vertical nodes; right-angle
      corridor routing for diagonal or multi-cell distance pairs.
    - "orthogonal": Manhattan right-angle routing between row/column corridors.
    - "straight": Direct line connecting exact boundary intersections.

    Args:
        src: Source node layout.
        dst: Destination node layout.
        routing_style: Path routing strategy ("smart", "orthogonal", "straight").

    Returns:
        tuple containing (src_port, waypoints, dst_port).
    """
    if routing_style == "straight":
        return route_radial_edge(src, dst)

    dx = dst.x - src.x
    dy = dst.y - src.y

    # Same row (horizontal)
    if abs(dy) < 0.5:
        if dx > 0:
            src_port = (round(src.right, 2), round(src.y, 2))
            dst_port = (round(dst.left, 2), round(dst.y, 2))
        else:
            src_port = (round(src.left, 2), round(src.y, 2))
            dst_port = (round(dst.right, 2), round(dst.y, 2))
        return src_port, [], dst_port

    # Same column (vertical)
    if abs(dx) < 0.5:
        if dy > 0:  # src is below dst (canvas Y increases upwards)
            src_port = (round(src.x, 2), round(src.top, 2))
            dst_port = (round(dst.x, 2), round(dst.bottom, 2))
        else:  # src is above dst
            src_port = (round(src.x, 2), round(src.bottom, 2))
            dst_port = (round(dst.x, 2), round(dst.top, 2))
        return src_port, [], dst_port

    # Diagonal / Multi-row/col
    if dy < 0:  # src is above dst
        src_port = (round(src.x, 2), round(src.bottom, 2))
        dst_port = (round(dst.x, 2), round(dst.top, 2))
    else:  # src is below dst
        src_port = (round(src.x, 2), round(src.top, 2))
        dst_port = (round(dst.x, 2), round(dst.bottom, 2))

    mid_y = round((src_port[1] + dst_port[1]) / 2.0, 2)
    waypoints = [(src_port[0], mid_y), (dst_port[0], mid_y)]
    return src_port, waypoints, dst_port
