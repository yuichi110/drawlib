# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Shape utility module for canvas operations."""

from __future__ import annotations

from typing import Any, cast

from matplotlib.patches import PathPatch
from matplotlib.path import Path
from matplotlib.text import Text

from drawlib._core.l2_types import (
    Angle,
    Bezier2,
    Bezier3,
    Coordinate,
    PathPoints,
)
from drawlib._core.l3_colors import ColorUtils
from drawlib._core.l3_fonts import Font
from drawlib._core.l3_math import (
    get_center_and_size,
    rotate_point,
)
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas._shapes._path_utils import (
    _normalize_shape_radii,
    _rotate_and_place_path_point,
    _shift_path_point,
    arc_points_local,
    build_ellipse_path,
    build_hollow_ellipse_path,
    build_matplotlib_path,
    build_plaque_path,
    darken_rgba,
    inset_convex_polygon,
    lighten_rgba,
    resolve_feature_colors,
    round_polygon_points,
    shrink_shape_r,
    subpaths_to_compound_path,
    validate_hole_ratio,
)
from drawlib._core.l4_canvas._text_utils import TextUtils


class ShapeUtils:
    """A utility class for handling shape styles and options."""

    def __init__(self) -> None:
        """Raise TypeError to prevent instantiation of utility class."""
        raise TypeError(f"'{self.__class__.__name__}' is a static utility class and cannot be instantiated.")

    build_matplotlib_path = staticmethod(build_matplotlib_path)
    _normalize_shape_radii = staticmethod(_normalize_shape_radii)
    round_polygon_points = staticmethod(round_polygon_points)
    _shift_path_point = staticmethod(_shift_path_point)
    _rotate_and_place_path_point = staticmethod(_rotate_and_place_path_point)
    validate_hole_ratio = staticmethod(validate_hole_ratio)
    build_ellipse_path = staticmethod(build_ellipse_path)
    build_hollow_ellipse_path = staticmethod(build_hollow_ellipse_path)
    build_plaque_path = staticmethod(build_plaque_path)
    inset_convex_polygon = staticmethod(inset_convex_polygon)
    shrink_shape_r = staticmethod(shrink_shape_r)
    lighten_rgba = staticmethod(lighten_rgba)
    darken_rgba = staticmethod(darken_rgba)
    resolve_feature_colors = staticmethod(resolve_feature_colors)
    arc_points_local = staticmethod(arc_points_local)
    subpaths_to_compound_path = staticmethod(subpaths_to_compound_path)

    @staticmethod
    def validate_shape_style(style: Style) -> None:
        """Validate that the Style supports shape drawing."""
        style.validate_for("shape")

    @staticmethod
    def resolve_embedded_text_style(
        shape_style: Style,
        text_style: Style | None = None,
    ) -> Style:
        """Resolve effective text style for embedded text in shapes with automatic contrast.

        Args:
            shape_style: The container shape's Style instance.
            text_style: Optional explicit text_style provided by the caller.

        Returns:
            Style: Validated, complete text style for drawing embedded text.
        """
        if text_style is not None:
            if not isinstance(text_style, Style):
                raise TypeError(f'Arg "text_style" must be Style, but {type(text_style)} given.')
            TextUtils.validate_text_style(text_style)
            return text_style

        # Automatic contrast resolution
        fill_color = shape_style.shape_fill_color
        fill_alpha = shape_style.alpha
        text_col = ColorUtils.get_contrast_text_color(
            fill_color,
            fill_alpha,
            transparent_color=shape_style.shape_line_color,
        )

        size = shape_style.text_size if shape_style.text_size is not None else 16
        font = shape_style.text_font if shape_style.text_font is not None else Font.SANSSERIF_REGULAR
        halign = shape_style.halign if shape_style.halign is not None else "center"
        valign = shape_style.valign if shape_style.valign is not None else "center"

        return Style(
            supports={"text"},
            text_color=text_col,
            text_size=size,
            text_font=font,
            halign=halign,
            valign=valign,
            text_line_spacing=shape_style.text_line_spacing,
        )

    @staticmethod
    def format_styles(
        style: Style,
        text_style: Style | None = None,
    ) -> tuple[Style, Style | None]:
        """Validate and return shape style and optional embedded text_style."""
        if not isinstance(style, Style):
            raise TypeError(f'Arg "style" must be Style, but {type(style)} given.')
        style.validate_for("shape")
        if text_style is not None:
            if not isinstance(text_style, Style):
                raise TypeError(f'Arg "text_style" must be Style, but {type(text_style)} given.')
            text_style.validate_for("text")
        return (style, text_style)

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

        halign = style.halign if style.halign is not None else default_halign
        valign = style.valign if style.valign is not None else default_valign

        if is_default_center:
            h_shifts = {"left": width / 2.0, "right": -width / 2.0}
            v_shifts = {"bottom": height / 2.0, "top": -height / 2.0}
        else:
            h_shifts = {"center": -width / 2.0, "right": -width}
            v_shifts = {"center": -height / 2.0, "top": -height}

        x += h_shifts.get(halign, 0.0)
        y += v_shifts.get(valign, 0.0)

        return (x, y), style.patch(halign=halign, valign=valign)

    @staticmethod
    def apply_xy_shift(
        xy: Coordinate,
        angle: float,
        style: Style,
    ) -> Coordinate:
        """Apply rotated relative xy_shift and unrotated xy_abs_shift from Style."""
        x, y = xy
        if style.xy_shift is not None:
            x_shift, y_shift = style.xy_shift
            if angle == 0:
                x += x_shift
                y += y_shift
            else:
                rx_shift, ry_shift = rotate_point((x_shift, y_shift), angle=angle)
                x += rx_shift
                y += ry_shift

        if style.xy_abs_shift is not None:
            x += style.xy_abs_shift[0]
            y += style.xy_abs_shift[1]
        return (x, y)

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
        centered_points = [ShapeUtils._shift_path_point(p, orig_center) for p in path_points]

        # 3. Apply alignment
        align_xy = (xy[0] - width / 2.0, xy[1] - height / 2.0) if is_default_center else xy
        (adj_x, adj_y), effective_style = ShapeUtils.apply_alignment(
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
        transformed_points = [ShapeUtils._rotate_and_place_path_point(p, angle, center_xy) for p in centered_points]

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

        text_angle = style.angle if style.angle is not None else shape_angle
        if style.text_flip is not None and style.text_flip:
            text_angle = (text_angle + 180) % 360

        x, y = ShapeUtils.apply_xy_shift(xy, shape_angle, style)

        options = TextUtils.get_text_options(style)
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
            fontproperties=TextUtils.get_font_properties(style),
            **options,
        )

    @staticmethod
    def get_shape_options(
        style: Style,
    ) -> dict[str, Any]:
        """Convert drawlib's Style to matplotlib's patches(shape) options."""
        lcolor = None if style.shape_line_color is None else ColorUtils.get_mplot_rgba(style.shape_line_color)
        fcolor = None if style.shape_fill_color is None else ColorUtils.get_mplot_rgba(style.shape_fill_color)

        options: dict[str, Any] = {
            "facecolor": fcolor,
            "edgecolor": lcolor,
            "linestyle": style.shape_line_style if style.shape_line_style is not None else "solid",
            "linewidth": style.shape_line_width,
            "alpha": style.alpha,
        }

        return {k: v for k, v in options.items() if v is not None}

    @staticmethod
    def prepare_centered_shape(
        xy: Coordinate,
        width: float,
        height: float,
        style: Style,
    ) -> tuple[Coordinate, Angle, Style]:
        """Resolve center coordinate (cx, cy), angle, and post-alignment style for a centered shape."""
        angle: Angle = style.angle if style.angle is not None else 0.0
        xy_aligned, style = ShapeUtils.apply_alignment(
            xy=xy,
            width=width,
            height=height,
            angle=angle,
            style=style,
            is_default_center=True,
        )
        return xy_aligned, angle, style

    @staticmethod
    def append_path_and_text(
        artists: list[Any],
        path: Path,
        style: Style,
        text: str,
        text_style: Style | None,
        text_xy: Coordinate,
        angle: float,
    ) -> None:
        """Append a PathPatch and optional embedded text artist to the canvas artist list."""
        options = ShapeUtils.get_shape_options(style)
        artists.append(PathPatch(path=path, **options))
        if text:
            effective_text_style = ShapeUtils.resolve_embedded_text_style(style, text_style)
            artists.append(
                ShapeUtils.get_shape_text(
                    xy=text_xy,
                    text=text,
                    angle=angle,
                    style=effective_text_style,
                )
            )

    @staticmethod
    def append_patches_and_text(
        artists: list[Any],
        patches: list[Any],
        style: Style,
        text: str,
        text_style: Style | None,
        text_xy: Coordinate,
        angle: float,
    ) -> None:
        """Append multiple patch artists and optional embedded text artist to the canvas artist list."""
        artists.extend(patches)
        if text:
            effective_text_style = ShapeUtils.resolve_embedded_text_style(style, text_style)
            artists.append(
                ShapeUtils.get_shape_text(
                    xy=text_xy,
                    text=text,
                    angle=angle,
                    style=effective_text_style,
                )
            )

    @staticmethod
    def draw_shape_path_points(
        artists: list[Any],
        xy: Coordinate,
        path_points: PathPoints,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
        is_default_center: bool = False,
    ) -> None:
        """Draw a custom path shape defined by local PathPoints with alignment and optional text."""
        style, text_style = ShapeUtils.format_styles(
            style,
            text_style,
        )
        angle: Angle = style.angle if style.angle is not None else 0.0

        transformed_points, (cx, cy), effective_style = ShapeUtils.transform_shape_path_points(
            xy=xy,
            path_points=path_points,
            angle=angle,
            style=style,
            is_default_center=is_default_center,
        )

        path = ShapeUtils.build_matplotlib_path(transformed_points)
        ShapeUtils.append_path_and_text(
            artists=artists,
            path=path,
            style=effective_style,
            text=text,
            text_style=text_style,
            text_xy=(cx, cy),
            angle=angle,
        )

    @staticmethod
    def draw_convex_polygon_with_hole(
        artists: list[Any],
        xy: Coordinate,
        vertices: list[Coordinate],
        hole_ratio: float | None,
        style: Style,
        text: str = "",
        text_style: Style | None = None,
        is_default_center: bool = False,
    ) -> None:
        """Draw a convex polygon with optional inner hole_ratio cutout and corner rounding."""
        if hole_ratio is None:
            path_points = ShapeUtils.round_polygon_points(vertices, style.shape_r)
            ShapeUtils.draw_shape_path_points(
                artists=artists,
                xy=xy,
                path_points=path_points,
                style=style,
                text=text,
                text_style=text_style,
                is_default_center=is_default_center,
            )
            return

        style, text_style = ShapeUtils.format_styles(style, text_style)
        h_ratio = float(ShapeUtils.validate_hole_ratio(hole_ratio) or 0.5)
        angle: Angle = style.angle if style.angle is not None else 0.0

        inner_local_verts, inset = ShapeUtils.inset_convex_polygon(vertices, h_ratio)
        outer_points = ShapeUtils.round_polygon_points(vertices, style.shape_r)
        inner_shape_r = ShapeUtils.shrink_shape_r(style.shape_r, inset, reversed_order=True)
        inner_points = ShapeUtils.round_polygon_points(inner_local_verts, inner_shape_r)

        orig_center, (width, height) = get_center_and_size(vertices)
        centered_outer = [ShapeUtils._shift_path_point(p, orig_center) for p in outer_points]
        centered_inner = [ShapeUtils._shift_path_point(p, orig_center) for p in inner_points]

        align_xy = (xy[0] - width / 2.0, xy[1] - height / 2.0) if is_default_center else xy
        (adj_x, adj_y), effective_style = ShapeUtils.apply_alignment(
            align_xy,
            width=width,
            height=height,
            angle=angle,
            style=style,
            is_default_center=is_default_center,
        )
        center_xy = (adj_x + width / 2.0, adj_y + height / 2.0)

        transformed_outer = [ShapeUtils._rotate_and_place_path_point(p, angle, center_xy) for p in centered_outer]
        transformed_inner = [ShapeUtils._rotate_and_place_path_point(p, angle, center_xy) for p in centered_inner]

        outer_path = ShapeUtils.build_matplotlib_path(transformed_outer)
        inner_path = ShapeUtils.build_matplotlib_path(transformed_inner)
        compound_path = Path.make_compound_path(outer_path, inner_path)

        ShapeUtils.append_path_and_text(
            artists=artists,
            path=compound_path,
            style=effective_style,
            text=text,
            text_style=text_style,
            text_xy=center_xy,
            angle=angle,
        )


__all__ = ["ShapeUtils"]
