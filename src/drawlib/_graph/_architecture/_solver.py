# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Compound macro/micro architecture graph layout solver."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from drawlib._graph._layered._solver import solve_layered_layout

if TYPE_CHECKING:
    from drawlib._graph._common._models import Cluster, Edge, Node


def _assign_nodes_to_containers(
    nodes: dict[str, Node],
    clusters: dict[str, Cluster],
) -> tuple[dict[str, list[str]], dict[str, str]]:
    """Map containers to their member node IDs and nodes to their leaf container ID."""
    container_nodes: dict[str, list[str]] = {cid: [] for cid in clusters}
    node_to_container: dict[str, str] = {}

    for nid, node in nodes.items():
        target_cid: str | None = None
        if node.subgroup and node.subgroup in clusters:
            target_cid = node.subgroup
        elif node.group and node.group in clusters:
            target_cid = node.group

        if target_cid is not None:
            container_nodes[target_cid].append(nid)
            node_to_container[nid] = target_cid

    # Include nodes explicitly declared in cluster.nodes
    for cid, cluster in clusters.items():
        for nid in cluster.nodes:
            if nid in nodes and nid not in node_to_container:
                container_nodes[cid].append(nid)
                node_to_container[nid] = cid

    # If any nodes remain ungrouped, place in default container
    ungrouped = [nid for nid in nodes if nid not in node_to_container]
    if ungrouped:
        default_cid = "__default_zone__"
        container_nodes[default_cid] = ungrouped
        for nid in ungrouped:
            node_to_container[nid] = default_cid

    return container_nodes, node_to_container


def _order_by_inter_edges(
    cids: list[str],
    node_to_container: dict[str, str],
    edges: list[Edge],
) -> list[str]:
    """Order containers according to inter-container dependency edges."""
    in_degree: dict[str, int] = {cid: 0 for cid in cids}
    adj: dict[str, set[str]] = {cid: set() for cid in cids}

    for edge in edges:
        c_src = node_to_container.get(edge.src)
        c_dst = node_to_container.get(edge.dst)
        if c_src and c_dst and c_src != c_dst and c_src in adj and c_dst in adj:
            if c_dst not in adj[c_src]:
                adj[c_src].add(c_dst)
                in_degree[c_dst] += 1

    queue = [cid for cid in cids if in_degree[cid] == 0]
    ordered: list[str] = []
    while queue:
        curr = queue.pop(0)
        ordered.append(curr)
        for nxt in adj[curr]:
            in_degree[nxt] -= 1
            if in_degree[nxt] == 0:
                queue.append(nxt)

    for cid in cids:
        if cid not in ordered:
            ordered.append(cid)

    return ordered


def _order_containers(
    cids: list[str],
    clusters: dict[str, Cluster],
    node_to_container: dict[str, str],
    edges: list[Edge],
) -> list[str]:
    """Determine flow sequence of peer containers using order attribute and inter-container edges."""
    if len(cids) <= 1:
        return list(cids)

    has_explicit_order = any(clusters[cid].order is not None for cid in cids if cid in clusters)
    if has_explicit_order:

        def _get_order(cid: str) -> int:
            if cid in clusters:
                ord_val = clusters[cid].order
                if ord_val is not None:
                    return ord_val
            return 9999

        return sorted(cids, key=_get_order)

    return _order_by_inter_edges(cids, node_to_container, edges)


