# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Shared visual building blocks for Drawlib OGP / Social Preview (1280x640) banners."""

from __future__ import annotations

from pathlib import Path

from drawlib.canvas import setup
from drawlib.fonts import FontRoboto, FontSansSerif, FontSourceCode
from drawlib.icons import ai, devops, phosphor, workspace
from drawlib.images import image
from drawlib.lines import line
from drawlib.shapes import circle, cloud, cylinder, document, rectangle
from drawlib.styles import Colors, Style, Styles
from drawlib.text import text

ASSETS_DIR = Path(__file__).resolve().parent / "_assets"

# 10.0 in * 128 dpi = 1280 px width, 5.0 in * 128 dpi = 640 px height
OGP_W: int = 128
OGP_H: int = 64
OGP_DPI: int = 128


def setup_ogp(*, is_dark: bool = False) -> None:
    """Configure an exact 1280x640 px OGP canvas."""
    bg = (15, 23, 42) if is_dark else (244, 247, 251)
    setup(width=OGP_W, height=OGP_H, dpi=OGP_DPI, background_color=bg)


def draw_top_brand_bar(
    headline: str = "Illustration & Docs as Code for AI Agents",
    *,
    is_dark: bool = False,
    top_y: float = 56.4,
) -> None:
    """Draw the top Drawlib logo + bold headline."""
    logo_file = ASSETS_DIR / ("logo_dark_transparent.png" if is_dark else "logo_transparent.png")
    image((24.0, top_y), width=31.0, image=str(logo_file))
    headline_color = Colors.White if is_dark else (15, 23, 42)
    text(
        (43.5, top_y - 0.4),
        headline,
        style=Styles.DarkBold.patch(
            text_font=FontSansSerif.POPPINS_BOLD,
            text_size=16.5,
            text_color=headline_color,
            halign="left",
            valign="center",
        ),
    )


def draw_soft_card(
    xy: tuple[float, float],
    width: float,
    height: float,
    *,
    fill: tuple[int, int, int] = (255, 255, 255),
    border: tuple[int, int, int] | None = (226, 232, 240),
    r: float = 2.8,
    is_dark: bool = False,
) -> None:
    """Draw a rounded card with subtle multi-step drop shadow."""
    cx, cy = xy
    if is_dark:
        shadow_outer = (8, 13, 26, 0.55)
        shadow_inner = (8, 13, 26, 0.35)
    else:
        shadow_outer = (148, 163, 184, 0.16)
        shadow_inner = (148, 163, 184, 0.26)

    rectangle(
        (cx + 0.35, cy - 0.85),
        width=width + 0.8,
        height=height + 0.8,
        style=Styles.Neutral.patch(shape_fill_color=shadow_outer, shape_line_width=0.0, shape_r=r + 0.3),
    )
    rectangle(
        (cx + 0.2, cy - 0.45),
        width=width + 0.2,
        height=height + 0.2,
        style=Styles.Neutral.patch(shape_fill_color=shadow_inner, shape_line_width=0.0, shape_r=r + 0.1),
    )
    line_w = 1.2 if border is not None else 0.0
    line_c = border if border is not None else fill
    rectangle(
        xy,
        width=width,
        height=height,
        style=Styles.Neutral.patch(
            shape_fill_color=fill,
            shape_line_color=line_c,
            shape_line_width=line_w,
            shape_r=r,
        ),
    )


def draw_folded_file_icon(
    xy: tuple[float, float],
    width: float,
    height: float,
    label: str,
    *,
    fill: tuple[int, int, int] = (241, 245, 249),
    stroke: tuple[int, int, int] = (51, 65, 85),
    bar_color: tuple[int, int, int] = (186, 198, 212),
) -> None:
    """Draw a dog-eared file card (.md / .py) with horizontal skeleton lines."""
    cx, cy = xy
    document(
        xy,
        width=width,
        height=height,
        variant="folded",
        fold_ratio=0.26,
        style=Styles.Neutral.patch(
            shape_fill_color=fill,
            shape_line_color=stroke,
            shape_line_width=1.5,
        ),
    )
    text(
        (cx, cy + height * 0.08),
        label,
        style=Styles.DarkBold.patch(
            text_font=FontRoboto.ROBOTO_BOLD,
            text_size=13.5,
            text_color=(15, 23, 42),
        ),
    )
    left_x = cx - width * 0.30
    for idx, frac in enumerate([0.60, 0.52, 0.38]):
        by = cy - height * (0.16 + idx * 0.10)
        line(
            (left_x, by),
            (left_x + width * frac, by),
            style=Style(line_color=bar_color, line_width=2.2),
        )


