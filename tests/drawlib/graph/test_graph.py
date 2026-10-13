# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Tests for declarative graph layout solvers in drawlib.graph."""

from __future__ import annotations

import pytest

from drawlib.canvas import canvas, clear
from drawlib.diagrams.architecture import ArchitectureDiagram, NodeGroup
from drawlib.diagrams.architecture import Edge as ArchEdge
from drawlib.diagrams.architecture import Node as ArchNode
from drawlib.diagrams.flow import FlowDiagram, Process
from drawlib.graph import (
    ArchitectureGraph,
    BaseGraph,
    Cluster,
    ClusterLayout,
    Edge,
    EdgeLayout,
    GraphLayout,
    GridGraph,
    LayerGraph,
    Node,
    NodeLayout,
    RadialGraph,
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
        g.node("root")
        g.child("root", "c1")
        g.child("root", "c2")

        layout = g.get_layout(width=100.0, height=100.0, margin=10.0)

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
        g.node("root")
        g.child("root", "c1")
        g.child("root", "c2")

        layout = g.get_layout(width=100.0, height=100.0, margin=10.0)

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

        layout = g.get_layout(width=160.0, height=100.0, margin=10.0)

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

        layout = g.get_layout(width=120.0, height=80.0, margin=10.0)
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

        g.cluster("my_cluster", ["c1", "c2"], padding=3.0)
        layout = g.get_layout(width=100.0, height=80.0)

        assert "my_cluster" in layout.clusters
        cluster = layout.clusters["my_cluster"]

        c1 = layout.nodes["c1"]
        c2 = layout.nodes["c2"]

        assert cluster.left <= min(c1.left, c2.left)
        assert cluster.right >= max(c1.right, c2.right)
        assert cluster.bottom <= min(c1.bottom, c2.bottom)
        assert cluster.top >= max(c1.top, c2.top)

    def test_layout_offset(self) -> None:
        """Verify manual offset fine-tuning on GraphLayout."""
        g = TreeGraph()
        g.node("root")
        g.child("root", "c1")

        layout = g.get_layout(width=100.0, height=100.0)
        initial_x = layout.nodes["c1"].x
        initial_port_x = layout.edges[0].dst_port[0]

        returned = layout.offset("c1", dx=5.0, dy=-2.0)
        assert returned is layout

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
            g2.get_layout()

        # Cycle detection
        g3 = TreeGraph()
        g3.edge("a", "b")
        g3.edge("b", "c")
        g3.edge("c", "a")
        with pytest.raises(ValueError, match="Cycle detected"):
            g3.get_layout()

        # Invalid explicit root
        g4 = TreeGraph(root="missing")
        g4.node("a")
        with pytest.raises(ValueError, match="Specified root 'missing' was not registered"):
            g4.get_layout()


class TestRadialGraph:
    """Test suite for RadialGraph layout solver."""

    def setup_method(self) -> None:
        """Reset canvas before each test."""
        clear()

    def test_radial_subclass(self) -> None:
        """Verify RadialGraph is a subclass of BaseGraph."""
        assert issubclass(RadialGraph, BaseGraph)

    def test_basic_hub_spokes(self) -> None:
        """Verify central hub placement and equidistant spoke distribution."""
        g = RadialGraph(hub="broker")
        g.node("broker", width=16.0, height=16.0)
        g.spoke("broker", "s1")
        g.spoke("broker", "s2")
        g.spoke("broker", "s3")
        g.spoke("broker", "s4")

        layout = g.get_layout(width=100.0, height=100.0, margin=10.0)

        assert len(layout.nodes) == 5
        assert len(layout.edges) == 4

        # Hub at exact center
        hub = layout.nodes["broker"]
        assert hub.xy == (50.0, 50.0)

        # All 4 spokes on same radial distance from hub
        distances: list[float] = []
        for sid in ["s1", "s2", "s3", "s4"]:
            spoke = layout.nodes[sid]
            dx = spoke.x - hub.x
            dy = spoke.y - hub.y
            dist = round((dx**2 + dy**2) ** 0.5, 1)
            distances.append(dist)

        assert len(set(distances)) == 1
        assert distances[0] > 15.0

    def test_concentric_multiring(self) -> None:
        """Verify concentric multi-ring assignments and increasing radii."""
        g = RadialGraph(hub="core")
        g.node("core")
        # Ring 1
        g.spoke("core", "gw1")
        g.spoke("core", "gw2")
        # Ring 2
        g.spoke("gw1", "app1")
        g.spoke("gw1", "app2")
        g.spoke("gw2", "app3")

        layout = g.get_layout(width=120.0, height=120.0, margin=10.0)

        assert len(layout.nodes) == 6

        hub = layout.nodes["core"]
        gw1 = layout.nodes["gw1"]
        app1 = layout.nodes["app1"]

        dist_ring1 = ((gw1.x - hub.x) ** 2 + (gw1.y - hub.y) ** 2) ** 0.5
        dist_ring2 = ((app1.x - hub.x) ** 2 + (app1.y - hub.y) ** 2) ** 0.5

        assert dist_ring2 > dist_ring1
        assert 1 in layout.ring_radii
        assert 2 in layout.ring_radii
        assert layout.ring_radii[2] > layout.ring_radii[1]

    def test_custom_center_and_semicircle(self) -> None:
        """Verify custom center and fan angle sweep (semicircle)."""
        g = RadialGraph(
            hub="root",
            center=(30.0, 30.0),
            start_angle=0.0,
            angle_range=180.0,
        )
        g.node("root")
        g.spoke("root", "a")
        g.spoke("root", "b")
        g.spoke("root", "c")

        layout = g.get_layout(width=100.0, height=100.0)

        hub = layout.nodes["root"]
        assert hub.xy == (30.0, 30.0)

        # With 0 to 180 degrees sweep, Y should be >= hub.y
        for nid in ["a", "b", "c"]:
            node = layout.nodes[nid]
            assert node.y >= hub.y - 0.1

    def test_boundary_port_intersections(self) -> None:
        """Verify edge ports touch node perimeters rather than node centers."""
        g = RadialGraph(hub="center")
        g.node("center", width=20.0, height=20.0)
        g.spoke("center", "east", width=20.0, height=10.0)

        layout = g.get_layout(width=100.0, height=100.0)
        edge = layout.edges[0]

        center_nl = layout.nodes["center"]
        east_nl = layout.nodes["east"]

        # src_port should be on center node boundary (half_w = 10.0 from center.xy)
        src_dist = ((edge.src_port[0] - center_nl.x) ** 2 + (edge.src_port[1] - center_nl.y) ** 2) ** 0.5
        assert abs(src_dist - 10.0) < 0.5

        # dst_port should not equal east_nl.xy
        assert edge.dst_port != east_nl.xy


class TestGridGraph:
    """Test suite for GridGraph layout solver."""

    def setup_method(self) -> None:
        """Reset canvas before each test."""
        clear()

    def test_grid_subclass(self) -> None:
        """Verify GridGraph is a subclass of BaseGraph."""
        assert issubclass(GridGraph, BaseGraph)

    def test_basic_row_major_tiling(self) -> None:
        """Verify regular 3x2 matrix tiling in row-major order."""
        g = GridGraph(columns=3, order="row-major")
        for i in range(6):
            g.node(f"n{i}")

        layout = g.get_layout(width=120.0, height=80.0, margin=10.0)

        assert len(layout.nodes) == 6
        n0 = layout.nodes["n0"]
        n1 = layout.nodes["n1"]
        n2 = layout.nodes["n2"]
        n3 = layout.nodes["n3"]

        # Row 0 (n0, n1, n2) should have same Y, higher than Row 1 (n3)
        assert n0.y == n1.y == n2.y
        assert n0.y > n3.y

        # Columns should advance rightwards
        assert n0.x < n1.x < n2.x

    def test_column_major_tiling(self) -> None:
        """Verify column-major tiling order."""
        g = GridGraph(columns=3, rows=2, order="column-major")
        for i in range(6):
            g.node(f"n{i}")

        layout = g.get_layout(width=120.0, height=80.0, margin=10.0)

        assert len(layout.nodes) == 6
        n0 = layout.nodes["n0"]
        n1 = layout.nodes["n1"]
        n2 = layout.nodes["n2"]

        # In column-major with 2 rows, n0 is at (0, 0) and n1 is at (1, 0)
        assert n0.x == n1.x
        assert n0.y > n1.y
        # n2 is at (0, 1), so same row as n0 but next column
        assert n2.y == n0.y
        assert n2.x > n0.x

    def test_explicit_pinning_and_cell_helper(self) -> None:
        """Verify explicit (row, col) slot pinning with cell helper."""
        g = GridGraph(columns=3)
        # Pin a node at (1, 1) - center slot
        g.cell("center", row=1, col=1)
        # Add unpinned nodes
        g.node("a")
        g.node("b")
        g.node("c")

        layout = g.get_layout(width=120.0, height=80.0)

        # "a", "b", "c" should fill (0, 0), (0, 1), (0, 2)
        # while "center" is at (1, 1)
        a = layout.nodes["a"]
        b = layout.nodes["b"]
        c = layout.nodes["c"]
        center = layout.nodes["center"]

        assert a.y == b.y == c.y
        assert a.x < b.x < c.x
        assert center.y < a.y
        assert center.x == b.x

    def test_edge_routing_strategies(self) -> None:
        """Verify horizontal, vertical, and corridor routing."""
        g = GridGraph(columns=2, order="row-major", edge_routing="smart")
        g.cell("top_left", row=0, col=0)
        g.cell("top_right", row=0, col=1)
        g.cell("bot_left", row=1, col=0)
        g.cell("bot_right", row=1, col=1)

        # Horizontal neighbor edge
        g.edge("top_left", "top_right")
        # Vertical neighbor edge
        g.edge("top_left", "bot_left")
        # Diagonal neighbor edge
        g.edge("top_left", "bot_right")

        layout = g.get_layout(width=100.0, height=100.0)

        assert len(layout.edges) == 3

        # Horizontal edge: no waypoints
        e_horiz = layout.edges[0]
        assert e_horiz.waypoints == []
        assert e_horiz.src_port[1] == e_horiz.dst_port[1]

        # Vertical edge: no waypoints
        e_vert = layout.edges[1]
        assert e_vert.waypoints == []
        assert e_vert.src_port[0] == e_vert.dst_port[0]

        # Diagonal edge: 2 waypoints creating Manhattan corridor
        e_diag = layout.edges[2]
        assert len(e_diag.waypoints) == 2
        # Corridor mid_y should be between src and dst
        mid_y = e_diag.waypoints[0][1]
        assert e_diag.src_port[1] > mid_y > e_diag.dst_port[1]

    def test_cluster_row_and_column(self) -> None:
        """Verify dynamic row and column cluster conveniences."""
        g = GridGraph(columns=3)
        for i in range(6):
            g.node(f"n{i}")

        g.cluster_row(0, "row_0")
        g.cluster_column(1, "col_1")

        # Duplicate ID should raise ValueError
        with pytest.raises(ValueError, match="already registered"):
            g.cluster_row(1, "row_0")

        layout = g.get_layout(width=120.0, height=80.0)

        assert "row_0" in layout.clusters
        assert "col_1" in layout.clusters

        r0_cl = layout.clusters["row_0"]
        n0 = layout.nodes["n0"]
        n1 = layout.nodes["n1"]
        n2 = layout.nodes["n2"]

        assert r0_cl.left <= min(n0.left, n1.left, n2.left)
        assert r0_cl.right >= max(n0.right, n1.right, n2.right)


class TestLayerGraph:
    """Test suite for LayerGraph layout solver."""

    def setup_method(self) -> None:
        """Reset canvas before each test."""
        clear()

    def test_layer_subclass(self) -> None:
        """Verify LayerGraph is a subclass of BaseGraph."""
        assert issubclass(LayerGraph, BaseGraph)

    def test_basic_dag_lr(self) -> None:
        """Verify basic DAG pipeline in Left-to-Right direction."""
        g = LayerGraph(direction="LR")
        g.edge("checkout", "test")
        g.edge("checkout", "lint")
        g.edge("test", "build")
        g.edge("lint", "build")
        g.edge("build", "deploy")

        layout = g.get_layout(width=140.0, height=80.0)

        assert len(layout.nodes) == 5
        checkout = layout.nodes["checkout"]
        test = layout.nodes["test"]
        lint = layout.nodes["lint"]
        build = layout.nodes["build"]
        deploy = layout.nodes["deploy"]

        # LR flow: X increases along pipeline stages
        assert checkout.x < test.x
        assert test.x == lint.x
        assert test.x < build.x < deploy.x

        # Parallel branches in same layer should have different Y
        assert test.y != lint.y

    def test_basic_dag_tb(self) -> None:
        """Verify basic DAG pipeline in Top-to-Bottom direction."""
        g = LayerGraph(direction="TB")
        g.edge("checkout", "test")
        g.edge("checkout", "lint")
        g.edge("test", "build")
        g.edge("lint", "build")
        g.edge("build", "deploy")

        layout = g.get_layout(width=100.0, height=120.0)

        assert len(layout.nodes) == 5
        checkout = layout.nodes["checkout"]
        test = layout.nodes["test"]
        lint = layout.nodes["lint"]
        build = layout.nodes["build"]
        deploy = layout.nodes["deploy"]

        # TB flow: Y decreases downwards
        assert checkout.y > test.y
        assert test.y == lint.y
        assert test.y > build.y > deploy.y

        # Parallel branches in same layer should have different X
        assert test.x != lint.x

    def test_multi_parent_merge(self) -> None:
        """Verify LayerGraph supports multiple parents merging into one child."""
        g = LayerGraph(direction="LR")
        g.node("api_gw")
        g.node("msg_queue")
        g.edge("api_gw", "processor")
        g.edge("msg_queue", "processor")

        layout = g.get_layout(width=100.0, height=80.0)
        assert len(layout.nodes) == 3

        gw = layout.nodes["api_gw"]
        queue = layout.nodes["msg_queue"]
        proc = layout.nodes["processor"]

        assert proc.x > max(gw.x, queue.x)

    def test_cycle_handling(self) -> None:
        """Verify graphs with cycles / feedback loops do not crash and assign layers."""
        g = LayerGraph(direction="LR")
        g.edge("a", "b")
        g.edge("b", "c")
        g.edge("c", "a")  # Feedback loop

        layout = g.get_layout(width=100.0, height=80.0)
        assert len(layout.nodes) == 3
        assert len(layout.edges) == 3

    def test_explicit_tier_and_layer_pinning(self) -> None:
        """Verify explicit layer and tier pinning."""
        g = LayerGraph(direction="LR")
        g.tier("input", ["in1", "in2"], layer=0)
        g.node("custom", layer=2)
        g.edge("in1", "mid")
        g.edge("mid", "custom")

        layout = g.get_layout(width=120.0, height=80.0)
        in1 = layout.nodes["in1"]
        in2 = layout.nodes["in2"]
        custom = layout.nodes["custom"]

        assert in1.x == in2.x
        assert custom.x > in1.x

    def test_edge_routing_styles(self) -> None:
        """Verify orthogonal and straight routing styles in LayerGraph."""
        g_ortho = LayerGraph(direction="LR", edge_routing="orthogonal")
        g_ortho.edge("a", "b")
        g_ortho.edge("a", "c")
        l_ortho = g_ortho.get_layout(width=100.0, height=80.0)
        assert len(l_ortho.edges) == 2

        g_straight = LayerGraph(direction="LR", edge_routing="straight")
        g_straight.edge("a", "b")
        g_straight.edge("a", "c")
        l_straight = g_straight.get_layout(width=100.0, height=80.0)
        assert len(l_straight.edges) == 2
        for e in l_straight.edges:
            assert e.waypoints == []

    def test_clusters(self) -> None:
        """Verify cluster grouping in LayerGraph."""
        g = LayerGraph(direction="LR")
        g.edge("in", "p1")
        g.edge("in", "p2")
        g.cluster("pool", ["p1", "p2"])

        layout = g.get_layout(width=100.0, height=80.0)
        assert "pool" in layout.clusters
        c = layout.clusters["pool"]
        p1 = layout.nodes["p1"]
        p2 = layout.nodes["p2"]

        assert c.top >= max(p1.top, p2.top)
        assert c.bottom <= min(p1.bottom, p2.bottom)


class TestArchitectureGraph:
    """Test suite for ArchitectureGraph compound layout solver."""

    def setup_method(self) -> None:
        """Reset canvas before each test."""
        clear()

    def test_architecture_subclass(self) -> None:
        """Verify ArchitectureGraph is a subclass of BaseGraph."""
        assert issubclass(ArchitectureGraph, BaseGraph)

    def test_empty_graph(self) -> None:
        """Verify empty ArchitectureGraph returns empty layout."""
        g = ArchitectureGraph()
        layout = g.get_layout(width=100.0, height=80.0)
        assert len(layout.nodes) == 0
        assert len(layout.edges) == 0
        assert len(layout.clusters) == 0

    def test_fallback_to_layered(self) -> None:
        """Verify graph without containers cleanly falls back to LayerGraph layout."""
        g = ArchitectureGraph(direction="LR")
        g.edge("app", "db")
        layout = g.get_layout(width=100.0, height=80.0)
        assert len(layout.nodes) == 2
        assert layout.nodes["app"].x < layout.nodes["db"].x

    def test_multi_container_lr(self) -> None:
        """Verify root containers are ordered left-to-right along edge flows."""
        g = ArchitectureGraph(direction="LR")
        g.cluster("clients", ["browser", "mobile"])
        g.cluster("cloud", ["api_gateway", "service"])
        g.cluster("storage", ["rds", "s3"])

        g.edge("browser", "api_gateway")
        g.edge("mobile", "api_gateway")
        g.edge("api_gateway", "service")
        g.edge("service", "rds")
        g.edge("service", "s3")

        layout = g.get_layout(width=160.0, height=90.0)
        assert len(layout.nodes) == 6
        assert len(layout.clusters) == 3

        c_clients = layout.clusters["clients"]
        c_cloud = layout.clusters["cloud"]
        c_storage = layout.clusters["storage"]

        # Container sequence along LR
        assert c_clients.cx < c_cloud.cx < c_storage.cx

        # Nodes must be placed inside their cluster bounds
        for nid in ["browser", "mobile"]:
            node = layout.nodes[nid]
            assert c_clients.left <= node.left and node.right <= c_clients.right
            assert c_clients.bottom <= node.bottom and node.top <= c_clients.top

        for nid in ["api_gateway", "service"]:
            node = layout.nodes[nid]
            assert c_cloud.left <= node.left and node.right <= c_cloud.right

        for nid in ["rds", "s3"]:
            node = layout.nodes[nid]
            assert c_storage.left <= node.left and node.right <= c_storage.right

    def test_multi_container_tb(self) -> None:
        """Verify root containers are ordered top-to-bottom along edge flows."""
        g = ArchitectureGraph(direction="TB")
        g.cluster("edge_zone", ["cdn"])
        g.cluster("app_zone", ["backend"])

        g.edge("cdn", "backend")

        layout = g.get_layout(width=100.0, height=120.0)
        assert len(layout.clusters) == 2

        c_edge = layout.clusters["edge_zone"]
        c_app = layout.clusters["app_zone"]

        assert c_edge.cy > c_app.cy

    def test_explicit_container_order(self) -> None:
        """Verify explicit container ordering overrides automatic topological sort."""
        g = ArchitectureGraph(direction="LR")
        g.cluster("zone_b", ["b1"], order=1)
        g.cluster("zone_a", ["a1"], order=0)
        g.cluster("zone_c", ["c1"], order=2)

        layout = g.get_layout(width=120.0, height=60.0)
        c_a = layout.clusters["zone_a"]
        c_b = layout.clusters["zone_b"]
        c_c = layout.clusters["zone_c"]

        assert c_a.cx < c_b.cx < c_c.cx

    def test_nested_subgroups(self) -> None:
        """Verify nested subgroups (e.g. subnets inside VPC) position correctly."""
        g = ArchitectureGraph(direction="LR")
        g.cluster("vpc", [])
        g.cluster("public_subnet", ["alb"], parent="vpc")
        g.cluster("private_subnet", ["ecs_task"], parent="vpc")

        g.edge("alb", "ecs_task")

        layout = g.get_layout(width=140.0, height=80.0)
        assert "vpc" in layout.clusters
        assert "public_subnet" in layout.clusters
        assert "private_subnet" in layout.clusters

        c_vpc = layout.clusters["vpc"]
        c_pub = layout.clusters["public_subnet"]
        c_priv = layout.clusters["private_subnet"]

        # Subnets are ordered LR inside VPC
        assert c_pub.cx < c_priv.cx

        # Subnets are contained within VPC bounds
        assert c_vpc.left <= c_pub.left and c_pub.right <= c_vpc.right
        assert c_vpc.left <= c_priv.left and c_priv.right <= c_vpc.right
        assert c_vpc.bottom <= c_pub.bottom and c_pub.top <= c_vpc.top
        assert c_vpc.bottom <= c_priv.bottom and c_priv.top <= c_vpc.top

    def test_node_group_and_subgroup_attributes(self) -> None:
        """Verify nodes can assign their group and subgroup via node() parameters."""
        g = ArchitectureGraph(direction="LR")
        g.cluster("vpc", [])
        g.node("gateway", group="vpc", subgroup="public")
        g.node("api", group="vpc", subgroup="private")
        g.edge("gateway", "api")

        layout = g.get_layout(width=120.0, height=80.0)
        assert "gateway" in layout.nodes
        assert "api" in layout.nodes
        assert "vpc" in layout.clusters
        assert "public" in layout.clusters
        assert "private" in layout.clusters

    def test_group_convenience_method(self) -> None:
        """Verify group() convenience method creates a container."""
        g = ArchitectureGraph(direction="LR")
        g.group("k8s_cluster", nodes=["pod1", "pod2"])
        g.edge("pod1", "pod2")

        layout = g.get_layout(width=100.0, height=80.0)
        assert "k8s_cluster" in layout.clusters
        assert len(layout.nodes) == 2

    def test_compass_5_zones(self) -> None:
        """Verify 2D compass layout positioning for all 5 zones (center, top, bottom, left, right)."""
        g = ArchitectureGraph()
        g.cluster("clients", ["browser"], pos="left")
        g.cluster("monitoring", ["cloudwatch"], pos="top")
        g.cluster("vpc", ["api"], pos="center")
        g.cluster("db", ["aurora"], pos="bottom")
        g.cluster("saas", ["stripe"], pos="right")

        g.edge("browser", "api")
        g.edge("api", "cloudwatch")
        g.edge("api", "aurora")
        g.edge("api", "stripe")

        layout = g.get_layout(width=160.0, height=120.0)
        assert len(layout.clusters) == 5

        c_left = layout.clusters["clients"]
        c_right = layout.clusters["saas"]
        c_center = layout.clusters["vpc"]
        c_top = layout.clusters["monitoring"]
        c_bottom = layout.clusters["db"]

        # Horizontal alignment
        assert c_left.cx < c_center.cx < c_right.cx

        # Vertical alignment
        assert c_bottom.cy < c_center.cy < c_top.cy

        # Relative containment
        assert c_left.right <= c_center.left
        assert c_center.right <= c_right.left
        assert c_bottom.top <= c_center.bottom
        assert c_center.top <= c_top.bottom

    def test_compass_top_and_bottom_into_center(self) -> None:
        """Verify convergent flows from top and bottom into center."""
        g = ArchitectureGraph()
        g.cluster("ingress", ["apigw"], pos="top")
        g.cluster("core", ["service"], pos="center")
        g.cluster("legacy", ["mainframe"], pos="bottom")

        # Top flows down, bottom flows up
        g.edge("apigw", "service")
        g.edge("mainframe", "service")

        layout = g.get_layout(width=100.0, height=120.0)
        assert len(layout.clusters) == 3

        c_top = layout.clusters["ingress"]
        c_center = layout.clusters["core"]
        c_bottom = layout.clusters["legacy"]

        assert c_top.cy > c_center.cy > c_bottom.cy

        # Verify edge port directions
        e_top = layout.edges[0]
        assert e_top.src == "apigw" and e_top.dst == "service"
        assert e_top.src_port[1] > e_top.dst_port[1]  # Flows downward

        e_bot = layout.edges[1]
        assert e_bot.src == "mainframe" and e_bot.dst == "service"
        assert e_bot.src_port[1] < e_bot.dst_port[1]  # Flows upward


class TestGraphLayoutModelsAndDiagramsIntegration:
    """Test suite for GraphLayout coordinate helpers, string representation, and diagrams integration."""

    def setup_method(self) -> None:
        """Reset canvas before each test."""
        clear()

    def test_layout_properties_and_str_summary(self) -> None:
        """Verify local_xy, local_bottom_left, bottom_left, mid_xy, __getitem__, and __str__."""
        g = ArchitectureGraph(direction="LR")
        g.group("vpc")
        g.cluster("app_tier", ["api", "worker"], parent="vpc", order=1)
        g.node("client")
        g.edge("client", "api")
        g.edge("api", "worker")

        layout = g.get_layout(width=140.0, height=80.0)

        # __getitem__ lookup for both clusters and nodes
        c_vpc = layout["vpc"]
        c_app = layout["app_tier"]
        n_api = layout["api"]
        assert isinstance(c_vpc, ClusterLayout)
        assert isinstance(c_app, ClusterLayout)
        assert isinstance(n_api, NodeLayout)

        with pytest.raises(KeyError):
            _ = layout["nonexistent"]

        # Verify hierarchy coordinates math
        assert c_app.parent_id == "vpc"
        assert c_app.local_bottom_left == (
            round(c_app.left - c_vpc.left, 2),
            round(c_app.bottom - c_vpc.bottom, 2),
        )
        assert n_api.parent_id == "app_tier"
        assert n_api.local_xy == (
            round(n_api.x - c_app.left, 2),
            round(n_api.y - c_app.bottom, 2),
        )
        assert n_api.bottom_left == (n_api.left, n_api.bottom)
        assert n_api.center == n_api.xy
        assert n_api.size == (n_api.width, n_api.height)
        assert c_vpc.center == c_vpc.xy
        assert c_vpc.size == (c_vpc.width, c_vpc.height)

        # Verify EdgeLayout.mid_xy and points
        for edge in layout.edges:
            assert len(edge.points) >= 2
            mx, my = edge.mid_xy
            assert isinstance(mx, float) and isinstance(my, float)

        # Verify str(layout) output
        text_report = str(layout)
        assert "GraphLayout(width=140.0, height=80.0)" in text_report
        assert "Clusters:" in text_report
        assert "vpc" in text_report
        assert "local_bottom_left=" in text_report
        assert "Nodes:" in text_report
        assert "local_xy=" in text_report
        assert "Edges:" in text_report

    def test_2step_integration_with_architecture_and_flow_diagrams(self) -> None:
        """Verify 2-step workflow: Step 1 get_layout() -> Step 2 ArchitectureDiagram and FlowDiagram."""
        # 1. ArchitectureGraph -> ArchitectureDiagram
        g_arch = ArchitectureGraph(direction="LR", default_node_width=20.0, default_node_height=16.0)
        g_arch.group("vpc")
        g_arch.cluster("compute", ["api", "worker"], parent="vpc")
        g_arch.node("client")
        g_arch.edge("client", "api")
        g_arch.edge("api", "worker")

        arch_layout = g_arch.get_layout(width=140.0, height=80.0)

        d_arch = ArchitectureDiagram(
            node_style=Styles.Primary,
            node_text_style=Styles.DarkBold,
            edge_style=Styles.DarkBold,
            edge_text_style=Styles.Dark,
            node_card_style=Styles.Neutral,
        )
        c_vpc = arch_layout.clusters["vpc"]
        c_comp = arch_layout.clusters["compute"]
        vpc_grp = d_arch.add(
            NodeGroup(
                "VPC",
                width=c_vpc.width,
                height=c_vpc.height,
                style=Styles.PrimaryNeutral,
                text_style=Styles.DarkBold,
            ),
            xy=c_vpc.bottom_left,
        )
        comp_grp = vpc_grp.add(
            NodeGroup(
                "Compute",
                width=c_comp.width,
                height=c_comp.height,
                style=Styles.SecondaryNeutral,
                text_style=Styles.DarkBold,
            ),
            xy=c_comp.local_bottom_left,
        )

        n_client = d_arch.add(ArchNode("Client"), xy=arch_layout.nodes["client"].xy)
        n_api = comp_grp.add(ArchNode("API"), xy=arch_layout.nodes["api"].local_xy)
        n_worker = comp_grp.add(ArchNode("Worker"), xy=arch_layout.nodes["worker"].local_xy)
        d_arch.add_edge(ArchEdge(n_client, n_api, label="HTTPS"))
        d_arch.add_edge(ArchEdge(n_api, n_worker, label="gRPC"))
        d_arch.draw(xy=(0.0, 0.0))
        assert len(canvas._artists) > 0

        # 2. LayerGraph -> FlowDiagram
        clear()
        g_flow = LayerGraph(direction="LR")
        g_flow.edge("build", "test")
        g_flow.edge("test", "deploy")
        flow_layout = g_flow.get_layout(width=120.0, height=60.0)

        d_flow = FlowDiagram(
            node_style=Styles.Neutral,
            edge_style=Styles.DarkBold,
            edge_text_style=Styles.Dark,
        )
        p_build = d_flow.add(Process("Build"), xy=flow_layout.nodes["build"].xy)
        p_test = d_flow.add(Process("Test"), xy=flow_layout.nodes["test"].xy)
        p_deploy = d_flow.add(Process("Deploy"), xy=flow_layout.nodes["deploy"].xy)
        d_flow.connect(p_build, p_test)
        d_flow.connect(p_test, p_deploy)
        d_flow.draw(xy=(0.0, 0.0))
        assert len(canvas._artists) > 0
