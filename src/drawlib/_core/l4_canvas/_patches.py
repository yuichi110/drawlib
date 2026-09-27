# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Canvas's matplotlib base shape feature implementation module."""

import math

from matplotlib.patches import (
    Arc,
    Circle,
    Ellipse,
    RegularPolygon,
    Wedge,
)
from pydantic import validate_call

from drawlib._core.l2_types import (
    Angle,
    Coordinate,
    NumVertex,
    PosFloat,
    Size,
)
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas._base import CanvasBase
from drawlib._core.l4_canvas_utils import ShapeUtil, TextUtil


class CanvasPatchesFeature(CanvasBase):
    """A class for drawing various shapes using matplotlib patches on a canvas."""

    def __init__(self) -> None:
        """Initializes a CanvasPatchesFeature object."""
        super().__init__()

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
        effective_textstyle = textstyle if textstyle is not None else style
        if textsize is not None:
            effective_textstyle = effective_textstyle.patch(text_size=textsize)
        TextUtil.validate_text_style(effective_textstyle)
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
        effective_textstyle = textstyle if textstyle is not None else style
        if textsize is not None:
            effective_textstyle = effective_textstyle.patch(text_size=textsize)
        TextUtil.validate_text_style(effective_textstyle)
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
            xy: Center coordinates tuple (x, y).
            width: Width of the ellipse.
            height: Height of the ellipse.
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

        xy, style = ShapeUtil.apply_alignment(xy, width, height, angle, style, is_default_center=True)
        options = ShapeUtil.get_shape_options(style)
        self._artists.append(
            Ellipse(
                xy=xy,
                width=width,
                height=height,
                angle=angle,
                **options,
            ),
        )

        if not text:
            return
        effective_textstyle = textstyle if textstyle is not None else style
        if textsize is not None:
            effective_textstyle = effective_textstyle.patch(text_size=textsize)
        TextUtil.validate_text_style(effective_textstyle)
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
            xy: Center coordinates tuple (x, y).
            num_vertex: Number of vertices.
            radius: Radius of polygon.
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
            RegularPolygon(
                xy,
                numVertices=num_vertex,
                radius=radius,
                orientation=math.radians(angle),
                **options,
            )
        )

        if not text:
            return
        effective_textstyle = textstyle if textstyle is not None else style
        if textsize is not None:
            effective_textstyle = effective_textstyle.patch(text_size=textsize)
        TextUtil.validate_text_style(effective_textstyle)
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
        effective_textstyle = textstyle if textstyle is not None else style
        if textsize is not None:
            effective_textstyle = effective_textstyle.patch(text_size=textsize)
        TextUtil.validate_text_style(effective_textstyle)
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