def _layout_leaf_nodes(
    member_nids: list[str],
    nodes: dict[str, Node],
    edges: list[Edge],
    direction: Literal["LR", "TB"],
    default_nw: float,
    default_nh: float,
) -> tuple[dict[str, tuple[float, float]], float, float]:
    """Layout nodes within a single leaf container and compute its local bounding size."""
    if not member_nids:
        return {}, 20.0, 20.0

    sub_nodes = {nid: nodes[nid] for nid in member_nids}
    sub_edges = [e for e in edges if e.src in sub_nodes and e.dst in sub_nodes]

    # Use internal layered solver with generous clearance
    internal_dir: Literal["LR", "TB"] = direction
    local_coords, _ = solve_layered_layout(
        nodes=sub_nodes,
        edges=sub_edges,
        direction=internal_dir,
        rank_sep=12.0,
        node_sep=8.0,
        width=100.0,
        height=100.0,
        margin=4.0,
        default_node_width=default_nw,
        default_node_height=default_nh,
    )

    xs = [pt[0] for pt in local_coords.values()]
    ys = [pt[1] for pt in local_coords.values()]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    max_w = max(sub_nodes[nid].width or default_nw for nid in member_nids)
    max_h = max(sub_nodes[nid].height or default_nh for nid in member_nids)

    # Shift local coordinates to center around (0, 0)
    center_x = (min_x + max_x) / 2.0
    center_y = (min_y + max_y) / 2.0
    centered_coords = {
        nid: (round(pt[0] - center_x, 2), round(pt[1] - center_y, 2))
        for nid, pt in local_coords.items()
    }

    content_w = (max_x - min_x) + max_w
    content_h = (max_y - min_y) + max_h

    return centered_coords, content_w, content_h


def _compute_container_boxes(
    ordered_roots: list[str],
    child_containers: dict[str, list[str]],
    container_nodes: dict[str, list[str]],
    nodes: dict[str, Node],
    edges: list[Edge],
    clusters: dict[str, Cluster],
    direction: Literal["LR", "TB"],
    default_nw: float,
    default_nh: float,
) -> tuple[
    dict[str, tuple[dict[str, tuple[float, float]], float, float]],
    dict[str, tuple[float, float]],
]:
    """Compute local layouts and dimensions for all root and child containers."""
    leaf_layouts: dict[str, tuple[dict[str, tuple[float, float]], float, float]] = {}
    root_dims: dict[str, tuple[float, float]] = {}

    for root_id in ordered_roots:
        r_pos = clusters[root_id].pos if root_id in clusters and clusters[root_id].pos else None
        if r_pos in {"top", "bottom"}:
            c_dir: Literal["LR", "TB"] = "TB"
        elif r_pos in {"left", "right"}:
            c_dir = "LR"
        else:
            c_dir = direction

        sub_cids = child_containers.get(root_id, [])
        if not sub_cids:
            # Simple root container without subgroups
            members = container_nodes.get(root_id, [])
            pad = clusters[root_id].padding if root_id in clusters else 4.0
            top_extra = 3.5 if (root_id in clusters and clusters[root_id].label) else 0.0

            coords, cw, ch = _layout_leaf_nodes(members, nodes, edges, c_dir, default_nw, default_nh)
            lbl = clusters[root_id].label if root_id in clusters else None
            lbl_w = len(lbl) * 1.3 if lbl else 0.0
            eff_cw = max(cw, lbl_w)
            leaf_layouts[root_id] = (coords, eff_cw, ch)
            root_dims[root_id] = (eff_cw + 2.0 * pad, ch + 2.0 * pad + top_extra)
        else:
            # Complex root container with subgroups
            pad = clusters[root_id].padding if root_id in clusters else 5.0
            top_extra = 4.0 if (root_id in clusters and clusters[root_id].label) else 0.0
            sub_w_list: list[float] = []
            sub_h_list: list[float] = []

            for sub_id in sub_cids:
                s_members = container_nodes.get(sub_id, [])
                s_pad = clusters[sub_id].padding if sub_id in clusters else 4.0
                s_extra = 3.5 if (sub_id in clusters and clusters[sub_id].label) else 0.0

                s_coords, s_cw, s_ch = _layout_leaf_nodes(
                    s_members, nodes, edges, c_dir, default_nw, default_nh
                )
                s_lbl = clusters[sub_id].label if sub_id in clusters else None
                s_lbl_w = len(s_lbl) * 1.3 if s_lbl else 0.0
                eff_scw = max(s_cw, s_lbl_w)
                leaf_layouts[sub_id] = (s_coords, eff_scw, s_ch)
                sub_w_list.append(eff_scw + 2.0 * s_pad)
                sub_h_list.append(s_ch + 2.0 * s_pad + s_extra)

            # Subgroups layout inside parent container
            if c_dir == "LR":
                total_sw = sum(sub_w_list) + (len(sub_w_list) - 1) * 12.0
                max_sh = max(sub_h_list) if sub_h_list else 20.0
                root_dims[root_id] = (total_sw + 2.0 * pad, max_sh + 2.0 * pad + top_extra)
            else:
                max_sw = max(sub_w_list) if sub_w_list else 20.0
                total_sh = sum(sub_h_list) + (len(sub_h_list) - 1) * 8.0
                root_dims[root_id] = (max_sw + 2.0 * pad, total_sh + 2.0 * pad + top_extra)

    return leaf_layouts, root_dims


