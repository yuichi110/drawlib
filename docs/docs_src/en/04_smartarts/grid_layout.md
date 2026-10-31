# GridLayout

The `GridLayout` component positions cards and rectangular blocks across a uniform or flexible column/row matrix.
It supports multi-column and multi-row cell spanning, outer container borders, and proportional scaling—making it ideal for layered system architectures, service matrices, and executive dashboard layouts.

```drawlib code=fold align=center file=smartarts_gridlayout_indexing_geometry.png caption="GridLayout Bottom-Up (col, row) Matrix Indexing and Multi-Cell Spanning"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import circle
from drawlib.smartarts import GridLayout
from drawlib.styles import Styles
from drawlib.text import text

setup(width=126, height=62)

grid = GridLayout(
    num_column=3,
    num_row=3,
    style=Styles.Neutral.patch(shape_r=1.2),
    text_style=Styles.DarkBold.patch(text_size=10.0),
)

# Row 0 (Bottom Row)
grid.add(position=(0, 0), width=1, height=1, text="pos=(0, 0)\nw=1, h=1", style=Styles.PrimaryNeutral.patch(shape_r=1.2))
grid.add(position=(1, 0), width=1, height=1, text="pos=(1, 0)\nw=1, h=1")
grid.add(position=(2, 0), width=1, height=1, text="pos=(2, 0)\nw=1, h=1")

# Row 1 (Middle Row) & Spanned Cell across Columns 1..2, Rows 1..2
grid.add(position=(0, 1), width=1, height=1, text="pos=(0, 1)\nw=1, h=1")
grid.add(
    position=(1, 1),
    width=2,
    height=2,
    text="\nSpanned Cell: pos=(1, 1), w=2, h=2\n(Covers cols 1..2, rows 1..2)",
    style=Styles.PrimaryFlat.patch(shape_r=1.2),
    text_style=Styles.WhiteBold.patch(text_size=10.0),
)

# Row 2 (Top Row, Column 0)
grid.add(position=(0, 2), width=1, height=1, text="pos=(0, 2)\nw=1, h=1", style=Styles.SecondaryNeutral.patch(shape_r=1.2))

grid.draw(
    xy=(24.0, 11.0),
    width=96.0,
    height=41.0,
    margin=1.8,
    outer_style=Styles.MutedDashed.patch(shape_r=1.8),
)

# Icon inside the spanned hero cell
phosphor.activity(xy=(85.5, 42.5), width=4.2, style=Styles.White)

# Axis arrows and anchor dot at bottom-left xy=(24, 11)
line((42.0, 6.0), (120.0, 6.0), arrow_head="->", style=Styles.PrimaryBold)
text((81.0, 2.5), "Column Index (col = 0 → 2, +x Rightward)", style=Styles.PrimaryBold.patch(text_size=10.0))

line((18.5, 11.0), (18.5, 52.0), arrow_head="->", style=Styles.PrimaryBold)
text((9.5, 31.5), "Row Index\n(row = 0 → 2)\n+y Upward", style=Styles.PrimaryBold.patch(text_size=10.0))

circle((24.0, 11.0), radius=1.2, style=Styles.DangerFlat)
text((24.0, 6.0), "xy=(24, 11)", style=Styles.DangerBold.patch(text_size=10.0))
text((72.0, 56.8), "3×3 GridLayout Matrix (Bottom-Up Indexing & Spanning)", style=Styles.BlackBold.patch(text_size=11.0))

save()
```

---

## 1. Core Concepts & Basic Usage

`GridLayout` arranges cards across a zero-indexed **Bottom-Up `(col, row)`** matrix anchored by default at the **Bottom-Left `(x, y)`** corner (`align="bottom_left"`) or centered via `align="center"`. Cells added with `.add((col, row), width, height, ...)` can span multiple columns and rows, render inside an `outer_style` container with equal or `draw_flexible(...)` proportions, and toggle `.items[i].show = False` without shifting sibling coordinates:

