# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Sugiyama-style layered hierarchical graph layout solver."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from drawlib._graph._common._models import Edge, Node


def _build_dag(
    nodes: dict[str, Node],
    edges: list[Edge],
) -> tuple[dict[str, list[str]], set[tuple[str, str]]]:
    """Break cycles using DFS and return a directed acyclic graph (DAG).

    Returns:
        tuple containing:
            - dag_adj: mapping from node ID to list of downstream neighbor node IDs
            - reversed_edges: set of (src, dst) pairs that were reversed to break cycles
    """
    raw_adj: dict[str, list[str]] = {nid: [] for nid in nodes}
    for edge in edges:
        if edge.src in nodes and edge.dst in nodes:
            raw_adj[edge.src].append(edge.dst)

    state: dict[str, int] = {nid: 0 for nid in nodes}  # 0: unvisited, 1: visiting, 2: visited
    dag_adj: dict[str, list[str]] = {nid: [] for nid in nodes}
    reversed_edges: set[tuple[str, str]] = set()

    def dfs(u: str) -> None:
        state[u] = 1
        for v in raw_adj[u]:
            if state[v] == 1:
                # Cycle detected: reverse edge v -> u in DAG
                reversed_edges.add((u, v))
                dag_adj[v].append(u)
            else:
                dag_adj[u].append(v)
                if state[v] == 0:
                    dfs(v)
        state[u] = 2

    for nid in nodes:
        if state[nid] == 0:
            dfs(nid)

    return dag_adj, reversed_edges


def _get_topological_order(
    nodes: dict[str, Node],
    dag_adj: dict[str, list[str]],
) -> list[str]:
    """Compute topological ordering of nodes in the DAG."""
    in_degree: dict[str, int] = {nid: 0 for nid in nodes}
    for targets in dag_adj.values():
        for v in targets:
            in_degree[v] += 1

    queue = [nid for nid in nodes if in_degree[nid] == 0]
    topo_order: list[str] = []
    while queue:
        u = queue.pop(0)
        topo_order.append(u)
        for v in dag_adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    # Add any remaining nodes
    for nid in nodes:
        if nid not in topo_order:
            topo_order.append(nid)

    return topo_order


def _compute_longest_path_layers(
    nodes: dict[str, Node],
    dag_adj: dict[str, list[str]],
) -> dict[str, int]:
    """Assign an integer layer (rank) to each node using longest-path leveling."""
    topo_order = _get_topological_order(nodes, dag_adj)

    layers: dict[str, int] = {}
    for nid, node in nodes.items():
        layers[nid] = node.layer if node.layer is not None else 0

    for u in topo_order:
        u_layer = layers[u]
        for v in dag_adj[u]:
            req_layer = u_layer + 1
            v_explicit = nodes[v].layer
            if v_explicit is not None:
                layers[v] = max(layers[v], v_explicit)
            else:
                layers[v] = max(layers[v], req_layer)

    min_level = min(layers.values()) if layers else 0
    return {nid: lvl - min_level for nid, lvl in layers.items()}


def _barycenter_pass_forward(
    layers_map: dict[int, list[str]],
    sorted_levels: list[int],
    rev_adj: dict[str, list[str]],
) -> None:
    """Sort nodes in each layer based on average position of predecessors."""
    for idx in range(1, len(sorted_levels)):
        prev_layer = layers_map[sorted_levels[idx - 1]]
        pos_map = {nid: i for i, nid in enumerate(prev_layer)}
        curr_layer = layers_map[sorted_levels[idx]]
        curr_pos = {nid: i for i, nid in enumerate(curr_layer)}

        def score(v: str) -> float:
            preds = [pos_map[u] for u in rev_adj[v] if u in pos_map]
            return sum(preds) / len(preds) if preds else float(curr_pos[v])

        curr_layer.sort(key=score)


def _barycenter_pass_backward(
    layers_map: dict[int, list[str]],
    sorted_levels: list[int],
    dag_adj: dict[str, list[str]],
) -> None:
    """Sort nodes in each layer based on average position of successors."""
    for idx in range(len(sorted_levels) - 2, -1, -1):
        next_layer = layers_map[sorted_levels[idx + 1]]
        pos_map = {nid: i for i, nid in enumerate(next_layer)}
        curr_layer = layers_map[sorted_levels[idx]]
        curr_pos = {nid: i for i, nid in enumerate(curr_layer)}

        def score(u: str) -> float:
            succs = [pos_map[v] for v in dag_adj[u] if v in pos_map]
            return sum(succs) / len(succs) if succs else float(curr_pos[u])

        curr_layer.sort(key=score)


def _reduce_crossings(
    nodes: dict[str, Node],
    layers: dict[str, int],
    dag_adj: dict[str, list[str]],
) -> list[list[str]]:
    """Organize nodes into layers and apply barycenter crossing reduction."""
    layers_map: dict[int, list[str]] = {}
    for nid, lvl in layers.items():
        layers_map.setdefault(lvl, []).append(nid)

    sorted_levels = sorted(layers_map.keys())

    rev_adj: dict[str, list[str]] = {nid: [] for nid in nodes}
    for u, targets in dag_adj.items():
        for v in targets:
            rev_adj[v].append(u)

    # 2 rounds of forward and backward sweeps
    for _ in range(2):
        _barycenter_pass_forward(layers_map, sorted_levels, rev_adj)
        _barycenter_pass_backward(layers_map, sorted_levels, dag_adj)

    return [layers_map[lvl] for lvl in sorted_levels]