def _position_root_containers(
    ordered_roots: list[str],
    root_dims: dict[str, tuple[float, float]],
    direction: Literal["LR", "TB"],
    width: float,
    height: float,
    container_sep: float | None,
) -> dict[str, tuple[float, float]]:
    """Place root containers along direction and center them on canvas."""
    root_centers: dict[str, tuple[float, float]] = {}

    if direction == "LR":
        sum_w = sum(root_dims[r][0] for r in ordered_roots)
        if container_sep is not None:
            sep = container_sep
        elif len(ordered_roots) > 1:
            sep = max(8.0, (width - 24.0 - sum_w) / (len(ordered_roots) - 1))
        else:
            sep = 16.0

        total_w = sum_w + (len(ordered_roots) - 1) * sep
        origin_x = max(12.0, (width - total_w) / 2.0)
        curr_x = origin_x
        cy = height / 2.0

        for r in ordered_roots:
            rw, _ = root_dims[r]
            rcx = round(curr_x + rw / 2.0, 2)
            root_centers[r] = (rcx, cy)
            curr_x += rw + sep
    else:  # "TB"
        sum_h = sum(root_dims[r][1] for r in ordered_roots)
        if container_sep is not None:
            sep = container_sep
        elif len(ordered_roots) > 1:
            sep = max(8.0, (height - 24.0 - sum_h) / (len(ordered_roots) - 1))
        else:
            sep = 16.0

        total_h = sum_h + (len(ordered_roots) - 1) * sep
        top_y = min(height - 12.0, (height + total_h) / 2.0)
        curr_y = top_y
        cx = width / 2.0

        for r in ordered_roots:
            _, rh = root_dims[r]
            rcy = round(curr_y - rh / 2.0, 2)
            root_centers[r] = (cx, rcy)
            curr_y -= rh + sep

    return root_centers


def _group_containers_by_zone(
    ordered_roots: list[str],
    clusters: dict[str, Cluster],
) -> dict[str, list[str]]:
    """Group root containers into 5 compass zones."""
    zone_roots: dict[str, list[str]] = {
        "center": [],
        "top": [],
        "bottom": [],
        "left": [],
        "right": [],
    }
    for r in ordered_roots:
        pos = clusters[r].pos if r in clusters and clusters[r].pos else "center"
        if pos in zone_roots:
            zone_roots[pos].append(r)
        else:
            zone_roots["center"].append(r)
    return zone_roots


def _compute_zone_dimensions(
    zone_roots: dict[str, list[str]],
    root_dims: dict[str, tuple[float, float]],
    direction: Literal["LR", "TB"],
    gap: float,
) -> dict[str, tuple[float, float]]:
    """Compute (width, height) bounding dimensions for each compass zone."""
    dims: dict[str, tuple[float, float]] = {}

    # Center zone
    c_roots = zone_roots["center"]
    if not c_roots:
        dims["center"] = (0.0, 0.0)
    elif direction == "LR":
        w = sum(root_dims[r][0] for r in c_roots) + (len(c_roots) - 1) * gap
        h = max(root_dims[r][1] for r in c_roots)
        dims["center"] = (w, h)
    else:  # "TB"
        w = max(root_dims[r][0] for r in c_roots)
        h = sum(root_dims[r][1] for r in c_roots) + (len(c_roots) - 1) * gap
        dims["center"] = (w, h)

    # Top and bottom zones (horizontal layout)
    for z in ("top", "bottom"):
        roots = zone_roots[z]
        if not roots:
            dims[z] = (0.0, 0.0)
        else:
            w = sum(root_dims[r][0] for r in roots) + (len(roots) - 1) * gap
            h = max(root_dims[r][1] for r in roots)
            dims[z] = (w, h)

    # Left and right zones (vertical layout)
    for z in ("left", "right"):
        roots = zone_roots[z]
        if not roots:
            dims[z] = (0.0, 0.0)
        else:
            w = max(root_dims[r][0] for r in roots)
            h = sum(root_dims[r][1] for r in roots) + (len(roots) - 1) * gap
            dims[z] = (w, h)

    return dims


