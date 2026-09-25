# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for drawlib.diagrams.sequence."""

import tempfile
from pathlib import Path

from PIL import Image

from drawlib import canvas
from drawlib._core.l3_styles import Colors, Style
from drawlib.diagrams.sequence import (
    Block,
    CustomIcon,
    GcpIcon,
    Message,
    Note,
    Participant,
    ParticipantGroup,
    PhosphorIcon,
    SequenceDiagram,
)


class TestSequenceParticipantAndMessage:
    """Test suite for Participant and Message components."""

    def test_participant_creation(self) -> None:
        """Verify Participant creation and properties."""
        p1 = Participant("Web Server", icon=PhosphorIcon.BROWSER, icon_size=10.0)
        assert p1.text == "Web Server"
        assert p1.icon == PhosphorIcon.BROWSER
        assert p1.icon_size == 10.0

        p2 = Participant("Auth Service")
        assert isinstance(p2, Participant)
        assert p2.text == "Auth Service"

    def test_participant_fixed_x(self) -> None:
        """Verify explicit x coordinate pinning on participant."""
        p = Participant("Database")
        p.set_x(45.0)
        assert p._fixed_x == 45.0

    def test_message_creation_request_and_reply(self) -> None:
        """Verify Message creation, request (solid), and reply (dashed) semantics."""
        p1 = Participant("Client")
        p2 = Participant("Server")

        # Request: solid line
        m1 = p1.request(p2, "GET /data")
        assert isinstance(m1, Message)
        assert m1.source is p1
        assert m1.target is p2
        assert m1.label == "GET /data"
        assert m1.is_reply is False
        assert m1.is_async is False
        assert m1.arrow == "->"

        # Reply: dashed line
        m2 = p2.reply(p1, "200 OK")
        assert m2.source is p2
        assert m2.target is p1
        assert m2.label == "200 OK"
        assert m2.is_reply is True

    def test_message_async_and_bidirectional(self) -> None:
        """Verify asynchronous messages and bidirectional connection streams."""
        p1 = Participant("Publisher")
        p2 = Participant("Subscriber")

        async_msg = p1.request(p2, "Notify", is_async=True)
        assert async_msg.is_async is True

        stream_msg = p1.connect(p2, "WebSocket Stream", arrow="<->")
        assert stream_msg.arrow == "<->"
        assert stream_msg.is_reply is False

    def test_message_self_call(self) -> None:
        """Verify self-call identification."""
        p = Participant("Service")
        self_msg = p.request(p, "Internal Validation")
        assert self_msg.is_self_call is True

    def test_message_fluent_setters(self) -> None:
        """Verify Message fluent setter methods."""
        p1 = Participant("A")
        p2 = Participant("B")
        m = Message(p1, p2)

        m.set_label("Ping").set_reply(True).set_async(True).set_arrow("<->").set_padding(2.0)
        assert m.label == "Ping"
        assert m.is_reply is True
        assert m.is_async is True
        assert m.arrow == "<->"
        assert m.padding == 2.0


class TestSequenceNoteAndBlock:
    """Test suite for Note annotations and Block context managers."""

    def test_note_creation(self) -> None:
        """Verify Note initialization on single and multiple participants."""
        p1 = Participant("A")
        p2 = Participant("B")

        note1 = Note("User credentials checked", on=p1, pos="right")
        assert note1.text == "User credentials checked"
        assert note1.on is p1
        assert note1.pos == "right"

        note2 = Note("Span over both", over=[p1, p2], pos="over")
        assert note2.over == [p1, p2]
        assert note2.pos == "over"

    def test_block_context_manager(self) -> None:
        """Verify Block context manager records boundary events in Diagram."""
        d = SequenceDiagram()
        client = d.add(Participant("Client"))
        server = d.add(Participant("Server"))

        with d.loop("Retry 3 times") as loop_block:
            assert isinstance(loop_block, Block)
            client.request(server, "Ping")
            server.reply(client, "Timeout")

        # Events list should contain block_start, 2 messages, block_end
        events = d.events
        assert len(events) == 4
        assert isinstance(events[0], tuple) and events[0][0] == "block_start"
        assert isinstance(events[1], Message)
        assert isinstance(events[2], Message)
        assert isinstance(events[3], tuple) and events[3][0] == "block_end"

    def test_participant_group(self) -> None:
        """Verify ParticipantGroup clustering box."""
        d = SequenceDiagram()
        group = d.add_group(ParticipantGroup("Internal Cluster", padding=6.0))
        p1 = group.add(Participant("Service Alpha"))
        p2 = group.add(Participant("Service Beta"))

        assert p1 in group.participants
        assert p2 in group.participants
        assert p1 in d.participants
        assert p2 in d.participants


