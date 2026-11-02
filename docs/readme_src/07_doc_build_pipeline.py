# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Animated i18n-native documentation & slide build lifecycle (APNG)."""

from __future__ import annotations

from drawlib.anim import Animation
from drawlib.canvas import save, setup
from drawlib.icons import ai, code, devops, phosphor, workspace
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.styles import Styles
from drawlib.text import text

W, H = 138.0, 82.0
setup(width=138, height=82)
anim = Animation(fps=10.0, loop=0)

# Shared styles
PANE_BG = Styles.Neutral.patch(
    shape_fill_color=(250, 252, 255),
    shape_line_width=0,
    shape_r=1.8,
)
PANE_HEADER_TOP = Styles.Neutral.patch(
    shape_fill_color=(238, 243, 250),
    shape_line_width=0,
    shape_r=1.8,
)
PANE_HEADER_FLAT = Styles.Neutral.patch(
    shape_fill_color=(238, 243, 250),
    shape_line_width=0,
    shape_r=0.0,
)
PANE_BORDER = Styles.Neutral.patch(
    shape_fill_color=(0, 0, 0, 0),
    shape_line_color=(203, 213, 225),
    shape_line_width=1.2,
    shape_r=1.8,
)
SUBPANEL_BG = Styles.Neutral.patch(
    shape_fill_color=(243, 246, 252),
    shape_line_color=(214, 223, 236),
    shape_line_width=1.0,
    shape_r=1.4,
)
ROW_ACTIVE = Styles.PrimaryNeutral.patch(
    shape_fill_color=(232, 242, 255),
    shape_line_color=(59, 130, 246),
    shape_line_width=1.3,
    shape_r=1.0,
)
ROW_USER = Styles.Neutral.patch(
    shape_fill_color=(241, 245, 251),
    shape_line_color=(51, 65, 85),
    shape_line_width=1.4,
    shape_r=1.0,
)
ROW_OPTIONAL = Styles.PrimaryDashed.patch(
    shape_fill_color=(242, 247, 255),
    shape_line_color=(59, 130, 246),
    shape_line_width=1.2,
    shape_r=1.0,
)
ROW_OPTIONAL_DONE = Styles.MutedDashed.patch(
    shape_fill_color=(255, 255, 255),
    shape_line_color=(196, 208, 224),
    shape_line_width=1.0,
    shape_r=1.0,
)
ROW_OUTPUT = Styles.SecondaryNeutral.patch(
    shape_fill_color=(236, 250, 244),
    shape_line_color=(34, 160, 107),
    shape_line_width=1.2,
    shape_r=1.0,
)
ROW_DONE = Styles.Neutral.patch(
    shape_fill_color=(255, 255, 255),
    shape_line_color=(218, 226, 238),
    shape_line_width=1.0,
    shape_r=1.0,
)


def draw_pane_shell(cx: float, width: float) -> None:
    """Draw a rounded pane container with a seamlessly rounded top header bar."""
    rectangle((cx, 36.75), width=width, height=65.5, style=PANE_BG)
    rectangle((cx, 66.25), width=width, height=6.5, style=PANE_HEADER_TOP)
    rectangle((cx, 64.60), width=width, height=3.2, style=PANE_HEADER_FLAT)
    line(
        (cx - width / 2.0, 63.0),
        (cx + width / 2.0, 63.0),
        style=Styles.Neutral.patch(line_color=(203, 213, 225), line_width=1.2),
    )
    rectangle((cx, 36.75), width=width, height=65.5, style=PANE_BORDER)


def draw_user_avatar(xy: tuple[float, float], radius: float = 4.3) -> None:
    """Draw circular User (Developer) avatar badge."""
    circle(
        xy,
        radius=radius,
        style=Styles.Neutral.patch(
            shape_fill_color=(241, 245, 250),
            shape_line_color=(51, 65, 85),
            shape_line_width=1.6,
        ),
    )
    phosphor.user(xy, width=radius * 1.25, style=Styles.DarkBold)


def draw_gemini_avatar(xy: tuple[float, float], radius: float = 4.3) -> None:
    """Draw circular Gemini AI Agent avatar badge."""
    circle(
        xy,
        radius=radius,
        style=Styles.Neutral.patch(
            shape_fill_color=(248, 250, 255),
            shape_line_color=(59, 130, 246),
            shape_line_width=1.5,
        ),
    )
    ai.gemini(xy, width=radius * 1.42, style=Styles.Neutral)


