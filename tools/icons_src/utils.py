# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Shared color palettes, style builders, and geometric primitives for `tools/icons_src/`."""

from __future__ import annotations

import math
from typing import Any

from drawlib.canvas import setup
from drawlib.lines import line, lines, lines_curved
from drawlib.shapes import arc, circle, ellipse, polygon, rectangle
from drawlib.styles import Colors, Style


class Icon:
    """Core canvas setup, color constants, style builders, and shared geometric primitives."""

    CANVAS_SIZE: int = 100
    CANVAS_DPI: int = 200
    PTS_PER_UNIT: float = 720.0 / float(CANVAS_SIZE)

    DARK = Colors.Dark  # #323A48 (Deep Slate structural outline)
    WHITE = Colors.White  # Crisp white fill (#FFFFFF)
    ORIG_STROKE: float = 2.0  # Unified structural stroke width in 100x100 units

    PASTEL_BLUE = "#6888F0"  # Medium Cornflower Blue (primary surface, Tone 3)
    PASTEL_BLUE_DARK = "#4862DA"  # Deeper cornflower blue for high-contrast white glyphs (Tone 4)
    PASTEL_BLUE_LIGHT = "#9AB6F8"  # Lighter blue companion tint (Tone 2)
    PASTEL_GREEN = "#5CC46E"  # Medium Mint/Sage Green (secondary/accent surface, Tone 3)

    @classmethod
    def pt(cls, units: float) -> float:
        """Convert stroke width in 100x100 canvas units into Matplotlib points."""
        return units * cls.PTS_PER_UNIT

    @classmethod
    def setup(cls) -> None:
        """Initialize a transparent 100x100 icon canvas at 200 DPI (2000x2000 supersampled)."""
        setup(
            width=cls.CANVAS_SIZE,
            height=cls.CANVAS_SIZE,
            dpi=cls.CANVAS_DPI,
            color=Colors.Canvas,
            alpha=0.0,
        )

    @classmethod
    def fill_style(
        cls,
        fill_color: Any,
        *,
        border_color: Any | None = None,
        border_units: float = 0.0,
        shape_r: float | tuple[float, ...] | None = None,
        angle: float | None = None,
        alpha: float | None = None,
    ) -> Style:
        """Create a shape Style with unit-converted border width."""
        b_col = fill_color if border_color is None else border_color
        kw: dict[str, Any] = {
            "shape_fill_color": fill_color,
            "shape_line_color": b_col,
            "shape_line_width": cls.pt(border_units) if border_units > 0 else 0.0,
            "shape_line_style": "solid",
        }
        if shape_r is not None:
            kw["shape_r"] = shape_r
        if angle is not None:
            kw["angle"] = angle
        if alpha is not None:
            kw["alpha"] = alpha
        return Style(**kw)

    @classmethod
    def no_border_fill(cls, fill_color: Any, *, shape_r: float | None = None) -> Style:
        """Create a borderless fill style with zero line width and matching edge color."""
        kw: dict[str, Any] = {
            "shape_fill_color": fill_color,
            "shape_line_color": fill_color,
            "shape_line_width": 0.0,
        }
        if shape_r is not None:
            kw["shape_r"] = shape_r
        return Style(**kw)

    @classmethod
    def stroke_style(
        cls,
        color: Any = DARK,
        *,
        width_units: float = ORIG_STROKE,
        line_style: str = "solid",
    ) -> Style:
        """Create a line/arc stroke Style with unit-converted stroke width."""
        return Style(
            line_color=color,
            line_width=cls.pt(width_units),
            line_style=line_style,  # type: ignore[arg-type]
            shape_line_color=color,
            shape_line_width=cls.pt(width_units),
            shape_line_style=line_style,  # type: ignore[arg-type]
            shape_fill_color=Colors.Transparent,
        )

    @classmethod
    def draw_cap(
        cls,
        xy: tuple[float, float],
        *,
        width_units: float = ORIG_STROKE,
        color: Any = DARK,
    ) -> None:
        """Draw a circular round cap of diameter width_units at xy."""
        circle(xy, radius=width_units / 2.0, style=cls.fill_style(color))

    @classmethod
    def draw_round_segment(
        cls,
        xy1: tuple[float, float],
        xy2: tuple[float, float],
        *,
        width_units: float = ORIG_STROKE,
        color: Any = DARK,
    ) -> None:
        """Draw a straight line segment with smooth circular end caps."""
        line(xy1, xy2, style=cls.stroke_style(color, width_units=width_units))
        r = width_units / 2.0
        st = cls.fill_style(color)
        circle(xy1, radius=r, style=st)
        circle(xy2, radius=r, style=st)

    @classmethod
    def draw_round_polyline(
        cls,
        points: list[tuple[float, float]],
        *,
        width_units: float = ORIG_STROKE,
        color: Any = DARK,
        corner_r: float = 0.0,
        closed: bool = False,
    ) -> None:
        """Draw a multi-point polyline with rounded joins and end caps."""
        st = cls.stroke_style(color, width_units=width_units)
        pts = [*points, points[0]] if closed else points
        if corner_r > 0.0 and len(pts) >= 3:
            lines_curved(pts, r=corner_r, style=st)
        else:
            lines(pts, style=st)
        cap_st = cls.fill_style(color)
        r = width_units / 2.0
        if corner_r > 0.0 and not closed:
            circle(pts[0], radius=r, style=cap_st)
            circle(pts[-1], radius=r, style=cap_st)
        else:
            for p in points:
                circle(p, radius=r, style=cap_st)

    @classmethod
    def draw_capsule(
        cls,
        xy1: tuple[float, float],
        xy2: tuple[float, float],
        *,
        width_units: float,
        color: Any,
        cap_start: bool = True,
        cap_end: bool = True,
    ) -> None:
        """Draw a geometric stadium/capsule bar between xy1 and xy2 in canvas units."""
        x1, y1 = xy1
        x2, y2 = xy2
        dx, dy = x2 - x1, y2 - y1
        length = math.hypot(dx, dy)
        r = width_units / 2.0
        st = cls.fill_style(color)
        if length > 1e-6:
            nx = -dy / length * r
            ny = dx / length * r
            verts = [
                (x1 + nx, y1 + ny),
                (x2 + nx, y2 + ny),
                (x2 - nx, y2 - ny),
                (x1 - nx, y1 - ny),
            ]
            polygon(verts, style=st)
        if cap_start:
            circle(xy1, radius=r, style=st)
        if cap_end:
            circle(xy2, radius=r, style=st)

    @classmethod
    def draw_chunky_arrow(
        cls,
        *,
        y_center: float,
        x_tail: float,
        x_tip: float,
        x_head_base: float,
        shaft_half_h: float,
        head_half_h: float,
        fill_color: Any,
        border_units: float = ORIG_STROKE,
        border_color: Any = DARK,
    ) -> None:
        """Draw a unified single-polygon horizontal arrow with smooth rounded joins."""
        pts = [
            (x_tail, y_center - shaft_half_h),
            (x_head_base, y_center - shaft_half_h),
            (x_head_base, y_center - head_half_h),
            (x_tip, y_center),
            (x_head_base, y_center + head_half_h),
            (x_head_base, y_center + shaft_half_h),
            (x_tail, y_center + shaft_half_h),
        ]
        polygon(pts, style=cls.fill_style(fill_color))
        if border_units > 0:
            cls.draw_round_polyline(pts, width_units=border_units, color=border_color, closed=True)

    @classmethod
    def draw_iso_cube(
        cls,
        cx: float,
        cy: float,
        radius: float,
        *,
        top_color: Any,
        left_color: Any,
        right_color: Any,
        border_color: Any | None = DARK,
        border_units: float = ORIG_STROKE,
    ) -> dict[str, tuple[float, float]]:
        """Draw an isometric 3D cube centered at (cx, cy) and return key vertices."""
        dx = radius * math.cos(math.radians(30.0))
        dy = radius * math.sin(math.radians(30.0))

        v_center = (cx, cy)
        v_top = (cx, cy + radius)
        v_tr = (cx + dx, cy + dy)
        v_br = (cx + dx, cy - dy)
        v_bottom = (cx, cy - radius)
        v_bl = (cx - dx, cy - dy)
        v_tl = (cx - dx, cy + dy)

        polygon([v_center, v_tl, v_top, v_tr], style=cls.fill_style(top_color))
        polygon([v_center, v_bottom, v_bl, v_tl], style=cls.fill_style(left_color))
        polygon([v_center, v_tr, v_br, v_bottom], style=cls.fill_style(right_color))

        if border_color is not None and border_units > 0.0:
            outer = [v_top, v_tr, v_br, v_bottom, v_bl, v_tl]
            cls.draw_round_polyline(outer, width_units=border_units, color=border_color, closed=True)
            for v in (v_tl, v_tr, v_bottom):
                cls.draw_round_segment(v_center, v, width_units=border_units * 0.9, color=border_color)

        return {
            "center": v_center,
            "top": v_top,
            "tr": v_tr,
            "br": v_br,
            "bottom": v_bottom,
            "bl": v_bl,
            "tl": v_tl,
        }

    @classmethod
    def draw_cylinder_tier(
        cls,
        cx: float,
        y_bottom: float,
        width: float,
        body_h: float,
        ry: float,
        *,
        body_color: Any,
        top_color: Any | None = None,
        border_color: Any = DARK,
        border_units: float = ORIG_STROKE,
        draw_top_cap: bool = True,
    ) -> None:
        """Draw a single 3D cylinder tier from y_bottom to y_bottom + body_h."""
        y_top = y_bottom + body_h
        w_half = width / 2.0

        ellipse((cx, y_bottom), width=width, height=ry * 2.0, style=cls.fill_style(body_color))
        if body_h > 0:
            rectangle((cx, y_bottom + body_h / 2.0), width=width, height=body_h, style=cls.fill_style(body_color))

        arc(
            (cx, y_bottom),
            width=width,
            height=ry * 2.0,
            angle_start=180.0,
            angle_end=360.0,
            style=cls.stroke_style(border_color, width_units=border_units),
        )
        if body_h > 0:
            cls.draw_round_segment(
                (cx - w_half, y_bottom), (cx - w_half, y_top), width_units=border_units, color=border_color
            )
            cls.draw_round_segment(
                (cx + w_half, y_bottom), (cx + w_half, y_top), width_units=border_units, color=border_color
            )

        if draw_top_cap:
            t_col = body_color if top_color is None else top_color
            ellipse(
                (cx, y_top),
                width=width,
                height=ry * 2.0,
                style=cls.fill_style(t_col, border_color=border_color, border_units=border_units),
            )

    @classmethod
    def build_shield_half_points(
        cls,
        cx: float,
        y_bottom: float,
        y_top: float,
        half_w: float,
        *,
        side: str,
    ) -> list[tuple[float, float]]:
        """Generate smooth polygon vertices for the left or right half of a heraldic shield."""
        height = y_top - y_bottom
        y_shoulder = y_top - height * 0.11
        y_waist = y_bottom + height * 0.50
        sign = -1.0 if side == "left" else 1.0
        x_edge = cx + sign * half_w

        p0 = (x_edge, y_waist)
        p1 = (x_edge, y_bottom + height * 0.21)
        p2 = (cx + sign * (half_w * 0.45), y_bottom + height * 0.065)
        p3 = (cx, y_bottom)

        curve_pts: list[tuple[float, float]] = []
        steps = 20
        for i in range(steps + 1):
            t = i / steps
            mt = 1.0 - t
            bx = (mt**3) * p0[0] + 3 * (mt**2) * t * p1[0] + 3 * mt * (t**2) * p2[0] + (t**3) * p3[0]
            by = (mt**3) * p0[1] + 3 * (mt**2) * t * p1[1] + 3 * mt * (t**2) * p2[1] + (t**3) * p3[1]
            curve_pts.append((bx, by))

        return [
            (cx, y_top),
            (x_edge, y_shoulder),
            *curve_pts,
        ]

    @classmethod
    def build_sparkle_4pt_polygon(
        cls,
        cx: float,
        cy: float,
        outer_r: float,
        inner_r: float,
    ) -> list[tuple[float, float]]:
        """Build smooth 4-pointed sparkle vertices in exact canvas coordinates."""
        tips = [
            (cx, cy + outer_r),
            (cx + outer_r, cy),
            (cx, cy - outer_r),
            (cx - outer_r, cy),
        ]
        diag = inner_r * math.cos(math.radians(45.0))
        controls = [
            (cx + diag, cy + diag),
            (cx + diag, cy - diag),
            (cx - diag, cy - diag),
            (cx - diag, cy + diag),
        ]
        pts: list[tuple[float, float]] = []
        steps = 16
        for i in range(4):
            p0 = tips[i]
            ctrl = controls[i]
            p2 = tips[(i + 1) % 4]
            for s in range(steps):
                t = s / steps
                mt = 1.0 - t
                bx = (mt**2) * p0[0] + 2 * mt * t * ctrl[0] + (t**2) * p2[0]
                by = (mt**2) * p0[1] + 2 * mt * t * ctrl[1] + (t**2) * p2[1]
                pts.append((bx, by))
        return pts


