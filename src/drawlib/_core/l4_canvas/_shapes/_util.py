# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Shape utility module for canvas operations."""

from typing import Any, cast

from matplotlib.path import Path
from matplotlib.text import Text

from drawlib._core.l2_types import (
    Angle,
    Bezier2,
    Bezier3,
    Coordinate,
    PathPoint,
    PathPoints,
    Size,
)
from drawlib._core.l3_fonts import Font
from drawlib._core.l3_math import (
    get_center_and_size,
    minus_2points,
    rotate_point,
)
from drawlib._core.l3_styles import ColorUtil, Style
from drawlib._core.l4_canvas._text_util import TextUtil


class ShapeUtil:
    """A utility class for handling shape styles and options."""

    def __init__(self) -> None:
        """Raise TypeError to prevent instantiation of utility class."""
        raise TypeError(f"'{self.__class__.__name__}' is a static utility class and cannot be instantiated.")

    @staticmethod
    def validate_shape_style(style: Style) -> None:
        """Validate that the Style supports shape drawing."""
        style.validate_for("shape")

    @staticmethod
    def resolve_embedded_text_style(
        shape_style: Style,
        textstyle: Style | None = None,
        textsize: Size | None = None,
    ) -> Style:
        """Resolve effective text style for embedded text in shapes with automatic contrast.

        Args:
            shape_style: The container shape's Style instance.
            textstyle: Optional explicit textstyle provided by the caller.
            textsize: Optional font size override.

        Returns:
            Style: Validated, complete text style for drawing embedded text.
        """
        if textstyle is not None:
            if not isinstance(textstyle, Style):
                raise TypeError(f'Arg "textstyle" must be Style, but {type(textstyle)} given.')
            effective = textstyle
            if textsize is not None:
                effective = effective.patch(text_size=textsize)
            TextUtil.validate_text_style(effective)
            return effective

        # Automatic contrast resolution
        fill_color = shape_style.shape_fill_color
        fill_alpha = shape_style.shape_fill_alpha
        text_col = ColorUtil.get_contrast_text_color(
            fill_color,
            fill_alpha,
            transparent_color=shape_style.shape_line_color,
        )

        size = (
            textsize
            if textsize is not None
            else (shape_style.text_size if shape_style.text_size is not None else 16)
        )
        font = shape_style.text_font if shape_style.text_font is not None else Font.SANSSERIF_REGULAR
        halign = shape_style.text_halign if shape_style.text_halign is not None else "center"
        valign = shape_style.text_valign if shape_style.text_valign is not None else "center"

        return Style(
            supports={"text"},
            text_color=text_col,
            text_size=size,
            text_font=font,
            text_halign=halign,
            text_valign=valign,
        )

    @staticmethod
    def format_styles(
        style: Style,
        textstyle: Style | None = None,
    ) -> tuple[Style, Style | None]:
        """Validate and return shape style and optional embedded textstyle."""
        if not isinstance(style, Style):
            raise TypeError(f'Arg "style" must be Style, but {type(style)} given.')
        style.validate_for("shape")
        if textstyle is not None:
            if not isinstance(textstyle, Style):
                raise TypeError(f'Arg "textstyle" must be Style, but {type(textstyle)} given.')
            textstyle.validate_for("text")
        return (style, textstyle)

    @staticmethod
    def apply_alignment(
        xy: tuple[float, float],
        width: float,
        height: float,
        angle: float | None,
        style: Style,
        is_default_center: bool = False,
    ) -> tuple[tuple[float, float], Style]:
        """Apply alignment adjustments to coordinates based on Style alignment settings.

        Args:
            xy (tuple[float, float]): The x, y coordinates to be adjusted.
            width (float): The width of the shape.
            height (float): The height of the shape.
            angle (float | None): The angle of rotation for the shape.
            style (Style): The Style object containing alignment properties.
            is_default_center (bool, optional): Flag indicating default center alignment.

        Returns:
            tuple[tuple[float, float], Style]: Adjusted coordinates and updated Style object.
        """
        x, y = xy
        is_centered_mode = is_default_center or angle is not None
        default_halign = "center" if is_centered_mode else "left"
        default_valign = "center" if is_centered_mode else "bottom"

        text_halign = style.text_halign if style.text_halign is not None else default_halign
        text_valign = style.text_valign if style.text_valign is not None else default_valign

        if is_default_center:
            h_shifts = {"left": width / 2.0, "right": -width / 2.0}
            v_shifts = {"bottom": height / 2.0, "top": -height / 2.0}
        else:
            h_shifts = {"center": -width / 2.0, "right": -width}
            v_shifts = {"center": -height / 2.0, "top": -height}

        x += h_shifts.get(text_halign, 0.0)
        y += v_shifts.get(text_valign, 0.0)

        return (x, y), style.patch(text_halign=text_halign, text_valign=text_valign)

    @staticmethod
    def build_matplotlib_path(path_points: PathPoints) -> Path:
        """Construct a closed Matplotlib Path from transformed path points.

        Args:
            path_points: List of path points including straight lines and Bezier control points.

        Returns:
            Path: Closed Matplotlib Path object.

        Raises:
            ValueError: If path_points is empty or any item has invalid length.
        """
        if not path_points:
            raise ValueError("Path points cannot be empty.")

        # First point is always the initial MOVETO point
        first_pt = path_points[0]
        start_coord: Coordinate
        if isinstance(first_pt[0], (int, float)):
            start_coord = cast(Coordinate, first_pt)
        else:
            start_coord = cast(Bezier2 | Bezier3, first_pt)[0]

        vertices: list[Coordinate] = [start_coord]
        codes: list[Any] = [Path.MOVETO]

        for p in path_points[1:]:
            if isinstance(p[0], (int, float)):
                coord = cast(Coordinate, p)
                vertices.append(coord)
                codes.append(Path.LINETO)
            elif len(p) == 2:
                b2 = cast(Bezier2, p)
                vertices.extend([b2[0], b2[1]])
                codes.extend([Path.CURVE3, Path.CURVE3])
            elif len(p) == 3:
                b3 = cast(Bezier3, p)
                vertices.extend([b3[0], b3[1], b3[2]])
                codes.extend([Path.CURVE4, Path.CURVE4, Path.CURVE4])
            else:
                raise ValueError(f"Invalid path point length: {len(p)}. Must be 2 or 3.")

        vertices.append(start_coord)
        codes.append(Path.CLOSEPOLY)
        return Path(vertices=vertices, codes=codes)

    @staticmethod
    def _shift_path_point(p: PathPoint, offset: Coordinate) -> PathPoint:
        """Translate a single PathPoint by subtracting the given offset."""
        if isinstance(p[0], (int, float)):
            return minus_2points(cast(Coordinate, p), offset)
        if len(p) == 2:
            b2 = cast(Bezier2, p)
            return (
                minus_2points(b2[0], offset),
                minus_2points(b2[1], offset),
            )
        if len(p) == 3:
            b3 = cast(Bezier3, p)
            return (
                minus_2points(b3[0], offset),
                minus_2points(b3[1], offset),
                minus_2points(b3[2], offset),
            )
        raise ValueError(f"Invalid path point length: {len(p)}.")

    @staticmethod
    def _rotate_and_place_path_point(
        p: PathPoint,
        angle: Angle,
        center: Coordinate,
    ) -> PathPoint:
        """Rotate a single PathPoint around (0, 0) and translate to target center."""
        cx, cy = center
        if isinstance(p[0], (int, float)):
            coord = cast(Coordinate, p)
            rx, ry = rotate_point(coord, angle=angle)
            return (rx + cx, ry + cy)
        if len(p) == 2:
            b2 = cast(Bezier2, p)
            rx1, ry1 = rotate_point(b2[0], angle=angle)
            rx2, ry2 = rotate_point(b2[1], angle=angle)
            return ((rx1 + cx, ry1 + cy), (rx2 + cx, ry2 + cy))
        if len(p) == 3:
            b3 = cast(Bezier3, p)
            rx1, ry1 = rotate_point(b3[0], angle=angle)
            rx2, ry2 = rotate_point(b3[1], angle=angle)
            rx3, ry3 = rotate_point(b3[2], angle=angle)
            return (
                (rx1 + cx, ry1 + cy),
                (rx2 + cx, ry2 + cy),
                (rx3 + cx, ry3 + cy),
            )
        raise ValueError(f"Invalid path point length: {len(p)}.")

    @staticmethod
    def transform_shape_path_points(
        xy: Coordinate,
        path_points: PathPoints,
        angle: Angle,
        style: Style,
        is_default_center: bool = False,
    ) -> tuple[PathPoints, Coordinate, Style]:
        """Center, align, rotate, and translate path points to target canvas coordinates.

        Args:
            xy: Anchor coordinate for positioning the shape.
            path_points: Raw input path points.
            angle: Rotation angle in degrees.
            style: Shape style with alignment attributes.
            is_default_center: Whether xy is the shape center.

        Returns:
            tuple containing:
                - PathPoints: Transformed path points ready for Path construction.
                - Coordinate: Center point (cx, cy) of the shape.
                - Style: Updated Style object with effective alignments.
        """
        if not path_points:
            raise ValueError("Path points cannot be empty.")

        # 1. Determine bounding box and original center using anchor points
        anchor_points = [
            cast(Coordinate, p) if isinstance(p[0], (int, float)) else cast(Bezier2 | Bezier3, p)[0]
            for p in path_points
        ]
        orig_center, (width, height) = get_center_and_size(anchor_points)

        # 2. Shift points relative to center (0, 0)
        centered_points = [ShapeUtil._shift_path_point(p, orig_center) for p in path_points]

        # 3. Apply alignment
        align_xy = (xy[0] - width / 2.0, xy[1] - height / 2.0) if is_default_center else xy
        (adj_x, adj_y), effective_style = ShapeUtil.apply_alignment(
            align_xy,
            width=width,
            height=height,
            angle=angle,
            style=style,
            is_default_center=is_default_center,
        )

        # 4. Center coordinates for target placement
        center_xy = (adj_x + width / 2.0, adj_y + height / 2.0)

        # 5. Rotate and place at canvas center
        transformed_points = [
            ShapeUtil._rotate_and_place_path_point(p, angle, center_xy) for p in centered_points
        ]

        return transformed_points, center_xy, effective_style

    @staticmethod
    def get_shape_text(
        xy: tuple[float, float],
        angle: float | None,
        text: str,
        style: Style,
    ) -> Text:
        """Get text object drawn inside shape center."""
        shape_angle = angle if angle is not None else 0.0

        text_angle = style.text_angle if style.text_angle is not None else shape_angle
        if style.text_flip is not None and style.text_flip:
            text_angle = (text_angle + 180) % 360

        x, y = xy
        if style.text_xy_shift is not None:
            x_shift, y_shift = style.text_xy_shift
            if shape_angle == 0:
                x += x_shift
                y += y_shift
            else:
                rx_shift, ry_shift = rotate_point((x_shift, y_shift), angle=shape_angle)
                x += rx_shift
                y += ry_shift

        if style.text_xy_abs_shift is not None:
            x += style.text_xy_abs_shift[0]
            y += style.text_xy_abs_shift[1]

        options = TextUtil.get_text_options(style)
        if "horizontalalignment" in options:
            del options["horizontalalignment"]
        if "verticalalignment" in options:
            del options["verticalalignment"]

        return Text(
            x,
            y,
            text,
            rotation=text_angle,
            rotation_mode="anchor",
            horizontalalignment="center",
            verticalalignment="center",
            fontproperties=TextUtil.get_font_properties(style),
            **options,
        )

    @staticmethod
    def get_shape_options(
        style: Style,
    ) -> dict[str, Any]:
        """Convert drawlib's Style to matplotlib's patches(shape) options."""
        lcolor = None if style.shape_line_color is None else ColorUtil.get_mplot_rgba(style.shape_line_color)
        fcolor = None if style.shape_fill_color is None else ColorUtil.get_mplot_rgba(style.shape_fill_color)

        options: dict[str, Any] = {
            "facecolor": fcolor,
            "edgecolor": lcolor,
            "linestyle": style.shape_line_style if style.shape_line_style is not None else "solid",
            "linewidth": style.shape_line_width,
            "alpha": style.shape_fill_alpha,
        }

        return {k: v for k, v in options.items() if v is not None}


__all__ = ["ShapeUtil"]