def draw_scene_init_patterns(highlight_doc: bool) -> None:
    """Scene 1: Show 4 drawlib init project archetypes and select 'doc'."""
    text(
        (69.0, 76.2),
        "Project Scaffolding Patterns — drawlib init project <type>",
        style=Styles.DarkBold.patch(text_size=13.5),
    )
    sub_msg = (
        "2. Sample walkthrough: Linear Document (drawlib init project doc)"
        if highlight_doc
        else "1. Choose from 4 starter project archetypes"
    )
    sub_st = (
        Styles.PrimaryBold.patch(text_size=11.0)
        if highlight_doc
        else Styles.Dark.patch(text_size=11.0)
    )
    text((69.0, 71.0), sub_msg, style=sub_st)

    cards = [
        (
            37.5,
            51.5,
            "doc",
            "drawlib init project doc",
            "Linear Document / Spec / RFC",
            "Out: doc_html/<lang>/, doc_<lang>.pdf/.docx",
            phosphor.file_pdf,
        ),
        (
            100.5,
            51.5,
            "site",
            "drawlib init project site",
            "Multi-Page Docs Website",
            "Out: docs_html/<lang>/, docs_markdown/",
            phosphor.globe,
        ),
        (
            37.5,
            21.5,
            "slide",
            "drawlib init project slide",
            "16:9 Presentation Deck",
            "Out: slide_html/<lang>/, slide_<lang>.pdf/.pptx",
            phosphor.presentation_chart,
        ),
        (
            100.5,
            21.5,
            "images",
            "drawlib init project images",
            "Standalone Python Scripts",
            "Out: images/*.png, *.svg, *.webp",
            phosphor.images,
        ),
    ]

    for cx, cy, key, cmd_title, line1, line2, icon_fn in cards:
        is_selected = highlight_doc and key == "doc"
        is_dimmed = highlight_doc and key != "doc"

        if is_selected:
            card_st = Styles.PrimaryNeutral.patch(
                shape_fill_color=(242, 247, 255),
                shape_line_color=(37, 99, 235),
                shape_line_width=2.2,
                shape_r=2.0,
            )
            hdr_st = Styles.PrimaryFlat.patch(shape_r=1.2)
            hdr_txt = Styles.WhiteBold.patch(text_size=11.5)
            icon_st = Styles.PrimaryBold
            l1_st = Styles.DarkBold.patch(text_size=11.0, halign="left")
            l2_st = Styles.Dark.patch(text_size=9.8, halign="left")
        elif is_dimmed:
            card_st = Styles.Neutral.patch(
                shape_fill_color=(248, 250, 252),
                shape_line_color=(226, 232, 240),
                shape_line_width=1.0,
                shape_r=2.0,
            )
            hdr_st = Styles.Neutral.patch(
                shape_fill_color=(238, 242, 247),
                shape_line_width=0,
                shape_r=1.2,
            )
            hdr_txt = Styles.MutedBold.patch(text_size=11.2)
            icon_st = Styles.Muted
            l1_st = Styles.MutedBold.patch(text_size=10.8, halign="left")
            l2_st = Styles.Muted.patch(text_size=9.7, halign="left")
        else:
            card_st = Styles.Neutral.patch(
                shape_fill_color=(250, 252, 255),
                shape_line_color=(203, 213, 225),
                shape_line_width=1.3,
                shape_r=2.0,
            )
            hdr_st = Styles.Neutral.patch(
                shape_fill_color=(236, 242, 250),
                shape_line_color=(196, 209, 228),
                shape_line_width=1.1,
                shape_r=1.2,
            )
            hdr_txt = Styles.DarkBold.patch(text_size=11.2)
            icon_st = Styles.Primary
            l1_st = Styles.DarkBold.patch(text_size=10.8, halign="left")
            l2_st = Styles.Dark.patch(text_size=9.7, halign="left")

        rectangle((cx, cy), width=59.0, height=25.0, style=card_st)
        rectangle(
            (cx, cy + 8.3),
            width=55.0,
            height=5.6,
            style=hdr_st,
            text=cmd_title,
            text_style=hdr_txt,
        )
        icon_fn((cx - 21.5, cy - 2.2), width=5.8, style=icon_st)
        text((cx - 15.5, cy + 0.2), line1, style=l1_st)
        text((cx - 15.5, cy - 4.8), line2, style=l2_st)

        if is_selected:
            rectangle(
                (cx + 18.0, cy - 9.2),
                width=18.0,
                height=4.2,
                style=Styles.PrimaryFlat.patch(shape_r=1.0),
                text="Selected Sample",
                text_style=Styles.WhiteBold.patch(text_size=9.5),
            )


def draw_intertitle_one_day_later() -> None:
    """Scene 3: Clean time transition slide ('1 day later')."""
    rectangle(
        (69.0, 41.0),
        width=78.0,
        height=36.0,
        style=Styles.Neutral.patch(
            shape_fill_color=(248, 250, 255),
            shape_line_color=(196, 210, 230),
            shape_line_width=1.5,
            shape_r=2.5,
        ),
    )
    phosphor.clock((69.0, 50.5), width=7.2, style=Styles.Primary)
    text(
        (69.0, 40.5),
        "1 day later...",
        style=Styles.DarkBold.patch(text_size=17.0),
    )
    text(
        (69.0, 31.5),
        "Codebase evolves — update the specification incrementally",
        style=Styles.Dark.patch(text_size=10.8),
    )


