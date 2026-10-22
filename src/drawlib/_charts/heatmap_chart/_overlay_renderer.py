# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Rendering engine for spatial and diagram HeatmapOverlay."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import numpy
from PIL import Image

from drawlib._charts._common._style_utils import (
    clamp_ratio,
    ensure_shape_style,
    ensure_text_style,
)
from drawlib._charts.heatmap_chart._models import (
    extract_heatmap_color,
    format_heatmap_value,
    interpolate_color_stops,
)
from drawlib._core.l3_colors import Color
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas import circle as canvas_circle
from drawlib._core.l4_canvas import image as canvas_image
from drawlib._core.l4_canvas import rectangle as canvas_rectangle
from drawlib._core.l4_canvas import text as canvas_text
from drawlib._preset_colors import DefaultColors as Colors

if TYPE_CHECKING:
    from drawlib._charts.heatmap_chart._overlay import HeatmapOverlay


def _render_smooth_overlay(
    overlay: HeatmapOverlay,
    bx: float,
    by: float,
    bounds: tuple[float, float, float, float],
) -> None:
    """Render smooth 2D Gaussian thermal gradient field as an RGBA canvas image."""
    visible_spots = [s for s in overlay._spots if s.show and s.draw_ratio > 0.0]
    if not visible_spots:
        return

    min_x, min_y, max_x, max_y = bounds
    reg_min_x, reg_max_x = bx + min_x, bx + max_x
    reg_min_y, reg_max_y = by + min_y, by + max_y
    reg_w = max(1.0, reg_max_x - reg_min_x)
    reg_h = max(1.0, reg_max_y - reg_min_y)
    reg_cx = (reg_min_x + reg_max_x) / 2.0
    reg_cy = (reg_min_y + reg_max_y) / 2.0

    res = overlay.resolution
    if reg_w >= reg_h:
        px_w = res
        px_h = max(32, int(round(res * (reg_h / reg_w))))
    else:
        px_h = res
        px_w = max(32, int(round(res * (reg_w / reg_h))))

    # Match exact aspect ratio used by canvas_image(width=reg_w)
    actual_reg_h = reg_w * (px_h / px_w)
    xs = numpy.linspace(reg_cx - reg_w / 2.0, reg_cx + reg_w / 2.0, px_w)
    ys = numpy.linspace(reg_cy + actual_reg_h / 2.0, reg_cy - actual_reg_h / 2.0, px_h)
    grid_x, grid_y = numpy.meshgrid(xs, ys)

    heat = numpy.zeros((px_h, px_w), dtype=numpy.float64)
    span = max(1e-9, overlay.max_value - overlay.min_value)

    for s in visible_spots:
        ratio_r = clamp_ratio(s.draw_ratio)
        w_k = clamp_ratio((s.value - overlay.min_value) / span) * ratio_r
        if w_k <= 0.0:
            continue

        cx_k = bx + s.xy[0]
        cy_k = by + s.xy[1]
        eff_r = max(0.5, s.radius * (0.35 + 0.65 * ratio_r))
        support_r = eff_r * 1.25

        u2 = ((grid_x - cx_k) ** 2 + (grid_y - cy_k) ** 2) / (support_r**2)
        mask = u2 < 1.0
        if not numpy.any(mask):
            continue

        u2_m = u2[mask]
        # Smooth compactly-supported Gaussian kernel vanishing with zero derivative at u=1
        k_val = w_k * numpy.exp(-3.2 * u2_m) * ((1.0 - u2_m) ** 2)
        if overlay.blend_mode == "add":
            heat[mask] += k_val
        else:
            heat[mask] = numpy.maximum(heat[mask], k_val)

    heat = numpy.clip(heat, 0.0, 1.0)
    active_mask = heat > 1e-3
    if not numpy.any(active_mask):
        return

    stops = overlay.color_stops
    n_stops = len(stops)
    stop_t = numpy.linspace(0.0, 1.0, n_stops)
    stop_r = numpy.array([c.r for c in stops], dtype=numpy.float64)
    stop_g = numpy.array([c.g for c in stops], dtype=numpy.float64)
    stop_b = numpy.array([c.b for c in stops], dtype=numpy.float64)
    stop_a = numpy.array([c.alpha for c in stops], dtype=numpy.float64)

    rgba = numpy.zeros((px_h, px_w, 4), dtype=numpy.uint8)
    h_active = heat[active_mask]
    rgba[active_mask, 0] = numpy.clip(numpy.round(numpy.interp(h_active, stop_t, stop_r)), 0, 255).astype(numpy.uint8)
    rgba[active_mask, 1] = numpy.clip(numpy.round(numpy.interp(h_active, stop_t, stop_g)), 0, 255).astype(numpy.uint8)
    rgba[active_mask, 2] = numpy.clip(numpy.round(numpy.interp(h_active, stop_t, stop_b)), 0, 255).astype(numpy.uint8)

    interp_a = numpy.interp(h_active, stop_t, stop_a)
    alpha_val = overlay.max_alpha * interp_a * (h_active**0.72) * 255.0
    rgba[active_mask, 3] = numpy.clip(numpy.round(alpha_val), 0, 255).astype(numpy.uint8)

    pil_img = Image.fromarray(rgba, mode="RGBA")
    canvas_image(
        xy=(reg_cx, reg_cy),
        width=reg_w,
        image=pil_img,
        style=Style(halign="center", valign="center", image_border_width=0),
    )


