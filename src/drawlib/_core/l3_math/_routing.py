# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Orthogonal path routing calculations for diagrams and geometry."""

from __future__ import annotations

from typing import Literal

Side = Literal["left", "right", "top", "bottom"]
RoutingType = Literal["direct", "orthogonal"]


def compute_orthogonal_path(
    start_pt: tuple[float, float],
    end_pt: tuple[float, float],
    start_side: Side = "right",
    end_side: Side = "left",
    routing: RoutingType = "orthogonal",
    offset: float = 3.0,
) -> list[tuple[float, float]]:
    """Compute 2D polyline waypoints connecting start and end anchors.

    Calculates right-angled orthogonal or direct line waypoints between two anchor points
    given their boundary exit/entry sides.

    Args:
        start_pt: Starting anchor coordinate (x, y).
        end_pt: Ending anchor coordinate (x, y).
        start_side: Side of the source node where path exits.
            Defaults to "right".
        end_side: Side of the target node where path enters.
            Defaults to "left".
        routing: Routing style. "direct" returns a straight
            2-point line, while "orthogonal" generates right-angled segments. Defaults to "orthogonal".
        offset: Clearance distance to extend outwards when routing around nodes. Defaults to 3.0.

    Returns:
        list[tuple[float, float]]: Ordered list of 2D waypoints defining the path polyline.
    """
    if routing == "direct" or abs(start_pt[0] - end_pt[0]) < 1e-4 or abs(start_pt[1] - end_pt[1]) < 1e-4:
        return [start_pt, end_pt]

    sx, sy = start_pt
    ex, ey = end_pt

    path: list[tuple[float, float]]
    # Horizontal exit to Horizontal entry (e.g. right -> left)
    if start_side in {"left", "right"} and end_side in {"left", "right"}:
        if (start_side == "right" and ex > sx) or (start_side == "left" and ex < sx):
            mid_x = (sx + ex) / 2.0
            path = [start_pt, (mid_x, sy), (mid_x, ey), end_pt]
        else:
            offset_s = offset if start_side == "right" else -offset
            offset_e = offset if end_side == "right" else -offset
            mid_y = (sy + ey) / 2.0
            path = [
                start_pt,
                (sx + offset_s, sy),
                (sx + offset_s, mid_y),
                (ex + offset_e, mid_y),
                (ex + offset_e, ey),
                end_pt,
            ]

    # Vertical exit to Vertical entry (e.g. bottom -> top)
    elif start_side in {"top", "bottom"} and end_side in {"top", "bottom"}:
        if (start_side == "top" and ey > sy) or (start_side == "bottom" and ey < sy):
            mid_y = (sy + ey) / 2.0
            path = [start_pt, (sx, mid_y), (ex, mid_y), end_pt]
        else:
            offset_s = offset if start_side == "top" else -offset
            offset_e = offset if end_side == "top" else -offset
            mid_x = (sx + ex) / 2.0
            path = [
                start_pt,
                (sx, sy + offset_s),
                (mid_x, sy + offset_s),
                (mid_x, ey + offset_e),
                (ex, ey + offset_e),
                end_pt,
            ]

    # Horizontal exit to Vertical entry
    elif start_side in {"left", "right"} and end_side in {"top", "bottom"}:
        path = [start_pt, (ex, sy), end_pt]

    # Vertical exit to Horizontal entry
    elif start_side in {"top", "bottom"} and end_side in {"left", "right"}:
        path = [start_pt, (sx, ey), end_pt]

    else:
        path = [start_pt, (ex, sy), end_pt]

    return path
