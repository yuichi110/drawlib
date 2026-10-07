# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for unified component lifecycle across all 6 diagram types."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from drawlib._core.l4_canvas import canvas
from drawlib.diagrams.architecture import ArchitectureDiagram, Junction, Node, NodeGroup, PhosphorIcon
from drawlib.diagrams.class_diagram import ClassDiagram, ClassNode
from drawlib.diagrams.er import Entity, ERDiagram
from drawlib.diagrams.flow import Decision, End, FlowDiagram, Process, Start
from drawlib.diagrams.sequence import Participant, ParticipantGroup, SequenceDiagram
from drawlib.diagrams.state import ChoiceState, FinalState, ForkJoinState, InitialState, State, StateDiagram
from drawlib.styles import Styles


class TestArchitectureDiagramLifecycle:
    """Lifecycle tests for ArchitectureDiagram (show, mutate, scale)."""

    def test_show_and_connected_edge_auto_hide(self) -> None:
        """Verify show=False preserves size and hides nodes, groups, junctions, and dangling pass-throughs."""
        canvas.clear()
        d = ArchitectureDiagram(
            node_style=Styles.Neutral,
            edge_style=Styles.Primary,
            node_text_style=Styles.Dark,
            edge_text_style=Styles.Dark,
        )
        vpc = d.add(NodeGroup("VPC", width=70.0, height=50.0), (50.0, 50.0))
        n1 = vpc.add(Node("API", icon=PhosphorIcon.CLOUD), (-20.0, 0.0))
        j = d.add(Junction((50.0, 50.0)), (50.0, 50.0))
        n2 = vpc.add(Node("DB1", icon=PhosphorIcon.DATABASE), (20.0, 12.0))
        n3 = vpc.add(Node("DB2", icon=PhosphorIcon.DATABASE), (20.0, -12.0))
        e1 = d.connect(n1, j, label="req", arrow="-")
        e2 = d.connect(j, n2, label="sql1")
        e3 = d.connect(j, n3, label="sql2")

        full_size = d.get_size()
        d.draw()
        full_artists = len(canvas._artists)
        assert full_artists > 0

        # Hide n2 -> n2 and e2 should be skipped, but e1 and e3 remain visible; size remains identical
        canvas.clear()
        n2.show = False
        assert d.get_size() == full_size
        d.draw()
        partial_artists = len(canvas._artists)
        assert 0 < partial_artists < full_artists

        # Hide n3 -> now all outgoing edges of j (e2, e3) are hidden, so dangling pass-through e1 is auto-hidden!
        canvas.clear()
        n3.show = False
        d.draw()
        both_targets_hidden_artists = len(canvas._artists)
        assert 0 < both_targets_hidden_artists < partial_artists

        # Explicitly hiding j does not change artist count since e1 was already auto-hidden as a dangling stem
        canvas.clear()
        j.show = False
        d.draw()
        assert len(canvas._artists) == both_targets_hidden_artists

        # Hide all
        canvas.clear()
        vpc.show = False
        n1.show = False
        e1.show = False
        e2.show = False
        e3.show = False
        d.draw()
        assert len(canvas._artists) == 0

    def test_waypoints_included_in_get_size(self) -> None:
        """Verify edge waypoints are included in ArchitectureDiagram.get_size() bounding box."""
        d = ArchitectureDiagram(
            node_style=Styles.Neutral,
            edge_style=Styles.Primary,
            node_text_style=Styles.Dark,
            edge_text_style=Styles.Dark,
        )
        n1 = d.add(Node("A"), (20.0, 20.0))
        n2 = d.add(Node("B"), (40.0, 20.0))
        size_no_waypoints = d.get_size()

        d.connect(n1, n2).via((30.0, 90.0))
        size_with_waypoints = d.get_size()
        assert size_with_waypoints[1] > size_no_waypoints[1]

    def test_mutate_and_scale(self) -> None:
        """Verify mutating node/edge styles and drawing with xy and scale."""
        canvas.clear()
        d = ArchitectureDiagram(
            node_style=Styles.Neutral,
            edge_style=Styles.Primary,
            node_text_style=Styles.Dark,
            edge_text_style=Styles.Dark,
        )
        n1 = d.add(Node("Service A", show=False), (20.0, 30.0), show=True)
        n2 = d.add(Node("Service B"), (60.0, 30.0))
        edge = n1.connect(n2, label="v1", show=True)

        assert n1.show is True
        assert edge.show is True

        n1.style = Styles.PrimaryFlat
        n1.text = "Service A (Active)"
        edge.label = "v2"

        d.draw(xy=(10.0, 15.0), scale=0.5)
        assert len(canvas._artists) > 0

        with pytest.raises((ValueError, ValidationError)):
            d.draw(scale=0.0)


