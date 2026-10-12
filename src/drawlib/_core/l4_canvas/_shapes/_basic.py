# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Canvas basic geometric and radial shape feature implementation module."""

from matplotlib.patches import Arc, Circle, Ellipse, PathPatch, Wedge
from pydantic import validate_call

from drawlib._core.l2_types import (
    Angle,
    Coordinate,
    PosFloat,
    Ratio,
)
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas._base import CanvasBase
from drawlib._core.l4_canvas._shapes._util import ShapeUtil


class CanvasShapeBasicFeature(CanvasBase):
    """A feature class for drawing basic geometrical and radial shapes on a canvas."""

    def __init__(self) -> None:
        """Initializes a CanvasShapeBasicFeature object."""
        super().__init__()

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

        p1 = (0.0, 0.0)
        p2 = (0.0, height)
        p3 = (width, height)
        p4 = (width, 0.0)
        ShapeUtil.draw_convex_polygon_with_hole(
            artists=self._artists,
            xy=xy,
            vertices=[p1, p2, p3, p4],
            hole_ratio=hole_ratio,
            style=style,
            text=text,
            text_style=text_style,
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
        width = radius * 2
        height = radius * 2
        xy, angle, style = ShapeUtil.prepare_centered_shape(xy, width, height, style)
        options = ShapeUtil.get_shape_options(style)
        if h_ratio is None:
            patch: Circle | PathPatch = Circle(
                xy=xy,
                radius=radius,
                **options,
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
            patch = PathPatch(path=path, **options)

        ShapeUtil.append_patches_and_text(
            artists=self._artists,
            patches=[patch],
            style=style,
            text=text,
            text_style=text_style,
            text_xy=xy,
            angle=angle,
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
        xy, angle, style = ShapeUtil.prepare_centered_shape(xy, width, height, style)

        options = ShapeUtil.get_shape_options(style)
        if h_ratio is None:
            patch: Ellipse | PathPatch = Ellipse(
                xy,
                width=width,
                height=height,
                angle=angle,
                **options,
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
            patch = PathPatch(path=path, **options)

        ShapeUtil.append_patches_and_text(
            artists=self._artists,
            patches=[patch],
            style=style,
            text=text,
            text_style=text_style,
            text_xy=xy,
            angle=angle,
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
        ext_width = radius * 2
        ext_height = radius * 2
        xy, angle, style = ShapeUtil.prepare_centered_shape(xy, ext_width, ext_height, style)
        options = ShapeUtil.get_shape_options(style)
        patch = Wedge(
            center=xy,
            r=radius,
            width=width,
            theta1=angle_start + angle,
            theta2=angle_end + angle,
            **options,
        )
        ShapeUtil.append_patches_and_text(
            artists=self._artists,
            patches=[patch],
            style=style,
            text=text,
            text_style=text_style,
            text_xy=xy,
            angle=angle,
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
        xy, angle, style = ShapeUtil.prepare_centered_shape(xy, width, height, style)
        options = ShapeUtil.get_shape_options(style)
        patch = Arc(
            xy,
            width=width,
            height=height,
            angle=angle,
            theta1=angle_start,
            theta2=angle_end,
            **options,
        )
        ShapeUtil.append_patches_and_text(
            artists=self._artists,
            patches=[patch],
            style=style,
            text=text,
            text_style=text_style,
            text_xy=xy,
            angle=angle,
        )


__all__ = [
    "CanvasShapeBasicFeature",
]
