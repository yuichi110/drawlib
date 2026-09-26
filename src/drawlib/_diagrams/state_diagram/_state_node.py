# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""StateNode models for State diagrams."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import drawlib._diagrams.state_diagram._transition as _transition_module
from drawlib._diagrams.state_diagram._types import (
    LoopSide,
    PaddingType,
    RoutingType,
    ShapeType,
    Side,
    StateAction,
)

if TYPE_CHECKING:
    from drawlib._core.types import Style
    from drawlib._diagrams.state_diagram._diagram import StateDiagram
    from drawlib._diagrams.state_diagram._transition import StateTransition


class StateNodeBase:
    """Base class for all state nodes and pseudo-states in a StateDiagram."""

    def __init__(
        self,
        name: str = "",
        width: float = 20.0,
        height: float = 12.0,
        style: Style | None = None,
    ) -> None:
        """Initialize StateNodeBase.

        Args:
            name: Node label or state name.
            width: Width of the state shape.
            height: Height of the state shape.
            style: Optional Style object overriding visual appearance.
        """
        self.name = name
        self.width = float(width)
        self.height = float(height)
        self.style = style

        self._local_xy: tuple[float, float] = (0.0, 0.0)
        self._diagram: StateDiagram | None = None

    @property
    def xy(self) -> tuple[float, float]:
        """Get relative center coordinate (cx, cy) of the state node."""
        return self._local_xy

    @property
    def center(self) -> tuple[float, float]:
        """Get relative center coordinate (cx, cy) of the state node."""
        return self._local_xy

    @property
    def effective_width(self) -> float:
        """Get actual rendered width of the state node."""
        return self.width

    @property
    def effective_height(self) -> float:
        """Get actual rendered height of the state node."""
        return self.height

    def get_bounds(self) -> tuple[float, float, float, float]:
        """Get bounding box [min_x, min_y, max_x, max_y] relative to center (0, 0)."""
        half_w = self.effective_width / 2.0
        half_h = self.effective_height / 2.0
        return (-half_w, -half_h, half_w, half_h)

    def get_anchor(self, side: Side) -> tuple[float, float]:
        """Get anchor coordinate on the state boundary.

        Args:
            side: Attachment side ('left', 'right', 'top', 'bottom', 'auto').

        Returns:
            Relative coordinate (x, y) on boundary.
        """
        cx, cy = self._local_xy
        half_w = self.effective_width / 2.0
        half_h = self.effective_height / 2.0

        if side == "top":
            return (cx, cy + half_h)
        if side == "bottom":
            return (cx, cy - half_h)
        if side == "left":
            return (cx - half_w, cy)
        if side == "right":
            return (cx + half_w, cy)
        return (cx, cy)

    def loop(
        self,
        side: LoopSide = "top",
        label: str = "",
        event: str = "",
        guard: str = "",
        action: str = "",
        width: float | None = None,
        height: float | None = None,
        ratio: float = 0.88,
        style: Style | None = None,
    ) -> StateTransition:
        """Create and register a self-transition loop on this state.

        Args:
            side: Attachment side for loop ('top', 'bottom', 'left', 'right',
                  'top_right', 'top_left', 'bottom_right', 'bottom_left'). Default is 'top'.
            label: Optional full transition label string. Overrides event/guard/action if specified.
            event: Trigger event name (e.g. 'heartbeat', 'tick').
            guard: Guard condition text (automatically formatted as '[guard]').
            action: Effect / action text (automatically formatted as '/ action').
            width: Optional width of loop ellipse. Defaults to height, proportional size, or standard.
            height: Optional height of loop ellipse. Defaults to width, proportional size, or standard.
            ratio: Arc coverage ratio along ellipse circumference (default 0.88).
            style: Optional Style object overriding edge color, width, and dash style.

        Returns:
            StateTransition: Newly created self-loop transition edge.
        """
        trans = _transition_module.StateTransition(
            start=self,
            end=self,
            label=label,
            event=event,
            guard=guard,
            action=action,
            style=style,
            loop_side=side,
            loop_width=width,
            loop_height=height,
            loop_ratio=ratio,
            is_loop=True,
        )
        if self._diagram is not None:
            self._diagram.add_transition(trans)
        return trans

    def to(
        self,
        target: StateNodeBase,
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
    ) -> StateTransition:
        """Create and register a state transition from self to target.

        Args:
            target: Destination StateNodeBase instance.
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

        Returns:
            StateTransition: Newly created transition edge.
        """
        if target is self:
            chosen_side: LoopSide = start_side if start_side != "auto" else "top"
            return self.loop(
                side=chosen_side,
                label=label,
                event=event,
                guard=guard,
                action=action,
                style=style,
            )

        trans = _transition_module.StateTransition(
            start=self,
            end=target,
            label=label,
            event=event,
            guard=guard,
            action=action,
            bend=bend,
            start_side=start_side,
            end_side=end_side,
            routing=routing,
            style=style,
            padding=padding,
        )
        if self._diagram is not None:
            self._diagram.add_transition(trans)
        elif target._diagram is not None:
            target._diagram.add_transition(trans)
        return trans


