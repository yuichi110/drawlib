# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Animated tour of the five auto-layout graph coordinate solvers (APNG)."""

from __future__ import annotations

import math

from drawlib.anim import Animation
from drawlib.canvas import save, setup
from drawlib.graph import (
    ArchitectureGraph,
    GridGraph,
    LayerGraph,
    RadialGraph,
    TreeGraph,
)
from drawlib.icons import phosphor
from drawlib.lines import line, lines
from drawlib.shapes import circle, rectangle
from drawlib.styles import Style, Styles
from drawlib.text import text

W, H = 136.0, 96.0
setup(width=W, height=H)
anim = Animation(fps=10.0, loop=0)


def trim_polyline(
    pts: list[tuple[float, float]],
    frac: float,
) -> list[tuple[float, float]]:
    """Interpolate a prefix polyline covering `frac` (0..1) of total arc length."""
    if len(pts) < 2 or frac >= 1.0:
        return list(pts)
    segs: list[tuple[tuple[float, float], tuple[float, float], float]] = []
    total = 0.0
    for idx in range(len(pts) - 1):
        p0, p1 = pts[idx], pts[idx + 1]
        seg_len = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
        segs.append((p0, p1, seg_len))
        total += seg_len
    if total <= 1e-6:
        return [pts[0], pts[-1]]
    target = max(0.0, min(1.0, frac)) * total
    out = [pts[0]]
    acc = 0.0
    for p0, p1, seg_len in segs:
        if acc + seg_len >= target and seg_len > 1e-6:
            t = (target - acc) / seg_len
            out.append((p0[0] + t * (p1[0] - p0[0]), p0[1] + t * (p1[1] - p0[1])))
            break
        out.append(p1)
        acc += seg_len
    return out


STEM_STYLE = Styles.DarkBold.patch(line_width=1.6, line_arrow_head_scale=11.0)
STEM_PRIMARY = Styles.PrimaryBold.patch(line_width=1.6, line_arrow_head_scale=11.0)


def draw_stem(
    pts: list[tuple[float, float]],
    frac: float,
    style: Style = STEM_STYLE,
    bud_style: Style = Styles.PrimaryFlat,
) -> None:
    """Draw either a partial sprouting stem with a bud tip or a completed arrow."""
    if frac <= 0.0 or len(pts) < 2:
        return
    if frac >= 1.0:
        lines(pts, arrow_head="->", style=style)
    else:
        sub = trim_polyline(pts, frac)
        if len(sub) >= 2:
            lines(sub, style=style)
            circle(sub[-1], radius=0.48, style=bud_style)


# =========================================================================
# 1. Pre-Solve All 5 Topologies Using Real drawlib.graph Solvers
# =========================================================================

# (A) ArchitectureGraph: 5-Zone Compass + Nested VPC (app, data)
g_arch = ArchitectureGraph(
    direction="LR",
    container_sep=3.2,
    default_node_width=9.6,
    default_node_height=5.8,
)
g_arch.cluster("top_z", ["iam"], pos="top", padding=1.0, header_height=0.4)
g_arch.cluster("left_z", ["waf"], pos="left", padding=1.0, header_height=0.4)
g_arch.group("vpc", pos="center", padding=1.5, header_height=4.4)
g_arch.cluster("app", ["api"], parent="vpc", order=1, padding=1.1, header_height=0.5)
g_arch.cluster("data", ["db"], parent="vpc", order=2, padding=1.1, header_height=0.5)
g_arch.cluster("right_z", ["dr"], pos="right", padding=1.0, header_height=0.4)
g_arch.cluster("bot_z", ["log"], pos="bottom", padding=1.0, header_height=0.4)
g_arch.edge("waf", "api")
g_arch.edge("api", "db")
g_arch.edge("iam", "api")
g_arch.edge("db", "dr")
g_arch.edge("api", "log")
raw_arch = g_arch.get_layout(width=68.0, height=44.0, margin=1.5)

a_min_x = min(c.left for c in raw_arch.clusters.values())
a_max_x = max(c.right for c in raw_arch.clusters.values())
a_min_y = min(c.bottom for c in raw_arch.clusters.values())
a_max_y = max(c.top for c in raw_arch.clusters.values())
a_cx_raw = (a_min_x + a_max_x) / 2.0
a_cy_raw = (a_min_y + a_max_y) / 2.0
ARCH_VP_CX, ARCH_VP_CY = 24.0, 61.75
ARCH_S = min(37.4 / (a_max_x - a_min_x), 27.4 / (a_max_y - a_min_y))


