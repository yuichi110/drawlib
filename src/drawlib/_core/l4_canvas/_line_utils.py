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
from typing import TYPE_CHECKING, Any, cast

from matplotlib.patches import ArrowStyle, FancyArrowPatch
from matplotlib.path import Path

from drawlib._core.l2_types import ArrowHead, Coordinate, PathPoints
from drawlib._core.l3_colors import ColorUtils
from drawlib._core.l3_math import get_point_on_ellipse
from drawlib._core.l3_styles import Style

if TYPE_CHECKING:
    from collections.abc import Sequence

    import matplotlib.artist

_Point2D = tuple[float, float]
_CubicSeg = tuple[_Point2D, _Point2D, _Point2D, _Point2D]


def _lerp_pt(a: _Point2D, b: _Point2D, t: float) -> _Point2D:
    return (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))


def _quad_to_cubic(p0: _Point2D, cp: _Point2D, p2: _Point2D) -> _CubicSeg:
    c1 = (p0[0] + (2.0 / 3.0) * (cp[0] - p0[0]), p0[1] + (2.0 / 3.0) * (cp[1] - p0[1]))
    c2 = (p2[0] + (2.0 / 3.0) * (cp[0] - p2[0]), p2[1] + (2.0 / 3.0) * (cp[1] - p2[1]))
    return (p0, c1, c2, p2)


def _eval_cubic(seg: _CubicSeg, t: float) -> _Point2D:
    p0, p1, p2, p3 = seg
    u = 1.0 - t
    u2 = u * u
    t2 = t * t
    return (
        u2 * u * p0[0] + 3.0 * u2 * t * p1[0] + 3.0 * u * t2 * p2[0] + t2 * t * p3[0],
        u2 * u * p0[1] + 3.0 * u2 * t * p1[1] + 3.0 * u * t2 * p2[1] + t2 * t * p3[1],
    )


def _subdivide_cubic_prefix(seg: _CubicSeg, t: float) -> _CubicSeg:
    p0, p1, p2, p3 = seg
    q0 = _lerp_pt(p0, p1, t)
    q1 = _lerp_pt(p1, p2, t)
    q2 = _lerp_pt(p2, p3, t)
    r0 = _lerp_pt(q0, q1, t)
    r1 = _lerp_pt(q1, q2, t)
    s0 = _lerp_pt(r0, r1, t)
    return (p0, q0, r0, s0)


def _subdivide_cubic_suffix(seg: _CubicSeg, t: float) -> _CubicSeg:
    p0, p1, p2, p3 = seg
    q0 = _lerp_pt(p0, p1, t)
    q1 = _lerp_pt(p1, p2, t)
    q2 = _lerp_pt(p2, p3, t)
    r0 = _lerp_pt(q0, q1, t)
    r1 = _lerp_pt(q1, q2, t)
    s0 = _lerp_pt(r0, r1, t)
    return (s0, r1, q2, p3)


def _subdivide_cubic_range(seg: _CubicSeg, t0: float, t1: float) -> _CubicSeg:
    if t0 <= 0.0 and t1 >= 1.0:
        return seg
    if t0 <= 0.0:
        return _subdivide_cubic_prefix(seg, t1)
    if t1 >= 1.0:
        return _subdivide_cubic_suffix(seg, t0)
    suffix = _subdivide_cubic_suffix(seg, t0)
    rem_t = (t1 - t0) / max(1e-9, 1.0 - t0)
    return _subdivide_cubic_prefix(suffix, rem_t)


def _path_to_cubic_segments(path: Path) -> list[_CubicSeg]:
    verts = cast(Any, path.vertices)
    codes = cast(Any, path.codes)
    n = len(verts)
    if n < 2:
        return []

    if codes is None:
        segs: list[_CubicSeg] = []
        for i in range(n - 1):
            a = (float(verts[i][0]), float(verts[i][1]))
            b = (float(verts[i + 1][0]), float(verts[i + 1][1]))
            segs.append((a, _lerp_pt(a, b, 1.0 / 3.0), _lerp_pt(a, b, 2.0 / 3.0), b))
        return segs

    segs = []
    curr: _Point2D = (float(verts[0][0]), float(verts[0][1]))
    i = 0
    while i < n:
        code = int(codes[i])
        if code == Path.MOVETO:
            curr = (float(verts[i][0]), float(verts[i][1]))
            i += 1
        elif code == Path.LINETO:
            nxt = (float(verts[i][0]), float(verts[i][1]))
            segs.append((curr, _lerp_pt(curr, nxt, 1.0 / 3.0), _lerp_pt(curr, nxt, 2.0 / 3.0), nxt))
            curr = nxt
            i += 1
        elif code == Path.CURVE3 and i + 1 < n:
            cp = (float(verts[i][0]), float(verts[i][1]))
            nxt = (float(verts[i + 1][0]), float(verts[i + 1][1]))
            segs.append(_quad_to_cubic(curr, cp, nxt))
            curr = nxt
            i += 2
        elif code == Path.CURVE4 and i + 2 < n:
            c1 = (float(verts[i][0]), float(verts[i][1]))
            c2 = (float(verts[i + 1][0]), float(verts[i + 1][1]))
            nxt = (float(verts[i + 2][0]), float(verts[i + 2][1]))
            segs.append((curr, c1, c2, nxt))
            curr = nxt
            i += 3
        else:
            i += 1
    return segs


