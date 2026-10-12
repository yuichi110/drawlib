# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Canvas basic shapes and matplotlib patches feature implementation module."""

import math
from collections.abc import Callable
from typing import Any

from matplotlib.patches import (
    Arc,
    Circle,
    Ellipse,
    PathPatch,
    Polygon,
    RegularPolygon,
    Wedge,
)
from matplotlib.path import Path
from pydantic import validate_call

from drawlib._core.l2_types import (
    Angle,
    BraceDirection,
    BraceSymbol,
    CheckmarkVariant,
    ClockVariant,
    CloudVariant,
    Coordinate,
    Coordinates,
    DocumentVariant,
    FaceVariant,
    ForbiddenVariant,
    FunnelVariant,
    HeartVariant,
    MoonVariant,
    NumVertex,
    PathPoints,
    PinVariant,
    PosFloat,
    PosInt,
    Ratio,
    RibbonVariant,
    ShieldVariant,
    Size,
    SunVariant,
)
from drawlib._core.l3_colors import ColorUtil
from drawlib._core.l3_math import get_center_and_size
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas._base import CanvasBase
from drawlib._core.l4_canvas._shapes._basic_ext import (
    build_checkmark_path,
    build_clock_patches,
    build_forbidden_path,
    build_funnel_patches,
    build_heart_path,
    build_moon_path,
    build_pin_path_and_center,
    build_ribbon_patches,
    build_shield_path,
    build_sun_path,
)
from drawlib._core.l4_canvas._shapes._util import ShapeUtil


def _get_cylinder_fill_colors(
    style: Style,
) -> tuple[tuple[float, float, float, float] | str, tuple[float, float, float, float] | str]:
    """Get body fill and top cap fill colors for cylinder.

    Args:
        style: Shape style object.

    Returns:
        A tuple of (body_fill, top_fill) formatted for matplotlib.
    """
    if style.shape_fill_color is None:
        return "none", "none"
    raw_fill = ColorUtil.get_mplot_rgba(style.shape_fill_color, alpha=style.alpha)
    if raw_fill[3] <= 0.0:
        return "none", "none"
    top_fill = (
        min(1.0, raw_fill[0] + (1.0 - raw_fill[0]) * 0.28),
        min(1.0, raw_fill[1] + (1.0 - raw_fill[1]) * 0.28),
        min(1.0, raw_fill[2] + (1.0 - raw_fill[2]) * 0.28),
        raw_fill[3],
    )
    return raw_fill, top_fill


def _build_cylinder_disk_patches(
    cx: float,
    cy: float,
    hw: float,
    hh: float,
    hr: float,
    ky: float,
    kx: float,
    disks: int,
    cos_a: float,
    sin_a: float,
    stroke_color: tuple[float, float, float, float] | str,
    line_w: float,
    line_style: str,
    has_stroke: bool,
) -> list[PathPatch]:
    """Generate divider curve patches for multi-disk cylinders.

    Args:
        cx: Center x coordinate.
        cy: Center y coordinate.
        hw: Half width.
        hh: Half height of cylinder body.
        hr: Half radius (vertical radius of cap ellipse).
        ky: Vertical control point delta for Bezier curve.
        kx: Horizontal control point delta for Bezier curve.
        disks: Number of disks.
        cos_a: Cosine of rotation angle.
        sin_a: Sine of rotation angle.
        stroke_color: Line color for stroke.
        line_w: Line width.
        line_style: Line style.
        has_stroke: Whether shape has line stroke.

    Returns:
        List of PathPatch objects representing disk divider curves.
    """
    if disks <= 1 or hh <= 0:
        return []

    d_color = stroke_color if has_stroke else (1.0, 1.0, 1.0, 0.7)
    d_w = line_w if has_stroke else 1.5
    step_h = (2 * hh) / disks
    d_codes = [
        Path.MOVETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
    ]
    patches: list[PathPatch] = []

    for i in range(1, disks):
        dy = -hh + i * step_h
        d_verts = [
            (-hw, dy),
            (-hw, dy - ky),
            (-kx, dy - hr),
            (0, dy - hr),
            (kx, dy - hr),
            (hw, dy - ky),
            (hw, dy),
        ]
        world_verts = [(cx + vx * cos_a - vy * sin_a, cy + vx * sin_a + vy * cos_a) for vx, vy in d_verts]
        patches.append(
            PathPatch(
                Path(vertices=world_verts, codes=d_codes),
                facecolor="none",
                edgecolor=d_color,
                linewidth=d_w,
                linestyle=line_style,
                zorder=1,
            )
        )
    return patches


