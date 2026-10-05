# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Buchheim tidy tree layout algorithm implementation.

Based on Christoph Buchheim, Michael Jünger, and Sebastian Leipert (2002):
'Improving Walker's Algorithm to Run in Linear Time'.
Guarantees O(V) runtime, strict symmetry, and overlap-free positioning.
"""

from __future__ import annotations


class _DrawTreeNode:
    """Internal tree node representation for the Buchheim layout algorithm."""

    def __init__(
        self,
        node_id: str,
        parent: _DrawTreeNode | None = None,
        depth: int = 0,
        number: int = 1,
    ) -> None:
        self.id = node_id
        self.x: float = -1.0
        self.y: float = float(depth)
        self.children: list[_DrawTreeNode] = []
        self.parent: _DrawTreeNode | None = parent
        self.thread: _DrawTreeNode | None = None
        self.mod: float = 0.0
        self.ancestor: _DrawTreeNode = self
        self.change: float = 0.0
        self.shift: float = 0.0
        self.number: int = number
        self._lmost_sibling: _DrawTreeNode | None = None

    def left(self) -> _DrawTreeNode | None:
        """Leftmost child or threaded thread link."""
        return self.thread or (self.children[0] if self.children else None)

    def right(self) -> _DrawTreeNode | None:
        """Rightmost child or threaded thread link."""
        return self.thread or (self.children[-1] if self.children else None)

    def lbrother(self) -> _DrawTreeNode | None:
        """Left sibling in the parent's children list."""
        if self.parent:
            n = None
            for node in self.parent.children:
                if node is self:
                    return n
                n = node
        return None

    @property
    def lmost_sibling(self) -> _DrawTreeNode | None:
        """Leftmost sibling among children of the parent."""
        if not self._lmost_sibling and self.parent and self is not self.parent.children[0]:
            self._lmost_sibling = self.parent.children[0]
        return self._lmost_sibling


def _buchheim_first_walk(v: _DrawTreeNode, distance: float = 1.0) -> _DrawTreeNode:
    """First post-order walk of the Buchheim tree algorithm."""
    if not v.children:
        if v.lmost_sibling:
            lb = v.lbrother()
            v.x = (lb.x + distance) if lb else 0.0
        else:
            v.x = 0.0
    else:
        default_ancestor = v.children[0]
        for w in v.children:
            _buchheim_first_walk(w, distance)
            default_ancestor = _buchheim_apportion(w, default_ancestor, distance)
        _buchheim_execute_shifts(v)
        midpoint = (v.children[0].x + v.children[-1].x) / 2.0
        w = v.lbrother()
        if w:
            v.x = w.x + distance
            v.mod = v.x - midpoint
        else:
            v.x = midpoint
    return v


def _buchheim_apportion(  # noqa: C901
    v: _DrawTreeNode, default_ancestor: _DrawTreeNode, distance: float
) -> _DrawTreeNode:
    """Apportion shifts between subtrees."""
    w = v.lbrother()
    if w is not None:
        vir = vor = v
        vil = w
        vol = v.lmost_sibling
        sir = sor = v.mod
        sil = vil.mod
        sol = vol.mod if vol else 0.0

        while vil is not None and vir is not None:
            vil_next = vil.right()
            vir_next = vir.left()
            if vil_next is None or vir_next is None:
                break
            vil = vil_next
            vir = vir_next
            if vol is not None:
                vol = vol.left()
            if vor is not None:
                vor = vor.right()
                if vor is not None:
                    vor.ancestor = v

            shift = (vil.x + sil) - (vir.x + sir) + distance
            if shift > 0:
                anc = _buchheim_ancestor(vil, v, default_ancestor)
                _buchheim_move_subtree(anc, v, shift)
                sir += shift
                sor += shift
            sil += vil.mod
            sir += vir.mod
            if vol is not None:
                sol += vol.mod
            if vor is not None:
                sor += vor.mod

        if vil is not None and vor is not None and vil.right() is not None and not vor.right():
            vor.thread = vil.right()
            vor.mod += sil - sor
        else:
            if vir is not None and vol is not None and vir.left() is not None and not vol.left():
                vol.thread = vir.left()
                vol.mod += sir - sol
            default_ancestor = v
    return default_ancestor


def _buchheim_move_subtree(wl: _DrawTreeNode, wr: _DrawTreeNode, shift: float) -> None:
    subtrees = wr.number - wl.number
    if subtrees > 0:
        wr.change -= shift / subtrees
        wr.shift += shift
        wl.change += shift / subtrees
    wr.x += shift
    wr.mod += shift


def _buchheim_execute_shifts(v: _DrawTreeNode) -> None:
    shift = 0.0
    change = 0.0
    for w in reversed(v.children):
        w.x += shift
        w.mod += shift
        change += w.change
        shift += w.shift + change


def _buchheim_ancestor(
    vil: _DrawTreeNode, v: _DrawTreeNode, default_ancestor: _DrawTreeNode
) -> _DrawTreeNode:
    if v.parent and vil.ancestor in v.parent.children:
        return vil.ancestor
    return default_ancestor


def _buchheim_second_walk(
    v: _DrawTreeNode, m: float = 0.0, depth: int = 0, min_val: float | None = None
) -> float:
    v.x += m
    v.y = float(depth)
    if min_val is None or v.x < min_val:
        min_val = v.x
    for w in v.children:
        min_val = _buchheim_second_walk(w, m + v.mod, depth + 1, min_val)
    return min_val


def _buchheim_third_walk(v: _DrawTreeNode, offset: float) -> None:
    v.x += offset
    for c in v.children:
        _buchheim_third_walk(c, offset)


def solve_buchheim_tree(
    roots: list[str],
    children_map: dict[str, list[str]],
) -> dict[str, tuple[float, int]]:
    """Compute logical (x, depth) tree coordinates using the Buchheim algorithm.

    Handles single trees as well as multiple-root forests (using a virtual super-root).

    Args:
        roots: List of root node IDs.
        children_map: Adjacency dictionary mapping parent IDs to ordered lists of child IDs.

    Returns:
        Dictionary mapping node IDs to (logical_x, logical_depth).
    """
    def build_draw_node(nid: str, parent: _DrawTreeNode | None, depth: int, number: int) -> _DrawTreeNode:
        dnode = _DrawTreeNode(nid, parent=parent, depth=depth, number=number)
        dnode.children = [
            build_draw_node(cid, dnode, depth + 1, idx + 1)
            for idx, cid in enumerate(children_map.get(nid, []))
        ]
        return dnode

    is_forest = len(roots) > 1
    if is_forest:
        super_root = _DrawTreeNode("__super_root__", None, 0, 1)
        super_root.children = [
            build_draw_node(rid, super_root, 1, idx + 1) for idx, rid in enumerate(roots)
        ]
        layout_root = super_root
    else:
        layout_root = build_draw_node(roots[0], None, 0, 1)

    dt = _buchheim_first_walk(layout_root, distance=1.0)
    min_x = _buchheim_second_walk(dt, m=0.0, depth=0)
    if min_x < 0:
        _buchheim_third_walk(dt, -min_x)

    logical_coords: dict[str, tuple[float, int]] = {}

    def collect_coords(node: _DrawTreeNode) -> None:
        if node.id != "__super_root__":
            depth = int(node.y) - (1 if is_forest else 0)
            logical_coords[node.id] = (node.x, depth)
        for c in node.children:
            collect_coords(c)

    collect_coords(layout_root)
    return logical_coords