class _SecantCurveArrowStyle(ArrowStyle._Base):
    """Curved-path ArrowStyle aligning arrowheads along the secant over head_length.

    Standard Matplotlib ArrowStyle._Curve orients arrowheads strictly along the
    instantaneous endpoint tangent (t=1.0 or t=0.0), causing curved shafts on
    short or tight bends to intersect the inner arrowhead wing. Aligning the
    arrowhead axis with the secant from the curve point one head_length back to
    the retracted tip (combined with de Casteljau shaft subdivision) keeps the
    curve centered between both wings without altering arrowhead scale.
    """

    def __init__(
        self,
        arrow: str = "->",
        head_length: float = 0.4,
        head_width: float = 0.2,
    ) -> None:
        self.arrow = arrow
        self.head_length = head_length
        self.head_width = head_width
        beginarrow, endarrow = arrow.split("-", 1)
        self._beginarrow_head = beginarrow in {"<", "<|"}
        self.fillbegin = beginarrow == "<|"
        self._endarrow_head = endarrow in {">", "|>"}
        self.fillend = endarrow == "|>"
        super().__init__()

    @staticmethod
    def _build_wedge(
        p_base: _Point2D,
        p_tip: _Point2D,
        head_dist: float,
        cos_t: float,
        sin_t: float,
    ) -> list[_Point2D]:
        dx = p_base[0] - p_tip[0]
        dy = p_base[1] - p_tip[1]
        d = math.hypot(dx, dy)
        if d < 1e-9:
            return []
        ux, uy = dx / d, dy / d
        vx, vy = ux * head_dist, uy * head_dist
        w1 = (p_tip[0] + cos_t * vx - sin_t * vy, p_tip[1] + sin_t * vx + cos_t * vy)
        w2 = (p_tip[0] + cos_t * vx + sin_t * vy, p_tip[1] - sin_t * vx + cos_t * vy)
        return [w1, p_tip, w2]

    @staticmethod
    def _walk_forward(
        samples: list[tuple[int, float, _Point2D]],
        start_idx: int,
        origin_pt: _Point2D,
        target_dist: float,
        max_arc: float,
    ) -> tuple[int, int, float, _Point2D]:
        arc_acc = 0.0
        for idx in range(start_idx + 1, len(samples)):
            prev_pt = samples[idx - 1][2]
            curr_pt = samples[idx][2]
            arc_acc += math.hypot(curr_pt[0] - prev_pt[0], curr_pt[1] - prev_pt[1])
            d_curr = math.hypot(curr_pt[0] - origin_pt[0], curr_pt[1] - origin_pt[1])
            if d_curr >= target_dist:
                d_prev = math.hypot(prev_pt[0] - origin_pt[0], prev_pt[1] - origin_pt[1])
                frac = (target_dist - d_prev) / max(1e-9, d_curr - d_prev) if d_curr > d_prev else 1.0
                frac = max(0.0, min(1.0, frac))
                s_prev, t_prev, _ = samples[idx - 1]
                s_curr, t_curr, _ = samples[idx]
                t_interp = (t_prev + frac * (t_curr - t_prev)) if s_prev == s_curr else frac * t_curr
                return idx, s_curr, t_interp, _lerp_pt(prev_pt, curr_pt, frac)
            if arc_acc >= max_arc:
                s_curr, t_curr, _ = samples[idx]
                return idx, s_curr, t_curr, curr_pt
        last_s, last_t, last_pt = samples[-1]
        return len(samples) - 1, last_s, last_t, last_pt

    @staticmethod
    def _walk_backward(
        samples: list[tuple[int, float, _Point2D]],
        start_idx: int,
        origin_pt: _Point2D,
        target_dist: float,
        max_arc: float,
    ) -> tuple[int, int, float, _Point2D]:
        arc_acc = 0.0
        for idx in range(start_idx - 1, -1, -1):
            next_pt = samples[idx + 1][2]
            curr_pt = samples[idx][2]
            arc_acc += math.hypot(next_pt[0] - curr_pt[0], next_pt[1] - curr_pt[1])
            d_curr = math.hypot(origin_pt[0] - curr_pt[0], origin_pt[1] - curr_pt[1])
            if d_curr >= target_dist:
                d_next = math.hypot(origin_pt[0] - next_pt[0], origin_pt[1] - next_pt[1])
                frac = (target_dist - d_next) / max(1e-9, d_curr - d_next) if d_curr > d_next else 1.0
                frac = max(0.0, min(1.0, frac))
                s_next, t_next, _ = samples[idx + 1]
                s_curr, t_curr, _ = samples[idx]
                t_interp = (t_next + frac * (t_curr - t_next)) if s_curr == s_next else (1.0 - frac * (1.0 - t_curr))
                return idx, s_curr, t_interp, _lerp_pt(next_pt, curr_pt, frac)
            if arc_acc >= max_arc:
                s_curr, t_curr, _ = samples[idx]
                return idx, s_curr, t_curr, curr_pt
        first_s, first_t, first_pt = samples[0]
        return 0, first_s, first_t, first_pt

    @staticmethod
    def _sample_segments(segs: list[_CubicSeg], steps: int = 64) -> tuple[list[tuple[int, float, _Point2D]], float]:
        samples: list[tuple[int, float, _Point2D]] = []
        total_arc = 0.0
        for s_idx, seg in enumerate(segs):
            start_k = 0 if s_idx == 0 else 1
            for k in range(start_k, steps + 1):
                t = k / steps
                pt = _eval_cubic(seg, t)
                if samples:
                    prev = samples[-1][2]
                    total_arc += math.hypot(pt[0] - prev[0], pt[1] - prev[1])
                samples.append((s_idx, t, pt))
        return samples, total_arc

    def _assemble_paths(
        self,
        fallback_path: Path,
        trimmed_segs: list[_CubicSeg],
        verts_a: list[_Point2D],
        verts_b: list[_Point2D],
    ) -> tuple[list[Path], list[bool]]:
        paths: list[Path] = []
        fills: list[bool] = []

        if trimmed_segs:
            shaft_verts: list[_Point2D] = [trimmed_segs[0][0]]
            shaft_codes: list[Any] = [Path.MOVETO]
            for _, c1, c2, p3 in trimmed_segs:
                shaft_verts.extend([c1, c2, p3])
                shaft_codes.extend([Path.CURVE4, Path.CURVE4, Path.CURVE4])
            paths.append(Path(shaft_verts, shaft_codes))
            fills.append(False)

        for verts, is_filled in ((verts_a, self.fillbegin), (verts_b, self.fillend)):
            if not verts:
                continue
            if is_filled:
                paths.append(Path([*verts, (0.0, 0.0)], [Path.MOVETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY]))
                fills.append(True)
            else:
                paths.append(Path(verts, [Path.MOVETO, Path.LINETO, Path.LINETO]))
                fills.append(False)

        if not paths:
            return [fallback_path], [False]
        return paths, fills

    def transmute(
        self,
        path: Path,
        mutation_size: float,
        linewidth: float,
    ) -> tuple[Path, bool]:
        """Transform display-coordinate path into trimmed shaft and secant-aligned arrowheads."""
        segs = _path_to_cubic_segments(path)
        if not segs:
            return cast("tuple[Path, bool]", ([path], [False]))

        samples, total_arc = self._sample_segments(segs)
        if total_arc < 1e-6:
            return cast("tuple[Path, bool]", ([path], [False]))

        head_len = self.head_length * mutation_size
        head_wid = self.head_width * mutation_size
        head_dist = math.hypot(head_len, head_wid)
        cos_t, sin_t = head_len / head_dist, head_wid / head_dist
        pad_proj = 0.5 * linewidth / sin_t

        beg_seg, beg_t = 0, 0.0
        end_seg, end_t = len(segs) - 1, 1.0
        verts_a: list[_Point2D] = []
        verts_b: list[_Point2D] = []

        if self._beginarrow_head:
            idx_tip_a, beg_seg, beg_t, p_tip_a = self._walk_forward(
                samples, 0, samples[0][2], pad_proj, max_arc=pad_proj * 1.5
            )
            _, _, _, p_base_a = self._walk_forward(samples, idx_tip_a, p_tip_a, head_len, max_arc=head_len * 1.35)
            verts_a = self._build_wedge(p_base_a, p_tip_a, head_dist, cos_t, sin_t)

        if self._endarrow_head:
            idx_tip_b, end_seg, end_t, p_tip_b = self._walk_backward(
                samples, len(samples) - 1, samples[-1][2], pad_proj, max_arc=pad_proj * 1.5
            )
            _, _, _, p_base_b = self._walk_backward(samples, idx_tip_b, p_tip_b, head_len, max_arc=head_len * 1.35)
            verts_b = self._build_wedge(p_base_b, p_tip_b, head_dist, cos_t, sin_t)

        trimmed_segs = [
            _subdivide_cubic_range(segs[s_idx], beg_t if s_idx == beg_seg else 0.0, end_t if s_idx == end_seg else 1.0)
            for s_idx in range(beg_seg, end_seg + 1)
            if (beg_seg, beg_t) < (end_seg, end_t)
            and ((end_t if s_idx == end_seg else 1.0) - (beg_t if s_idx == beg_seg else 0.0)) > 1e-6
        ]
        return cast("tuple[Path, bool]", self._assemble_paths(path, trimmed_segs, verts_a, verts_b))


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
        *,
        curved: bool = False,
    ) -> dict[str, Any]:
        """Convert drawlib's Style to matplotlib's FancyArrowPatch options."""
        color = None if style.line_color is None else ColorUtils.get_mplot_rgba(style.line_color)
        options: dict[str, Any] = {
            "linewidth": style.line_width,
            "linestyle": style.line_style if style.line_style is not None else "solid",
            "color": color,
            "alpha": style.alpha,
        }

        if not arrow_head or arrow_head == "-":
            options["arrowstyle"] = "-"
        else:
            scale = style.line_arrow_head_scale if style.line_arrow_head_scale is not None else 20.0
            options["mutation_scale"] = scale
            if style.line_arrow_head_fill:
                if arrow_head == "->":
                    arrow_str = "-|>"
                elif arrow_head == "<-":
                    arrow_str = "<|-"
                else:
                    arrow_str = "<|-|>"
            else:
                arrow_str = arrow_head

            options["arrowstyle"] = _SecantCurveArrowStyle(arrow_str) if curved else arrow_str

        return {k: v for k, v in options.items() if v is not None}

    @staticmethod
    def _check_pos_arrow(
        pos_a_b: tuple[Any, Any],
        pt_per_unit: float,
        need_pt: float,
    ) -> list[str]:
        p_a, p_b = pos_a_b
        seg_units = math.hypot(float(p_b[0]) - float(p_a[0]), float(p_b[1]) - float(p_a[1]))
        seg_pt = seg_units * pt_per_unit
        if seg_pt + 0.25 < need_pt:
            need_u = need_pt / pt_per_unit
            return [
                f"Arrowhead footprint ({need_u:.2f}u / {need_pt:.1f}pt) exceeds line length "
                f"({seg_units:.2f}u / {seg_pt:.1f}pt) between "
                f"({float(p_a[0]):.1f}, {float(p_a[1]):.1f}) and ({float(p_b[0]):.1f}, {float(p_b[1]):.1f})."
            ]
        return []

    @staticmethod
    def _check_curved_path_arrow(
        orig_path: Path,
        orig_verts: Any,  # noqa: ANN401
        pt_per_unit: float,
        need_pt: float,
    ) -> list[str]:
        segs = _path_to_cubic_segments(orig_path)
        arc_units = 0.0
        for seg in segs:
            prev = seg[0]
            for step_k in range(1, 17):
                curr = _eval_cubic(seg, step_k / 16.0)
                arc_units += math.hypot(curr[0] - prev[0], curr[1] - prev[1])
                prev = curr
        arc_pt = arc_units * pt_per_unit
        if arc_pt + 0.25 < need_pt:
            end_v = orig_verts[-1]
            need_u = need_pt / pt_per_unit
            return [
                f"Arrowhead footprint ({need_u:.2f}u / {need_pt:.1f}pt) exceeds curved path length "
                f"({arc_units:.2f}u / {arc_pt:.1f}pt) near ({float(end_v[0]):.1f}, {float(end_v[1]):.1f})."
            ]
        return []

    @staticmethod
    def _check_polyline_arrow(
        orig_verts: Any,  # noqa: ANN401
        pt_per_unit: float,
        req_direct_pt: float,
        req_corner_pt: float,
        has_begin: bool,
        has_end: bool,
    ) -> list[str]:
        pts = LineUtils.sanitize_xys([(float(vx), float(vy)) for vx, vy in orig_verts])
        if len(pts) < 2:
            return []

        is_corner = len(pts) >= 3
        threshold_pt = req_corner_pt if is_corner else (req_direct_pt * (2.0 if (has_begin and has_end) else 1.0))
        out: list[str] = []

        if has_end:
            p_prev, p_end = pts[-2], pts[-1]
            seg_u = math.hypot(p_end[0] - p_prev[0], p_end[1] - p_prev[1])
            seg_pt = seg_u * pt_per_unit
            if seg_pt + 0.25 < threshold_pt:
                need_u = threshold_pt / pt_per_unit
                kind = "terminal polyline segment" if is_corner else "line segment"
                out.append(
                    f"Arrowhead footprint ({need_u:.2f}u / {threshold_pt:.1f}pt) exceeds {kind} "
                    f"({seg_u:.2f}u / {seg_pt:.1f}pt) from ({p_prev[0]:.1f}, {p_prev[1]:.1f}) "
                    f"to ({p_end[0]:.1f}, {p_end[1]:.1f}); increase node gap or lower line_arrow_head_scale."
                )

        if has_begin and is_corner:
            p_start, p_next = pts[0], pts[1]
            seg_u = math.hypot(p_next[0] - p_start[0], p_next[1] - p_start[1])
            seg_pt = seg_u * pt_per_unit
            if seg_pt + 0.25 < threshold_pt:
                need_u = threshold_pt / pt_per_unit
                out.append(
                    f"Start arrowhead footprint ({need_u:.2f}u / {threshold_pt:.1f}pt) exceeds initial "
                    f"polyline segment ({seg_u:.2f}u / {seg_pt:.1f}pt) from ({p_start[0]:.1f}, {p_start[1]:.1f}) "
                    f"to ({p_next[0]:.1f}, {p_next[1]:.1f}); increase node gap or lower line_arrow_head_scale."
                )
        return out

    @staticmethod
    def check_arrowhead_segment_warnings(
        artists: Sequence[matplotlib.artist.Artist],
        canvas_width: float,
    ) -> list[str]:
        """Detect arrowheads whose physical footprint exceeds their terminal line segment."""
        if canvas_width <= 0:
            return []

        pt_per_unit = 720.0 / float(canvas_width)
        sin_t = 0.2 / math.hypot(0.4, 0.2)
        warnings_out: list[str] = []

        for artist in artists:
            if not isinstance(artist, FancyArrowPatch):
                continue
            arrow_style = artist.get_arrowstyle()
            has_begin = bool(getattr(arrow_style, "_beginarrow_head", False))
            has_end = bool(getattr(arrow_style, "_endarrow_head", False))
            if not has_begin and not has_end:
                continue

            scale = float(artist.get_mutation_scale() or 20.0)
            lw = float(artist.get_linewidth() or 1.5)
            req_direct_pt = 0.4 * scale + 0.5 * lw / sin_t
            req_corner_pt = req_direct_pt + 0.95 * lw
            need_direct_pt = req_direct_pt * (2.0 if (has_begin and has_end) else 1.0)

            pos_a_b = getattr(artist, "_posA_posB", None)
            if pos_a_b is not None:
                warnings_out.extend(LineUtils._check_pos_arrow(pos_a_b, pt_per_unit, need_direct_pt))
                continue

            orig_path: Path | None = getattr(artist, "_path_original", None)
            if orig_path is None:
                continue
            orig_verts = cast(Any, orig_path.vertices)
            if len(orig_verts) < 2:
                continue

            orig_codes = cast(Any, orig_path.codes)
            if orig_codes is not None and any(int(c) in {Path.CURVE3, Path.CURVE4} for c in orig_codes):
                warnings_out.extend(
                    LineUtils._check_curved_path_arrow(orig_path, orig_verts, pt_per_unit, need_direct_pt)
                )
            else:
                warnings_out.extend(
                    LineUtils._check_polyline_arrow(
                        orig_verts, pt_per_unit, req_direct_pt, req_corner_pt, has_begin, has_end
                    )
                )

        return warnings_out


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