def map_arch(pt: tuple[float, float]) -> tuple[float, float]:
    return (
        ARCH_VP_CX + (pt[0] - a_cx_raw) * ARCH_S,
        ARCH_VP_CY + (pt[1] - a_cy_raw) * ARCH_S,
    )


# (B) LayerGraph: 4-Rank DAG with Fan-Out & 3-into-1 Merge + Split
g_layer = LayerGraph(
    direction="LR",
    rank_sep=4.2,
    node_sep=2.7,
    default_node_width=5.4,
    default_node_height=3.5,
)
g_layer.edge("S1", "E1")
g_layer.edge("S1", "E2")
g_layer.edge("S2", "E2")
g_layer.edge("S2", "E3")
g_layer.edge("E1", "Join")
g_layer.edge("E2", "Join")
g_layer.edge("E3", "Join")
g_layer.edge("Join", "O1")
g_layer.edge("Join", "O2")
lay_layer = g_layer.get_layout(width=38.5, height=24.5, margin=1.8)
LAY_OX, LAY_OY = 68.0 - 38.5 / 2.0, 47.2


def map_layer(pt: tuple[float, float]) -> tuple[float, float]:
    return (LAY_OX + pt[0], LAY_OY + pt[1])


# (C) TreeGraph: Strict 1 -> 2 -> 4 Top-Down Hierarchy
g_tree = TreeGraph(
    root="Root",
    direction="TB",
    edge_routing="orthogonal",
    default_node_width=5.9,
    default_node_height=3.3,
    sibling_sep=1.9,
    level_sep=4.6,
)
g_tree.child("Root", "B1")
g_tree.child("Root", "B2")
g_tree.child("B1", "L1")
g_tree.child("B1", "L2")
g_tree.child("B2", "L3")
g_tree.child("B2", "L4")
lay_tree = g_tree.get_layout(width=33.6, height=27.5, margin=1.5)
TREE_OX, TREE_OY = 97.6, 48.0


def map_tree(pt: tuple[float, float]) -> tuple[float, float]:
    return (TREE_OX + pt[0], TREE_OY + pt[1])


# (D) RadialGraph: Hub -> 4 Ring-1 Spokes -> 8 Ring-2 Satellites
g_rad = RadialGraph(
    hub="Hub",
    radius_step=6.35,
    start_angle=45.0,
    default_node_width=4.2,
    default_node_height=2.8,
)
g_rad.node("Hub", width=3.25, height=3.25)
for sp_id in ["A", "B", "C", "D"]:
    g_rad.spoke("Hub", sp_id, ring=1, width=2.5, height=2.5)
for sp_id, sat_ids in [
    ("A", ["A1", "A2"]),
    ("B", ["B1", "B2"]),
    ("C", ["C1", "C2"]),
    ("D", ["D1", "D2"]),
]:
    for sat_id in sat_ids:
        g_rad.spoke(sp_id, sat_id, ring=2, width=4.2, height=2.75)
lay_rad = g_rad.get_layout(width=30.0, height=28.5, margin=1.5)
RAD_OX, RAD_OY = 35.0 - 15.0, 19.05 - 14.25


def map_rad(pt: tuple[float, float]) -> tuple[float, float]:
    return (RAD_OX + pt[0], RAD_OY + pt[1])


# (E) GridGraph: 3x2 Matrix + Smart Inter-Row Corridor Highway
g_grid = GridGraph(
    columns=3,
    rows=2,
    edge_routing="smart",
    default_node_width=11.4,
    default_node_height=5.0,
)
for r_i in range(2):
    for c_i in range(3):
        g_grid.cell(f"{r_i},{c_i}", row=r_i, col=c_i)
g_grid.edge("0,0", "0,1")
g_grid.edge("0,1", "0,2")
g_grid.edge("0,0", "1,0")
g_grid.edge("1,0", "1,1")
g_grid.edge("1,1", "1,2")
g_grid.edge("0,0", "1,2")
lay_grid = g_grid.get_layout(width=52.0, height=23.2, margin=2.0)
GRID_OX, GRID_OY = 77.2, 4.9


def map_grid(pt: tuple[float, float]) -> tuple[float, float]:
    return (GRID_OX + pt[0], GRID_OY + pt[1])


# =========================================================================
# 2. Shared Banner & 5-Card Chrome Helpers
# =========================================================================