def draw_flow_arrow(
    start_x: float,
    end_x: float,
    y: float,
    *,
    is_dark: bool = False,
) -> None:
    """Draw a crisp bold horizontal pipeline arrow."""
    arrow_color = (203, 213, 225) if is_dark else (30, 41, 59)
    line(
        (start_x, y),
        (end_x, y),
        arrow_head="->",
        style=Styles.DarkBold.patch(line_color=arrow_color, line_width=3.2),
    )


def draw_mini_docs_browser(
    xy: tuple[float, float],
    width: float = 25.0,
    height: float = 20.5,
    *,
    title_label: str = "Cloud architecture",
) -> None:
    """Draw a mini browser window rendering an illustrated documentation page."""
    cx, cy = xy
    x0 = cx - width / 2.0
    y0 = cy - height / 2.0
    top_y = cy + height / 2.0

    rectangle(
        (cx + 0.3, cy - 0.5),
        width=width + 0.4,
        height=height + 0.4,
        style=Styles.Neutral.patch(shape_fill_color=(15, 23, 42, 0.16), shape_line_width=0.0, shape_r=1.5),
    )
    rectangle(
        xy,
        width=width,
        height=height,
        style=Styles.Neutral.patch(
            shape_fill_color=(255, 255, 255),
            shape_line_color=(71, 85, 105),
            shape_line_width=1.3,
            shape_r=1.4,
        ),
    )

    bar_h = 2.6
    rectangle(
        (cx, top_y - bar_h / 2.0),
        width=width,
        height=bar_h,
        style=Styles.Neutral.patch(
            shape_fill_color=(49, 100, 244),
            shape_line_color=(71, 85, 105),
            shape_line_width=1.1,
            shape_r=1.1,
        ),
    )
    rectangle(
        (cx, top_y - bar_h + 0.55),
        width=width - 0.4,
        height=1.1,
        style=Styles.Neutral.patch(shape_fill_color=(49, 100, 244), shape_line_width=0.0, shape_r=0.0),
    )
    line((x0, top_y - bar_h), (x0 + width, top_y - bar_h), style=Style(line_color=(71, 85, 105), line_width=1.0))

    for idx in range(3):
        circle(
            (x0 + 1.5 + idx * 1.15, top_y - bar_h / 2.0),
            radius=0.35,
            style=Styles.Neutral.patch(shape_fill_color=(255, 255, 255), shape_line_width=0.0),
        )

    side_w = width * 0.23
    line(
        (x0 + side_w, y0 + 0.3),
        (x0 + side_w, top_y - bar_h),
        style=Style(line_color=(226, 232, 240), line_width=0.9),
    )
    for idx in range(6):
        ly = top_y - bar_h - 2.2 - idx * 1.9
        if ly <= y0 + 0.8:
            break
        lw = side_w * (0.62 if idx != 1 else 0.72)
        lc = (59, 130, 246) if idx == 1 else (203, 213, 225)
        line((x0 + 1.0, ly), (x0 + 1.0 + lw, ly), style=Style(line_color=lc, line_width=1.6))

    scale = width / 25.0
    content_x0 = x0 + side_w + 1.2 * scale
    content_cx = (x0 + side_w + x0 + width) / 2.0

    effective_title = "Architecture" if (width < 20.0 and title_label == "Cloud architecture") else title_label
    text(
        (content_x0, top_y - bar_h - 1.9 * scale),
        effective_title,
        style=Styles.DarkBold.patch(
            text_font=FontRoboto.ROBOTO_BOLD,
            text_size=max(6.8, 7.5 * scale),
            text_color=(30, 41, 59),
            halign="left",
            valign="center",
        ),
    )
    line(
        (content_x0, top_y - bar_h - 3.2 * scale),
        (x0 + width - 1.6 * scale, top_y - bar_h - 3.2 * scale),
        style=Style(line_color=(226, 232, 240), line_width=1.2),
    )

    diag_cy = cy - 0.5 * scale
    diag_w = width - side_w - 2.4 * scale
    diag_h = height * 0.46
    rectangle(
        (content_cx, diag_cy),
        width=diag_w,
        height=diag_h,
        style=Style(
            shape_fill_color=(248, 250, 252),
            shape_line_color=(226, 232, 240),
            shape_line_width=0.8,
            shape_r=0.8 * scale,
        ),
    )

    cloud_y = diag_cy + diag_h * 0.22
    cloud(
        (content_cx, cloud_y),
        width=diag_w * 0.46,
        height=diag_h * 0.38,
        style=Style(
            shape_fill_color=(224, 242, 254),
            shape_line_color=(100, 116, 139),
            shape_line_width=0.85,
        ),
    )
    cylinder(
        (content_cx, cloud_y - 0.1 * scale),
        width=diag_w * 0.12,
        height=diag_h * 0.22,
        disks=2,
        style=Style(
            shape_fill_color=(59, 130, 246),
            shape_line_color=(30, 64, 175),
            shape_line_width=0.65,
        ),
    )

    node_y = diag_cy - diag_h * 0.29
    bus_y = diag_cy - diag_h * 0.08
    line(
        (content_cx, cloud_y - diag_h * 0.17),
        (content_cx, bus_y),
        style=Style(line_color=(100, 116, 139), line_width=0.85),
    )
    dx = diag_w * 0.32
    xs = [content_cx - dx, content_cx - dx / 3.0, content_cx + dx / 3.0, content_cx + dx]
    line((xs[0], bus_y), (xs[-1], bus_y), style=Style(line_color=(100, 116, 139), line_width=0.85))
    node_fills = [(35, 148, 155), (59, 102, 245), (59, 102, 245), (35, 148, 155)]
    for nx, nf in zip(xs, node_fills, strict=True):
        line((nx, bus_y), (nx, node_y + diag_h * 0.09), style=Style(line_color=(100, 116, 139), line_width=0.85))
        cylinder(
            (nx, node_y),
            width=diag_w * 0.13,
            height=diag_h * 0.19,
            style=Style(shape_fill_color=nf, shape_line_color=(51, 65, 85), shape_line_width=0.65),
        )

    for idx, frac in enumerate([0.75, 0.58]):
        py = y0 + (2.1 - idx * 1.0) * scale
        line(
            (content_x0, py),
            (content_x0 + diag_w * frac, py),
            style=Style(line_color=(203, 213, 225), line_width=1.2),
        )


