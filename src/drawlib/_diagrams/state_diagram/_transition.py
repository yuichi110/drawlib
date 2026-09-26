# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Transition edge model for State diagrams."""

from __future__ import annotations

from typing import TYPE_CHECKING

from drawlib._diagrams.state_diagram._types import LoopSide, PaddingType, RoutingType, Side

if TYPE_CHECKING:
    from drawlib._core.types import Style
    from drawlib._diagrams.state_diagram._diagram import StateDiagram
    from drawlib._diagrams.state_diagram._state_node import StateNodeBase


class StateTransition:
    """Represents a state transition edge connecting two states."""

    def __init__(
        self,
        start: StateNodeBase,
        end: StateNodeBase,
        label: str = "",
        event: str = "",
        guard: str = "",
        action: str = "",
        bend: float = 0.0,
        start_side: Side = "auto",
        end_side: Side = "auto",
        routing: RoutingType = "curved",
        style: Style | None = None,
        padding: PaddingType = 0.0,
        loop_side: LoopSide = "top",
        loop_width: float | None = None,
        loop_height: float | None = None,
        loop_ratio: float = 0.88,
        is_loop: bool = False,
    ) -> None:
        """Initialize StateTransition.

        Args:
            start: Source StateNode.
            end: Target StateNode.
            label: Optional full transition label string. Overrides event/guard/action if specified.
            event: Trigger event name (e.g. 'click', 'timeout').
            guard: Guard condition text (automatically formatted as '[guard]').
            action: Effect / action text (automatically formatted as '/ action').
            bend: Curvature amount for curved routing (0 is straight, positive curves outward).
            start_side: Attachment side on start state ('left', 'right', 'top', 'bottom', 'auto').
            end_side: Attachment side on end state ('left', 'right', 'top', 'bottom', 'auto').
            routing: Line path routing strategy ('curved', 'orthogonal', 'direct').
            style: Optional Style object overriding edge color, width, and dash style.
            padding: Distance offset between state boundary and arrow ends.
            loop_side: Attachment side for self-loop ('top', 'bottom', 'left', 'right', etc.).
            loop_width: Optional width of loop ellipse.
            loop_height: Optional height of loop ellipse.
            loop_ratio: Arc coverage ratio along ellipse circumference (default 0.88).
            is_loop: Whether this transition was created as an explicit self-loop.
        """
        valid_sides = {
            "left",
            "right",
            "top",
            "bottom",
            "auto",
            "top_right",
            "top_left",
            "bottom_right",
            "bottom_left",
        }
        if start_side not in valid_sides:
            raise ValueError(f"Invalid start_side: {start_side!r}. Must be one of {sorted(valid_sides)}.")
        if end_side not in valid_sides:
            raise ValueError(f"Invalid end_side: {end_side!r}. Must be one of {sorted(valid_sides)}.")

        valid_routings = {"curved", "orthogonal", "direct"}
        if routing not in valid_routings:
            raise ValueError(f"Invalid routing: {routing!r}. Must be one of {sorted(valid_routings)}.")

        self.start = start
        self.end = end
        self.label = label
        self.event = event
        self.guard = guard
        self.action = action
        self.bend = float(bend)
        self.start_side: Side = start_side
        self.end_side: Side = end_side
        self.routing: RoutingType = routing
        self.style = style
        self.padding: PaddingType = padding
        self.loop_side: LoopSide = loop_side
        self.loop_width = float(loop_width) if loop_width is not None else None
        self.loop_height = float(loop_height) if loop_height is not None else None
        self.loop_ratio = float(loop_ratio)
        self.is_loop = is_loop or (start is end)

        self._diagram: StateDiagram | None = None

    @property
    def is_self_transition(self) -> bool:
        """Check whether this transition loops back to the same state."""
        return self.is_loop or (self.start is self.end)

    @property
    def effective_label(self) -> str:
        """Get the formatted label text displayed along the transition line."""
        if self.label:
            return self.label

        parts: list[str] = []
        if self.event:
            parts.append(self.event)
        if self.guard:
            parts.append(f"[{self.guard}]")
        if self.action:
            parts.append(f"/ {self.action}")

        return " ".join(parts)
