# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Default-styled slide drawing utilities and presentation helper functions."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from drawlib.canvas import clear, setup
from drawlib.lines import line, line_bezier1
from drawlib.shapes import circle, rectangle
from drawlib.slide import current_slide
from drawlib.styles import Style, Styles
from drawlib.text import text

_DEFAULT_PALETTE = [
    (79, 70, 229),   # Indigo 600 (Primary)
    (22, 163, 74),   # Green 600 (Secondary)
    (217, 119, 6),   # Amber 600 (Accent)
    (37, 99, 235),   # Blue 600
    (147, 51, 234),  # Purple 600
    (13, 148, 136),  # Teal 600
    (220, 38, 38),   # Red 600
]


def draw_page_number(
    width: int = 14,
    height: int = 3,
    style: Style | None = None,
) -> None:
    """Draw a standardized slide page number badge.

    Args:
        width: Canvas width in coordinate units.
        height: Canvas height in coordinate units.
        style: Text style for the page counter (defaults to gray 65pt text with transparent background).
    """
    clear()
    setup(width=width, height=height, alpha=0.0)
    effective_style = style or Styles.Black.patch(
        text_size=65,
        text_color=(128, 128, 128),
    )
    text((width / 2.0, height / 2.0), current_slide.text, style=effective_style)


def draw_chapter_divider(
    chapter_num: int,
    title: str,
    subtitle: str = "",
    topics: Sequence[str] = (),
    total_chapters: int = 7,
) -> None:
    """Draw a full-bleed 16:9 chapter divider slide (192.0 x 108.0 coordinate canvas).

    Args:
        chapter_num: 1-based chapter number.
        title: Chapter title displayed prominently on the right panel.
        subtitle: One-line summary displayed under the chapter title.
        topics: List of key topic strings previewed in the chapter.
        total_chapters: Total number of chapters in the presentation.
    """
    clear()
    setup(width=192, height=108)

    # Right panel background (soft slate)
    rectangle(
        (132.0, 54.0),
        width=120.0,
        height=108.0,
        style=Styles.WhiteFlat.patch(
            shape_fill_color=(248, 250, 252),
            shape_line_color=(248, 250, 252),
            shape_line_width=0.0,
        ),
    )

    # Left dark slate panel
    rectangle(
        (36.0, 54.0),
        width=72.0,
        height=108.0,
        style=Styles.WhiteFlat.patch(
            shape_fill_color=(15, 23, 42),
            shape_line_color=(15, 23, 42),
            shape_line_width=0.0,
        ),
    )

    # Subtle decorative geometry on left panel
    circle(
        (14.0, 92.0),
        radius=24.0,
        style=Style(
            shape_fill_color=(30, 41, 59),
            shape_line_color=(51, 65, 85),
            shape_line_width=1.0,
        ),
    )
    circle(
        (50.0, 14.0),
        radius=14.0,
        style=Style(
            shape_fill_color=(30, 41, 59),
            shape_line_color=(51, 65, 85),
            shape_line_width=1.0,
        ),
    )

    # Indigo accent vertical bar separating left & right panels
    rectangle(
        (72.0, 54.0),
        width=1.4,
        height=108.0,
        style=Styles.WhiteFlat.patch(
            shape_fill_color=(79, 70, 229),
            shape_line_color=(79, 70, 229),
            shape_line_width=0.0,
        ),
    )

    # Chapter label and large two-digit number
    text(
        (36.0, 70.0),
        "CHAPTER",
        style=Styles.WhiteBold.patch(
            text_size=13.0,
            text_color=(129, 140, 248),
        ),
    )
    text(
        (36.0, 52.0),
        f"{chapter_num:02d}",
        style=Styles.WhiteBold.patch(
            text_size=54.0,
            text_color=(255, 255, 255),
        ),
    )

    # Chapter progress indicator dots
    if total_chapters > 0:
        spacing = 6.2
        start_x = 36.0 - ((total_chapters - 1) * spacing) / 2.0
        for i in range(1, total_chapters + 1):
            cx = start_x + (i - 1) * spacing
            if i == chapter_num:
                circle(
                    (cx, 26.0),
                    radius=2.1,
                    style=Style(
                        shape_fill_color=(99, 102, 241),
                        shape_line_color=(199, 210, 254),
                        shape_line_width=1.2,
                    ),
                )
            elif i < chapter_num:
                circle(
                    (cx, 26.0),
                    radius=1.3,
                    style=Styles.WhiteFlat.patch(
                        shape_fill_color=(79, 70, 229),
                        shape_line_color=(79, 70, 229),
                        shape_line_width=0.0,
                    ),
                )
            else:
                circle(
                    (cx, 26.0),
                    radius=1.3,
                    style=Styles.WhiteFlat.patch(
                        shape_fill_color=(51, 65, 85),
                        shape_line_color=(51, 65, 85),
                        shape_line_width=0.0,
                    ),
                )

    # Right panel header badge
    rectangle(
        (98.0, 84.0),
        width=24.0,
        height=5.2,
        r=2.5,
        style=Style(
            shape_fill_color=(224, 231, 255),
            shape_line_color=(199, 210, 254),
            shape_line_width=1.0,
        ),
    )
    text(
        (98.0, 84.0),
        f"Part {chapter_num} of {total_chapters}",
        style=Styles.BlackBold.patch(
            text_size=9.5,
            text_color=(67, 56, 202),
        ),
    )

    # Chapter title & subtitle
    text(
        (86.0, 72.0),
        title,
        style=Styles.BlackBold.patch(
            text_size=22.0,
            text_halign="left",
            text_valign="center",
            text_color=(15, 23, 42),
        ),
    )
    if subtitle:
        text(
            (86.0, 62.5),
            subtitle,
            style=Styles.Black.patch(
                text_size=12.0,
                text_halign="left",
                text_valign="center",
                text_color=(71, 85, 105),
            ),
        )

    line(
        (86.0, 55.0),
        (178.0, 55.0),
        style=Style(line_color=(203, 213, 225), line_width=1.5),
    )

    # Key topics list cards
    if topics:
        n_topics = len(topics)
        card_h = min(7.2, 36.0 / max(n_topics, 1))
        gap = min(2.4, (40.0 - card_h * n_topics) / max(n_topics, 1))
        top_y = 48.0
        for idx, topic in enumerate(topics, start=1):
            cy = top_y - (idx - 1) * (card_h + gap) - card_h / 2.0
            rectangle(
                (132.0, cy),
                width=92.0,
                height=card_h,
                r=1.8,
                style=Style(
                    shape_fill_color=(255, 255, 255),
                    shape_line_color=(226, 232, 240),
                    shape_line_width=1.0,
                ),
            )
            circle(
                (91.5, cy),
                radius=2.3,
                style=Styles.WhiteFlat.patch(
                    shape_fill_color=(79, 70, 229),
                    shape_line_color=(79, 70, 229),
                    shape_line_width=0.0,
                ),
                text=f"{chapter_num}.{idx}",
                text_style=Styles.WhiteBold.patch(text_size=7.5),
            )
            text(
                (96.5, cy),
                topic,
                style=Styles.BlackBold.patch(
                    text_size=10.5,
                    text_halign="left",
                    text_valign="center",
                    text_color=(30, 41, 59),
                ),
            )

    # Bottom-right slide counter
    text(
        (182.0, 4.5),
        current_slide.text,
        style=Styles.Black.patch(
            text_size=9.0,
            text_color=(148, 163, 184),
        ),
    )