class State(StateNodeBase):
    """Represents a state node in a StateDiagram.

    Supports box (rounded rectangle), oval (ellipse), circle, double_circle, and text_only shapes.
    """

    def __init__(
        self,
        name: str,
        shape: ShapeType = "box",
        entry: str = "",
        do: str = "",
        exit: str = "",  # noqa: A002
        r: float = 2.0,
        width: float | None = None,
        height: float | None = None,
        size: tuple[float, float] | None = None,
        style: Style | None = None,
    ) -> None:
        """Initialize State.

        Args:
            name: State name.
            shape: Visual shape kind ('box', 'oval', 'circle', 'double_circle', 'text_only').
            entry: Optional entry action string ('entry / action').
            do: Optional internal activity string ('do / activity').
            exit: Optional exit action string ('exit / action').
            r: Corner radius when shape is 'box' (default: 2.0).
            width: Optional width of the state shape.
            height: Optional height of the state shape.
            size: Optional shorthand (width, height) tuple overriding width and height.
            style: Optional Style object overriding border, fill, and text colors.
        """
        valid_shapes = {"box", "oval", "circle", "double_circle", "text_only"}
        if shape not in valid_shapes:
            raise ValueError(f"Invalid shape: {shape!r}. Must be one of {sorted(valid_shapes)}.")

        self.shape: ShapeType = shape
        self.r = float(r)

        # Actions
        self.actions: list[StateAction] = []
        if entry:
            self.actions.append(StateAction(kind="entry", action=entry))
        if do:
            self.actions.append(StateAction(kind="do", action=do))
        if exit:
            self.actions.append(StateAction(kind="exit", action=exit))

        # Dimensions
        init_w, init_h = _compute_state_default_size(shape, width, height, size)

        super().__init__(name=name, width=init_w, height=init_h, style=style)
        self.custom_width = width is not None or size is not None
        self.custom_height = height is not None or size is not None

    @property
    def effective_height(self) -> float:
        """Get actual rendered height of the state node."""
        if self.shape == "box" and self.actions:
            # Header + divider + actions
            header_h = 4.5
            row_h = 2.8
            content_h = header_h + len(self.actions) * row_h + 1.2
            if self.custom_height:
                return max(self.height, content_h)
            return content_h

        if self.shape in {"circle", "double_circle"}:
            return self.width

        return self.height

    @property
    def effective_width(self) -> float:
        """Get actual rendered width of the state node."""
        if self.shape in {"circle", "double_circle"}:
            return self.width
        return self.width

    def add_action(self, kind: str, action: str) -> State:
        """Add an internal action or activity to the state.

        Args:
            kind: Action trigger ('entry', 'do', 'exit', or custom label).
            action: Action code or description.

        Returns:
            State: self for chaining.
        """
        self.actions.append(StateAction(kind=kind, action=action))
        return self


