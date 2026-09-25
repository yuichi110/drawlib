# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for drawlib.diagrams.state_diagram."""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any, cast

import pytest

from drawlib import canvas
from drawlib._core.l3_styles import Colors, Style
from drawlib.diagrams.state_diagram import (
    ChoiceState,
    FinalState,
    ForkJoinState,
    InitialState,
    State,
    StateAction,
    StateDiagram,
    StateTransition,
)


class TestStateNode:
    """Unit tests for State model and shape options."""

    def test_state_default_initialization(self) -> None:
        """Verify default initialization of State."""
        state = State(name="Idle")
        assert state.name == "Idle"
        assert state.shape == "box"
        assert state.r == 2.0
        assert state.effective_width == 22.0
        assert state.effective_height == 12.0
        assert len(state.actions) == 0
        assert state.xy == (0.0, 0.0)
        assert state.center == (0.0, 0.0)

    def test_state_shapes(self) -> None:
        """Verify State initialization for different shapes."""
        oval = State(name="Running", shape="oval")
        assert oval.shape == "oval"
        assert oval.effective_width == 24.0
        assert oval.effective_height == 13.0

        circle = State(name="S0", shape="circle")
        assert circle.shape == "circle"
        assert circle.effective_width == 16.0
        assert circle.effective_height == 16.0

        double_circle = State(name="Accepted", shape="double_circle")
        assert double_circle.shape == "double_circle"
        assert double_circle.effective_width == 16.0
        assert double_circle.effective_height == 16.0

        text_only = State(name="Note", shape="text_only")
        assert text_only.shape == "text_only"
        assert text_only.effective_width == 16.0
        assert text_only.effective_height == 8.0

    def test_state_invalid_shape(self) -> None:
        """Verify invalid shape raises ValueError."""
        with pytest.raises(ValueError, match="Invalid shape"):
            State(name="Bad", shape=cast(Any, "triangle"))

    def test_state_size_shorthand(self) -> None:
        """Verify size tuple override."""
        state = State(name="Custom", size=(30.0, 18.0))
        assert state.width == 30.0
        assert state.height == 18.0
        assert state.effective_width == 30.0
        assert state.effective_height == 18.0

    def test_state_actions(self) -> None:
        """Verify entry, do, exit actions and custom actions."""
        state = State(
            name="Processing",
            entry="init_buffers()",
            do="stream_data()",
            exit="cleanup()",
        )
        assert len(state.actions) == 3
        assert state.actions[0] == StateAction(kind="entry", action="init_buffers()")
        assert state.actions[0].display_text == "entry / init_buffers()"
        assert state.actions[1] == StateAction(kind="do", action="stream_data()")
        assert state.actions[2] == StateAction(kind="exit", action="cleanup()")

        # Chaining add_action
        state.add_action("custom", "notify_observers()")
        assert len(state.actions) == 4
        assert state.actions[3].display_text == "custom / notify_observers()"

        # Effective height expands for actions
        assert state.effective_height > 12.0

    def test_state_get_bounds_and_anchors(self) -> None:
        """Verify bounding box and border anchors."""
        state = State(name="Test", width=20.0, height=10.0)
        state._local_xy = (10.0, 20.0)

        bounds = state.get_bounds()
        assert bounds == (-10.0, -5.0, 10.0, 5.0)

        assert state.get_anchor("top") == (10.0, 25.0)
        assert state.get_anchor("bottom") == (10.0, 15.0)
        assert state.get_anchor("left") == (0.0, 20.0)
        assert state.get_anchor("right") == (20.0, 20.0)