def draw_actor_row_icon(
    actor_kind: str,
    xy: tuple[float, float],
    *,
    muted: bool = False,
) -> None:
    """Draw mini User or Gemini icon at the start of an operation row."""
    if actor_kind == "user":
        phosphor.user(
            xy,
            width=2.8,
            style=Styles.Muted if muted else Styles.DarkBold,
        )
    elif actor_kind == "user_git":
        phosphor.user(
            xy,
            width=2.8,
            style=Styles.Muted if muted else Styles.DarkBold,
        )
        devops.git((xy[0] + 2.8, xy[1]), width=2.6, style=Styles.Neutral)
    else:
        ai.gemini(xy, width=2.9, style=Styles.Neutral)


def draw_tree_icon(kind: str, xy: tuple[float, float], *, muted: bool = False) -> None:
    """Draw file or folder icon in the right-side directory tree."""
    if kind == "folder_open":
        phosphor.folder_open(
            xy,
            width=3.0,
            style=Styles.Muted if muted else Styles.PrimaryBold,
        )
    elif kind == "folder_out":
        phosphor.folder(
            xy,
            width=3.0,
            style=Styles.Muted if muted else Styles.SecondaryBold,
        )
    elif kind == "toml":
        phosphor.gear_six(
            xy,
            width=2.9,
            style=Styles.Muted if muted else Styles.PrimaryBold,
        )
    elif kind == "py":
        code.python(xy, width=2.8, style=Styles.Neutral)
    elif kind == "html":
        phosphor.file_html(
            xy,
            width=2.9,
            style=Styles.Muted if muted else Styles.Dark,
        )
    elif kind == "md":
        phosphor.file_text(
            xy,
            width=2.9,
            style=Styles.Muted if muted else Styles.Dark,
        )
    elif kind == "sh":
        phosphor.file_code(
            xy,
            width=2.9,
            style=Styles.Muted if muted else Styles.Dark,
        )
    elif kind == "globe":
        phosphor.globe(
            xy,
            width=2.9,
            style=Styles.Muted if muted else Styles.PrimaryBold,
        )
    elif kind == "pdf":
        phosphor.file_pdf(
            xy,
            width=2.9,
            style=Styles.Muted if muted else Styles.Danger,
        )
    elif kind == "word":
        workspace.word(xy, width=2.8, style=Styles.Neutral)


