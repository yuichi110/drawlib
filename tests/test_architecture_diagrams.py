# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for drawlib.diagrams.architecture."""

import tempfile
from pathlib import Path
from typing import Any, cast

import pytest
from PIL import Image

import drawlib.diagrams.architecture.icons as arch_icons
from drawlib import canvas
from drawlib._core.l2_models import Dimage
from drawlib._core.l3_styles import Colors, Style
from drawlib._diagrams.architecture._renderer import _apply_edge_padding
from drawlib.diagrams.architecture import (
    ArchitectureDiagram,
    CustomIcon,
    Edge,
    GcpIcon,
    Junction,
    Node,
    NodeGroup,
    PhosphorIcon,
)


class TestArchitectureIcons:
    """Test suite for architecture diagram icon definitions."""

    def test_gcp_icons(self) -> None:
        """Verify GCP icons enum members and string values."""
        assert GcpIcon.COMPUTE_ENGINE == "compute_engine"
        assert GcpIcon.CLOUD_STORAGE == "cloud_storage"
        assert GcpIcon.CLOUD_SQL == "cloud_sql"
        assert GcpIcon.BIGQUERY == "bigquery"
        assert arch_icons.GcpIcon.GOOGLE_KUBERNETES_ENGINE == "google_kubernetes_engine"

    def test_phosphor_icons(self) -> None:
        """Verify Phosphor icons enum members and string values."""
        assert PhosphorIcon.DATABASE == "database"
        assert PhosphorIcon.USER == "user"
        assert PhosphorIcon.CLOUD == "cloud"
        assert arch_icons.PhosphorIcon.BROWSER == "browser"

    def test_custom_icon_from_pil_image(self) -> None:
        """Verify CustomIcon creation from PIL Image."""
        pil_img = Image.new("RGBA", (100, 100), (255, 0, 0, 255))
        icon = CustomIcon(pil_img)
        assert isinstance(icon.dimage, Dimage)
        copied = icon.copy()
        assert isinstance(copied, CustomIcon)
        assert copied is not icon

    def test_custom_icon_from_dimage(self) -> None:
        """Verify CustomIcon creation from Dimage."""
        pil_img = Image.new("RGBA", (50, 50), (0, 255, 0, 255))
        dimage = Dimage(pil_img)
        icon = CustomIcon(dimage)
        assert isinstance(icon.dimage, Dimage)

    def test_custom_icon_from_custom_icon(self) -> None:
        """Verify CustomIcon copy construction."""
        pil_img = Image.new("RGBA", (20, 20), (0, 0, 255, 255))
        icon1 = CustomIcon(pil_img)
        icon2 = CustomIcon(icon1)
        assert isinstance(icon2.dimage, Dimage)

    def test_custom_icon_invalid_type(self) -> None:
        """Verify CustomIcon raises ValueError on invalid input type."""
        with pytest.raises(ValueError, match="CustomIcon does not support image of type"):
            CustomIcon(cast(Any, 12345))


class TestArchitectureNode:
    """Test suite for Node vertex component."""

    def test_node_coordinates_are_icon_centered(self) -> None:
        """Verify node coordinates always refer to the icon center regardless of label text."""
        node_no_text = Node(icon=GcpIcon.COMPUTE_ENGINE, icon_size=10.0)
        node_no_text._local_xy = (20.0, 30.0)
        assert node_no_text.xy == (20.0, 30.0)
        assert node_no_text.center == (20.0, 30.0)

        node_with_text = Node(
            text="Very Long Production Service Label\nLine 2",
            icon=GcpIcon.COMPUTE_ENGINE,
            icon_size=10.0,
            text_position="bottom",
        )
        node_with_text._local_xy = (20.0, 30.0)
        assert node_with_text.xy == (20.0, 30.0)
        assert node_with_text.center == (20.0, 30.0)

    def test_node_anchors_horizontal_axis(self) -> None:
        """Verify left and right anchors are precisely centered along the icon's horizontal axis."""
        node = Node(text="App", icon_size=10.0)
        node._local_xy = (50.0, 50.0)
        assert node.left == (45.0, 50.0)
        assert node.right == (55.0, 50.0)

    def test_node_anchors_vertical_clearance(self) -> None:
        """Verify top/bottom anchors adjust for text position to avoid collisions."""
        node_bottom_text = Node(text="Bottom Text", icon_size=10.0, text_position="bottom")
        node_bottom_text._local_xy = (50.0, 50.0)
        # Top anchor should be on the icon edge
        assert node_bottom_text.top == (50.0, 55.0)
        # Bottom anchor should be offset below the label text
        bx, by = node_bottom_text.bottom
        assert bx == 50.0
        assert by < 45.0

    def test_node_size_calculation(self) -> None:
        """Verify get_size includes icon size and text dimensions."""
        node = Node(text="Server", icon_size=8.0, text_position="bottom")
        w, h = node.get_size()
        assert w >= 8.0
        assert h > 8.0


