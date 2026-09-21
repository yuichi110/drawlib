# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for drawlib.diagrams.flow."""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any, cast

import pytest

from drawlib import canvas
from drawlib._core.l3_styles import Colors, Style
from drawlib.diagrams.flow import (
    Data,
    Decision,
    End,
    FlowDiagram,
    FlowEdge,
    FlowNode,
    Junction,
    Lane,
    Process,
    Start,
)


class TestFlowNodes:
    """Unit tests for FlowNode shape classes."""

    def test_process_initialization(self) -> None:
        """Verify Process node defaults and attributes."""
        p = Process(text="Execute Job", width=30.0, height=15.0, r=2.0)
        assert p.text == "Execute Job"
        assert p.width == 30.0
        assert p.height == 15.0
        assert p.r == 2.0
        assert p.shape_type == "process"
        assert p.xy == (0.0, 0.0)

    def test_decision_initialization(self) -> None:
        """Verify Decision node defaults and attributes."""
        d = Decision(text="Is Valid?", width=20.0, height=16.0)
        assert d.text == "Is Valid?"
        assert d.width == 20.0
        assert d.height == 16.0
        assert d.shape_type == "decision"

    def test_terminal_initialization(self) -> None:
        """Verify Start and End terminal nodes."""
        s = Start("Begin")
        e = End("Finish")
        assert s.text == "Begin"
        assert s.shape_type == "start"
        assert s.r == 5.0
        assert e.text == "Finish"
        assert e.shape_type == "end"
        assert e.r == 5.0

    def test_data_initialization(self) -> None:
        """Verify Data parallelogram node."""
        d = Data("User Input", width=25.0, height=12.0)
        assert d.text == "User Input"
        assert d.shape_type == "data"
        assert d.width == 25.0

    def test_node_anchors_and_bounds(self) -> None:
        """Verify anchor coordinates relative to placed center."""
        flow = FlowDiagram()
        node = flow.add(Process("Task", width=20.0, height=10.0), xy=(50.0, 50.0))

        assert node.center == (50.0, 50.0)
        assert node.left == (40.0, 50.0)
        assert node.right == (60.0, 50.0)
        assert node.top == (50.0, 55.0)
        assert node.bottom == (50.0, 45.0)

        min_x, min_y, max_x, max_y = node.get_bounds()
        assert min_x == -10.0
        assert max_x == 10.0
        assert min_y == -5.0
        assert max_y == 5.0


class TestJunction:
    """Unit tests for Junction element."""

    def test_junction_properties(self) -> None:
        """Verify Junction coordinate and anchor consistency."""
        flow = FlowDiagram()
        j = flow.junction(xy=(30.0, 40.0))

        assert j.xy == (30.0, 40.0)
        assert j.center == (30.0, 40.0)
        assert j.top == (30.0, 40.0)
        assert j.bottom == (30.0, 40.0)
        assert j.left == (30.0, 40.0)
        assert j.right == (30.0, 40.0)
        assert j.get_size() == (0.0, 0.0)
        assert j.get_bounds() == (0.0, 0.0, 0.0, 0.0)


class TestFlowEdge:
    """Unit tests for FlowEdge and routing."""

    def test_edge_validation(self) -> None:
        """Verify error raised on invalid parameters."""
        n1 = Process("A")
        n2 = Process("B")

        with pytest.raises(ValueError, match="Invalid arrow"):
            FlowEdge(start=n1, end=n2, arrow="-->")

        with pytest.raises(ValueError, match="Invalid routing"):
            FlowEdge(start=n1, end=n2, routing=cast(Any, "curved"))

        with pytest.raises(ValueError, match="Invalid start_side"):
            FlowEdge(start=n1, end=n2, start_side=cast(Any, "center"))

    def test_edge_waypoints_and_add_point(self) -> None:
        """Verify waypoints specification and branching add_point."""
        flow = FlowDiagram()
        p1 = flow.add(Process("P1"), xy=(10.0, 50.0))
        p2 = flow.add(Process("P2"), xy=(80.0, 50.0))

        edge = p1.connect(p2)
        edge.via((30.0, 70.0), (60.0, 70.0))
        assert edge.waypoints == [(30.0, 70.0), (60.0, 70.0)]

        j = edge.add_point((45.0, 70.0))
        assert isinstance(j, Junction)
        assert j.xy == (45.0, 70.0)
        assert (45.0, 70.0) in edge.waypoints

    def test_edge_default_arrow_to_junction(self) -> None:
        """Verify connecting to a Junction defaults to arrow='-' while connecting to node defaults to '->'."""
        flow = FlowDiagram()
        dec = flow.add(Decision("Branch?"), xy=(50.0, 80.0))
        j = flow.junction(xy=(50.0, 60.0))
        proc = flow.add(Process("Task"), xy=(30.0, 40.0))

        e1 = dec.connect(j)
        assert e1.arrow == "-"

        e2 = j.connect(proc)
        assert e2.arrow == "->"

    def test_node_fork(self) -> None:
        """Verify fork branching method."""
        flow = FlowDiagram()
        root = flow.add(Decision("Branch"), xy=(50.0, 80.0))
        b1 = flow.add(Process("Path 1"), xy=(30.0, 40.0))
        b2 = flow.add(Process("Path 2"), xy=(70.0, 40.0))

        fork_edges = root.fork([b1, b2], at_x=50.0, at_y=60.0)
        assert len(fork_edges) == 3  # root -> junction, junction -> b1, junction -> b2
        assert len(flow.edges) == 3