def _place_zone_members(
    zone: str,
    roots: list[str],
    z_cx: float,
    z_cy: float,
    z_w: float,
    z_h: float,
    root_dims: dict[str, tuple[float, float]],
    direction: Literal["LR", "TB"],
    gap: float,
    root_centers: dict[str, tuple[float, float]],
) -> None:
    """Place member containers within a single compass zone."""
    if not roots:
        return

    is_horizontal = (zone in {"top", "bottom"}) or (zone == "center" and direction == "LR")
    if is_horizontal:
        curr_x = z_cx - z_w / 2.0
        for r in roots:
            rw, _ = root_dims[r]
            rcx = round(curr_x + rw / 2.0, 2)
            root_centers[r] = (rcx, round(z_cy, 2))
            curr_x += rw + gap
    else:
        curr_y = z_cy + z_h / 2.0
        for r in roots:
            _, rh = root_dims[r]
            rcy = round(curr_y - rh / 2.0, 2)
            root_centers[r] = (round(z_cx, 2), rcy)
            curr_y -= rh + gap


def _position_compass_containers(
    ordered_roots: list[str],
    root_dims: dict[str, tuple[float, float]],
    clusters: dict[str, Cluster],
    direction: Literal["LR", "TB"],
    width: float,
    height: float,
    container_sep: float | None,
) -> dict[str, tuple[float, float]]:
    """Position root containers using 2D Compass (center/top/bottom/left/right) layout."""
    sep = container_sep if container_sep is not None else 16.0
    gap = 12.0
    zone_roots = _group_containers_by_zone(ordered_roots, clusters)
    z_dims = _compute_zone_dimensions(zone_roots, root_dims, direction, gap)

    w_left, h_left = z_dims["left"]
    w_right, h_right = z_dims["right"]
    w_top, h_top = z_dims["top"]
    w_bottom, h_bottom = z_dims["bottom"]
    w_center, h_center = z_dims["center"]

    core_w = max(w_center, w_top, w_bottom)
    core_h = max(h_center, h_left, h_right)

    left_pad = (w_left + sep) if w_left > 0 else 0.0
    right_pad = (w_right + sep) if w_right > 0 else 0.0
    top_pad = (h_top + sep) if h_top > 0 else 0.0
    bottom_pad = (h_bottom + sep) if h_bottom > 0 else 0.0

    total_w = left_pad + core_w + right_pad
    total_h = bottom_pad + core_h + top_pad

    min_x = max(10.0, (width - total_w) / 2.0)
    min_y = max(10.0, (height - total_h) / 2.0)

    core_cx = min_x + left_pad + core_w / 2.0
    core_cy = min_y + bottom_pad + core_h / 2.0

    root_centers: dict[str, tuple[float, float]] = {}

    # Center zone
    _place_zone_members(
        "center", zone_roots["center"], core_cx, core_cy, w_center, h_center,
        root_dims, direction, gap, root_centers,
    )

    # Left and right zones
    left_cx = core_cx - core_w / 2.0 - sep - w_left / 2.0
    _place_zone_members(
        "left", zone_roots["left"], left_cx, core_cy, w_left, h_left,
        root_dims, direction, gap, root_centers,
    )

    right_cx = core_cx + core_w / 2.0 + sep + w_right / 2.0
    _place_zone_members(
        "right", zone_roots["right"], right_cx, core_cy, w_right, h_right,
        root_dims, direction, gap, root_centers,
    )

    # Top and bottom zones
    top_cy = core_cy + core_h / 2.0 + sep + h_top / 2.0
    _place_zone_members(
        "top", zone_roots["top"], core_cx, top_cy, w_top, h_top,
        root_dims, direction, gap, root_centers,
    )

    bottom_cy = core_cy - core_h / 2.0 - sep - h_bottom / 2.0
    _place_zone_members(
        "bottom", zone_roots["bottom"], core_cx, bottom_cy, w_bottom, h_bottom,
        root_dims, direction, gap, root_centers,
    )

    return root_centers


