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
    TypeAngle,
    TypeAngle90,
    TypeBool,
    TypeCoordinate,
    TypeFloat,
    TypeNumVertex,
    TypePosFloat,
    TypePosInt,
    TypeSize,
    TypeStr,
)
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas._base import CanvasBase
from drawlib._core.l4_canvas_utils import ShapeUtil, TextUtil


class CanvasOriginalPolygonFeature(CanvasBase):
    """Canvas's original shape feature implementation module.

    This class provides methods to draw various polygonal shapes such as
    triangles, parallelograms, trapezoids, rhombuses, chevrons, and stars
    on a canvas.
    """

    def __init__(self) -> None:
        """Initializes a CanvasOriginalPolygonFeature object.

        Initializes an instance of CanvasOriginalPolygonFeature by calling the
        constructor of its superclass, CanvasBase.
        """
        super().__init__()

    @validate_call
    def triangle(
        self,
        xy: TypeCoordinate,
        width: TypePosFloat,
        height: TypePosFloat,
        topvertex_x: TypeFloat | None = None,
        angle: TypeAngle = 0.0,
        *,
        style: Style,
        text: TypeStr = "",
        textsize: TypeSize | None = None,
        textstyle: Style | None = None,
    ) -> None:
        """Draw a triangle on the canvas.

        Args:
            xy: Bottom-left coordinate tuple (x, y).
            width: Width of triangle.
            height: Height of triangle.
            topvertex_x: X-offset of top vertex relative to left edge.
            angle: Rotation angle in degrees.
            style: Style object.
            text: Text to display inside shape.
            textsize: Font size of text.
            textstyle: Style object for text or None.
        """
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
        )

        if topvertex_x is None:
            topvertex_x = width / 2
        p1 = (0, 0)
        p2 = (topvertex_x, height)
        p3 = (width, 0)
        self.shape(
            xy=xy,
            path_points=[p1, p2, p3],
            angle=angle,
            style=style,
            text=text,
            textsize=textsize,
            textstyle=textstyle,
        )

    @validate_call
    def parallelogram(
        self,
        xy: TypeCoordinate,
        width: TypePosFloat,
        height: TypePosFloat,
        corner_angle: TypeAngle90,
        angle: TypeAngle = 0.0,
        *,
        style: Style,
        text: TypeStr = "",
        textsize: TypeSize | None = None,
        textstyle: Style | None = None,
    ) -> None:
        """Draw a parallelogram on the canvas.

        Args:
            xy: Bottom-left coordinate tuple (x, y).
            width: Width of parallelogram.
            height: Height of parallelogram.
            corner_angle: Corner angle in degrees.
            angle: Rotation angle in degrees.
            style: Style object.
            text: Text to display inside shape.
            textsize: Font size of text.
            textstyle: Style object for text or None.
        """
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
        )

        def calculate_parallelogram_lefttop_coordinate() -> TypeCoordinate:
            angle_rad = math.radians(corner_angle)
            x = height / math.tan(angle_rad)
            return x, height

        p1 = (0, 0)
        p2 = calculate_parallelogram_lefttop_coordinate()
        p3 = (p2[0] + width, height)
        p4 = (width, 0)

        self.shape(
            xy=xy,
            path_points=[p1, p2, p3, p4],
            angle=angle,
            style=style,
            text=text,
            textsize=textsize,
            textstyle=textstyle,
        )

    @validate_call
    def trapezoid(
        self,
        xy: TypeCoordinate,
        height: TypePosFloat,
        bottomedge_width: TypePosFloat,
        topedge_width: TypePosFloat,
        topedge_x: TypeFloat | None = None,
        angle: TypeAngle = 0.0,
        *,
        style: Style,
        text: TypeStr = "",
        textsize: TypeSize | None = None,
        textstyle: Style | None = None,
    ) -> None:
        """Draw a trapezoid on the canvas.

        Args:
            xy: Bottom-left coordinate tuple (x, y).
            height: Height of trapezoid.
            bottomedge_width: Width of bottom edge.
            topedge_width: Width of top edge.
            topedge_x: X-offset of top edge left vertex.
            angle: Rotation angle in degrees.
            style: Style object.
            text: Text to display inside shape.
            textsize: Font size of text.
            textstyle: Style object for text or None.
        """
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
        )

        if topedge_x is None:
            topedge_x = (bottomedge_width - topedge_width) / 2
        p1 = (0, 0)
        p2 = (topedge_x, height)
        p3 = (topedge_x + topedge_width, height)
        p4 = (bottomedge_width, 0)

        self.shape(
            xy=xy,
            path_points=[p1, p2, p3, p4],
            angle=angle,
            style=style,
            text=text,
            textsize=textsize,
            textstyle=textstyle,
        )

    @validate_call
    def rhombus(
        self,
        xy: TypeCoordinate,
        width: TypePosFloat,
        height: TypePosFloat,
        angle: TypeAngle = 0.0,
        *,
        style: Style,
        text: TypeStr = "",
        textsize: TypeSize | None = None,
        textstyle: Style | None = None,
    ) -> None:
        """Draw a rhombus on the canvas.

        Args:
            xy: Center or bottom-left coordinate tuple (x, y).
            width: Horizontal diagonal length.
            height: Vertical diagonal length.
            angle: Rotation angle in degrees.
            style: Style object.
            text: Text to display inside shape.
            textsize: Font size of text.
            textstyle: Style object for text or None.
        """
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
        )

        p1 = (0, height / 2)
        p2 = (width / 2, height)
        p3 = (width, height / 2)
        p4 = (width / 2, 0)

        self.shape(
            xy=xy,
            path_points=[p1, p2, p3, p4],
            angle=angle,
            style=style,
            text=text,
            textsize=textsize,
            textstyle=textstyle,
        )

    @validate_call
    def chevron(
        self,
        xy: TypeCoordinate,
        width: TypePosFloat,
        height: TypePosFloat,
        corner_angle: TypeAngle90,
        mirror: TypeBool = False,
        angle: TypeAngle = 0.0,
        *,
        style: Style,
        text: TypeStr = "",
        textsize: TypeSize | None = None,
        textstyle: Style | None = None,
    ) -> None:
        """Draw a chevron (arrow-head block) shape on the canvas.

        Args:
            xy: Bottom-left coordinate tuple (x, y).
            width: Width of chevron.
            height: Height of chevron.
            corner_angle: Angle of the arrowhead point.
            mirror: Whether to mirror chevron horizontally.
            angle: Rotation angle in degrees.
            style: Style object.
            text: Text to display inside shape.
            textsize: Font size of text.
            textstyle: Style object for text or None.
        """
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
        )

        def calculate_p2_coordinate(h: float) -> TypeCoordinate:
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

        self.shape(
            xy=xy,
            path_points=[p1, p2, p3, p4, p5, p6],
            angle=angle,
            style=style,
            text=text,
            textsize=textsize,
            textstyle=textstyle,
        )

    @validate_call
    def star(
        self,
        xy: TypeCoordinate,
        num_vertex: TypeNumVertex,
        radius_ext: TypePosFloat,
        radius_int: TypePosFloat,
        angle: TypeAngle = 0.0,
        *,
        style: Style,
        text: TypeStr = "",
        textsize: TypeSize | None = None,
        textstyle: Style | None = None,
    ) -> None:
        """Draw a star shape on the canvas.

        Args:
            xy: Center coordinate tuple (x, y).
            num_vertex: Number of star points.
            radius_ext: Outer radius of star points.
            radius_int: Inner radius of star points.
            angle: Rotation angle in degrees.
            style: Style object.
            text: Text to display inside shape.
            textsize: Font size of text.
            textstyle: Style object for text or None.
        """
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
        )

        if radius_ext < radius_int:
            raise ValueError("radius_ext must be bigger than radius_int.")

        # helper

        def get_rotate_point(
            x: TypeFloat,
            y: TypeFloat,
            angle: TypeFloat | None,
            move_x: TypeFloat,
            move_y: TypeFloat,
        ) -> TypeCoordinate:
            if angle is None:
                angle = 0.0
            angle_rad = math.radians(angle)
            x_rotated = x * math.cos(angle_rad) - y * math.sin(angle_rad)
            y_rotated = x * math.sin(angle_rad) + y * math.cos(angle_rad)
            return x_rotated + move_x, y_rotated + move_y

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
        points2 = []
        for pp in points:
            x1, y1 = get_rotate_point(x=pp[0], y=pp[1], angle=angle, move_x=cx, move_y=cy)
            points2.append((x1, y1))

        # create Path

        vertices = [points2[0]]
        codes = [Path.MOVETO]
        for p in points2[1:]:
            vertices.append((p[0], p[1]))
            codes.append(Path.LINETO)
        vertices.append(points2[0])
        codes.append(Path.CLOSEPOLY)
        path = Path(vertices=vertices, codes=codes)

        # create PathPatch

        options = ShapeUtil.get_shape_options(style)
        self._artists.append(PathPatch(path=path, **options))

        if text:
            effective_textstyle = textstyle if textstyle is not None else style
            if textsize is not None:
                effective_textstyle = effective_textstyle.patch(text_size=textsize)
            TextUtil.validate_text_style(effective_textstyle)
            self._artists.append(
                ShapeUtil.get_shape_text(
                    xy=(cx, cy),
                    text=text,
                    angle=angle,
                    style=effective_textstyle,
                )
            )