class TestArchitectureGroup:
    """Test suite for NodeGroup boundary component."""

    def test_group_auto_bounds(self) -> None:
        """Verify auto-bounding box calculation based on children and padding."""
        group = NodeGroup(title="Subnet", padding=5.0)
        n1 = Node(icon=GcpIcon.COMPUTE_ENGINE, icon_size=10.0)
        n2 = Node(icon=GcpIcon.COMPUTE_ENGINE, icon_size=10.0)
        group.add(n1, (10.0, 10.0))
        group.add(n2, (30.0, 10.0))

        min_x, min_y, max_x, max_y = group.get_bounds()
        assert min_x <= 10.0 - 5.0 - 5.0  # icon center 10 - half_size 5 - padding 5
        assert max_x >= 30.0 + 5.0 + 5.0  # icon center 30 + half_size 5 + padding 5
        assert max_y > min_y

    def test_group_fixed_dimensions(self) -> None:
        """Verify explicit width and height override auto-bounds."""
        group = NodeGroup(title="Fixed Group", width=100.0, height=80.0)
        bounds = group.get_bounds()
        assert bounds == (0.0, 0.0, 100.0, 80.0)
        assert group.get_size() == (100.0, 80.0)

    def test_group_anchors(self) -> None:
        """Verify anchor points on group boundaries."""
        group = NodeGroup(width=40.0, height=20.0)
        assert group.left == (0.0, 10.0)
        assert group.right == (40.0, 10.0)
        assert group.top == (20.0, 20.0)
        assert group.bottom == (20.0, 0.0)
        assert group.center == (20.0, 10.0)


class TestArchitectureJunctionAndEdge:
    """Test suite for Junction and Edge chaining."""

    def test_junction_properties(self) -> None:
        """Verify Junction coordinate and anchor properties."""
        j = Junction((15.0, 25.0))
        assert j.xy == (15.0, 25.0)
        assert j.center == (15.0, 25.0)
        assert j.left == (15.0, 25.0)
        assert j.right == (15.0, 25.0)
        assert j.top == (15.0, 25.0)
        assert j.bottom == (15.0, 25.0)
        assert j.get_size() == (0.0, 0.0)

    def test_edge_chaining(self) -> None:
        """Verify Edge fluent chaining methods."""
        n1 = Node(text="A")
        n2 = Node(text="B")
        edge = Edge(start=n1, end=n2)

        edge.set_label("HTTPS", pos=0.5).set_arrow("<->").via((10.0, 20.0), (30.0, 40.0))
        assert edge.label == "HTTPS"
        assert edge.arrow == "<->"
        assert edge.waypoints == [(10.0, 20.0), (30.0, 40.0)]

    def test_edge_add_point(self) -> None:
        """Verify edge.add_point adds waypoint and returns connected Junction."""
        d = ArchitectureDiagram()
        n1 = d.add(Node(text="A"), (0.0, 0.0))
        n2 = d.add(Node(text="B"), (50.0, 0.0))
        edge = d.connect(n1, n2)

        j = edge.add_point((25.0, 0.0))
        assert isinstance(j, Junction)
        assert (25.0, 0.0) in edge.waypoints
        assert j in d.items

    def test_edge_padding_properties(self) -> None:
        """Verify edge padding parameter and fluent setter."""
        n1 = Node(text="A")
        n2 = Node(text="B")
        edge = Edge(start=n1, end=n2, padding=2.0)
        assert edge.padding == 2.0

        edge.set_padding((1.0, 3.0))
        assert edge.padding == (1.0, 3.0)

    def test_connect_methods_propagate_padding(self) -> None:
        """Verify all connect methods forward the padding argument to Edge."""
        d = ArchitectureDiagram()
        n1 = d.add(Node(text="A"), (10.0, 10.0))
        n2 = d.add(Node(text="B"), (30.0, 10.0))
        grp = d.add(NodeGroup(title="G"), (50.0, 10.0))

        e1 = d.connect(n1, n2, padding=1.5)
        assert e1.padding == 1.5

        e2 = n1.connect(n2, padding=(1.0, 2.0))
        assert e2.padding == (1.0, 2.0)

        e3 = grp.connect(n1, padding=2.5)
        assert e3.padding == 2.5

        j = e1.add_point((20.0, 10.0))
        e4 = j.connect(n2, padding=0.5)
        assert e4.padding == 0.5

    def test_apply_edge_padding_direct(self) -> None:
        """Verify _apply_edge_padding calculation on 2-point and polyline edges."""
        # Zero padding
        pts = [(0.0, 0.0), (10.0, 0.0)]
        assert _apply_edge_padding(pts, 0.0) == [(0.0, 0.0), (10.0, 0.0)]

        # Symmetric float padding on horizontal line
        padded = _apply_edge_padding([(0.0, 0.0), (10.0, 0.0)], 2.0)
        assert padded == pytest.approx([(2.0, 0.0), (8.0, 0.0)])

        # Asymmetric tuple padding
        padded_asym = _apply_edge_padding([(0.0, 0.0), (10.0, 0.0)], (1.0, 3.0))
        assert padded_asym == pytest.approx([(1.0, 0.0), (7.0, 0.0)])

        # Polyline (3 points)
        pts3 = [(0.0, 0.0), (10.0, 0.0), (10.0, 10.0)]
        padded3 = _apply_edge_padding(pts3, 2.0)
        assert padded3[0] == pytest.approx((2.0, 0.0))
        assert padded3[1] == (10.0, 0.0)
        assert padded3[2] == pytest.approx((10.0, 8.0))

    def test_node_fork(self) -> None:
        """Verify node.fork creates junction and multiple connecting edges."""
        d = ArchitectureDiagram()
        src = d.add(Node(text="Client"), (10.0, 50.0))
        t1 = d.add(Node(text="API 1"), (60.0, 70.0))
        t2 = d.add(Node(text="API 2"), (60.0, 30.0))

        edges = src.fork([t1, t2], at_x=35.0, padding=1.5)
        assert len(edges) == 3
        assert len(d.edges) == 3
        assert edges[0].padding == (1.5, 0.0)
        assert edges[1].padding == (0.0, 1.5)
        assert edges[2].padding == (0.0, 1.5)


