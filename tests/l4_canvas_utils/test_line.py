# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

import pytest

from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas_utils._line import LineUtil
from drawlib._preset_styles import get_style


class TestLineUtil:
    """Unit tests for the LineUtil static helper class."""

    def test_remove_consecutive_duplicates(self) -> None:
        """Verifies _remove_consecutive_duplicates removes consecutive duplicate points."""
        points = [(0.0, 0.0), (0.0, 0.0), (1.0, 1.0), (1.0, 1.0), (0.0, 0.0)]
        expected = [(0.0, 0.0), (1.0, 1.0), (0.0, 0.0)]
        assert LineUtil._remove_consecutive_duplicates(points) == expected

    def test_merge_straight_lines(self) -> None:
        """Verifies slope-based point merging on horizontal, vertical, and diagonal lines."""
        # 1. Less than 3 points
        assert LineUtil._merge_straight_lines([(0, 0), (1, 1)]) == [(0, 0), (1, 1)]

        # 2. Horizontal line merging (merges every other point due to skip_next behavior)
        assert LineUtil._merge_straight_lines([(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0)]) == [
            (0.0, 0.0),
            (2.0, 0.0),
        ]

        # 3. Vertical line merging (merges every other point due to skip_next behavior)
        assert LineUtil._merge_straight_lines([(0.0, 0.0), (0.0, 1.0), (0.0, 2.0), (0.0, 3.0)]) == [
            (0.0, 0.0),
            (0.0, 2.0),
        ]

        # 4. Diagonal line merging (slope = 1.0)
        assert LineUtil._merge_straight_lines([(0.0, 0.0), (1.0, 1.0), (2.0, 2.0)]) == [(0.0, 0.0), (2.0, 2.0)]

        # 5. Non-straight transition
        assert LineUtil._merge_straight_lines([(0.0, 0.0), (1.0, 1.0), (2.0, 1.0)]) == [
            (0.0, 0.0),
            (1.0, 1.0),
            (2.0, 1.0),
        ]

    def test_sanitize_xys(self) -> None:
        """Verifies sanitize_xys merges straight lines and removes consecutive duplicates."""
        points = [(0.0, 0.0), (0.0, 0.0), (1.0, 1.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)]
        assert LineUtil.sanitize_xys(points) == [(0.0, 0.0), (2.0, 2.0)]

    def test_format_style(self) -> None:
        """Verifies format_style merges Style correctly and raises ValueError on invalid types."""
        # 1. Test None style
        formatted_none = LineUtil.format_style(None)
        assert isinstance(formatted_none, Style)
        assert formatted_none.line_width == get_style().line_width

        # 2. Test string style
        formatted_str = LineUtil.format_style("primary")
        assert formatted_str.text_color == get_style("primary").text_color

        # 3. Test Style object
        custom_style = Style(line_width=8.0)
        formatted_obj = LineUtil.format_style(custom_style)
        assert formatted_obj.line_width == 8.0

        # 4. Test invalid style types raise ValueError
        with pytest.raises(ValueError):
            LineUtil.format_style(123)  # type: ignore

    def test_get_fancyarrowpatch_options(self) -> None:
        """Verifies conversion of Style to matplotlib's FancyArrowPatch options."""
        style = Style(
            line_width=3.5,
            line_style="dashed",
            line_color=(255, 0, 0),
            fill_alpha=0.9,
            arrow_head_scale=15.0,
            arrow_head_fill=True,
        )

        # 1. Test without arrowhead ("")
        options_no_arrow = LineUtil.get_fancyarrowpatch_options("", style)
        assert options_no_arrow["linewidth"] == 3.5
        assert options_no_arrow["linestyle"] == "dashed"
        assert options_no_arrow["color"] == (1.0, 0.0, 0.0, 1.0)
        assert options_no_arrow["alpha"] == 0.9
        assert options_no_arrow["arrowstyle"] == "-"

        # 2. Test with filled arrowhead ("->")
        options_filled_arrow = LineUtil.get_fancyarrowpatch_options("->", style)
        assert options_filled_arrow["arrowstyle"] == "-|>"
        assert options_filled_arrow["mutation_scale"] == 15.0

        # 3. Test with filled arrowhead ("<-")
        options_left_filled = LineUtil.get_fancyarrowpatch_options("<-", style)
        assert options_left_filled["arrowstyle"] == "<|-"

        # 4. Test with filled arrowhead ("<->")
        options_both_filled = LineUtil.get_fancyarrowpatch_options("<->", style)
        assert options_both_filled["arrowstyle"] == "<|-|>"

        # 5. Test with unfilled arrowhead (ahfill = False)
        unfilled_style = Style(line_width=3.5, line_style="solid", arrow_head_fill=False)
        options_unfilled = LineUtil.get_fancyarrowpatch_options("->", unfilled_style)
        assert options_unfilled["arrowstyle"] == "->"