class TestPseudoStates:
    """Unit tests for InitialState, FinalState, ChoiceState, and ForkJoinState."""

    def test_initial_state(self) -> None:
        """Verify InitialState properties."""
        init = InitialState(name="start", radius=2.0)
        assert init.radius == 2.0
        assert init.effective_width == 4.0
        assert init.effective_height == 4.0

    def test_final_state(self) -> None:
        """Verify FinalState properties."""
        final = FinalState(radius=2.5)
        assert final.radius == 2.5
        assert final.effective_width == 5.0
        assert final.effective_height == 5.0

    def test_choice_state(self) -> None:
        """Verify ChoiceState diamond properties."""
        choice = ChoiceState(name="check", size=6.0)
        assert choice.size == 6.0
        assert choice.effective_width == 6.0
        assert choice.effective_height == 6.0

    def test_fork_join_state(self) -> None:
        """Verify ForkJoinState horizontal and vertical orientation."""
        horiz = ForkJoinState(orientation="horizontal", length=20.0, thickness=2.0)
        assert horiz.effective_width == 20.0
        assert horiz.effective_height == 2.0

        vert = ForkJoinState(orientation="vertical", length=25.0, thickness=3.0)
        assert vert.effective_width == 3.0
        assert vert.effective_height == 25.0

    def test_fork_join_invalid_orientation(self) -> None:
        """Verify invalid orientation raises ValueError."""
        with pytest.raises(ValueError, match="Invalid orientation"):
            ForkJoinState(orientation=cast(Any, "diagonal"))


class TestStateTransition:
    """Unit tests for StateTransition edge model."""

    def test_transition_effective_label(self) -> None:
        """Verify formatted transition labels."""
        s1 = State("A")
        s2 = State("B")

        # Full label overrides
        t1 = StateTransition(start=s1, end=s2, label="Direct Label")
        assert t1.effective_label == "Direct Label"

        # Structured event, guard, action
        t2 = StateTransition(start=s1, end=s2, event="submit", guard="valid", action="save()")
        assert t2.effective_label == "submit [valid] / save()"

        # Partial combinations
        t3 = StateTransition(start=s1, end=s2, event="tick")
        assert t3.effective_label == "tick"

        t4 = StateTransition(start=s1, end=s2, guard="x > 0")
        assert t4.effective_label == "[x > 0]"

        t5 = StateTransition(start=s1, end=s2, action="count += 1")
        assert t5.effective_label == "/ count += 1"

    def test_self_transition(self) -> None:
        """Verify is_self_transition detection."""
        s1 = State("Loop")
        s2 = State("Other")
        t_self = StateTransition(start=s1, end=s1)
        t_other = StateTransition(start=s1, end=s2)

        assert t_self.is_self_transition is True
        assert t_other.is_self_transition is False

    def test_loop_transition(self) -> None:
        """Verify self-loop transition properties."""
        s = State("LoopState")
        t = s.loop(side="right", label="tick", width=14.0, height=8.0, ratio=0.85)
        assert t.is_self_transition is True
        assert t.is_loop is True
        assert t.loop_side == "right"
        assert t.loop_width == 14.0
        assert t.loop_height == 8.0
        assert t.loop_ratio == 0.85
        assert t.effective_label == "tick"

    def test_loop_defaults(self) -> None:
        """Verify default parameters for self-loop."""
        s = State("DefaultLoop")
        t = s.loop()
        assert t.is_self_transition is True
        assert t.loop_side == "top"
        assert t.loop_width is None
        assert t.loop_height is None
        assert t.loop_ratio == 0.88

    def test_to_self_delegates_to_loop(self) -> None:
        """Verify state.to(state) creates a self-loop transition."""
        s = State("SelfTo")
        t = s.to(s, event="retry", start_side="bottom")
        assert t.is_self_transition is True
        assert t.loop_side == "bottom"
        assert t.effective_label == "retry"

    def test_invalid_parameters(self) -> None:
        """Verify invalid side and routing values raise ValueError."""
        s1 = State("A")
        s2 = State("B")

        with pytest.raises(ValueError, match="Invalid start_side"):
            StateTransition(start=s1, end=s2, start_side=cast(Any, "center"))

        with pytest.raises(ValueError, match="Invalid end_side"):
            StateTransition(start=s1, end=s2, end_side=cast(Any, "middle"))

        with pytest.raises(ValueError, match="Invalid routing"):
            StateTransition(start=s1, end=s2, routing=cast(Any, "zigzag"))