STAGE_LABELS = [
    "1. Seed Anchor",
    "2. Inner Growth",
    "3. Outer Structure",
    "4. Cross Routing",
    "5. Full Topologies",
]

GUIDE_DASH = Styles.MutedDashed.patch(
    line_color=(194, 206, 222),
    line_width=0.85,
    shape_line_color=(198, 210, 226),
    shape_line_width=0.85,
    shape_fill_color=(0, 0, 0, 0),
)
GUIDE_TXT = Styles.MutedBold.patch(text_size=9.5)
PULSE_RING = Styles.PrimaryDashed.patch(shape_fill_color=(0, 0, 0, 0), shape_line_width=1.2)


def draw_banner(active_stage: int) -> None:
    """Draw top 5-stage connected growth progress banner."""
    pill_w, pill_h, gap = 24.4, 5.2, 2.0
    start_x = 3.0 + pill_w / 2.0
    cy = 91.2
    for idx, label in enumerate(STAGE_LABELS, start=1):
        cx = start_x + (idx - 1) * (pill_w + gap)
        if idx > 1:
            prev_cx = cx - (pill_w + gap)
            line(
                (prev_cx + pill_w / 2.0 + 0.15, cy),
                (cx - pill_w / 2.0 - 0.15, cy),
                style=Styles.PrimaryBold if idx <= active_stage else Styles.MutedThin,
            )
        if idx == active_stage:
            st = Styles.PrimaryFlat.patch(shape_r=1.3)
            tst = Styles.WhiteBold.patch(text_size=9.9)
        elif idx < active_stage:
            st = Styles.PrimaryNeutral.patch(shape_r=1.3, shape_line_width=1.1)
            tst = Styles.PrimaryBold.patch(text_size=9.9)
        else:
            st = Styles.Neutral.patch(shape_r=1.3, shape_line_width=1.1)
            tst = Styles.MutedBold.patch(text_size=9.9)
        rectangle((cx, cy), width=pill_w, height=pill_h, style=st, text=label, text_style=tst)


def draw_card_shell(
    cx: float,
    cy: float,
    cw: float,
    ch: float,
    title: str,
    subtitle: str,
    icon_fn: object,
    hdr_style: Style,
    icon_style: Style,
) -> tuple[float, float, float, float]:
    """Draw card container, header bar with title + rule subtitle, and white inner viewport."""
    rectangle(
        (cx, cy),
        width=cw,
        height=ch,
        style=Styles.Neutral.patch(shape_r=2.0, shape_line_width=1.2),
    )
    top_y = cy + ch / 2.0
    bot_y = cy - ch / 2.0
    hdr_h = 6.6
    hdr_cy = top_y - 0.65 - hdr_h / 2.0
    hdr_w = cw - 1.6
    rectangle((cx, hdr_cy), width=hdr_w, height=hdr_h, style=hdr_style.patch(shape_r=1.4))

    ix = cx - hdr_w / 2.0 + 3.2
    icon_fn((ix, hdr_cy), width=3.8, style=icon_style)  # type: ignore[operator]
    tx = ix + 2.8
    text(
        (tx, hdr_cy + 1.35),
        title,
        style=Styles.DarkBold.patch(text_size=10.2, halign="left"),
    )
    text(
        (tx, hdr_cy - 1.45),
        subtitle,
        style=Styles.Dark.patch(text_size=9.5, halign="left"),
    )

    vp_top = hdr_cy - hdr_h / 2.0 - 0.55
    vp_bot = bot_y + 0.85
    vp_h = vp_top - vp_bot
    vp_cy = (vp_top + vp_bot) / 2.0
    vp_w = cw - 2.2
    rectangle(
        (cx, vp_cy),
        width=vp_w,
        height=vp_h,
        style=Styles.White.patch(
            shape_r=1.2,
            shape_line_color=(206, 216, 230),
            shape_line_width=1.0,
        ),
    )
    return cx, vp_cy, vp_w, vp_h


# =========================================================================
# 3. Per-Card Coordinate Guides & Sprouting Renderers (Frames 0..7)
# =========================================================================


