# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Pure path geometry, polygon rounding, hole inset, and color shading helpers for canvas shapes."""

from __future__ import annotations

import math
from typing import Any

from matplotlib.path import Path

from drawlib._core.l2_types import (
    Angle,
    Bezier2,
    Bezier3,
    Coordinate,
    PathPoint,
    PathPoints,
    ShapeRadius,
)
from drawlib._core.l3_colors import ColorUtils
from drawlib._core.l3_math import (
    minus_2points,
    rotate_point,
)
from drawlib._core.l3_styles import Style


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
        start_coord = first_pt
    else:
        start_coord = first_pt[0]

    vertices: list[Coordinate] = [start_coord]
    codes: list[Any] = [Path.MOVETO]

    for p in path_points[1:]:
        if isinstance(p[0], (int, float)):
            coord = p
            vertices.append(coord)
            codes.append(Path.LINETO)
        elif len(p) == 2:
            b2 = p
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
    radii = _normalize_shape_radii(n, shape_r)
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


def _shift_path_point(p: PathPoint, offset: Coordinate) -> PathPoint:
    """Translate a single PathPoint by subtracting the given offset."""
    if isinstance(p[0], (int, float)):
        return minus_2points(p, offset)
    if len(p) == 2:
        b2 = p
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


def _rotate_and_place_path_point(
    p: PathPoint,
    angle: Angle,
    center: Coordinate,
) -> PathPoint:
    """Rotate a single PathPoint around (0, 0) and translate to target center."""
    cx, cy = center
    if isinstance(p[0], (int, float)):
        coord = p
        rx, ry = rotate_point(coord, angle=angle)
        return (rx + cx, ry + cy)
    if len(p) == 2:
        b2 = p
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


def validate_hole_ratio(hole_ratio: float | None) -> float | None:
    """Validate that hole_ratio is strictly in (0.0, 1.0) when provided."""
    if hole_ratio is None:
        return None
    val = float(hole_ratio)
    if not (0.0 < val < 1.0):
        raise ValueError("hole_ratio must be strictly between 0.0 and 1.0.")
    return val


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


def build_hollow_ellipse_path(
    cx: float,
    cy: float,
    rx: float,
    ry: float,
    hole_ratio: float,
    angle: float = 0.0,
) -> Path:
    """Build a compound Path for an ellipse/circle with an inner hole cutout."""
    outer = build_ellipse_path(cx, cy, rx, ry, angle=angle, cw=False)
    inner = build_ellipse_path(
        cx,
        cy,
        rx * hole_ratio,
        ry * hole_ratio,
        angle=angle,
        cw=True,
    )
    return Path.make_compound_path(outer, inner)


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
        ColorUtils.get_mplot_rgba(style.shape_line_color)
        if style.shape_line_color is not None
        else (0.0, 0.0, 0.0, 0.0)
    )
    has_stroke = style.shape_line_color is not None and line_w > 0 and raw_stroke[3] > 0.0

    if style.shape_fill_color is None:
        face_fill: tuple[float, float, float, float] | str = "none"
    else:
        raw_fill = ColorUtils.get_mplot_rgba(style.shape_fill_color, alpha=style.alpha)
        face_fill = "none" if raw_fill[3] <= 0.0 else raw_fill

    stroke_color: tuple[float, float, float, float] | str = raw_stroke if has_stroke else "none"

    if has_stroke:
        feature_color = raw_stroke
        feature_w = line_w
    elif style.text_color is not None:
        feature_color = ColorUtils.get_mplot_rgba(style.text_color)
        feature_w = 1.5
    else:
        contrast_col = ColorUtils.get_contrast_text_color(style.shape_fill_color, style.alpha)
        feature_color = ColorUtils.get_mplot_rgba(contrast_col)
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


def build_plaque_path(
    xy: Coordinate,
    width: float,
    height: float,
    variant: str,
    cut_ratio: float | None,
    shape_r: float | tuple[float, ...] | None,
    angle: float,
) -> Path:
    """Build world-space Matplotlib Path for plaque shape variants."""
    cx, cy = xy
    hw, hh = width / 2.0, height / 2.0
    c_ratio = 0.22 if cut_ratio is None else float(cut_ratio)
    r = min(width, height) * min(0.45, c_ratio)

    if variant in {"concave", "standard"}:
        local_pts = (
            arc_points_local(hw, -hh, r, 180.0, 90.0, 12)
            + arc_points_local(hw, hh, r, 270.0, 180.0, 12)
            + arc_points_local(-hw, hh, r, 0.0, -90.0, 12)
            + arc_points_local(-hw, -hh, r, 90.0, 0.0, 12)
        )
        return subpaths_to_compound_path([local_pts], cx, cy, angle)

    if variant in {"chamfered", "octagon"}:
        local_pts = [
            (-hw + r, -hh),
            (hw - r, -hh),
            (hw, -hh + r),
            (hw, hh - r),
            (hw - r, hh),
            (-hw + r, hh),
            (-hw, hh - r),
            (-hw, -hh + r),
        ]
    else:
        # "notched"
        local_pts = [
            (-hw + r, -hh),
            (hw - r, -hh),
            (hw - r, -hh + r),
            (hw, -hh + r),
            (hw, hh - r),
            (hw - r, hh - r),
            (hw - r, hh),
            (-hw + r, hh),
            (-hw + r, hh - r),
            (-hw, hh - r),
            (-hw, -hh + r),
            (-hw + r, -hh + r),
        ]

    world_pts: list[Coordinate] = []
    for lx, ly in local_pts:
        rx, ry = rotate_point((lx, ly), angle=angle)
        world_pts.append((cx + rx, cy + ry))
    path_points = round_polygon_points(world_pts, shape_r)
    return build_matplotlib_path(path_points)


def signed_polygon_area(ring: list[Coordinate]) -> float:
    """Compute signed area of a 2D polygon ring (> 0 for CCW, < 0 for CW).

    Args:
        ring: Ordered list of polygon vertices.

    Returns:
        float: Signed planar area of the polygon ring.
    """
    n = len(ring)
    if n < 3:
        return 0.0
    area = 0.0
    for i in range(n):
        x1, y1 = ring[i]
        x2, y2 = ring[(i + 1) % n]
        area += x1 * y2 - x2 * y1
    return 0.5 * area


def orient_polygon_ring(
    ring: list[Coordinate],
    *,
    ccw: bool,
) -> tuple[list[Coordinate], bool]:
    """Return a copy of ring oriented CCW (ccw=True) or CW (ccw=False).

    Args:
        ring: Ordered list of polygon vertices.
        ccw: True for counter-clockwise orientation, False for clockwise.

    Returns:
        tuple[list[Coordinate], bool]: Oriented vertex list and True if reversed.
    """
    pts = list(ring)
    area = signed_polygon_area(pts)
    if area == 0.0:
        return pts, False
    is_ccw = area > 0.0
    if is_ccw != ccw:
        pts.reverse()
        return pts, True
    return pts, False


__all__ = [
    "_normalize_shape_radii",
    "_rotate_and_place_path_point",
    "_shift_path_point",
    "arc_points_local",
    "build_ellipse_path",
    "build_hollow_ellipse_path",
    "build_matplotlib_path",
    "build_plaque_path",
    "darken_rgba",
    "inset_convex_polygon",
    "lighten_rgba",
    "orient_polygon_ring",
    "resolve_feature_colors",
    "round_polygon_points",
    "shrink_shape_r",
    "signed_polygon_area",
    "subpaths_to_compound_path",
    "validate_hole_ratio",
]
