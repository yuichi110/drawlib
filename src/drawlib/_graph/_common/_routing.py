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
