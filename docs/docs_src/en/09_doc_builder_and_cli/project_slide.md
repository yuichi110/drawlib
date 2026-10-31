# Slide Deck Project Guide (`drawlib init slide`)

The `slide` starter template creates 16:9 presentation slide decks with rich architectural diagrams, metrics cards, badges, and structured layouts.

Drawlib compiles your slide deck into an **interactive HTML web presentation**, a **1-slide-per-page vector PDF**, and a **native editable 16:9 MS PowerPoint (`.pptx`) deck**, perfectly sized for conferences, client briefings, and team reviews.

```drawlib code=fold align=center file=slide_presenter_view_layout.png caption="Presenter View (?presenter=1) 4-Pane Workspace and BroadcastChannel Synchronization"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=128, height=62)

# Left Container: Presenter View Window (?presenter=1)
rectangle((40, 31), width=72, height=54, style=Styles.Neutral.patch(shape_r=2.0))
phosphor.presentation_chart((12.5, 54.0), width=4.4, style=Styles.PrimaryBold)
text((43.0, 54.0), "Presenter View (?presenter=1)", style=Styles.DarkBold.patch(text_size=10.8))

# Pane 1: Left Column (Slide Thumbnails Strip)
rectangle((16.5, 28.0), width=19, height=44, style=Styles.SecondaryNeutral.patch(shape_r=1.5))
text((16.5, 46.5), "1. Slides", style=Styles.DarkBold.patch(text_size=10.2))
rectangle((16.5, 39.2), width=16, height=7.8, style=Styles.Neutral.patch(shape_r=1.0), text="Slide 1", text_style=Styles.Dark.patch(text_size=10.0))
rectangle(
    (16.5, 29.0),
    width=16,
    height=8.2,
    style=Styles.PrimaryNeutral.patch(shape_r=1.0),
    text="Slide 2",
    text_style=Styles.PrimaryBold.patch(text_size=10.2),
)
rectangle((16.5, 18.8), width=16, height=7.8, style=Styles.Neutral.patch(shape_r=1.0), text="Slide 3", text_style=Styles.Dark.patch(text_size=10.0))
text((16.5, 10.5), "Jump", style=Styles.Muted.patch(text_size=10.0))

# Pane 2: Top-Right (Live 16:9 Current Slide Preview)
rectangle(
    (51.0, 41.2),
    width=45,
    height=17.5,
    style=Styles.PrimaryFlat.patch(shape_r=1.5),
    text="2. Live 16:9 Stage\n(Active Slide + Anim)",
    text_style=Styles.WhiteBold.patch(text_size=10.5),
)

# Pane 3: Middle-Right (Control & Timer Bar)
rectangle((51.0, 27.0), width=45, height=7.5, style=Styles.PrimaryNeutral.patch(shape_r=1.2))
phosphor.timer((33.0, 27.0), width=4.2, style=Styles.PrimaryBold)
text((54.0, 27.0), "3. Prev | Next | Play | 00:00", style=Styles.DarkBold.patch(text_size=10.0))

# Pane 4: Bottom-Right (Speaker Notes Pane)
rectangle((51.0, 13.8), width=45, height=15.0, style=Styles.SecondaryNeutral.patch(shape_r=1.5))
phosphor.note((33.0, 16.5), width=4.4, style=Styles.PrimaryBold)
text((54.0, 16.5), "4. Speaker Notes", style=Styles.DarkBold.patch(text_size=10.2))
text((51.0, 10.2), "::: note Markdown  [A- / A+]", style=Styles.Dark.patch(text_size=10.0))

# Bidirectional BroadcastChannel Sync Connector
phosphor.arrows_left_right((84.0, 40.5), width=4.6, style=Styles.PrimaryBold)
line((76, 31), (92, 31), arrow_head="<->", style=Styles.PrimaryBold)
text((84.0, 35.0), "Sync", style=Styles.PrimaryBold.patch(text_size=10.2))
text((84.0, 24.5), "Broadcast\nChannel", style=Styles.Muted.patch(text_size=10.0))

# Right Container: Audience Main Stage Window
rectangle((108, 31), width=32, height=54, style=Styles.Neutral.patch(shape_r=2.0))
text((108, 54.0), "Audience Stage", style=Styles.DarkBold.patch(text_size=10.8))
text((108, 49.0), "1920x1080 Screen", style=Styles.Muted.patch(text_size=10.0))

rectangle(
    (108, 33.5),
    width=28,
    height=23,
    style=Styles.PrimaryNeutral.patch(shape_r=1.5),
    text="16:9 Stage\n\nSlide 2\nDiagrams",
    text_style=Styles.DarkBold.patch(text_size=10.5),
)
rectangle(
    (108, 13.5),
    width=28,
    height=11.5,
    style=Styles.SecondaryNeutral.patch(shape_r=1.2),
    text="Notes Hidden\nZero Chrome",
    text_style=Styles.Dark.patch(text_size=10.0),
)

save()
```