class CanvasShapeBasicFeature(CanvasBase):
    """A feature class for drawing basic geometrical shapes and matplotlib patches on a canvas."""

    def __init__(self) -> None:
        """Initializes a CanvasShapeBasicFeature object."""
        super().__init__()

    @validate_call
    def shape(
        self,
        xy: Coordinate,
        path_points: PathPoints,
        *,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
        is_default_center: bool = False,
    ) -> None:
        """Draw basic shape on the canvas.

        Args:
            xy: Starting point of the shape.
            path_points: List of path points including control points for Bezier curves.
            style: Style of the shape (required).
            text (str, optional): Text to display along with the shape.
            text_style (Style | None, optional): Style of the text.
            is_default_center (bool, optional): Whether to place (xy) at the center of the shape.

        Raises:
            ValueError: If invalid path points are provided.
        """
        style, text_style = ShapeUtil.format_styles(
            style,
            text_style,
        )
        angle: Angle = style.angle if style.angle is not None else 0.0

        transformed_points, (cx, cy), effective_style = ShapeUtil.transform_shape_path_points(
            xy=xy,
            path_points=path_points,
            angle=angle,
            style=style,
            is_default_center=is_default_center,
        )

        path = ShapeUtil.build_matplotlib_path(transformed_points)
        options = ShapeUtil.get_shape_options(effective_style)
        self._artists.append(PathPatch(path=path, **options))

        if text:
            effective_text_style = ShapeUtil.resolve_embedded_text_style(effective_style, text_style)
            self._artists.append(
                ShapeUtil.get_shape_text(
                    xy=(cx, cy),
                    text=text,
                    angle=angle,
                    style=effective_text_style,
                )
            )

    def _draw_convex_polygon_with_hole(
        self,
        xy: Coordinate,
        vertices: list[Coordinate],
        hole_ratio: float | None,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
        is_default_center: bool = False,
    ) -> None:
        """Draw a convex polygon with optional inner hole_ratio cutout and corner rounding."""
        if hole_ratio is None:
            path_points = ShapeUtil.round_polygon_points(vertices, style.shape_r)
            self.shape(
                xy=xy,
                path_points=path_points,
                style=style,
                text=text,
                text_style=text_style,
                is_default_center=is_default_center,
            )
            return

        style, text_style = ShapeUtil.format_styles(style, text_style)
        h_ratio = float(ShapeUtil.validate_hole_ratio(hole_ratio) or 0.5)
        angle: Angle = style.angle if style.angle is not None else 0.0

        inner_local_verts, inset = ShapeUtil.inset_convex_polygon(vertices, h_ratio)
        outer_points = ShapeUtil.round_polygon_points(vertices, style.shape_r)
        inner_shape_r = ShapeUtil.shrink_shape_r(style.shape_r, inset, reversed_order=True)
        inner_points = ShapeUtil.round_polygon_points(inner_local_verts, inner_shape_r)

        orig_center, (width, height) = get_center_and_size(vertices)
        centered_outer = [ShapeUtil._shift_path_point(p, orig_center) for p in outer_points]
        centered_inner = [ShapeUtil._shift_path_point(p, orig_center) for p in inner_points]

        align_xy = (xy[0] - width / 2.0, xy[1] - height / 2.0) if is_default_center else xy
        (adj_x, adj_y), effective_style = ShapeUtil.apply_alignment(
            align_xy,
            width=width,
            height=height,
            angle=angle,
            style=style,
            is_default_center=is_default_center,
        )
        center_xy = (adj_x + width / 2.0, adj_y + height / 2.0)

        transformed_outer = [
            ShapeUtil._rotate_and_place_path_point(p, angle, center_xy) for p in centered_outer
        ]
        transformed_inner = [
            ShapeUtil._rotate_and_place_path_point(p, angle, center_xy) for p in centered_inner
        ]

        outer_path = ShapeUtil.build_matplotlib_path(transformed_outer)
        inner_path = ShapeUtil.build_matplotlib_path(transformed_inner)
        compound_path = Path.make_compound_path(outer_path, inner_path)

        options = ShapeUtil.get_shape_options(effective_style)
        self._artists.append(PathPatch(path=compound_path, **options))

        if text:
            effective_text_style = ShapeUtil.resolve_embedded_text_style(effective_style, text_style)
            self._artists.append(
                ShapeUtil.get_shape_text(
                    xy=center_xy,
                    text=text,
                    angle=angle,
                    style=effective_text_style,
                )
            )

    @validate_call
    def rectangle(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        *,
        hole_ratio: Ratio | None = None,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a rectangle on the canvas.

        Args:
            xy: Center or aligned coordinate of the rectangle.
            width: Width of the rectangle.
            height: Height of the rectangle.
            hole_ratio: Optional inner cutout hole ratio in (0.0, 1.0) for frame shapes.
            style: Style of the rectangle (required).
            text (str, optional): Text to display within the rectangle.
            text_style (Style | None, optional): Style of the text.

        Raises:
            ValueError: If invalid path points, hole_ratio, or shape_r are provided.
        """
        style, text_style = ShapeUtil.format_styles(
            style,
            text_style,
        )

        p1 = (0, 0)
        p2 = (0, height)
        p3 = (width, height)
        p4 = (width, 0)
        self._draw_convex_polygon_with_hole(
            xy=xy,
            vertices=[p1, p2, p3, p4],
            hole_ratio=hole_ratio,
            style=style,
            text=text,
            text_style=text_style,
        )

    @validate_call
    def polygon(
        self,
        xys: Coordinates,
        *,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a polygon on the canvas.

        Args:
            xys: List of vertices [(x1, y1), ...(x_n, y_n)].
            style: Style of the polygon (required).
            text (optional): Text shown at the center of the polygon.
            text_style (optional): Style of the text.

        Returns:
            None
        """
        style, text_style = ShapeUtil.format_styles(
            style,
            text_style,
        )

        path_points = ShapeUtil.round_polygon_points(list(xys), style.shape_r)
        style = style.patch(halign=None, valign=None)
        options = ShapeUtil.get_shape_options(style)
        if len(path_points) == len(xys) and all(isinstance(p[0], (int, float)) for p in path_points):
            self._artists.append(Polygon(xy=xys, closed=True, **options))
        else:
            path = ShapeUtil.build_matplotlib_path(path_points)
            self._artists.append(PathPatch(path=path, **options))

        if not text:
            return
        effective_text_style = ShapeUtil.resolve_embedded_text_style(style, text_style)
        center, (_, _) = get_center_and_size(xys)
        self._artists.append(
            ShapeUtil.get_shape_text(
                center,
                text=text,
                angle=0,
                style=effective_text_style,
            ),
        )


    @validate_call
    def arc(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        *,
        style: Style,
        angle_start: Angle = 0.0,
        angle_end: Angle = 360.0,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw an arc on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            width: Width of arc.
            height: Height of arc.
            style: Style object (required).
            angle_start: Starting angle in degrees.
            angle_end: Ending angle in degrees.
            text: Text to display inside shape.
            text_style: Style object for text.
        """
        style, text_style = ShapeUtil.format_styles(
            style,
            text_style,
        )
        angle: Angle = style.angle if style.angle is not None else 0.0

        xy, style = ShapeUtil.apply_alignment(xy, width, height, angle, style, is_default_center=True)
        options = ShapeUtil.get_shape_options(style)
        self._artists.append(
            Arc(
                xy,
                width=width,
                height=height,
                angle=angle,
                theta1=angle_start,
                theta2=angle_end,
                **options,
            )
        )

        if not text:
            return
        effective_text_style = ShapeUtil.resolve_embedded_text_style(style, text_style)
        self._artists.append(
            ShapeUtil.get_shape_text(
                xy=xy,
                text=text,
                angle=angle,
                style=effective_text_style,
            ),
        )

    @validate_call
    def circle(
        self,
        xy: Coordinate,
        radius: PosFloat,
        *,
        hole_ratio: Ratio | None = None,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a circle or hollow ring on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            radius: Outer radius of the circle.
            hole_ratio: Optional inner cutout hole ratio in (0.0, 1.0) for ring/donut shapes.
            style: Style object (required).
            text: Text to display inside shape.
            text_style: Style object for text.
        """
        style, text_style = ShapeUtil.format_styles(
            style,
            text_style,
        )
        h_ratio = ShapeUtil.validate_hole_ratio(hole_ratio)
        angle: Angle = style.angle if style.angle is not None else 0.0

        width = radius * 2
        height = radius * 2
        xy, style = ShapeUtil.apply_alignment(xy, width, height, angle, style, is_default_center=True)
        options = ShapeUtil.get_shape_options(style)
        if h_ratio is None:
            self._artists.append(
                Circle(
                    xy=xy,
                    radius=radius,
                    **options,
                ),
            )
        else:
            path = ShapeUtil.build_hollow_ellipse_path(
                cx=xy[0],
                cy=xy[1],
                rx=radius,
                ry=radius,
                hole_ratio=h_ratio,
                angle=angle,
            )
            self._artists.append(PathPatch(path=path, **options))

        if not text:
            return
        effective_text_style = ShapeUtil.resolve_embedded_text_style(style, text_style)
        self._artists.append(
            ShapeUtil.get_shape_text(
                xy=xy,
                text=text,
                angle=angle,
                style=effective_text_style,
            ),
        )

    @validate_call
    def ellipse(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        *,
        hole_ratio: Ratio | None = None,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw an ellipse or hollow oval ring on the canvas.

        Args:
            xy: Center coordinates (x, y) of the ellipse.
            width: Width (horizontal axis) of the ellipse.
            height: Height (vertical axis) of the ellipse.
            hole_ratio: Optional inner cutout hole ratio in (0.0, 1.0).
            style: Style of the ellipse (required).
            text (optional): Text to display inside the ellipse.
            text_style (optional): Style of the text.
        """
        style, text_style = ShapeUtil.format_styles(
            style,
            text_style,
        )
        h_ratio = ShapeUtil.validate_hole_ratio(hole_ratio)
        angle: Angle = style.angle if style.angle is not None else 0.0

        xy, style = ShapeUtil.apply_alignment(
            xy=xy,
            width=width,
            height=height,
            angle=angle,
            style=style,
            is_default_center=True,
        )

        options = ShapeUtil.get_shape_options(style)
        if h_ratio is None:
            self._artists.append(
                Ellipse(
                    xy,
                    width=width,
                    height=height,
                    angle=angle,
                    **options,
                )
            )
        else:
            path = ShapeUtil.build_hollow_ellipse_path(
                cx=xy[0],
                cy=xy[1],
                rx=width / 2.0,
                ry=height / 2.0,
                hole_ratio=h_ratio,
                angle=angle,
            )
            self._artists.append(PathPatch(path=path, **options))

        if not text:
            return
        effective_text_style = ShapeUtil.resolve_embedded_text_style(style, text_style)
        self._artists.append(
            ShapeUtil.get_shape_text(
                xy=xy,
                text=text,
                angle=angle,
                style=effective_text_style,
            ),
        )

    @validate_call
    def regularpolygon(
        self,
        xy: Coordinate,
        num_vertex: NumVertex,
        radius: PosFloat,
        *,
        hole_ratio: Ratio | None = None,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a regular polygon on the canvas.

        Args:
            xy: Center coordinates (x, y) of the regular polygon.
            num_vertex: Number of vertices in the polygon.
            radius: Radius of the circumscribed circle.
            hole_ratio: Optional inner cutout hole ratio in (0.0, 1.0).
            style: Style of the polygon (required).
            text (optional): Text to display inside the polygon.
            text_style (optional): Style of the text.
        """
        style, text_style = ShapeUtil.format_styles(
            style,
            text_style,
        )
        h_ratio = ShapeUtil.validate_hole_ratio(hole_ratio)
        angle: Angle = style.angle if style.angle is not None else 0.0

        xy, style = ShapeUtil.apply_alignment(
            xy=xy,
            width=radius * 2,
            height=radius * 2,
            angle=angle,
            style=style,
            is_default_center=True,
        )

        angle_rad = math.radians(angle)
        options = ShapeUtil.get_shape_options(style)
        if h_ratio is not None or style.shape_r is not None:
            start_a = math.pi / 2.0 + angle_rad
            verts: list[Coordinate] = [
                (
                    xy[0] + radius * math.cos(start_a + i * 2.0 * math.pi / num_vertex),
                    xy[1] + radius * math.sin(start_a + i * 2.0 * math.pi / num_vertex),
                )
                for i in range(num_vertex)
            ]
            path_points = ShapeUtil.round_polygon_points(verts, style.shape_r)
            if h_ratio is not None:
                inner_verts, inset = ShapeUtil.inset_convex_polygon(verts, h_ratio)
                inner_r = ShapeUtil.shrink_shape_r(style.shape_r, inset, reversed_order=True)
                inner_points = ShapeUtil.round_polygon_points(inner_verts, inner_r)
                outer_path = ShapeUtil.build_matplotlib_path(path_points)
                inner_path = ShapeUtil.build_matplotlib_path(inner_points)
                path = Path.make_compound_path(outer_path, inner_path)
                self._artists.append(PathPatch(path=path, **options))
            elif len(path_points) == num_vertex and all(isinstance(p[0], (int, float)) for p in path_points):
                self._artists.append(
                    RegularPolygon(
                        xy,
                        numVertices=num_vertex,
                        radius=radius,
                        orientation=angle_rad,
                        **options,
                    )
                )
            else:
                path = ShapeUtil.build_matplotlib_path(path_points)
                self._artists.append(PathPatch(path=path, **options))
        else:
            self._artists.append(
                RegularPolygon(
                    xy,
                    numVertices=num_vertex,
                    radius=radius,
                    orientation=angle_rad,
                    **options,
                )
            )

        if not text:
            return
        effective_text_style = ShapeUtil.resolve_embedded_text_style(style, text_style)
        self._artists.append(
            ShapeUtil.get_shape_text(
                xy=xy,
                text=text,
                angle=angle,
                style=effective_text_style,
            ),
        )

    @validate_call
    def wedge(
        self,
        xy: Coordinate,
        radius: PosFloat,
        *,
        style: Style,
        width: PosFloat | None = None,
        angle_start: Angle = 0,
        angle_end: Angle = 360,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a wedge shape on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            radius: Outer radius of the wedge.
            style: Style object (required).
            width: Width of the wedge ring (inner radius = radius - width).
            angle_start: Starting theta angle in degrees.
            angle_end: Ending theta angle in degrees.
            text: Text to display inside shape.
            text_style: Style object for text.
        """
        style, text_style = ShapeUtil.format_styles(
            style,
            text_style,
        )
        angle: Angle = style.angle if style.angle is not None else 0.0

        ext_width = radius * 2
        ext_height = radius * 2
        xy, style = ShapeUtil.apply_alignment(xy, ext_width, ext_height, angle, style, is_default_center=True)
        options = ShapeUtil.get_shape_options(style)
        self._artists.append(
            Wedge(
                center=xy,
                r=radius,
                width=width,
                theta1=angle_start + angle,
                theta2=angle_end + angle,
                **options,
            )
        )

        if not text:
            return
        effective_text_style = ShapeUtil.resolve_embedded_text_style(style, text_style)
        self._artists.append(
            ShapeUtil.get_shape_text(
                xy=xy,
                text=text,
                angle=angle,
                style=effective_text_style,
            ),
        )

    @validate_call
    def fan(
        self,
        xy: Coordinate,
        radius: PosFloat,
        *,
        style: Style,
        angle_start: Angle = 0,
        angle_end: Angle = 180,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a fan shape on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            radius: Radius of the fan.
            style: Style object (required).
            angle_start: Starting theta angle in degrees.
            angle_end: Ending theta angle in degrees.
            text: Text to display inside shape.
            text_style: Style object for text.
        """
        self.wedge(
            xy=xy,
            radius=radius,
            width=None,
            angle_start=angle_start,
            angle_end=angle_end,
            style=style,
            text=text,
            text_style=text_style,
        )

    @validate_call
    def cylinder(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        *,
        style: Style,
        disks: PosInt = 1,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a 3D cylinder shape on the canvas.

        Args:
            xy: Center coordinates (x, y) of the cylinder.
            width: Width of the cylinder.
            height: Height of the cylinder.
            style: Style object (required).
            disks: Number of stacked disks (default is 1).
            text: Text to display inside shape.
            text_style: Style object for text.
        """
        style, text_style = ShapeUtil.format_styles(
            style,
            text_style,
        )
        angle: Angle = style.angle if style.angle is not None else 0.0

        if width <= 0 or height <= 0:
            raise ValueError(f"width and height must be positive, but got width={width}, height={height}.")
        if disks < 1:
            raise ValueError(f"disks must be >= 1, but got {disks}.")

        xy, style = ShapeUtil.apply_alignment(
            xy=xy,
            width=width,
            height=height,
            angle=angle,
            style=style,
            is_default_center=True,
        )
        cx, cy = xy

        eh = min(width * 0.35, height * 0.35)
        hw = width / 2.0
        hh = max(0.0, (height - eh) / 2.0)
        hr = eh / 2.0

        kappa = 0.5522847498307936
        kx = hw * kappa
        ky = hr * kappa

        rad = math.radians(angle)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)

        def xform(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
            return [(cx + vx * cos_a - vy * sin_a, cy + vx * sin_a + vy * cos_a) for vx, vy in pts]

        # 1. Seamless body path (sides + bottom curve + top inner seam)
        b_verts = [
            (-hw, hh),
            (-hw, -hh),
            (-hw, -hh - ky),
            (-kx, -hh - hr),
            (0, -hh - hr),
            (kx, -hh - hr),
            (hw, -hh - ky),
            (hw, -hh),
            (hw, hh),
            (hw, hh - ky),
            (kx, hh - hr),
            (0, hh - hr),
            (-kx, hh - hr),
            (-hw, hh - ky),
            (-hw, hh),
        ]
        b_codes = [
            Path.MOVETO,
            Path.LINETO,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.LINETO,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CLOSEPOLY,
        ]
        b_verts.append((-hw, hh))
        body_path = Path(vertices=xform(b_verts), codes=b_codes)

        # 2. Top cap path (full ellipse at +hh)
        t_verts = [
            (hw, hh),
            (hw, hh + ky),
            (kx, hh + hr),
            (0, hh + hr),
            (-kx, hh + hr),
            (-hw, hh + ky),
            (-hw, hh),
            (-hw, hh - ky),
            (-kx, hh - hr),
            (0, hh - hr),
            (kx, hh - hr),
            (hw, hh - ky),
            (hw, hh),
        ]
        t_codes = [
            Path.MOVETO,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CLOSEPOLY,
        ]
        t_verts.append((hw, hh))
        top_path = Path(vertices=xform(t_verts), codes=t_codes)

        line_w = style.shape_line_width if style.shape_line_width is not None else 0.0
        has_stroke = style.shape_line_color is not None and line_w > 0
        line_style = style.shape_line_style if style.shape_line_style is not None else "solid"

        m_fill, top_fill = _get_cylinder_fill_colors(style)
        stroke_color = ColorUtil.get_mplot_rgba(style.shape_line_color) if has_stroke else "none"

        body_patch = PathPatch(body_path, facecolor=m_fill, edgecolor="none", linewidth=0, zorder=1)
        top_patch = PathPatch(
            top_path,
            facecolor=top_fill,
            edgecolor=stroke_color if has_stroke else "none",
            linewidth=line_w,
            linestyle=line_style,
            zorder=1,
        )
        self._artists.append(body_patch)
        self._artists.append(top_patch)

        if has_stroke:
            out_verts = [
                (-hw, hh),
                (-hw, -hh),
                (-hw, -hh - ky),
                (-kx, -hh - hr),
                (0, -hh - hr),
                (kx, -hh - hr),
                (hw, -hh - ky),
                (hw, -hh),
                (hw, hh),
            ]
            out_codes = [
                Path.MOVETO,
                Path.LINETO,
                Path.CURVE4,
                Path.CURVE4,
                Path.CURVE4,
                Path.CURVE4,
                Path.CURVE4,
                Path.CURVE4,
                Path.LINETO,
            ]
            out_path = Path(vertices=xform(out_verts), codes=out_codes)
            out_patch = PathPatch(
                out_path,
                facecolor="none",
                edgecolor=stroke_color,
                linewidth=line_w,
                linestyle=line_style,
                zorder=1,
            )
            self._artists.append(out_patch)

        self._artists.extend(
            _build_cylinder_disk_patches(
                cx=cx,
                cy=cy,
                hw=hw,
                hh=hh,
                hr=hr,
                ky=ky,
                kx=kx,
                disks=disks,
                cos_a=cos_a,
                sin_a=sin_a,
                stroke_color=stroke_color,
                line_w=line_w,
                line_style=line_style,
                has_stroke=has_stroke,
            )
        )

        if text:
            effective_text_style = ShapeUtil.resolve_embedded_text_style(style, text_style)
            self._artists.append(
                ShapeUtil.get_shape_text(
                    xy=xy,
                    text=text,
                    angle=angle,
                    style=effective_text_style,
                )
            )

    @validate_call
    def face(
        self,
        xy: Coordinate,
        radius: PosFloat,
        *,
        variant: FaceVariant = "smile",
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw an expressive face shape on the canvas.

        Args:
            xy: Center coordinates (x, y) of the face circle.
            radius: Radius of the face circle.
            variant: Facial expression or silhouette ("smile", "neutral", "sad",
                "angry", "surprised", "dizzy", "dead", "skull", or "devil").
            style: Style object (required).
            text: Text to display inside shape.
            text_style: Style object for text.
        """
        style, text_style = ShapeUtil.format_styles(
            style,
            text_style,
        )
        angle: Angle = style.angle if style.angle is not None else 0.0

        if radius <= 0:
            raise ValueError(f"radius must be positive, but got radius={radius}.")

        width = radius * 2.0
        height = radius * 2.0
        xy, style = ShapeUtil.apply_alignment(
            xy=xy,
            width=width,
            height=height,
            angle=angle,
            style=style,
            is_default_center=True,
        )
        cx, cy = xy

        face_fill, stroke_color, feature_color, feature_w = _get_face_colors(style)
        line_w = style.shape_line_width if style.shape_line_width is not None else 0.0
        line_style = style.shape_line_style if style.shape_line_style is not None else "solid"

        rad = math.radians(angle)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)

        self._artists.append(
            _build_face_head_patch(
                cx=cx,
                cy=cy,
                radius=radius,
                variant=variant,
                cos_a=cos_a,
                sin_a=sin_a,
                face_fill=face_fill,
                stroke_color=stroke_color,
                line_w=line_w,
                line_style=line_style,
            )
        )

        self._artists.extend(
            _build_face_feature_patches(
                cx=cx,
                cy=cy,
                radius=radius,
                variant=variant,
                cos_a=cos_a,
                sin_a=sin_a,
                feature_color=feature_color,
                feature_w=feature_w,
            )
        )

        if text:
            effective_text_style = ShapeUtil.resolve_embedded_text_style(style, text_style)
            self._artists.append(
                ShapeUtil.get_shape_text(
                    xy=xy,
                    text=text,
                    angle=angle,
                    style=effective_text_style,
                )
            )

    @validate_call
    def cloud(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        *,
        variant: CloudVariant = "standard",
        bump_ratio: Ratio | None = None,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a cloud shape on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            width: Width of the cloud bounding box.
            height: Height of the cloud bounding box.
            variant: Cloud silhouette variant ("standard", "flat", "fluffy", "simple").
            bump_ratio: Optional bulge depth ratio in (0.0, 1.0).
            style: Style object (required).
            text: Text to display inside shape.
            text_style: Style object for text.

        Raises:
            ValueError: If width, height, or bump_ratio are out of valid bounds.
        """
        style, text_style = ShapeUtil.format_styles(style, text_style)
        if width <= 0.0 or height <= 0.0:
            raise ValueError("width and height must be positive.")
        if bump_ratio is not None and not (0.0 < bump_ratio < 1.0):
            raise ValueError("bump_ratio must be strictly between 0.0 and 1.0.")

        angle: Angle = style.angle if style.angle is not None else 0.0
        xy, style = ShapeUtil.apply_alignment(
            xy=xy,
            width=width,
            height=height,
            angle=angle,
            style=style,
            is_default_center=True,
        )

        path = _build_cloud_path(
            xy=xy,
            width=width,
            height=height,
            variant=variant,
            bump_ratio=bump_ratio,
            angle=angle,
        )
        options = ShapeUtil.get_shape_options(style)
        self._artists.append(PathPatch(path=path, **options))

        if text:
            effective_text_style = ShapeUtil.resolve_embedded_text_style(style, text_style)
            self._artists.append(
                ShapeUtil.get_shape_text(
                    xy=xy,
                    text=text,
                    angle=angle,
                    style=effective_text_style,
                )
            )

    @validate_call
    def brace(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        *,
        symbol: BraceSymbol = "{",
        direction: BraceDirection | None = None,
        tip_ratio: Ratio | None = None,
        tip_position_ratio: Ratio | None = None,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a curly, square, or round brace shape on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            width: Width of the brace bounding box.
            height: Height of the brace bounding box.
            symbol: Brace symbol ("{", "}", "{}", "curly", "[", "]", "[]", "square", "(", ")", "()", "round").
            direction: Orientation direction ("left", "right", "top", "bottom") or None.
            tip_ratio: Optional center tip depth ratio in (0.0, 1.0) for curly braces.
            tip_position_ratio: Optional center tip span position ratio in (0.0, 1.0) for curly braces.
            style: Style object (controls line_width, line_color, line_style, shape_r, and angle).
            text: Text to display inside shape.
            text_style: Style object for text.

        Raises:
            ValueError: If width, height, tip_ratio, or tip_position_ratio are out of valid bounds.
        """
        style, text_style = _format_brace_styles(style, text_style)
        if width <= 0.0 or height <= 0.0:
            raise ValueError("width and height must be positive.")
        if tip_ratio is not None and not (0.0 < tip_ratio < 1.0):
            raise ValueError("tip_ratio must be strictly between 0.0 and 1.0.")
        if tip_position_ratio is not None and not (0.0 < tip_position_ratio < 1.0):
            raise ValueError("tip_position_ratio must be strictly between 0.0 and 1.0.")

        angle: Angle = style.angle if style.angle is not None else 0.0
        xy, style = ShapeUtil.apply_alignment(
            xy=xy,
            width=width,
            height=height,
            angle=angle,
            style=style,
            is_default_center=True,
        )

        shape_r_scalar = style.shape_r if isinstance(style.shape_r, (int, float)) else None
        path = _build_brace_path(
            xy=xy,
            width=width,
            height=height,
            symbol=symbol,
            direction=direction,
            tip_ratio=tip_ratio,
            tip_position_ratio=tip_position_ratio,
            shape_r=shape_r_scalar,
            angle=angle,
        )
        options = _get_brace_stroke_options(style)
        self._artists.append(PathPatch(path=path, **options))

        if text:
            effective_text_style = ShapeUtil.resolve_embedded_text_style(style, text_style)
            self._artists.append(
                ShapeUtil.get_shape_text(
                    xy=xy,
                    text=text,
                    angle=angle,
                    style=effective_text_style,
                )
            )

    @validate_call
    def cube(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        *,
        depth_ratio: Ratio | None = None,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a 3D cube or rectangular box shape on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            width: Outer width of the cube bounding box.
            height: Outer height of the cube bounding box.
            depth_ratio: Optional 3D depth fraction in (0.0, 1.0) relative to min(width, height).
            style: Style object (required).
            text: Text to display on the front face of the cube.
            text_style: Style object for text.

        Raises:
            ValueError: If width, height, or depth_ratio are out of valid bounds.
        """
        style, text_style = ShapeUtil.format_styles(style, text_style)
        if width <= 0.0 or height <= 0.0:
            raise ValueError("width and height must be positive.")
        if depth_ratio is not None and not (0.0 < depth_ratio < 1.0):
            raise ValueError("depth_ratio must be strictly between 0.0 and 1.0.")

        angle: Angle = style.angle if style.angle is not None else 0.0
        xy, style = ShapeUtil.apply_alignment(
            xy=xy,
            width=width,
            height=height,
            angle=angle,
            style=style,
            is_default_center=True,
        )

        patches, text_xy = _build_cube_patches(
            xy=xy,
            width=width,
            height=height,
            depth_ratio=depth_ratio,
            angle=angle,
            style=style,
        )
        self._artists.extend(patches)

        if text:
            effective_text_style = ShapeUtil.resolve_embedded_text_style(style, text_style)
            self._artists.append(
                ShapeUtil.get_shape_text(
                    xy=text_xy,
                    text=text,
                    angle=angle,
                    style=effective_text_style,
                )
            )

    @validate_call
    def document(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        *,
        variant: DocumentVariant = "wave",
        stacked: PosInt = 1,
        wave_ratio: Ratio | None = None,
        fold_ratio: Ratio | None = None,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a wavy-bottom or folded-corner document shape on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            width: Outer width of the document bounding box.
            height: Outer height of the document bounding box.
            variant: Document silhouette ("wave", "standard", "folded", "page", "note",
                "double_wave", "snippet", "folded_wave", "report").
            stacked: Number of stacked document sheets (default is 1).
            wave_ratio: Optional wave amplitude ratio in (0.0, 1.0).
            fold_ratio: Optional top-right corner fold size ratio in (0.0, 1.0).
            style: Style object (required).
            text: Text to display on the front document sheet.
            text_style: Style object for text.

        Raises:
            ValueError: If dimensions, stacked count, or ratios are out of valid bounds.
        """
        style, text_style = ShapeUtil.format_styles(style, text_style)
        if width <= 0.0 or height <= 0.0:
            raise ValueError("width and height must be positive.")
        if stacked < 1:
            raise ValueError("stacked must be >= 1.")
        if wave_ratio is not None and not (0.0 < wave_ratio < 1.0):
            raise ValueError("wave_ratio must be strictly between 0.0 and 1.0.")
        if fold_ratio is not None and not (0.0 < fold_ratio < 1.0):
            raise ValueError("fold_ratio must be strictly between 0.0 and 1.0.")

        angle: Angle = style.angle if style.angle is not None else 0.0
        xy, style = ShapeUtil.apply_alignment(
            xy=xy,
            width=width,
            height=height,
            angle=angle,
            style=style,
            is_default_center=True,
        )

        patches, text_xy = _build_document_patches(
            xy=xy,
            width=width,
            height=height,
            variant=variant,
            stacked=stacked,
            wave_ratio=wave_ratio,
            fold_ratio=fold_ratio,
            angle=angle,
            style=style,
        )
        self._artists.extend(patches)

        if text:
            effective_text_style = ShapeUtil.resolve_embedded_text_style(style, text_style)
            self._artists.append(
                ShapeUtil.get_shape_text(
                    xy=text_xy,
                    text=text,
                    angle=angle,
                    style=effective_text_style,
                )
            )

    @validate_call
    def forbidden(
        self,
        xy: Coordinate,
        radius: PosFloat,
        *,
        variant: ForbiddenVariant = "slash",
        thickness_ratio: Ratio | None = None,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a forbidden or no-entry mark shape on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            radius: Outer radius of the forbidden circle.
            variant: Visual variant ("slash", "standard", "backslash", "cross", "no_entry", "minus").
            thickness_ratio: Optional ring/bar thickness ratio in (0.0, 1.0).
            style: Style object (required).
            text: Text to display inside shape.
            text_style: Style object for text.
        """
        ShapeUtil.validate_hole_ratio(thickness_ratio)
        style, text_style = ShapeUtil.format_styles(style, text_style)
        angle: Angle = style.angle if style.angle is not None else 0.0
        width = radius * 2.0
        xy, style = ShapeUtil.apply_alignment(
            xy=xy,
            width=width,
            height=width,
            angle=angle,
            style=style,
            is_default_center=True,
        )
        path = build_forbidden_path(xy, radius, variant, thickness_ratio, angle)
        options = ShapeUtil.get_shape_options(style)
        self._artists.append(PathPatch(path=path, **options))
        if text:
            effective_text_style = ShapeUtil.resolve_embedded_text_style(style, text_style)
            self._artists.append(
                ShapeUtil.get_shape_text(xy=xy, text=text, angle=angle, style=effective_text_style)
            )

    @validate_call
    def checkmark(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat | None = None,
        *,
        variant: CheckmarkVariant = "standard",
        thickness_ratio: Ratio | None = None,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a checkmark symbol or badge shape on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            width: Width of the checkmark bounding box.
            height: Height of the checkmark bounding box (defaults to width when None).
            variant: Checkmark variant ("standard", "check", "circle", "solid_circle").
            thickness_ratio: Optional stroke thickness ratio in (0.0, 1.0).
            style: Style object (required).
            text: Text to display inside shape.
            text_style: Style object for text.
        """
        ShapeUtil.validate_hole_ratio(thickness_ratio)
        style, text_style = ShapeUtil.format_styles(style, text_style)
        eff_h = width if height is None else height
        angle: Angle = style.angle if style.angle is not None else 0.0
        xy, style = ShapeUtil.apply_alignment(
            xy=xy,
            width=width,
            height=eff_h,
            angle=angle,
            style=style,
            is_default_center=True,
        )
        path = build_checkmark_path(xy, width, eff_h, variant, thickness_ratio, style.shape_r, angle)
        options = ShapeUtil.get_shape_options(style)
        self._artists.append(PathPatch(path=path, **options))
        if text:
            effective_text_style = ShapeUtil.resolve_embedded_text_style(style, text_style)
            self._artists.append(
                ShapeUtil.get_shape_text(xy=xy, text=text, angle=angle, style=effective_text_style)
            )

    @validate_call
    def shield(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        *,
        variant: ShieldVariant = "classic",
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a security shield shape on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            width: Width of the shield bounding box.
            height: Height of the shield bounding box.
            variant: Shield silhouette variant ("classic", "standard", "flat", "heater", "round").
            style: Style object (required).
            text: Text to display inside shape.
            text_style: Style object for text.
        """
        style, text_style = ShapeUtil.format_styles(style, text_style)
        angle: Angle = style.angle if style.angle is not None else 0.0
        xy, style = ShapeUtil.apply_alignment(
            xy=xy,
            width=width,
            height=height,
            angle=angle,
            style=style,
            is_default_center=True,
        )
        path = build_shield_path(xy, width, height, variant, angle)
        options = ShapeUtil.get_shape_options(style)
        self._artists.append(PathPatch(path=path, **options))
        if text:
            effective_text_style = ShapeUtil.resolve_embedded_text_style(style, text_style)
            self._artists.append(
                ShapeUtil.get_shape_text(xy=xy, text=text, angle=angle, style=effective_text_style)
            )

    @validate_call
    def ribbon(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        *,
        variant: RibbonVariant = "down",
        tail_width_ratio: Ratio | None = None,
        drop_ratio: Ratio | None = None,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a ribbon banner shape on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            width: Outer width of the ribbon bounding box.
            height: Outer height of the ribbon bounding box.
            variant: Ribbon variant ("down", "standard", "up", "flat", "banner").
            tail_width_ratio: Optional side tail width fraction in (0.0, 1.0).
            drop_ratio: Optional vertical step drop fraction in (0.0, 1.0).
            style: Style object (required).
            text: Text to display on the front banner panel.
            text_style: Style object for text.
        """
        ShapeUtil.validate_hole_ratio(tail_width_ratio)
        ShapeUtil.validate_hole_ratio(drop_ratio)
        style, text_style = ShapeUtil.format_styles(style, text_style)
        angle: Angle = style.angle if style.angle is not None else 0.0
        xy, style = ShapeUtil.apply_alignment(
            xy=xy,
            width=width,
            height=height,
            angle=angle,
            style=style,
            is_default_center=True,
        )
        patches, text_xy = build_ribbon_patches(
            xy=xy,
            width=width,
            height=height,
            variant=variant,
            tail_width_ratio=tail_width_ratio,
            drop_ratio=drop_ratio,
            angle=angle,
            style=style,
        )
        self._artists.extend(patches)
        if text:
            effective_text_style = ShapeUtil.resolve_embedded_text_style(style, text_style)
            self._artists.append(
                ShapeUtil.get_shape_text(
                    xy=text_xy,
                    text=text,
                    angle=angle,
                    style=effective_text_style,
                )
            )

    @validate_call
    def funnel(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        *,
        variant: FunnelVariant = "standard",
        neck_width_ratio: Ratio | None = None,
        neck_height_ratio: Ratio | None = None,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a filter funnel shape on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            width: Outer width of the funnel top opening.
            height: Total height of the funnel.
            variant: Funnel silhouette ("standard", "flat", "3d", "cylinder", "curved").
            neck_width_ratio: Optional bottom spout width ratio in (0.0, 1.0).
            neck_height_ratio: Optional bottom spout height ratio in (0.0, 1.0).
            style: Style object (required).
            text: Text to display inside the funnel.
            text_style: Style object for text.
        """
        ShapeUtil.validate_hole_ratio(neck_width_ratio)
        ShapeUtil.validate_hole_ratio(neck_height_ratio)
        style, text_style = ShapeUtil.format_styles(style, text_style)
        angle: Angle = style.angle if style.angle is not None else 0.0
        xy, style = ShapeUtil.apply_alignment(
            xy=xy,
            width=width,
            height=height,
            angle=angle,
            style=style,
            is_default_center=True,
        )
        patches, text_xy = build_funnel_patches(
            xy=xy,
            width=width,
            height=height,
            variant=variant,
            neck_width_ratio=neck_width_ratio,
            neck_height_ratio=neck_height_ratio,
            angle=angle,
            style=style,
        )
        self._artists.extend(patches)
        if text:
            effective_text_style = ShapeUtil.resolve_embedded_text_style(style, text_style)
            self._artists.append(
                ShapeUtil.get_shape_text(
                    xy=text_xy,
                    text=text,
                    angle=angle,
                    style=effective_text_style,
                )
            )

    @validate_call
    def pin(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        *,
        variant: PinVariant = "pointer",
        hole_ratio: Ratio | None = None,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a callout pointer badge or map pin shape on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            width: Width of the pin bounding box.
            height: Height of the pin bounding box.
            variant: Pin silhouette ("pointer", "standard", "teardrop", "drop", "pin", "badge").
            hole_ratio: Optional center circular hole ratio in (0.0, 1.0).
            style: Style object (required).
            text: Text to display centered inside the pin head.
            text_style: Style object for text.
        """
        ShapeUtil.validate_hole_ratio(hole_ratio)
        style, text_style = ShapeUtil.format_styles(style, text_style)
        angle: Angle = style.angle if style.angle is not None else 0.0
        xy, style = ShapeUtil.apply_alignment(
            xy=xy,
            width=width,
            height=height,
            angle=angle,
            style=style,
            is_default_center=True,
        )
        path, head_xy = build_pin_path_and_center(xy, width, height, variant, hole_ratio, angle)
        options = ShapeUtil.get_shape_options(style)
        self._artists.append(PathPatch(path=path, **options))
        if text:
            effective_text_style = ShapeUtil.resolve_embedded_text_style(style, text_style)
            self._artists.append(
                ShapeUtil.get_shape_text(
                    xy=head_xy,
                    text=text,
                    angle=angle,
                    style=effective_text_style,
                )
            )

    @validate_call
    def heart(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        *,
        variant: HeartVariant = "standard",
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a heart or broken-heart shape on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            width: Width of the heart bounding box.
            height: Height of the heart bounding box.
            variant: Heart silhouette ("standard", "classic", "broken").
            style: Style object (required).
            text: Text to display inside shape.
            text_style: Style object for text.
        """
        style, text_style = ShapeUtil.format_styles(style, text_style)
        angle: Angle = style.angle if style.angle is not None else 0.0
        xy, style = ShapeUtil.apply_alignment(
            xy=xy,
            width=width,
            height=height,
            angle=angle,
            style=style,
            is_default_center=True,
        )
        path = build_heart_path(xy, width, height, variant, angle)
        options = ShapeUtil.get_shape_options(style)
        self._artists.append(PathPatch(path=path, **options))
        if text:
            effective_text_style = ShapeUtil.resolve_embedded_text_style(style, text_style)
            self._artists.append(
                ShapeUtil.get_shape_text(xy=xy, text=text, angle=angle, style=effective_text_style)
            )

    @validate_call
    def sun(
        self,
        xy: Coordinate,
        radius: PosFloat,
        *,
        variant: SunVariant = "rays",
        num_rays: NumVertex = 8,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a sun shape with surrounding rays on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            radius: Outer radius to ray tips.
            variant: Sun variant ("rays", "standard", "ring", "beams").
            num_rays: Number of surrounding rays (must be >= 3).
            style: Style object (required).
            text: Text to display inside shape.
            text_style: Style object for text.
        """
        style, text_style = ShapeUtil.format_styles(style, text_style)
        angle: Angle = style.angle if style.angle is not None else 0.0
        width = radius * 2.0
        xy, style = ShapeUtil.apply_alignment(
            xy=xy,
            width=width,
            height=width,
            angle=angle,
            style=style,
            is_default_center=True,
        )
        path = build_sun_path(xy, radius, variant, num_rays, angle)
        options = ShapeUtil.get_shape_options(style)
        self._artists.append(PathPatch(path=path, **options))
        if text:
            effective_text_style = ShapeUtil.resolve_embedded_text_style(style, text_style)
            self._artists.append(
                ShapeUtil.get_shape_text(xy=xy, text=text, angle=angle, style=effective_text_style)
            )

    @validate_call
    def moon(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        *,
        variant: MoonVariant = "crescent",
        mirror: bool = False,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a crescent or half moon shape on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            width: Width of the moon bounding box.
            height: Height of the moon bounding box.
            variant: Moon silhouette ("crescent", "standard", "thin", "waxing", "half").
            mirror: Whether to flip the moon horizontally.
            style: Style object (required).
            text: Text to display inside shape.
            text_style: Style object for text.
        """
        style, text_style = ShapeUtil.format_styles(style, text_style)
        angle: Angle = style.angle if style.angle is not None else 0.0
        xy, style = ShapeUtil.apply_alignment(
            xy=xy,
            width=width,
            height=height,
            angle=angle,
            style=style,
            is_default_center=True,
        )
        path = build_moon_path(xy, width, height, variant, mirror, angle)
        options = ShapeUtil.get_shape_options(style)
        self._artists.append(PathPatch(path=path, **options))
        if text:
            effective_text_style = ShapeUtil.resolve_embedded_text_style(style, text_style)
            self._artists.append(
                ShapeUtil.get_shape_text(xy=xy, text=text, angle=angle, style=effective_text_style)
            )

    @validate_call
    def clock(
        self,
        xy: Coordinate,
        radius: PosFloat,
        *,
        variant: ClockVariant = "standard",
        hour: float = 10.0,
        minute: float = 10.0,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw an analog or 7-segment digital clock shape on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            radius: Radius of the clock dial (or scale reference for digital clock).
            variant: Clock variant ("standard", "ticks", "dial", "stopwatch",
                "timer", "alarm", "digital").
            hour: Hour value (e.g., 10.0 for 10 o'clock).
            minute: Minute value (e.g., 10.0 for 10 minutes).
            style: Style object (required).
            text: Text to display inside shape.
            text_style: Style object for text.
        """
        style, text_style = ShapeUtil.format_styles(style, text_style)
        angle: Angle = style.angle if style.angle is not None else 0.0
        width = radius * 2.15 if variant == "digital" else radius * 2.0
        height = radius * 1.22 if variant == "digital" else radius * 2.0
        xy, style = ShapeUtil.apply_alignment(
            xy=xy,
            width=width,
            height=height,
            angle=angle,
            style=style,
            is_default_center=True,
        )
        face_fill, stroke_color, feature_color, feature_w = _get_face_colors(style)
        self._artists.extend(
            build_clock_patches(
                xy=xy,
                radius=radius,
                variant=variant,
                hour=hour,
                minute=minute,
                angle=angle,
                face_fill=face_fill,
                stroke_color=stroke_color,
                feature_color=feature_color,
                feature_w=feature_w,
                style=style,
            )
        )
        if text:
            effective_text_style = ShapeUtil.resolve_embedded_text_style(style, text_style)
            self._artists.append(
                ShapeUtil.get_shape_text(xy=xy, text=text, angle=angle, style=effective_text_style)
            )


def _get_face_colors(
    style: Style,
) -> tuple[
    tuple[float, float, float, float] | str,
    tuple[float, float, float, float] | str,
    tuple[float, float, float, float],
    float,
]:
    """Derive face fill, outline stroke, and inner feature color/width from Style.

    Args:
        style: Shape style object.

    Returns:
        A tuple of (face_fill, stroke_color, feature_color, feature_line_w).
    """
    line_w = style.shape_line_width if style.shape_line_width is not None else 0.0
    raw_stroke = (
        ColorUtil.get_mplot_rgba(style.shape_line_color)
        if style.shape_line_color is not None
        else (0.0, 0.0, 0.0, 0.0)
    )
    has_stroke = style.shape_line_color is not None and line_w > 0 and raw_stroke[3] > 0.0

    if style.shape_fill_color is None:
        face_fill: tuple[float, float, float, float] | str = "none"
    else:
        raw_fill = ColorUtil.get_mplot_rgba(style.shape_fill_color, alpha=style.alpha)
        face_fill = "none" if raw_fill[3] <= 0.0 else raw_fill

    stroke_color: tuple[float, float, float, float] | str = raw_stroke if has_stroke else "none"

    if has_stroke:
        feature_color = raw_stroke
        feature_w = line_w
    elif style.text_color is not None:
        feature_color = ColorUtil.get_mplot_rgba(style.text_color)
        feature_w = 1.5
    else:
        contrast_col = ColorUtil.get_contrast_text_color(style.shape_fill_color, style.alpha)
        feature_color = ColorUtil.get_mplot_rgba(contrast_col)
        feature_w = 1.5

    if style.alpha is not None and 0.0 < style.alpha < 1.0:
        feature_color = (
            feature_color[0],
            feature_color[1],
            feature_color[2],
            round(feature_color[3] * style.alpha, 5),
        )
        if isinstance(stroke_color, tuple):
            stroke_color = (
                stroke_color[0],
                stroke_color[1],
                stroke_color[2],
                round(stroke_color[3] * style.alpha, 5),
            )

    return face_fill, stroke_color, feature_color, feature_w


def _build_face_head_patch(
    cx: float,
    cy: float,
    radius: float,
    variant: str,
    cos_a: float,
    sin_a: float,
    face_fill: tuple[float, float, float, float] | str,
    stroke_color: tuple[float, float, float, float] | str,
    line_w: float,
    line_style: str,
) -> Circle | PathPatch:
    """Build the outer head silhouette patch for a face shape."""

    def xform_pt(lx: float, ly: float) -> tuple[float, float]:
        return (cx + lx * cos_a - ly * sin_a, cy + lx * sin_a + ly * cos_a)

    if variant == "skull":
        r = radius
        jw = r * 0.52
        jy_bot = -r * 0.92
        jy_cheek = -r * 0.28
        cr = r * 0.92
        cy_dome = r * 0.12
        local_verts = [
            (-jw, jy_cheek),
            (-jw, jy_bot + r * 0.16),
            (-jw, jy_bot),
            (-jw + r * 0.16, jy_bot),
            (jw - r * 0.16, jy_bot),
            (jw, jy_bot),
            (jw, jy_bot + r * 0.16),
            (jw, jy_cheek),
            (cr * 1.02, jy_cheek + r * 0.08),
            (cr * 1.05, cy_dome + r * 0.25),
            (cr * 0.78, r * 0.78),
            (cr * 0.42, r * 1.02),
            (-cr * 0.42, r * 1.02),
            (-cr * 0.78, r * 0.78),
            (-cr * 1.05, cy_dome + r * 0.25),
            (-cr * 1.02, jy_cheek + r * 0.08),
            (-jw, jy_cheek),
            (-jw, jy_cheek),
        ]
        codes = [
            Path.MOVETO,
            Path.LINETO,
            Path.CURVE3,
            Path.CURVE3,
            Path.LINETO,
            Path.CURVE3,
            Path.CURVE3,
            Path.LINETO,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CLOSEPOLY,
        ]
        verts = [xform_pt(lx, ly) for lx, ly in local_verts]
        return PathPatch(
            Path(vertices=verts, codes=codes),
            facecolor=face_fill,
            edgecolor=stroke_color,
            linewidth=line_w,
            linestyle=line_style,
            joinstyle="round",
            zorder=1,
        )

    if variant == "devil":
        r = radius
        local_pts: list[tuple[float, float]] = []
        codes_d: list[Any] = []

        def add_arc(deg_start: float, deg_end: float, steps: int) -> None:
            for i in range(steps + 1):
                rad_ang = math.radians(deg_start + (deg_end - deg_start) * (i / steps))
                pt = (r * math.cos(rad_ang), r * math.sin(rad_ang))
                if not local_pts:
                    local_pts.append(pt)
                    codes_d.append(Path.MOVETO)
                else:
                    local_pts.append(pt)
                    codes_d.append(Path.LINETO)

        add_arc(142.0, 398.0, 48)
        r_tip = (r * 0.62, r * 1.25)
        r_base_in = (r * math.cos(math.radians(66.0)), r * math.sin(math.radians(66.0)))
        local_pts.extend(
            [
                (r * 1.05, r * 0.85),
                (r * 0.94, r * 1.16),
                r_tip,
                (r * 0.62, r * 1.04),
                (r * 0.50, r * 0.96),
                r_base_in,
            ]
        )
        codes_d.extend([Path.CURVE4] * 6)
        add_arc(66.0, 114.0, 14)
        l_tip = (-r * 0.62, r * 1.25)
        l_base_out = (r * math.cos(math.radians(142.0)), r * math.sin(math.radians(142.0)))
        local_pts.extend(
            [
                (-r * 0.50, r * 0.96),
                (-r * 0.62, r * 1.04),
                l_tip,
                (-r * 0.94, r * 1.16),
                (-r * 1.05, r * 0.85),
                l_base_out,
            ]
        )
        codes_d.extend([Path.CURVE4] * 6)
        local_pts.append(local_pts[0])
        codes_d.append(Path.CLOSEPOLY)
        verts_d = [xform_pt(lx, ly) for lx, ly in local_pts]
        return PathPatch(
            Path(vertices=verts_d, codes=codes_d),
            facecolor=face_fill,
            edgecolor=stroke_color,
            linewidth=line_w,
            linestyle=line_style,
            joinstyle="round",
            zorder=1,
        )

    return Circle(
        xy=(cx, cy),
        radius=radius,
        facecolor=face_fill,
        edgecolor=stroke_color,
        linewidth=line_w,
        linestyle=line_style,
        zorder=1,
    )


def _build_skull_feature_patches(
    xform_pt: Callable[[float, float], tuple[float, float]],
    radius: float,
    feature_color: tuple[float, float, float, float],
    feature_w: float,
) -> list[Circle | PathPatch]:
    """Build eye sockets, nasal cavity, and teeth lines for the skull face variant."""
    r = radius
    eye_x = r * 0.34
    eye_y = r * 0.16
    eye_r = r * 0.20
    patches: list[Circle | PathPatch] = [
        Circle(
            xy=xform_pt(-eye_x, eye_y),
            radius=eye_r,
            facecolor=feature_color,
            edgecolor="none",
            linewidth=0,
            zorder=2,
        ),
        Circle(
            xy=xform_pt(eye_x, eye_y),
            radius=eye_r,
            facecolor=feature_color,
            edgecolor="none",
            linewidth=0,
            zorder=2,
        ),
    ]

    nw = r * 0.11
    ny_top = -r * 0.04
    ny_bot = -r * 0.24
    nose_verts = [
        xform_pt(0.0, ny_top),
        xform_pt(-nw, ny_bot),
        xform_pt(nw, ny_bot),
        xform_pt(0.0, ny_top),
    ]
    nose_codes = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
    patches.append(
        PathPatch(
            Path(vertices=nose_verts, codes=nose_codes),
            facecolor=feature_color,
            edgecolor="none",
            linewidth=0,
            zorder=2,
        )
    )

    t_top = -r * 0.52
    t_bot = -r * 0.92
    t_verts: list[tuple[float, float]] = []
    t_codes: list[Any] = []
    for tx in (-r * 0.24, 0.0, r * 0.24):
        t_verts.extend([xform_pt(tx, t_top), xform_pt(tx, t_bot)])
        t_codes.extend([Path.MOVETO, Path.LINETO])
    patches.append(
        PathPatch(
            Path(vertices=t_verts, codes=t_codes),
            facecolor="none",
            edgecolor=feature_color,
            linewidth=feature_w,
            capstyle="round",
            zorder=2,
        )
    )
    return patches


def _build_x_eye_face_patches(
    xform_pt: Callable[[float, float], tuple[float, float]],
    radius: float,
    variant: str,
    feature_color: tuple[float, float, float, float],
    feature_w: float,
) -> list[Circle | PathPatch]:
    """Build X-eyes and mouth patches for 'dizzy' and 'dead' face variants."""
    eye_x = radius * 0.33
    eye_y = radius * 0.18
    d = radius * 0.14
    x_verts = [
        xform_pt(-eye_x - d, eye_y - d),
        xform_pt(-eye_x + d, eye_y + d),
        xform_pt(-eye_x - d, eye_y + d),
        xform_pt(-eye_x + d, eye_y - d),
        xform_pt(eye_x - d, eye_y - d),
        xform_pt(eye_x + d, eye_y + d),
        xform_pt(eye_x - d, eye_y + d),
        xform_pt(eye_x + d, eye_y - d),
    ]
    x_codes = [
        Path.MOVETO,
        Path.LINETO,
        Path.MOVETO,
        Path.LINETO,
        Path.MOVETO,
        Path.LINETO,
        Path.MOVETO,
        Path.LINETO,
    ]
    patches: list[Circle | PathPatch] = [
        PathPatch(
            Path(vertices=x_verts, codes=x_codes),
            facecolor="none",
            edgecolor=feature_color,
            linewidth=feature_w * 1.15,
            capstyle="round",
            zorder=2,
        )
    ]

    my = -radius * 0.30
    if variant == "dizzy":
        w = radius * 0.38
        h = radius * 0.12
        m_verts = [
            xform_pt(-w, my),
            xform_pt(-w * 0.5, my + h),
            xform_pt(0.0, my),
            xform_pt(w * 0.5, my - h),
            xform_pt(w, my),
        ]
        m_codes = [Path.MOVETO, Path.CURVE3, Path.CURVE3, Path.CURVE3, Path.CURVE3]
    else:
        rx = radius * 0.17
        ry = radius * 0.18
        kappa = 0.5522847498307936
        kx = rx * kappa
        ky = ry * kappa
        local_o = [
            (rx, my),
            (rx, my + ky),
            (kx, my + ry),
            (0.0, my + ry),
            (-kx, my + ry),
            (-rx, my + ky),
            (-rx, my),
            (-rx, my - ky),
            (-kx, my - ry),
            (0.0, my - ry),
            (kx, my - ry),
            (rx, my - ky),
            (rx, my),
            (rx, my),
        ]
        m_verts = [xform_pt(lx, ly) for lx, ly in local_o]
        m_codes = [
            Path.MOVETO,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CLOSEPOLY,
        ]

    patches.append(
        PathPatch(
            Path(vertices=m_verts, codes=m_codes),
            facecolor="none",
            edgecolor=feature_color,
            linewidth=feature_w,
            capstyle="round",
            joinstyle="round",
            zorder=2,
        )
    )
    return patches


def _build_face_feature_patches(
    cx: float,
    cy: float,
    radius: float,
    variant: str,
    cos_a: float,
    sin_a: float,
    feature_color: tuple[float, float, float, float],
    feature_w: float,
) -> list[Circle | PathPatch]:
    """Generate eye, eyebrow, and mouth patches for a face shape.

    Args:
        cx: Center x coordinate.
        cy: Center y coordinate.
        radius: Face circle radius.
        variant: Facial expression or silhouette name.
        cos_a: Cosine of rotation angle.
        sin_a: Sine of rotation angle.
        feature_color: RGBA color for eyes, eyebrows, and mouth.
        feature_w: Line width for mouth and eyebrows.

    Returns:
        List of Circle and PathPatch artists for facial features.
    """

    def xform_pt(lx: float, ly: float) -> tuple[float, float]:
        return (cx + lx * cos_a - ly * sin_a, cy + lx * sin_a + ly * cos_a)

    if variant == "skull":
        return _build_skull_feature_patches(xform_pt, radius, feature_color, feature_w)
    if variant in {"dizzy", "dead"}:
        return _build_x_eye_face_patches(xform_pt, radius, variant, feature_color, feature_w)

    eye_x = radius * 0.32
    if variant == "devil":
        eye_y = radius * 0.10
        eye_r = radius * 0.105
    elif variant == "angry":
        eye_y = radius * 0.13
        eye_r = radius * 0.105
    else:
        eye_y = radius * 0.20
        eye_r = radius * 0.11

    left_eye = Circle(
        xy=xform_pt(-eye_x, eye_y),
        radius=eye_r,
        facecolor=feature_color,
        edgecolor="none",
        linewidth=0,
        zorder=1,
    )
    right_eye = Circle(
        xy=xform_pt(eye_x, eye_y),
        radius=eye_r,
        facecolor=feature_color,
        edgecolor="none",
        linewidth=0,
        zorder=1,
    )
    patches: list[Circle | PathPatch] = [left_eye, right_eye]

    if variant in {"angry", "devil"}:
        bx_out = 0.50 if variant == "devil" else 0.48
        by_out = 0.38 if variant == "devil" else 0.40
        bx_in = 0.13 if variant == "devil" else 0.15
        by_in = 0.20 if variant == "devil" else 0.25
        brow_verts = [
            xform_pt(-radius * bx_out, radius * by_out),
            xform_pt(-radius * bx_in, radius * by_in),
            xform_pt(radius * bx_out, radius * by_out),
            xform_pt(radius * bx_in, radius * by_in),
        ]
        brow_codes = [Path.MOVETO, Path.LINETO, Path.MOVETO, Path.LINETO]
        patches.append(
            PathPatch(
                Path(vertices=brow_verts, codes=brow_codes),
                facecolor="none",
                edgecolor=feature_color,
                linewidth=feature_w,
                capstyle="round",
                joinstyle="round",
                zorder=1,
            )
        )

    if variant in {"smile", "devil"}:
        mx_out = 0.46 if variant == "devil" else 0.44
        my_out = -0.14 if variant == "devil" else -0.18
        m_verts = [
            xform_pt(-radius * mx_out, radius * my_out),
            xform_pt(-radius * 0.24, -radius * 0.54),
            xform_pt(radius * 0.24, -radius * 0.54),
            xform_pt(radius * mx_out, radius * my_out),
        ]
        m_codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
    elif variant == "neutral":
        m_verts = [
            xform_pt(-radius * 0.36, -radius * 0.28),
            xform_pt(radius * 0.36, -radius * 0.28),
        ]
        m_codes = [Path.MOVETO, Path.LINETO]
    elif variant in {"sad", "angry"}:
        m_verts = [
            xform_pt(-radius * 0.42, -radius * 0.42),
            xform_pt(-radius * 0.22, -radius * 0.14),
            xform_pt(radius * 0.22, -radius * 0.14),
            xform_pt(radius * 0.42, -radius * 0.42),
        ]
        m_codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
    else:
        # "surprised": open 'O' ellipse mouth
        rx = radius * 0.16
        ry = radius * 0.20
        my = -radius * 0.30
        kappa = 0.5522847498307936
        kx = rx * kappa
        ky = ry * kappa
        local_o = [
            (rx, my),
            (rx, my + ky),
            (kx, my + ry),
            (0.0, my + ry),
            (-kx, my + ry),
            (-rx, my + ky),
            (-rx, my),
            (-rx, my - ky),
            (-kx, my - ry),
            (0.0, my - ry),
            (kx, my - ry),
            (rx, my - ky),
            (rx, my),
            (rx, my),
        ]
        m_verts = [xform_pt(lx, ly) for lx, ly in local_o]
        m_codes = [
            Path.MOVETO,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CLOSEPOLY,
        ]

    patches.append(
        PathPatch(
            Path(vertices=m_verts, codes=m_codes),
            facecolor="none",
            edgecolor=feature_color,
            linewidth=feature_w,
            capstyle="round",
            joinstyle="round",
            zorder=1,
        )
    )
    return patches


def _arc_bezier_between(
    p0: tuple[float, float],
    p1: tuple[float, float],
    sagitta_ratio: float,
) -> list[tuple[tuple[float, float], Any]]:
    """Build circular arc cubic Bezier segments from p0 to p1 bulging outward (CCW)."""
    dx = p1[0] - p0[0]
    dy = p1[1] - p0[1]
    chord = math.hypot(dx, dy)
    if chord < 1e-9 or sagitta_ratio <= 1e-4:
        return [(p1, Path.LINETO)]

    nx = dy / chord
    ny = -dx / chord
    h = sagitta_ratio * chord
    r = (chord * chord) / (8.0 * h) + (h / 2.0)
    theta = 4.0 * math.atan((2.0 * h) / chord)

    mx = 0.5 * (p0[0] + p1[0])
    my = 0.5 * (p0[1] + p1[1])
    cx = mx + (h - r) * nx
    cy = my + (h - r) * ny

    angle_peak = math.atan2(ny, nx)
    a0 = angle_peak - 0.5 * theta
    a1 = angle_peak + 0.5 * theta

    num_seg = 1 if theta <= (math.pi * 0.55) else 2
    d_theta = (a1 - a0) / num_seg
    k = (4.0 / 3.0) * math.tan(d_theta / 4.0)

    segments: list[tuple[tuple[float, float], Any]] = []
    for i in range(num_seg):
        t0 = a0 + i * d_theta
        t1 = t0 + d_theta
        x0_s, y0_s = cx + r * math.cos(t0), cy + r * math.sin(t0)
        x1_s, y1_s = cx + r * math.cos(t1), cy + r * math.sin(t1)
        cp1 = (x0_s - k * r * math.sin(t0), y0_s + k * r * math.cos(t0))
        cp2 = (x1_s + k * r * math.sin(t1), y1_s - k * r * math.cos(t1))
        segments.extend([(cp1, Path.CURVE4), (cp2, Path.CURVE4), ((x1_s, y1_s), Path.CURVE4)])
    return segments


def _get_cloud_valleys_and_sagittas(
    variant: str,
    bump_ratio: float | None,
) -> tuple[list[tuple[float, float]], list[float]]:
    """Return valley coordinates and sagitta ratios for the selected cloud variant."""
    if variant in ("flat", "flat_bottom"):
        br = 0.24 if bump_ratio is None else bump_ratio
        scale_b = br / 0.24
        valleys = [
            (-0.34, -0.38),
            (0.36, -0.38),
            (0.32, 0.06),
            (0.02, 0.24),
            (-0.28, 0.12),
        ]
        sagittas = [0.0, 0.40 * scale_b, 0.42 * scale_b, 0.46 * scale_b, 0.40 * scale_b]
        return valleys, sagittas

    if variant in ("fluffy", "dense"):
        br = 0.20 if bump_ratio is None else bump_ratio
        scale_b = br / 0.20
        angles_deg = [-150, -120, -90, -60, -30, 0, 30, 62, 92, 122, 150, 180]
        radii_scale = [0.96, 0.94, 0.95, 0.94, 0.96, 0.98, 0.95, 0.98, 0.96, 0.95, 0.97, 0.96]
        valleys = [
            (0.38 * s * math.cos(math.radians(a)), 0.36 * s * math.sin(math.radians(a)))
            for a, s in zip(angles_deg, radii_scale, strict=True)
        ]
        return valleys, [0.38 * scale_b] * len(valleys)

    if variant in ("simple", "minimal"):
        br = 0.24 if bump_ratio is None else bump_ratio
        scale_b = br / 0.24
        angles_deg = [-145, -90, -35, 35, 90, 145]
        valleys = [
            (0.35 * math.cos(math.radians(a)), 0.32 * math.sin(math.radians(a)))
            for a in angles_deg
        ]
        sagittas = [0.36 * scale_b, 0.36 * scale_b, 0.42 * scale_b, 0.38 * scale_b, 0.38 * scale_b, 0.42 * scale_b]
        return valleys, sagittas

    br = 0.22 if bump_ratio is None else bump_ratio
    scale_b = br / 0.22
    angles_deg = [-148, -108, -68, -26, 22, 68, 118, 156]
    radii_scale = [0.95, 0.92, 0.92, 0.95, 0.96, 0.98, 0.96, 0.95]
    valleys = [
        (0.37 * s * math.cos(math.radians(a)), 0.34 * s * math.sin(math.radians(a)))
        for a, s in zip(angles_deg, radii_scale, strict=True)
    ]
    sagittas = [
        0.34 * scale_b,
        0.32 * scale_b,
        0.34 * scale_b,
        0.42 * scale_b,
        0.40 * scale_b,
        0.45 * scale_b,
        0.38 * scale_b,
        0.42 * scale_b,
    ]
    return valleys, sagittas


def _build_cloud_path(
    xy: tuple[float, float],
    width: float,
    height: float,
    variant: str,
    bump_ratio: float | None,
    angle: float,
) -> Path:
    """Build normalized and rotated cloud Path for the given variant and bump_ratio."""
    valleys, sagittas = _get_cloud_valleys_and_sagittas(variant, bump_ratio)
    raw_verts: list[tuple[float, float]] = [valleys[0]]
    codes: list[Any] = [Path.MOVETO]

    n = len(valleys)
    for i in range(n):
        segs = _arc_bezier_between(valleys[i], valleys[(i + 1) % n], max(0.0, sagittas[i]))
        for pt, code in segs:
            raw_verts.append(pt)
            codes.append(code)

    min_x = min(p[0] for p in raw_verts)
    max_x = max(p[0] for p in raw_verts)
    min_y = min(p[1] for p in raw_verts)
    max_y = max(p[1] for p in raw_verts)
    span_x = max(max_x - min_x, 1e-6)
    span_y = max(max_y - min_y, 1e-6)
    cx_norm = 0.5 * (min_x + max_x)
    cy_norm = 0.5 * (min_y + max_y)

    rad = math.radians(angle)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)

    scaled_verts: list[tuple[float, float]] = []
    for vx, vy in raw_verts:
        lx = ((vx - cx_norm) / span_x) * width
        ly = ((vy - cy_norm) / span_y) * height
        rx = xy[0] + lx * cos_a - ly * sin_a
        ry = xy[1] + lx * sin_a + ly * cos_a
        scaled_verts.append((rx, ry))

    scaled_verts.append((0.0, 0.0))
    codes.append(Path.CLOSEPOLY)
    return Path(scaled_verts, codes)


def _format_brace_styles(
    style: Style,
    text_style: Style | None = None,
) -> tuple[Style, Style | None]:
    """Validate and return style (supporting 'line' or 'shape') and optional text_style."""
    if not isinstance(style, Style):
        raise TypeError(f'Arg "style" must be Style, but {type(style)} given.')
    if "line" not in style.supports and "shape" not in style.supports:
        style.validate_for("line")
    if text_style is not None:
        if not isinstance(text_style, Style):
            raise TypeError(f'Arg "text_style" must be Style, but {type(text_style)} given.')
        text_style.validate_for("text")
    return style, text_style


def _get_brace_stroke_options(style: Style) -> dict[str, Any]:
    """Extract Matplotlib PathPatch stroke options from Style for brace rendering."""
    lw = style.line_width
    if lw is None:
        lw = style.shape_line_width if (style.shape_line_width or 0.0) > 0.0 else 1.5

    col = style.line_color
    if col is None:
        col = (
            style.shape_line_color
            if (style.shape_line_width or 0.0) > 0.0 and style.shape_line_color is not None
            else style.shape_fill_color
        )
    rgba = ColorUtil.get_mplot_rgba(col) if col is not None else (0.0, 0.0, 0.0, 1.0)
    ls = style.line_style if style.line_style is not None else (style.shape_line_style or "solid")

    options: dict[str, Any] = {
        "facecolor": "none",
        "edgecolor": rgba,
        "linewidth": lw,
        "linestyle": ls,
        "capstyle": "round",
        "joinstyle": "round",
    }
    if style.alpha is not None:
        options["alpha"] = style.alpha
    return options


def _build_square_brace_local(
    hd: float,
    hs: float,
    depth: float,
    span: float,
    shape_r: float | None,
) -> tuple[list[tuple[float, float]], list[Any]]:
    """Build local canonical 'left' vertices and Path codes for square bracket '['."""
    r = 0.0 if shape_r is None else min(float(shape_r), depth * 0.9, span * 0.45)
    if r <= 1e-6:
        verts = [(hd, hs), (-hd, hs), (-hd, -hs), (hd, -hs)]
        codes: list[Any] = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO]
        return verts, codes

    k = 0.5522847498307936
    verts = [
        (hd, hs),
        (-hd + r, hs),
        (-hd + r * (1.0 - k), hs),
        (-hd, hs - r * (1.0 - k)),
        (-hd, hs - r),
        (-hd, -hs + r),
        (-hd, -hs + r * (1.0 - k)),
        (-hd + r * (1.0 - k), -hs),
        (-hd + r, -hs),
        (hd, -hs),
    ]
    codes = [
        Path.MOVETO,
        Path.LINETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.LINETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.LINETO,
    ]
    return verts, codes


def _build_curly_brace_local(
    hd: float,
    hs: float,
    depth: float,
    span: float,
    tip_ratio: float | None,
    tip_position_ratio: float | None,
) -> tuple[list[tuple[float, float]], list[Any]]:
    """Build local canonical 'left' vertices and Path codes for curly brace '{'."""
    tip_r = 0.50 if tip_ratio is None else tip_ratio
    pos_r = 0.50 if tip_position_ratio is None else tip_position_ratio

    tip_depth = tip_r * depth
    hook_depth = (1.0 - tip_r) * depth
    x_spine = -hd + tip_depth

    r_hook = min(max(hook_depth, depth * 0.15), span * 0.14)
    h_tip = min(max(tip_depth * 0.95, depth * 0.20), span * 0.16)

    y_tip = (pos_r - 0.5) * span
    y_tip = max(-hs + r_hook + h_tip, min(hs - r_hook - h_tip, y_tip))

    k = 0.5522847498307936
    verts = [
        (hd, hs),
        (x_spine + hook_depth * (1.0 - k), hs),
        (x_spine, hs - r_hook * (1.0 - k)),
        (x_spine, hs - r_hook),
        (x_spine, y_tip + h_tip),
        (x_spine, y_tip + h_tip * (1.0 - k)),
        (-hd + tip_depth * (1.0 - k), y_tip),
        (-hd, y_tip),
        (-hd + tip_depth * (1.0 - k), y_tip),
        (x_spine, y_tip - h_tip * (1.0 - k)),
        (x_spine, y_tip - h_tip),
        (x_spine, -hs + r_hook),
        (x_spine, -hs + r_hook * (1.0 - k)),
        (x_spine + hook_depth * (1.0 - k), -hs),
        (hd, -hs),
    ]
    codes: list[Any] = [
        Path.MOVETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.LINETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.LINETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
    ]
    return verts, codes


def _build_brace_path(
    xy: tuple[float, float],
    width: float,
    height: float,
    symbol: str,
    direction: str | None,
    tip_ratio: float | None,
    tip_position_ratio: float | None,
    shape_r: float | None,
    angle: float,
) -> Path:
    """Build rotated open Path for curly {}, square [], and round () braces."""
    eff_dir = direction if direction is not None else ("right" if symbol in ("}", "]", ")") else "left")
    is_horizontal = eff_dir in ("top", "bottom")
    span = width if is_horizontal else height
    depth = height if is_horizontal else width
    hs = span / 2.0
    hd = depth / 2.0

    if symbol in ("[", "]", "[]", "square"):
        verts, codes = _build_square_brace_local(hd, hs, depth, span, shape_r)
    elif symbol in ("(", ")", "()", "round"):
        k_y = hs * 0.5522847498307936
        verts = [
            (hd, hs),
            (-hd * 0.25, hs),
            (-hd, k_y),
            (-hd, 0.0),
            (-hd, -k_y),
            (-hd * 0.25, -hs),
            (hd, -hs),
        ]
        codes = [
            Path.MOVETO,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
        ]
    else:
        verts, codes = _build_curly_brace_local(hd, hs, depth, span, tip_ratio, tip_position_ratio)

    rad = math.radians(angle)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)

    transformed: list[tuple[float, float]] = []
    for lx, ly in verts:
        if eff_dir == "left":
            tx, ty = lx, ly
        elif eff_dir == "right":
            tx, ty = -lx, ly
        elif eff_dir == "top":
            tx, ty = ly, -lx
        else:
            tx, ty = ly, lx
        rx = xy[0] + tx * cos_a - ty * sin_a
        ry = xy[1] + tx * sin_a + ty * cos_a
        transformed.append((rx, ry))

    return Path(transformed, codes)


def _get_cube_face_fills(
    style: Style,
) -> tuple[
    tuple[float, float, float, float] | str,
    tuple[float, float, float, float] | str,
    tuple[float, float, float, float] | str,
]:
    """Derive front, top, and right-side face fills from a shape Style."""
    if style.shape_fill_color is None:
        return "none", "none", "none"

    raw = ColorUtil.get_mplot_rgba(style.shape_fill_color, alpha=style.alpha)
    if raw[3] <= 0.0:
        return "none", "none", "none"

    lum = 0.299 * raw[0] + 0.587 * raw[1] + 0.114 * raw[2]
    top_lift = 0.55 if lum > 0.85 else 0.28
    side_mul = 0.92 if lum > 0.85 else 0.82
    top_fill = (
        min(1.0, raw[0] + (1.0 - raw[0]) * top_lift),
        min(1.0, raw[1] + (1.0 - raw[1]) * top_lift),
        min(1.0, raw[2] + (1.0 - raw[2]) * top_lift),
        raw[3],
    )
    side_fill = (
        raw[0] * side_mul,
        raw[1] * side_mul,
        raw[2] * side_mul,
        raw[3],
    )
    return raw, top_fill, side_fill


def _build_cube_patches(
    xy: tuple[float, float],
    width: float,
    height: float,
    depth_ratio: float | None,
    angle: float,
    style: Style,
) -> tuple[list[PathPatch], tuple[float, float]]:
    """Build 3D cube face and outline patches and return (patches, front_face_text_xy)."""
    cx, cy = xy
    dr = 0.25 if depth_ratio is None else depth_ratio
    base_d = min(width, height) * dr
    dx = min(base_d, width * 0.48)
    dy = min(base_d * 0.82, height * 0.48)

    hw = width / 2.0
    hh = height / 2.0
    fx0, fx1 = -hw, hw - dx
    fy0, fy1 = -hh, hh - dy

    rad = math.radians(angle)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)

    def xform(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
        return [(cx + vx * cos_a - vy * sin_a, cy + vx * sin_a + vy * cos_a) for vx, vy in pts]

    front_pts = [(fx0, fy0), (fx1, fy0), (fx1, fy1), (fx0, fy1), (fx0, fy0)]
    top_pts = [(fx0, fy1), (fx1, fy1), (hw, hh), (fx0 + dx, hh), (fx0, fy1)]
    side_pts = [(fx1, fy0), (hw, -hh + dy), (hw, hh), (fx1, fy1), (fx1, fy0)]
    codes_quad: list[Any] = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY]

    front_fill, top_fill, side_fill = _get_cube_face_fills(style)
    patches: list[PathPatch] = [
        PathPatch(
            Path(vertices=xform(pts), codes=codes_quad),
            facecolor=fill,
            edgecolor="none",
            linewidth=0,
            zorder=1,
        )
        for pts, fill in ((top_pts, top_fill), (side_pts, side_fill), (front_pts, front_fill))
    ]

    line_w = style.shape_line_width if style.shape_line_width is not None else 0.0
    if style.shape_line_color is not None and line_w > 0:
        stroke_color = ColorUtil.get_mplot_rgba(style.shape_line_color, alpha=style.alpha)
        if stroke_color[3] > 0.0:
            line_style = style.shape_line_style if style.shape_line_style is not None else "solid"
            outer_pts = [
                (fx0, fy0),
                (fx1, fy0),
                (hw, -hh + dy),
                (hw, hh),
                (fx0 + dx, hh),
                (fx0, fy1),
                (fx0, fy0),
                (fx0, fy1),
                (fx1, fy1),
                (fx1, fy0),
                (fx1, fy1),
                (hw, hh),
            ]
            outer_codes: list[Any] = [
                Path.MOVETO,
                Path.LINETO,
                Path.LINETO,
                Path.LINETO,
                Path.LINETO,
                Path.LINETO,
                Path.CLOSEPOLY,
                Path.MOVETO,
                Path.LINETO,
                Path.LINETO,
                Path.MOVETO,
                Path.LINETO,
            ]
            patches.append(
                PathPatch(
                    Path(vertices=xform(outer_pts), codes=outer_codes),
                    facecolor="none",
                    edgecolor=stroke_color,
                    linewidth=line_w,
                    linestyle=line_style,
                    joinstyle="round",
                    capstyle="round",
                    zorder=1,
                )
            )

    fcx_local = 0.5 * (fx0 + fx1)
    fcy_local = 0.5 * (fy0 + fy1)
    text_xy = (
        cx + fcx_local * cos_a - fcy_local * sin_a,
        cy + fcx_local * sin_a + fcy_local * cos_a,
    )
    return patches, text_xy


def _build_document_sheet_paths(
    x0: float,
    y0: float,
    w: float,
    h: float,
    variant: str,
    wave_h: float,
    fold_s: float,
    cx: float,
    cy: float,
    cos_a: float,
    sin_a: float,
) -> tuple[Path, Path | None, Path]:
    """Build rotated (body_fill_path, flap_fill_path, stroke_path) for one document sheet."""

    def xform(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
        return [(cx + vx * cos_a - vy * sin_a, cy + vx * sin_a + vy * cos_a) for vx, vy in pts]

    has_bottom_wave = variant in ("wave", "standard", "double_wave", "snippet", "folded_wave", "report")
    has_top_wave = variant in ("double_wave", "snippet")
    has_fold = variant in ("folded", "page", "note", "folded_wave", "report")

    x1 = x0 + w
    xm = x0 + w * 0.5
    y1 = y0 + h

    yt_base = y1 - 0.5 * wave_h if has_top_wave else y1
    verts: list[tuple[float, float]] = [(x0, yt_base)]
    codes: list[Any] = [Path.MOVETO]

    if has_bottom_wave:
        yb_base = y0 + 0.5 * wave_h
        db = (2.0 / 3.0) * wave_h
        verts.extend([
            (x0, yb_base),
            (x0 + w * 0.16, yb_base - db),
            (x0 + w * 0.34, yb_base - db),
            (xm, yb_base),
            (x0 + w * 0.66, yb_base + db),
            (x0 + w * 0.84, yb_base + db),
            (x1, yb_base),
        ])
        codes.extend([Path.LINETO] + [Path.CURVE4] * 6)
    else:
        verts.extend([(x0, y0), (x1, y0)])
        codes.extend([Path.LINETO, Path.LINETO])

    if has_fold:
        verts.extend([(x1, y1 - fold_s), (x1 - fold_s, y1), (x0, y1)])
        codes.extend([Path.LINETO, Path.LINETO, Path.CLOSEPOLY])
    elif has_top_wave:
        dt = (2.0 / 3.0) * wave_h
        verts.extend([
            (x1, yt_base),
            (x0 + w * 0.84, yt_base + dt),
            (x0 + w * 0.66, yt_base + dt),
            (xm, yt_base),
            (x0 + w * 0.34, yt_base - dt),
            (x0 + w * 0.16, yt_base - dt),
            (x0, yt_base),
            (x0, yt_base),
        ])
        codes.extend([Path.LINETO] + [Path.CURVE4] * 6 + [Path.CLOSEPOLY])
    else:
        verts.extend([(x1, y1), (x0, y1)])
        codes.extend([Path.LINETO, Path.CLOSEPOLY])

    body_path = Path(vertices=xform(verts), codes=codes)
    flap_path: Path | None = None
    stroke_verts = list(verts)
    stroke_codes = list(codes)

    if has_fold:
        flap_verts = [
            (x1 - fold_s, y1),
            (x1 - fold_s, y1 - fold_s),
            (x1, y1 - fold_s),
            (x1 - fold_s, y1),
        ]
        flap_codes: list[Any] = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
        flap_path = Path(vertices=xform(flap_verts), codes=flap_codes)
        stroke_verts.extend([
            (x1 - fold_s, y1),
            (x1 - fold_s, y1 - fold_s),
            (x1, y1 - fold_s),
        ])
        stroke_codes.extend([Path.MOVETO, Path.LINETO, Path.LINETO])

    return body_path, flap_path, Path(vertices=xform(stroke_verts), codes=stroke_codes)


def _get_document_sheet_fills(
    raw_fill: tuple[float, float, float, float] | None,
    idx: int,
) -> tuple[tuple[float, float, float, float] | str, tuple[float, float, float, float] | str]:
    """Compute body fill and folded flap fill for a document sheet at stack index idx."""
    if raw_fill is None or raw_fill[3] <= 0.0:
        return "none", "none"

    factor = 0.14 * idx
    fill_c = (
        min(1.0, raw_fill[0] + (1.0 - raw_fill[0]) * factor),
        min(1.0, raw_fill[1] + (1.0 - raw_fill[1]) * factor),
        min(1.0, raw_fill[2] + (1.0 - raw_fill[2]) * factor),
        raw_fill[3],
    )
    lum = 0.299 * fill_c[0] + 0.587 * fill_c[1] + 0.114 * fill_c[2]
    flap_mul = 0.90 if lum > 0.85 else 0.80
    flap_c = (
        fill_c[0] * flap_mul,
        fill_c[1] * flap_mul,
        fill_c[2] * flap_mul,
        fill_c[3],
    )
    return fill_c, flap_c


def _get_document_text_center(
    cx: float,
    cy: float,
    hw: float,
    hh: float,
    sheet_w: float,
    sheet_h: float,
    wave_h: float,
    fold_s: float,
    variant: str,
    cos_a: float,
    sin_a: float,
) -> tuple[float, float]:
    """Calculate optical center on the front document sheet for embedded text."""
    fcx_local = -hw + sheet_w / 2.0
    if variant in ("wave", "standard"):
        fcy_local = -hh + wave_h * 0.50 + (sheet_h - wave_h * 0.50) / 2.0
    elif variant in ("folded_wave", "report"):
        fcy_local = -hh + wave_h * 0.45 + (sheet_h - wave_h * 0.45 - fold_s * 0.25) / 2.0
    elif variant in ("folded", "page", "note"):
        fcy_local = -hh + (sheet_h - fold_s * 0.20) / 2.0
    else:
        fcy_local = -hh + sheet_h / 2.0
    return (
        cx + fcx_local * cos_a - fcy_local * sin_a,
        cy + fcx_local * sin_a + fcy_local * cos_a,
    )


def _build_document_patches(
    xy: tuple[float, float],
    width: float,
    height: float,
    variant: str,
    stacked: int,
    wave_ratio: float | None,
    fold_ratio: float | None,
    angle: float,
    style: Style,
) -> tuple[list[PathPatch], tuple[float, float]]:
    """Build document sheet patches (supporting stacked sheets and variants) and return (patches, text_xy)."""
    cx, cy = xy
    wr = 0.14 if wave_ratio is None else wave_ratio
    fr = 0.24 if fold_ratio is None else fold_ratio

    rad = math.radians(angle)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)

    n = max(1, stacked)
    step_x = 0.0 if n == 1 else min(width * 0.075, 2.2)
    step_y = 0.0 if n == 1 else min(height * 0.075, 2.2)
    sheet_w = width - step_x * (n - 1)
    sheet_h = height - step_y * (n - 1)
    wave_h = sheet_h * wr
    fold_s = min(sheet_w, sheet_h) * fr

    line_w = style.shape_line_width if style.shape_line_width is not None else 0.0
    stroke_rgba = (
        ColorUtil.get_mplot_rgba(style.shape_line_color, alpha=style.alpha)
        if style.shape_line_color is not None and line_w > 0
        else None
    )
    has_stroke = stroke_rgba is not None and stroke_rgba[3] > 0.0
    line_style = style.shape_line_style if style.shape_line_style is not None else "solid"
    raw_fill = (
        ColorUtil.get_mplot_rgba(style.shape_fill_color, alpha=style.alpha)
        if style.shape_fill_color is not None
        else None
    )

    hw = width / 2.0
    hh = height / 2.0
    patches: list[PathPatch] = []

    for idx in range(n - 1, -1, -1):
        body_p, flap_p, stroke_p = _build_document_sheet_paths(
            -hw + idx * step_x,
            -hh + idx * step_y,
            sheet_w,
            sheet_h,
            variant,
            wave_h,
            fold_s,
            cx,
            cy,
            cos_a,
            sin_a,
        )
        fill_c, flap_c = _get_document_sheet_fills(raw_fill, idx)
        patches.append(
            PathPatch(
                body_p,
                facecolor=fill_c,
                edgecolor="none",
                linewidth=0,
                zorder=1,
            )
        )
        if flap_p is not None and flap_c != "none":
            patches.append(
                PathPatch(
                    flap_p,
                    facecolor=flap_c,
                    edgecolor="none",
                    linewidth=0,
                    zorder=1,
                )
            )

        needs_sep = (n > 1 or flap_p is not None) and fill_c != "none"
        edge_c: tuple[float, float, float, float] | str = (
            stroke_rgba if (has_stroke and stroke_rgba is not None) else ("#ffffff" if needs_sep else "none")
        )
        edge_w = line_w if has_stroke else (1.0 if needs_sep else 0.0)
        if edge_c != "none" and edge_w > 0:
            patches.append(
                PathPatch(
                    stroke_p,
                    facecolor="none",
                    edgecolor=edge_c,
                    linewidth=edge_w,
                    linestyle=line_style,
                    joinstyle="round",
                    capstyle="round",
                    zorder=1,
                )
            )

    text_xy = _get_document_text_center(
        cx, cy, hw, hh, sheet_w, sheet_h, wave_h, fold_s, variant, cos_a, sin_a
    )
    return patches, text_xy


__all__ = ["CanvasShapeBasicFeature"]
