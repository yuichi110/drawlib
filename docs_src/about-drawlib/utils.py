# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Default-styled slide drawing utilities calibrated for 1920x1080 16:9 stages."""

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
    """Draw a standardized slide page number badge."""
    _draw_page_number(width=width, height=height, style=style)


def draw_chapter_divider(
    chapter_num: int,
    title: str,
    subtitle: str = "",
    topics: Sequence[str] = (),
    total_chapters: int = 6,
    section_label: str = "CHAPTER",
    badge_text: str | None = None,
    variant: Literal["split", "centered", "banner", "minimal"] = "split",
) -> None:
    """Draw a full-bleed 16:9 chapter divider slide via drawlib.slide.draw_section_header."""
    resolved_badge = badge_text
    if resolved_badge is None and chapter_num <= total_chapters:
        resolved_badge = f"Chapter {chapter_num} of {total_chapters}"
    _draw_section_header(
        chapter_num,
        title,
        subtitle=subtitle,
        topics=topics,
        total_sections=total_chapters,
        variant=variant,
        section_label=section_label,
        badge_text=resolved_badge or "",
    )


def service_card(
    xy: tuple[float, float],
    title: str,
    subtitle: str = "",
    width: float = 28.0,
    height: float = 16.0,
    style: Style = Styles.PrimaryFlat,
) -> None:
    """Draw a standardized service card with slide-scale typography."""
    x, y = xy
    card_style = style if style.shape_r is not None else style.patch(shape_r=2.0)
    rectangle(xy, width=width, height=height, style=card_style)
    is_light_fill = style in (
        Styles.Neutral,
        Styles.PrimaryNeutral,
        Styles.SecondaryNeutral,
        Styles.White,
        Styles.WhiteFlat,
    )
    title_style = (Styles.DarkBold if is_light_fill else Styles.WhiteBold).patch(text_size=14.0)
    sub_style = (Styles.Muted if is_light_fill else Styles.White).patch(text_size=11.5)
    if subtitle:
        text((x, y + 2.6), title, style=title_style)
        text((x, y - 3.4), subtitle, style=sub_style)
    else:
        text((x, y), title, style=title_style)


def connect(
    start: tuple[float, float],
    end: tuple[float, float],
    label: str = "",
    arrow_head: Literal["", "->", "<-", "<->"] = "->",
    style: Style = Styles.PrimaryBold,
    label_offset_y: float = 3.2,
) -> None:
    """Draw a styled connecting line with a slide-scale protocol label."""
    line(start, end, arrow_head=arrow_head, style=style)
    if label:
        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2
        text((mid_x, mid_y + label_offset_y), label, style=Styles.PrimaryBold.patch(text_size=12.5))


def draw_curved_agenda(
    items: Sequence[str | tuple[str, str]],
    width: float = 108.0,
    height: float = 82.0,
    accent_bar: bool = True,
) -> None:
    """Draw a curved agenda/roadmap diagram calibrated for a 1080x820 slide block."""
    if not items:
        return

    if accent_bar:
        rectangle(
            (1.2, height / 2.0),
            width=1.4,
            height=height * 0.90,
            style=Styles.PrimaryFlat.patch(shape_line_width=0.0),
        )

    roadmap = Roadmap(
        style=Styles.White,
        text_style=Styles.DarkBold.patch(text_size=14.5),
        description_style=Styles.Dark.patch(text_size=12.0),
        spine_style=Styles.PrimaryBold,
        badge_style=Styles.PrimaryFlat,
        badge_text_style=Styles.WhiteBold.patch(text_size=14.0),
        direction="vertical",
        curve_bend=0.12,
        card_shape="pill",
        spacing=2.4,
    )
    for item in items:
        if isinstance(item, tuple):
            roadmap.add(item[0], item[1])
        else:
            roadmap.add(str(item))
    x0 = 4.2 if accent_bar else 2.0
    roadmap.draw(xy=(x0, height * 0.04), width=width - x0 - 2.0, height=height * 0.92)


def draw_kpi_cards(
    cards: Sequence[tuple[str, str, str]],
    width: float = 64.0,
    height: float = 80.0,
) -> None:
    """Draw vertically stacked KPI metric cards calibrated for narrow (620-640px) slide columns."""
    if not cards:
        return

    kpi = KpiCards(
        style=Styles.Neutral.patch(shape_r=2.5),
        metric_style=Styles.PrimaryBold.patch(text_size=27.0),
        text_style=Styles.DarkBold.patch(text_size=18.0),
        description_style=Styles.Dark.patch(text_size=14.2),
        accent_style=Styles.PrimaryFlat,
        accent_position="left_pill",
        metric_layout="left_column",
        metric_width_ratio=0.34,
        spacing=3.4,
    )
    for metric, label, subtext in cards:
        kpi.add(metric, label, subtext)
    kpi.draw(xy=(width * 0.02, height * 0.04), width=width * 0.96, height=height * 0.92, columns=1)