def render_arch_card(f_idx: int) -> None:
    """Card 1: ArchitectureGraph (5-Zone Compass + Nested VPC)."""
    draw_card_shell(
        24.0,
        65.5,
        42.0,
        39.5,
        "ArchitectureGraph",
        "5-Zone Compass & Nested VPC",
        phosphor.cloud,
        Styles.PrimaryNeutral,
        Styles.PrimaryBold,
    )
    # Faint 5-zone compass crosshairs & blueprint zone slots
    line((6.0, ARCH_VP_CY), (42.0, ARCH_VP_CY), style=GUIDE_DASH)
    line((ARCH_VP_CX, 48.0), (ARCH_VP_CX, 75.5), style=GUIDE_DASH)
    for cid in ["top_z", "left_z", "vpc", "right_z", "bot_z"]:
        cl = raw_arch.clusters[cid]
        rectangle(
            map_arch(cl.xy),
            width=cl.width * ARCH_S,
            height=cl.height * ARCH_S,
            style=GUIDE_DASH.patch(shape_r=0.9),
        )
    c_top = raw_arch.clusters["top_z"]
    c_bot = raw_arch.clusters["bot_z"]
    c_left = raw_arch.clusters["left_z"]
    c_right = raw_arch.clusters["right_z"]
    text((map_arch(c_top.xy)[0] + 6.4, map_arch(c_top.xy)[1]), "top", style=GUIDE_TXT)
    text((map_arch(c_bot.xy)[0] + 6.8, map_arch(c_bot.xy)[1]), "bot", style=GUIDE_TXT)
    text((map_arch(c_left.xy)[0], map_arch(c_left.xy)[1] + 4.3), "left", style=GUIDE_TXT)
    text((map_arch(c_right.xy)[0], map_arch(c_right.xy)[1] + 4.3), "right", style=GUIDE_TXT)

    # Stage 1+: Center VPC macro shell
    c_vpc = raw_arch.clusters["vpc"]
    vpc_xy = map_arch(c_vpc.xy)
    vpc_w, vpc_h = c_vpc.width * ARCH_S, c_vpc.height * ARCH_S
    vpc_st = (
        Styles.PrimaryNeutral.patch(shape_r=1.0, shape_line_width=1.5)
        if f_idx == 0
        else Styles.Neutral.patch(shape_r=1.0, shape_line_width=1.15)
    )
    rectangle(vpc_xy, width=vpc_w, height=vpc_h, style=vpc_st)
    text(
        (vpc_xy[0] + vpc_w / 2.0 - 0.95, vpc_xy[1] + vpc_h / 2.0 - 1.5),
        "VPC",
        style=Styles.DarkBold.patch(text_size=9.5, halign="right"),
    )
    if f_idx == 0:
        rectangle(vpc_xy, width=vpc_w + 1.3, height=vpc_h + 1.3, style=PULSE_RING.patch(shape_r=1.2))

    # Stage 2+: Nested App & Data subnets + internal stem api -> db
    e_map = {(e.src, e.dst): [map_arch(p) for p in e.points] for e in raw_arch.edges}
    if f_idx >= 1:
        for sub_id, sub_st in [("app", Styles.PrimaryNeutral), ("data", Styles.SecondaryNeutral)]:
            cs = raw_arch.clusters[sub_id]
            rectangle(
                map_arch(cs.xy),
                width=cs.width * ARCH_S,
                height=cs.height * ARCH_S,
                style=(GUIDE_DASH if f_idx == 1 else sub_st).patch(shape_r=0.8),
            )
        draw_stem(e_map[("api", "db")], 0.55 if f_idx == 1 else 1.0, STEM_STYLE)

    if f_idx >= 2:
        for nid, lbl, is_hero in [("api", "API", True), ("db", "DB", False)]:
            nl = raw_arch.nodes[nid]
            nst = Styles.PrimaryFlat if is_hero else Styles.White
            ntxt = Styles.WhiteBold.patch(text_size=9.5) if is_hero else Styles.DarkBold.patch(text_size=9.5)
            rectangle(
                map_arch(nl.xy),
                width=nl.width * ARCH_S,
                height=nl.height * ARCH_S,
                style=nst.patch(shape_r=0.7),
                text=lbl,
                text_style=ntxt,
            )

    # Stage 3+: 4 peripheral compass zones sprout around VPC
    if f_idx >= 3:
        for zid in ["top_z", "left_z", "right_z", "bot_z"]:
            cz = raw_arch.clusters[zid]
            zst = GUIDE_DASH if f_idx == 3 else Styles.Neutral.patch(shape_r=0.9, shape_line_width=1.05)
            rectangle(map_arch(cz.xy), width=cz.width * ARCH_S, height=cz.height * ARCH_S, style=zst)

    # Stage 4+: Cross-boundary compass edges snake across zone gaps
    if f_idx >= 5:
        c_frac = 0.55 if f_idx == 5 else 1.0
        draw_stem(e_map[("waf", "api")], c_frac, STEM_STYLE)
        draw_stem(e_map[("db", "dr")], c_frac, STEM_STYLE)
        draw_stem(e_map[("iam", "api")], c_frac, STEM_PRIMARY)
        draw_stem(e_map[("api", "log")], c_frac, STEM_PRIMARY)

    if f_idx >= 4:
        for nid, lbl in [("iam", "IAM"), ("waf", "WAF"), ("dr", "DR"), ("log", "Log")]:
            nl = raw_arch.nodes[nid]
            hi = f_idx == 4
            nst = Styles.PrimaryNeutral if hi else Styles.White
            rectangle(
                map_arch(nl.xy),
                width=nl.width * ARCH_S,
                height=nl.height * ARCH_S,
                style=nst.patch(shape_r=0.7),
                text=lbl,
                text_style=Styles.DarkBold.patch(text_size=9.5),
            )