def draw_split_workspace(
    *,
    phase_badge: str,
    step_heading: str,
    actor: str,
    actor_title: str,
    actor_sub: str,
    actor_optional: bool,
    ops: list[tuple[str, str, str]],
    show_day2_note: bool,
    show_src: bool,
    show_outputs: bool,
    row_states: dict[str, tuple[str, str]],
    committed: bool,
    pulse_arrow: bool,
) -> None:
    """Draw split-screen workspace (Left: User & Gemini Actions, Right: Directory Tree).

    actor: 'user' or 'gemini'
    ops items: (actor_kind, label, state)
        actor_kind in {'user', 'user_git', 'gemini'}
        state in {'active_user', 'active_gemini', 'optional', 'optional_done', 'done'}
    row_states: mapping from tree item key to (state, badge_text)
        where state in {'new', 'active', 'optional', 'output', 'muted'}
    """
    # Top phase banner
    rectangle(
        (24.0, 75.8),
        width=40.0,
        height=5.8,
        style=Styles.PrimaryFlat.patch(shape_r=1.3),
        text=phase_badge,
        text_style=Styles.WhiteBold.patch(text_size=10.5),
    )
    text(
        (47.0, 75.8),
        step_heading,
        style=Styles.DarkBold.patch(text_size=11.2, halign="left"),
    )

    # =========================================================
    # Left Pane: User & Gemini Agent — Prompts & Commands
    # =========================================================
    draw_pane_shell(36.0, 64.0)
    phosphor.user((8.3, 66.25), width=3.4, style=Styles.DarkBold)
    ai.gemini((12.2, 66.25), width=3.7, style=Styles.Neutral)
    text(
        (15.4, 66.25),
        "User & Gemini — Prompts & Commands",
        style=Styles.DarkBold.patch(text_size=10.5, halign="left"),
    )

    # Prominent active actor avatar (User vs Gemini) + speech card
    if actor == "user":
        draw_user_avatar((10.8, 55.3), radius=4.2)
        bubble_st = ROW_USER
        title_st = Styles.DarkBold.patch(text_size=10.4, halign="left")
    else:
        draw_gemini_avatar((10.8, 55.3), radius=4.2)
        bubble_st = ROW_OPTIONAL if actor_optional else ROW_ACTIVE
        title_st = Styles.PrimaryBold.patch(text_size=10.4, halign="left")

    rectangle((41.5, 55.3), width=48.6, height=9.8, style=bubble_st)
    text((19.2, 57.3), actor_title, style=title_st)
    text(
        (19.2, 53.0),
        actor_sub,
        style=Styles.Dark.patch(text_size=9.8, halign="left"),
    )

    # Workflow log sub-panel (supports up to 8 steady rows)
    rectangle((36.0, 26.7), width=59.6, height=42.2, style=SUBPANEL_BG)
    phosphor.terminal_window((9.2, 45.2), width=3.1, style=Styles.Dark)
    text(
        (12.0, 45.2),
        "Workflow Steps",
        style=Styles.DarkBold.patch(text_size=9.8, halign="left"),
    )

    op_ys = [40.8, 36.2, 31.6, 27.0, 22.4, 17.8, 13.2, 8.6]
    for (akind, label, state), oy in zip(ops, op_ys):
        is_done_like = state in {"done", "optional_done"}
        if state == "active_user":
            ost = ROW_USER
            otxt = Styles.DarkBold.patch(text_size=9.8, halign="left")
        elif state == "active_gemini":
            ost = ROW_ACTIVE
            otxt = Styles.PrimaryBold.patch(text_size=9.8, halign="left")
        elif state == "optional":
            ost = ROW_OPTIONAL
            otxt = Styles.PrimaryBold.patch(text_size=9.8, halign="left")
        elif state == "optional_done":
            ost = ROW_OPTIONAL_DONE
            otxt = Styles.Dark.patch(text_size=9.6, halign="left")
        else:
            ost = ROW_DONE
            otxt = Styles.Dark.patch(text_size=9.6, halign="left")

        rectangle((36.0, oy), width=56.4, height=4.0, style=ost)
        draw_actor_row_icon(akind, (10.3, oy), muted=is_done_like)
        text((15.5 if akind == "user_git" else 12.8, oy), label, style=otxt)

        if state in {"optional", "optional_done"}:
            opt_pill_st = (
                Styles.PrimaryNeutral.patch(shape_r=0.8)
                if state == "optional"
                else Styles.Neutral.patch(
                    shape_fill_color=(244, 247, 252),
                    shape_line_color=(196, 208, 224),
                    shape_line_width=1.0,
                    shape_r=0.8,
                )
            )
            opt_txt_st = (
                Styles.PrimaryBold.patch(text_size=9.5)
                if state == "optional"
                else Styles.MutedBold.patch(text_size=9.5)
            )
            rectangle(
                (58.2, oy),
                width=10.4,
                height=3.2,
                style=opt_pill_st,
                text="Optional",
                text_style=opt_txt_st,
            )

    if show_day2_note:
        rectangle(
            (36.0, 12.0),
            width=55.6,
            height=7.4,
            style=Styles.Neutral.patch(
                shape_fill_color=(255, 255, 255),
                shape_line_color=(210, 220, 234),
                shape_line_width=1.0,
                shape_r=1.1,
            ),
        )
        text(
            (36.0, 13.7),
            "drawlib.toml, styles.py & template.html stay untouched",
            style=Styles.MutedBold.patch(text_size=9.5),
        )
        text(
            (36.0, 10.1),
            "Unchanged diagrams hit .drawlib/cache.db instantly",
            style=Styles.Muted.patch(text_size=9.5),
        )

    # Center connector arrow
    line(
        (68.4, 36.75),
        (71.6, 36.75),
        arrow_head="->",
        style=(
            Styles.PrimaryBold.patch(line_width=1.8)
            if pulse_arrow
            else Styles.MutedThin.patch(line_width=1.2)
        ),
    )

    # =========================================================
    # Right Pane: Project Directory Structure
    # =========================================================
    draw_pane_shell(103.0, 62.0)
    phosphor.folder_open((76.6, 66.25), width=3.8, style=Styles.PrimaryBold)
    text(
        (79.8, 66.25),
        "Directory Structure",
        style=Styles.DarkBold.patch(text_size=10.6, halign="left"),
    )

    if committed:
        rectangle(
            (123.2, 66.25),
            width=17.6,
            height=4.4,
            style=ROW_OUTPUT,
        )
        devops.git((116.8, 66.25), width=2.8, style=Styles.Neutral)
        text(
            (119.0, 66.25),
            "Committed",
            style=Styles.SecondaryBold.patch(text_size=9.5, halign="left"),
        )

    # Tree item definitions: (key, level, icon_kind, label)
    tree_items: list[tuple[str, int, str, str]] = [
        ("root", 0, "folder_open", "my_repo/"),
    ]
    if show_src:
        tree_items.extend(
            [
                ("doc_src", 1, "folder_open", "doc_src/"),
                ("toml", 2, "toml", "drawlib.toml"),
                ("styles", 2, "py", "styles.py, utils.py"),
                ("template", 2, "html", "template.html, style.css"),
                ("en_dir", 2, "folder_open", "en/"),
                ("cover", 3, "md", "00_cover.md"),
                ("overview", 3, "md", "01_overview.md"),
                ("build_sh", 2, "sh", "build.sh"),
            ]
        )
    if show_outputs:
        tree_items.extend(
            [
                ("out_md", 1, "folder_out", "doc_markdown/en/"),
                ("out_html", 1, "globe", "doc_html/en/"),
                ("out_pdf", 1, "pdf", "doc_en.pdf"),
                ("out_docx", 1, "word", "doc_en.docx"),
            ]
        )

    tree_rows: list[tuple[str, int, str, str, float]] = [
        (key, lvl, ik, lbl, 59.25 - idx * 4.25)
        for idx, (key, lvl, ik, lbl) in enumerate(tree_items)
    ]

    # Draw row highlight pills first (behind tree lines & text)
    for key, _lvl, _ik, _lbl, ry in tree_rows:
        if key not in row_states:
            continue
        rstate, badge_txt = row_states[key]
        if rstate in {"new", "active"}:
            rst = ROW_ACTIVE
            b_st = Styles.PrimaryFlat.patch(shape_r=0.8)
            b_txt = Styles.WhiteBold.patch(text_size=9.5)
        elif rstate == "optional":
            rst = ROW_OPTIONAL
            b_st = Styles.PrimaryNeutral.patch(shape_r=0.8)
            b_txt = Styles.PrimaryBold.patch(text_size=9.5)
        elif rstate == "output":
            rst = ROW_OUTPUT
            b_st = Styles.SecondaryFlat.patch(shape_r=0.8)
            b_txt = Styles.WhiteBold.patch(text_size=9.5)
        else:
            rst = None
            b_st = None
            b_txt = None

        if rst is not None:
            rectangle((103.1, ry), width=57.8, height=3.70, style=rst)
        if badge_txt and b_st is not None and b_txt is not None:
            rectangle(
                (125.0, ry),
                width=12.6,
                height=3.1,
                style=b_st,
                text=badge_txt,
                text_style=b_txt,
            )

    # Draw crisp geometric tree guide lines (supports levels 0..3)
    icon_xs = [77.2, 81.6, 85.8, 90.0]
    label_xs = [79.8, 84.2, 88.3, 92.5]
    guide_st = Styles.MutedThin.patch(line_color=(180, 194, 212), line_width=1.0)
    for idx_p, (_kp, lvl_p, _ikp, _lblp, ry_p) in enumerate(tree_rows):
        last_child_y: float | None = None
        for j in range(idx_p + 1, len(tree_rows)):
            lvl_j = tree_rows[j][1]
            if lvl_j <= lvl_p:
                break
            if lvl_j == lvl_p + 1:
                last_child_y = tree_rows[j][4]
        if last_child_y is not None:
            px = icon_xs[lvl_p]
            line((px, ry_p - 1.65), (px, last_child_y), style=guide_st)

    for key, lvl, ik, lbl, ry in tree_rows:
        rstate = row_states.get(key, ("normal", ""))[0]
        is_muted = rstate == "muted"

        ix = icon_xs[lvl]
        lx = label_xs[lvl]
        if lvl >= 1:
            line((icon_xs[lvl - 1], ry), (ix - 2.0, ry), style=guide_st)

        draw_tree_icon(ik, (ix, ry), muted=is_muted)

        if rstate in {"new", "active", "optional"}:
            t_st = Styles.PrimaryBold.patch(text_size=9.9, halign="left")
        elif rstate == "output":
            t_st = Styles.SecondaryBold.patch(text_size=9.9, halign="left")
        elif is_muted:
            t_st = Styles.Muted.patch(text_size=9.7, halign="left")
        elif lvl <= 1:
            t_st = Styles.DarkBold.patch(text_size=9.9, halign="left")
        else:
            t_st = Styles.Dark.patch(text_size=9.8, halign="left")

        text((lx, ry), lbl, style=t_st)

    if not show_src:
        text(
            (103.0, 35.0),
            "(Empty repository — waiting for drawlib init project)",
            style=Styles.Muted.patch(text_size=10.0),
        )