class TestArchitectureDiagramEndToEnd:
    """End-to-end rendering and canvas integration tests."""

    def test_diagram_rendering_scenario_a_gcp_vpc(self) -> None:
        """Verify rendering complete GCP VPC architecture diagram on canvas."""
        canvas.initialize()

        d = ArchitectureDiagram(title="GCP Architecture")
        vpc = d.add(NodeGroup(title="VPC Network", padding=6.0), (10.0, 10.0))
        subnet = vpc.add(NodeGroup(title="us-central1 Subnet", padding=4.0), (5.0, 5.0))

        vm1 = subnet.add(Node("Web Server 1", icon=GcpIcon.COMPUTE_ENGINE), (15.0, 20.0))
        vm2 = subnet.add(Node("Web Server 2", icon=GcpIcon.COMPUTE_ENGINE), (15.0, 45.0))

        db = d.add(Node("Primary DB", icon=GcpIcon.CLOUD_SQL), (60.0, 30.0))

        d.connect(vm1, db, label="SQL Query")
        d.connect(vm2, db, label="SQL Query")

        # Render diagram onto canvas
        d.draw(xy=(5.0, 5.0))

        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "test_vpc_arch.png"
            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_diagram_rendering_custom_and_phosphor_icons(self) -> None:
        """Verify rendering with Phosphor icons, CustomIcon, and custom style."""
        canvas.initialize()

        pil_img = Image.new("RGBA", (64, 64), (100, 150, 200, 255))
        custom_icon = CustomIcon(pil_img)

        d = ArchitectureDiagram(title="Microservices")
        client = d.add(Node("Browser", icon=PhosphorIcon.BROWSER, icon_size=8.0), (15.0, 50.0))
        gateway = d.add(
            Node(
                "Custom Gateway",
                icon=custom_icon,
                icon_size=10.0,
                style=Style(fill_color=Colors.White, line_color=Colors.Gray, line_width=1.0),
            ),
            (45.0, 50.0),
        )
        storage = d.add(Node("Database", icon=PhosphorIcon.DATABASE, icon_size=8.0), (75.0, 50.0))

        d.connect(client, gateway, label="HTTPS", routing="orthogonal")
        d.connect(gateway, storage, label="TCP", routing="orthogonal")

        d.draw(xy=(10.0, 10.0))

        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "test_microservices.png"
            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_diagram_rendering_with_edge_padding(self) -> None:
        """Verify diagram rendering with edge padding succeeds without errors."""
        canvas.initialize()
        d = ArchitectureDiagram()
        n1 = d.add(Node("A", icon=PhosphorIcon.BROWSER), (20.0, 50.0))
        n2 = d.add(Node("B", icon=PhosphorIcon.DATABASE), (80.0, 50.0))
        d.connect(n1, n2, padding=3.0)
        d.draw()

        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "test_padding.png"
            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0