def render_layer_card(f_idx: int) -> None:
    """Card 2: LayerGraph (4-Rank DAG with Fan-Out & 3-into-1 Merge)."""
    draw_card_shell(
        68.0,
        65.5,
        42.0,
        39.5,
        "LayerGraph",
        "Ranked DAG (Fan-Out & Merge)",
        phosphor.git_merge,
        Styles.SecondaryNeutral,
        Styles.SecondaryBold,
    )
    rank_reps = [("R0", "S1"), ("R1", "E1"), ("R2", "Join"), ("R3", "O1")]
    for r_lbl, rep_id in rank_reps:
        rx = map_layer(lay_layer.nodes[rep_id].xy)[0]
        line((rx, 48.6), (rx, 71.6), style=GUIDE_DASH)
        text((rx, 73.7), r_lbl, style=GUIDE_TXT)

    e_map = {(e.src, e.dst): [map_layer(p) for p in e.points] for e in lay_layer.edges}

    # Stems by stage
    if f_idx >= 1:
        f1 = 0.55 if f_idx == 1 else 1.0
        for pair in [("S1", "E1"), ("S1", "E2"), ("S2", "E2"), ("S2", "E3")]:
            draw_stem(e_map[pair], f1, STEM_STYLE)
    if f_idx >= 3:
        f2 = 0.55 if f_idx == 3 else 1.0
        for pair in [("E1", "Join"), ("E2", "Join"), ("E3", "Join")]:
            draw_stem(e_map[pair], f2, STEM_PRIMARY if f_idx in {3, 4} else STEM_STYLE)
    if f_idx >= 5:
        f3 = 0.55 if f_idx == 5 else 1.0
        for pair in [("Join", "O1"), ("Join", "O2")]:
            draw_stem(e_map[pair], f3, STEM_STYLE)

    def draw_lnode(nid: str, st: Style, tst: Style, pulse: bool = False) -> None:
        nl = lay_layer.nodes[nid]
        cxy = map_layer(nl.xy)
        rectangle(cxy, width=nl.width, height=nl.height, style=st.patch(shape_r=0.8), text=nid, text_style=tst)
        if pulse:
            rectangle(cxy, width=nl.width + 1.2, height=nl.height + 1.2, style=PULSE_RING.patch(shape_r=1.0))

    dark_t = Styles.DarkBold.patch(text_size=9.5)
    white_t = Styles.WhiteBold.patch(text_size=9.5)

    # R0 seeds (Frame 0+)
    r0_st = Styles.PrimaryFlat if f_idx == 0 else Styles.White
    r0_t = white_t if f_idx == 0 else dark_t
    for nid in ["S1", "S2"]:
        draw_lnode(nid, r0_st, r0_t, pulse=(f_idx == 0))

    # R1 fan-out column (Frame 2+)
    if f_idx >= 2:
        for nid in ["E1", "E2", "E3"]:
            st = Styles.PrimaryNeutral if nid == "E2" or f_idx == 2 else Styles.Neutral
            draw_lnode(nid, st, dark_t)

    # R2 3-into-1 DAG merge focal node (Frame 4+)
    if f_idx >= 4:
        draw_lnode("Join", Styles.PrimaryFlat, white_t, pulse=(f_idx == 4))

    # R3 output split (Frame 6+)
    if f_idx >= 6:
        for nid in ["O1", "O2"]:
            draw_lnode(nid, Styles.SecondaryNeutral, dark_t)