def draw_git_repo_3col_ogp(
    *,
    left_title: str = "Source",
    left_sub: str = "App Code & Specs",
    center_title: str = "Doc Code (.md / .py)",
    center_title_size: float = 13.2,
    right_title: str = "Output",
    right_sub: str = "Site, Doc, Slide",
) -> None:
    """Draw the 3-column Git Repo OGP banner onto the current canvas."""
    setup_ogp(is_dark=False)
    draw_top_brand_bar("Illustration & Docs as Code for AI Agents", top_y=56.5)

    # Outer Frame: Git Repo • Single Source of Truth (x=5.0..123.0, y=4.8..44.4)
    # Perimeter margins: left=5.0, right=5.0, bottom=4.8
    rectangle(
        (64.0, 24.6),
        width=118.0,
        height=39.6,
        style=Styles.Neutral.patch(
            shape_fill_color=(233, 240, 248),
            shape_line_color=(148, 163, 184),
            shape_line_width=1.5,
            shape_line_style="dashed",
            shape_r=3.2,
        ),
    )

    # Prominent Floating Pill Badge on Outer Frame
    rectangle(
        (30.2, 44.4),
        width=43.4,
        height=6.0,
        style=Styles.Neutral.patch(
            shape_fill_color=Colors.White,
            shape_line_color=(148, 163, 184),
            shape_line_width=1.4,
            shape_r=3.0,
        ),
    )
    devops.github((12.0, 44.4), width=4.3, style=Styles.Dark)
    text(
        (15.3, 44.4),
        "Git Repo  •  Single Source of Truth",
        style=Styles.DarkBold.patch(
            text_font=FontRoboto.ROBOTO_BOLD,
            text_size=12.6,
            text_color=(15, 23, 42),
            halign="left",
            valign="center",
        ),
    )

    # Stage 1 (Left) — y=6.7..39.5 (cy=23.1, height=32.8)
    draw_soft_card((22.8, 23.1), 28.6, 32.8)
    text(
        (22.8, 35.8),
        left_title,
        style=Styles.DarkBold.patch(
            text_font=FontSansSerif.POPPINS_BOLD,
            text_size=14.0,
            text_color=(15, 23, 42),
        ),
    )
    rectangle(
        (22.8, 23.1),
        width=22.8,
        height=15.0,
        style=Styles.Neutral.patch(
            shape_fill_color=(30, 41, 59),
            shape_line_color=(71, 85, 105),
            shape_line_width=1.1,
            shape_r=1.6,
        ),
    )
    for idx, dot_c in enumerate([(248, 113, 113), (251, 191, 36), (52, 211, 153)]):
        circle(
            (13.5 + idx * 1.4, 28.8),
            radius=0.42,
            style=Styles.Neutral.patch(shape_fill_color=dot_c, shape_line_width=0.0),
        )
    text(
        (13.2, 25.3),
        "src/app/",
        style=Styles.DarkBold.patch(
            text_font=FontSourceCode.ROBOTO_MONO,
            text_size=10.2,
            text_color=(147, 197, 253),
            halign="left",
            valign="center",
        ),
    )
    for idx, (bar_w, bar_c) in enumerate([(13.8, (148, 163, 184)), (16.8, (96, 165, 250)), (10.8, (94, 234, 212))]):
        by = 21.9 - idx * 2.1
        line((14.4, by), (14.4 + bar_w, by), style=Style(line_color=bar_c, line_width=2.2))
    text(
        (22.8, 10.4),
        left_sub,
        style=Styles.DarkBold.patch(
            text_font=FontRoboto.ROBOTO_BOLD,
            text_size=11.0,
            text_color=(71, 85, 105),
        ),
    )

    # Stage 2 (Center Royal Blue Hero) — y=6.7..39.5 (cy=23.1, height=32.8)
    draw_soft_card(
        (64.0, 23.1),
        34.4,
        32.8,
        fill=(45, 98, 237),
        border=(37, 84, 212),
    )
    text(
        (64.0, 35.8),
        center_title,
        style=Styles.DarkBold.patch(
            text_font=FontSansSerif.POPPINS_BOLD,
            text_size=center_title_size,
            text_color=Colors.White,
        ),
    )
    for bx, icon_fn in zip([55.0, 64.0, 73.0], [ai.claude, ai.openai, ai.gemini], strict=True):
        circle(
            (bx, 29.5),
            radius=3.1,
            style=Styles.Neutral.patch(
                shape_fill_color=Colors.White,
                shape_line_color=(219, 234, 254),
                shape_line_width=0.8,
            ),
        )
        icon_fn((bx, 29.5), width=3.9, style=Styles.Primary)

    rectangle(
        (64.0, 18.95),
        width=27.2,
        height=9.3,
        style=Styles.Neutral.patch(
            shape_fill_color=Colors.White,
            shape_line_color=(219, 234, 254),
            shape_line_width=0.9,
            shape_r=2.1,
        ),
    )
    phosphor.check_circle((56.6, 21.05), width=3.2, style=Styles.Success.patch(icon_style="fill"))
    text(
        (59.1, 21.05),
        "Best Practices",
        style=Styles.DarkBold.patch(
            text_font=FontRoboto.ROBOTO_BOLD,
            text_size=11.2,
            text_color=(15, 23, 42),
            halign="left",
            valign="center",
        ),
    )
    phosphor.arrows_clockwise((56.6, 16.85), width=3.2, style=Styles.Primary.patch(icon_style="bold"))
    text(
        (59.1, 16.85),
        "Check/Fix Loop",
        style=Styles.DarkBold.patch(
            text_font=FontRoboto.ROBOTO_BOLD,
            text_size=11.2,
            text_color=(15, 23, 42),
            halign="left",
            valign="center",
        ),
    )
    text(
        (64.0, 10.4),
        "AI Agent + Drawlib",
        style=Styles.DarkBold.patch(
            text_font=FontSansSerif.POPPINS_BOLD,
            text_size=13.0,
            text_color=Colors.White,
        ),
    )

    # Stage 3 (Right) — y=6.7..39.5 (cy=23.1, height=32.8)
    draw_soft_card((105.2, 23.1), 28.6, 32.8)
    text(
        (105.2, 35.8),
        right_title,
        style=Styles.DarkBold.patch(
            text_font=FontSansSerif.POPPINS_BOLD,
            text_size=14.0,
            text_color=(15, 23, 42),
        ),
    )
    draw_mini_docs_browser((101.6, 23.5), width=18.4, height=15.2)
    for py, icon_fn, lbl in [
        (28.7, workspace.adobe_acrobat, "PDF"),
        (23.2, workspace.word, "DOCX"),
        (17.7, workspace.powerpoint, "PPTX"),
    ]:
        draw_soft_card((113.3, py), 10.4, 4.7, border=(148, 163, 184), r=1.2)
        icon_fn((110.3, py), width=3.1, style=Styles.Primary)
        text(
            (112.5, py),
            lbl,
            style=Styles.DarkBold.patch(
                text_font=FontRoboto.ROBOTO_BOLD,
                text_size=10.0,
                text_color=(15, 23, 42),
                halign="left",
                valign="center",
            ),
        )
    text(
        (105.2, 10.4),
        right_sub,
        style=Styles.DarkBold.patch(
            text_font=FontRoboto.ROBOTO_BOLD,
            text_size=11.2,
            text_color=(71, 85, 105),
        ),
    )

    draw_flow_arrow(38.8, 45.0, 23.1)
    draw_flow_arrow(83.0, 89.2, 23.1)
