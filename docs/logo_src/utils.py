# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Reusable drawing utilities for the Drawlib brand logo."""

from __future__ import annotations

from drawlib.canvas import canvas
from drawlib.fonts import FontSansSerif
from drawlib.lines import line, lines, lines_bezier
from drawlib.shapes import circle
from drawlib.styles import Colors, Style, Styles
from drawlib.text import text

# Cubic Bezier kappa constant for exact 90-degree circular arcs
_KAPPA: float = 0.55228475


def _corner_arc(
    p_in: tuple[float, float],
    corner: tuple[float, float],
    p_out: tuple[float, float],
) -> tuple[tuple[float, float], tuple[float, float], tuple[float, float]]:
    """Create cubic Bezier control points for a 90-degree circular fillet."""
    cx, cy = corner
    cp1 = (p_in[0] + _KAPPA * (cx - p_in[0]), p_in[1] + _KAPPA * (cy - p_in[1]))
    cp2 = (p_out[0] + _KAPPA * (cx - p_out[0]), p_out[1] + _KAPPA * (cy - p_out[1]))
    return (cp1, cp2, p_out)


def draw_logo_icon(
    *,
    canvas_width: float = 100.0,
) -> None:
    """Draw the Drawlib icon mark in a 100x100 local coordinate space.

    The icon combines:
    - A document outline with a top-right dog-ear fold and open bottom-left corner.
    - An equilateral 3-node triangle graph nestled in the lower-left opening,
      colored with Drawlib's Primary (Blue), Secondary (Teal), and Accent (Purple) tokens.

    Args:
        canvas_width: Virtual width of the active canvas (used to convert canvas stroke
            units into exact Matplotlib point widths: pt = units * 720 / canvas_width).
    """
    pts_per_unit = 720.0 / canvas_width

    # --- Geometry Constants (centered in 100x100 space) ---
    stroke_units = 4.3
    stroke_pt = stroke_units * pts_per_unit
    cap_radius = stroke_units / 2.0

    # Document outline coordinates (shifted +2.75 X, +1.0 Y for exact canvas centering)
    x_left = 20.75
    y_left_end = 38.5
    y_top = 90.0
    x_fold = 65.25
    x_right = 88.75
    y_fold = 66.5
    y_bottom = 19.0
    x_right_end = 82.75

    r_top_left = 5.0
    r_fold_inner = 4.5
    r_bottom_right = 4.5

    # Triangle graph coordinates (equilateral triangle of side length 43.0)
    node_radius = 11.2
    pt_bottom_left = (20.25, 19.0)
    pt_bottom_right = (63.25, 19.0)
    pt_top = (41.75, 56.2)

    # --- Styles ---
    dark_color = Colors.Dark
    stroke_style = Style(
        line_color=dark_color,
        line_width=stroke_pt,
        line_style="solid",
    )
    cap_style = Style(
        shape_fill_color=dark_color,
        shape_line_color=dark_color,
        shape_line_width=0.0,
    )

    node_top_style = Styles.PrimaryFlat.patch(
        shape_fill_color=Colors.Primary,
        shape_line_color=Colors.Primary,
        shape_line_width=0.0,
    )
    node_left_style = Styles.SecondaryFlat.patch(
        shape_fill_color=Colors.Secondary,
        shape_line_color=Colors.Secondary,
        shape_line_width=0.0,
    )
    node_right_style = Styles.AccentFlat.patch(
        shape_fill_color=Colors.Accent,
        shape_line_color=Colors.Accent,
        shape_line_width=0.0,
    )

    # 1. Document Outline: Left vertical -> Top-left fillet -> Top horizontal
    lines_bezier(
        xy=(x_left, y_left_end),
        path_points=[
            (x_left, y_top - r_top_left),
            _corner_arc(
                (x_left, y_top - r_top_left),
                (x_left, y_top),
                (x_left + r_top_left, y_top),
            ),
            (x_fold, y_top),
        ],
        style=stroke_style,
    )

    # 2. Document Outline: Dog-ear inner fold (Vertical down -> Inner fillet -> Horizontal right)
    lines_bezier(
        xy=(x_fold, y_top),
        path_points=[
            (x_fold, y_fold + r_fold_inner),
            _corner_arc(
                (x_fold, y_fold + r_fold_inner),
                (x_fold, y_fold),
                (x_fold + r_fold_inner, y_fold),
            ),
            (x_right, y_fold),
        ],
        style=stroke_style,
    )

    # 3. Document Outline: Dog-ear diagonal crease
    line((x_fold, y_top), (x_right, y_fold), style=stroke_style)

    # 4. Document Outline: Right vertical -> Bottom-right fillet -> Bottom-right hook
    lines_bezier(
        xy=(x_right, y_fold),
        path_points=[
            (x_right, y_bottom + r_bottom_right),
            _corner_arc(
                (x_right, y_bottom + r_bottom_right),
                (x_right, y_bottom),
                (x_right - r_bottom_right, y_bottom),
            ),
            (x_right_end, y_bottom),
        ],
        style=stroke_style,
    )

    # 5. Rounded line caps and fold corner joins
    for cap_xy in [
        (x_left, y_left_end),
        (x_right_end, y_bottom),
        (x_fold, y_top),
        (x_right, y_fold),
    ]:
        circle(cap_xy, radius=cap_radius, style=cap_style)

    # 6. Triangle Graph Edges (drawn underneath the circular nodes)
    lines(
        [pt_bottom_left, pt_top, pt_bottom_right, pt_bottom_left],
        style=stroke_style,
    )

    # 7. Triangle Graph Nodes (Primary Blue, Secondary Teal, Accent Purple)
    circle(pt_top, radius=node_radius, style=node_top_style)
    circle(pt_bottom_left, radius=node_radius, style=node_left_style)
    circle(pt_bottom_right, radius=node_radius, style=node_right_style)


