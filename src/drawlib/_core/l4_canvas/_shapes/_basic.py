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
    Coordinate,
    Coordinates,
    FaceMood,
    NumVertex,
    PathPoints,
    PosFloat,
    PosInt,
    Size,
)
from drawlib._core.l3_colors import ColorUtil
from drawlib._core.l3_math import get_center_and_size
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas._base import CanvasBase
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

    @validate_call
    def rectangle(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        *,
        style: Style,
        r: PosFloat = 0.0,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a rectangle on the canvas.

        Args:
            xy: Bottom-left corner of the rectangle.
            width: Width of the rectangle.
            height: Height of the rectangle.
            style: Style of the rectangle (required).
            r (float, optional): Radius for rounded corners (default is 0.0).
            text (str, optional): Text to display within the rectangle.
            text_style (Style | None, optional): Style of the text.

        Raises:
            ValueError: If invalid path points are provided.
        """
        style, text_style = ShapeUtil.format_styles(
            style,
            text_style,
        )

        if r == 0:
            p1 = (0, 0)
            p2 = (0, height)
            p3 = (width, height)
            p4 = (width, 0)
            self.shape(
                xy=xy,
                path_points=[p1, p2, p3, p4],
                style=style,
                text=text,
                text_style=text_style,
            )
            return

        # left center
        p1 = (0, height / 2)

        # left top corner
        p2 = (0, height - r)
        p3 = ((0, height), (r, height))

        # right top corner
        p4 = (width - r, height)
        p5 = ((width, height), (width, height - r))

        # right bottom corner
        p6 = (width, r)
        p7 = ((width, 0), (width - r, 0))

        # left bottom corner
        p8 = (r, 0)
        p9 = ((0, 0), (0, r))

        self.shape(
            xy=xy,
            path_points=[p1, p2, p3, p4, p5, p6, p7, p8, p9],
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

        style = style.patch(halign=None, valign=None)
        options = ShapeUtil.get_shape_options(style)
        self._artists.append(Polygon(xy=xys, closed=True, **options))

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
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a circle on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            radius: Radius of the circle.
            style: Style object (required).
            text: Text to display inside shape.
            text_style: Style object for text.
        """
        style, text_style = ShapeUtil.format_styles(
            style,
            text_style,
        )
        angle: Angle = style.angle if style.angle is not None else 0.0

        width = radius * 2
        height = radius * 2
        xy, style = ShapeUtil.apply_alignment(xy, width, height, angle, style, is_default_center=True)
        options = ShapeUtil.get_shape_options(style)
        self._artists.append(
            Circle(
                xy=xy,
                radius=radius,
                **options,
            ),
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
    def ellipse(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        *,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw an ellipse on the canvas.

        Args:
            xy: Center coordinates (x, y) of the ellipse.
            width: Width (major axis) of the ellipse.
            height: Height (minor axis) of the ellipse.
            style: Style of the ellipse (required).
            text (optional): Text to display inside the ellipse.
            text_style (optional): Style of the text.
        """
        style, text_style = ShapeUtil.format_styles(
            style,
            text_style,
        )
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
        self._artists.append(
            Ellipse(
                xy,
                width=width,
                height=height,
                angle=angle,
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
    def regularpolygon(
        self,
        xy: Coordinate,
        num_vertex: NumVertex,
        radius: PosFloat,
        *,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a regular polygon on the canvas.

        Args:
            xy: Center coordinates (x, y) of the regular polygon.
            num_vertex: Number of vertices in the polygon.
            radius: Radius of the circumscribed circle.
            style: Style of the polygon (required).
            text (optional): Text to display inside the polygon.
            text_style (optional): Style of the text.
        """
        style, text_style = ShapeUtil.format_styles(
            style,
            text_style,
        )
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
    def donuts(
        self,
        xy: Coordinate,
        radius: PosFloat,
        *,
        style: Style,
        width: PosFloat | None = None,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a donut shape on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            radius: Outer radius of the donut.
            style: Style object (required).
            width: Width of the donut ring.
            text: Text to display inside shape.
            text_style: Style object for text.
        """
        self.wedge(
            xy=xy,
            radius=radius,
            width=width,
            style=style,
            text=text,
            text_style=text_style,
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
        style: Style,
        mood: FaceMood = "smile",
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw an expressive face shape on the canvas.

        Args:
            xy: Center coordinates (x, y) of the face circle.
            radius: Radius of the face circle.
            style: Style object (required).
            mood: Facial expression ("smile", "neutral", "sad", "angry", or "surprised").
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

        self._artists.append(
            Circle(
                xy=(cx, cy),
                radius=radius,
                facecolor=face_fill,
                edgecolor=stroke_color,
                linewidth=line_w,
                linestyle=line_style,
                zorder=1,
            )
        )

        rad = math.radians(angle)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)

        self._artists.extend(
            _build_face_feature_patches(
                cx=cx,
                cy=cy,
                radius=radius,
                mood=mood,
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


def _build_face_feature_patches(
    cx: float,
    cy: float,
    radius: float,
    mood: str,
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
        mood: Facial expression name.
        cos_a: Cosine of rotation angle.
        sin_a: Sine of rotation angle.
        feature_color: RGBA color for eyes, eyebrows, and mouth.
        feature_w: Line width for mouth and eyebrows.

    Returns:
        List of Circle and PathPatch artists for facial features.
    """

    def xform_pt(lx: float, ly: float) -> tuple[float, float]:
        return (cx + lx * cos_a - ly * sin_a, cy + lx * sin_a + ly * cos_a)

    eye_x = radius * 0.32
    eye_y = radius * 0.13 if mood == "angry" else radius * 0.20
    eye_r = radius * 0.105 if mood == "angry" else radius * 0.11

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

    if mood == "angry":
        brow_verts = [
            xform_pt(-radius * 0.48, radius * 0.40),
            xform_pt(-radius * 0.15, radius * 0.25),
            xform_pt(radius * 0.48, radius * 0.40),
            xform_pt(radius * 0.15, radius * 0.25),
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

    if mood == "smile":
        m_verts = [
            xform_pt(-radius * 0.44, -radius * 0.18),
            xform_pt(-radius * 0.24, -radius * 0.54),
            xform_pt(radius * 0.24, -radius * 0.54),
            xform_pt(radius * 0.44, -radius * 0.18),
        ]
        m_codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
    elif mood == "neutral":
        m_verts = [
            xform_pt(-radius * 0.36, -radius * 0.28),
            xform_pt(radius * 0.36, -radius * 0.28),
        ]
        m_codes = [Path.MOVETO, Path.LINETO]
    elif mood in {"sad", "angry"}:
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


__all__ = ["CanvasShapeBasicFeature"]