# =====================================================================
# Scene 1: Project Scaffolding Patterns (Frames 0 & 1)
# =====================================================================
with anim.frame(duration=2.6):
    draw_scene_init_patterns(highlight_doc=False)

with anim.frame(duration=2.4):
    draw_scene_init_patterns(highlight_doc=True)

# =====================================================================
# Scene 2: Day 1 — Initial Project Setup, Authoring & Commit
# =====================================================================
# Day 1 - 1. [User] Ask Gemini to create initial project
with anim.frame(duration=2.4):
    draw_split_workspace(
        phase_badge="Day 1: Initial Project Setup",
        step_heading="1. User — Ask Gemini to Create Project",
        actor="user",
        actor_title='User: "Create an initial doc project"',
        actor_sub="Ask Gemini to scaffold & configure theme",
        actor_optional=False,
        ops=[
            ("user", 'Ask Gemini: "Create initial doc project"', "active_user"),
        ],
        show_day2_note=False,
        show_src=False,
        show_outputs=False,
        row_states={},
        committed=False,
        pulse_arrow=False,
    )

# Day 1 - 2. [Gemini] Run drawlib init project doc
with anim.frame(duration=2.2):
    draw_split_workspace(
        phase_badge="Day 1: Initial Project Setup",
        step_heading="2. Gemini — Run drawlib init project doc",
        actor="gemini",
        actor_title="Gemini: Initialize 'doc' project",
        actor_sub="Scaffold doc_src/en/, config & build scripts",
        actor_optional=False,
        ops=[
            ("user", 'Ask Gemini: "Create initial doc project"', "done"),
            ("gemini", "$ drawlib init project doc", "active_gemini"),
        ],
        show_day2_note=False,
        show_src=False,
        show_outputs=False,
        row_states={},
        committed=False,
        pulse_arrow=True,
    )

