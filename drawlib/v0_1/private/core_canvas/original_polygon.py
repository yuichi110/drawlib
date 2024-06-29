# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.


"""Canvas's original shape feature implementation module."""

import math
from typing import Optional, Tuple, Union

from matplotlib.patches import PathPatch
from matplotlib.path import Path

import drawlib.v0_1.private.validators.args as validator
from drawlib.v0_1.private.core.model import ShapeStyle, ShapeTextStyle
from drawlib.v0_1.private.core.theme import dtheme
from drawlib.v0_1.private.core.util import ShapeUtil
from drawlib.v0_1.private.core_canvas.base import CanvasBase
from drawlib.v0_1.private.util import error_handler


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

    @error_handler
    def triangle(
        self,
        xy: Tuple[float, float],
        width: float,
        height: float,
        topvertex_x: Optional[float] = None,
        angle: Union[int, float] = 0.0,
        style: Union[ShapeStyle, str, None] = None,
        text: str = "",
        textsize: Optional[float] = None,
        textstyle: Union[ShapeTextStyle, str, None] = None,
    ) -> None:
        """Draw a triangle on the canvas.

        Args:
            xy: Bottom-left coordinates of the triangle.
            width: Width of the triangle's base.
            height: Height of the triangle.
            topvertex_x (optional): X-coordinate of the top vertex from the left side.
                                    Defaults to center if not provided.
            angle (optional): Rotation angle in degrees.
            style (optional): Style of the triangle.
            text (optional): Text to be placed at the center of the triangle.
            textsize (optional): Size of the text.
            textstyle (optional): Style of the text.

        Returns:
            None
        """
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
            dtheme.trianglestyles.get,
            dtheme.triangletextstyles.get,
        )
        validator.validate_shape_args(locals())

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

    @error_handler
    def parallelogram(
        self,
        xy: Tuple[float, float],
        width: float,
        height: float,
        corner_angle: Union[int, float],
        angle: Union[int, float] = 0.0,
        style: Union[ShapeStyle, str, None] = None,
        text: str = "",
        textsize: Optional[float] = None,
        textstyle: Union[ShapeTextStyle, str, None] = None,
    ) -> None:
        """Draw a parallelogram on the canvas.

        Args:
            xy: Bottom-left coordinates of the parallelogram.
            width: Width of the parallelogram's base.
            height: Height of the parallelogram.
            corner_angle: Angle of the left bottom corner in degrees.
            angle (optional): Rotation angle in degrees.
            style (optional): Style of the parallelogram.
            text (optional): Text to be placed at the center of the parallelogram.
            textsize (optional): Size of the text.
            textstyle (optional): Style of the text.

        Returns:
            None

        """
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
            dtheme.parallelogramstyles.get,
            dtheme.parallelogramtextstyles.get,
        )
        validator.validate_shape_args(locals())

        def calculate_parallelogram_lefttop_coordinate() -> Tuple[float, float]:
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

    @error_handler
    def trapezoid(
        self,
        xy: Tuple[float, float],
        height: float,
        bottomedge_width: float,
        topedge_width: float,
        topedge_x: Optional[float] = None,
        angle: float = 0.0,
        style: Union[ShapeStyle, str, None] = None,
        text: str = "",
        textsize: Optional[float] = None,
        textstyle: Union[ShapeTextStyle, str, None] = None,
    ) -> None:
        """Draw a trapezoid on the canvas.

        Args:
            xy: Bottom-left coordinates of the trapezoid.
            height: Height of the trapezoid.
            bottomedge_width: Width of the bottom edge of the trapezoid.
            topedge_width: Width of the top edge of the trapezoid.
            topedge_x (optional): X-coordinate of the start point of the top edge.
                                  Defaults to center if not provided.
            angle (optional): Rotation angle in degrees.
            style (optional): Style of the trapezoid.
            text (optional): Text to be placed at the center of the trapezoid.
            textsize (optional): Size of the text.
            textstyle (optional): Style of the text.

        Returns:
            None

        """
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
            dtheme.trapezoidstyles.get,
            dtheme.trapezoidtextstyles.get,
        )
        validator.validate_shape_args(locals())

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

    @error_handler
    def rhombus(
        self,
        xy: Tuple[float, float],
        width: float,
        height: float,
        angle: Union[int, float] = 0.0,
        style: Union[ShapeStyle, str, None] = None,
        text: str = "",
        textsize: Optional[float] = None,
        textstyle: Union[ShapeTextStyle, str, None] = None,
    ) -> None:
        """Draw a chevron on the canvas.

        Args:
            xy: Bottom-left coordinates of the chevron.
            width: Width of the bottom of the chevron.
            height: Height of the chevron.
            corner_angle: Angle of the left bottom corner in degrees (0.0 ~ 90.0).
            mirror (optional): If True, makes the vertex appear on the left side.
            angle (optional): Rotation angle in degrees.
            style (optional): Style of the chevron.
            text (optional): Text to be placed at the center of the chevron.
            textsize (optional): Size of the text.
            textstyle (optional): Style of the text.

        Returns:
            None
        """
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
            dtheme.rhombusstyles.get,
            dtheme.rhombustextstyles.get,
        )
        validator.validate_shape_args(locals())

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

    @error_handler
    def chevron(
        self,
        xy: Tuple[float, float],
        width: float,
        height: float,
        corner_angle: float,
        mirror: bool = False,
        angle: Union[int, float] = 0.0,
        style: Union[ShapeStyle, str, None] = None,
        text: str = "",
        textsize: Optional[float] = None,
        textstyle: Union[ShapeTextStyle, str, None] = None,
    ) -> None:
        """Draw chevron.

        Vertex is right on default. Provide True for mirror makes left side vertex.

        Args:
            xy: default left bottom.
            width: width of bottom of chevron
            height: height of chevron
            corner_angle: left bottom corner angle. 0.0 ~ 90.0.
            mirror(optional): make vertex left side.
            angle(optional): rotate degree
            style(optional): style of shape.
            text(optional): center text.
            textsize (optional): Size of the text.
            textstyle(optional): style of text.

        Returns:
            None
        """
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
            dtheme.chevronstyles.get,
            dtheme.chevrontextstyles.get,
        )
        validator.validate_shape_args(locals())

        def calculate_p2_coordinate(h: float) -> Tuple[float, float]:
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

    @error_handler
    def star(
        self,
        xy: Tuple[float, float],
        num_vertex: int,
        radius_ext: float,
        radius_int: float,
        angle: Union[int, float] = 0.0,
        style: Union[ShapeStyle, str, None] = None,
        text: str = "",
        textsize: Optional[float] = None,
        textstyle: Union[ShapeTextStyle, str, None] = None,
    ) -> None:
        """Draw a star on the canvas.

        Args:
            xy: Center coordinates of the star.
            num_vertex: Number of external vertices (3 or more).
            radius_ext: Radius of the external vertices.
            radius_int: Radius of the internal vertices.
            angle (optional): Rotation angle in degrees.
            style (optional): Style of the star.
            text (optional): Text to be placed at the center of the star.
            textsize (optional): Size of the text.
            textstyle (optional): Style of the text.

        Returns:
            None

        Raises:
            ValueError: If the external radius is smaller than the internal radius.
        """
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
            dtheme.starstyles.get,
            dtheme.startextstyles.get,
        )
        validator.validate_shape_args(locals())

        if textsize is not None:
            textstyle.size = textsize
        if radius_ext < radius_int:
            raise ValueError("radius_ext must be bigger than radius_int.")

        # helper

        def get_rotate_point(
            x: float,
            y: float,
            angle: Optional[float],
            move_x: float,
            move_y: float,
        ) -> Tuple[float, float]:
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

        if text is not None:
            self._artists.append(
                ShapeUtil.get_shape_text(
                    xy=(cx, cy),
                    text=text,
                    angle=angle,
                    style=textstyle,
                )
            )
