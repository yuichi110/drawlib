# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Google-styled slide drawing utilities and presentation helper functions."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.slide import (
    draw_page_number as _draw_page_number,
    draw_section_header as _draw_section_header,
)
from drawlib.smartarts import KpiCards, Roadmap
from drawlib.styles import Style, Styles
from drawlib.text import text


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
    _draw_page_number(width=width, height=height, style=style)


def draw_chapter_divider(
    chapter_num: int,
    title: str,
    subtitle: str = "",
    topics: Sequence[str] = (),
    total_chapters: int = 4,
) -> None:
    """Draw a full-bleed 16:9 chapter divider slide via drawlib.slide.draw_section_header.

    Args:
        chapter_num: 1-based chapter number.
        title: Chapter title displayed prominently on the right panel.
        subtitle: One-line summary displayed under the chapter title.
        topics: List of key topic strings previewed in the chapter.
        total_chapters: Total number of chapters in the presentation.
    """
    _draw_section_header(
        chapter_num,
        title,
        subtitle=subtitle,
        topics=topics,
        total_sections=total_chapters,
        variant="split",
        section_label="ACT / CHAPTER",
        badge_text=f"Act {chapter_num} of {total_chapters}",
    )


def service_card(
    xy: tuple[float, float],
    title: str,
    subtitle: str = "",
    width: float = 24.0,
    height: float = 16.0,
    style: Style = Styles.PrimaryFlat,
) -> None:
    """Draw a standardized service card with a title and optional subtitle.

    Args:
        xy: Center coordinate (x, y).
        title: Main service name (e.g. 'API Gateway').
        subtitle: Secondary label or tech stack (e.g. 'FastAPI / :8000').
        width: Card width.
        height: Card height.
        style: Card shape style.
    """
    x, y = xy
    card_style = style if style.shape_r is not None else style.patch(shape_r=2.0)
    rectangle(xy, width=width, height=height, style=card_style)
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
    """Draw a styled connecting line with an optional centered protocol label.

    Args:
        start: Starting point (x, y).
        end: Ending point (x, y).
        label: Protocol or description text (e.g. 'HTTPS', 'gRPC').
        arrow_head: Arrowhead style ('->', '<->', '-').
        style: Line style.
    """
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
) -> None:
    """Draw a curved agenda/roadmap diagram via drawlib.smartarts.Roadmap."""
    if not items:
        return

    if accent_bar:
        rectangle(
            (1.0, height / 2.0),
            width=1.5,
            height=height * 0.9,
            style=Styles.PrimaryFlat.patch(shape_line_width=0.0),
        )

    roadmap = Roadmap(
        style=Styles.White,
        text_style=Styles.DarkBold.patch(text_size=14.0),
        description_style=Styles.Muted.patch(text_size=11.0),
        spine_style=Styles.PrimaryBold,
        badge_style=Styles.PrimaryFlat,
        badge_text_style=Styles.WhiteBold.patch(text_size=14.0),
        direction="vertical",
        curve_bend=0.14,
        card_shape="pill",
        spacing=3.0,
    )
    for item in items:
        if isinstance(item, tuple):
            roadmap.add(item[0], item[1])
        else:
            roadmap.add(str(item))
    x0 = 4.0 if accent_bar else 2.0
    roadmap.draw(xy=(x0, height * 0.06), width=width - x0 - 2.0, height=height * 0.88)


def draw_kpi_cards(
    cards: Sequence[tuple[str, str, str]],
    width: float = 100.0,
    height: float = 84.0,
) -> None:
    """Draw vertically stacked KPI metric cards via drawlib.smartarts.KpiCards."""
    if not cards:
        return

    kpi = KpiCards(
        style=Styles.Neutral.patch(shape_r=2.5),
        metric_style=Styles.PrimaryBold.patch(text_size=22.0),
        text_style=Styles.DarkBold.patch(text_size=14.0),
        description_style=Styles.Muted.patch(text_size=11.0),
        accent_style=Styles.PrimaryFlat,
        accent_position="left_pill",
        metric_layout="left_column",
        metric_width_ratio=0.30,
        spacing=3.5,
    )
    for metric, label, subtext in cards:
        kpi.add(metric, label, subtext)
    kpi.draw(xy=(width * 0.02, height * 0.05), width=width * 0.96, height=height * 0.90, columns=1)