class TestFlowDiagramLifecycle:
    """Lifecycle tests for FlowDiagram (show, mutate, scale)."""

    def test_show_and_swimlane_stability(self) -> None:
        """Verify show=False preserves swimlane layout and hides nodes, lanes, and incident edges."""
        canvas.clear()
        flow = FlowDiagram(
            node_style=Styles.Neutral,
            edge_style=Styles.Primary,
            edge_text_style=Styles.Dark,
        )
        lane1 = flow.add_lane("Lane 1", width=40.0)
        lane2 = flow.add_lane("Lane 2", width=40.0, show=True)

        s = flow.add(Start("Start"), (20.0, 70.0))
        p = flow.add(Process("Step 1"), (20.0, 45.0))
        dec = flow.add(Decision("OK?"), (60.0, 45.0))
        j = flow.junction((60.0, 28.0))
        e_node = flow.add(End("Done"), (60.0, 12.0))

        s.connect(p)
        p.connect(dec, label="check")
        dec.connect(j)
        j.connect(e_node)

        full_size = flow.get_size()
        flow.draw()
        full_count = len(canvas._artists)

        # Hide Decision node -> edges connected to dec are also hidden, size unchanged
        canvas.clear()
        dec.show = False
        assert flow.get_size() == full_size
        flow.draw()
        dec_hidden_count = len(canvas._artists)
        assert 0 < dec_hidden_count < full_count

        # Hide lane2 and remaining nodes
        canvas.clear()
        lane1.show = False
        lane2.show = False
        s.show = False
        p.show = False
        j.show = False
        e_node.show = False
        flow.draw()
        assert len(canvas._artists) == 0

    def test_scale_validation(self) -> None:
        """Verify FlowDiagram.draw scale parameter and validation."""
        canvas.clear()
        flow = FlowDiagram(
            node_style=Styles.Neutral,
            edge_style=Styles.Primary,
            edge_text_style=Styles.Dark,
        )
        s = flow.add(Start("Go"), (20.0, 20.0))
        e = flow.add(End("Stop"), (50.0, 20.0))
        flow.connect(s, e)
        flow.draw(xy=(5.0, 5.0), scale=0.6)
        assert len(canvas._artists) > 0

        with pytest.raises(ValidationError):
            flow.draw(scale=-0.5)


class TestSequenceDiagramLifecycle:
    """Lifecycle tests for SequenceDiagram (show, mutate, scale)."""

    def test_show_preserves_timeline_and_hides_dependents(self) -> None:
        """Verify hiding participants, messages, notes, groups, and blocks preserves timeline coordinates."""
        canvas.clear()
        seq = SequenceDiagram(
            node_style=Styles.Neutral,
            edge_style=Styles.Primary,
            edge_text_style=Styles.Dark,
        )
        client = seq.add(Participant("Client"))
        grp = seq.add(ParticipantGroup("Backend"))
        api = grp.add(Participant("API"))
        db = grp.add(Participant("DB"))

        m1 = seq.request(client, api, "GET /items")
        with seq.loop("retry") as loop_blk:
            m2 = seq.request(api, db, "SELECT *")
            m3 = seq.reply(db, api, "rows")
        n1 = seq.note("Cached", on=api)
        m4 = seq.reply(api, client, "200 OK")

        full_size = seq.get_size()
        seq.draw()
        full_count = len(canvas._artists)

        # Hide db participant -> m2 and m3 connected to db should auto-hide, size unchanged
        canvas.clear()
        db.show = False
        assert seq.get_size() == full_size
        seq.draw()
        db_hidden_count = len(canvas._artists)
        assert 0 < db_hidden_count < full_count

        # Hide note, m1, m4, loop_blk, group, and remaining participants
        canvas.clear()
        n1.show = False
        m1.show = False
        m2.show = False
        m3.show = False
        m4.show = False
        loop_blk.show = False
        grp.show = False
        client.show = False
        api.show = False
        seq.draw()
        assert len(canvas._artists) == 0

    def test_scale_render(self) -> None:
        """Verify SequenceDiagram.draw supports scale."""
        canvas.clear()
        seq = SequenceDiagram(
            node_style=Styles.Neutral,
            edge_style=Styles.Primary,
            edge_text_style=Styles.Dark,
        )
        a = seq.add(Participant("A"))
        b = seq.add(Participant("B"))
        seq.request(a, b, "ping")
        seq.draw(xy=(10.0, 10.0), scale=0.7)
        assert len(canvas._artists) > 0