---

## 1. End-to-End Project Workflow

From initial `drawlib init slide` scaffolding and story-arc planning to dual-layer authoring (`::: block` stage + `::: note` speaker scripts), HTML/PDF/`.pptx` compilation, live Presenter View (`?presenter=1`), and Day-2 cached edits:

```drawlib code=fold align=center file=project_slide_workflow_tour.png caption="16:9 Slide Deck Lifecycle: Scaffolding, Dual-Layer Authoring, HTML/PDF/PPTX Export, and Presenter View (APNG Animation)"
from __future__ import annotations

from drawlib.anim import Animation
from drawlib.canvas import save, setup
from drawlib.icons import ai, code, devops, phosphor, workspace
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.styles import Styles
from drawlib.text import text

W, H = 138.0, 82.0
setup(width=W, height=H)
anim = Animation(fps=10.0, loop=0)

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
ROW_CACHED = Styles.PrimaryNeutral.patch(
    shape_fill_color=(242, 247, 255),
    shape_line_color=(147, 197, 253),
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

PART_ITEMS = [
    ("1. Init Slide Deck", "Scaffold & story arc"),
    ("2. Stage & Notes", "::: block & ::: note"),
    ("3. HTML, PDF & PPTX", "Web, vector & deck"),
    ("4. Present & Edit", "Presenter & cache"),
]


def draw_step_bar(active_part: int) -> None:
    """Draw top 4-pill progress bar aligned with both panes."""
    pill_w = 31.0
    pill_h = 7.4
    gap = 2.0
    start_x = 4.0 + pill_w / 2.0
    cy = 75.2

    for idx, (label, sublabel) in enumerate(PART_ITEMS, start=1):
        cx = start_x + (idx - 1) * (pill_w + gap)
        if idx > 1:
            prev_cx = cx - (pill_w + gap)
            line(
                (prev_cx + pill_w / 2.0 + 0.2, cy),
                (cx - pill_w / 2.0 - 0.2, cy),
                style=Styles.PrimaryBold if idx <= active_part else Styles.MutedThin,
            )

        if idx == active_part:
            st = Styles.PrimaryFlat.patch(shape_r=1.4)
            tst = Styles.WhiteBold.patch(text_size=10.2)
            sub_tst = Styles.White.patch(text_size=9.5)
        elif idx < active_part:
            st = Styles.PrimaryNeutral.patch(shape_r=1.4, shape_line_width=1.1)
            tst = Styles.PrimaryBold.patch(text_size=10.2)
            sub_tst = Styles.Primary.patch(text_size=9.5)
        else:
            st = Styles.Neutral.patch(shape_r=1.4, shape_line_width=1.1)
            tst = Styles.MutedBold.patch(text_size=10.2)
            sub_tst = Styles.Muted.patch(text_size=9.5)

        rectangle((cx, cy), width=pill_w, height=pill_h, style=st)
        text((cx, cy + 1.35), label, style=tst)
        text((cx, cy - 1.55), sublabel, style=sub_tst)


def draw_pane_shell(cx: float, width: float) -> None:
    """Draw rounded pane container with top header bar."""
    rectangle((cx, 36.75), width=width, height=65.5, style=PANE_BG)
    rectangle((cx, 66.25), width=width, height=6.5, style=PANE_HEADER_TOP)
    rectangle((cx, 64.60), width=width, height=3.2, style=PANE_HEADER_FLAT)
    line(
        (cx - width / 2.0, 63.0),
        (cx + width / 2.0, 63.0),
        style=Styles.Neutral.patch(line_color=(203, 213, 225), line_width=1.2),
    )
    rectangle((cx, 36.75), width=width, height=65.5, style=PANE_BORDER)


def draw_user_avatar(xy: tuple[float, float], radius: float = 4.2) -> None:
    """Draw circular User avatar badge."""
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


def draw_gemini_avatar(xy: tuple[float, float], radius: float = 4.2) -> None:
    """Draw circular Gemini avatar badge."""
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
    elif kind == "py":
        code.python(xy, width=2.8, style=Styles.Neutral)
    elif kind == "css":
        phosphor.file_css(
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
        phosphor.presentation_chart(
            xy,
            width=3.0,
            style=Styles.Muted if muted else Styles.PrimaryBold,
        )
    elif kind == "pdf":
        phosphor.file_pdf(
            xy,
            width=3.0,
            style=Styles.Muted if muted else Styles.Danger,
        )
    elif kind == "pptx":
        workspace.powerpoint(xy, width=2.9, style=Styles.Neutral)


def draw_workspace(
    *,
    active_part: int,
    actor: str,
    actor_title: str,
    actor_sub: str,
    actor_optional: bool,
    ops: list[tuple[str, str, str]],
    show_day2_note: bool,
    show_flow: bool,
    show_outputs: bool,
    row_states: dict[str, tuple[str, str]],
    committed: bool,
    pulse_arrow: bool,
) -> None:
    """Draw 2-pane split workspace for the slide project workflow."""
    draw_step_bar(active_part)

    # Left Pane: User & Gemini — Prompts & Commands
    draw_pane_shell(36.0, 64.0)
    phosphor.user((8.3, 66.25), width=3.4, style=Styles.DarkBold)
    ai.gemini((12.2, 66.25), width=3.7, style=Styles.Neutral)
    text(
        (15.4, 66.25),
        "User & Gemini — Prompts & Commands",
        style=Styles.DarkBold.patch(text_size=10.5, halign="left"),
    )

    if actor == "user":
        draw_user_avatar((10.8, 55.3), radius=4.2)
        bubble_st = ROW_USER
        title_st = Styles.DarkBold.patch(text_size=10.2, halign="left")
    else:
        draw_gemini_avatar((10.8, 55.3), radius=4.2)
        bubble_st = ROW_OPTIONAL if actor_optional else ROW_ACTIVE
        title_st = Styles.PrimaryBold.patch(text_size=10.2, halign="left")

    rectangle((41.5, 55.3), width=48.6, height=9.8, style=bubble_st)
    text((19.0, 57.3), actor_title, style=title_st)
    text(
        (19.0, 53.0),
        actor_sub,
        style=Styles.Dark.patch(text_size=9.7, halign="left"),
    )

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
            otxt = Styles.DarkBold.patch(text_size=9.7, halign="left")
        elif state == "active_gemini":
            ost = ROW_ACTIVE
            otxt = Styles.PrimaryBold.patch(text_size=9.7, halign="left")
        elif state == "optional":
            ost = ROW_OPTIONAL
            otxt = Styles.PrimaryBold.patch(text_size=9.7, halign="left")
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
                height=3.1,
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
            "styles.py, utils.py & style.css stay untouched",
            style=Styles.MutedBold.patch(text_size=9.6),
        )
        text(
            (36.0, 10.1),
            "Unchanged slides restore from .drawlib/cache.db",
            style=Styles.Muted.patch(text_size=9.5),
        )

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

    # Right Pane: Directory Structure
    draw_pane_shell(103.0, 62.0)
    phosphor.folder_open((76.6, 66.25), width=3.8, style=Styles.PrimaryBold)
    text(
        (79.8, 66.25),
        "Directory Structure",
        style=Styles.DarkBold.patch(text_size=10.6, halign="left"),
    )

    if committed:
        rectangle((123.2, 66.25), width=17.6, height=4.4, style=ROW_OUTPUT)
        devops.git((116.8, 66.25), width=2.8, style=Styles.Neutral)
        text(
            (119.0, 66.25),
            "Committed",
            style=Styles.SecondaryBold.patch(text_size=9.5, halign="left"),
        )

    tree_rows: list[tuple[str, int, str, str, float]] = [
        ("root", 0, "folder_open", "my_deck/", 59.50),
        ("slide_src", 1, "folder_open", "slide_src/", 55.30),
        ("styles", 2, "py", "styles.py", 51.10),
        ("utils", 2, "py", "utils.py", 46.90),
        ("css", 2, "css", "style.css", 42.70),
        ("scripts", 2, "sh", "build.sh, serve.sh", 38.50),
        ("s01", 2, "md", "01_title.md", 34.30),
        ("s02", 2, "md", "02_arch.md", 30.10),
    ]
    if show_flow:
        tree_rows.append(("s03", 2, "md", "03_flow.md", 25.90))
    if show_outputs:
        tree_rows.extend(
            [
                ("out_html", 1, "globe", "slide_html/", 19.60),
                ("out_pdf", 1, "pdf", "slide.pdf", 15.20),
                ("out_pptx", 1, "pptx", "slide.pptx", 10.80),
            ]
        )

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
        elif rstate == "cached":
            rst = ROW_CACHED
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
            rectangle((103.1, ry), width=57.8, height=3.60, style=rst)
        if badge_txt and b_st is not None and b_txt is not None:
            bw = 15.6 if len(badge_txt) >= 10 else 12.8
            bcx = 131.3 - bw / 2.0
            rectangle(
                (bcx, ry),
                width=bw,
                height=3.05,
                style=b_st,
                text=badge_txt,
                text_style=b_txt,
            )

    guide_st = Styles.MutedThin.patch(line_color=(180, 194, 212), line_width=1.0)
    last_lvl1_y = min(ry for _k, lvl, _ik, _l, ry in tree_rows if lvl == 1)
    last_lvl2_y = min(ry for _k, lvl, _ik, _l, ry in tree_rows if lvl == 2)
    line((77.2, 57.7), (77.2, last_lvl1_y), style=guide_st)
    line((81.6, 53.5), (81.6, last_lvl2_y), style=guide_st)

    for key, lvl, ik, lbl, ry in tree_rows:
        rstate = row_states.get(key, ("normal", ""))[0]
        is_muted = rstate == "muted"

        if lvl == 0:
            ix, lx = 77.2, 79.8
        elif lvl == 1:
            line((77.2, ry), (79.5, ry), style=guide_st)
            ix, lx = 81.6, 84.2
        else:
            line((81.6, ry), (83.9, ry), style=guide_st)
            ix, lx = 86.0, 88.5

        draw_tree_icon(ik, (ix, ry), muted=is_muted)

        if rstate in {"new", "active", "optional", "cached"}:
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


# Phase 1: 1. Init Slide Deck (f0..f2)
with anim.frame(duration=3.1):
    draw_workspace(
        active_part=1,
        actor="user",
        actor_title="$ drawlib init slide -s google",
        actor_sub="Scaffold 16:9 slide_src/ deck & scripts",
        actor_optional=False,
        ops=[
            ("user", "$ drawlib init slide -s google", "active_user"),
        ],
        show_day2_note=False,
        show_flow=False,
        show_outputs=False,
        row_states={
            "slide_src": ("new", "Created"),
            "styles": ("new", "Created"),
            "utils": ("new", "Created"),
            "css": ("new", "Created"),
            "scripts": ("new", "Created"),
            "s01": ("new", "Created"),
            "s02": ("new", "Created"),
        },
        committed=False,
        pulse_arrow=True,
    )

with anim.frame(duration=3.1):
    draw_workspace(
        active_part=1,
        actor="gemini",
        actor_title="Gemini: Configure theme in styles.py",
        actor_sub="Set presentation palette, cards & fonts",
        actor_optional=False,
        ops=[
            ("user", "$ drawlib init slide -s google", "done"),
            ("gemini", "Edit slide_src/styles.py, utils.py", "active_gemini"),
        ],
        show_day2_note=False,
        show_flow=False,
        show_outputs=False,
        row_states={
            "styles": ("active", "Updated"),
            "utils": ("active", "Updated"),
        },
        committed=False,
        pulse_arrow=True,
    )

with anim.frame(duration=3.3):
    draw_workspace(
        active_part=1,
        actor="gemini",
        actor_title="Gemini: Plan slide deck story arc",
        actor_sub="Structure numbered slides 01_title..03_flow",
        actor_optional=False,
        ops=[
            ("user", "$ drawlib init slide -s google", "done"),
            ("gemini", "Edit slide_src/styles.py, utils.py", "done"),
            ("gemini", "Plan story arc (01_title..03_flow.md)", "active_gemini"),
        ],
        show_day2_note=False,
        show_flow=True,
        show_outputs=False,
        row_states={
            "s01": ("active", "Updated"),
            "s02": ("active", "Updated"),
            "s03": ("new", "Created"),
        },
        committed=False,
        pulse_arrow=True,
    )

# Phase 2: 2. Stage & Notes (f3..f5)
with anim.frame(duration=3.1):
    draw_workspace(
        active_part=2,
        actor="gemini",
        actor_title="Gemini: Author ::: block stage panels",
        actor_sub="1920x1080 layout + .svg / animated .webp",
        actor_optional=False,
        ops=[
            ("user", "$ drawlib init slide -s google", "done"),
            ("gemini", "Configure styles.py & 01..03 story arc", "done"),
            ("gemini", "Author ::: block stage + .svg / .webp", "active_gemini"),
        ],
        show_day2_note=False,
        show_flow=True,
        show_outputs=False,
        row_states={
            "s01": ("active", "Updated"),
            "s02": ("active", "Updated"),
            "s03": ("active", "Updated"),
        },
        committed=False,
        pulse_arrow=True,
    )

with anim.frame(duration=3.1):
    draw_workspace(
        active_part=2,
        actor="gemini",
        actor_title="Gemini: Add ::: note speaker scripts",
        actor_sub="Hidden on stage; synced to Presenter & PPTX",
        actor_optional=False,
        ops=[
            ("user", "$ drawlib init slide -s google", "done"),
            ("gemini", "Configure styles.py & 01..03 story arc", "done"),
            ("gemini", "Author ::: block stage + .svg / .webp", "done"),
            ("gemini", "Add ::: note speaker notes to slides", "active_gemini"),
        ],
        show_day2_note=False,
        show_flow=True,
        show_outputs=False,
        row_states={
            "s01": ("active", "::: note"),
            "s02": ("active", "::: note"),
            "s03": ("active", "::: note"),
        },
        committed=False,
        pulse_arrow=True,
    )

with anim.frame(duration=3.3):
    draw_workspace(
        active_part=2,
        actor="gemini",
        actor_title="$ drawlib show .../02_arch.md arch.svg -g",
        actor_sub="Verify diagram coordinates & stage margins",
        actor_optional=False,
        ops=[
            ("user", "$ drawlib init slide -s google", "done"),
            ("gemini", "Configure styles.py & 01..03 story arc", "done"),
            ("gemini", "Author ::: block stage & ::: note", "done"),
            ("gemini", "$ drawlib show .../02_arch.md arch.svg -g", "active_gemini"),
        ],
        show_day2_note=False,
        show_flow=True,
        show_outputs=False,
        row_states={
            "s01": ("output", "Verified"),
            "s02": ("output", "Verified"),
            "s03": ("output", "Verified"),
        },
        committed=False,
        pulse_arrow=False,
    )

# Phase 3: 3. HTML, PDF & PPTX (f6..f8)
with anim.frame(duration=3.1):
    draw_workspace(
        active_part=3,
        actor="gemini",
        actor_title="$ ./slide_src/build.sh",
        actor_sub="Compile interactive slide_html/ & vector PDF",
        actor_optional=False,
        ops=[
            ("user", "$ drawlib init slide -s google", "done"),
            ("gemini", "Configure styles.py & 01..03 story arc", "done"),
            ("gemini", "Author & grid-verify slides + notes", "done"),
            ("gemini", "$ ./slide_src/build.sh  (HTML + PDF)", "active_gemini"),
        ],
        show_day2_note=False,
        show_flow=True,
        show_outputs=True,
        row_states={
            "scripts": ("active", "Running"),
            "out_html": ("output", "Output"),
            "out_pdf": ("output", "Output"),
            "out_pptx": ("optional", "Optional"),
        },
        committed=False,
        pulse_arrow=True,
    )

with anim.frame(duration=3.1):
    draw_workspace(
        active_part=3,
        actor="gemini",
        actor_title="$ drawlib build pptx slide_src/ -o slide.pptx",
        actor_sub="Export editable 16:9 PowerPoint + notes",
        actor_optional=True,
        ops=[
            ("user", "$ drawlib init slide -s google", "done"),
            ("gemini", "Configure styles.py & 01..03 story arc", "done"),
            ("gemini", "Author & grid-verify slides + notes", "done"),
            ("gemini", "$ ./slide_src/build.sh  (HTML + PDF)", "done"),
            ("gemini", "$ drawlib build pptx slide_src/", "optional"),
        ],
        show_day2_note=False,
        show_flow=True,
        show_outputs=True,
        row_states={
            "out_html": ("output", "Output"),
            "out_pdf": ("output", "Output"),
            "out_pptx": ("output", "Output"),
        },
        committed=False,
        pulse_arrow=True,
    )

with anim.frame(duration=3.3):
    draw_workspace(
        active_part=3,
        actor="user",
        actor_title='User: $ git commit -m "Add slide deck"',
        actor_sub="Markdown slides & exports versioned in Git",
        actor_optional=False,
        ops=[
            ("user", "$ drawlib init slide -s google", "done"),
            ("gemini", "Configure styles.py & 01..03 story arc", "done"),
            ("gemini", "Author & grid-verify slides + notes", "done"),
            ("gemini", "$ ./slide_src/build.sh  (HTML + PDF)", "done"),
            ("gemini", "$ drawlib build pptx slide_src/", "optional_done"),
            ("user_git", '$ git add . && git commit -m "Init deck"', "active_user"),
        ],
        show_day2_note=False,
        show_flow=True,
        show_outputs=True,
        row_states={},
        committed=True,
        pulse_arrow=False,
    )

# Phase 4: 4. Present & Edit (f9..f11)
with anim.frame(duration=3.1):
    draw_workspace(
        active_part=4,
        actor="user",
        actor_title="$ ./slide_src/serve.sh  (?presenter=1)",
        actor_sub="Audience Deck + Presenter (BroadcastChannel)",
        actor_optional=False,
        ops=[
            ("user", "$ ./slide_src/serve.sh  (?presenter=1)", "active_user"),
        ],
        show_day2_note=False,
        show_flow=True,
        show_outputs=True,
        row_states={
            "scripts": ("active", "Serving"),
            "out_html": ("active", "Presenter"),
        },
        committed=False,
        pulse_arrow=True,
    )

with anim.frame(duration=3.1):
    draw_workspace(
        active_part=4,
        actor="gemini",
        actor_title="1 day later: Tweak 02_arch.md & rebuild",
        actor_sub="Unchanged slides hit .drawlib/cache.db (<1ms)",
        actor_optional=False,
        ops=[
            ("user", "$ ./slide_src/serve.sh  (?presenter=1)", "done"),
            ("user", '1 day later: "Refine 02_arch.md"', "done"),
            ("gemini", "Edit 02_arch.md & ./slide_src/build.sh", "active_gemini"),
        ],
        show_day2_note=True,
        show_flow=True,
        show_outputs=True,
        row_states={
            "styles": ("muted", ""),
            "utils": ("muted", ""),
            "css": ("muted", ""),
            "s01": ("cached", "Cached <1ms"),
            "s02": ("active", "Modified"),
            "s03": ("cached", "Cached <1ms"),
            "out_html": ("output", "Output"),
            "out_pdf": ("output", "Output"),
            "out_pptx": ("muted", ""),
        },
        committed=False,
        pulse_arrow=True,
    )

with anim.frame(duration=3.3):
    draw_workspace(
        active_part=4,
        actor="user",
        actor_title="Re-export updated deck & git commit",
        actor_sub="HTML, PDF & PPTX refreshed and committed",
        actor_optional=False,
        ops=[
            ("user", "$ ./slide_src/serve.sh  (?presenter=1)", "done"),
            ("user", '1 day later: "Refine 02_arch.md"', "done"),
            ("gemini", "Edit 02_arch.md & ./slide_src/build.sh", "done"),
            ("gemini", "$ drawlib build pptx slide_src/", "optional_done"),
            ("user_git", '$ git commit -m "Update arch slide"', "active_user"),
        ],
        show_day2_note=True,
        show_flow=True,
        show_outputs=True,
        row_states={
            "out_html": ("output", "Updated"),
            "out_pdf": ("output", "Updated"),
            "out_pptx": ("output", "Updated"),
        },
        committed=True,
        pulse_arrow=False,
    )

save()
```