def render_tree_card(f_idx: int) -> None:
    """Card 3: TreeGraph (1 -> 2 -> 4 Symmetric Buchheim Hierarchy)."""
    draw_card_shell(
        112.0,
        65.5,
        42.0,
        39.5,
        "TreeGraph",
        "1 -> 2 -> 4 Strict Hierarchy",
        phosphor.tree_structure,
        Styles.PrimaryNeutral,
        Styles.PrimaryBold,
    )
    for d_lbl, rep_id in [("d0", "Root"), ("d1", "B1"), ("d2", "L1")]:
        dy = map_tree(lay_tree.nodes[rep_id].xy)[1]
        line((98.2, dy), (130.6, dy), style=GUIDE_DASH)
        text((95.4, dy), d_lbl, style=GUIDE_TXT)

    e_map = {(e.src, e.dst): [map_tree(p) for p in e.points] for e in lay_tree.edges}
    if f_idx >= 1:
        f1 = 0.55 if f_idx == 1 else 1.0
        for pair in [("Root", "B1"), ("Root", "B2")]:
            draw_stem(e_map[pair], f1, STEM_STYLE)
    if f_idx >= 3:
        f2 = 0.55 if f_idx == 3 else 1.0
        for pair in [("B1", "L1"), ("B1", "L2"), ("B2", "L3"), ("B2", "L4")]:
            draw_stem(e_map[pair], f2, STEM_STYLE)

    dark_t = Styles.DarkBold.patch(text_size=9.5)
    white_t = Styles.WhiteBold.patch(text_size=9.5)

    # d0 Root (Frame 0+)
    nl_r = lay_tree.nodes["Root"]
    r_xy = map_tree(nl_r.xy)
    rectangle(
        r_xy,
        width=nl_r.width,
        height=nl_r.height,
        style=Styles.PrimaryFlat.patch(shape_r=0.8),
        text="Root",
        text_style=white_t,
    )
    if f_idx == 0:
        rectangle(r_xy, width=nl_r.width + 1.2, height=nl_r.height + 1.2, style=PULSE_RING.patch(shape_r=1.0))

    # d1 Branches (Frame 2+)
    if f_idx >= 2:
        for nid in ["B1", "B2"]:
            nl = lay_tree.nodes[nid]
            rectangle(
                map_tree(nl.xy),
                width=nl.width,
                height=nl.height,
                style=Styles.PrimaryNeutral.patch(shape_r=0.8),
                text=nid,
                text_style=dark_t,
            )

    # d2 Leaves (Frame 4+)
    if f_idx >= 4:
        for idx_l, nid in enumerate(["L1", "L2", "L3", "L4"]):
            nl = lay_tree.nodes[nid]
            st = Styles.SecondaryNeutral if idx_l % 2 == 0 else Styles.White
            rectangle(
                map_tree(nl.xy),
                width=nl.width,
                height=nl.height,
                style=st.patch(shape_r=0.8),
                text=nid,
                text_style=dark_t,
            )