class Gcp:
    """Google Cloud Platform color palette and geometric helpers."""

    BLUE = "#4285F4"
    RED = "#EA4335"
    YELLOW = "#FBBC04"
    GREEN = "#34A853"
    GREY = "#9AA0A6"

    TECH_DARK = "#3367D6"
    TECH_MID = "#4285F4"
    TECH_MED_LIGHT = "#669DF6"
    TECH_LIGHT = "#AECBFA"

    @classmethod
    def draw_rounded_corner_block(
        cls,
        x0: float,
        y0: float,
        x1: float,
        y1: float,
        *,
        r: float,
        round_tl: bool = False,
        round_tr: bool = False,
        round_br: bool = False,
        round_bl: bool = False,
        color: str,
    ) -> None:
        """Draw an axis-aligned rectangular block with selective rounded corners."""
        st = Icon.fill_style(color)
        pts: list[tuple[float, float]] = []
        steps = 16

        if round_bl and r > 0:
            cx, cy = x0 + r, y0 + r
            for i in range(steps + 1):
                ang = math.radians(180.0 + 90.0 * (i / steps))
                pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
        else:
            pts.append((x0, y0))

        if round_br and r > 0:
            cx, cy = x1 - r, y0 + r
            for i in range(steps + 1):
                ang = math.radians(270.0 + 90.0 * (i / steps))
                pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
        else:
            pts.append((x1, y0))

        if round_tr and r > 0:
            cx, cy = x1 - r, y1 - r
            for i in range(steps + 1):
                ang = math.radians(0.0 + 90.0 * (i / steps))
                pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
        else:
            pts.append((x1, y1))

        if round_tl and r > 0:
            cx, cy = x0 + r, y1 - r
            for i in range(steps + 1):
                ang = math.radians(90.0 + 90.0 * (i / steps))
                pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
        else:
            pts.append((x0, y1))

        polygon(pts, style=st)

    @classmethod
    def draw_pin_h(
        cls,
        x_inner: float,
        x_tip: float,
        yc: float,
        width: float,
        color: str,
    ) -> None:
        """Draw a horizontal pin with a flat inner root at x_inner and semicircular tip at x_tip."""
        r = width / 2.0
        st = Icon.fill_style(color)
        steps = 20
        pts: list[tuple[float, float]] = []
        if x_tip < x_inner:
            cx = x_tip + r
            pts.append((x_inner, yc + r))
            for i in range(steps + 1):
                ang = math.radians(90.0 + 180.0 * (i / steps))
                pts.append((cx + r * math.cos(ang), yc + r * math.sin(ang)))
            pts.append((x_inner, yc - r))
        else:
            cx = x_tip - r
            pts.append((x_inner, yc - r))
            for i in range(steps + 1):
                ang = math.radians(-90.0 + 180.0 * (i / steps))
                pts.append((cx + r * math.cos(ang), yc + r * math.sin(ang)))
            pts.append((x_inner, yc + r))
        polygon(pts, style=st)

    @classmethod
    def draw_pin_v(
        cls,
        xc: float,
        y_inner: float,
        y_tip: float,
        width: float,
        color: str,
    ) -> None:
        """Draw a vertical pin with a flat inner root at y_inner and semicircular tip at y_tip."""
        r = width / 2.0
        st = Icon.fill_style(color)
        steps = 20
        pts: list[tuple[float, float]] = []
        if y_tip > y_inner:
            cy = y_tip - r
            pts.append((xc + r, y_inner))
            for i in range(steps + 1):
                ang = math.radians(0.0 + 180.0 * (i / steps))
                pts.append((xc + r * math.cos(ang), cy + r * math.sin(ang)))
            pts.append((xc - r, y_inner))
        else:
            cy = y_tip + r
            pts.append((xc - r, y_inner))
            for i in range(steps + 1):
                ang = math.radians(180.0 + 180.0 * (i / steps))
                pts.append((xc + r * math.cos(ang), cy + r * math.sin(ang)))
            pts.append((xc + r, y_inner))
        polygon(pts, style=st)

    @classmethod
    def draw_radial_spoke(
        cls,
        cx: float,
        cy: float,
        angle_deg: float,
        r_inner: float,
        r_outer: float,
        width_units: float,
        color: str,
    ) -> None:
        """Draw a constant-width spoke whose inner edge follows a concentric concave circle of radius r_inner."""
        half_w = width_units / 2.0
        theta = math.radians(angle_deg)
        ux, uy = math.cos(theta), math.sin(theta)
        nx, ny = -uy, ux

        steps = 12
        verts: list[tuple[float, float]] = []
        for i in range(steps + 1):
            t = -half_w + (2.0 * half_w) * (i / steps)
            d_rad = math.sqrt(max(0.0, r_inner * r_inner - t * t))
            px = cx + d_rad * ux + t * nx
            py = cy + d_rad * uy + t * ny
            verts.append((px, py))

        verts.append((cx + r_outer * ux + half_w * nx, cy + r_outer * uy + half_w * ny))
        verts.append((cx + r_outer * ux - half_w * nx, cy + r_outer * uy - half_w * ny))
        polygon(verts, style=Icon.fill_style(color))