---

## 2. Project Initialization

Scaffold a presentation project using `drawlib init`:

```bash
# Scaffold standard slide project in current directory (creates 'slide_src/'):
drawlib init slide

# With custom target name, theme, and language (creates 'my_deck_src/'):
drawlib init slide my_deck -s google -l en
```

---

## 3. Directory Layout & Anatomy

A `slide` project keeps all authoring source files inside `slide_src/` and compiles presentation deliverables alongside it:

- **`slide_src/` (Single Source of Truth)**:
  - **`01_title.md`, `02_agenda.md`, `03_arch.md` (and section sub-folders)**: Individual `1920x1080` 16:9 slides compiled in sorted path order, combining `::: block` stage containers, ```` ```drawlib ```` diagrams (`.svg`, `.png`, `.webp`), and `::: note` speaker notes.
  - **`_`-Prefixed Files & `README.md`**: Planning outlines, draft slides (`_planning.md`, `_drafts/`), and `README.md` are automatically excluded from deck compilation.
  - **`_assets/`**: Static logos, fonts, and reference media synchronized into output folders.
  - **`styles.py` & `utils.py`**: Shared presentation color tokens, typography defaults, slide header/footer helpers, and KPI/card utilities.
  - **`style.css` & `slide.js`**: 16:9 viewport scaling stylesheet, keyboard navigation controller, and `BroadcastChannel` Presenter View runtime.
  - **`build.sh`, `build_html.sh`, `build_pdf.sh`, `build_image.sh`, `serve.sh`**: Modular build scripts and local presentation preview launcher.
- **Generated Outputs (Do Not Edit Directly)**:
  - **`slide_html/`**: Interactive browser slide deck (`index.html`) supporting full-screen mode, overview grid, and `?presenter=1` Presenter View.
  - **`slide.pdf`**: Multi-page vector-sharp 16:9 PDF (`1920px × 1080px` per page) rendered via headless Chromium.
  - **`slide.pptx`**: Native editable 16:9 (`960×540 pt`) MS PowerPoint deck exported on demand via `drawlib build pptx`, preserving stage cards, text runs, diagrams, and speaker notes.
  - **`slide_images/`**: Standalone extracted illustrations when running `build_image.sh`.

---

## 4. Multiple Presentation Outputs

A `slide` project produces presentation artifacts tailored for every scenario:

| Output | Audience & Environment | Key Features | Build Script / Command |
| :--- | :--- | :--- | :--- |
| **`slide_html/index.html`** | Interactive Presenting | 1920x1080 fixed stage, auto-scaling viewport, keyboard navigation (`Space`, `Arrows`, `F`), Presenter View (`?presenter=1`), overview grid | `build_html.sh` (`drawlib build slide`) |
| **`slide.pdf`** | Print & Read-Only Distribution | 1 slide per page, vector-sharp graphics, exact 16:9 aspect ratio (`@page { size: 1920px 1080px; margin: 0; }`) | `build_pdf.sh` (`drawlib build pdf`) |
| **`slide.pptx`** | Collaborative Editing & Executive Decks | Native editable 16:9 (`960×540 pt`) MS PowerPoint deck (`::: block` cards with `rgba` alpha, text boxes, lists, tables, `::: note` speaker notes, high-DPI diagram PNGs) | `drawlib build pptx` |
| **`slide_images/`** | Slides & Social Media | Extracted standalone slide illustrations for external decks and sharing | `build_image.sh` (`drawlib build image`) |

---

## 5. Authoring Slides & Stage Blocks

Each Markdown file in `slide_src/` (and any nested chapter subdirectories such as `01_intro/01_cover.md`) represents a single 16:9 slide (`1920x1080` stage), compiled in sorted relative-path order.
- **Excluding Non-Slide Files (`_` Prefix)**: Prefix any planning notes, outlines, or draft files/folders with an underscore `_` (e.g., `_planning.md`, `_drafts/`) to exclude them from slide compilation.
- **Special Excluded Files**: `README.md` and `navbar.md` are also automatically excluded from the slide deck.

Use `::: block xy=(x, y) width=W height=H` containers alongside standard Markdown and helper components from `utils.py` (see [Slide Stage Layout & API](./slide_layout_and_api.md) for the complete stage coordinate reference, layout templates, and `drawlib.slide` API):

````markdown
::: block xy=(80, 40) width=1760 height=60
# Architecture Overview
:::

::: block xy=(80, 140) width=1760 height=840
```drawlib file=arch_flow.svg
from drawlib.canvas import clear, save, setup
from drawlib.shapes import rectangle
from drawlib.lines import line
from drawlib.styles import Styles

