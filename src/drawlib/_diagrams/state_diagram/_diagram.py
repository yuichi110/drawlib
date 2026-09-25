# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Diagram container for State diagrams."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

import drawlib._diagrams.state_diagram._renderer as _renderer_module
from drawlib._diagrams.state_diagram._state_node import State, StateNodeBase
from drawlib._diagrams.state_diagram._transition import StateTransition

if TYPE_CHECKING:
    from drawlib._core.l3_styles import Style

NodeT = TypeVar("NodeT", bound=StateNodeBase)


class StateDiagram:
    """Top-level container managing states, transitions, and layout for State diagrams."""

    def __init__(
        self,
        title: str = "",
        style: Style | None = None,
        width: float | None = None,
        height: float | None = None,
        margin: float = 5.0,
    ) -> None:
        """Initialize StateDiagram.

        Args:
            title: Optional title displayed above the diagram.
            style: Optional Style overriding diagram background.
            width: Optional fixed canvas width. If None, auto-calculated from content.
            height: Optional fixed canvas height. If None, auto-calculated from content.
            margin: Outer margin padding surrounding all states (default: 5.0).
        """
        self.title = title
        self.style = style
        self.custom_width = float(width) if width is not None else None
        self.custom_height = float(height) if height is not None else None
        self.margin = float(margin)

        self.states: list[StateNodeBase] = []
        self.transitions: list[StateTransition] = []

    def add(
        self,
        item: NodeT,
        xy: tuple[float, float] = (0.0, 0.0),
        width: float | None = None,
        height: float | None = None,
        style: Style | None = None,
    ) -> NodeT:
        """Add a State or pseudo-state to the diagram at the specified center coordinate.

        Args:
            item: StateNodeBase instance (State, InitialState, FinalState, ChoiceState, ForkJoinState).
            xy: Center placement coordinate (cx, cy).
            width: Optional width override for the state.
            height: Optional height override for the state.
            style: Optional Style override for the state.

        Returns:
            NodeT: The added state node instance for convenient chaining or assignment.
        """
        item._local_xy = (float(xy[0]), float(xy[1]))
        item._diagram = self

        if width is not None:
            item.width = float(width)
            if isinstance(item, State):
                item.custom_width = True
        if height is not None:
            item.height = float(height)
            if isinstance(item, State):
                item.custom_height = True
        if style is not None:
            item.style = style if item.style is None else item.style.merge(style)

        if item not in self.states:
            self.states.append(item)
        return item

    def add_transition(self, trans: StateTransition) -> StateTransition:
        """Register a StateTransition with this diagram.

        Args:
            trans: StateTransition instance to register.

        Returns:
            StateTransition: The registered transition.
        """
        trans._diagram = self
        if trans not in self.transitions:
            self.transitions.append(trans)
        return trans

    def get_bounds(self) -> tuple[float, float, float, float]:
        """Compute the enclosing bounding box [min_x, min_y, max_x, max_y] of all registered states.

        Returns:
            Tuple of (min_x, min_y, max_x, max_y).
        """
        if not self.states:
            return (0.0, 0.0, 0.0, 0.0)

        min_x = float("inf")
        min_y = float("inf")
        max_x = float("-inf")
        max_y = float("-inf")

        for s in self.states:
            cx, cy = s._local_xy
            half_w = s.effective_width / 2.0
            half_h = s.effective_height / 2.0
            min_x = min(min_x, cx - half_w)
            min_y = min(min_y, cy - half_h)
            max_x = max(max_x, cx + half_w)
            max_y = max(max_y, cy + half_h)

        for t in self.transitions:
            if t.is_loop and t.start is not None:
                s = t.start
                cx, cy = s._local_xy
                half_w = s.effective_width / 2.0
                half_h = s.effective_height / 2.0
                w_l = t.loop_width if t.loop_width is not None else min(10.0, s.effective_width * 0.5)
                h_l = t.loop_height if t.loop_height is not None else min(10.0, s.effective_height * 0.5)
                side = t.loop_side or "top"
                if "top" in side:
                    max_y = max(max_y, cy + half_h + h_l + 3.0)
                if "bottom" in side:
                    min_y = min(min_y, cy - half_h - h_l - 3.0)
                if "right" in side:
                    max_x = max(max_x, cx + half_w + w_l + 3.0)
                if "left" in side:
                    min_x = min(min_x, cx - half_w - w_l - 3.0)

        return (min_x, min_y, max_x, max_y)

    def get_size(self) -> tuple[float, float]:
        """Compute overall dimensions (width, height) of the diagram.

        Returns:
            Tuple of (width, height).
        """
        if self.custom_width is not None and self.custom_height is not None:
            return (self.custom_width, self.custom_height)

        min_x, min_y, max_x, max_y = self.get_bounds()
        w = max_x - min_x + self.margin * 2.0
        h = max_y - min_y + self.margin * 2.0

        if self.custom_width is not None:
            w = self.custom_width
        if self.custom_height is not None:
            h = self.custom_height

        return (max(w, 10.0), max(h, 10.0))

    def draw(self, xy: tuple[float, float] = (0.0, 0.0)) -> None:
        """Render the complete state diagram onto the canvas anchored at coordinate xy.

        Args:
            xy: Base canvas placement coordinate (x, y).
        """
        _renderer_module.draw_state_diagram(self, xy)
