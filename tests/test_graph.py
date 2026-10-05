# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Tests for declarative graph solvers in drawlib.graph."""

from __future__ import annotations

import pytest

from drawlib.canvas import canvas, clear
from drawlib.graph import (
    BaseGraph,
    Cluster,
    ClusterLayout,
    Edge,
    EdgeLayout,
    GraphLayout,
    Node,
    NodeLayout,
    TreeGraph,
)
from drawlib.styles import Styles


class TestTreeGraph:
    """Test suite for TreeGraph layout solver."""

    def setup_method(self) -> None:
        """Reset canvas before each test."""
        clear()

    def test_exports_and_types(self) -> None:
        """Verify public classes and inheritance."""
        assert issubclass(TreeGraph, BaseGraph)
        assert Node is not None
        assert Edge is not None
        assert Cluster is not None
        assert NodeLayout is not None
        assert EdgeLayout is not None
        assert ClusterLayout is not None
        assert GraphLayout is not None

    def test_basic_tb_layout(self) -> None:
        """Verify standard top-to-bottom tree layout."""
        g = TreeGraph(direction="TB")
        g.node("root", "Root Node")
        g.child("root", "c1", "Child 1")
        g.child("root", "c2", "Child 2")

        layout = g.calc(width=100.0, height=100.0, margin=10.0)

        assert len(layout.nodes) == 3
        assert len(layout.edges) == 2

        root = layout.nodes["root"]
        c1 = layout.nodes["c1"]
        c2 = layout.nodes["c2"]

        # In TB, root is above children (higher Y)
        assert root.y > c1.y
        assert c1.y == c2.y

        # c1 is to the left of c2
        assert c1.x < c2.x
        assert c1.right < c2.left

        # Root is centered between children
        assert abs(root.x - (c1.x + c2.x) / 2.0) < 0.1

    def test_basic_lr_layout(self) -> None:
        """Verify standard left-to-right tree layout."""
        g = TreeGraph(direction="LR")
        g.node("root", "Root Node")
        g.child("root", "c1", "Child 1")
        g.child("root", "c2", "Child 2")

        layout = g.calc(width=100.0, height=100.0, margin=10.0)

        root = layout.nodes["root"]
        c1 = layout.nodes["c1"]
        c2 = layout.nodes["c2"]

        # In LR, root is to the left of children (smaller X)
        assert root.x < c1.x
        assert c1.x == c2.x

        # Vertical ordering
        assert c1.y != c2.y

        # Root is centered vertically between children
        assert abs(root.y - (c1.y + c2.y) / 2.0) < 0.1

    def test_asymmetrical_tree_no_overlap(self) -> None:
        """Verify that subtrees in an asymmetrical hierarchy never overlap."""
        g = TreeGraph(direction="TB")
        g.node("root")
        g.child("root", "c1")
        g.child("root", "c2")
        g.child("root", "c3")

        g.child("c1", "c1_1")
        g.child("c1", "c1_2")

        g.child("c2", "c2_1")

        g.child("c3", "c3_1")
        g.child("c3", "c3_2")
        g.child("c3", "c3_3")
        g.child("c3_1", "c3_1_1")

        layout = g.calc(width=160.0, height=100.0, margin=10.0)

        # Check that no two nodes overlap in bounding box
        node_list = list(layout.nodes.values())
        for i in range(len(node_list)):
            for j in range(i + 1, len(node_list)):
                n1, n2 = node_list[i], node_list[j]
                # Check horizontal or vertical separation
                separated = (
                    n1.right <= n2.left
                    or n2.right <= n1.left
                    or n1.top <= n2.bottom
                    or n2.top <= n1.bottom
                )
                assert separated, f"Nodes '{n1.id}' and '{n2.id}' overlap!"

    def test_multi_root_forest(self) -> None:
        """Verify layout of multiple disconnected trees (forest)."""
        g = TreeGraph(direction="TB")
        g.node("root1")
        g.child("root1", "r1_c1")

        g.node("root2")
        g.child("root2", "r2_c1")

        layout = g.calc(width=120.0, height=80.0, margin=10.0)
        assert len(layout.nodes) == 4

        # Verify separation between the two root components
        r1 = layout.nodes["root1"]
        r2 = layout.nodes["root2"]
        assert r1.right < r2.left or r2.right < r1.left

    def test_clusters(self) -> None:
        """Verify cluster bounding box encloses all constituent nodes."""
        g = TreeGraph()
        g.node("root")
        g.child("root", "c1")
        g.child("root", "c2")

        g.cluster("my_cluster", ["c1", "c2"], label="Children Group", padding=3.0)
        layout = g.calc(width=100.0, height=80.0)

        assert "my_cluster" in layout.clusters
        cluster = layout.clusters["my_cluster"]

        c1 = layout.nodes["c1"]
        c2 = layout.nodes["c2"]

        c_left = cluster.cx - cluster.width / 2.0
        c_right = cluster.cx + cluster.width / 2.0
        c_bottom = cluster.cy - cluster.height / 2.0
        c_top = cluster.cy + cluster.height / 2.0

        assert c_left <= min(c1.left, c2.left)
        assert c_right >= max(c1.right, c2.right)
        assert c_bottom <= min(c1.bottom, c2.bottom)
        assert c_top >= max(c1.top, c2.top)

    def test_layout_offset(self) -> None:
        """Verify manual offset fine-tuning on GraphLayout."""
        g = TreeGraph()
        g.node("root")
        g.child("root", "c1")

        layout = g.calc(width=100.0, height=100.0)
        initial_x = layout.nodes["c1"].x
        initial_port_x = layout.edges[0].dst_port[0]

        layout.offset("c1", dx=5.0, dy=-2.0)

        assert layout.nodes["c1"].x == initial_x + 5.0
        assert layout.edges[0].dst_port[0] == initial_port_x + 5.0

    def test_validation_errors(self) -> None:
        """Verify validation errors for invalid trees (cycles, multiple parents, duplicate nodes)."""
        g = TreeGraph()
        g.node("n1")
        with pytest.raises(ValueError, match="already registered"):
            g.node("n1")

        # Duplicate cluster ID
        g.cluster("cl1", ["n1"])
        with pytest.raises(ValueError, match="already registered"):
            g.cluster("cl1", ["n1"])

        # Multiple parents
        g2 = TreeGraph()
        g2.edge("p1", "child")
        g2.edge("p2", "child")
        with pytest.raises(ValueError, match="multiple parents"):
            g2.calc()

        # Cycle detection
        g3 = TreeGraph()
        g3.edge("a", "b")
        g3.edge("b", "c")
        g3.edge("c", "a")
        with pytest.raises(ValueError, match="Cycle detected"):
            g3.calc()

        # Invalid explicit root
        g4 = TreeGraph(root="missing")
        g4.node("a")
        with pytest.raises(ValueError, match="Specified root 'missing' was not registered"):
            g4.calc()

    def test_draw_and_code_export(self) -> None:
        """Verify draw() and export_code() generate valid output without errors."""
        g = TreeGraph(
            direction="TB",
            default_node_style=Styles.PrimaryFlat,
            default_edge_style=Styles.DarkBold,
        )
        g.node("root", "Root")
        g.child("root", "leaf1", "Leaf 1", style=Styles.SecondaryFlat)
        g.child("root", "leaf2", "Leaf 2", style=Styles.AccentFlat)
        g.cluster("leaves", ["leaf1", "leaf2"], label="Cluster")

        # Test draw() execution
        layout = g.draw(width=120.0, height=70.0)
        assert len(layout.nodes) == 3

        # Test export_code()
        code = g.export_code(width=120.0, height=70.0)
        assert "setup(width=120.0, height=70.0)" in code
        assert "root_xy" in code
        assert "leaf1_xy" in code
        assert "leaf2_xy" in code
        assert "rectangle(" in code
        assert "save()" in code

        # Verify that generated code can be executed safely
        local_scope: dict[str, object] = {}
        exec(code, {}, local_scope)  # noqa: S102