def _calculate_lr_coords(
    ordered_layers: list[list[str]],
    width: float,
    height: float,
    avail_w: float,
    avail_h: float,
    max_nw: float,
    max_nh: float,
    rank_sep: float | None,
    node_sep: float | None,
) -> dict[str, tuple[float, float]]:
    """Compute (x, y) coordinates for Left-to-Right layout."""
    num_layers = len(ordered_layers)
    max_nodes = max(len(layer) for layer in ordered_layers) if ordered_layers else 1

    # Step X: layer separation
    min_step_x = max_nw + 16.0
    if rank_sep is not None:
        step_x = max_nw + rank_sep
    elif num_layers > 1:
        ideal_step_x = (avail_w - max_nw) / (num_layers - 1)
        step_x = max(min_step_x, ideal_step_x)
    else:
        step_x = 0.0

    # Step Y: sibling separation within layer
    min_step_y = max_nh + 4.0
    if node_sep is not None:
        step_y = max_nh + node_sep
    elif max_nodes > 1:
        ideal_step_y = (avail_h - max_nh) / (max_nodes - 1)
        step_y = max(min_step_y, ideal_step_y)
    else:
        step_y = 0.0

    total_w = (num_layers - 1) * step_x + max_nw if num_layers > 1 else max_nw
    origin_x = (width - total_w) / 2.0 + max_nw / 2.0

    coords: dict[str, tuple[float, float]] = {}
    for l_idx, layer in enumerate(ordered_layers):
        x = round(origin_x + l_idx * step_x, 2)
        k = len(layer)
        layer_h = (k - 1) * step_y if k > 1 else 0.0
        top_y = height / 2.0 + layer_h / 2.0
        for i, nid in enumerate(layer):
            y = round(top_y - i * step_y, 2)
            coords[nid] = (x, y)

    return coords


def _calculate_tb_coords(
    ordered_layers: list[list[str]],
    width: float,
    height: float,
    avail_w: float,
    avail_h: float,
    max_nw: float,
    max_nh: float,
    rank_sep: float | None,
    node_sep: float | None,
) -> dict[str, tuple[float, float]]:
    """Compute (x, y) coordinates for Top-to-Bottom layout."""
    num_layers = len(ordered_layers)
    max_nodes = max(len(layer) for layer in ordered_layers) if ordered_layers else 1

    # Step Y: layer separation
    min_step_y = max_nh + 16.0
    if rank_sep is not None:
        step_y = max_nh + rank_sep
    elif num_layers > 1:
        ideal_step_y = (avail_h - max_nh) / (num_layers - 1)
        step_y = max(min_step_y, ideal_step_y)
    else:
        step_y = 0.0

    # Step X: sibling separation within layer
    min_step_x = max_nw + 4.0
    if node_sep is not None:
        step_x = max_nw + node_sep
    elif max_nodes > 1:
        ideal_step_x = (avail_w - max_nw) / (max_nodes - 1)
        step_x = max(min_step_x, ideal_step_x)
    else:
        step_x = 0.0

    total_h = (num_layers - 1) * step_y + max_nh if num_layers > 1 else max_nh
    top_y = (height + total_h) / 2.0 - max_nh / 2.0

    coords: dict[str, tuple[float, float]] = {}
    for l_idx, layer in enumerate(ordered_layers):
        y = round(top_y - l_idx * step_y, 2)
        k = len(layer)
        layer_w = (k - 1) * step_x if k > 1 else 0.0
        left_x = width / 2.0 - layer_w / 2.0
        for i, nid in enumerate(layer):
            x = round(left_x + i * step_x, 2)
            coords[nid] = (x, y)

    return coords


def solve_layered_layout(
    nodes: dict[str, Node],
    edges: list[Edge],
    direction: Literal["LR", "TB"],
    rank_sep: float | None,
    node_sep: float | None,
    width: float,
    height: float,
    margin: float,
    default_node_width: float,
    default_node_height: float,
) -> tuple[dict[str, tuple[float, float]], dict[str, int]]:
    """Compute tidy hierarchical layered coordinates for all nodes.

    Args:
        nodes: Registered nodes dictionary.
        edges: Registered edges list.
        direction: Flow direction ("LR" or "TB").
        rank_sep: Separation between layers. If None, auto-scales.
        node_sep: Separation between nodes within the same layer. If None, auto-scales.
        width: Target canvas width.
        height: Target canvas height.
        margin: Outer canvas margin.
        default_node_width: Fallback width for nodes.
        default_node_height: Fallback height for nodes.

    Returns:
        tuple containing:
            - node_coords: mapping from node ID to (x, y)
            - node_layers: mapping from node ID to layer index (0, 1, 2...)
    """
    if not nodes:
        return {}, {}

    dag_adj, _ = _build_dag(nodes, edges)
    node_layers = _compute_longest_path_layers(nodes, dag_adj)
    ordered_layers = _reduce_crossings(nodes, node_layers, dag_adj)

    max_nw = max(n.width or default_node_width for n in nodes.values())
    max_nh = max(n.height or default_node_height for n in nodes.values())
    avail_w = max(width - 2.0 * margin, max_nw)
    avail_h = max(height - 2.0 * margin, max_nh)

    if direction == "LR":
        coords = _calculate_lr_coords(
            ordered_layers=ordered_layers,
            width=width,
            height=height,
            avail_w=avail_w,
            avail_h=avail_h,
            max_nw=max_nw,
            max_nh=max_nh,
            rank_sep=rank_sep,
            node_sep=node_sep,
        )
    else:
        coords = _calculate_tb_coords(
            ordered_layers=ordered_layers,
            width=width,
            height=height,
            avail_w=avail_w,
            avail_h=avail_h,
            max_nw=max_nw,
            max_nh=max_nh,
            rank_sep=rank_sep,
            node_sep=node_sep,
        )

    return coords, node_layers