```drawlib code=fold align=center file=grid_layout_parameter_tour.png caption="Basic Usage & Parameter Tour: Bottom-Up Matrix Indexing, Multi-Cell Spanning, Flexible Proportions, and Visibility (APNG Animation)"
from __future__ import annotations

from collections.abc import Callable
from typing import Any

from drawlib.anim import Animation
from drawlib.canvas import save, setup
from drawlib.icons import code as code_icons
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.smartarts import GridLayout, SourceCode, SourceCodeStyles
from drawlib.styles import Styles
from drawlib.text import text

W, H = 138.0, 82.0
setup(width=W, height=H)
anim = Animation(fps=10.0, loop=0)

CODE_TEXT_SIZE = 10.0
PT_TO_CANVAS = W / 720.0
FONT_CANVAS = CODE_TEXT_SIZE * PT_TO_CANVAS
LINE_H = FONT_CANVAS * 1.8
PAD_Y = FONT_CANVAS * 1.2

CODE_STYLES = SourceCodeStyles.get("default", font_lang="en", text_size=CODE_TEXT_SIZE).patch(
    box_style=Styles.Neutral.patch(shape_fill_color=(0, 0, 0, 0), shape_line_width=0),
)

PANE_HEADER = Styles.Neutral.patch(
    shape_fill_color=(238, 243, 250),
    shape_line_color=(203, 213, 225),
    shape_line_width=1.2,
    shape_r=0.0,
)
EDITOR_BODY = Styles.Neutral.patch(
    shape_fill_color=(250, 252, 255),
    shape_line_color=(203, 213, 225),
    shape_line_width=1.2,
    shape_r=0.0,
)
TAKEAWAY_BODY = Styles.Neutral.patch(
    shape_fill_color=(242, 246, 253),
    shape_line_color=(203, 213, 225),
    shape_line_width=1.2,
    shape_r=0.0,
)
STUDIO_BODY = Styles.Neutral.patch(
    shape_fill_color=(239, 243, 249),
    shape_line_color=(203, 213, 225),
    shape_line_width=1.2,
    shape_r=0.0,
)

PART_ITEMS = [
    ("1. Bottom-Up Grid", "(col, row) indexing"),
    ("2. Cell Spanning", "width & height spans"),
    ("3. Frame & Flexible", "outer_style & flexible"),
    ("4. Hide & Align", "show=False & center"),
]


def draw_step_bar(active_part: int) -> None:
    """Draw top 4-part progress bar (active_part is 1..4)."""
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
            tst = Styles.WhiteBold.patch(text_size=10.3)
            sub_tst = Styles.White.patch(text_size=9.5)
        elif idx < active_part:
            st = Styles.PrimaryNeutral.patch(shape_r=1.4, shape_line_width=1.1)
            tst = Styles.PrimaryBold.patch(text_size=10.3)
            sub_tst = Styles.Primary.patch(text_size=9.5)
        else:
            st = Styles.Neutral.patch(shape_r=1.4, shape_line_width=1.1)
            tst = Styles.MutedBold.patch(text_size=10.3)
            sub_tst = Styles.Muted.patch(text_size=9.5)

        rectangle((cx, cy), width=pill_w, height=pill_h, style=st)
        text((cx, cy + 1.35), label, style=tst)
        text((cx, cy - 1.55), sublabel, style=sub_tst)


def draw_left_pane(
    active_part: int,
    code_lines: list[str],
    hl_range: tuple[int, int],
    icon_fn: Callable[..., Any],
    summary_title: str,
    summary_line1: str,
    summary_line2: str,
) -> None:
    """Draw left Python code editor + bottom concept takeaway card."""
    x0, w = 4.0, 63.5
    cx = x0 + w / 2.0
    top_y = 63.2
    header_h = 5.4
    editor_h = 43.8
    takeaway_h = 15.8

    rectangle((cx, top_y + header_h / 2.0), width=w, height=header_h, style=PANE_HEADER)
    code_icons.python((x0 + 3.6, top_y + header_h / 2.0), width=3.4, style=Styles.Neutral)
    text(
        (x0 + 6.5, top_y + header_h / 2.0),
        "gridlayout_tour.py",
        style=Styles.DarkBold.patch(text_size=10.2, halign="left"),
    )
    text(
        (x0 + w - 2.6, top_y + header_h / 2.0),
        f"Part {active_part} / 4",
        style=Styles.PrimaryBold.patch(text_size=9.8, halign="right"),
    )

    rectangle((cx, top_y - editor_h / 2.0), width=w, height=editor_h, style=EDITOR_BODY)

    hl_start, hl_end = hl_range
    hl_top = top_y - PAD_Y - hl_start * LINE_H
    hl_bot = top_y - PAD_Y - (hl_end + 1) * LINE_H
    hl_cy = (hl_top + hl_bot) / 2.0
    hl_h = hl_top - hl_bot
    rectangle(
        (cx, hl_cy),
        width=w - 0.6,
        height=hl_h,
        style=Styles.Neutral.patch(shape_fill_color=(229, 239, 255), shape_line_width=0),
    )
    rectangle(
        (x0 + 0.55, hl_cy),
        width=0.9,
        height=hl_h,
        style=Styles.PrimaryFlat.patch(shape_line_width=0),
    )

    SourceCode.draw(
        xy=(x0, top_y),
        width=w,
        code="\n".join(code_lines),
        styles=CODE_STYLES,
        code_lang="python",
        show_linenum=True,
        align="top_left",
    )

    take_cy = 3.6 + takeaway_h / 2.0
    rectangle((cx, take_cy), width=w, height=takeaway_h, style=TAKEAWAY_BODY)
    circle(
        (x0 + 6.4, take_cy),
        radius=3.3,
        style=Styles.PrimaryNeutral.patch(shape_line_width=1.2),
    )
    icon_fn((x0 + 6.4, take_cy), width=3.8, style=Styles.PrimaryBold)
    text(
        (x0 + 11.4, take_cy + 3.6),
        summary_title,
        style=Styles.DarkBold.patch(text_size=10.4, halign="left"),
    )
    text(
        (x0 + 11.4, take_cy - 0.2),
        summary_line1,
        style=Styles.Dark.patch(text_size=9.7, halign="left"),
    )
    text(
        (x0 + 11.4, take_cy - 3.8),
        summary_line2,
        style=Styles.PrimaryBold.patch(text_size=9.6, halign="left"),
    )


def draw_geometry_studio(param_badge: str, footer_caption: str) -> tuple[float, float]:
    """Draw right geometry lab shell, inner coordinate sheet with subtle grid, and footer."""
    x0, w = 70.0, 64.0
    cx = x0 + w / 2.0
    top_y = 63.2
    header_h = 5.4
    body_h = 59.6

    rectangle((cx, top_y + header_h / 2.0), width=w, height=header_h, style=PANE_HEADER)
    phosphor.ruler((x0 + 3.6, top_y + header_h / 2.0), width=3.4, style=Styles.Primary)
    text(
        (x0 + 6.5, top_y + header_h / 2.0),
        "Live Geometry & Guides",
        style=Styles.DarkBold.patch(text_size=10.2, halign="left"),
    )
    text(
        (x0 + w - 2.6, top_y + header_h / 2.0),
        param_badge,
        style=Styles.PrimaryBold.patch(text_size=9.6, halign="right"),
    )

    rectangle((cx, 3.6 + body_h / 2.0), width=w, height=body_h, style=STUDIO_BODY)

    sheet_cx, sheet_cy = cx, 36.2
    sheet_w, sheet_h = 54.0, 40.0
    sx0, sy0 = sheet_cx - sheet_w / 2.0, sheet_cy - sheet_h / 2.0
    rectangle(
        (sheet_cx, sheet_cy),
        width=sheet_w,
        height=sheet_h,
        style=Styles.Neutral.patch(
            shape_fill_color=(255, 255, 255),
            shape_line_color=(180, 194, 214),
            shape_line_width=1.2,
        ),
    )
    g_st = Styles.MutedThin.patch(line_color=(232, 238, 246), line_width=0.8)
    for gx in range(1, 6):
        vx = sx0 + gx * (sheet_w / 6.0)
        line((vx, sy0), (vx, sy0 + sheet_h), style=g_st)
    for gy in range(1, 5):
        vy = sy0 + gy * (sheet_h / 5.0)
        line((sx0, vy), (sx0 + sheet_w, vy), style=g_st)

    rectangle(
        (cx, 8.4),
        width=59.2,
        height=5.2,
        style=Styles.Neutral.patch(
            shape_fill_color=(255, 255, 255),
            shape_line_color=(203, 213, 225),
            shape_line_width=1.1,
            shape_r=2.4,
        ),
        text=footer_caption,
        text_style=Styles.DarkBold.patch(text_size=9.8),
    )
    return sheet_cx, sheet_cy


def draw_sub_pills(scx: float, labels: list[str], active_idx: int) -> None:
    """Draw 3-step tracker pills near the top of the studio sheet."""
    pw, ph, pgap = 16.2, 4.2, 0.9
    p_start = scx - (3 * pw + 2 * pgap) / 2.0 + pw / 2.0
    for idx, lbl in enumerate(labels):
        px = p_start + idx * (pw + pgap)
        if idx == active_idx:
            pst = Styles.PrimaryFlat.patch(shape_r=1.2)
            ptst = Styles.WhiteBold.patch(text_size=9.5)
        elif idx < active_idx:
            pst = Styles.PrimaryNeutral.patch(shape_r=1.2, shape_line_width=1.0)
            ptst = Styles.PrimaryBold.patch(text_size=9.5)
        else:
            pst = Styles.Neutral.patch(shape_r=1.2, shape_line_width=1.0)
            ptst = Styles.Muted.patch(text_size=9.5)
        rectangle((px, 52.0), width=pw, height=ph, style=pst, text=lbl, text_style=ptst)


CELL_DARK = Styles.DarkBold.patch(text_size=10.0)
CELL_WHITE = Styles.WhiteBold.patch(text_size=10.0)
GHOST_SLOT = Styles.MutedDashed.patch(
    shape_fill_color=(248, 250, 252),
    shape_line_color=(180, 194, 214),
    shape_line_width=1.0,
    shape_r=1.2,
)

# =========================================================================
# Part 1: Bottom-Up Grid — (col, row) Zero-Indexed Matrix
# =========================================================================
INDEX_STATES = [
    (
        1,
        3.3,
        [
            "grid = GridLayout(",
            "    num_column=3, num_row=2,",
            "    style=Styles.Neutral,",
            "    text_style=Styles.DarkBold,",
            ")",
            "# (col=0, row=0) at bottom-left",
            "grid.add((0, 0), 1, 1,",
            '         text="(0, 0)")',
            "grid.draw(",
            "    xy=(10, 8), width=44,",
            "    height=22, margin=1.8)",
        ],
        (5, 10),
        "pos = (0, 0)",
        "Step 1: (0, 0) Anchors Bottom-Left Slot Next to xy=(10, 8)",
        "1. Bottom-Left Origin Slot (0, 0)",
        "xy=(x, y) pins the bottom-left grid corner by default",
        "col=0 is left-most column; row=0 is bottom-most row",
    ),
    (
        2,
        3.3,
        [
            "grid = GridLayout(",
            "    num_column=3, num_row=2, ...)",
            "grid.add((0, 0), 1, 1,",
            '         text="(0, 0)")',
            "# col increases +X rightward",
            "grid.add((1, 0), 1, 1,",
            '         text="(1, 0)",',
            "         style=Styles.PrimaryFlat)",
            "grid.draw((10, 8), 44, 22, 1.8)",
        ],
        (4, 7),
        "pos = (1, 0)",
        "Step 2: Column Index Increases +X Rightward to (1, 0)",
        "2. Rightward Column Indexing (+X)",
        "Column index steps 0 -> 1 -> 2 from left to right",
        "Each 1x1 cell occupies one equal matrix slot",
    ),
    (
        3,
        3.4,
        [
            "grid = GridLayout(",
            "    num_column=3, num_row=2, ...)",
            "grid.add((0, 0), 1, 1, ...)",
            "grid.add((1, 0), 1, 1, ...)",
            "# row increases +Y upward",
            "grid.add((2, 1), 1, 1,",
            '         text="(2, 1)",',
            "         style=Styles.PrimaryFlat)",
            "grid.draw((10, 8), 44, 22, 1.8)",
        ],
        (4, 7),
        "pos = (2, 1)",
        "Step 3: Row Index Increases +Y Upward to Top-Right (2, 1)",
        "3. Upward Row Indexing (+Y)",
        "Row index steps 0 -> 1 from bottom to top",
        "(num_column-1, num_row-1) lands at top-right corner",
    ),
]

for i_idx, (step_n, dur, code_i, hl_rng, badge_txt, foot_txt, s_t, s_1, s_2) in enumerate(INDEX_STATES):
    with anim.frame(duration=dur):
        draw_step_bar(1)
        draw_left_pane(1, code_i, hl_rng, phosphor.grid_four, s_t, s_1, s_2)
        scx, scy = draw_geometry_studio(badge_txt, foot_txt)
        draw_sub_pills(scx, ["Cell (0, 0)", "Row 0: (1, 0)", "Top-Right (2, 1)"], i_idx)

        gx0, gy0, gw, gh, m = 82.0, 22.8, 43.2, 20.6, 1.8
        cw = (gw - 2.0 * m) / 3.0
        rh = (gh - m) / 2.0

        # Faint ghost matrix slots + col/row index headers
        for c in range(3):
            cx_s = gx0 + c * (cw + m) + cw / 2.0
            text((cx_s, gy0 + gh + 2.2), f"col {c}", style=Styles.MutedBold.patch(text_size=9.5))
            for r in range(2):
                cy_s = gy0 + r * (rh + m) + rh / 2.0
                rectangle((cx_s, cy_s), width=cw, height=rh, style=GHOST_SLOT)
        for r in range(2):
            cy_s = gy0 + r * (rh + m) + rh / 2.0
            text((gx0 - 1.6, cy_s), f"r{r}", style=Styles.MutedBold.patch(text_size=9.5, halign="right"))

        grid = GridLayout(
            num_column=3,
            num_row=2,
            style=Styles.Neutral.patch(shape_r=1.2),
            text_style=CELL_DARK,
        )
        if step_n == 1:
            grid.add(
                (0, 0),
                1,
                1,
                text="(0, 0)",
                style=Styles.PrimaryFlat.patch(shape_r=1.2),
                text_style=CELL_WHITE,
            )
        elif step_n == 2:
            grid.add((0, 0), 1, 1, text="(0, 0)", style=Styles.PrimaryNeutral.patch(shape_r=1.2))
            grid.add(
                (1, 0),
                1,
                1,
                text="(1, 0)",
                style=Styles.PrimaryFlat.patch(shape_r=1.2),
                text_style=CELL_WHITE,
            )
        else:
            grid.add((0, 0), 1, 1, text="(0, 0)", style=Styles.PrimaryNeutral.patch(shape_r=1.2))
            grid.add((1, 0), 1, 1, text="(1, 0)")
            grid.add((2, 0), 1, 1, text="(2, 0)")
            grid.add((0, 1), 1, 1, text="(0, 1)")
            grid.add((1, 1), 1, 1, text="(1, 1)")
            grid.add(
                (2, 1),
                1,
                1,
                text="(2, 1)",
                style=Styles.PrimaryFlat.patch(shape_r=1.2),
                text_style=CELL_WHITE,
            )

        grid.draw((gx0, gy0), width=gw, height=gh, margin=m)

        line((gx0, gy0), (gx0, gy0 + 8.5), arrow_head="->", style=Styles.DangerBold.patch(line_width=1.4))
        line((gx0, gy0), (gx0 + 10.5, gy0), arrow_head="->", style=Styles.DangerBold.patch(line_width=1.4))
        circle((gx0, gy0), radius=1.2, style=Styles.DangerFlat)
        text(
            (gx0 + 21.0, 18.4),
            "xy = (10, 8) (bottom-left)",
            style=Styles.DangerBold.patch(text_size=9.5),
        )

# =========================================================================
# Part 2: Cell Spanning — Multi-Column & Multi-Row Spans on 3x3 Matrix
# =========================================================================
SPAN_STATES = [
    (
        1,
        3.3,
        [
            "grid = GridLayout(",
            "    num_column=3, num_row=3,",
            "    style=Styles.Neutral, ...)",
            "# Top row=2 spanning all 3 cols",
            "grid.add(",
            "    (0, 2), width=3, height=1,",
            '    text="Edge Ingress",',
            "    style=Styles.PrimaryFlat,",
            "    text_style=Styles.WhiteBold,",
            ")",
            "grid.draw((10, 8), 44, 25, 1.6)",
        ],
        (4, 9),
        "span 3 × 1",
        "add((0, 2), 3, 1): Top Header Spans All 3 Columns",
        "1. Full-Width Row Span (width=3, height=1)",
        "Starts at (col=0, row=2) and spans 3 columns right",
        "Ideal for top ingress layers and banner headers",
    ),
    (
        2,
        3.3,
        [
            "grid = GridLayout(",
            "    num_column=3, num_row=3, ...)",
            "grid.add((0, 2), 3, 1,",
            '         text="Edge Ingress", ...)',
            "# Left col=0 spanning rows 0..1",
            "grid.add(",
            "    (0, 0), width=1, height=2,",
            '    text="Auth",',
            "    style=Styles.PrimaryNeutral,",
            ")",
            "grid.draw((10, 8), 44, 25, 1.6)",
        ],
        (5, 9),
        "span 1 × 2",
        "add((0, 0), 1, 2): Left Sidebar Spans Rows 0 and 1 Upward",
        "2. Vertical Column Span (width=1, height=2)",
        "Starts at (0, 0) and spans 2 rows upward (rows 0..1)",
        "Great for cross-cutting auth or navigation sidebars",
    ),
    (
        3,
        3.4,
        [
            "grid = GridLayout(",
            "    num_column=3, num_row=3, ...)",
            "grid.add((0, 2), 3, 1, ...)",
            "grid.add((0, 0), 1, 2, ...)",
            "# 2x2 core across cols 1..2, 0..1",
            "grid.add(",
            "    (1, 0), width=2, height=2,",
            '    text="App Pool",',
            "    style=Styles.SecondaryNeutral",
            ")",
            "grid.draw((10, 8), 44, 25, 1.6)",
        ],
        (5, 9),
        "span 2 × 2",
        "add((1, 0), 2, 2): 2x2 Block Fills Columns 1..2 & Rows 0..1",
        "3. Multi-Axis Block Span (width=2, height=2)",
        "Merges 4 unit cells + internal gutters seamlessly",
        "Calm neutrals ground 67% of the 3x3 matrix area",
    ),
]

for sp_idx, (sp_step, dur, code_sp, hl_rng, badge_txt, foot_txt, s_t, s_1, s_2) in enumerate(SPAN_STATES):
    with anim.frame(duration=dur):
        draw_step_bar(2)
        draw_left_pane(2, code_sp, hl_rng, phosphor.squares_four, s_t, s_1, s_2)
        scx, scy = draw_geometry_studio(badge_txt, foot_txt)
        draw_sub_pills(scx, ["3×1 Top Span", "1×2 Left Span", "2×2 Core Span"], sp_idx)

        gx0, gy0, gw, gh, m = 80.0, 21.6, 44.0, 24.8, 1.6
        cw = (gw - 2.0 * m) / 3.0
        rh = (gh - 2.0 * m) / 3.0

        for c in range(3):
            for r in range(3):
                rectangle(
                    (gx0 + c * (cw + m) + cw / 2.0, gy0 + r * (rh + m) + rh / 2.0),
                    width=cw,
                    height=rh,
                    style=GHOST_SLOT,
                )

        grid = GridLayout(
            num_column=3,
            num_row=3,
            style=Styles.Neutral.patch(shape_r=1.3),
            text_style=CELL_DARK,
        )
        grid.add(
            (0, 2),
            3,
            1,
            text="Edge Ingress",
            style=Styles.PrimaryFlat.patch(shape_r=1.3),
            text_style=CELL_WHITE,
        )
        if sp_step >= 2:
            grid.add(
                (0, 0),
                1,
                2,
                text="Auth",
                style=Styles.PrimaryNeutral.patch(shape_r=1.3),
                text_style=Styles.PrimaryBold.patch(text_size=10.0),
            )
        if sp_step >= 3:
            grid.add(
                (1, 0),
                2,
                2,
                text="App Pool",
                style=Styles.SecondaryNeutral.patch(shape_r=1.3),
            )

        grid.draw((gx0, gy0), width=gw, height=gh, margin=m)

        if sp_step == 1:
            text((scx, 18.2), "pos=(0, 2), width=3, height=1  (cols 0..2)", style=Styles.PrimaryBold.patch(text_size=9.5))
        elif sp_step == 2:
            text((scx, 18.2), "pos=(0, 0), width=1, height=2  (rows 0..1)", style=Styles.PrimaryBold.patch(text_size=9.5))
        else:
            text(
                (scx, 18.2),
                "pos=(1, 0), width=2, height=2  (cols 1..2, rows 0..1)",
                style=Styles.DarkBold.patch(text_size=9.5),
            )

# =========================================================================
# Part 3: Frame & Flexible — outer_style & draw_flexible()
# =========================================================================
FLEX_STATES = [
    (
        "no_outer",
        3.3,
        [
            "grid = GridLayout(",
            "    num_column=3, num_row=2, ...)",
            'grid.add((0, 1), 1, 1, text="Nav")',
            "grid.add((1, 1), 1, 1, ...)",
            "# Equal cols & rows, no outer box",
            "grid.draw(",
            "    xy=(10, 8),",
            "    width=47, height=27,",
            "    margin=2.0,",
            ")",
        ],
        (5, 9),
        "outer_style=None",
        "outer_style=None: Equal Slots Flush With Outer Perimeter",
        "Uniform Grid (outer_style=None)",
        "Divides width=47 and height=27 into equal cells",
        "margin=2.0 applies only between adjacent cells",
    ),
    (
        "with_outer",
        3.4,
        [
            "grid = GridLayout(",
            "    num_column=3, num_row=2, ...)",
            "# Outer frame + perimeter margin",
            "grid.draw(",
            "    xy=(10, 8),",
            "    width=47, height=27,",
            "    margin=2.0,",
            "    outer_style=Styles.Neutral,",
            ")",
        ],
        (6, 7),
        "outer_style",
        "outer_style=Styles.Neutral: Outer Card & Perimeter Margin",
        "Container Backing (outer_style)",
        "Draws an outer backing card around the entire matrix",
        "Automatically adds margin=2.0 around all 4 outer sides",
    ),
    (
        "flexible",
        3.4,
        [
            "grid = GridLayout(",
            "    num_column=3, num_row=2, ...)",
            "grid.draw_flexible(",
            "    xy=(10, 8),",
            "    column_widths=[12, 16, 12],",
            "    column_margins=[",
            "        1.5, 2.0, 2.0, 1.5],",
            "    row_heights=[9, 13],",
            "    row_margins=[1.5, 2.0, 1.5],",
            "    outer_style=Styles.Neutral,",
            ")",
        ],
        (2, 10),
        "draw_flexible()",
        "draw_flexible(): Custom Column [12, 16, 12] & Row [9, 13] Sizes",
        "Asymmetric Tracks (draw_flexible)",
        "Explicit column_widths (N) and column_margins (N+1)",
        "Explicit row_heights (M) and row_margins (M+1)",
    ),
]

for fl_idx, (fl_mode, dur, code_fl, hl_rng, badge_txt, foot_txt, s_t, s_1, s_2) in enumerate(FLEX_STATES):
    with anim.frame(duration=dur):
        draw_step_bar(3)
        draw_left_pane(3, code_fl, hl_rng, phosphor.columns, s_t, s_1, s_2)
        scx, scy = draw_geometry_studio(badge_txt, foot_txt)
        draw_sub_pills(scx, ["No Outer Frame", "outer_style", "draw_flexible()"], fl_idx)

        grid = GridLayout(
            num_column=3,
            num_row=2,
            style=Styles.Neutral.patch(
                shape_fill_color=(255, 255, 255),
                shape_line_color=(180, 194, 214),
                shape_line_width=1.1,
                shape_r=1.2,
            ),
            text_style=Styles.DarkBold.patch(text_size=9.7),
        )
        grid.add((0, 1), 1, 1, text="Nav", style=Styles.PrimaryNeutral.patch(shape_r=1.2))
        grid.add(
            (1, 1),
            1,
            1,
            text="Main View",
            style=Styles.PrimaryFlat.patch(shape_r=1.2),
            text_style=Styles.WhiteBold.patch(text_size=9.7),
        )
        grid.add((2, 1), 1, 1, text="Logs", style=Styles.PrimaryNeutral.patch(shape_r=1.2))
        grid.add((0, 0), 1, 1, text="Auth")
        grid.add((1, 0), 1, 1, text="Metrics")
        grid.add((2, 0), 1, 1, text="Alerts")

        outer_st = Styles.Neutral.patch(
            shape_fill_color=(235, 241, 248),
            shape_line_color=(148, 163, 184),
            shape_line_width=1.3,
            shape_r=1.6,
        )

        if fl_mode == "no_outer":
            gx0, gy0 = 78.5, 20.6
            grid.draw((gx0, gy0), width=47.0, height=25.5, margin=2.0)
            text((scx, 18.0), "Equal columns & rows (flush outer edges)", style=Styles.MutedBold.patch(text_size=9.5))
        elif fl_mode == "with_outer":
            gx0, gy0 = 78.5, 20.6
            grid.draw((gx0, gy0), width=47.0, height=25.5, margin=2.0, outer_style=outer_st)
            text(
                (scx, 18.0),
                "outer_style backing + 2.0 perimeter padding",
                style=Styles.PrimaryBold.patch(text_size=9.5),
            )
        else:
            gx0, gy0 = 77.2, 18.0
            c_w = [12.0, 16.0, 12.0]
            c_m = [1.5, 2.0, 2.0, 1.5]
            r_h = [9.0, 13.0]
            r_m = [1.5, 2.0, 1.5]
            grid.draw_flexible(
                xy=(gx0, gy0),
                column_widths=c_w,
                column_margins=c_m,
                row_heights=r_h,
                row_margins=r_m,
                outer_style=outer_st,
            )
            # Column width labels above top edge (gy0 + 27 = 45.0)
            x_cur = gx0 + c_m[0]
            for idx_c, w_val in enumerate(c_w):
                text(
                    (x_cur + w_val / 2.0, 47.1),
                    f"w={int(w_val)}",
                    style=Styles.PrimaryBold.patch(text_size=9.5),
                )
                if idx_c < 2:
                    x_cur += w_val + c_m[idx_c + 1]
            # Row height labels on right (gx0 + 47 = 124.2)
            text(
                (gx0 + 48.0, gy0 + r_m[0] + r_h[0] / 2.0),
                "9",
                style=Styles.DangerBold.patch(text_size=9.5, halign="left"),
            )
            text(
                (gx0 + 48.0, gy0 + r_m[0] + r_h[0] + r_m[1] + r_h[1] / 2.0),
                "13",
                style=Styles.DangerBold.patch(text_size=9.5, halign="left"),
            )

# =========================================================================
# Part 4: Hide & Align — grid.items[1].show = False & align="center"
# =========================================================================
HIDE_ALIGN_STATES = [
    (
        "all_shown",
        3.3,
        [
            "grid = GridLayout(",
            "    num_column=3, num_row=2, ...)",
            'grid.add((0, 1), 1, 1, text="API")',
            "grid.add((1, 1), 1, 1,",
            '         text="Cache")',
            'grid.add((2, 1), 1, 1, text="MQ")',
            "grid.add((0, 0), 3, 1, ...)",
            "# Inspect mutable GridItem list",
            "grid.draw((10, 8), 44, 22, 1.8)",
        ],
        (3, 7),
        "grid.items[0..3]",
        "All 4 GridItem Models Registered in grid.items",
        "Inspectable Cell List (grid.items)",
        ".add() returns & stores mutable GridItem models",
        "items[1] corresponds to 'Cache' at pos=(1, 1)",
    ),
    (
        "hide_cell",
        3.4,
        [
            "grid = GridLayout(",
            "    num_column=3, num_row=2, ...)",
            'grid.add((0, 1), 1, 1, text="API")',
            "grid.add((1, 1), 1, 1, ...)",
            'grid.add((2, 1), 1, 1, text="MQ")',
            "grid.add((0, 0), 3, 1, ...)",
            "# Hide cell; matrix stays fixed!",
            "grid.items[1].show = False",
            "grid.draw((10, 8), 44, 22, 1.8)",
        ],
        (6, 7),
        "items[1].show=False",
        "items[1].show = False Hides Cell Without Shifting Matrix",
        "Slot-Preserving Hide (.show = False)",
        "Skips rendering items[1] while keeping 3x2 coordinates",
        "Neighboring 'API' and 'MQ' stay pinned in place",
    ),
    (
        "center_align",
        3.5,
        [
            "grid = GridLayout(",
            "    num_column=3, num_row=2, ...)",
            'grid.add((0, 1), 1, 1, text="API")',
            "grid.add((1, 1), 1, 1, ...)",
            'grid.add((2, 1), 1, 1, text="MQ")',
            "grid.add((0, 0), 3, 1, ...)",
            "# Center entire grid on (cx, cy)",
            "grid.draw(",
            "    xy=(32, 20), width=44,",
            "    height=22, margin=1.8,",
            '    align="center")',
        ],
        (7, 10),
        'align = "center"',
        "grid.draw(..., align='center') Centers Matrix on (cx, cy)",
        'Centered Matrix Anchor (align="center")',
        "Centers total width & height symmetrically on xy",
        "Supported by both draw() and draw_flexible()",
    ),
]

for h_idx, (h_mode, dur, code_h, hl_rng, badge_txt, foot_txt, s_t, s_1, s_2) in enumerate(HIDE_ALIGN_STATES):
    with anim.frame(duration=dur):
        draw_step_bar(4)
        draw_left_pane(4, code_h, hl_rng, phosphor.eye_slash, s_t, s_1, s_2)
        scx, scy = draw_geometry_studio(badge_txt, foot_txt)
        draw_sub_pills(scx, ["grid.items[i]", "show = False", 'align="center"'], h_idx)

        gw, gh, m = 44.0, 22.0, 1.8
        cw = (gw - 2.0 * m) / 3.0
        rh = (gh - m) / 2.0

        grid = GridLayout(
            num_column=3,
            num_row=2,
            style=Styles.Neutral.patch(shape_r=1.2),
            text_style=CELL_DARK,
        )
        grid.add((0, 1), 1, 1, text="API", style=Styles.PrimaryNeutral.patch(shape_r=1.2))
        if h_mode == "center_align":
            grid.add((1, 1), 1, 1, text="Cache", style=Styles.PrimaryNeutral.patch(shape_r=1.2))
        else:
            grid.add(
                (1, 1),
                1,
                1,
                text="Cache",
                style=Styles.PrimaryFlat.patch(shape_r=1.2),
                text_style=CELL_WHITE,
            )
        grid.add((2, 1), 1, 1, text="MQ", style=Styles.PrimaryNeutral.patch(shape_r=1.2))
        grid.add((0, 0), 3, 1, text="Shared Storage Tier", style=Styles.SecondaryNeutral.patch(shape_r=1.2))

        if h_mode == "all_shown":
            gx0, gy0 = 80.0, 21.8
            grid.draw((gx0, gy0), width=gw, height=gh, margin=m)
            mid_cx = gx0 + cw + m + cw / 2.0
            rectangle(
                (mid_cx, 46.8),
                width=14.6,
                height=3.6,
                style=Styles.PrimaryFlat.patch(shape_r=1.0),
                text="items[1]",
                text_style=Styles.WhiteBold.patch(text_size=9.5),
            )
            text((scx, 18.2), "4 mutable GridItem models in grid.items", style=Styles.DarkBold.patch(text_size=9.5))
        elif h_mode == "hide_cell":
            gx0, gy0 = 80.0, 21.8
            grid.items[1].show = False
            grid.draw((gx0, gy0), width=gw, height=gh, margin=m)
            mid_cx = gx0 + cw + m + cw / 2.0
            mid_cy = gy0 + rh + m + rh / 2.0
            rectangle(
                (mid_cx, mid_cy),
                width=cw,
                height=rh,
                style=Styles.MutedDashed.patch(
                    shape_fill_color=(248, 250, 252),
                    shape_line_color=(148, 163, 184),
                    shape_line_width=1.3,
                    shape_r=1.2,
                ),
                text="slot\npreserved",
                text_style=Styles.MutedBold.patch(text_size=9.5),
            )
            text(
                (scx, 18.2),
                "items[1] hidden • neighbor coordinates unchanged",
                style=Styles.PrimaryBold.patch(text_size=9.5),
            )
        else:
            cx_g, cy_g = scx, 34.2
            grid.draw((cx_g, cy_g), width=gw, height=gh, margin=m, align="center")
            rectangle(
                (cx_g, cy_g),
                width=gw,
                height=gh,
                style=Styles.PrimaryDashed.patch(shape_fill_color=(0, 0, 0, 0), shape_line_width=1.3),
            )
            line((cx_g - 24.6, cy_g), (cx_g - 22.0, cy_g), style=Styles.DangerBold.patch(line_width=1.5))
            line((cx_g + 22.0, cy_g), (cx_g + 24.6, cy_g), style=Styles.DangerBold.patch(line_width=1.5))
            line((cx_g, cy_g + 11.0), (cx_g, cy_g + 13.6), style=Styles.DangerBold.patch(line_width=1.5))
            line((cx_g, cy_g - 13.6), (cx_g, cy_g - 11.0), style=Styles.DangerBold.patch(line_width=1.5))
            circle(
                (cx_g, cy_g),
                radius=1.6,
                style=Styles.Neutral.patch(shape_fill_color=(255, 255, 255), shape_line_width=0),
            )
            circle((cx_g, cy_g), radius=1.15, style=Styles.DangerFlat)
            text(
                (cx_g, 18.2),
                'xy = (32, 20)  •  align="center"',
                style=Styles.DangerBold.patch(text_size=9.5),
            )

save()
```