def draw_logo_text(
    *,
    xy: tuple[float, float] = (9.68, 29.45),
    text_size_pt: float = 162.0,
    canvas_width: float = 210.0,
    dot_color: object | None = None,
) -> None:
    """Draw the Drawlib wordmark in Poppins Bold with a circular colored 'i' dot.

    Default parameters center the wordmark with equal top/bottom/left/right margins on a 210x66 canvas.

    Args:
        xy: Left-center anchor coordinate (x, y) for the wordmark text.
        text_size_pt: Font size in points.
        canvas_width: Virtual width of the active canvas (defaults to 210.0).
        dot_color: Color for the circular 'i' dot (defaults to Colors.Secondary).
    """
    pts_per_unit = 720.0 / canvas_width
    resolved_dot_color = Colors.Secondary if dot_color is None else dot_color
    wx, wy = xy

    text(
        (wx, wy),
        "Drawl\u0131b",
        style=Styles.DarkBold.patch(
            text_font=FontSansSerif.POPPINS_BOLD,
            text_size=text_size_pt,
            text_color=Colors.Dark,
            halign="left",
            valign="center",
        ),
    )

    # Exact proportional offset of the 'i' dot in Poppins Bold
    unit_scale = text_size_pt / pts_per_unit
    dot_x = wx + 3.1586 * unit_scale
    dot_y = wy + 0.39375 * unit_scale
    dot_r = 0.1125 * unit_scale

    circle(
        (dot_x, dot_y),
        radius=dot_r,
        style=Style(
            shape_fill_color=resolved_dot_color,  # type: ignore[arg-type]
            shape_line_color=resolved_dot_color,  # type: ignore[arg-type]
            shape_line_width=0.0,
        ),
    )


def draw_logo(
    *,
    canvas_width: float = 310.0,
    dot_color: object | None = None,
) -> None:
    """Draw the horizontal Drawlib logo (icon mark + Poppins Bold wordmark with colored 'i' dot).

    Designed for a 310x100 coordinate space.

    Args:
        canvas_width: Virtual width of the active canvas (defaults to 310.0).
        dot_color: Color for the circular 'i' dot (defaults to Colors.Secondary).
    """
    # 1. Left: Icon mark
    with canvas.transform(origin=(0, 0), scale=1.0, translate=(1.5, 0.0)):
        draw_logo_icon(canvas_width=canvas_width)

    # 2. Right: Wordmark "Drawlıb" in Poppins Bold with circular 'i' dot
    draw_logo_text(
        xy=(111.5, 46.5),
        text_size_pt=110.0,
        canvas_width=canvas_width,
        dot_color=dot_color,
    )
