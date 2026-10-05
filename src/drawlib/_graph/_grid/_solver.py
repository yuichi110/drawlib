# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Matrix grid layout solver implementation."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from drawlib._graph._common._models import Node


def _assign_row_major(
    unpinned: list[str],
    cols: int,
    occupied: set[tuple[int, int]],
    slot_map: dict[str, tuple[int, int]],
) -> None:
    """Assign remaining nodes in row-major order."""
    r, c = 0, 0
    for nid in unpinned:
        while (r, c) in occupied:
            c += 1
            if c >= cols:
                c = 0
                r += 1
        slot = (r, c)
        slot_map[nid] = slot
        occupied.add(slot)
        c += 1
        if c >= cols:
            c = 0
            r += 1


def _assign_column_major(
    unpinned: list[str],
    cols: int,
    rows: int | None,
    occupied: set[tuple[int, int]],
    slot_map: dict[str, tuple[int, int]],
) -> None:
    """Assign remaining nodes in column-major order."""
    calc_rows = rows if rows is not None else max(1, math.ceil((len(occupied) + len(unpinned)) / cols))
    r, c = 0, 0
    for nid in unpinned:
        while (r, c) in occupied:
            r += 1
            if r >= calc_rows:
                r = 0
                c += 1
        slot = (r, c)
        slot_map[nid] = slot
        occupied.add(slot)
        r += 1
        if r >= calc_rows:
            r = 0
            c += 1


def _assign_slots(
    nodes: dict[str, Node],
    columns: int,
    rows: int | None,
    order: Literal["row-major", "column-major"],
) -> dict[str, tuple[int, int]]:
    """Assign (row, col) matrix slots to all nodes.

    Respects explicit node.row and node.col attributes. Remaining nodes fill
    unoccupied slots in row-major or column-major order.
    """
    slot_map: dict[str, tuple[int, int]] = {}
    occupied: set[tuple[int, int]] = set()

    # 1. Place explicitly pinned nodes
    unpinned: list[str] = []
    for nid, node in nodes.items():
        if node.row is not None and node.col is not None:
            slot = (node.row, node.col)
            slot_map[nid] = slot
            occupied.add(slot)
        else:
            unpinned.append(nid)

    # 2. Assign unpinned nodes
    cols = max(1, columns)
    if order == "row-major":
        _assign_row_major(unpinned, cols, occupied, slot_map)
    else:
        _assign_column_major(unpinned, cols, rows, occupied, slot_map)

    return slot_map


def solve_grid_layout(
    nodes: dict[str, Node],
    columns: int,
    rows: int | None,
    order: Literal["row-major", "column-major"],
    col_sep: float | None,
    row_sep: float | None,
    width: float,
    height: float,
    margin: float,
    default_node_width: float,
    default_node_height: float,
) -> tuple[dict[str, tuple[float, float]], dict[str, tuple[int, int]]]:
    """Calculate matrix grid coordinates for all nodes.

    Args:
        nodes: Registered nodes dictionary.
        columns: Number of grid columns.
        rows: Optional fixed number of rows (used in column-major order).
        order: Flow ordering ("row-major" or "column-major").
        col_sep: Horizontal gap between columns. If None, auto-scales.
        row_sep: Vertical gap between rows. If None, auto-scales.
        width: Canvas width.
        height: Canvas height.
        margin: Outer margin surrounding the grid.
        default_node_width: Fallback width for nodes.
        default_node_height: Fallback height for nodes.

    Returns:
        tuple containing:
            - node_coords: mapping from node ID to (cx, cy)
            - slot_map: mapping from node ID to (row, col)
    """
    if not nodes:
        return {}, {}

    slot_map = _assign_slots(nodes, columns=columns, rows=rows, order=order)

    # Determine grid matrix dimensions
    all_rows = [s[0] for s in slot_map.values()]
    all_cols = [s[1] for s in slot_map.values()]
    num_rows = max(all_rows) + 1 if all_rows else 1
    num_cols = max(all_cols) + 1 if all_cols else 1

    max_nw = max(n.width or default_node_width for n in nodes.values())
    max_nh = max(n.height or default_node_height for n in nodes.values())

    avail_w = max(width - 2.0 * margin, max_nw)
    avail_h = max(height - 2.0 * margin, max_nh)

    # Calculate column step (step_x)
    min_step_x = max_nw + 4.0
    if col_sep is not None:
        step_x = max_nw + col_sep
    elif num_cols > 1:
        ideal_step_x = (avail_w - max_nw) / (num_cols - 1)
        step_x = max(min_step_x, ideal_step_x)
        if step_x * (num_cols - 1) + max_nw > avail_w:
            step_x = max(min_step_x, (avail_w - max_nw) / (num_cols - 1))
    else:
        step_x = 0.0

    # Calculate row step (step_y)
    min_step_y = max_nh + 4.0
    if row_sep is not None:
        step_y = max_nh + row_sep
    elif num_rows > 1:
        ideal_step_y = (avail_h - max_nh) / (num_rows - 1)
        step_y = max(min_step_y, ideal_step_y)
        if step_y * (num_rows - 1) + max_nh > avail_h:
            step_y = max(min_step_y, (avail_h - max_nh) / (num_rows - 1))
    else:
        step_y = 0.0

    # Total grid dimensions
    total_grid_w = (num_cols - 1) * step_x + max_nw if num_cols > 1 else max_nw
    total_grid_h = (num_rows - 1) * step_y + max_nh if num_rows > 1 else max_nh

    # Center grid within canvas
    origin_x = (width - total_grid_w) / 2.0 + max_nw / 2.0
    top_y = (height + total_grid_h) / 2.0 - max_nh / 2.0

    node_coords: dict[str, tuple[float, float]] = {}
    for nid, (r, c) in slot_map.items():
        cx = round(origin_x + c * step_x, 2)
        cy = round(top_y - r * step_y, 2)
        node_coords[nid] = (cx, cy)

    return node_coords, slot_map