def render_radial_card(f_idx: int) -> None:
    """Card 4: RadialGraph (Concentric Orbit Rings r=0, r=1, r=2)."""
    draw_card_shell(
        35.0,
        22.8,
        64.0,
        40.5,
        "RadialGraph",
        "360 deg Concentric Orbit Rings",
        phosphor.circles_three_plus,
        Styles.PrimaryNeutral,
        Styles.PrimaryBold,
    )
    hub_xy = map_rad(lay_rad.nodes["Hub"].xy)
    r1 = lay_rad.ring_radii[1]
    r2 = lay_rad.ring_radii[2]

    # Always-visible concentric orbit guides from layout.ring_radii
    circle(hub_xy, radius=r1, style=GUIDE_DASH)
    circle(hub_xy, radius=r2, style=GUIDE_DASH)
    line((hub_xy[0] - r2 - 1.2, hub_xy[1]), (hub_xy[0] + r2 + 1.2, hub_xy[1]), style=GUIDE_DASH)
    line((hub_xy[0], hub_xy[1] - r2 - 1.2), (hub_xy[0], hub_xy[1] + r2 + 1.2), style=GUIDE_DASH)

    # Left flank ring-tier tracker pills + Right flank polar geometry tags
    ring_badges = [
        (25.8, "r=0  Hub", f_idx >= 0, f_idx == 0),
        (19.05, "r=1  (4)", f_idx >= 2, f_idx in {1, 2}),
        (12.3, "r=2  (8)", f_idx >= 4, f_idx in {3, 4}),
    ]
    for by, b_lbl, done, active in ring_badges:
        if active:
            bst = Styles.PrimaryFlat.patch(shape_r=1.1)
            btst = Styles.WhiteBold.patch(text_size=9.5)
        elif done:
            bst = Styles.PrimaryNeutral.patch(shape_r=1.1, shape_line_width=1.0)
            btst = Styles.PrimaryBold.patch(text_size=9.5)
        else:
            bst = Styles.Neutral.patch(shape_r=1.1, shape_line_width=1.0)
            btst = Styles.Muted.patch(text_size=9.5)
        rectangle((12.4, by), width=13.2, height=4.4, style=bst, text=b_lbl, text_style=btst)

    rectangle(
        (57.6, 22.8),
        width=13.2,
        height=4.4,
        style=Styles.Neutral.patch(shape_r=1.1),
        text="360 deg",
        text_style=Styles.DarkBold.patch(text_size=9.5),
    )
    rectangle(
        (57.6, 15.3),
        width=13.2,
        height=4.4,
        style=Styles.SecondaryNeutral.patch(shape_r=1.1),
        text="ring_radii",
        text_style=Styles.DarkBold.patch(text_size=9.5),
    )

    e_map = {(e.src, e.dst): [map_rad(p) for p in e.points] for e in lay_rad.edges}
    if f_idx >= 1:
        f1 = 0.55 if f_idx == 1 else 1.0
        for sp_id in ["A", "B", "C", "D"]:
            draw_stem(e_map[("Hub", sp_id)], f1, STEM_STYLE)
    if f_idx >= 3:
        f2 = 0.55 if f_idx == 3 else 1.0
        for sp_id, sat_ids in [
            ("A", ["A1", "A2"]),
            ("B", ["B1", "B2"]),
            ("C", ["C1", "C2"]),
            ("D", ["D1", "D2"]),
        ]:
            for sat_id in sat_ids:
                draw_stem(e_map[(sp_id, sat_id)], f2, STEM_PRIMARY if f_idx in {3, 4} else STEM_STYLE)

    # r=0 Hub
    circle(
        hub_xy,
        radius=2.30,
        style=Styles.PrimaryFlat,
        text="Hub",
        text_style=Styles.WhiteBold.patch(text_size=9.5),
    )
    if f_idx == 0:
        circle(hub_xy, radius=2.95, style=PULSE_RING)

    # r=1 Inner spokes (Frame 2+)
    if f_idx >= 2:
        for sp_id in ["A", "B", "C", "D"]:
            circle(
                map_rad(lay_rad.nodes[sp_id].xy),
                radius=1.75,
                style=Styles.PrimaryNeutral,
                text=sp_id,
                text_style=Styles.DarkBold.patch(text_size=9.5),
            )

    # r=2 Outer satellites (Frame 4+)
    if f_idx >= 4:
        for idx_s, sat_id in enumerate(["A1", "A2", "B1", "B2", "C1", "C2", "D1", "D2"]):
            nl = lay_rad.nodes[sat_id]
            st = Styles.SecondaryNeutral if idx_s % 2 == 0 else Styles.White
            rectangle(
                map_rad(nl.xy),
                width=nl.width,
                height=nl.height,
                style=st.patch(shape_r=1.1),
                text=sat_id,
                text_style=Styles.DarkBold.patch(text_size=9.5),
            )