- **Bottom-Up `(col, row)` Matrix (`xy`, `num_column`, `num_row`)**: Anchor at **Bottom-Left `xy`** by default (`align="bottom_left"`), where `col = 0` starts at the left edge (`+X` rightward) and `row = 0` starts at the bottom edge (`+Y` upward).
- **Multi-Cell Spanning (`.add((col, row), width, height)`)**: Merge `width` columns rightward and `height` rows upward seamlessly across internal gutters to compose banner headers, sidebars, and multi-slot cores.
- **Outer Backing & Flexible Tracks (`outer_style`, `draw_flexible`)**: Pass `outer_style` to wrap the matrix in a padded container card, or call `draw_flexible(...)` with explicit `column_widths`, `column_margins`, `row_heights`, and `row_margins`.
- **Slot-Preserving Visibility & Centering (`items[i].show`, `align="center"`)**: Set `grid.items[i].show = False` to hide a cell without shifting matrix coordinates, or pass `align="center"` to center the entire grid on `xy`.

---

## 2. Multi-Span Architecture & Dashboard Layout (`draw`)

In standard mode (`grid.draw(...)`), `GridLayout` divides the total `width` and `height` evenly across `num_column` columns and `num_row` rows with a uniform `margin` gutter between cells. If `outer_style` is provided, an outer container frame is drawn with an inner margin around the perimeter.