class TestSwimlane:
    """Unit tests for Swimlane (Lane)."""

    def test_lane_defaults(self) -> None:
        """Verify Lane initialization."""
        lane = Lane(title="DevOps", size=40.0)
        assert lane.title == "DevOps"
        assert lane.size == 40.0
        assert lane.header_size == 6.0

    def test_diagram_add_lane_aliases(self) -> None:
        """Verify add_lane with width and height aliases."""
        flow_v = FlowDiagram(lane_orientation="vertical")
        lane1 = flow_v.add_lane("Client", width=35.0)
        assert lane1.size == 35.0

        flow_h = FlowDiagram(lane_orientation="horizontal")
        lane2 = flow_h.add_lane("Server", height=45.0)
        assert lane2.size == 45.0


class TestFlowDiagramIntegration:
    """Integration and rendering tests for FlowDiagram."""

    def test_basic_flow_render(self) -> None:
        """Verify basic flow diagram rendering and file output."""
        canvas.initialize()

        flow = FlowDiagram(title="Basic Registration Flow")
        start = flow.add(Start("Start"), xy=(50.0, 90.0))
        input_data = flow.add(Data("User Info"), xy=(50.0, 75.0))
        decision = flow.add(Decision("Valid?"), xy=(50.0, 55.0))
        success = flow.add(Process("Create User"), xy=(30.0, 35.0))
        error = flow.add(Process("Show Error"), xy=(70.0, 55.0))
        end = flow.add(End("End"), xy=(30.0, 15.0))

        start.connect(input_data)
        input_data.connect(decision)
        decision.connect(success, label="Yes", start_side="bottom", end_side="top")
        decision.connect(error, label="No", start_side="right", end_side="left")
        error.connect(input_data, start_side="top", end_side="right")
        success.connect(end)

        flow.draw()

        with tempfile.TemporaryDirectory() as tmp_dir:
            out_file = Path(tmp_dir) / "basic_flow.png"
            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_swimlane_and_junction_flow_render(self) -> None:
        """Verify swimlane workflow rendering with junctions and custom styles."""
        canvas.initialize()

        flow = FlowDiagram(
            title="Cross-Functional Approval Workflow",
            width=100.0,
            height=100.0,
        )

        flow.add_lane("User", width=30.0)
        flow.add_lane("Manager", width=35.0)
        flow.add_lane("Finance", width=35.0)

        s = flow.add(Start("Submit"), xy=(15.0, 85.0))
        review = flow.add(Process("Review"), xy=(47.5, 85.0))
        decision = flow.add(Decision("Approve?"), xy=(47.5, 65.0))

        j = flow.junction(xy=(47.5, 50.0))
        decision.connect(j)

        reject = flow.add(Process("Reject Notification"), xy=(15.0, 50.0))
        pay = flow.add(Process("Disburse Funds"), xy=(82.5, 50.0))
        end = flow.add(End("Done"), xy=(82.5, 20.0))

        s.connect(review)
        review.connect(decision)
        j.connect(reject, label="No")
        j.connect(pay, label="Yes")
        pay.connect(end)

        flow.draw()

        with tempfile.TemporaryDirectory() as tmp_dir:
            out_file = Path(tmp_dir) / "swimlane_flow.png"
            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_horizontal_swimlane_render(self) -> None:
        """Verify horizontal swimlane workflow diagram."""
        canvas.initialize()

        flow = FlowDiagram(
            title="Horizontal Order Pipeline",
            lane_orientation="horizontal",
            width=100.0,
            height=60.0,
        )

        flow.add_lane("Storefront", height=30.0)
        flow.add_lane("Warehouse", height=30.0)

        order = flow.add(Start("New Order"), xy=(20.0, 45.0))
        pack = flow.add(Process("Pack Items"), xy=(50.0, 15.0))
        ship = flow.add(End("Ship Order"), xy=(80.0, 15.0))

        order.connect(pack, routing="orthogonal")
        pack.connect(ship)

        flow.draw()

        with tempfile.TemporaryDirectory() as tmp_dir:
            out_file = Path(tmp_dir) / "horizontal_flow.png"
            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0