def _render_contour_overlay(
    overlay: HeatmapOverlay,
    bx: float,
    by: float,
) -> None:
    """Render concentric vector isoline rings for each visible hotspot."""
    visible_spots = [s for s in overlay._spots if s.show and s.draw_ratio > 0.0]
    if not visible_spots:
        return

    stops = overlay.color_stops
    span = max(1e-9, overlay.max_value - overlay.min_value)
    n_levels = max(1, overlay.levels)

    for s in visible_spots:
        ratio_r = clamp_ratio(s.draw_ratio)
        w_k = clamp_ratio((s.value - overlay.min_value) / span) * ratio_r
        if w_k <= 0.0:
            continue

        cx_k = bx + s.xy[0]
        cy_k = by + s.xy[1]
        eff_r = max(0.5, s.radius * (0.35 + 0.65 * ratio_r))

        for l_idx in range(n_levels):
            frac = (l_idx + 1) / n_levels
            r_l = eff_r * (1.0 - (l_idx / n_levels) * 0.72)
            t_l = clamp_ratio(w_k * frac)
            col = extract_heatmap_color(s.style) if s.style is not None else interpolate_color_stops(stops, t_l)

            ring_alpha = min(
                overlay.max_alpha,
                overlay.max_alpha * (0.30 + 0.45 * frac) / max(1.0, n_levels * 0.42),
            )
            fill_col = Color(col.r, col.g, col.b, alpha=round(ring_alpha, 4))

            if overlay.show_contour_lines and overlay.contour_line_width > 0.0:
                stroke_alpha = min(0.92, ring_alpha + 0.28)
                line_col: Color | tuple[int, int, int, float] = Color(col.r, col.g, col.b, alpha=round(stroke_alpha, 4))
                line_w = overlay.contour_line_width
                line_style: Literal["solid", "dashed"] = "solid" if l_idx == n_levels - 1 else "dashed"
            else:
                line_col = Colors.Transparent
                line_w = 0.0
                line_style = "solid"

            canvas_circle(
                xy=(cx_k, cy_k),
                radius=r_l,
                style=Style(
                    shape_fill_color=fill_col,
                    shape_line_color=line_col,
                    shape_line_width=line_w,
                    shape_line_style=line_style,
                ),
            )


def _render_spot_labels(
    overlay: HeatmapOverlay,
    bx: float,
    by: float,
) -> None:
    """Render annotation labels on hotspots when configured."""
    for s in overlay._spots:
        if not s.show or s.draw_ratio < 0.5:
            continue
        lbl = s.label
        if not lbl and overlay.value_text_style is not None and overlay.value_format is not None:
            lbl = format_heatmap_value(s.value, overlay.value_format)
        if not lbl:
            continue

        raw_t_style = s.label_style or overlay.value_text_style
        if raw_t_style is None:
            raw_t_style = Style(text_color=(30, 41, 59, 1.0), text_size=9.5)
        t_style = ensure_text_style(raw_t_style, halign="center", valign="center")
        canvas_text(xy=(bx + s.xy[0], by + s.xy[1]), text=lbl, style=t_style)


def draw_heatmap_overlay(overlay: HeatmapOverlay, base_xy: tuple[float, float]) -> None:
    """Render a spatial thermal heatmap overlay onto the canvas.

    Args:
        overlay: HeatmapOverlay container instance.
        base_xy: Base canvas coordinate (x, y) offset applied to spot coordinates.
    """
    bx, by = float(base_xy[0]), float(base_xy[1])
    bounds = overlay.get_bounds()
    min_x, min_y, max_x, max_y = bounds
    reg_w = max(1.0, max_x - min_x)
    reg_h = max(1.0, max_y - min_y)
    reg_cx = bx + (min_x + max_x) / 2.0
    reg_cy = by + (min_y + max_y) / 2.0

    if overlay.mode == "smooth":
        _render_smooth_overlay(overlay, bx, by, bounds)
    else:
        _render_contour_overlay(overlay, bx, by)

    _render_spot_labels(overlay, bx, by)

    if overlay.border_style is not None:
        b_style = ensure_shape_style(overlay.border_style).patch(shape_fill_color=Colors.Transparent)
        if b_style.shape_line_width is None or b_style.shape_line_width <= 0.0:
            b_style = b_style.patch(
                shape_line_color=overlay.border_style.line_color
                or overlay.border_style.shape_line_color
                or (100, 116, 139, 1.0),
                shape_line_width=overlay.border_style.line_width or 1.0,
            )
        canvas_rectangle(xy=(reg_cx, reg_cy), width=reg_w, height=reg_h, style=b_style)

    if overlay.title and overlay.title_style is not None:
        title_s = ensure_text_style(overlay.title_style, halign="center", valign="bottom")
        canvas_text(xy=(reg_cx, by + max_y + 1.5), text=overlay.title, style=title_s)