```drawlib code=show align=center file=smartarts_gridlayout_architecture.png caption="Multi-Tier Cloud Architecture with GridLayout Cell Spanning"
from drawlib.canvas import save, setup
from drawlib.smartarts import GridLayout
from drawlib.styles import Styles

setup(width=118, height=68)

grid = GridLayout(
    num_column=4,
    num_row=4,
    style=Styles.Neutral.patch(shape_r=1.5),
    text_style=Styles.DarkBold.patch(text_size=10.0),
)

# Row 3 (Top): Edge Ingress spanning all 4 columns (Hero focal layer)
grid.add(
    position=(0, 3),
    width=4,
    height=1,
    text="Edge Ingress: CDN & WAF Gateway",
    style=Styles.PrimaryFlat.patch(shape_r=1.5),
    text_style=Styles.WhiteBold.patch(text_size=10.5),
)

# Row 2: Application Services Layer
grid.add(position=(0, 2), width=2, height=1, text="Order & Checkout API", style=Styles.PrimaryNeutral.patch(shape_r=1.5))
grid.add(position=(2, 2), width=1, height=1, text="Auth API", style=Styles.PrimaryNeutral.patch(shape_r=1.5))
grid.add(position=(3, 2), width=1, height=1, text="Worker", style=Styles.PrimaryNeutral.patch(shape_r=1.5))

# Row 1: Persistence & Caching Tier
grid.add(position=(0, 1), width=1, height=1, text="PostgreSQL", style=Styles.SecondaryNeutral.patch(shape_r=1.5))
grid.add(position=(1, 1), width=1, height=1, text="OpenSearch", style=Styles.SecondaryNeutral.patch(shape_r=1.5))
grid.add(position=(2, 1), width=2, height=1, text="Redis Cluster (Multi-AZ)", style=Styles.SecondaryNeutral.patch(shape_r=1.5))

# Row 0 (Bottom): Shared Infrastructure Foundation
grid.add(
    position=(0, 0),
    width=4,
    height=1,
    text="Kubernetes Platform Foundation (Multi-Region)",
    style=Styles.Neutral.patch(shape_r=1.5),
)

grid.draw(
    xy=(6, 6),
    width=106,
    height=56,
    margin=1.8,
    outer_style=Styles.MutedDashed.patch(shape_r=2.0),
)
save()
```

