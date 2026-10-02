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
from drawlib._core.l3_math import get_center_and_size
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas._base import CanvasBase
from drawlib._core.l4_canvas._shapes._util import ShapeUtil


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
            effective_textstyle = ShapeUtil.resolve_embedded_text_style(effective_style, textstyle, textsize)
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
