# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Canvas polygon, star, plaque, and custom path shape feature implementation module."""

from __future__ import annotations

import math

from matplotlib.patches import PathPatch, Polygon, RegularPolygon
from matplotlib.path import Path
from pydantic import validate_call

from drawlib._core.l2_types import (
    Angle,
    Angle90,
    Coordinate,
    Coordinates,
    NumVertex,
    PathPoints,
    PlaqueVariant,
    PosFloat,
    Ratio,
)
from drawlib._core.l3_math import (
    get_center_and_size,
    get_rotated_points,
    rotate_point,
)
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas._shapes._basic import CanvasShapeBasicFeature
from drawlib._core.l4_canvas._shapes._shape_utils import ShapeUtils


def build_plaque_path(
    xy: Coordinate,
    width: float,
    height: float,
    variant: str,
    cut_ratio: float | None,
    shape_r: float | tuple[float, ...] | None,
    angle: float,
) -> Path:
    """Build world-space Matplotlib Path for plaque shape variants."""
    cx, cy = xy
    hw, hh = width / 2.0, height / 2.0
    c_ratio = 0.22 if cut_ratio is None else float(cut_ratio)
    r = min(width, height) * min(0.45, c_ratio)

    if variant in {"concave", "standard"}:
        local_pts = (
            ShapeUtils.arc_points_local(hw, -hh, r, 180.0, 90.0, 12)
            + ShapeUtils.arc_points_local(hw, hh, r, 270.0, 180.0, 12)
            + ShapeUtils.arc_points_local(-hw, hh, r, 0.0, -90.0, 12)
            + ShapeUtils.arc_points_local(-hw, -hh, r, 90.0, 0.0, 12)
        )
        return ShapeUtils.subpaths_to_compound_path([local_pts], cx, cy, angle)

    if variant in {"chamfered", "octagon"}:
        local_pts = [
            (-hw + r, -hh),
            (hw - r, -hh),
            (hw, -hh + r),
            (hw, hh - r),
            (hw - r, hh),
            (-hw + r, hh),
            (-hw, hh - r),
            (-hw, -hh + r),
        ]
    else:
        # "notched"
        local_pts = [
            (-hw + r, -hh),
            (hw - r, -hh),
            (hw - r, -hh + r),
            (hw, -hh + r),
            (hw, hh - r),
            (hw - r, hh - r),
            (hw - r, hh),
            (-hw + r, hh),
            (-hw + r, hh - r),
            (-hw, hh - r),
            (-hw, -hh + r),
            (-hw + r, -hh + r),
        ]

    world_pts: list[Coordinate] = []
    for lx, ly in local_pts:
        rx, ry = rotate_point((lx, ly), angle=angle)
        world_pts.append((cx + rx, cy + ry))
    path_points = ShapeUtils.round_polygon_points(world_pts, shape_r)
    return ShapeUtils.build_matplotlib_path(path_points)


