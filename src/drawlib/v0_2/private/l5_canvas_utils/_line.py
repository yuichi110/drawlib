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

from drawlib.v0_2.private.l2_models import StaticContainer
from drawlib.v0_2.private.l2_types import TypeArrowHead
from drawlib.v0_2.private.l3_styles import SYSTEM_DEFAULT_LINE_STYLE, LineStyle
from drawlib.v0_2.private.l4_theme import dtheme
from drawlib.v0_2.private.l5_canvas_utils._colors import ColorUtil
from drawlib.v0_2.private.l5_canvas_utils._utils import get_dict_value_none_keys_removed


class LineUtil(StaticContainer):
    """A utility class for handling line styles and options."""

    @staticmethod
    def _remove_consecutive_duplicates(xys: list[tuple[float, float]]) -> list[tuple[float, float]]:
        """Remove consecutive duplicate points from a list of coordinates.

        Args:
            xys (list[tuple[float, float]]): List of x, y coordinates.

        Returns:
            list[tuple[float, float]]: List with consecutive duplicates removed.
        """
        return [v for i, v in enumerate(xys) if i == 0 or v != xys[i - 1]]

    @staticmethod
    def _merge_straight_lines(xys: list[tuple[float, float]]) -> list[tuple[float, float]]:  # noqa: C901
        """Merge consecutive points that form a straight line.

        Args:
            xys (list[tuple[float, float]]): List of x, y coordinates.

        Returns:
            list[tuple[float, float]]: List with redundant intermediate points removed.
        """
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

            x0, y0 = points[-1]
            x1, y1 = xys[i]
            x2, y2 = xys[i + 1]

            # vertical lines
            if x1 - x0 == 0:
                if x2 - x1 == 0:
                    points.append(xys[i + 1])
                    skip_next = True
                    continue
                else:
                    points.append(xys[i])
                    if i == len(xys) - 2:
                        points.append(xys[i + 1])
                    continue

            if x2 - x1 == 0:
                points.append(xys[i])
                if i == len(xys) - 2:
                    points.append(xys[i + 1])
                continue

            # calculate slopes
            m1 = (y1 - y0) / (x1 - x0)
            m2 = (y2 - y1) / (x2 - x1)
            if m1 == m2:
                skip_next = True
                points.append(xys[i + 1])
            else:
                points.append(xys[i])
                if i == len(xys) - 2:
                    points.append(xys[i + 1])

        return points

    @staticmethod
    def sanitize_xys(xys: list[tuple[float, float]]) -> list[tuple[float, float]]:
        """Sanitize a list of coordinates by removing duplicates and merging straight lines.

        Args:
            xys (list[tuple[float, float]]): List of x, y coordinates to sanitize.

        Returns:
            list[tuple[float, float]]: Sanitized list of coordinates.
        """
        xys = LineUtil._remove_consecutive_duplicates(xys)
        return LineUtil._merge_straight_lines(xys)

    @staticmethod
    def format_style(
        style: LineStyle | str | None,
    ) -> LineStyle:
        """Format and retrieve a LineStyle object based on input parameters.

        Args:
            style (LineStyle | str | None):
                The style to format. Can be a LineStyle object, a style name (str),
                or None. If None, the default line style from dtheme.linestyles is used.

        Returns:
            LineStyle: The formatted LineStyle object.

        Raises:
            ValueError: If the input style parameter is invalid or cannot be formatted.

        Notes:
            - The returned style is a merged result of the input style, dtheme.linestyles.get(),
              and SYSTEM_DEFAULT_LINE_STYLE.
        """
        if style is None:
            style = dtheme.linestyles.get()
        elif isinstance(style, str):
            style = dtheme.linestyles.get(name=style)
        elif isinstance(style, LineStyle):
            ...
        else:
            raise ValueError(f'Arg "style" type must be one of LineStyle, str, None. But "{type(style)}" is given.')

        style = dtheme.linestyles.get().merge(style)
        style = SYSTEM_DEFAULT_LINE_STYLE.merge(style)
        return style

    @staticmethod
    def get_fancyarrowpatch_options(
        arrowhead: TypeArrowHead,
        style: LineStyle,
    ) -> dict[str, Any]:
        """Convert drawlib's LineStyle to matplotlib's line options for fancy arrow patches.

        Matplotlib handles line style arguments in its function calls.
        This method converts drawlib's LineStyle into a dictionary suitable for
        matplotlib's function parameters.

        Args:
            arrowhead (TypeArrowHead):
                The arrowhead style to apply. "" for no arrow, "->" for one-way arrow,
                "<-" for opposite one-way arrow, "<->" for two-way arrow.
            style (LineStyle):
                The LineStyle object containing line properties.

        Returns:
            dict[str, Any]: A dictionary containing matplotlib's line options.

        Notes:
            - Apply the returned options dictionary to matplotlib's function calls,
              e.g., `Line2D(arg1, ..., **options)`, to apply LineStyle's style.
        """
        color = None if style.color is None else ColorUtil.get_mplot_rgba(style.color)
        options: dict[str, Any] = {
            "linewidth": style.width,
            "linestyle": style.style,
            "color": color,
            "alpha": style.alpha,
        }

        if not arrowhead:
            options["arrowstyle"] = "-"

        else:
            options["mutation_scale"] = style.ahscale
            if style.ahfill:
                if arrowhead == "->":
                    options["arrowstyle"] = "-|>"
                elif arrowhead == "<-":
                    options["arrowstyle"] = "<|-"
                else:
                    options["arrowstyle"] = "<|-|>"
            else:
                options["arrowstyle"] = arrowhead

        return get_dict_value_none_keys_removed(options)