def _position_subgroups(
    root_id: str,
    sub_cids: list[str],
    rcx: float,
    rcy: float,
    clusters: dict[str, Cluster],
    node_to_container: dict[str, str],
    edges: list[Edge],
    leaf_layouts: dict[str, tuple[dict[str, tuple[float, float]], float, float]],
    direction: Literal["LR", "TB"],
    node_coords: dict[str, tuple[float, float]],
    cluster_boxes: dict[str, tuple[float, float, float, float]],
) -> None:
    """Position subgroups and their child nodes within a parent root container."""
    ordered_subs = _order_containers(sub_cids, clusters, node_to_container, edges)
    top_extra = 4.0 if (root_id in clusters and clusters[root_id].label) else 0.0

    if direction == "LR":
        sub_widths = [leaf_layouts[s][1] + 2.0 * clusters[s].padding for s in ordered_subs]
        total_sw = sum(sub_widths) + (len(ordered_subs) - 1) * 12.0
        curr_sx = rcx - total_sw / 2.0
        for s in ordered_subs:
            s_coords, s_cw, s_ch = leaf_layouts[s]
            s_pad = clusters[s].padding
            sw = s_cw + 2.0 * s_pad
            sh = s_ch + 2.0 * s_pad
            scx = round(curr_sx + sw / 2.0, 2)
            scy = round(rcy - top_extra / 2.0, 2)
            cluster_boxes[s] = (scx, scy, sw, sh)

            for nid, (lx, ly) in s_coords.items():
                node_coords[nid] = (round(scx + lx, 2), round(scy + ly, 2))
            curr_sx += sw + 12.0
    else:
        sub_heights = [leaf_layouts[s][2] + 2.0 * clusters[s].padding for s in ordered_subs]
        total_sh = sum(sub_heights) + (len(ordered_subs) - 1) * 8.0
        curr_sy = rcy + total_sh / 2.0 - top_extra / 2.0
        for s in ordered_subs:
            s_coords, s_cw, s_ch = leaf_layouts[s]
            s_pad = clusters[s].padding
            sw = s_cw + 2.0 * s_pad
            sh = s_ch + 2.0 * s_pad
            scx = rcx
            scy = round(curr_sy - sh / 2.0, 2)
            cluster_boxes[s] = (scx, scy, sw, sh)

            for nid, (lx, ly) in s_coords.items():
                node_coords[nid] = (round(scx + lx, 2), round(scy + ly, 2))
            curr_sy -= sh + 8.0


def _partition_containers(
    container_nodes: dict[str, list[str]],
    clusters: dict[str, Cluster],
) -> tuple[dict[str, list[str]], list[str]]:
    """Separate container IDs into parent->children hierarchy and root container IDs."""
    child_containers: dict[str, list[str]] = {}
    root_cids: list[str] = []

    for cid in container_nodes:
        parent_id = clusters[cid].parent if cid in clusters else None
        if parent_id and parent_id in clusters:
            child_containers.setdefault(parent_id, []).append(cid)
        else:
            root_cids.append(cid)

    return child_containers, root_cids