# Day 1 - 3. [Gemini] Starter files created in doc_src/
with anim.frame(duration=2.5):
    draw_split_workspace(
        phase_badge="Day 1: Initial Project Setup",
        step_heading="3. Gemini — Starter Files Created",
        actor="gemini",
        actor_title="Gemini: Starter template generated",
        actor_sub="doc_src/ holds drawlib.toml, theme & en/",
        actor_optional=False,
        ops=[
            ("user", 'Ask Gemini: "Create initial doc project"', "done"),
            ("gemini", "$ drawlib init project doc", "active_gemini"),
        ],
        show_day2_note=False,
        show_src=True,
        show_outputs=False,
        row_states={
            "doc_src": ("new", "Created"),
            "toml": ("new", ""),
            "styles": ("new", ""),
            "template": ("new", ""),
            "en_dir": ("new", ""),
            "cover": ("new", ""),
            "overview": ("new", ""),
            "build_sh": ("new", ""),
        },
        committed=False,
        pulse_arrow=True,
    )

# Day 1 - 4. [Gemini] Update styles.py & utils.py
with anim.frame(duration=2.4):
    draw_split_workspace(
        phase_badge="Day 1: Initial Project Setup",
        step_heading="4. Gemini — Update styles.py & utils.py",
        actor="gemini",
        actor_title="Gemini: Configure styles & helpers",
        actor_sub="Set brand palette, fonts & reusable helpers",
        actor_optional=False,
        ops=[
            ("user", 'Ask Gemini: "Create initial doc project"', "done"),
            ("gemini", "$ drawlib init project doc", "done"),
            ("gemini", "Edit doc_src/styles.py, utils.py", "active_gemini"),
        ],
        show_day2_note=False,
        show_src=True,
        show_outputs=False,
        row_states={
            "styles": ("active", "Updated"),
        },
        committed=False,
        pulse_arrow=True,
    )

# Day 1 - 5. [Gemini] Optional template.html & style.css update
with anim.frame(duration=2.4):
    draw_split_workspace(
        phase_badge="Day 1: Initial Project Setup",
        step_heading="5. Gemini — Customize Template (Optional)",
        actor="gemini",
        actor_title="Gemini: Tweak HTML/CSS (Optional)",
        actor_sub="Default theme works out of the box",
        actor_optional=True,
        ops=[
            ("user", 'Ask Gemini: "Create initial doc project"', "done"),
            ("gemini", "$ drawlib init project doc", "done"),
            ("gemini", "Edit doc_src/styles.py, utils.py", "done"),
            ("gemini", "Edit template.html, style.css", "optional"),
        ],
        show_day2_note=False,
        show_src=True,
        show_outputs=False,
        row_states={
            "template": ("optional", "Optional"),
        },
        committed=False,
        pulse_arrow=True,
    )

# Day 1 - 6. [User] Ask Gemini to update project docs
with anim.frame(duration=2.4):
    draw_split_workspace(
        phase_badge="Day 1: Initial Project Setup",
        step_heading="6. User — Ask Gemini to Update Project",
        actor="user",
        actor_title='User: "Write & build the spec docs"',
        actor_sub="Ask Gemini to author chapters & diagrams",
        actor_optional=False,
        ops=[
            ("user", 'Ask Gemini: "Create initial doc project"', "done"),
            ("gemini", "$ drawlib init project doc", "done"),
            ("gemini", "Edit doc_src/styles.py, utils.py", "done"),
            ("gemini", "Edit template.html, style.css", "optional_done"),
            ("user", 'Ask Gemini: "Update project docs"', "active_user"),
        ],
        show_day2_note=False,
        show_src=True,
        show_outputs=False,
        row_states={},
        committed=False,
        pulse_arrow=False,
    )