class TestStateDiagram:
    """Unit tests for StateDiagram container."""

    def test_diagram_add_and_connect(self) -> None:
        """Verify adding nodes and connecting them with .to()."""
        sd = StateDiagram(title="Test FSM")

        s1 = sd.add(State("Start"), xy=(10.0, 20.0))
        s2 = sd.add(State("End"), xy=(40.0, 20.0))

        assert len(sd.states) == 2
        assert s1.xy == (10.0, 20.0)
        assert s2.xy == (40.0, 20.0)

        edge = s1.to(s2, event="go", bend=0.2)
        assert len(sd.transitions) == 1
        assert edge.start is s1
        assert edge.end is s2
        assert edge.bend == 0.2
        assert edge.effective_label == "go"

    def test_diagram_bounds_and_size(self) -> None:
        """Verify diagram bounding box and canvas sizing."""
        sd = StateDiagram(margin=10.0)
        sd.add(State("A", width=20.0, height=10.0), xy=(0.0, 0.0))
        sd.add(State("B", width=20.0, height=10.0), xy=(50.0, 0.0))

        bounds = sd.get_bounds()
        # A: [-10, -5, 10, 5], B: [40, -5, 60, 5] -> min_x=-10, max_x=60, min_y=-5, max_y=5
        assert bounds == (-10.0, -5.0, 60.0, 5.0)

        # Width = (60 - (-10)) + 20 = 90; Height = (5 - (-5)) + 20 = 30
        w, h = sd.get_size()
        assert w == 90.0
        assert h == 30.0

    def test_diagram_custom_size(self) -> None:
        """Verify custom width and height override."""
        sd = StateDiagram(width=150.0, height=100.0)
        assert sd.get_size() == (150.0, 100.0)


class TestStateDiagramRendering:
    """Integration test verifying full visual rendering and file export."""

    def test_render_all_state_diagram_features(self) -> None:
        """Render a comprehensive state diagram exercising all shapes, pseudo-states, and transitions."""
        canvas.config(width=160, height=110)

        sd = StateDiagram(title="Turnstile & Auth FSM")

        # 1. Pseudo-states & States
        init = sd.add(InitialState(), xy=(20.0, 75.0))
        locked = sd.add(
            State(
                "Locked",
                shape="box",
                entry="lock_barrier()",
                do="blink_red_led()",
            ),
            xy=(55.0, 75.0),
        )
        unlocked = sd.add(
            State(
                "Unlocked",
                shape="box",
                entry="unlock_barrier()",
                do="green_led()",
                exit="chime()",
            ),
            xy=(115.0, 75.0),
        )

        # Automaton nodes (circle & double_circle)
        audit = sd.add(State("Audit", shape="oval"), xy=(55.0, 35.0))
        success = sd.add(
            State("Done", shape="double_circle", style=Style(shape_fill_color=Colors.Green)),
            xy=(115.0, 35.0),
        )
        final = sd.add(FinalState(), xy=(145.0, 35.0))

        # Branching pseudo-states
        choice = sd.add(ChoiceState(name="auth?"), xy=(85.0, 55.0))
        sync = sd.add(ForkJoinState(orientation="horizontal", length=18.0), xy=(85.0, 18.0))

        # 2. Transitions
        # Initial -> Locked
        init.to(locked)

        # Locked -> Choice -> Unlocked
        locked.to(choice, event="coin")
        choice.to(unlocked, guard="valid_card")
        choice.to(locked, guard="invalid", bend=0.3)

        # Bidirectional curved transitions between Locked and Unlocked
        unlocked.to(locked, event="push", bend=0.3)

        # Self-transition on Locked (invalid action)
        locked.to(locked, event="push", action="alarm()")

        # Transitions to Audit and Done
        locked.to(audit, event="admin_key", routing="orthogonal")
        unlocked.to(success, event="pass_through")
        success.to(final)
        locked.to(sync, event="shutdown")

        # Draw diagram
        sd.draw(xy=(0.0, 0.0))

        # Verify export to temporary image file
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_file = Path(tmp_dir) / "state_diagram_test.png"
            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0