class Aws:
    """AWS official category palette and service/category plate helpers."""

    ORANGE = "#ED7100"
    TEAL = "#01A88D"
    RED = "#DD344C"
    PURPLE = "#8C4FFF"
    PINK = "#E7157B"
    MAGENTA = "#C925D1"
    GREEN = "#7AA116"
    SQUID_INK = "#232F3E"

    @classmethod
    def draw_service_plate(cls, color: Any) -> None:
        """Draw a standard AWS Architecture Service square background tile in [8.0, 92.0]."""
        rectangle((50.0, 50.0), width=84.0, height=84.0, style=Icon.fill_style(color))

    @classmethod
    def draw_category_plate(cls, color: Any, *, border_color: Any = "#879196") -> None:
        """Draw a standard AWS Category framed background tile in [8.0, 92.0]."""
        outer = [(8.0, 8.0), (92.0, 8.0), (92.0, 92.0), (8.0, 92.0)]
        inner = [(9.87, 9.87), (90.13, 9.87), (90.13, 90.13), (9.87, 90.13)]
        polygon(outer, holes=[inner], style=Icon.fill_style(border_color))
        rectangle((50.0, 50.0), width=74.67, height=74.67, style=Icon.fill_style(color))


class Azure:
    """Azure official multi-tone color palette."""

    BLUE = "#0078D4"
    DARK_BLUE = "#005BA1"
    LIGHT_BLUE = "#5EA0EF"
    PALE_BLUE = "#83B9F9"
    CYAN = "#50E6FF"
    LIGHT_CYAN = "#9CEBFF"
    PALE_CYAN = "#C3F1FF"
    TEAL = "#32BEDD"
    DARK_TEAL = "#198AB3"
    PURPLE = "#773ADC"
    LIGHT_PURPLE = "#A67AF4"
    DARK_PURPLE = "#341A6E"
    GREEN = "#76BC2D"
    LIGHT_GREEN = "#86D633"
    DARK_GREEN = "#5E9624"
    ORANGE = "#F78D1E"
    GRAY = "#949494"
    LIGHT_GRAY = "#CCCCCC"
    PALE_GRAY = "#F2F2F2"