def _place_single_container_contents(
    root_id: str,
    rcx: float,
    rcy: float,
    sub_cids: list[str],
    leaf_layouts: dict[str, tuple[dict[str, tuple[float, float]], float, float]],
    clusters: dict[str, Cluster],
    node_to_container: dict[str, str],
    edges: list[Edge],
    direction: Literal["LR", "TB"],
    node_coords: dict[str, tuple[float, float]],
    cluster_boxes: dict[str, tuple[float, float, float, float]],
) -> None:
    """Place contents (leaf nodes or subgroups) within a single root container."""
    if not sub_cids:
        local_coords, _, _ = leaf_layouts[root_id]
        top_extra = 3.5 if (root_id in clusters and clusters[root_id].label) else 0.0
        shift_y = -top_extra / 2.0
        for nid, (lx, ly) in local_coords.items():
            node_coords[nid] = (round(rcx + lx, 2), round(rcy + ly + shift_y, 2))
    else:
        r_pos = clusters[root_id].pos if root_id in clusters and clusters[root_id].pos else None
        if r_pos in {"top", "bottom"}:
            c_dir: Literal["LR", "TB"] = "TB"
        elif r_pos in {"left", "right"}:
            c_dir = "LR"
        else:
            c_dir = direction

        _position_subgroups(
            root_id=root_id,
            sub_cids=sub_cids,
            rcx=rcx,
            rcy=rcy,
            clusters=clusters,
            node_to_container=node_to_container,
            edges=edges,
            leaf_layouts=leaf_layouts,
            direction=c_dir,
            node_coords=node_coords,
            cluster_boxes=cluster_boxes,
        )


def solve_architecture_layout(
    nodes: dict[str, Node],
    edges: list[Edge],
    clusters: dict[str, Cluster],
    direction: Literal["LR", "TB"],
    container_sep: float | None,
    width: float,
    height: float,
    default_node_width: float,
    default_node_height: float,
) -> tuple[
    dict[str, tuple[float, float]],
    dict[str, tuple[float, float, float, float]],
]:
    """Compute compound 2-level macro/micro architecture coordinates.

    Returns:
        tuple containing:
            - node_coords: mapping from node ID to (x, y)
            - cluster_boxes: mapping from cluster ID to (cx, cy, width, height)
    """
    if not nodes:
        return {}, {}

    # If no clusters exist, fall back cleanly to pure layered layout
    if not clusters and not any(n.group or n.subgroup for n in nodes.values()):
        l_coords, _ = solve_layered_layout(
            nodes=nodes,
            edges=edges,
            direction=direction,
            rank_sep=16.0,
            node_sep=8.0,
            width=width,
            height=height,
            margin=10.0,
            default_node_width=default_node_width,
            default_node_height=default_node_height,
        )
        return l_coords, {}

    container_nodes, node_to_container = _assign_nodes_to_containers(nodes, clusters)
    child_containers, root_cids = _partition_containers(container_nodes, clusters)
    ordered_roots = _order_containers(root_cids, clusters, node_to_container, edges)

    # Compute container sizes and internal layouts
    leaf_layouts, root_dims = _compute_container_boxes(
        ordered_roots=ordered_roots,
        child_containers=child_containers,
        container_nodes=container_nodes,
        nodes=nodes,
        edges=edges,
        clusters=clusters,
        direction=direction,
        default_nw=default_node_width,
        default_nh=default_node_height,
    )

    is_compass = any(clusters[r].pos is not None for r in ordered_roots if r in clusters)
    if is_compass:
        root_centers = _position_compass_containers(
            ordered_roots, root_dims, clusters, direction, width, height, container_sep
        )
    else:
        root_centers = _position_root_containers(
            ordered_roots, root_dims, direction, width, height, container_sep
        )

    node_coords: dict[str, tuple[float, float]] = {}
    cluster_boxes: dict[str, tuple[float, float, float, float]] = {}

    for root_id in ordered_roots:
        rcx, rcy = root_centers[root_id]
        rw, rh = root_dims[root_id]
        if root_id in clusters and root_id != "__default_zone__":
            cluster_boxes[root_id] = (rcx, rcy, rw, rh)

        sub_cids = child_containers.get(root_id, [])
        _place_single_container_contents(
            root_id=root_id,
            rcx=rcx,
            rcy=rcy,
            sub_cids=sub_cids,
            leaf_layouts=leaf_layouts,
            clusters=clusters,
            node_to_container=node_to_container,
            edges=edges,
            direction=direction,
            node_coords=node_coords,
            cluster_boxes=cluster_boxes,
        )

    return node_coords, cluster_boxes
