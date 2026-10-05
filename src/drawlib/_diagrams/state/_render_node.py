# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""State and pseudo-state node rendering functions for StateDiagram."""

from __future__ import annotations

from drawlib._core.l3_fonts import Font
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas import circle as canvas_circle
from drawlib._core.l4_canvas import ellipse as canvas_ellipse
from drawlib._core.l4_canvas import line as canvas_line
from drawlib._core.l4_canvas import rectangle as canvas_rectangle
from drawlib._core.l4_canvas import rhombus as canvas_rhombus
from drawlib._core.l4_canvas import text as canvas_text
from drawlib._diagrams.state._state_node import (
    ChoiceState,
    FinalState,
    ForkJoinState,
    InitialState,
    State,
    StateNodeBase,
)
from drawlib._preset_colors import DefaultColors as Colors


def render_node(node: StateNodeBase, center_xy: tuple[float, float], default_node_style: Style) -> None:
    """Dispatch rendering for a state node or pseudo-state.

    Args:
        node: StateNodeBase instance to render.
        center_xy: Center coordinate (cx, cy) on canvas.
        default_node_style: Base Style for state nodes.
    """
    if isinstance(node, State):
        _render_state_node(node, center_xy, default_node_style)
    elif isinstance(node, InitialState):
        _render_initial_state(node, center_xy, default_node_style)
    elif isinstance(node, FinalState):
        _render_final_state(node, center_xy, default_node_style)
    elif isinstance(node, ChoiceState):
        _render_choice_state(node, center_xy, default_node_style)
    elif isinstance(node, ForkJoinState):
        _render_fork_join_state(node, center_xy, default_node_style)


def _render_state_node(node: State, center_xy: tuple[float, float], default_node_style: Style) -> None:
    """Render a State instance based on its shape type.

    Args:
        node: State instance.
        center_xy: Center coordinate (cx, cy) on canvas.
        default_node_style: Base Style for state nodes.
    """
    if node.shape == "box":
        _render_box_state(node, center_xy, default_node_style)
    elif node.shape == "oval":
        _render_oval_state(node, center_xy, default_node_style)
    elif node.shape == "circle":
        _render_circle_state(node, center_xy, default_node_style)
    elif node.shape == "double_circle":
        _render_double_circle_state(node, center_xy, default_node_style)
    elif node.shape == "text_only":
        _render_text_only_state(node, center_xy, default_node_style)


def _render_box_state(node: State, center_xy: tuple[float, float], default_node_style: Style) -> None:
    """Render a rounded box state node with optional actions.

    Args:
        node: State instance with shape='box'.
        center_xy: Center coordinate (cx, cy) on canvas.
        default_node_style: Base Style for state nodes.
    """
    cx, cy = center_xy
    w = node.effective_width
    h = node.effective_height

    style = default_node_style.patch(node.style) if node.style is not None else default_node_style
    border_color = style.shape_line_color or (71, 85, 105, 1.0)
    text_color = style.text_color or (30, 41, 59, 1.0)
    canvas_rectangle(xy=(cx, cy), width=w, height=h, r=node.r, style=style)

    if not node.actions:
        # Single central name label
        text_style = Style(
            text_size=11,
            text_font=Font.SANSSERIF_BOLD,
            text_color=text_color,
            text_halign="center",
            text_valign="center",
        )
        if node.style is not None and node.style.text_color is not None:
            text_style = text_style.patch(node.style)
        canvas_text(xy=(cx, cy), text=node.name, style=text_style)
        return

    # Complex state with header and action compartments
    header_h = 4.5
    top_y = cy + h / 2.0
    header_cy = top_y - header_h / 2.0
    div_y = top_y - header_h

    # State name in header compartment
    name_style = Style(
        text_size=11,
        text_font=Font.SANSSERIF_BOLD,
        text_color=text_color,
        text_halign="center",
        text_valign="center",
    )
    if node.style is not None and node.style.text_color is not None:
        name_style = name_style.patch(node.style)
    canvas_text(xy=(cx, header_cy), text=node.name, style=name_style)

    # Divider line
    div_style = Style(
        line_color=border_color,
        line_width=1.0,
    )
    canvas_line(xy1=(cx - w / 2.0, div_y), xy2=(cx + w / 2.0, div_y), style=div_style)

    # Internal actions list
    row_h = 2.8
    act_x = cx - w / 2.0 + 2.0
    action_style = Style(
        text_size=9,
        text_font=Font.SANSSERIF_REGULAR,
        text_color=(100, 116, 139, 1.0),
        text_halign="left",
        text_valign="center",
    )
    for i, action in enumerate(node.actions):
        act_y = div_y - 1.8 - i * row_h
        canvas_text(xy=(act_x, act_y), text=action.display_text, style=action_style)