clear()
setup(width=176, height=84)
rectangle((35, 42), width=38, height=22, style=Styles.Neutral, text="Producer")
rectangle((88, 42), width=38, height=22, style=Styles.PrimaryFlat, text="Kafka", text_style=Styles.WhiteBold)
rectangle((141, 42), width=38, height=22, style=Styles.SecondaryNeutral, text="Consumer")
line((54, 42), (69, 42), arrow_head="->", style=Styles.DarkBold)
line((107, 42), (122, 42), arrow_head="->", style=Styles.DarkBold)
save()
```
:::
````

---

## 6. Modular Build Scripts & MS PowerPoint (`.pptx`) Export

- **`build_html.sh`**:
  Compiles slides into the web presentation deck in `slide_html/index.html` (`drawlib build slide`).
- **`build_pdf.sh`**:
  Uses headless Chromium to capture each slide into a multi-page vector PDF (`slide.pdf`).
- **`build_image.sh`**:
  Extracts embedded ````drawlib```` blocks into standalone diagram images in `slide_images/`.
- **`build.sh` (Master Script)**:
  Runs HTML, PDF, and Image builds in sequence.
- **Editable MS PowerPoint Export (`drawlib build pptx`)**:
  Measures the `1920x1080` slide DOM and computed CSS styles via headless Chromium and exports a native editable 16:9 (`960x540 pt`) `.pptx` file:
  ```bash
  uv run drawlib build pptx slide_src/ -o slide.pptx --dpi 240 --anim-frame last
  ```

---

## 7. Local Preview & Presenting

Launch the local development preview server:

```bash
./slide_src/serve.sh
```

Or run directly:

```bash
uv run drawlib serve slide_html/
```

### Keyboard Shortcuts & URL Deep-Linking:
- **`→` / `Space` / `PageDown`**: Next slide
- **`←` / `PageUp`**: Previous slide
- **`F`**: Toggle full screen
- **`O` / `Esc`**: Toggle slide overview grid
- **`P` / `S`**: Open **Presenter View** in a synchronized companion window
- **`A`**: Play / pause / resume animation on the current slide
- **URL Hash Deep-Linking (`#1`, `#2`, ...)**: Navigating to `index.html#4` jumps directly to Slide 4, and advancing slides updates the URL hash in real time for bookmarking and sharing.
- **Direct Presenter URL (`?presenter=1`)**: Appending `?presenter=1#1` launches the window directly in Presenter View mode, synchronizing slide changes and animation playback across windows via `BroadcastChannel` / `localStorage`.