---

## 3. Flexible Grid Sizing & Custom Cell Overlays (`draw_flexible`)

When columns or rows require asymmetric proportions (such as a narrow sidebar next to a wide content area, or a compact header row), use `grid.draw_flexible(...)` with explicit `column_widths`, `column_margins`, `row_heights`, and `row_margins`. Because the cell positions are deterministic from `xy`, you can also overlay standard icons and shapes inside any cell.

```drawlib code=show align=center file=smartarts_gridlayout_flexible_icons.png caption="Flexible Dashboard Grid with Custom Column/Row Proportions and Icon Overlays"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.smartarts import GridLayout
from drawlib.styles import Styles

setup(width=116, height=62)

grid = GridLayout(
    num_column=3,
    num_row=3,
    style=Styles.Neutral.patch(shape_r=1.5),
    text_style=Styles.DarkBold.patch(text_size=10.0),
)

# Top Header (Row 2, spanning 3 columns)
grid.add(
    position=(0, 2),
    width=3,
    height=1,
    text="Observability Control Plane",
    style=Styles.PrimaryFlat.patch(shape_r=1.5),
    text_style=Styles.WhiteBold.patch(text_size=11.0),
)

# Left Navigation Sidebar (Column 0, spanning Rows 0..1)
grid.add(
    position=(0, 0),
    width=1,
    height=2,
    text="Routing\n&\nPolicies",
    style=Styles.PrimaryNeutral.patch(shape_r=1.5),
)

# Main Content Cards (Columns 1..2, Rows 0..1)
grid.add(position=(1, 1), width=1, height=1, text="      Metrics Store", style=Styles.Neutral.patch(shape_r=1.5))
grid.add(position=(2, 1), width=1, height=1, text="      Trace Collector", style=Styles.Neutral.patch(shape_r=1.5))
grid.add(
    position=(1, 0),
    width=2,
    height=1,
    text="      Alerting & Incident Automation Engine",
    style=Styles.SecondaryNeutral.patch(shape_r=1.5),
)

# Render with custom column widths [24, 38, 38] and row heights [16, 16, 11]
grid.draw_flexible(
    xy=(4, 5),
    column_widths=[24.0, 38.0, 38.0],
    column_margins=[2.0, 2.0, 2.0, 2.0],
    row_heights=[16.0, 16.0, 11.0],
    row_margins=[2.0, 2.0, 2.0, 2.0],
    outer_style=Styles.MutedDashed.patch(shape_r=2.0),
)

# Overlay Phosphor icons inside the metric/trace/alert cells using deterministic coordinates
phosphor.chart_bar(xy=(36, 33), width=4.0, style=Styles.PrimaryFlat)
phosphor.activity(xy=(76, 33), width=4.0, style=Styles.PrimaryFlat)
phosphor.bell_ringing(xy=(40, 15), width=4.0, style=Styles.DarkBold)
save()
```