# Day 1 - 7. [Gemini] Edit Markdown chapters inside doc_src/en/
with anim.frame(duration=2.4):
    draw_split_workspace(
        phase_badge="Day 1: Initial Project Setup",
        step_heading="7. Gemini — Author Markdown & Diagrams",
        actor="gemini",
        actor_title="Gemini: Write chapters & ```drawlib",
        actor_sub="Prose and Python diagrams live in doc_src/en/",
        actor_optional=False,
        ops=[
            ("user", 'Ask Gemini: "Create initial doc project"', "done"),
            ("gemini", "$ drawlib init project doc", "done"),
            ("gemini", "Edit doc_src/styles.py, utils.py", "done"),
            ("gemini", "Edit template.html, style.css", "optional_done"),
            ("user", 'Ask Gemini: "Update project docs"', "done"),
            ("gemini", "Edit en/00_cover.md, en/01_overview.md", "active_gemini"),
        ],
        show_day2_note=False,
        show_src=True,
        show_outputs=False,
        row_states={
            "cover": ("active", "Updated"),
            "overview": ("active", "Updated"),
        },
        committed=False,
        pulse_arrow=True,
    )

# Day 1 - 8. [Gemini] Run build
with anim.frame(duration=2.2):
    draw_split_workspace(
        phase_badge="Day 1: Initial Project Setup",
        step_heading="8. Gemini — Run Build Pipeline",
        actor="gemini",
        actor_title="Gemini: Compile all deliverables",
        actor_sub="Execute ./doc_src/build.sh + build docx",
        actor_optional=False,
        ops=[
            ("user", 'Ask Gemini: "Create initial doc project"', "done"),
            ("gemini", "$ drawlib init project doc", "done"),
            ("gemini", "Edit doc_src/styles.py, utils.py", "done"),
            ("gemini", "Edit template.html, style.css", "optional_done"),
            ("user", 'Ask Gemini: "Update project docs"', "done"),
            ("gemini", "Edit en/00_cover.md, en/01_overview.md", "done"),
            ("gemini", "$ ./doc_src/build.sh  (+ build docx)", "active_gemini"),
        ],
        show_day2_note=False,
        show_src=True,
        show_outputs=False,
        row_states={
            "build_sh": ("active", "Running"),
        },
        committed=False,
        pulse_arrow=True,
    )

# Day 1 - 9. [Gemini] Outputs generated (markdown, html, pdf, docx)
with anim.frame(duration=2.8):
    draw_split_workspace(
        phase_badge="Day 1: Initial Project Setup",
        step_heading="9. Gemini — Outputs Generated",
        actor="gemini",
        actor_title="Gemini: Built MD, HTML, PDF & DOCX",
        actor_sub="Locale outputs compiled from doc_src/en/",
        actor_optional=False,
        ops=[
            ("user", 'Ask Gemini: "Create initial doc project"', "done"),
            ("gemini", "$ drawlib init project doc", "done"),
            ("gemini", "Edit doc_src/styles.py, utils.py", "done"),
            ("gemini", "Edit template.html, style.css", "optional_done"),
            ("user", 'Ask Gemini: "Update project docs"', "done"),
            ("gemini", "Edit en/00_cover.md, en/01_overview.md", "done"),
            ("gemini", "$ ./doc_src/build.sh  (+ build docx)", "active_gemini"),
        ],
        show_day2_note=False,
        show_src=True,
        show_outputs=True,
        row_states={
            "out_md": ("output", "Output"),
            "out_html": ("output", "Output"),
            "out_pdf": ("output", "Output"),
            "out_docx": ("output", "Output"),
        },
        committed=False,
        pulse_arrow=True,
    )

# Day 1 - 10. [User] git commit
with anim.frame(duration=2.8):
    draw_split_workspace(
        phase_badge="Day 1: Initial Project Setup",
        step_heading="10. User — Review & Git Commit",
        actor="user",
        actor_title="User: Review outputs & commit to Git",
        actor_sub="Source & deliverables versioned together",
        actor_optional=False,
        ops=[
            ("user", 'Ask Gemini: "Create initial doc project"', "done"),
            ("gemini", "$ drawlib init project doc", "done"),
            ("gemini", "Edit doc_src/styles.py, utils.py", "done"),
            ("gemini", "Edit template.html, style.css", "optional_done"),
            ("user", 'Ask Gemini: "Update project docs"', "done"),
            ("gemini", "Edit en/00_cover.md, en/01_overview.md", "done"),
            ("gemini", "$ ./doc_src/build.sh  (+ build docx)", "done"),
            ("user_git", '$ git add . && git commit -m "Init doc"', "active_user"),
        ],
        show_day2_note=False,
        show_src=True,
        show_outputs=True,
        row_states={},
        committed=True,
        pulse_arrow=False,
    )

# =====================================================================
# Scene 3: Time Transition — "1 day later..."
# =====================================================================
with anim.frame(duration=2.4):
    draw_intertitle_one_day_later()