class CanvasShapePolygonFeature(CanvasShapeBasicFeature):
    """Canvas polygon shape feature implementation module.

    Provides triangle, parallelogram, trapezoid, rhombus, regularpolygon,
    star, plaque, polygon, and custom path shape methods.
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
        hole_ratio: Ratio | None = None,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a triangle on the canvas.

        Args:
            xy: Center or bottom-left coordinate tuple (x, y).
            width: Width of triangle.
            height: Height of triangle.
            topvertex_x: X-offset of top vertex relative to left edge.
            hole_ratio: Optional hollow cutout ratio in (0.0, 1.0).
            style: Style object.
            text: Text to display inside shape.
            text_style: Style object for text or None.
        """
        ShapeUtils.validate_hole_ratio(hole_ratio)
        style, text_style = ShapeUtils.format_styles(
            style,
            text_style,
        )

        if topvertex_x is None:
            topvertex_x = width / 2
        p1 = (0.0, 0.0)
        p2 = (topvertex_x, height)
        p3 = (width, 0.0)
        ShapeUtils.draw_convex_polygon_with_hole(
            artists=self._artists,
            xy=xy,
            vertices=[p1, p2, p3],
            hole_ratio=hole_ratio,
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
        hole_ratio: Ratio | None = None,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a parallelogram on the canvas.

        Args:
            xy: Center or bottom-left coordinate tuple (x, y).
            width: Width of parallelogram.
            height: Height of parallelogram.
            corner_angle: Corner angle in degrees.
            hole_ratio: Optional hollow cutout ratio in (0.0, 1.0).
            style: Style object.
            text: Text to display inside shape.
            text_style: Style object for text or None.
        """
        ShapeUtils.validate_hole_ratio(hole_ratio)
        style, text_style = ShapeUtils.format_styles(
            style,
            text_style,
        )

        angle_rad = math.radians(corner_angle)
        x_top = height / math.tan(angle_rad)
        p1 = (0.0, 0.0)
        p2 = (x_top, height)
        p3 = (x_top + width, height)
        p4 = (width, 0.0)
        ShapeUtils.draw_convex_polygon_with_hole(
            artists=self._artists,
            xy=xy,
            vertices=[p1, p2, p3, p4],
            hole_ratio=hole_ratio,
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
        hole_ratio: Ratio | None = None,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a trapezoid on the canvas.

        Args:
            xy: Center or bottom-left coordinate tuple (x, y).
            height: Height of trapezoid.
            bottomedge_width: Width of bottom edge.
            topedge_width: Width of top edge.
            topedge_x: X-offset of top edge left vertex.
            hole_ratio: Optional hollow cutout ratio in (0.0, 1.0).
            style: Style object.
            text: Text to display inside shape.
            text_style: Style object for text or None.
        """
        ShapeUtils.validate_hole_ratio(hole_ratio)
        style, text_style = ShapeUtils.format_styles(
            style,
            text_style,
        )

        if topedge_x is None:
            topedge_x = (bottomedge_width - topedge_width) / 2
        p1 = (0.0, 0.0)
        p2 = (topedge_x, height)
        p3 = (topedge_x + topedge_width, height)
        p4 = (bottomedge_width, 0.0)
        ShapeUtils.draw_convex_polygon_with_hole(
            artists=self._artists,
            xy=xy,
            vertices=[p1, p2, p3, p4],
            hole_ratio=hole_ratio,
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
        hole_ratio: Ratio | None = None,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a rhombus on the canvas.

        Args:
            xy: Center or bottom-left coordinate tuple (x, y).
            width: Horizontal diagonal length.
            height: Vertical diagonal length.
            hole_ratio: Optional hollow cutout ratio in (0.0, 1.0).
            style: Style object.
            text: Text to display inside shape.
            text_style: Style object for text or None.
        """
        ShapeUtils.validate_hole_ratio(hole_ratio)
        style, text_style = ShapeUtils.format_styles(
            style,
            text_style,
        )

        p1 = (0.0, height / 2)
        p2 = (width / 2, height)
        p3 = (width, height / 2)
        p4 = (width / 2, 0.0)
        ShapeUtils.draw_convex_polygon_with_hole(
            artists=self._artists,
            xy=xy,
            vertices=[p1, p2, p3, p4],
            hole_ratio=hole_ratio,
            style=style,
            text=text,
            text_style=text_style,
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
        style, text_style = ShapeUtils.format_styles(
            style,
            text_style,
        )
        h_ratio = ShapeUtils.validate_hole_ratio(hole_ratio)
        xy, angle, style = ShapeUtils.prepare_centered_shape(xy, radius * 2, radius * 2, style)

        angle_rad = math.radians(angle)
        options = ShapeUtils.get_shape_options(style)
        if h_ratio is not None or style.shape_r is not None:
            start_a = math.pi / 2.0 + angle_rad
            verts: list[Coordinate] = [
                (
                    xy[0] + radius * math.cos(start_a + i * 2.0 * math.pi / num_vertex),
                    xy[1] + radius * math.sin(start_a + i * 2.0 * math.pi / num_vertex),
                )
                for i in range(num_vertex)
            ]
            path_points = ShapeUtils.round_polygon_points(verts, style.shape_r)
            if h_ratio is not None:
                inner_verts, inset = ShapeUtils.inset_convex_polygon(verts, h_ratio)
                inner_r = ShapeUtils.shrink_shape_r(style.shape_r, inset, reversed_order=True)
                inner_points = ShapeUtils.round_polygon_points(inner_verts, inner_r)
                outer_path = ShapeUtils.build_matplotlib_path(path_points)
                inner_path = ShapeUtils.build_matplotlib_path(inner_points)
                path = Path.make_compound_path(outer_path, inner_path)
                patch: RegularPolygon | PathPatch = PathPatch(path=path, **options)
            elif len(path_points) == num_vertex and all(isinstance(p[0], (int, float)) for p in path_points):
                patch = RegularPolygon(
                    xy,
                    numVertices=num_vertex,
                    radius=radius,
                    orientation=angle_rad,
                    **options,
                )
            else:
                path = ShapeUtils.build_matplotlib_path(path_points)
                patch = PathPatch(path=path, **options)
        else:
            patch = RegularPolygon(
                xy,
                numVertices=num_vertex,
                radius=radius,
                orientation=angle_rad,
                **options,
            )

        ShapeUtils.append_patches_and_text(
            artists=self._artists,
            patches=[patch],
            style=style,
            text=text,
            text_style=text_style,
            text_xy=xy,
            angle=angle,
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
        style, text_style = ShapeUtils.format_styles(
            style,
            text_style,
        )
        if radius_ext < radius_int:
            raise ValueError("radius_ext must be bigger than radius_int.")

        points: list[Coordinate] = []
        start_angle = math.pi / 2.0
        for i in range(2 * num_vertex):
            r = radius_ext if i % 2 == 0 else radius_int
            point_angle = start_angle + i * 2.0 * math.pi / (2 * num_vertex)
            points.append((r * math.cos(point_angle), r * math.sin(point_angle)))

        width = radius_ext * 2.0
        height = radius_ext * 2.0
        (cx, cy), angle, style = ShapeUtils.prepare_centered_shape(
            xy=xy,
            width=width,
            height=height,
            style=style,
        )

        points2: list[Coordinate] = []
        for pp in points:
            rx, ry = rotate_point(pp, angle=angle)
            points2.append((rx + cx, ry + cy))

        path_points = ShapeUtils.round_polygon_points(points2, style.shape_r)
        path = ShapeUtils.build_matplotlib_path(path_points)
        ShapeUtils.append_path_and_text(
            artists=self._artists,
            path=path,
            style=style,
            text=text,
            text_style=text_style,
            text_xy=(cx, cy),
            angle=angle,
        )

    @validate_call
    def plaque(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        *,
        variant: PlaqueVariant = "concave",
        cut_ratio: Ratio | None = None,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
    ) -> None:
        """Draw a corner-cut plaque or ornamental plate shape on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            width: Width of the plaque bounding box.
            height: Height of the plaque bounding box.
            variant: Plaque corner variant ("concave", "standard", "chamfered",
                "octagon", "notched").
            cut_ratio: Optional corner cutout size ratio in (0.0, 1.0).
            style: Style object (required).
            text: Text to display inside shape.
            text_style: Style object for text.
        """
        ShapeUtils.validate_hole_ratio(cut_ratio)
        style, text_style = ShapeUtils.format_styles(style, text_style)
        (cx, cy), angle, style = ShapeUtils.prepare_centered_shape(
            xy=xy,
            width=width,
            height=height,
            style=style,
        )
        path = build_plaque_path(
            xy=(cx, cy),
            width=width,
            height=height,
            variant=variant,
            cut_ratio=cut_ratio,
            shape_r=style.shape_r,
            angle=angle,
        )
        ShapeUtils.append_path_and_text(
            artists=self._artists,
            path=path,
            style=style,
            text=text,
            text_style=text_style,
            text_xy=(cx, cy),
            angle=angle,
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
        style, text_style = ShapeUtils.format_styles(
            style,
            text_style,
        )

        path_points = ShapeUtils.round_polygon_points(list(xys), style.shape_r)
        style = style.patch(halign=None, valign=None)
        options = ShapeUtils.get_shape_options(style)
        if len(path_points) == len(xys) and all(isinstance(p[0], (int, float)) for p in path_points):
            self._artists.append(Polygon(xy=xys, closed=True, **options))
        else:
            path = ShapeUtils.build_matplotlib_path(path_points)
            self._artists.append(PathPatch(path=path, **options))

        if not text:
            return
        effective_text_style = ShapeUtils.resolve_embedded_text_style(style, text_style)
        center, (_, _) = get_center_and_size(xys)
        self._artists.append(
            ShapeUtils.get_shape_text(
                center,
                text=text,
                angle=0,
                style=effective_text_style,
            ),
        )

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
        ShapeUtils.draw_shape_path_points(
            artists=self._artists,
            xy=xy,
            path_points=path_points,
            style=style,
            text=text,
            text_style=text_style,
            is_default_center=is_default_center,
        )


__all__ = [
    "CanvasShapePolygonFeature",
]