def _render_oval_state(node: State, center_xy: tuple[float, float], default_node_style: Style) -> None:
    """Render an oval (capsule/ellipse) state node.

    Args:
        node: State instance with shape='oval'.
        center_xy: Center coordinate (cx, cy) on canvas.
        default_node_style: Base Style for state nodes.
    """
    cx, cy = center_xy
    w = node.effective_width
    h = node.effective_height

    style = default_node_style.patch(node.style) if node.style is not None else default_node_style
    canvas_ellipse(xy=(cx, cy), width=w, height=h, style=style)

    text_color = style.text_color or (30, 41, 59, 1.0)
    text_style = Style(
        text_size=11,
        text_font=Font.SANSSERIF_BOLD,
        text_color=text_color,
        text_halign="center",
        text_valign="center",
    )
    if node.style is not None and node.style.text_color is not None:
        text_style = text_style.patch(node.style)
    canvas_text(xy=(cx, cy), text=node.name, style=text_style)


def _render_circle_state(node: State, center_xy: tuple[float, float], default_node_style: Style) -> None:
    """Render a circle state node (transparent background by default).

    Args:
        node: State instance with shape='circle'.
        center_xy: Center coordinate (cx, cy) on canvas.
        default_node_style: Base Style for state nodes.
    """
    cx, cy = center_xy
    radius = node.effective_width / 2.0

    border_color = default_node_style.shape_line_color or (71, 85, 105, 1.0)
    base_style = Style(
        shape_fill_color=Colors.Transparent,
        shape_line_color=border_color,
        shape_line_width=default_node_style.shape_line_width or 1.5,
    )
    style = base_style.patch(node.style) if node.style is not None else base_style
    canvas_circle(xy=(cx, cy), radius=radius, style=style)

    text_color = style.text_color or default_node_style.text_color or (30, 41, 59, 1.0)
    text_style = Style(
        text_size=10.5,
        text_font=Font.SANSSERIF_BOLD,
        text_color=text_color,
        text_halign="center",
        text_valign="center",
    )
    if node.style is not None and node.style.text_color is not None:
        text_style = text_style.patch(node.style)
    canvas_text(xy=(cx, cy), text=node.name, style=text_style)


def _render_double_circle_state(node: State, center_xy: tuple[float, float], default_node_style: Style) -> None:
    """Render a double circle state node (FSM accepting state).

    Args:
        node: State instance with shape='double_circle'.
        center_xy: Center coordinate (cx, cy) on canvas.
        default_node_style: Base Style for state nodes.
    """
    cx, cy = center_xy
    r_outer = node.effective_width / 2.0
    r_inner = max(r_outer - 1.2, 0.5)

    border_color = default_node_style.shape_line_color or (71, 85, 105, 1.0)
    outer_base = Style(
        shape_fill_color=Colors.Transparent,
        shape_line_color=border_color,
        shape_line_width=default_node_style.shape_line_width or 1.5,
    )
    outer_style = outer_base.patch(node.style) if node.style is not None else outer_base
    canvas_circle(xy=(cx, cy), radius=r_outer, style=outer_style)

    inner_line_color = outer_style.shape_line_color or border_color
    inner_line_width = outer_style.shape_line_width or 1.5
    inner_style = Style(
        shape_fill_color=Colors.Transparent,
        shape_line_color=inner_line_color,
        shape_line_width=inner_line_width,
    )
    canvas_circle(xy=(cx, cy), radius=r_inner, style=inner_style)

    text_color = outer_style.text_color or default_node_style.text_color or (30, 41, 59, 1.0)
    text_style = Style(
        text_size=10.0,
        text_font=Font.SANSSERIF_BOLD,
        text_color=text_color,
        text_halign="center",
        text_valign="center",
    )
    if node.style is not None and node.style.text_color is not None:
        text_style = text_style.patch(node.style)
    canvas_text(xy=(cx, cy), text=node.name, style=text_style)


def _render_text_only_state(node: State, center_xy: tuple[float, float], default_node_style: Style) -> None:
    """Render a text-only state node without border.

    Args:
        node: State instance with shape='text_only'.
        center_xy: Center coordinate (cx, cy) on canvas.
        default_node_style: Base Style for state nodes.
    """
    cx, cy = center_xy
    text_color = (
        node.style.text_color if node.style and node.style.text_color is not None else default_node_style.text_color
    ) or (30, 41, 59, 1.0)
    text_style = Style(
        text_size=11,
        text_font=Font.SANSSERIF_BOLD,
        text_color=text_color,
        text_halign="center",
        text_valign="center",
    )
    canvas_text(xy=(cx, cy), text=node.name, style=text_style)