def service_card(
    xy: tuple[float, float],
    title: str,
    subtitle: str = "",
    width: float = 24.0,
    height: float = 16.0,
    style: Style = Styles.PrimaryFlat,
) -> None:
    """Draw a standardized service card with a title and optional subtitle."""
    x, y = xy
    rectangle(xy, width=width, height=height, r=2.0, style=style)
    if subtitle:
        text((x, y + 2.5), title, style=Styles.WhiteBold.patch(text_size=11))
        text((x, y - 3.5), subtitle, style=Styles.White.patch(text_size=8))
    else:
        text((x, y), title, style=Styles.WhiteBold)


def connect(
    start: tuple[float, float],
    end: tuple[float, float],
    label: str = "",
    arrow_head: Literal["", "->", "<-", "<->"] = "->",
    style: Style = Styles.PrimaryBold,
) -> None:
    """Draw a styled connecting line with an optional centered protocol label."""
    line(start, end, arrow_head=arrow_head, style=style)
    if label:
        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2
        text((mid_x, mid_y + 3.0), label, style=Styles.Primary.patch(text_size=9))


def draw_curved_agenda(
    items: Sequence[str | tuple[str, str]],
    width: float = 104.0,
    height: float = 86.0,
    accent_bar: bool = True,
    colors: Sequence[tuple[int, int, int]] | None = None,
) -> None:
    """Draw a curved agenda/roadmap diagram with numbered badges and pill containers."""
    if not items:
        return

    w = width
    h = height

    if accent_bar:
        bar_color = (79, 70, 229)
        bar_style = Style(shape_fill_color=bar_color, shape_line_color=bar_color, shape_line_width=0.0)
        rectangle((1.0, h / 2.0), width=1.5, height=h * 0.9, style=bar_style)

    # Smooth curved arc line
    p_start = (w * 0.16, h * 0.90)
    p_end = (w * 0.15, h * 0.10)
    p_ctrl = (w * 0.25, h * 0.50)

    arc_style = Style(line_color=(203, 213, 225), line_width=3.0)
    line_bezier1(p_start, p_end, p_ctrl, style=arc_style)

    palette = colors or _DEFAULT_PALETTE

    n = len(items)
    for i, item in enumerate(items):
        if isinstance(item, tuple):
            title_str, sub_str = item[0], item[1]
        else:
            title_str, sub_str = str(item), ""

        t = i / (n - 1) if n > 1 else 0.5
        xi = (1 - t) ** 2 * p_start[0] + 2 * (1 - t) * t * p_ctrl[0] + t**2 * p_end[0]
        yi = (1 - t) ** 2 * p_start[1] + 2 * (1 - t) * t * p_ctrl[1] + t**2 * p_end[1]

        color = palette[i % len(palette)]
        r_badge = min(3.4, h / (n * 3.0))
        badge_style = Style(shape_fill_color=color, shape_line_color=color, shape_line_width=0.0)
        circle((xi, yi), radius=r_badge, style=badge_style, text=str(i + 1), text_style=Styles.WhiteBold.patch(text_size=10))

        # Pill container
        x_pill_start = xi + r_badge + 2.2
        w_pill = min(w - x_pill_start - 2.0, 80.0)
        h_pill = max(6.0, min(r_badge * 2.3, 8.5))
        x_pill_center = x_pill_start + w_pill / 2.0
        pill_style = Style(
            shape_fill_color=(255, 255, 255),
            shape_line_color=(226, 232, 240),
            shape_line_width=1.0,
        )
        rectangle((x_pill_center, yi), width=w_pill, height=h_pill, r=h_pill / 2.0, style=pill_style)

        # Text labels
        x_text = x_pill_start + 3.5
        if sub_str:
            text(
                (x_text, yi + 1.15),
                title_str,
                style=Styles.BlackBold.patch(
                    text_size=10.5,
                    text_halign="left",
                    text_valign="center",
                    text_color=(15, 23, 42),
                ),
            )
            text(
                (x_text, yi - 1.35),
                sub_str,
                style=Styles.Black.patch(
                    text_size=8.2,
                    text_halign="left",
                    text_valign="center",
                    text_color=(100, 116, 139),
                ),
            )
        else:
            text(
                (x_text, yi),
                title_str,
                style=Styles.BlackBold.patch(
                    text_size=11.0,
                    text_halign="left",
                    text_valign="center",
                    text_color=(15, 23, 42),
                ),
            )


