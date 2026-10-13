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

import math
from typing import Any, cast

from matplotlib.patches import PathPatch
from matplotlib.path import Path
from matplotlib.text import Text

from drawlib._core.l2_types import (
    Angle,
    Bezier2,
    Bezier3,
    Coordinate,
    PathPoint,
    PathPoints,
    ShapeRadius,
    Size,
)
from drawlib._core.l3_colors import ColorUtil
from drawlib._core.l3_fonts import Font
from drawlib._core.l3_math import (
    get_center_and_size,
    minus_2points,
    rotate_point,
)
from drawlib._core.l3_styles import Style
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
            TextUtil.validate_text_style(text_style)
            return text_style

        # Automatic contrast resolution
        fill_color = shape_style.shape_fill_color
        fill_alpha = shape_style.alpha
        text_col = ColorUtil.get_contrast_text_color(
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
                b3 = p
                vertices.extend([b3[0], b3[1], b3[2]])
                codes.extend([Path.CURVE4, Path.CURVE4, Path.CURVE4])
            else:
                raise ValueError(f"Invalid path point length: {len(p)}. Must be 2 or 3.")

        vertices.append(start_coord)
        codes.append(Path.CLOSEPOLY)
        return Path(vertices=vertices, codes=codes)

    @staticmethod
    def _normalize_shape_radii(
        n: int,
        shape_r: ShapeRadius | None,
    ) -> list[float] | None:
        """Normalize scalar or tuple shape_r into a per-vertex radius list, or None if unrounded."""
        if shape_r is None:
            return None
        if isinstance(shape_r, (int, float)):
            r_val = float(shape_r)
            if r_val < 0.0:
                raise ValueError("shape_r must be non-negative.")
            if r_val == 0.0:
                return None
            return [r_val] * n

        if len(shape_r) != n:
            raise ValueError(f"shape_r tuple length ({len(shape_r)}) must match the number of vertices ({n}).")
        radii = [float(r) for r in shape_r]
        if any(r < 0.0 for r in radii):
            raise ValueError("shape_r values must be non-negative.")
        if all(r == 0.0 for r in radii):
            return None
        return radii

    @staticmethod
    def round_polygon_points(
        vertices: list[Coordinate],
        shape_r: ShapeRadius | None,
    ) -> PathPoints:
        """Convert polygon vertices into PathPoints with optional per-vertex corner rounding.

        Args:
            vertices: Ordered list of polygon vertices.
            shape_r: Single corner radius or tuple of per-vertex corner radii.

        Returns:
            PathPoints: Path points with quadratic Bezier curves at rounded corners.

        Raises:
            ValueError: If shape_r is a tuple whose length does not match len(vertices).
        """
        n = len(vertices)
        radii = ShapeUtil._normalize_shape_radii(n, shape_r)
        if radii is None:
            return list(vertices)

        p_in: list[Coordinate] = []
        p_out: list[Coordinate] = []
        is_rounded: list[bool] = []

        for i in range(n):
            v_prev = vertices[(i - 1) % n]
            v_curr = vertices[i]
            v_next = vertices[(i + 1) % n]
            r_curr = radii[i]
            r_prev = radii[(i - 1) % n]
            r_next = radii[(i + 1) % n]

            dx_in = v_prev[0] - v_curr[0]
            dy_in = v_prev[1] - v_curr[1]
            d_in = math.hypot(dx_in, dy_in)

            dx_out = v_next[0] - v_curr[0]
            dy_out = v_next[1] - v_curr[1]
            d_out = math.hypot(dx_out, dy_out)

            if r_curr <= 0.0 or d_in == 0.0 or d_out == 0.0:
                p_in.append(v_curr)
                p_out.append(v_curr)
                is_rounded.append(False)
            else:
                avail_in = d_in * (r_curr / (r_prev + r_curr)) if (r_prev + r_curr) > d_in else r_curr
                avail_out = d_out * (r_curr / (r_curr + r_next)) if (r_curr + r_next) > d_out else r_curr
                r_eff = min(r_curr, avail_in, avail_out)
                p_in.append((v_curr[0] + (dx_in / d_in) * r_eff, v_curr[1] + (dy_in / d_in) * r_eff))
                p_out.append((v_curr[0] + (dx_out / d_out) * r_eff, v_curr[1] + (dy_out / d_out) * r_eff))
                is_rounded.append(True)

        start_pt: Coordinate = (
            (p_out[-1][0] + p_in[0][0]) / 2.0,
            (p_out[-1][1] + p_in[0][1]) / 2.0,
        )
        path_points: PathPoints = [start_pt]
        for i in range(n):
            if is_rounded[i]:
                path_points.append(p_in[i])
                path_points.append((vertices[i], p_out[i]))
            else:
                path_points.append(vertices[i])

        return path_points

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
            b3 = p
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
            b3 = p
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
        transformed_points = [ShapeUtil._rotate_and_place_path_point(p, angle, center_xy) for p in centered_points]

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

        x, y = xy
        if style.xy_shift is not None:
            x_shift, y_shift = style.xy_shift
            if shape_angle == 0:
                x += x_shift
                y += y_shift
            else:
                rx_shift, ry_shift = rotate_point((x_shift, y_shift), angle=shape_angle)
                x += rx_shift
                y += ry_shift

        if style.xy_abs_shift is not None:
            x += style.xy_abs_shift[0]
            y += style.xy_abs_shift[1]

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
            "alpha": style.alpha,
        }

        return {k: v for k, v in options.items() if v is not None}

    @staticmethod
    def validate_hole_ratio(hole_ratio: float | None) -> float | None:
        """Validate that hole_ratio is strictly in (0.0, 1.0) when provided."""
        if hole_ratio is None:
            return None
        val = float(hole_ratio)
        if not (0.0 < val < 1.0):
            raise ValueError("hole_ratio must be strictly between 0.0 and 1.0.")
        return val

    @staticmethod
    def build_ellipse_path(
        cx: float,
        cy: float,
        rx: float,
        ry: float,
        angle: float = 0.0,
        *,
        cw: bool = False,
    ) -> Path:
        """Build a closed 4-segment cubic Bezier Path for an ellipse or circle."""
        kappa = 0.5522847498307936
        kx = rx * kappa
        ky = ry * kappa

        if not cw:
            local_pts: list[Coordinate] = [
                (rx, 0.0),
                (rx, ky),
                (kx, ry),
                (0.0, ry),
                (-kx, ry),
                (-rx, ky),
                (-rx, 0.0),
                (-rx, -ky),
                (-kx, -ry),
                (0.0, -ry),
                (kx, -ry),
                (rx, -ky),
                (rx, 0.0),
            ]
        else:
            local_pts = [
                (rx, 0.0),
                (rx, -ky),
                (kx, -ry),
                (0.0, -ry),
                (-kx, -ry),
                (-rx, -ky),
                (-rx, 0.0),
                (-rx, ky),
                (-kx, ry),
                (0.0, ry),
                (kx, ry),
                (rx, ky),
                (rx, 0.0),
            ]

        world_pts: list[Coordinate] = []
        for pt in local_pts:
            rx_pt, ry_pt = rotate_point(pt, angle=angle)
            world_pts.append((cx + rx_pt, cy + ry_pt))
        world_pts.append(world_pts[0])

        codes = [
            Path.MOVETO,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CLOSEPOLY,
        ]
        return Path(vertices=world_pts, codes=codes)

    @staticmethod
    def build_hollow_ellipse_path(
        cx: float,
        cy: float,
        rx: float,
        ry: float,
        hole_ratio: float,
        angle: float = 0.0,
    ) -> Path:
        """Build a compound Path for an ellipse/circle with an inner hole cutout."""
        outer = ShapeUtil.build_ellipse_path(cx, cy, rx, ry, angle=angle, cw=False)
        inner = ShapeUtil.build_ellipse_path(
            cx,
            cy,
            rx * hole_ratio,
            ry * hole_ratio,
            angle=angle,
            cw=True,
        )
        return Path.make_compound_path(outer, inner)

    @staticmethod
    def inset_convex_polygon(
        vertices: list[Coordinate],
        hole_ratio: float,
    ) -> tuple[list[Coordinate], float]:
        """Compute reversed inner hole vertices for a convex polygon by parallel edge inset.

        Returns:
            tuple[list[Coordinate], float]: Reversed inner polygon vertices (opposite winding to input)
                and the applied perpendicular inset thickness.
        """
        n = len(vertices)
        if n == 3:
            # Triangle incenter gives exact equal distance to all 3 edges
            l0 = math.hypot(vertices[2][0] - vertices[1][0], vertices[2][1] - vertices[1][1])
            l1 = math.hypot(vertices[0][0] - vertices[2][0], vertices[0][1] - vertices[2][1])
            l2 = math.hypot(vertices[1][0] - vertices[0][0], vertices[1][1] - vertices[0][1])
            perim = l0 + l1 + l2
            cx = (l0 * vertices[0][0] + l1 * vertices[1][0] + l2 * vertices[2][0]) / perim
            cy = (l0 * vertices[0][1] + l1 * vertices[1][1] + l2 * vertices[2][1]) / perim
        else:
            cx = sum(v[0] for v in vertices) / n
            cy = sum(v[1] for v in vertices) / n

        tangents: list[Coordinate] = []
        normals: list[Coordinate] = []
        lengths: list[float] = []
        dists: list[float] = []

        for i in range(n):
            v0 = vertices[i]
            v1 = vertices[(i + 1) % n]
            dx = v1[0] - v0[0]
            dy = v1[1] - v0[1]
            length = math.hypot(dx, dy)
            ux, uy = dx / length, dy / length
            nx, ny = -uy, ux
            if nx * (cx - v0[0]) + ny * (cy - v0[1]) < 0.0:
                nx, ny = -nx, -ny
            dist = nx * (cx - v0[0]) + ny * (cy - v0[1])
            tangents.append((ux, uy))
            normals.append((nx, ny))
            lengths.append(length)
            dists.append(dist)

        deltas: list[Coordinate] = []
        for i in range(n):
            ux, uy = tangents[i]
            nx, ny = normals[i]
            px, py = normals[(i - 1) % n]
            denom = ux * px + uy * py
            if abs(denom) < 1e-9:
                deltas.append((nx, ny))
            else:
                s = (1.0 - (nx * px + ny * py)) / denom
                deltas.append((nx + s * ux, ny + s * uy))

        t_max = min(dists)
        for i in range(n):
            d0 = deltas[i]
            d1 = deltas[(i + 1) % n]
            ux, uy = tangents[i]
            shrink_rate = -((d1[0] - d0[0]) * ux + (d1[1] - d0[1]) * uy)
            if shrink_rate > 1e-9:
                t_max = min(t_max, lengths[i] / shrink_rate)

        inset = (1.0 - hole_ratio) * t_max
        inner_same_winding: list[Coordinate] = [
            (vertices[i][0] + inset * deltas[i][0], vertices[i][1] + inset * deltas[i][1]) for i in range(n)
        ]
        return list(reversed(inner_same_winding)), inset

    @staticmethod
    def shrink_shape_r(
        shape_r: ShapeRadius | None,
        inset: float,
        reversed_order: bool = True,
    ) -> ShapeRadius | None:
        """Reduce corner radius for an inset inner hole polygon."""
        if shape_r is None:
            return None
        if isinstance(shape_r, (int, float)):
            r_in = max(0.0, float(shape_r) - inset * 0.5)
            return r_in if r_in > 0.0 else None
        radii = [max(0.0, float(r) - inset * 0.5) for r in shape_r]
        if reversed_order:
            radii = list(reversed(radii))
        return tuple(radii) if any(r > 0.0 for r in radii) else None

    @staticmethod
    def prepare_centered_shape(
        xy: Coordinate,
        width: float,
        height: float,
        style: Style,
    ) -> tuple[Coordinate, Angle, Style]:
        """Resolve center coordinate (cx, cy), angle, and post-alignment style for a centered shape."""
        angle: Angle = style.angle if style.angle is not None else 0.0
        xy_aligned, style = ShapeUtil.apply_alignment(
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
        options = ShapeUtil.get_shape_options(style)
        artists.append(PathPatch(path=path, **options))
        if text:
            effective_text_style = ShapeUtil.resolve_embedded_text_style(style, text_style)
            artists.append(
                ShapeUtil.get_shape_text(
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
            effective_text_style = ShapeUtil.resolve_embedded_text_style(style, text_style)
            artists.append(
                ShapeUtil.get_shape_text(
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
        style, text_style = ShapeUtil.format_styles(
            style,
            text_style,
        )
        angle: Angle = style.angle if style.angle is not None else 0.0

        transformed_points, (cx, cy), effective_style = ShapeUtil.transform_shape_path_points(
            xy=xy,
            path_points=path_points,
            angle=angle,
            style=style,
            is_default_center=is_default_center,
        )

        path = ShapeUtil.build_matplotlib_path(transformed_points)
        ShapeUtil.append_path_and_text(
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
            path_points = ShapeUtil.round_polygon_points(vertices, style.shape_r)
            ShapeUtil.draw_shape_path_points(
                artists=artists,
                xy=xy,
                path_points=path_points,
                style=style,
                text=text,
                text_style=text_style,
                is_default_center=is_default_center,
            )
            return

        style, text_style = ShapeUtil.format_styles(style, text_style)
        h_ratio = float(ShapeUtil.validate_hole_ratio(hole_ratio) or 0.5)
        angle: Angle = style.angle if style.angle is not None else 0.0

        inner_local_verts, inset = ShapeUtil.inset_convex_polygon(vertices, h_ratio)
        outer_points = ShapeUtil.round_polygon_points(vertices, style.shape_r)
        inner_shape_r = ShapeUtil.shrink_shape_r(style.shape_r, inset, reversed_order=True)
        inner_points = ShapeUtil.round_polygon_points(inner_local_verts, inner_shape_r)

        orig_center, (width, height) = get_center_and_size(vertices)
        centered_outer = [ShapeUtil._shift_path_point(p, orig_center) for p in outer_points]
        centered_inner = [ShapeUtil._shift_path_point(p, orig_center) for p in inner_points]

        align_xy = (xy[0] - width / 2.0, xy[1] - height / 2.0) if is_default_center else xy
        (adj_x, adj_y), effective_style = ShapeUtil.apply_alignment(
            align_xy,
            width=width,
            height=height,
            angle=angle,
            style=style,
            is_default_center=is_default_center,
        )
        center_xy = (adj_x + width / 2.0, adj_y + height / 2.0)

        transformed_outer = [ShapeUtil._rotate_and_place_path_point(p, angle, center_xy) for p in centered_outer]
        transformed_inner = [ShapeUtil._rotate_and_place_path_point(p, angle, center_xy) for p in centered_inner]

        outer_path = ShapeUtil.build_matplotlib_path(transformed_outer)
        inner_path = ShapeUtil.build_matplotlib_path(transformed_inner)
        compound_path = Path.make_compound_path(outer_path, inner_path)

        ShapeUtil.append_path_and_text(
            artists=artists,
            path=compound_path,
            style=effective_style,
            text=text,
            text_style=text_style,
            text_xy=center_xy,
            angle=angle,
        )

    @staticmethod
    def lighten_rgba(
        rgba: tuple[float, float, float, float],
        factor: float,
    ) -> tuple[float, float, float, float]:
        """Lighten an RGBA color tuple toward white by factor in [0.0, 1.0]."""
        r, g, b, a = rgba
        return (
            min(1.0, r + (1.0 - r) * factor),
            min(1.0, g + (1.0 - g) * factor),
            min(1.0, b + (1.0 - b) * factor),
            a,
        )

    @staticmethod
    def darken_rgba(
        rgba: tuple[float, float, float, float],
        factor: float,
    ) -> tuple[float, float, float, float]:
        """Darken an RGBA color tuple toward black by factor in [0.0, 1.0]."""
        r, g, b, a = rgba
        scale = 1.0 - factor
        return (
            max(0.0, r * scale),
            max(0.0, g * scale),
            max(0.0, b * scale),
            a,
        )

    @staticmethod
    def resolve_feature_colors(
        style: Style,
    ) -> tuple[
        tuple[float, float, float, float] | str,
        tuple[float, float, float, float] | str,
        tuple[float, float, float, float],
        float,
    ]:
        """Derive face fill, outline stroke, and inner feature color/width from Style."""
        line_w = style.shape_line_width if style.shape_line_width is not None else 0.0
        raw_stroke = (
            ColorUtil.get_mplot_rgba(style.shape_line_color)
            if style.shape_line_color is not None
            else (0.0, 0.0, 0.0, 0.0)
        )
        has_stroke = style.shape_line_color is not None and line_w > 0 and raw_stroke[3] > 0.0

        if style.shape_fill_color is None:
            face_fill: tuple[float, float, float, float] | str = "none"
        else:
            raw_fill = ColorUtil.get_mplot_rgba(style.shape_fill_color, alpha=style.alpha)
            face_fill = "none" if raw_fill[3] <= 0.0 else raw_fill

        stroke_color: tuple[float, float, float, float] | str = raw_stroke if has_stroke else "none"

        if has_stroke:
            feature_color = raw_stroke
            feature_w = line_w
        elif style.text_color is not None:
            feature_color = ColorUtil.get_mplot_rgba(style.text_color)
            feature_w = 1.5
        else:
            contrast_col = ColorUtil.get_contrast_text_color(style.shape_fill_color, style.alpha)
            feature_color = ColorUtil.get_mplot_rgba(contrast_col)
            feature_w = 1.5

        if style.alpha is not None and 0.0 < style.alpha < 1.0:
            feature_color = (
                feature_color[0],
                feature_color[1],
                feature_color[2],
                round(feature_color[3] * style.alpha, 5),
            )
            if isinstance(stroke_color, tuple):
                stroke_color = (
                    stroke_color[0],
                    stroke_color[1],
                    stroke_color[2],
                    round(stroke_color[3] * style.alpha, 5),
                )

        return face_fill, stroke_color, feature_color, feature_w

    @staticmethod
    def arc_points_local(
        cx: float,
        cy: float,
        r: float,
        a_start_deg: float,
        a_end_deg: float,
        n: int = 36,
    ) -> list[Coordinate]:
        """Sample points along a circular arc from a_start_deg to a_end_deg."""
        pts: list[Coordinate] = []
        for i in range(n + 1):
            a = math.radians(a_start_deg + (a_end_deg - a_start_deg) * (i / n))
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        return pts

    @staticmethod
    def subpaths_to_compound_path(
        subpaths: list[list[Coordinate]],
        cx: float,
        cy: float,
        angle: float,
    ) -> Path:
        """Transform local polygon subpaths by (cx, cy, angle) and combine into a single Matplotlib Path."""
        rad = math.radians(angle)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)

        all_verts: list[Coordinate] = []
        all_codes: list[Any] = []
        for sp in subpaths:
            if not sp:
                continue
            xformed = [(cx + lx * cos_a - ly * sin_a, cy + lx * sin_a + ly * cos_a) for lx, ly in sp]
            all_verts.extend(xformed)
            all_verts.append(xformed[0])
            all_codes.append(Path.MOVETO)
            all_codes.extend([Path.LINETO] * (len(xformed) - 1))
            all_codes.append(Path.CLOSEPOLY)
        return Path(vertices=all_verts, codes=all_codes)


__all__ = ["ShapeUtil"]