# =====================================================================
# Scene 4: Day 2 — Incremental Update Loop
# =====================================================================
# Day 2 - 1. [User] Ask Gemini to update project
with anim.frame(duration=2.4):
    draw_split_workspace(
        phase_badge="Day 2: Incremental Update",
        step_heading="1. User — Ask Gemini to Update Project",
        actor="user",
        actor_title='User: "Update spec for code changes"',
        actor_sub="Ask Gemini to refresh docs & diagrams",
        actor_optional=False,
        ops=[
            ("user", 'Ask Gemini: "Update project docs"', "active_user"),
        ],
        show_day2_note=True,
        show_src=True,
        show_outputs=True,
        row_states={
            "toml": ("muted", ""),
            "styles": ("muted", ""),
            "template": ("muted", ""),
            "out_md": ("muted", ""),
            "out_html": ("muted", ""),
            "out_pdf": ("muted", ""),
            "out_docx": ("muted", ""),
        },
        committed=False,
        pulse_arrow=False,
    )

# Day 2 - 2. [Gemini] Update Markdown only
with anim.frame(duration=2.6):
    draw_split_workspace(
        phase_badge="Day 2: Incremental Update",
        step_heading="2. Gemini — Update Markdown Only",
        actor="gemini",
        actor_title="Gemini: Edit en/01_overview.md",
        actor_sub="drawlib.toml, styles & templates untouched",
        actor_optional=False,
        ops=[
            ("user", 'Ask Gemini: "Update project docs"', "done"),
            ("gemini", "Edit doc_src/en/01_overview.md", "active_gemini"),
        ],
        show_day2_note=True,
        show_src=True,
        show_outputs=True,
        row_states={
            "toml": ("muted", ""),
            "styles": ("muted", ""),
            "template": ("muted", ""),
            "overview": ("active", "Modified"),
            "out_md": ("muted", ""),
            "out_html": ("muted", ""),
            "out_pdf": ("muted", ""),
            "out_docx": ("muted", ""),
        },
        committed=False,
        pulse_arrow=True,
    )

# Day 2 - 3. [Gemini] Rebuild
with anim.frame(duration=2.2):
    draw_split_workspace(
        phase_badge="Day 2: Incremental Update",
        step_heading="3. Gemini — Run Incremental Build",
        actor="gemini",
        actor_title="Gemini: Rebuild (SQLite cache active)",
        actor_sub="Only modified drawlib blocks re-render",
        actor_optional=False,
        ops=[
            ("user", 'Ask Gemini: "Update project docs"', "done"),
            ("gemini", "Edit doc_src/en/01_overview.md", "done"),
            ("gemini", "$ ./doc_src/build.sh  (+ build docx)", "active_gemini"),
        ],
        show_day2_note=True,
        show_src=True,
        show_outputs=True,
        row_states={
            "toml": ("muted", ""),
            "styles": ("muted", ""),
            "template": ("muted", ""),
            "build_sh": ("active", "Running"),
            "out_md": ("muted", ""),
            "out_html": ("muted", ""),
            "out_pdf": ("muted", ""),
            "out_docx": ("muted", ""),
        },
        committed=False,
        pulse_arrow=True,
    )

# Day 2 - 4. [Gemini] Outputs updated
with anim.frame(duration=2.6):
    draw_split_workspace(
        phase_badge="Day 2: Incremental Update",
        step_heading="4. Gemini — Deliverables Refreshed",
        actor="gemini",
        actor_title="Gemini: MD, HTML, PDF & DOCX updated",
        actor_sub="Zero manual screenshot copy-pasting",
        actor_optional=False,
        ops=[
            ("user", 'Ask Gemini: "Update project docs"', "done"),
            ("gemini", "Edit doc_src/en/01_overview.md", "done"),
            ("gemini", "$ ./doc_src/build.sh  (+ build docx)", "active_gemini"),
        ],
        show_day2_note=True,
        show_src=True,
        show_outputs=True,
        row_states={
            "toml": ("muted", ""),
            "styles": ("muted", ""),
            "template": ("muted", ""),
            "out_md": ("output", "Updated"),
            "out_html": ("output", "Updated"),
            "out_pdf": ("output", "Updated"),
            "out_docx": ("output", "Updated"),
        },
        committed=False,
        pulse_arrow=True,
    )

# Day 2 - 5. [User] git commit (final hold)
with anim.frame(duration=3.8):
    draw_split_workspace(
        phase_badge="Day 2: Incremental Update",
        step_heading="5. User — Review & Git Commit",
        actor="user",
        actor_title="User: Review & commit updated spec",
        actor_sub="Architecture and docs never drift apart",
        actor_optional=False,
        ops=[
            ("user", 'Ask Gemini: "Update project docs"', "done"),
            ("gemini", "Edit doc_src/en/01_overview.md", "done"),
            ("gemini", "$ ./doc_src/build.sh  (+ build docx)", "done"),
            ("user_git", '$ git add . && git commit -m "Update spec"', "active_user"),
        ],
        show_day2_note=True,
        show_src=True,
        show_outputs=True,
        row_states={},
        committed=True,
        pulse_arrow=False,
    )

save()
