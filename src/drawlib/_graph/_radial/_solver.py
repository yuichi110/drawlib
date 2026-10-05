# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Concentric ring and radial layout solver implementation."""

from __future__ import annotations

import collections
import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from drawlib._graph._common._models import Edge, Node


def _assign_rings(
    nodes: dict[str, Node],
    edges: list[Edge],
    hub_id: str,
) -> dict[str, int]:
    """Assign concentric ring numbers to all nodes.

    Hub node is assigned ring 0. Explicit node.ring attributes are respected;
    otherwise rings are determined by shortest path distance (BFS) from the hub.

    Args:
        nodes: Registered nodes dictionary.
        edges: Registered edges list.
        hub_id: ID of the central hub node.

    Returns:
        Mapping from node ID to ring index (0 for hub, 1+ for spokes).
    """
    # Build undirected adjacency
    adj: dict[str, list[str]] = {nid: [] for nid in nodes}
    for e in edges:
        if e.src in adj and e.dst in adj:
            adj[e.src].append(e.dst)
            adj[e.dst].append(e.src)

    rings: dict[str, int] = {hub_id: 0}

    # BFS from hub
    queue: collections.deque[str] = collections.deque([hub_id])
    while queue:
        curr = queue.popleft()
        curr_ring = rings[curr]
        for nbr in adj[curr]:
            if nbr not in rings:
                rings[nbr] = curr_ring + 1
                queue.append(nbr)

    # Assign explicit rings or fallback for disconnected nodes
    for nid, node in nodes.items():
        if node.ring is not None:
            rings[nid] = node.ring
        elif nid not in rings:
            rings[nid] = 1

    return rings


def _compute_angles_for_ring(
    nids: list[str],
    parent_angles: dict[str, float],
    edges: list[Edge],
    start_angle: float,
    angle_range: float,
) -> dict[str, float]:
    """Compute angular positions for nodes belonging to a single ring."""
    if not nids:
        return {}

    m = len(nids)
    if m == 1:
        # Single node: inherit parent angle if available, else start_angle
        ref = parent_angles.get(nids[0], start_angle)
        return {nids[0]: ref}

    # Sort nodes by their parent's angle if available to minimize edge crossings
    def get_sort_key(nid: str) -> float:
        return parent_angles.get(nid, start_angle)

    sorted_nids = sorted(nids, key=get_sort_key)

    angles: dict[str, float] = {}
    if angle_range >= 360.0:
        step_a = 360.0 / m
        for idx, nid in enumerate(sorted_nids):
            angles[nid] = (start_angle + idx * step_a) % 360.0
    else:
        step_a = angle_range / (m - 1) if m > 1 else 0.0
        for idx, nid in enumerate(sorted_nids):
            angles[nid] = start_angle + idx * step_a

    return angles


