# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Line utility module for canvas operations."""

from typing import Any

from drawlib._core.l2_types import ArrowHead
from drawlib._core.l3_colors import ColorUtil
from drawlib._core.l3_styles import Style


class LineUtil:
    """A utility class for handling line styles and options."""

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
        xys = LineUtil._remove_consecutive_duplicates(xys)
        return LineUtil._merge_straight_lines(xys)

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
        arrowhead: ArrowHead,
        style: Style,
    ) -> dict[str, Any]:
        """Convert drawlib's Style to matplotlib's FancyArrowPatch options."""
        color = None if style.line_color is None else ColorUtil.get_mplot_rgba(style.line_color)
        options: dict[str, Any] = {
            "linewidth": style.line_width,
            "linestyle": style.line_style if style.line_style is not None else "solid",
            "color": color,
            "alpha": style.line_alpha,
        }

        if not arrowhead:
            options["arrowstyle"] = "-"
        else:
            scale = style.line_arrow_head_scale if style.line_arrow_head_scale is not None else 20.0
            options["mutation_scale"] = scale
            if style.line_arrow_head_fill:
                if arrowhead == "->":
                    options["arrowstyle"] = "-|>"
                elif arrowhead == "<-":
                    options["arrowstyle"] = "<|-"
                else:
                    options["arrowstyle"] = "<|-|>"
            else:
                options["arrowstyle"] = arrowhead

        return {k: v for k, v in options.items() if v is not None}


__all__ = ["LineUtil"]
