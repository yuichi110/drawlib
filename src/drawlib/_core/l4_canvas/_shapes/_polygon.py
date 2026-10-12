# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.


"""Canvas's original shape feature implementation module."""

import math

from matplotlib.patches import PathPatch
from matplotlib.path import Path
from pydantic import validate_call

from drawlib._core.l2_types import (
    Angle,
    Angle90,
    Coordinate,
    NumVertex,
    PathPoints,
    PosFloat,
    PosInt,
    Ratio,
    Size,
    TailEdge,
)
from drawlib._core.l3_math import rotate_point
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas._shapes._basic import CanvasShapeBasicFeature
from drawlib._core.l4_canvas._shapes._util import ShapeUtil


def _gear_arc_bezier_segment(
    radius: float,
    a_start: float,
    a_end: float,
    cx: float,
    cy: float,
) -> tuple[Coordinate, Coordinate, Coordinate]:
    """Return cubic Bezier control and end points for a circular arc from a_start to a_end."""
    alpha = a_end - a_start
    k = (4.0 / 3.0) * math.tan(alpha / 4.0)
    x0 = cx + radius * math.cos(a_start)
    y0 = cy + radius * math.sin(a_start)
    x3 = cx + radius * math.cos(a_end)
    y3 = cy + radius * math.sin(a_end)
    cp1 = (x0 - k * radius * math.sin(a_start), y0 + k * radius * math.cos(a_start))
    cp2 = (x3 + k * radius * math.sin(a_end), y3 - k * radius * math.cos(a_end))
    return (cp1, cp2, (x3, y3))