class Cisco:
    """Cisco network topology palette and 3D / 2D helpers."""

    BLUE = "#1877B8"
    LIGHT_BLUE = "#7CC0EE"
    DARK_BLUE = "#0E5688"
    BORDER = "#0A3D62"

    @classmethod
    def draw_3d_box(
        cls,
        x0: float,
        y0: float,
        w_front: float,
        h_front: float,
        dx: float,
        dy: float,
        *,
        front_color: Any = BLUE,
        top_color: Any = LIGHT_BLUE,
        side_color: Any = DARK_BLUE,
        seam_color: Any = Icon.WHITE,
        border_color: Any = BORDER,
        seam_units: float = 1.6,
        border_units: float = 1.8,
    ) -> None:
        """Draw a 3-face oblique 3D Cisco box with white internal seams and dark outer contour."""
        x1 = x0 + w_front
        y1 = y0 + h_front

        front_pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
        top_pts = [(x0, y1), (x1, y1), (x1 + dx, y1 + dy), (x0 + dx, y1 + dy)]
        side_pts = [(x1, y0), (x1 + dx, y0 + dy), (x1 + dx, y1 + dy), (x1, y1)]

        polygon(front_pts, style=Icon.no_border_fill(front_color))
        polygon(top_pts, style=Icon.no_border_fill(top_color))
        polygon(side_pts, style=Icon.no_border_fill(side_color))

        Icon.draw_round_segment((x0, y1), (x1, y1), width_units=seam_units, color=seam_color)
        Icon.draw_round_segment((x1, y0), (x1, y1), width_units=seam_units, color=seam_color)
        Icon.draw_round_segment((x1, y1), (x1 + dx, y1 + dy), width_units=seam_units, color=seam_color)

        outer_pts = [
            (x0, y0),
            (x1, y0),
            (x1 + dx, y0 + dy),
            (x1 + dx, y1 + dy),
            (x0 + dx, y1 + dy),
            (x0, y1),
        ]
        Icon.draw_round_polyline(outer_pts, width_units=border_units, color=border_color, closed=True)

    @classmethod
    def draw_3d_cylinder(
        cls,
        cx: float,
        y_bot: float,
        width: float,
        body_h: float,
        ry: float,
        *,
        body_color: Any = BLUE,
        top_color: Any = LIGHT_BLUE,
        side_shadow_color: Any = DARK_BLUE,
        seam_color: Any = Icon.WHITE,
        border_color: Any = BORDER,
        seam_units: float = 1.7,
        border_units: float = 1.8,
    ) -> None:
        """Draw a 3D Cisco cylinder with shaded body, light top ellipse, white seam, and dark contour."""
        w_half = width / 2.0
        eh = ry * 2.0
        y_top = y_bot + body_h

        ellipse((cx, y_bot), width=width, height=eh, style=Icon.no_border_fill(body_color))
        if body_h > 0:
            rectangle((cx, y_bot + body_h / 2.0), width=width, height=body_h, style=Icon.no_border_fill(body_color))

        shadow_w = width * 0.24
        x_s = cx + w_half - shadow_w
        x_r = cx + w_half
        steps = 16
        shadow_pts: list[tuple[float, float]] = [(x_s, y_top), (x_r, y_top)]
        for i in range(steps + 1):
            px = x_r - shadow_w * (i / steps)
            dx_norm = (px - cx) / w_half
            py = y_bot - ry * math.sqrt(max(0.0, 1.0 - dx_norm * dx_norm))
            shadow_pts.append((px, py))
        polygon(shadow_pts, style=Icon.no_border_fill(side_shadow_color))

        arc(
            (cx, y_bot),
            width=width,
            height=eh,
            angle_start=180.0,
            angle_end=360.0,
            style=Icon.stroke_style(border_color, width_units=border_units),
        )
        if body_h > 0:
            Icon.draw_round_segment(
                (cx - w_half, y_bot), (cx - w_half, y_top), width_units=border_units, color=border_color
            )
            Icon.draw_round_segment(
                (cx + w_half, y_bot), (cx + w_half, y_top), width_units=border_units, color=border_color
            )

        ellipse((cx, y_top), width=width, height=eh, style=Icon.no_border_fill(top_color))
        arc(
            (cx, y_top),
            width=width,
            height=eh,
            angle_start=180.0,
            angle_end=360.0,
            style=Icon.stroke_style(seam_color, width_units=seam_units),
        )
        arc(
            (cx, y_top),
            width=width,
            height=eh,
            angle_start=0.0,
            angle_end=180.0,
            style=Icon.stroke_style(border_color, width_units=border_units),
        )

    @classmethod
    def draw_arrow(
        cls,
        xy1: tuple[float, float],
        xy2: tuple[float, float],
        *,
        shaft_w: float = 3.6,
        head_len: float = 7.5,
        head_w: float = 9.2,
        color: Any = Icon.WHITE,
    ) -> None:
        """Draw a crisp filled polygon arrow from xy1 to xy2."""
        x1, y1 = xy1
        x2, y2 = xy2
        dx = x2 - x1
        dy = y2 - y1
        dist = math.hypot(dx, dy)
        if dist < 1e-6:
            return
        ux = dx / dist
        uy = dy / dist
        nx = -uy
        ny = ux

        hl = min(head_len, dist * 0.65)
        bx = x2 - ux * hl
        by = y2 - uy * hl
        sh = shaft_w / 2.0
        hw = head_w / 2.0

        pts = [
            (x1 + nx * sh, y1 + ny * sh),
            (bx + nx * sh, by + ny * sh),
            (bx + nx * hw, by + ny * hw),
            (x2, y2),
            (bx - nx * hw, by - ny * hw),
            (bx - nx * sh, by - ny * sh),
            (x1 - nx * sh, y1 - ny * sh),
        ]
        polygon(pts, style=Icon.no_border_fill(color))

    @classmethod
    def draw_modern_badge(
        cls,
        *,
        color: Any = BLUE,
        border_color: Any = BORDER,
        border_units: float = 1.6,
    ) -> None:
        """Draw a standard 78x78 rounded-square badge for Modern 2D Cisco icons."""
        rectangle(
            (50.0, 50.0),
            width=78.0,
            height=78.0,
            style=Icon.fill_style(color, border_color=border_color, border_units=border_units, shape_r=16.0),
        )

    @classmethod
    def draw_sine_waves(
        cls,
        cx: float,
        cy: float,
        width: float,
        amp: float,
        *,
        cycles: float = 3.0,
        stroke_w: float = 2.8,
        color: Any = Icon.WHITE,
        steps: int = 48,
    ) -> None:
        """Draw the signature Cisco intertwined dual sine-wave symbol (used on Wireless APs)."""
        x_start = cx - width / 2.0
        pts1: list[tuple[float, float]] = []
        pts2: list[tuple[float, float]] = []
        for i in range(steps + 1):
            t = i / steps
            x = x_start + width * t
            ang = t * cycles * 2.0 * math.pi
            pts1.append((x, cy + amp * math.sin(ang)))
            pts2.append((x, cy - amp * math.sin(ang)))
        Icon.draw_round_polyline(pts1, width_units=stroke_w, color=color)
        Icon.draw_round_polyline(pts2, width_units=stroke_w, color=color)

    @classmethod
    def draw_router_top_arrows(
        cls,
        cx: float,
        cy: float,
        rx: float,
        ry: float,
        *,
        color: Any = Icon.WHITE,
    ) -> None:
        """Draw the classic 4 Cisco router arrows on a 3D top ellipse (2 inward horizontal, 2 outward vertical)."""
        cls.draw_arrow(
            (cx - rx * 0.78, cy),
            (cx - rx * 0.14, cy),
            shaft_w=ry * 0.25,
            head_len=rx * 0.24,
            head_w=ry * 0.62,
            color=color,
        )
        cls.draw_arrow(
            (cx + rx * 0.78, cy),
            (cx + rx * 0.14, cy),
            shaft_w=ry * 0.25,
            head_len=rx * 0.24,
            head_w=ry * 0.62,
            color=color,
        )
        cls.draw_arrow(
            (cx, cy + ry * 0.16),
            (cx, cy + ry * 0.82),
            shaft_w=rx * 0.095,
            head_len=ry * 0.36,
            head_w=rx * 0.25,
            color=color,
        )
        cls.draw_arrow(
            (cx, cy - ry * 0.16),
            (cx, cy - ry * 0.82),
            shaft_w=rx * 0.095,
            head_len=ry * 0.36,
            head_w=rx * 0.25,
            color=color,
        )

    @classmethod
    def draw_l3_star(
        cls,
        cx: float,
        cy: float,
        r_center: float,
        r_outer: float,
        *,
        shaft_w: float = 2.6,
        head_len: float = 5.2,
        head_w: float = 7.2,
        color: Any = Icon.WHITE,
    ) -> None:
        """Draw the signature Cisco Layer-3 center circle with 8 radial outward arrows."""
        circle((cx, cy), radius=r_center, style=Icon.no_border_fill(color))
        for k in range(8):
            ang = math.radians(k * 45.0)
            ux = math.cos(ang)
            uy = math.sin(ang)
            cls.draw_arrow(
                (cx + ux * (r_center * 0.85), cy + uy * (r_center * 0.85)),
                (cx + ux * r_outer, cy + uy * r_outer),
                shaft_w=shaft_w,
                head_len=head_len,
                head_w=head_w,
                color=color,
            )


