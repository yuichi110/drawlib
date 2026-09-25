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

from drawlib._core.l2_models import StaticContainer
from drawlib._core.l2_types import TypeArrowHead
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas_utils._colors import ColorUtil
from drawlib._core.l4_canvas_utils._utils import get_dict_value_none_keys_removed


class LineUtil(StaticContainer):
    """A utility class for handling line styles and options."""

    @staticmethod
    def _remove_consecutive_duplicates(xys: list[tuple[float, float]]) -> list[tuple[float, float]]:
        """Remove consecutive duplicate points from a list of coordinates."""
        return [v for i, v in enumerate(xys) if i == 0 or v != xys[i - 1]]

    @staticmethod
    def _merge_straight_lines(xys: list[tuple[float, float]]) -> list[tuple[float, float]]:  # noqa: C901
        """Merge consecutive points that form a straight line."""
        if len(xys) < 3:
            return xys

        points: list[tuple[float, float]] = []
        skip_next = False
        for i in range(len(xys) - 1):
            if skip_next:
                skip_next = False
                continue

            if i == 0:
                points.append(xys[i])
                continue

            p_prev = points[-1]
            p_curr = xys[i]
            p_next = xys[i + 1]

            if p_prev[0] == p_curr[0] == p_next[0] or p_prev[1] == p_curr[1] == p_next[1]:
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
        """Validate that the required line properties are set in Style.

        Args:
            style: The Style instance to validate.

        Raises:
            ValueError: If any required line property is None.
        """
        missing: list[str] = []
        if style.line_color is None:
            missing.append("line_color")
        if style.line_width is None:
            missing.append("line_width")

        if missing:
            raise ValueError(
                f"Line drawing requires attributes {missing}, but they are None in the provided Style."
            )

    @staticmethod
    def format_style(style: Style) -> Style:
        """Validate and format line style.

        Args:
            style: The Style instance for line drawing.

        Returns:
            Style: Validated Style instance.

        Raises:
            TypeError: If style is not a Style instance.
            ValueError: If required core properties are missing.
        """
        if not isinstance(style, Style):
            raise TypeError(f'Arg "style" must be Style, but {type(style)} given.')

        LineUtil.validate_line_style(style)
        return style

    @staticmethod
    def get_fancyarrowpatch_options(
        arrowhead: TypeArrowHead,
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

        return get_dict_value_none_keys_removed(options)
