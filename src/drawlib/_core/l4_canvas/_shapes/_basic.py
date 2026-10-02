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
    NumVertex,
    PathPoints,
    PosFloat,
    Size,
)
from drawlib._core.l3_math import (
    get_center_and_size,
    minus_2points,
    rotate_point,
)
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas._base import CanvasBase
from drawlib._core.l4_canvas._shapes._util import ShapeUtil


class CanvasShapeBasicFeature(CanvasBase):
    """A feature class for drawing basic geometrical shapes and matplotlib patches on a canvas."""

    def __init__(self) -> None:
        """Initializes a CanvasShapeBasicFeature object."""
        super().__init__()

    @validate_call
    def shape(  # noqa: C901
        self,
        xy: Coordinate,
        path_points: PathPoints,
        *,
        style: Style,
        angle: Angle = 0.0,
        text: str = "",
        textsize: Size | None = None,
        textstyle: Style | None = None,
        is_default_center: bool = False,
    ) -> None:
        """Draw basic shape on the canvas.

        Args:
            xy: Starting point of the shape.
            path_points: List of path points including control points for Bezier curves.
            style: Style of the shape (required).
            angle (float, optional): Rotation angle of the shape.
            text (str, optional): Text to display along with the shape.
            textsize (float | None, optional): Size of the text.
            textstyle (Style | None, optional): Style of the text.
            is_default_center (bool, optional): Whether to place (xy) at the center of the shape.

        Raises:
            ValueError: If invalid path points are provided.
        """
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
        )

        # shift to center (0, 0)
        points_without_cp = []
        for pp in path_points:
            if not isinstance(pp[0], tuple):
                points_without_cp.append(pp)
            else:
                points_without_cp.append(pp[0])
            center, (width, height) = get_center_and_size(points_without_cp)

        path_points2 = []
        for pp in path_points:
            # (x, y)
            if not isinstance(pp[0], tuple):
                xy1 = minus_2points(pp, center)  # type: ignore
                path_points2.append(xy1)
                continue

            # ((x1, y1), (x2, y2))
            xy1 = minus_2points(pp[0], center)
            xy2 = minus_2points(pp[1], center)  # type: ignore
            if len(pp) == 2:
                path_points2.append((xy1, xy2))
                continue

            # ((x1, y1), (x2, y2), (x3, y3))
            xy3 = minus_2points(pp[2], center)  # type: ignore
            path_points2.append((xy1, xy2, xy3))

        # alignment
        if is_default_center:
            # move to center
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
            is_default_center=is_default_center,
        )

        # rotate and move
        cx = x + width / 2
        cy = y + height / 2
        path_points3 = []
        for pp in path_points2:
            # (x, y)
            if not isinstance(pp[0], tuple):
                rx, ry = rotate_point(pp, angle=angle)
                path_points3.append((rx + cx, ry + cy))
                continue

            # ((x1, y1), (x2, y2))
            rx1, ry1 = rotate_point(pp[0], angle=angle)
            rx2, ry2 = rotate_point(pp[1], angle=angle)
            if len(pp) == 2:
                path_points3.append(((rx1 + cx, ry1 + cy), (rx2 + cx, ry2 + cy)))
                continue

            # ((x1, y1), (x2, y2), (x3, y3))
            rx3, ry3 = rotate_point(pp[2], angle=angle)
            path_points3.append(
                (
                    (rx1 + cx, ry1 + cy),
                    (rx2 + cx, ry2 + cy),
                    (rx3 + cx, ry3 + cy),
                )
            )

        # create Path
        vertices = [path_points3[0]]
        codes = [Path.MOVETO]
        for p in path_points3[1:]:
            length = len(p)
            if length not in {2, 3}:
                raise ValueError()

            if not isinstance(p[0], tuple):
                vertices.append(p)
                codes.append(Path.LINETO)

            elif length == 2:
                vertices.extend([p[0], p[1]])
                codes.extend([Path.CURVE3] * 2)

            else:
                vertices.extend([p[0], p[1], p[2]])
                codes.extend([Path.CURVE4] * 3)

        vertices.append(path_points3[0])
        codes.append(Path.CLOSEPOLY)
        path = Path(vertices=vertices, codes=codes)

        # create PathPatch
        options = ShapeUtil.get_shape_options(style)
        self._artists.append(PathPatch(path=path, **options))

        # create Text
        if text:
            effective_textstyle = ShapeUtil.resolve_embedded_text_style(style, textstyle, textsize)
            self._artists.append(
                ShapeUtil.get_shape_text(
                    xy=(cx, cy),
                    text=text,
                    angle=angle,
                    style=effective_textstyle,
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
        angle: Angle = 0.0,
        text: str = "",
        textsize: Size | None = None,
        textstyle: Style | None = None,
    ) -> None:
        """Draw a rectangle on the canvas.

        Args:
            xy: Bottom-left corner of the rectangle.
            width: Width of the rectangle.
            height: Height of the rectangle.
            style: Style of the rectangle (required).
            r (float, optional): Radius for rounded corners (default is 0.0).
            angle (int | float, optional): Rotation angle of the rectangle.
            text (str, optional): Text to display within the rectangle.
            textsize (float | None, optional): Size of the text.
            textstyle (Style | None, optional): Style of the text.

        Raises:
            ValueError: If invalid path points are provided.
        """
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
        )

        if r == 0:
            p1 = (0, 0)
            p2 = (0, height)
            p3 = (width, height)
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
            angle=angle,
            style=style,
            text=text,
            textsize=textsize,
            textstyle=textstyle,
        )

    @validate_call
    def polygon(
        self,
        xys: Coordinates,
        *,
        style: Style,
        text: str = "",
        textsize: Size | None = None,
        textstyle: Style | None = None,
    ) -> None:
        """Draw a polygon on the canvas.

        Args:
            xys: List of vertices [(x1, y1), ...(x_n, y_n)].
            style: Style of the polygon (required).
            text (optional): Text shown at the center of the polygon.
            textsize (optional): Font size of the text.
            textstyle (optional): Style of the text.

        Returns:
            None
        """
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
        )

        style = style.patch(text_halign=None, text_valign=None)
        options = ShapeUtil.get_shape_options(style)
        self._artists.append(Polygon(xy=xys, closed=True, **options))

        if not text:
            return
        effective_textstyle = ShapeUtil.resolve_embedded_text_style(style, textstyle, textsize)
        center, (_, _) = get_center_and_size(xys)
        self._artists.append(
            ShapeUtil.get_shape_text(
                center,
                text=text,
                angle=0,
                style=effective_textstyle,
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
        angle: Angle = 0.0,
        text: str = "",
        textsize: Size | None = None,
        textstyle: Style | None = None,
    ) -> None:
        """Draw an arc on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            width: Width of arc.
            height: Height of arc.
            style: Style object (required).
            angle_start: Starting angle in degrees.
            angle_end: Ending angle in degrees.
            angle: Rotation angle in degrees.
            text: Text to display inside shape.
            textsize: Font size of text.
            textstyle: Style object for text.
        """
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
        )

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
        effective_textstyle = ShapeUtil.resolve_embedded_text_style(style, textstyle, textsize)
        self._artists.append(
            ShapeUtil.get_shape_text(
                xy=xy,
                text=text,
                angle=angle,
                style=effective_textstyle,
            ),
        )

    @validate_call
    def circle(
        self,
        xy: Coordinate,
        radius: PosFloat,
        *,
        style: Style,
        angle: Angle = 0.0,
        text: str = "",
        textsize: Size | None = None,
        textstyle: Style | None = None,
    ) -> None:
        """Draw a circle on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            radius: Radius of the circle.
            style: Style object (required).
            angle: Rotation angle in degrees.
            text: Text to display inside shape.
            textsize: Font size of text.
            textstyle: Style object for text.
        """
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
        )

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
        effective_textstyle = ShapeUtil.resolve_embedded_text_style(style, textstyle, textsize)
        self._artists.append(
            ShapeUtil.get_shape_text(
                xy=xy,
                text=text,
                angle=angle,
                style=effective_textstyle,
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
        angle: Angle = 0.0,
        text: str = "",
        textsize: Size | None = None,
        textstyle: Style | None = None,
    ) -> None:
        """Draw an ellipse on the canvas.

        Args:
            xy: Center coordinates (x, y) of the ellipse.
            width: Width (major axis) of the ellipse.
            height: Height (minor axis) of the ellipse.
            angle (optional): Rotation angle of the ellipse in degrees.
            style: Style of the ellipse (required).
            text (optional): Text to display inside the ellipse.
            textsize (optional): Font size of the text.
            textstyle (optional): Style of the text.
        """
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
        )

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
        effective_textstyle = ShapeUtil.resolve_embedded_text_style(style, textstyle, textsize)
        self._artists.append(
            ShapeUtil.get_shape_text(
                xy=xy,
                text=text,
                angle=angle,
                style=effective_textstyle,
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
        angle: Angle = 0.0,
        text: str = "",
        textsize: Size | None = None,
        textstyle: Style | None = None,
    ) -> None:
        """Draw a regular polygon on the canvas.

        Args:
            xy: Center coordinates (x, y) of the regular polygon.
            num_vertex: Number of vertices in the polygon.
            radius: Radius of the circumscribed circle.
            angle (optional): Rotation angle of the polygon in degrees.
            style: Style of the polygon (required).
            text (optional): Text to display inside the polygon.
            textsize (optional): Font size of the text.
            textstyle (optional): Style of the text.
        """
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
        )

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
        effective_textstyle = ShapeUtil.resolve_embedded_text_style(style, textstyle, textsize)
        self._artists.append(
            ShapeUtil.get_shape_text(
                xy=xy,
                text=text,
                angle=angle,
                style=effective_textstyle,
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
        angle: Angle = 0.0,
        text: str = "",
        textsize: Size | None = None,
        textstyle: Style | None = None,
    ) -> None:
        """Draw a wedge shape on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            radius: Outer radius of the wedge.
            style: Style object (required).
            width: Width of the wedge ring (inner radius = radius - width).
            angle_start: Starting theta angle in degrees.
            angle_end: Ending theta angle in degrees.
            angle: Rotation angle in degrees.
            text: Text to display inside shape.
            textsize: Font size of text.
            textstyle: Style object for text.
        """
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
        )

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
        effective_textstyle = ShapeUtil.resolve_embedded_text_style(style, textstyle, textsize)
        self._artists.append(
            ShapeUtil.get_shape_text(
                xy=xy,
                text=text,
                angle=angle,
                style=effective_textstyle,
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
        angle: Angle = 0.0,
        text: str = "",
        textsize: Size | None = None,
        textstyle: Style | None = None,
    ) -> None:
        """Draw a donut shape on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            radius: Outer radius of the donut.
            style: Style object (required).
            width: Width of the donut ring.
            angle: Rotation angle in degrees.
            text: Text to display inside shape.
            textsize: Font size of text.
            textstyle: Style object for text.
        """
        self.wedge(
            xy=xy,
            radius=radius,
            width=width,
            angle=angle,
            style=style,
            text=text,
            textsize=textsize,
            textstyle=textstyle,
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
        angle: Angle = 0.0,
        text: str = "",
        textsize: Size | None = None,
        textstyle: Style | None = None,
    ) -> None:
        """Draw a fan shape on the canvas.

        Args:
            xy: Center coordinates tuple (x, y).
            radius: Radius of the fan.
            style: Style object (required).
            angle_start: Starting theta angle in degrees.
            angle_end: Ending theta angle in degrees.
            angle: Rotation angle in degrees.
            text: Text to display inside shape.
            textsize: Font size of text.
            textstyle: Style object for text.
        """
        self.wedge(
            xy=xy,
            radius=radius,
            width=None,
            angle_start=angle_start,
            angle_end=angle_end,
            angle=angle,
            style=style,
            text=text,
            textsize=textsize,
            textstyle=textstyle,
        )


__all__ = ["CanvasShapeBasicFeature"]
