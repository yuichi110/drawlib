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


class CanvasShapePolygonFeature(CanvasShapeBasicFeature):
    """Canvas polygon shape feature implementation module.

    This class provides methods to draw various polygonal shapes such as
    triangles, parallelograms, trapezoids, rhombuses, chevrons, and stars
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