def render_grid_card(f_idx: int) -> None:
    """Card 5: GridGraph ((row, col) Matrix & Smart Inter-Row Corridor)."""
    draw_card_shell(
        101.0,
        22.8,
        64.0,
        40.5,
        "GridGraph",
        "(row, col) Matrix & Smart Channel",
        phosphor.grid_four,
        Styles.SecondaryNeutral,
        Styles.SecondaryBold,
    )
    # Faint matrix slot outlines & row/col index headers
    for c_i in range(3):
        cx_slot = map_grid(lay_grid.nodes[f"0,{c_i}"].xy)[0]
        text((cx_slot, 31.3), f"c{c_i}", style=GUIDE_TXT)
    for r_i in range(2):
        cy_slot = map_grid(lay_grid.nodes[f"{r_i},0"].xy)[1]
        text((74.2, cy_slot), f"r{r_i}", style=GUIDE_TXT)
    for r_i in range(2):
        for c_i in range(3):
            nl = lay_grid.nodes[f"{r_i},{c_i}"]
            rectangle(
                map_grid(nl.xy),
                width=nl.width,
                height=nl.height,
                style=GUIDE_DASH.patch(shape_r=0.9),
            )

    # Faint smart corridor lane between r0 and r1
    corridor_y = (map_grid(lay_grid.nodes["0,0"].xy)[1] + map_grid(lay_grid.nodes["1,0"].xy)[1]) / 2.0
    line((78.0, corridor_y), (129.0, corridor_y), style=GUIDE_DASH)

    e_map = {(e.src, e.dst): [map_grid(p) for p in e.points] for e in lay_grid.edges}

    # Orthogonal neighbor stems
    if f_idx >= 1:
        f1 = 0.55 if f_idx == 1 else 1.0
        draw_stem(e_map[("0,0", "0,1")], f1, STEM_STYLE)
        draw_stem(e_map[("0,0", "1,0")], f1, STEM_STYLE)
    if f_idx >= 2:
        draw_stem(e_map[("0,1", "0,2")], 1.0, STEM_STYLE)
    if f_idx >= 3:
        f2 = 0.55 if f_idx == 3 else 1.0
        draw_stem(e_map[("1,0", "1,1")], f2, STEM_STYLE)
    if f_idx >= 4:
        draw_stem(e_map[("1,1", "1,2")], 1.0, STEM_STYLE)

    # Stage 4+: Smart corridor cross-edge (0,0) -> (1,2)
    if f_idx >= 5:
        fc = 0.55 if f_idx == 5 else 1.0
        draw_stem(e_map[("0,0", "1,2")], fc, STEM_PRIMARY.patch(line_width=1.8))
    if f_idx >= 6:
        text(
            (103.2, corridor_y + 1.85),
            "smart channel",
            style=Styles.PrimaryBold.patch(text_size=9.5),
        )

    def draw_cell(cid: str, st: Style, tst: Style, pulse: bool = False) -> None:
        nl = lay_grid.nodes[cid]
        cxy = map_grid(nl.xy)
        rectangle(cxy, width=nl.width, height=nl.height, style=st.patch(shape_r=0.9), text=f"({cid})", text_style=tst)
        if pulse:
            rectangle(cxy, width=nl.width + 1.3, height=nl.height + 1.3, style=PULSE_RING.patch(shape_r=1.1))

    dark_t = Styles.DarkBold.patch(text_size=9.6)
    white_t = Styles.WhiteBold.patch(text_size=9.6)

    # Seed (0,0)
    draw_cell("0,0", Styles.PrimaryFlat, white_t, pulse=(f_idx == 0))

    # Stage 2 neighbors: (0,1), (0,2), (1,0)
    if f_idx >= 2:
        draw_cell("0,1", Styles.PrimaryNeutral, dark_t)
        draw_cell("0,2", Styles.PrimaryNeutral, dark_t)
        draw_cell("1,0", Styles.White, dark_t)

    # Stage 3 remaining matrix cells: (1,1), (1,2)
    if f_idx >= 4:
        draw_cell("1,1", Styles.White, dark_t)
        c12_st = Styles.PrimaryNeutral if f_idx >= 6 else Styles.SecondaryNeutral
        draw_cell("1,2", c12_st, dark_t, pulse=(f_idx == 6))


# =========================================================================
# 4. Capture 8 Organic Sprouting Frames + 4.2s Comparison Hold
# =========================================================================

FRAME_SPECS = [
    (0, 0.85, 1),  # Frame 0: Seed anchors appear
    (1, 0.45, 2),  # Frame 1: First sprout stems (55%)
    (2, 0.85, 2),  # Frame 2: Inner tier blooms (100% + Stage-2 nodes)
    (3, 0.45, 3),  # Frame 3: Second sprout stems (55%)
    (4, 0.85, 3),  # Frame 4: Outer structure blooms
    (5, 0.50, 4),  # Frame 5: Cross-zone & smart corridor stems (55%)
    (6, 0.95, 4),  # Frame 6: Cross-zone & smart corridor complete (100%)
    (7, 4.20, 5),  # Frame 7: Settled full-overview comparison hold
]

for frame_idx, dur_sec, banner_stage in FRAME_SPECS:
    with anim.frame(duration=dur_sec):
        draw_banner(banner_stage)
        render_arch_card(frame_idx)
        render_layer_card(frame_idx)
        render_tree_card(frame_idx)
        render_radial_card(frame_idx)
        render_grid_card(frame_idx)

save()
