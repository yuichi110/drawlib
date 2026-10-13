# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Line utility module for canvas operations."""

from __future__ import annotations

import math
from typing import Any

from drawlib._core.l2_types import ArrowHead, Coordinate, PathPoints
from drawlib._core.l3_colors import ColorUtils
from drawlib._core.l3_math import get_point_on_ellipse
from drawlib._core.l3_styles import Style


class LineUtils:
    """A utility class for handling line styles, geometry, and options."""

    def __init__(self) -> None:
        """Raise TypeError to prevent instantiation of utility class."""
        raise TypeError(f"'{self.__class__.__name__}' is a static utility class and cannot be instantiated.")

    @staticmethod
    def _remove_consecutive_duplicates(xys: list[tuple[float, float]]) -> list[tuple[float, float]]:
        """Remove consecutive duplicate points from a list of coordinates."""
        return [v for i, v in enumerate(xys) if i == 0 or v != xys[i - 1]]

    @staticmethod
    def _merge_straight_lines(xys: list[tuple[float, float]]) -> list[tuple[float, float]]:
        """Merge consecutive intermediate points that form a straight horizontal or vertical line."""
        if len(xys) < 3:
            return xys

        points: list[tuple[float, float]] = [xys[0]]
        for i in range(1, len(xys) - 1):
            p_prev = points[-1]
            p_curr = xys[i]
            p_next = xys[i + 1]

            # Skip intermediate points on straight horizontal or vertical segments
            is_vertical = p_prev[0] == p_curr[0] == p_next[0]
            is_horizontal = p_prev[1] == p_curr[1] == p_next[1]
            if is_vertical or is_horizontal:
                continue

            points.append(p_curr)

        points.append(xys[-1])
        return points

    @staticmethod
    def sanitize_xys(xys: list[tuple[float, float]]) -> list[tuple[float, float]]:
        """Sanitize a list of coordinates by removing duplicates and merging straight lines."""
        xys = LineUtils._remove_consecutive_duplicates(xys)
        return LineUtils._merge_straight_lines(xys)

    @staticmethod
    def get_mid_points(
        xy1: tuple[float, float],
        xy2: tuple[float, float],
        r: float,
    ) -> tuple[tuple[float, float], tuple[float, float]]:
        """Calculate rounded corner transition points along segment xy1 -> xy2."""
        x1, y1 = xy1
        x2, y2 = xy2
        dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        if dist == 0:
            return xy1, xy2

        ratio = min(r / dist, 0.5)
        p1 = (x1 + (x2 - x1) * ratio, y1 + (y2 - y1) * ratio)
        p2 = (x2 - (x2 - x1) * ratio, y2 - (y2 - y1) * ratio)
        return p1, p2

    @staticmethod
    def validate_line_style(style: Style) -> None:
        """Validate that the Style supports line drawing."""
        style.validate_for("line")

    @staticmethod
    def format_style(style: Style) -> Style:
        """Validate and return line style."""
        if not isinstance(style, Style):
            raise TypeError(f'Arg "style" must be Style, but {type(style)} given.')
        style.validate_for("line")
        return style

    @staticmethod
    def get_fancyarrowpatch_options(
        arrow_head: ArrowHead,
        style: Style,
    ) -> dict[str, Any]:
        """Convert drawlib's Style to matplotlib's FancyArrowPatch options."""
        color = None if style.line_color is None else ColorUtils.get_mplot_rgba(style.line_color)
        options: dict[str, Any] = {
            "linewidth": style.line_width,
            "linestyle": style.line_style if style.line_style is not None else "solid",
            "color": color,
            "alpha": style.alpha,
        }

        if not arrow_head:
            options["arrowstyle"] = "-"
        else:
            scale = style.line_arrow_head_scale if style.line_arrow_head_scale is not None else 20.0
            options["mutation_scale"] = scale
            if style.line_arrow_head_fill:
                if arrow_head == "->":
                    options["arrowstyle"] = "-|>"
                elif arrow_head == "<-":
                    options["arrowstyle"] = "<|-"
                else:
                    options["arrowstyle"] = "<|-|>"
            else:
                options["arrowstyle"] = arrow_head

        return {k: v for k, v in options.items() if v is not None}


class LineArcHelper:
    """Helper class for elliptical arc Bezier approximations."""

    @classmethod
    def get_point_on_ellipse(
        cls,
        xy: Coordinate,
        width: float,
        height: float,
        angle: float,
    ) -> tuple[float, float]:
        """Get coordinates of a point on an ellipse at a given angle."""
        return get_point_on_ellipse(center=xy, width=width, height=height, angle=angle)

    @classmethod
    def get_ellipse_path_points(
        cls,
        xy: Coordinate,
        width: float,
        height: float,
        angle_start: float,
        angle_end: float,
    ) -> PathPoints:
        """Get bezier path points along an ellipse arc."""
        diff = angle_end - angle_start
        if diff == 0:
            return [cls.get_point_on_ellipse(xy, width, height, angle_start)]

        sweep = abs(diff)
        num_segments = max(1, math.ceil(sweep / 90.0))
        step = diff / num_segments
        path_points: PathPoints = []
        start: tuple[float, float] | None = None
        for i in range(num_segments):
            a_start = angle_start + i * step
            a_end = angle_start + (i + 1) * step
            p1, p2, p3, p4 = cls.bezier_ellipse_arc_approximation(
                xy,
                width,
                height,
                a_start,
                a_end,
            )
            if start is None:
                start = p1
            path_points.append((p2, p3, p4))

        if start is not None:
            path_points.insert(0, start)
        return path_points

    @classmethod
    def bezier_ellipse_arc_approximation(
        cls,
        xy: Coordinate,
        width: float,
        height: float,
        start_angle: float,
        end_angle: float,
    ) -> tuple[tuple[float, float], tuple[float, float], tuple[float, float], tuple[float, float]]:
        """Calculate Bezier curve approximation points for an elliptical arc."""
        x, y = xy

        start_angle_rad = math.radians(start_angle)
        end_angle_rad = math.radians(end_angle)

        start_point = (x + width / 2 * math.cos(start_angle_rad), y + height / 2 * math.sin(start_angle_rad))
        end_point = (x + width / 2 * math.cos(end_angle_rad), y + height / 2 * math.sin(end_angle_rad))

        t = (4 / 3) * math.tan((end_angle_rad - start_angle_rad) / 4)
        control_point1 = (
            start_point[0] - t * width / 2 * math.sin(start_angle_rad),
            start_point[1] + t * height / 2 * math.cos(start_angle_rad),
        )
        control_point2 = (
            end_point[0] + t * width / 2 * math.sin(end_angle_rad),
            end_point[1] - t * height / 2 * math.cos(end_angle_rad),
        )

        return start_point, control_point1, control_point2, end_point


__all__ = [
    "LineArcHelper",
    "LineUtils",
]