class Dell:
    """Dell EMC server and storage color palette."""

    BLUE = "#0076CE"


class Vmware:
    """VMware virtualization and storage color palette."""

    NAVY = "#1D428A"
    CYAN = "#0091DA"
    GREEN = "#64B145"


class K8s:
    """Kubernetes palette and heptagon badge helpers."""

    BLUE = "#326CE5"

    _OUTER_RING: list[tuple[float, float]] = [
        (49.71, 90.75),
        (49.16, 90.69),
        (48.61, 90.58),
        (48.08, 90.42),
        (47.57, 90.2),
        (18.37, 76.25),
        (17.31, 75.59),
        (16.42, 74.72),
        (15.76, 73.66),
        (15.34, 72.49),
        (8.14, 41.15),
        (8.0, 40.05),
        (8.09, 38.95),
        (8.39, 37.89),
        (8.9, 36.9),
        (8.97, 36.79),
        (9.05, 36.68),
        (9.13, 36.57),
        (9.22, 36.46),
        (29.43, 11.33),
        (30.31, 10.45),
        (31.37, 9.79),
        (32.55, 9.38),
        (33.79, 9.25),
        (66.21, 9.25),
        (67.45, 9.39),
        (68.63, 9.8),
        (69.69, 10.46),
        (70.58, 11.33),
        (90.78, 36.47),
        (91.45, 37.52),
        (91.86, 38.69),
        (92.0, 39.92),
        (91.86, 41.15),
        (84.65, 72.5),
        (84.23, 73.67),
        (83.57, 74.72),
        (82.68, 75.6),
        (81.63, 76.26),
        (52.42, 90.21),
        (51.77, 90.47),
        (51.1, 90.65),
        (50.41, 90.74),
    ]

    _INNER_RING: list[tuple[float, float]] = [
        (49.72, 88.6),
        (49.2, 88.54),
        (48.68, 88.44),
        (48.18, 88.29),
        (47.7, 88.08),
        (20.03, 74.87),
        (19.03, 74.24),
        (18.19, 73.41),
        (17.56, 72.42),
        (17.17, 71.31),
        (10.35, 41.62),
        (10.21, 40.58),
        (10.29, 39.53),
        (10.58, 38.52),
        (11.06, 37.59),
        (11.14, 37.49),
        (11.21, 37.38),
        (11.29, 37.28),
        (11.36, 37.18),
        (30.51, 13.37),
        (31.35, 12.54),
        (32.35, 11.91),
        (33.47, 11.53),
        (34.65, 11.39),
        (65.35, 11.4),
        (66.53, 11.53),
        (67.65, 11.92),
        (68.65, 12.54),
        (69.49, 13.37),
        (88.63, 37.18),
        (89.26, 38.18),
        (89.65, 39.29),
        (89.79, 40.46),
        (89.65, 41.62),
        (82.82, 71.31),
        (82.43, 72.42),
        (81.8, 73.42),
        (80.96, 74.25),
        (79.96, 74.87),
        (52.29, 88.08),
        (51.68, 88.33),
        (51.04, 88.5),
        (50.38, 88.59),
    ]

    @classmethod
    def draw_heptagon(cls, *, fill_color: Any = BLUE, border_color: Any = Icon.WHITE) -> None:
        """Draw the official Kubernetes rounded heptagon badge with white outer rim."""
        polygon(cls._OUTER_RING, style=Icon.fill_style(border_color))
        polygon(cls._INNER_RING, style=Icon.fill_style(fill_color))

    @classmethod
    def draw_original_heptagon(
        cls,
        *,
        fill_color: Any = Icon.PASTEL_BLUE,
        border_color: Any = Icon.DARK,
        border_units: float = Icon.ORIG_STROKE,
    ) -> None:
        """Draw the Drawlib Original Kubernetes rounded heptagon badge with dark structural rim."""
        polygon(
            cls._INNER_RING,
            style=Icon.fill_style(fill_color, border_color=border_color, border_units=border_units),
        )


__all__ = [
    "Aws",
    "Azure",
    "Cisco",
    "Dell",
    "Gcp",
    "Icon",
    "K8s",
    "Vmware",
]