---

## 4. Coordinate & Indexing Rules

As illustrated in the opening diagram at the top of this page:

- **Bottom-Left Anchor `(x, y)`**: The `xy` coordinate passed to `draw()` or `draw_flexible()` specifies the **bottom-left corner** of the overall grid.
- **Zero-Indexed Bottom-Up Rows**:
  - `column_start = 0` is the **left-most column**, increasing rightward (`0` to `num_column - 1`).
  - `row_start = 0` is the **bottom-most row**, increasing upward (`0` to `num_row - 1`).
- **Cell Spanning**: `grid.add(position=(col, row), width=w, height=h)` spans `w` columns rightward (`col` through `col + w - 1`) and `h` rows upward (`row` through `row + h - 1`).

---

## 5. API Reference

### Constructor
```python
GridLayout(
    *,
    num_column: int,
    num_row: int,
    style: Style,
    text_style: Style,
)
```

### Methods & Properties
- **`add(position: tuple[int, int], width: int, height: int, *, style: Style | None = None, text: str = "", text_style: Style | None = None, show: bool = True) -> GridItem`**:
  Registers a grid card at `position=(column_start, row_start)` spanning `width` columns and `height` rows. Returns a mutable `GridItem` (`position`, `width`, `height`, `style`, `text`, `text_style`, `show`). Setting `show=False` hides the cell while keeping the matrix layout intact.
- **`grid.items -> list[GridItem]`**:
  Returns the list of all registered `GridItem` instances (`position: tuple[int, int]`, `width: int`, `height: int`, `style: Style`, `text: str`, `text_style: Style`, `show: bool`), allowing deferred mutation before or between `draw()` calls.
- **`draw(xy: tuple[float, float], width: float, height: float, margin: float, outer_style: Style | None = None, scale: float = 1.0) -> None`**:
  Renders the grid with equal column widths and equal row heights separated by `margin`. If `outer_style` is provided, draws an outer container rectangle and adds `margin` padding around the outer perimeter.
- **`draw_flexible(xy: tuple[float, float], column_widths: list[float], column_margins: list[float], row_heights: list[float], row_margins: list[float], outer_style: Style | None = None, scale: float = 1.0) -> None`**:
  Renders the grid using explicit column widths (`len == num_column`), column margins (`len == num_column + 1`), row heights (`len == num_row`), and row margins (`len == num_row + 1`).