class InitialState(StateNodeBase):
    """UML Initial state pseudo-state (solid filled circle)."""

    def __init__(
        self,
        name: str = "",
        radius: float = 1.75,
        style: Style | None = None,
    ) -> None:
        """Initialize InitialState.

        Args:
            name: Optional label text.
            radius: Radius of the filled circle (default: 1.75).
            style: Optional Style overriding circle color.
        """
        self.radius = float(radius)
        size = self.radius * 2.0
        super().__init__(name=name, width=size, height=size, style=style)


class FinalState(StateNodeBase):
    """UML Final state (bullseye: outer ring with inner solid circle)."""

    def __init__(
        self,
        name: str = "",
        radius: float = 2.2,
        style: Style | None = None,
    ) -> None:
        """Initialize FinalState.

        Args:
            name: Optional label text.
            radius: Outer radius of the final state circle (default: 2.2).
            style: Optional Style overriding circle colors.
        """
        self.radius = float(radius)
        size = self.radius * 2.0
        super().__init__(name=name, width=size, height=size, style=style)


class ChoiceState(StateNodeBase):
    """UML Choice pseudo-state (diamond shape)."""

    def __init__(
        self,
        name: str = "",
        size: float = 4.5,
        style: Style | None = None,
    ) -> None:
        """Initialize ChoiceState.

        Args:
            name: Optional label text.
            size: Width and height of the diamond (default: 4.5).
            style: Optional Style overriding diamond appearance.
        """
        self.size = float(size)
        super().__init__(name=name, width=self.size, height=self.size, style=style)


class ForkJoinState(StateNodeBase):
    """UML Fork or Join synchronization bar."""

    def __init__(
        self,
        name: str = "",
        orientation: Literal["horizontal", "vertical"] = "horizontal",
        length: float = 16.0,
        thickness: float = 1.8,
        style: Style | None = None,
    ) -> None:
        """Initialize ForkJoinState.

        Args:
            name: Optional label text.
            orientation: Orientation of the bar ('horizontal' or 'vertical').
            length: Length of the synchronization bar (default: 16.0).
            thickness: Thickness of the synchronization bar (default: 1.8).
            style: Optional Style overriding bar fill color.
        """
        valid_orientations = {"horizontal", "vertical"}
        if orientation not in valid_orientations:
            raise ValueError(f"Invalid orientation: {orientation!r}. Must be one of {sorted(valid_orientations)}.")

        self.orientation: Literal["horizontal", "vertical"] = orientation
        self.length = float(length)
        self.thickness = float(thickness)

        if orientation == "horizontal":
            w = self.length
            h = self.thickness
        else:
            w = self.thickness
            h = self.length

        super().__init__(name=name, width=w, height=h, style=style)


def _compute_state_default_size(
    shape: ShapeType,
    width: float | None,
    height: float | None,
    size: tuple[float, float] | None,
) -> tuple[float, float]:
    """Compute default or explicitly configured dimensions for a State.

    Args:
        shape: Visual shape type.
        width: Optional explicit width.
        height: Optional explicit height.
        size: Optional (width, height) tuple.

    Returns:
        Resolved (width, height) tuple.
    """
    if size is not None:
        return (float(size[0]), float(size[1]))

    default_widths = {
        "box": 22.0,
        "oval": 24.0,
        "circle": 16.0,
        "double_circle": 16.0,
        "text_only": 16.0,
    }
    init_w = float(width) if width is not None else default_widths.get(shape, 22.0)

    if height is not None:
        init_h = float(height)
    elif shape in {"circle", "double_circle"}:
        init_h = init_w
    elif shape == "oval":
        init_h = 13.0
    elif shape == "text_only":
        init_h = 8.0
    else:
        init_h = 12.0

    return (init_w, init_h)