### Speaker Notes (`::: note`) & Presenter View:
Add speaker notes to any slide using `::: note` blocks. If a slide contains multiple `::: note` blocks, they are automatically joined with a blank line (`\n\n`), rendered as Markdown in **Presenter View**, and exported into **native PowerPoint speaker notes** during `drawlib build pptx` (while remaining completely hidden on the main presentation screen and in PDF exports):

```markdown
::: note
**Key Talking Points**:
- Emphasize single source of truth in Git.
- Click **Play Animation** (or press `A`) to step through the pipeline.
:::
```

Pressing **`P`** or **`S`** (or clicking the `🗒` button in the bottom-right control bar) opens **Presenter View** (`?presenter=1`), featuring:
- **Left Column**: Vertical scrollable list of live slide thumbnails for instant jumping.
- **Right Top**: Live 16:9 preview of the current slide.
- **Right Middle (Control Bar)**: `◀ Prev` / `Next ▶` navigation, **`▶ Play Animation` button** (synchronized with the main window; automatically disabled/grayed out on slides without animations), and an elapsed presentation timer (`00:00`).
- **Right Bottom (Speaker Notes)**: Compiled speaker notes with `A-` / `A+` font-size controls.

### Interactive Animation Playback (`anim_trigger`, `anim_loop`, `anim_pause`):
When embedding APNG (`.png` / `.apng`) or Animated WebP (`.webp`) diagrams inside slides, you can attach playback control attributes to the ````drawlib```` code fence:

````markdown
```drawlib file=workflow.webp anim_trigger=click anim_loop=once anim_pause=(2, 4)
```
````

- **`anim_trigger=click`** (`auto` | `click`): Holds on Frame 0 until clicked by the presenter.
- **`anim_loop=once`** (`once` | `infinite`): Stops on the final frame (`ENDED`); clicking again replays from Frame 0.
- **`anim_pause=(2, 4)`**: Pauses at 0-based frame indices `2` and `4` (`PAUSED`); clicking resumes to the next step.
- **Vector PDF Export (`build_pdf.sh`)**: Automatically renders Frame 0 onto the slide without the interactive play badge.
- **MS PowerPoint Export (`drawlib build pptx`)**: Extracts a crisp static PNG at `--dpi 240` using the final frame by default (`--anim-frame last`), or the initial frame when `--anim-frame first` is specified.

---

## 8. Parallel Multi-Agent Slide Deck Authoring

Because each slide in `slide_src/` is an isolated Markdown file (`01_title.md`, `02_agenda.md`, `03_arch.md`, or organized in section folders), AI coding agents can construct or overhaul multi-slide presentations in parallel:
1. **Phase 1 (Parent Setup)**: Scaffold `slide_src/` (`drawlib init slide`), configure `styles.py` and `utils.py`, and define the slide deck story arc and numbered filenames first.
2. **Phase 2 (Parallel Subagents)**: Delegate disjoint slide files (or section directories) to parallel subagents. Each subagent authors its assigned slides (`::: block` stage layout + `::: note` speaker script) and runs `-g` grid previews using unique scratch paths (`-o .drawlib/scratch/<slide>_<block>_grid.png`).
3. **Phase 3 (Unified Deck Build & Review)**: After all subagents complete their slides, the parent agent runs `./slide_src/build.sh` (and `drawlib build pptx` if needed) once and inspects the compiled `slide.pdf` and `slide_html/index.html`.