class TestSequenceDiagramLifecycle:
    """Test suite for Diagram container lifecycle and state tracking."""

    def test_autonumbering(self) -> None:
        """Verify automatic sequential numbering of message arrows."""
        d = SequenceDiagram(autonumber=True)
        p1 = d.add(Participant("A"))
        p2 = d.add(Participant("B"))

        m1 = p1.request(p2, "First")
        m2 = p2.reply(p1, "Second")
        m3 = p1.request(p2, "Third")

        assert m1.number == 1
        assert m2.number == 2
        assert m3.number == 3

    def test_activations(self) -> None:
        """Verify participant lifeline activation tracking."""
        d = SequenceDiagram()
        client = d.add(Participant("Client"))
        server = d.add(Participant("Server"))

        client.request(server, "Request")
        server.activate()
        server.request(server, "Processing")
        server.reply(client, "Response")
        server.deactivate()

        assert len(server._activations) == 1
        start, end = server._activations[0]
        assert start is not None
        assert end is not None
        assert end > start


class TestSequenceDiagramRenderingEndToEnd:
    """End-to-end rendering and canvas integration tests."""

    def test_render_full_sequence_diagram(self) -> None:
        """Verify full sequence diagram rendering to canvas and saving as PNG."""
        canvas.initialize()

        d = SequenceDiagram(title="OAuth2 Authentication Flow", autonumber=True)

        user = d.add(Participant("User", icon=PhosphorIcon.USER, icon_size=8.0))
        client = d.add(Participant("SPA Client", icon=PhosphorIcon.BROWSER, icon_size=8.0))
        auth = d.add(Participant("Auth Server", icon=GcpIcon.CLOUD_RUN, icon_size=8.0))
        db = d.add(Participant("Database", icon=GcpIcon.CLOUD_SQL, icon_size=8.0))

        user.request(client, "Click Login")
        client.request(auth, "POST /oauth/token")
        auth.activate()

        auth.request(auth, "Validate Client Secret")
        auth.note("JWT expiry: 3600s", pos="right")

        with d.alt("Valid Credentials"):
            auth.request(db, "Lookup User")
            db.reply(auth, "User Profile")
            auth.reply(client, "200 OK (Access Token)")
        with d.else_("Invalid Credentials"):
            auth.reply(client, "401 Unauthorized")

        auth.deactivate()
        client.reply(user, "Render Dashboard")

        # Bidirectional persistent session
        client.connect(auth, "WebSocket Keep-Alive", arrow="<->")

        d.draw(xy=(5.0, 5.0))

        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "test_sequence_diagram.png"
            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_with_custom_icon_and_groups(self) -> None:
        """Verify rendering with ParticipantGroup, CustomIcon, and custom style."""
        canvas.initialize()

        pil_img = Image.new("RGBA", (64, 64), (80, 140, 220, 255))
        custom_icon = CustomIcon(pil_img)

        d = SequenceDiagram(title="Microservices Event Stream")

        backend = d.add_group(
            ParticipantGroup(
                title="Backend VPC",
                style=Style(
                    shape_fill_color=(240, 245, 255, 0.5), shape_line_color=Colors.Gray, shape_line_style="dashed"
                ),
            )
        )
        api = backend.add(Participant("API Gateway", icon=custom_icon, icon_size=8.0))
        worker = backend.add(Participant("Worker Pod", icon=PhosphorIcon.CPU, icon_size=8.0))

        client = d.add(Participant("External Client", icon=PhosphorIcon.GLOBE, icon_size=8.0))

        client.request(api, "Enqueue Task")
        api.request(worker, "Dispatch Job", is_async=True)
        worker.reply(api, "Ack", is_async=True)
        api.reply(client, "202 Accepted")

        d.draw()

        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "test_sequence_groups.png"
            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0