def draw_kpi_cards(
    cards: Sequence[tuple[str, str, str]],
    width: float = 100.0,
    height: float = 84.0,
    colors: Sequence[tuple[int, int, int]] | None = None,
) -> None:
    """Draw vertically stacked KPI metric cards with highlight badges and descriptions."""
    if not cards:
        return

    w = width
    h = height
    n = len(cards)
    accent_colors = colors or _DEFAULT_PALETTE

    card_h = min(22.0, (h - 10.0) / max(n, 1))
    gap = (h - 10.0 - (card_h * n)) / max(n + 1, 1)

    for i, (metric, label, subtext) in enumerate(cards):
        cy = h - 5.0 - gap - (i * (card_h + gap)) - (card_h / 2.0)
        cx = w / 2.0
        card_w = w * 0.92

        # Background card
        card_style = Style(
            shape_fill_color=(248, 250, 252),
            shape_line_color=(226, 232, 240),
            shape_line_width=1.0,
        )
        rectangle((cx, cy), width=card_w, height=card_h, r=3.0, style=card_style)

        # Left accent pill
        accent = accent_colors[i % len(accent_colors)]
        pill_style = Styles.WhiteFlat.patch(
            shape_fill_color=accent,
            shape_line_color=accent,
            shape_line_width=0.0,
        )
        pill_x = cx - (card_w / 2.0) + 1.5
        rectangle((pill_x, cy), width=2.0, height=card_h * 0.7, r=1.0, style=pill_style)

        # Metric number
        text(
            (cx - (card_w / 2.0) + 8.0, cy),
            metric,
            style=Styles.BlackBold.patch(
                text_size=15.0,
                text_halign="left",
                text_valign="center",
                text_color=accent,
            ),
        )

        # Label
        if label:
            text(
                (cx - (card_w / 2.0) + 38.0, cy + 3.0),
                label,
                style=Styles.BlackBold.patch(
                    text_size=11.0,
                    text_halign="left",
                    text_valign="center",
                    text_color=(15, 23, 42),
                ),
            )

        # Subtext
        if subtext:
            text(
                (cx - (card_w / 2.0) + 38.0, cy - 3.5),
                subtext,
                style=Styles.Black.patch(
                    text_size=8.5,
                    text_halign="left",
                    text_valign="center",
                    text_color=(100, 116, 139),
                ),
            )