def _render_initial_state(node: InitialState, center_xy: tuple[float, float], default_node_style: Style) -> None:
    """Render an InitialState pseudo-state (filled solid circle).

    Args:
        node: InitialState instance.
        center_xy: Center coordinate (cx, cy) on canvas.
        default_node_style: Base Style for state nodes.
    """
    cx, cy = center_xy
    solid_color = default_node_style.shape_line_color or default_node_style.shape_fill_color or (30, 41, 59, 1.0)
    base_style = Style(
        shape_fill_color=solid_color,
        shape_line_color=solid_color,
        shape_line_width=1.0,
    )
    style = base_style.patch(node.style) if node.style is not None else base_style
    canvas_circle(xy=(cx, cy), radius=node.radius, style=style)

    if node.name:
        label_style = Style(
            text_size=9,
            text_font=Font.SANSSERIF_REGULAR,
            text_color=(100, 116, 139, 1.0),
            text_halign="center",
            text_valign="top",
        )
        canvas_text(xy=(cx, cy - node.radius - 1.0), text=node.name, style=label_style)


def _render_final_state(node: FinalState, center_xy: tuple[float, float], default_node_style: Style) -> None:
    """Render a FinalState pseudo-state (bullseye circle).

    Args:
        node: FinalState instance.
        center_xy: Center coordinate (cx, cy) on canvas.
        default_node_style: Base Style for state nodes.
    """
    cx, cy = center_xy
    r_outer = node.radius
    r_inner = r_outer * 0.65

    solid_color = default_node_style.shape_line_color or default_node_style.shape_fill_color or (30, 41, 59, 1.0)
    outer_base = Style(
        shape_fill_color=Colors.Transparent,
        shape_line_color=solid_color,
        shape_line_width=1.5,
    )
    outer_style = outer_base.patch(node.style) if node.style is not None else outer_base
    canvas_circle(xy=(cx, cy), radius=r_outer, style=outer_style)

    inner_style = Style(
        shape_fill_color=solid_color,
        shape_line_color=solid_color,
        shape_line_width=1.0,
    )
    canvas_circle(xy=(cx, cy), radius=r_inner, style=inner_style)

    if node.name:
        label_style = Style(
            text_size=9,
            text_font=Font.SANSSERIF_REGULAR,
            text_color=(100, 116, 139, 1.0),
            text_halign="center",
            text_valign="top",
        )
        canvas_text(xy=(cx, cy - r_outer - 1.0), text=node.name, style=label_style)


def _render_choice_state(node: ChoiceState, center_xy: tuple[float, float], default_node_style: Style) -> None:
    """Render a ChoiceState pseudo-state (diamond).

    Args:
        node: ChoiceState instance.
        center_xy: Center coordinate (cx, cy) on canvas.
        default_node_style: Base Style for state nodes.
    """
    cx, cy = center_xy
    style = default_node_style.patch(node.style) if node.style is not None else default_node_style
    canvas_rhombus(xy=(cx, cy), width=node.size, height=node.size, style=style)

    if node.name:
        label_style = Style(
            text_size=9,
            text_font=Font.SANSSERIF_REGULAR,
            text_color=(100, 116, 139, 1.0),
            text_halign="center",
            text_valign="bottom",
        )
        canvas_text(xy=(cx, cy + node.size / 2.0 + 1.0), text=node.name, style=label_style)


def _render_fork_join_state(node: ForkJoinState, center_xy: tuple[float, float], default_node_style: Style) -> None:
    """Render a ForkJoinState pseudo-state (solid sync bar).

    Args:
        node: ForkJoinState instance.
        center_xy: Center coordinate (cx, cy) on canvas.
        default_node_style: Base Style for state nodes.
    """
    cx, cy = center_xy
    solid_color = default_node_style.shape_line_color or default_node_style.shape_fill_color or (30, 41, 59, 1.0)
    base_style = Style(
        shape_fill_color=solid_color,
        shape_line_color=solid_color,
        shape_line_width=1.0,
    )
    style = base_style.patch(node.style) if node.style is not None else base_style
    canvas_rectangle(xy=(cx, cy), width=node.width, height=node.height, r=0.4, style=style)

    if node.name:
        label_style = Style(
            text_size=9,
            text_font=Font.SANSSERIF_REGULAR,
            text_color=(100, 116, 139, 1.0),
            text_halign="center",
            text_valign="bottom",
        )
        canvas_text(xy=(cx, cy + node.height / 2.0 + 1.0), text=node.name, style=label_style)