def _build_gear_hole_path(cx: float, cy: float, hole_radius: float) -> Path:
    """Build a clockwise circular Matplotlib Path for subtracting a center hole."""
    hr = hole_radius
    kappa = 0.5522847498307936
    k = hr * kappa
    h_verts: list[Coordinate] = [
        (cx, cy + hr),
        (cx + k, cy + hr),
        (cx + hr, cy + k),
        (cx + hr, cy),
        (cx + hr, cy - k),
        (cx + k, cy - hr),
        (cx, cy - hr),
        (cx - k, cy - hr),
        (cx - hr, cy - k),
        (cx - hr, cy),
        (cx - hr, cy + k),
        (cx - k, cy + hr),
        (cx, cy + hr),
        (cx, cy + hr),
    ]
    h_codes = [
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
    return Path(vertices=h_verts, codes=h_codes)


def _build_gear_outer_path_points(
    cx: float,
    cy: float,
    num_teeth: int,
    radius_ext: float,
    radius_int: float,
    ext_ratio: float,
    int_ratio: float,
    angle: float,
    shape_r: float | tuple[float, ...] | None,
) -> PathPoints:
    """Build outer path points for a gear shape with either rounded corners or exact circular arcs."""
    pitch_angle = (2.0 * math.pi) / num_teeth
    half_ext = (ext_ratio * pitch_angle) / 2.0
    half_int = (int_ratio * pitch_angle) / 2.0
    start_angle = math.pi / 2.0 + math.radians(angle)

    radii = ShapeUtil._normalize_shape_radii(4 * num_teeth, shape_r)
    if radii is not None:
        points_world: list[Coordinate] = []
        for i in range(num_teeth):
            center_a = start_angle + i * pitch_angle
            a1 = center_a - half_int
            a2 = center_a - half_ext
            a3 = center_a + half_ext
            a4 = center_a + half_int
            points_world.append((cx + radius_int * math.cos(a1), cy + radius_int * math.sin(a1)))
            points_world.append((cx + radius_ext * math.cos(a2), cy + radius_ext * math.sin(a2)))
            points_world.append((cx + radius_ext * math.cos(a3), cy + radius_ext * math.sin(a3)))
            points_world.append((cx + radius_int * math.cos(a4), cy + radius_int * math.sin(a4)))
        return ShapeUtil.round_polygon_points(points_world, shape_r)

    path_points: PathPoints = []
    for i in range(num_teeth):
        center_a = start_angle + i * pitch_angle
        a1 = center_a - half_int
        a2 = center_a - half_ext
        a3 = center_a + half_ext
        a4 = center_a + half_int
        next_a1 = (start_angle + (i + 1) * pitch_angle) - half_int

        if i == 0:
            path_points.append((cx + radius_int * math.cos(a1), cy + radius_int * math.sin(a1)))
        path_points.append((cx + radius_ext * math.cos(a2), cy + radius_ext * math.sin(a2)))
        path_points.append(_gear_arc_bezier_segment(radius_ext, a2, a3, cx, cy))
        path_points.append((cx + radius_int * math.cos(a4), cy + radius_int * math.sin(a4)))
        path_points.append(_gear_arc_bezier_segment(radius_int, a4, next_a1, cx, cy))
    return path_points


class CanvasShapePolygonFeature(CanvasShapeBasicFeature):
    """Canvas polygon shape feature implementation module.

    This class provides methods to draw various polygonal shapes such as
    triangles, parallelograms, trapezoids, rhombuses, chevrons, stars, and gears
    on a canvas.
    """

    def __init__(self) -> None:
        """Initializes a CanvasShapePolygonFeature object."""
        super().__init__()

    @validate_call
    def triangle(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        topvertex_x: float | None = None,
        *,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a triangle on the canvas.

        Args:
            xy: Bottom-left coordinate tuple (x, y).
            width: Width of triangle.
            height: Height of triangle.
            topvertex_x: X-offset of top vertex relative to left edge.
            style: Style object.
            text: Text to display inside shape.
            text_style: Style object for text or None.
        """
        style, text_style = ShapeUtil.format_styles(
            style,
            text_style,
        )

        if topvertex_x is None:
            topvertex_x = width / 2
        p1 = (0, 0)
        p2 = (topvertex_x, height)
        p3 = (width, 0)
        path_points = ShapeUtil.round_polygon_points([p1, p2, p3], style.shape_r)
        self.shape(
            xy=xy,
            path_points=path_points,
            style=style,
            text=text,
            text_style=text_style,
        )

    @validate_call
    def parallelogram(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        corner_angle: Angle90,
        *,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a parallelogram on the canvas.

        Args:
            xy: Bottom-left coordinate tuple (x, y).
            width: Width of parallelogram.
            height: Height of parallelogram.
            corner_angle: Corner angle in degrees.
            style: Style object.
            text: Text to display inside shape.
            text_style: Style object for text or None.
        """
        style, text_style = ShapeUtil.format_styles(
            style,
            text_style,
        )

        def calculate_parallelogram_lefttop_coordinate() -> Coordinate:
            angle_rad = math.radians(corner_angle)
            x = height / math.tan(angle_rad)
            return x, height

        p1 = (0, 0)
        p2 = calculate_parallelogram_lefttop_coordinate()
        p3 = (p2[0] + width, height)
        p4 = (width, 0)
        path_points = ShapeUtil.round_polygon_points([p1, p2, p3, p4], style.shape_r)

        self.shape(
            xy=xy,
            path_points=path_points,
            style=style,
            text=text,
            text_style=text_style,
        )

    @validate_call
    def trapezoid(
        self,
        xy: Coordinate,
        height: PosFloat,
        bottomedge_width: PosFloat,
        topedge_width: PosFloat,
        topedge_x: float | None = None,
        *,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a trapezoid on the canvas.

        Args:
            xy: Bottom-left coordinate tuple (x, y).
            height: Height of trapezoid.
            bottomedge_width: Width of bottom edge.
            topedge_width: Width of top edge.
            topedge_x: X-offset of top edge left vertex.
            style: Style object.
            text: Text to display inside shape.
            text_style: Style object for text or None.
        """
        style, text_style = ShapeUtil.format_styles(
            style,
            text_style,
        )

        if topedge_x is None:
            topedge_x = (bottomedge_width - topedge_width) / 2
        p1 = (0, 0)
        p2 = (topedge_x, height)
        p3 = (topedge_x + topedge_width, height)
        p4 = (bottomedge_width, 0)
        path_points = ShapeUtil.round_polygon_points([p1, p2, p3, p4], style.shape_r)

        self.shape(
            xy=xy,
            path_points=path_points,
            style=style,
            text=text,
            text_style=text_style,
        )

    @validate_call
    def rhombus(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        *,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a rhombus on the canvas.

        Args:
            xy: Center or bottom-left coordinate tuple (x, y).
            width: Horizontal diagonal length.
            height: Vertical diagonal length.
            style: Style object.
            text: Text to display inside shape.
            text_style: Style object for text or None.
        """
        style, text_style = ShapeUtil.format_styles(
            style,
            text_style,
        )

        p1 = (0, height / 2)
        p2 = (width / 2, height)
        p3 = (width, height / 2)
        p4 = (width / 2, 0)
        path_points = ShapeUtil.round_polygon_points([p1, p2, p3, p4], style.shape_r)

        self.shape(
            xy=xy,
            path_points=path_points,
            style=style,
            text=text,
            text_style=text_style,
        )

    @validate_call
    def chevron(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        corner_angle: Angle90,
        mirror: bool = False,
        *,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a chevron (arrow-head block) shape on the canvas.

        Args:
            xy: Bottom-left coordinate tuple (x, y).
            width: Width of chevron.
            height: Height of chevron.
            corner_angle: Angle of the arrowhead point.
            mirror: Whether to mirror chevron horizontally.
            style: Style object.
            text: Text to display inside shape.
            text_style: Style object for text or None.
        """
        style, text_style = ShapeUtil.format_styles(
            style,
            text_style,
        )

        def calculate_p2_coordinate(h: float) -> Coordinate:
            h /= 2
            angle_rad = math.radians(corner_angle)
            x = h / math.tan(angle_rad)
            return x, h

        p1 = (0, 0)
        p2 = calculate_p2_coordinate(height)
        p3 = (0, height)
        p4 = (width, height)
        p5 = (width + p2[0], height / 2)
        p6 = (width, 0)

        if mirror:
            p2 = (p2[0] * -1, p2[1])
            p4 = (p4[0] * -1, p4[1])
            p5 = (p5[0] * -1, p5[1])
            p6 = (p6[0] * -1, p6[1])

        path_points = ShapeUtil.round_polygon_points([p1, p2, p3, p4, p5, p6], style.shape_r)

        self.shape(
            xy=xy,
            path_points=path_points,
            style=style,
            text=text,
            text_style=text_style,
        )

    @validate_call
    def star(
        self,
        xy: Coordinate,
        num_vertex: NumVertex,
        radius_ext: PosFloat,
        radius_int: PosFloat,
        *,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a star shape on the canvas.

        Args:
            xy: Center coordinate tuple (x, y).
            num_vertex: Number of star points.
            radius_ext: Outer radius of star points.
            radius_int: Inner radius of star points.
            style: Style object.
            text: Text to display inside shape.
            text_style: Style object for text or None.
        """
        style, text_style = ShapeUtil.format_styles(
            style,
            text_style,
        )
        angle: Angle = style.angle if style.angle is not None else 0.0

        if radius_ext < radius_int:
            raise ValueError("radius_ext must be bigger than radius_int.")

        # calculate points

        points = []
        start_angle = math.pi / 2
        for i in range(2 * num_vertex):
            r = radius_ext if i % 2 == 0 else radius_int
            point_angle = start_angle + i * 2 * math.pi / (2 * num_vertex)
            x = r * math.cos(point_angle)
            y = r * math.sin(point_angle)
            points.append((x, y))

        # move x, y which fit to alignment

        width = radius_ext * 2
        height = radius_ext * 2
        x, y = xy
        x -= width / 2
        y -= height / 2
        xy = (x, y)
        ((x, y), style) = ShapeUtil.apply_alignment(
            xy,
            width,
            height,
            angle,
            style,
            is_default_center=True,
        )

        # shift

        cx = x + width / 2
        cy = y + height / 2
        points2: list[Coordinate] = []
        for pp in points:
            rx, ry = rotate_point(pp, angle=angle)
            points2.append((rx + cx, ry + cy))

        # create Path
        path_points = ShapeUtil.round_polygon_points(points2, style.shape_r)
        path = ShapeUtil.build_matplotlib_path(path_points)

        # create PathPatch

        options = ShapeUtil.get_shape_options(style)
        self._artists.append(PathPatch(path=path, **options))

        if text:
            effective_text_style = ShapeUtil.resolve_embedded_text_style(style, text_style)
            self._artists.append(
                ShapeUtil.get_shape_text(
                    xy=(cx, cy),
                    text=text,
                    angle=angle,
                    style=effective_text_style,
                )
            )

    @validate_call
    def gear(
        self,
        xy: Coordinate,
        num_teeth: NumVertex,
        radius_ext: PosFloat,
        radius_int: PosFloat,
        *,
        tooth_ext_ratio: Ratio | None = None,
        tooth_int_ratio: Ratio | None = None,
        hole_radius: PosFloat | None = None,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a gear shape on the canvas.

        Args:
            xy: Center coordinate tuple (x, y).
            num_teeth: Number of gear teeth (must be >= 3).
            radius_ext: Outer radius of gear tooth tips.
            radius_int: Inner radius of gear tooth roots/valleys.
            tooth_ext_ratio: Ratio of 1 pitch angle (360 / num_teeth) for the outer tooth tip.
                Defaults to 0.35 when None.
            tooth_int_ratio: Ratio of 1 pitch angle (360 / num_teeth) for the inner tooth base.
                Defaults to 0.55 when None.
            hole_radius: Radius of the center circular hole, or None for no hole.
            style: Style object.
            text: Text to display inside shape.
            text_style: Style object for text or None.

        Raises:
            ValueError: If radii, tooth ratios, or hole_radius are out of valid bounds.
        """
        style, text_style = ShapeUtil.format_styles(
            style,
            text_style,
        )
        angle: Angle = style.angle if style.angle is not None else 0.0

        if radius_int <= 0.0:
            raise ValueError("radius_int must be positive.")
        if radius_ext <= radius_int:
            raise ValueError("radius_ext must be bigger than radius_int.")

        ext_ratio = 0.35 if tooth_ext_ratio is None else float(tooth_ext_ratio)
        int_ratio = 0.55 if tooth_int_ratio is None else float(tooth_int_ratio)
        if not (0.0 < ext_ratio < 1.0):
            raise ValueError("tooth_ext_ratio must be strictly between 0.0 and 1.0.")
        if not (0.0 < int_ratio < 1.0):
            raise ValueError("tooth_int_ratio must be strictly between 0.0 and 1.0.")

        if hole_radius is not None and (hole_radius <= 0.0 or hole_radius >= radius_int):
            raise ValueError("hole_radius must be positive and smaller than radius_int.")

        width = radius_ext * 2.0
        height = radius_ext * 2.0
        x, y = xy
        xy_shifted = (x - width / 2.0, y - height / 2.0)
        ((x, y), style) = ShapeUtil.apply_alignment(
            xy_shifted,
            width,
            height,
            angle,
            style,
            is_default_center=True,
        )
        cx = x + width / 2.0
        cy = y + height / 2.0

        path_points = _build_gear_outer_path_points(
            cx=cx,
            cy=cy,
            num_teeth=num_teeth,
            radius_ext=radius_ext,
            radius_int=radius_int,
            ext_ratio=ext_ratio,
            int_ratio=int_ratio,
            angle=angle,
            shape_r=style.shape_r,
        )

        outer_path = ShapeUtil.build_matplotlib_path(path_points)
        if hole_radius is not None:
            hole_path = _build_gear_hole_path(cx, cy, hole_radius)
            path = Path.make_compound_path(outer_path, hole_path)
        else:
            path = outer_path

        options = ShapeUtil.get_shape_options(style)
        self._artists.append(PathPatch(path=path, **options))

        if text:
            effective_text_style = ShapeUtil.resolve_embedded_text_style(style, text_style)
            self._artists.append(
                ShapeUtil.get_shape_text(
                    xy=(cx, cy),
                    text=text,
                    angle=angle,
                    style=effective_text_style,
                )
            )

    @validate_call
    def bubblespeech(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        tail_edge: TailEdge,
        tail_start_ratio: Ratio,
        tail_vertex_xy: Coordinate,
        tail_end_ratio: Ratio,
        *,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a speech bubble shape on the canvas.

        Args:
            xy: The (x, y) coordinates of the bottom-left corner of the bubble body.
            width: The width of the bubble body.
            height: The height of the bubble body.
            tail_edge: The edge ("left", "top", "right", "bottom") where the tail originates.
            tail_start_ratio: Ratio (between 0.0 and 1.0) along the edge where the tail begins.
            tail_vertex_xy: The (x, y) target coordinates pointing to the vertex of the tail.
            tail_end_ratio: Ratio (between 0.0 and 1.0) along the edge where the tail ends.
            style: The Style of the speech bubble shape (required).
            text: Optional text to display inside the bubble. Defaults to an empty string.
            text_style: Optional Style of the text.

        Raises:
            ValueError: If tail_start_ratio is greater than or equal to tail_end_ratio.
        """
        if tail_start_ratio >= tail_end_ratio:
            raise ValueError("tail_start_ratio must be smaller than tail_end_ratio.")

        x, y = xy
        xys: list[Coordinate] = [(x, y)]  # left bottom

        if tail_edge == "left":
            xys.append((x, y + height * tail_start_ratio))
            xys.append(tail_vertex_xy)
            xys.append((x, y + height * tail_end_ratio))
        xys.append((x, y + height))  # left top

        if tail_edge == "top":
            xys.append((x + width * tail_start_ratio, y + height))
            xys.append(tail_vertex_xy)
            xys.append((x + width * tail_end_ratio, y + height))
        xys.append((x + width, y + height))  # right top

        if tail_edge == "right":
            xys.append((x + width, y + height * tail_end_ratio))
            xys.append(tail_vertex_xy)
            xys.append((x + width, y + height * tail_start_ratio))
        xys.append((x + width, y))  # right bottom

        if tail_edge == "bottom":
            xys.append((x + width * tail_end_ratio, y))
            xys.append(tail_vertex_xy)
            xys.append((x + width * tail_start_ratio, y))

        self.polygon(xys=xys, style=style.patch(shape_r=0.0))


        if text:
            center_x = x + width / 2.0
            center_y = y + height / 2.0
            effective_text_style = ShapeUtil.resolve_embedded_text_style(style, text_style)
            self._artists.append(
                ShapeUtil.get_shape_text(
                    xy=(center_x, center_y),
                    text=text,
                    angle=0.0,
                    style=effective_text_style,
                )
            )


__all__ = [
    "CanvasShapePolygonFeature",
]