class TestStateDiagramLifecycle:
    """Lifecycle tests for StateDiagram (show, mutate, scale)."""

    def test_show_and_transition_auto_hide(self) -> None:
        """Verify hiding states preserves bounds and hides connected transitions."""
        canvas.clear()
        sd = StateDiagram(
            node_style=Styles.Neutral,
            edge_style=Styles.Primary,
            edge_text_style=Styles.Dark,
        )
        init = sd.add(InitialState(), (15.0, 50.0))
        idle = sd.add(State("Idle", entry="reset()"), (40.0, 50.0))
        choice = sd.add(ChoiceState(), (65.0, 50.0))
        fork = sd.add(ForkJoinState(), (80.0, 50.0))
        final = sd.add(FinalState(), (95.0, 50.0))

        t1 = sd.connect(init, idle)
        t2 = sd.connect(idle, choice, event="start")
        t3 = sd.connect(choice, fork, guard="valid")
        t4 = sd.connect(fork, final)

        full_bounds = sd.get_bounds()
        sd.draw()
        full_count = len(canvas._artists)

        # Hide choice -> t2 and t3 should auto-hide
        canvas.clear()
        choice.show = False
        assert sd.get_bounds() == full_bounds
        sd.draw()
        partial_count = len(canvas._artists)
        assert 0 < partial_count < full_count

        # Hide all states
        canvas.clear()
        init.show = False
        idle.show = False
        fork.show = False
        final.show = False
        t1.show = False
        t2.show = False
        t3.show = False
        t4.show = False
        sd.draw()
        assert len(canvas._artists) == 0

    def test_scale_render(self) -> None:
        """Verify StateDiagram.draw supports scale."""
        canvas.clear()
        sd = StateDiagram(
            node_style=Styles.Neutral,
            edge_style=Styles.Primary,
            edge_text_style=Styles.Dark,
        )
        s1 = sd.add(State("S1"), (25.0, 30.0))
        s2 = sd.add(State("S2"), (65.0, 30.0))
        sd.connect(s1, s2, event="go")
        sd.draw(xy=(10.0, 10.0), scale=0.5)
        assert len(canvas._artists) > 0


class TestClassDiagramLifecycle:
    """Lifecycle tests for ClassDiagram (show, mutate, scale)."""

    def test_show_and_relationship_auto_hide(self) -> None:
        """Verify hiding ClassNode preserves bounds and hides connected ClassRelationship."""
        canvas.clear()
        cd = ClassDiagram(
            node_style=Styles.Neutral,
            edge_style=Styles.Primary,
            edge_text_style=Styles.Dark,
        )
        c1 = cd.add(ClassNode("Base"), (25.0, 50.0))
        c1.add_attribute("id", "int")
        c2 = cd.add(ClassNode("Derived"), (75.0, 50.0))
        c2.add_method("run", return_type="void")
        rel = cd.connect(c2, c1, "inheritance", label="extends")

        full_bounds = cd.get_bounds()
        cd.draw()
        full_count = len(canvas._artists)

        # Hide c2 -> c2 and rel are skipped, bounds preserved
        canvas.clear()
        c2.show = False
        assert cd.get_bounds() == full_bounds
        cd.draw()
        partial_count = len(canvas._artists)
        assert 0 < partial_count < full_count

        # Hide c1 as well
        canvas.clear()
        c1.show = False
        rel.show = False
        cd.draw()
        assert len(canvas._artists) == 0

        # Restore and draw with scale
        canvas.clear()
        c1.show = True
        c2.show = True
        rel.show = True
        cd.draw(xy=(10.0, 10.0), scale=0.6)
        assert len(canvas._artists) > 0


class TestERDiagramLifecycle:
    """Lifecycle tests for ERDiagram (show, mutate, scale)."""

    def test_show_and_relationship_auto_hide(self) -> None:
        """Verify hiding Entity preserves size and hides connected Relationship."""
        canvas.clear()
        er = ERDiagram(
            node_style=Styles.Neutral,
            edge_style=Styles.Primary,
            edge_text_style=Styles.Dark,
        )
        users = er.add(Entity("users"), (25.0, 50.0))
        users.add_column("id", "INT", pk=True)
        orders = er.add(Entity("orders"), (75.0, 50.0))
        orders.add_column("id", "INT", pk=True)
        orders.add_column("user_id", "INT", fk=True)
        rel = er.connect(users, orders, "1:*", label="places")

        full_size = er.get_size()
        er.draw()
        full_count = len(canvas._artists)

        # Hide orders -> orders and rel are skipped, size preserved
        canvas.clear()
        orders.show = False
        assert er.get_size() == full_size
        er.draw()
        partial_count = len(canvas._artists)
        assert 0 < partial_count < full_count

        # Hide users as well
        canvas.clear()
        users.show = False
        rel.show = False
        er.draw()
        assert len(canvas._artists) == 0

        # Restore and draw with scale
        canvas.clear()
        users.show = True
        orders.show = True
        rel.show = True
        er.draw(xy=(10.0, 10.0), scale=0.75)
        assert len(canvas._artists) > 0