def solve_radial_layout(  # noqa: C901
    nodes: dict[str, Node],
    edges: list[Edge],
    hub_id: str | None,
    center: tuple[float, float],
    radius_step: float | None,
    start_angle: float,
    angle_range: float,
    avail_w: float,
    avail_h: float,
    default_node_width: float,
    default_node_height: float,
) -> tuple[dict[str, tuple[float, float]], dict[str, int], dict[int, float]]:
    """Compute Cartesian coordinates, ring assignments, and ring radii for radial layout.

    Args:
        nodes: Registered nodes dictionary.
        edges: Registered edges list.
        hub_id: Optional explicit hub ID. If None, auto-detected from connectivity.
        center: Coordinates (cx, cy) of the radial origin.
        radius_step: Distance between successive rings. If None, auto-scaled to canvas.
        start_angle: Starting orientation in degrees.
        angle_range: Sweep span in degrees (360.0 for full circle).
        avail_w: Available canvas width.
        avail_h: Available canvas height.
        default_node_width: Node width used for margin clearance.
        default_node_height: Node height used for margin clearance.

    Returns:
        tuple containing:
            - node_coords: mapping from node ID to (x, y)
            - node_rings: mapping from node ID to ring number
            - ring_radii: mapping from ring number to circle radius
    """
    if not nodes:
        return {}, {}, {}

    # 1. Determine central hub
    resolved_hub: str
    if hub_id and hub_id in nodes:
        resolved_hub = hub_id
    else:
        # Auto-detect highest degree node
        degrees: dict[str, int] = {nid: 0 for nid in nodes}
        for e in edges:
            if e.src in degrees:
                degrees[e.src] += 1
            if e.dst in degrees:
                degrees[e.dst] += 1
        resolved_hub = max(degrees.keys(), key=lambda k: degrees[k]) if degrees else next(iter(nodes))

    # 2. Assign ring numbers
    node_rings = _assign_rings(nodes, edges, resolved_hub)

    # Group by ring
    ring_groups: dict[int, list[str]] = collections.defaultdict(list)
    for nid, r in node_rings.items():
        ring_groups[r].append(nid)

    max_ring = max(ring_groups.keys()) if ring_groups else 0

    # 3. Determine radii
    cx, cy = center
    max_nw = max(n.width or default_node_width for n in nodes.values())
    max_nh = max(n.height or default_node_height for n in nodes.values())
    node_clearance = max(max_nw, max_nh) / 2.0

    max_avail_r = min(cx, cy, avail_w - cx, avail_h - cy) - node_clearance
    max_avail_r = max(max_avail_r, 15.0)

    ring_radii: dict[int, float] = {0: 0.0}
    if radius_step is not None:
        for r in ring_groups:
            ring_radii[r] = r * radius_step
    elif max_ring > 0:
        # Calculate minimum required distance for each step to guarantee non-overlapping nodes
        hub_node = nodes[resolved_hub]
        hub_dim = max(hub_node.width or default_node_width, hub_node.height or default_node_height)

        min_steps: dict[int, float] = {}
        prev_dim = hub_dim
        for r in range(1, max_ring + 1):
            r_nids = ring_groups.get(r, [])
            if r_nids:
                curr_dim = max(
                    max(nodes[nid].width or default_node_width, nodes[nid].height or default_node_height)
                    for nid in r_nids
                )
            else:
                curr_dim = max(default_node_width, default_node_height)
            min_steps[r] = (prev_dim + curr_dim) / 2.0 + 8.0
            prev_dim = curr_dim

        total_min_r = sum(min_steps.values())
        if max_avail_r > total_min_r:
            scale = max_avail_r / total_min_r
            accum_r = 0.0
            for r in range(1, max_ring + 1):
                accum_r += min_steps[r] * scale
                ring_radii[r] = round(accum_r, 2)
        else:
            accum_r = 0.0
            for r in range(1, max_ring + 1):
                accum_r += min_steps[r]
                ring_radii[r] = round(accum_r, 2)

    # 4. Compute angles
    node_angles: dict[str, float] = {resolved_hub: 0.0}

    # Adjacency for tracking parent angles
    nbr_map: dict[str, list[str]] = collections.defaultdict(list)
    for e in edges:
        nbr_map[e.dst].append(e.src)
        nbr_map[e.src].append(e.dst)

    for r in range(1, max_ring + 1):
        r_nids = ring_groups.get(r, [])
        if not r_nids:
            continue

        # Find reference parent angle for each node from previous ring
        parent_angles: dict[str, float] = {}
        for nid in r_nids:
            p_angles = [node_angles[p] for p in nbr_map[nid] if p in node_angles and node_rings[p] < r]
            if p_angles:
                parent_angles[nid] = sum(p_angles) / len(p_angles)
            else:
                parent_angles[nid] = start_angle

        ring_angles = _compute_angles_for_ring(
            r_nids,
            parent_angles=parent_angles,
            edges=edges,
            start_angle=start_angle,
            angle_range=angle_range,
        )
        node_angles.update(ring_angles)

    # 5. Convert polar to Cartesian (x, y)
    node_coords: dict[str, tuple[float, float]] = {}
    for nid, r in node_rings.items():
        if r == 0:
            node_coords[nid] = (round(cx, 2), round(cy, 2))
        else:
            radius = ring_radii[r]
            theta_deg = node_angles.get(nid, 0.0)
            rad = math.radians(theta_deg)
            nx = round(cx + radius * math.cos(rad), 2)
            ny = round(cy + radius * math.sin(rad), 2)
            node_coords[nid] = (nx, ny)

    return node_coords, node_rings, ring_radii
