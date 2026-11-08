# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

import math
from typing import Any, cast

import pytest
from matplotlib.path import Path

from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas import canvas as global_canvas
from drawlib._core.l4_canvas._line_utils import LineUtils
from drawlib.canvas import clear, setup
from drawlib.lines import line, line_arc, lines
from drawlib.styles import Styles


class TestLineUtils:
    """Unit tests for the LineUtils static helper class."""

    def test_remove_consecutive_duplicates(self) -> None:
        """Verifies _remove_consecutive_duplicates removes consecutive duplicate points."""
        points = [(0.0, 0.0), (0.0, 0.0), (1.0, 1.0), (1.0, 1.0), (0.0, 0.0)]
        expected = [(0.0, 0.0), (1.0, 1.0), (0.0, 0.0)]
        assert LineUtils._remove_consecutive_duplicates(points) == expected

    def test_merge_straight_lines(self) -> None:
        """Verifies slope-based point merging on horizontal, vertical, and diagonal lines."""
        # 1. Less than 3 points
        assert LineUtils._merge_straight_lines([(0, 0), (1, 1)]) == [(0, 0), (1, 1)]

        # 2. Horizontal line merging (merges intermediate points)
        assert LineUtils._merge_straight_lines([(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0)]) == [
            (0.0, 0.0),
            (3.0, 0.0),
        ]

        # 3. Vertical line merging (merges intermediate points)
        assert LineUtils._merge_straight_lines([(0.0, 0.0), (0.0, 1.0), (0.0, 2.0), (0.0, 3.0)]) == [
            (0.0, 0.0),
            (0.0, 3.0),
        ]

        # 4. Diagonal points
        assert LineUtils._merge_straight_lines([(0.0, 0.0), (1.0, 1.0), (2.0, 2.0)]) == [
            (0.0, 0.0),
            (1.0, 1.0),
            (2.0, 2.0),
        ]

        # 5. Non-straight transition
        assert LineUtils._merge_straight_lines([(0.0, 0.0), (1.0, 1.0), (2.0, 1.0)]) == [
            (0.0, 0.0),
            (1.0, 1.0),
            (2.0, 1.0),
        ]

    def test_sanitize_xys(self) -> None:
        """Verifies sanitize_xys merges straight lines and removes consecutive duplicates."""
        points = [(0.0, 0.0), (0.0, 0.0), (1.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0)]
        assert LineUtils.sanitize_xys(points) == [(0.0, 0.0), (3.0, 0.0)]

    def test_format_style(self) -> None:
        """Verifies format_style validates Style and raises errors on invalid input."""
        # 1. Test valid Style object
        custom_style = Style(line_width=8.0, line_color=(255, 0, 0, 1.0))
        formatted_obj = LineUtils.format_style(custom_style)
        assert formatted_obj.line_width == 8.0
        assert formatted_obj.line_color == (255, 0, 0, 1.0)

        # 2. Test unsupported / missing required properties raises ValueError
        with pytest.raises(ValueError, match="Style cannot be used for line"):
            LineUtils.format_style(Style(line_width=8.0))
        with pytest.raises(ValueError, match="Style cannot be used for line"):
            LineUtils.format_style(Style(line_color=(255, 0, 0, 1.0)))
        with pytest.raises(ValueError, match="Style cannot be used for line"):
            LineUtils.validate_line_style(Style(line_width=8.0))

        # 3. Test invalid style types raise TypeError
        with pytest.raises(TypeError):
            LineUtils.format_style(123)  # type: ignore
        with pytest.raises(TypeError):
            LineUtils.format_style("primary")  # type: ignore

    def test_get_fancyarrowpatch_options(self) -> None:
        """Verifies conversion of Style to matplotlib's FancyArrowPatch options."""
        style = Style(
            line_width=3.5,
            line_style="dashed",
            line_color=(255, 0, 0),
            alpha=0.9,
            line_arrow_head_scale=15.0,
            line_arrow_head_fill=True,
        )

        # 1. Test without arrowhead ("")
        options_no_arrow = LineUtils.get_fancyarrowpatch_options("", style)
        assert options_no_arrow["linewidth"] == 3.5
        assert options_no_arrow["linestyle"] == "dashed"
        assert options_no_arrow["color"] == (1.0, 0.0, 0.0, 1.0)
        assert options_no_arrow["alpha"] == 0.9
        assert options_no_arrow["arrowstyle"] == "-"

        # 2. Test with filled arrowhead ("->")
        options_filled_arrow = LineUtils.get_fancyarrowpatch_options("->", style)
        assert options_filled_arrow["arrowstyle"] == "-|>"
        assert options_filled_arrow["mutation_scale"] == 15.0

        # 3. Test with filled arrowhead ("<-")
        options_left_filled = LineUtils.get_fancyarrowpatch_options("<-", style)
        assert options_left_filled["arrowstyle"] == "<|-"

        # 4. Test with filled arrowhead ("<->")
        options_both_filled = LineUtils.get_fancyarrowpatch_options("<->", style)
        assert options_both_filled["arrowstyle"] == "<|-|>"

        # 5. Test with unfilled arrowhead (ahfill = False)
        unfilled_style = Style(line_width=3.5, line_color=(0, 0, 0), line_style="solid", line_arrow_head_fill=False)
        options_unfilled = LineUtils.get_fancyarrowpatch_options("->", unfilled_style)
        assert options_unfilled["arrowstyle"] == "->"

        # 6. Test curved=True uses _SecantCurveArrowStyle
        options_curved = LineUtils.get_fancyarrowpatch_options("->", unfilled_style, curved=True)
        assert options_curved["arrowstyle"] != "->"
        assert getattr(options_curved["arrowstyle"], "_endarrow_head", False) is True
        assert getattr(options_curved["arrowstyle"], "fillend", True) is False

        options_curved_filled = LineUtils.get_fancyarrowpatch_options("<->", style, curved=True)
        assert getattr(options_curved_filled["arrowstyle"], "_beginarrow_head", False) is True
        assert getattr(options_curved_filled["arrowstyle"], "_endarrow_head", False) is True
        assert getattr(options_curved_filled["arrowstyle"], "fillbegin", False) is True
        assert getattr(options_curved_filled["arrowstyle"], "fillend", False) is True

    def test_secant_curve_arrow_transmute(self) -> None:
        """Verifies _SecantCurveArrowStyle aligns curved arrowheads along the secant over head_length."""
        style = Style(line_width=2.5, line_color=(0, 0, 0), line_style="solid", line_arrow_head_scale=20.0)
        arrow_style = LineUtils.get_fancyarrowpatch_options("->", style, curved=True)["arrowstyle"]

        # Tight quadratic Bezier curve in display coords: (0, 0) -> cp(15, 16) -> (30, 0)
        q_path = Path([(0.0, 0.0), (15.0, 16.0), (30.0, 0.0)], [Path.MOVETO, Path.CURVE3, Path.CURVE3])
        paths, fills = cast(
            "tuple[list[Path], list[bool]]", arrow_style.transmute(q_path, mutation_size=20.0, linewidth=2.5)
        )
        assert len(paths) == 2
        assert fills == [False, False]

        wedge_verts = cast(Any, paths[1].vertices)
        w1, tip, w2 = wedge_verts[0], wedge_verts[1], wedge_verts[2]
        mid_wing = ((w1[0] + w2[0]) / 2.0, (w1[1] + w2[1]) / 2.0)
        axis_deg = math.degrees(math.atan2(tip[1] - mid_wing[1], tip[0] - mid_wing[0]))
        endpoint_tangent_deg = math.degrees(math.atan2(0.0 - 16.0, 30.0 - 15.0))  # -46.8 deg
        # Secant axis should be noticeably shallower than the raw endpoint tangent (-46.8 deg)
        assert endpoint_tangent_deg < axis_deg < -10.0

    def test_check_arrowhead_segment_warnings(self) -> None:
        """Verifies non-fatal geometry warning detection for buried polyline arrowheads."""
        clear()
        setup(width=140, height=80)

        # 1. Sufficiently spaced orthogonal polyline -> no warning
        lines([(10.0, 20.0), (25.0, 20.0), (25.0, 40.0), (32.0, 40.0)], arrow_head="->", style=Styles.DarkBold)
        # 2. Full 360-degree closed arc -> no false positive warning
        line_arc(
            (70.0, 40.0),
            width=20.0,
            height=20.0,
            angle_start=0,
            angle_end=360,
            arrow_head="->",
            style=Styles.DarkBold,
        )
        assert LineUtils.check_arrowhead_segment_warnings(global_canvas._artists, 140.0) == []

        # 3. Buried terminal segment (1.5u < ~2.56u required on W=140 with DarkBold) -> emits warning
        lines([(40.0, 20.0), (45.0, 20.0), (45.0, 35.0), (46.5, 35.0)], arrow_head="->", style=Styles.DarkBold)
        warnings_list = LineUtils.check_arrowhead_segment_warnings(global_canvas._artists, 140.0)
        assert len(warnings_list) == 1
        assert "terminal polyline segment" in warnings_list[0]

        # 4. Ultra-short direct line -> emits warning
        line((80.0, 20.0), (81.0, 20.0), arrow_head="->", style=Styles.DarkBold)
        warnings_list2 = LineUtils.check_arrowhead_segment_warnings(global_canvas._artists, 140.0)
        assert len(warnings_list2) == 2
        clear()
