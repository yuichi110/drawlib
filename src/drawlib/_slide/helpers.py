# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Slide stage and section header drawing helper functions."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal

from pydantic import validate_call

from drawlib._core.l2_types import PosInt
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas import (
    circle,
    clear,
    line,
    rectangle,
    setup,
    text,
)
from drawlib._slide.base import current_slide
from drawlib._smartarts._cardlist import CardList
from drawlib.styles import Colors, Styles


@dataclass(frozen=True)
class _SectionHeaderConfig:
    """Resolved internal configuration and styles for draw_section_header."""

    section_num: int
    title: str
    subtitle: str
    norm_topics: list[tuple[str, str]]
    total_sections: int
    section_label: str
    resolved_badge: str
    show_decorations: bool
    left_panel_style: Style
    right_panel_style: Style
    divider_bar_style: Style
    decoration_style: Style | None
    section_label_style: Style | None
    section_num_style: Style | None
    active_dot_style: Style | None
    completed_dot_style: Style | None
    upcoming_dot_style: Style | None
    badge_style: Style | None
    badge_text_style: Style | None
    title_style: Style | None
    subtitle_style: Style | None
    line_style: Style
    topic_card_style: Style
    topic_text_style: Style
    topic_description_style: Style
    topic_badge_style: Style | None
    topic_badge_text_style: Style | None

    @property
    def has_topics(self) -> bool:
        """Whether at least one topic item is provided."""
        return len(self.norm_topics) > 0

    @property
    def has_subtitle(self) -> bool:
        """Whether a non-empty subtitle is provided."""
        return bool(self.subtitle.strip())

    @property
    def has_badge(self) -> bool:
        """Whether a non-empty part badge string is resolved."""
        return bool(self.resolved_badge.strip())

    @property
    def has_topic_descriptions(self) -> bool:
        """Whether any topic item includes a secondary description string."""
        return any(bool(desc.strip()) for _, desc in self.norm_topics)


def _normalize_topics(
    topics: Sequence[str | tuple[str, str]],
) -> list[tuple[str, str]]:
    """Normalize topic items into (title, description) tuples."""
    result: list[tuple[str, str]] = []
    for item in topics:
        if isinstance(item, tuple):
            t_str = str(item[0]) if len(item) > 0 else ""
            d_str = str(item[1]) if len(item) > 1 else ""
            result.append((t_str, d_str))
        else:
            result.append((str(item), ""))
    return result


def _draw_progress_dots(
    cfg: _SectionHeaderConfig,
    cx_center: float,
    cy: float,
    *,
    on_dark: bool,
    spacing: float = 6.6,
) -> None:
    """Draw horizontal section progress dots centered at (cx_center, cy)."""
    if cfg.total_sections <= 0:
        return

    if on_dark:
        active_st = cfg.active_dot_style or Styles.PrimaryFlat.patch(
            shape_line_color=Colors.White, shape_line_width=1.2
        )
        completed_st = cfg.completed_dot_style or Styles.PrimaryFlat.patch(
            shape_line_width=0.0
        )
        upcoming_st = cfg.upcoming_dot_style or Styles.WhiteFlat.patch(
            alpha=0.25, shape_line_width=0.0
        )
    else:
        active_st = cfg.active_dot_style or Styles.PrimaryFlat.patch(
            shape_line_width=0.0
        )
        completed_st = cfg.completed_dot_style or Styles.PrimaryFlat.patch(
            alpha=0.45, shape_line_width=0.0
        )
        upcoming_st = cfg.upcoming_dot_style or Styles.DarkFlat.patch(
            alpha=0.20, shape_line_width=0.0
        )

    start_x = cx_center - ((cfg.total_sections - 1) * spacing) / 2.0
    for i in range(1, cfg.total_sections + 1):
        dx = start_x + (i - 1) * spacing
        if i == cfg.section_num:
            circle((dx, cy), radius=2.1, style=active_st)
        elif i < cfg.section_num:
            circle((dx, cy), radius=1.35, style=completed_st)
        else:
            circle((dx, cy), radius=1.35, style=upcoming_st)


def _draw_topic_cards(
    cfg: _SectionHeaderConfig,
    *,
    xy: tuple[float, float],
    width: float,
    height: float,
    direction: Literal["vertical", "horizontal"],
    badge_shape: Literal["circle", "rounded_rect"],
    default_badge_style: Style,
    default_badge_text_style: Style,
    spacing: float,
) -> None:
    """Populate and render a CardList for section header topics."""
    cl = CardList(
        style=cfg.topic_card_style,
        text_style=cfg.topic_text_style,
        description_style=cfg.topic_description_style,
        badge_shape=badge_shape,
        badge_style=cfg.topic_badge_style or default_badge_style,
        badge_text_style=cfg.topic_badge_text_style or default_badge_text_style,
        direction=direction,
        spacing=spacing,
    )
    for idx, (t_str, d_str) in enumerate(cfg.norm_topics, start=1):
        cl.add(t_str, d_str, badge_text=f"{cfg.section_num}.{idx}")
    cl.draw(xy=xy, width=width, height=height)


def _draw_split_variant(cfg: _SectionHeaderConfig) -> None:
    """Render the 'split' (left dark panel + right neutral panel) layout."""
    # Right panel background & left dark panel
    rectangle((132.0, 54.0), width=120.0, height=108.0, style=cfg.right_panel_style)
    rectangle((36.0, 54.0), width=72.0, height=108.0, style=cfg.left_panel_style)

    if cfg.show_decorations:
        decor_st = cfg.decoration_style or Styles.WhiteFlat.patch(
            alpha=0.06,
            shape_line_color=Colors.White,
            shape_line_width=0.8,
        )
        circle((14.0, 92.0), radius=23.0, style=decor_st)
        circle((53.0, 14.0), radius=13.5, style=decor_st)

    # Vertical accent divider bar
    rectangle((72.0, 54.0), width=1.6, height=108.0, style=cfg.divider_bar_style)

    # Left panel section label & two-digit section number
    lbl_st = cfg.section_label_style or Styles.WhiteBold.patch(
        text_size=13.0, alpha=0.82
    )
    num_st = cfg.section_num_style or Styles.WhiteBold.patch(text_size=54.0)
    text((36.0, 70.0), cfg.section_label, style=lbl_st)
    text((36.0, 52.0), f"{cfg.section_num:02d}", style=num_st)

    _draw_progress_dots(cfg, cx_center=36.0, cy=26.0, on_dark=True)

    # Right panel vertical positioning
    base_top_y = 85.0 if cfg.has_topics else 68.0
    if cfg.has_badge:
        badge_w = max(24.0, len(cfg.resolved_badge) * 1.55 + 5.0)
        badge_st = cfg.badge_style or Styles.PrimaryNeutral.patch(
            shape_r=2.6, shape_line_width=0.8
        )
        badge_txt_st = cfg.badge_text_style or Styles.PrimaryBold.patch(
            text_size=10.5
        )
        rectangle(
            (82.0 + badge_w / 2.0, base_top_y),
            width=badge_w,
            height=5.6,
            style=badge_st,
        )
        text(
            (82.0 + badge_w / 2.0, base_top_y),
            cfg.resolved_badge,
            style=badge_txt_st,
        )
        title_y = base_top_y - 12.0
    else:
        title_y = base_top_y - 4.0

    t_st = cfg.title_style or Styles.BlackBold.patch(
        text_size=21.5, halign="left", valign="center"
    )
    text((82.0, title_y), cfg.title, style=t_st)

    if cfg.has_subtitle:
        sub_y = title_y - 9.5
        s_st = cfg.subtitle_style or Styles.Dark.patch(
            text_size=11.5, halign="left", valign="center"
        )
        text((82.0, sub_y), cfg.subtitle, style=s_st)
        line_y = sub_y - 7.0
    else:
        line_y = title_y - 8.5

    line((82.0, line_y), (185.0, line_y), style=cfg.line_style)

    if cfg.has_topics:
        n_t = len(cfg.norm_topics)
        item_h = 9.5 if cfg.has_topic_descriptions else 7.6
        gap = 2.4
        list_h = min(line_y - 11.0, n_t * item_h + (n_t - 1) * gap)
        list_y0 = line_y - 5.5 - list_h

        _draw_topic_cards(
            cfg,
            xy=(82.0, list_y0),
            width=103.0,
            height=list_h,
            direction="vertical",
            badge_shape="circle",
            default_badge_style=Styles.PrimaryFlat.patch(shape_line_width=0.0),
            default_badge_text_style=Styles.WhiteBold.patch(text_size=10.0),
            spacing=gap,
        )


def _draw_centered_variant(cfg: _SectionHeaderConfig) -> None:
    """Render the 'centered' (keynote hero + horizontal cards) layout."""
    rectangle((96.0, 54.0), width=192.0, height=108.0, style=cfg.right_panel_style)
    if cfg.show_decorations:
        decor_primary = cfg.decoration_style or Styles.PrimaryNeutral.patch(
            alpha=0.45, shape_line_width=0.0
        )
        decor_secondary = cfg.decoration_style or Styles.SecondaryNeutral.patch(
            alpha=0.45, shape_line_width=0.0
        )
        circle((16.0, 88.0), radius=24.0, style=decor_primary)
        circle((176.0, 18.0), radius=22.0, style=decor_secondary)

    rectangle((96.0, 106.8), width=192.0, height=2.4, style=cfg.divider_bar_style)

    top_anchor = 86.0 if cfg.has_topics else 74.0
    pill_label = (
        f"{cfg.section_label} {cfg.section_num:02d}  •  {cfg.resolved_badge}"
        if cfg.has_badge
        else f"{cfg.section_label} {cfg.section_num:02d}"
    )
    pill_w = max(32.0, len(pill_label) * 1.55 + 8.0)
    pill_bg_st = (
        cfg.badge_style
        or cfg.section_num_style
        or Styles.PrimaryFlat.patch(shape_r=3.4, shape_line_width=0.0)
    )
    pill_txt_st = (
        cfg.badge_text_style
        or cfg.section_label_style
        or Styles.WhiteBold.patch(text_size=11.5)
    )
    rectangle((96.0, top_anchor), width=pill_w, height=6.8, style=pill_bg_st)
    text((96.0, top_anchor), pill_label, style=pill_txt_st)

    title_y = top_anchor - 14.0
    t_st = cfg.title_style or Styles.BlackBold.patch(
        text_size=26.0, halign="center", valign="center"
    )
    text((96.0, title_y), cfg.title, style=t_st)

    if cfg.has_subtitle:
        sub_y = title_y - 10.5
        s_st = cfg.subtitle_style or Styles.Dark.patch(
            text_size=13.0, halign="center", valign="center"
        )
        text((96.0, sub_y), cfg.subtitle, style=s_st)
        div_y = sub_y - 7.5
    else:
        div_y = title_y - 9.0

    rectangle(
        (96.0, div_y),
        width=24.0,
        height=1.2,
        style=cfg.divider_bar_style.patch(shape_r=0.6),
    )

    if cfg.has_topics:
        n_t = len(cfg.norm_topics)
        card_h = 26.0 if cfg.has_topic_descriptions else 21.0
        list_y0 = div_y - 7.5 - card_h
        total_w = min(168.0, max(96.0, n_t * 42.0))

        _draw_topic_cards(
            cfg,
            xy=(96.0 - total_w / 2.0, list_y0),
            width=total_w,
            height=card_h,
            direction="horizontal",
            badge_shape="circle",
            default_badge_style=Styles.PrimaryNeutral.patch(
                shape_line_width=0.8
            ),
            default_badge_text_style=Styles.PrimaryBold.patch(text_size=10.5),
            spacing=3.2,
        )
        dots_y = 11.0
    else:
        dots_y = div_y - 12.0

    _draw_progress_dots(cfg, cx_center=96.0, cy=dots_y, on_dark=False)


def _draw_banner_variant(cfg: _SectionHeaderConfig) -> None:
    """Render the 'banner' (top dark hero band + horizontal cards) layout."""
    rectangle((96.0, 54.0), width=192.0, height=108.0, style=cfg.right_panel_style)

    band_h = 46.0 if cfg.has_topics else 62.0
    band_cy = (108.0 - band_h / 2.0) if cfg.has_topics else 54.0
    band_bot = band_cy - band_h / 2.0

    rectangle((96.0, band_cy), width=192.0, height=band_h, style=cfg.left_panel_style)
    rectangle((96.0, band_bot), width=192.0, height=1.8, style=cfg.divider_bar_style)

    if cfg.show_decorations:
        decor_st = cfg.decoration_style or Styles.WhiteFlat.patch(
            alpha=0.06,
            shape_line_color=Colors.White,
            shape_line_width=0.8,
        )
        circle((174.0, band_cy + 8.0), radius=20.0, style=decor_st)

    badge_box_x = 28.0
    box_st = cfg.badge_style or Styles.PrimaryFlat.patch(
        shape_r=3.5, shape_line_width=0.0
    )
    rectangle(
        (badge_box_x, band_cy),
        width=26.0,
        height=26.0,
        style=box_st,
    )
    lbl_st = cfg.section_label_style or Styles.WhiteBold.patch(
        text_size=9.5, alpha=0.9
    )
    num_st = cfg.section_num_style or Styles.WhiteBold.patch(text_size=28.0)
    text((badge_box_x, band_cy + 6.5), cfg.section_label, style=lbl_st)
    text((badge_box_x, band_cy - 3.5), f"{cfg.section_num:02d}", style=num_st)

    text_x = 50.0
    if cfg.has_badge:
        badge_txt_st = cfg.badge_text_style or Styles.WhiteBold.patch(
            text_size=10.5, halign="left", valign="center", alpha=0.75
        )
        text(
            (text_x, band_cy + 10.5),
            cfg.resolved_badge.upper(),
            style=badge_txt_st,
        )
        t_y = band_cy + 1.5 if cfg.has_subtitle else band_cy - 1.5
    else:
        t_y = band_cy + 4.5 if cfg.has_subtitle else band_cy

    t_st = cfg.title_style or Styles.WhiteBold.patch(
        text_size=23.5, halign="left", valign="center"
    )
    text((text_x, t_y), cfg.title, style=t_st)
    if cfg.has_subtitle:
        s_st = cfg.subtitle_style or Styles.White.patch(
            text_size=12.0, halign="left", valign="center", alpha=0.85
        )
        text((text_x, t_y - 10.0), cfg.subtitle, style=s_st)

    _draw_progress_dots(
        cfg,
        cx_center=168.0,
        cy=band_cy + band_h / 2.0 - 7.5,
        on_dark=True,
        spacing=5.8,
    )

    if cfg.has_topics:
        card_h = 34.0
        card_y0 = (band_bot - 8.0 - card_h) / 2.0 + 6.0
        _draw_topic_cards(
            cfg,
            xy=(14.0, card_y0),
            width=164.0,
            height=card_h,
            direction="horizontal",
            badge_shape="rounded_rect",
            default_badge_style=Styles.PrimaryFlat.patch(shape_line_width=0.0),
            default_badge_text_style=Styles.WhiteBold.patch(text_size=10.5),
            spacing=3.5,
        )


def _draw_minimal_variant(cfg: _SectionHeaderConfig) -> None:
    """Render the 'minimal' (editorial light background + left accent stripe) layout."""
    rectangle((96.0, 54.0), width=192.0, height=108.0, style=cfg.right_panel_style)

    stripe_x = 16.0
    rectangle(
        (stripe_x, 54.0),
        width=2.2,
        height=84.0,
        style=cfg.divider_bar_style.patch(shape_r=1.1),
    )

    content_x = 26.0
    top_y = 86.0 if cfg.has_topics else 68.0

    num_pill_w = 24.0
    pill_bg_st = (
        cfg.badge_style
        or cfg.section_num_style
        or Styles.PrimaryFlat.patch(shape_r=1.6, shape_line_width=0.0)
    )
    pill_txt_st = cfg.section_label_style or Styles.WhiteBold.patch(text_size=11.0)
    rectangle(
        (content_x + num_pill_w / 2.0, top_y),
        width=num_pill_w,
        height=6.5,
        style=pill_bg_st,
    )
    text(
        (content_x + num_pill_w / 2.0, top_y),
        f"{cfg.section_label} {cfg.section_num:02d}",
        style=pill_txt_st,
    )

    if cfg.has_badge:
        badge_txt_st = cfg.badge_text_style or Styles.Muted.patch(
            text_size=11.0, halign="left", valign="center"
        )
        text(
            (content_x + num_pill_w + 3.5, top_y),
            cfg.resolved_badge,
            style=badge_txt_st,
        )

    _draw_progress_dots(
        cfg,
        cx_center=164.0,
        cy=top_y,
        on_dark=False,
        spacing=5.8,
    )

    title_y = top_y - 12.0
    t_st = cfg.title_style or Styles.BlackBold.patch(
        text_size=24.0, halign="left", valign="center"
    )
    text((content_x, title_y), cfg.title, style=t_st)
    if cfg.has_subtitle:
        sub_y = title_y - 9.5
        s_st = cfg.subtitle_style or Styles.Dark.patch(
            text_size=12.5, halign="left", valign="center"
        )
        text((content_x, sub_y), cfg.subtitle, style=s_st)
        line_y = sub_y - 6.5
    else:
        line_y = title_y - 8.0

    line((content_x, line_y), (178.0, line_y), style=cfg.line_style)

    if cfg.has_topics:
        n_t = len(cfg.norm_topics)
        item_h = 9.5 if cfg.has_topic_descriptions else 7.8
        gap = 2.4
        list_h = min(line_y - 11.0, n_t * item_h + (n_t - 1) * gap)
        list_y0 = line_y - 5.5 - list_h

        _draw_topic_cards(
            cfg,
            xy=(content_x, list_y0),
            width=152.0,
            height=list_h,
            direction="vertical",
            badge_shape="rounded_rect",
            default_badge_style=Styles.PrimaryNeutral.patch(
                shape_line_width=0.8
            ),
            default_badge_text_style=Styles.PrimaryBold.patch(text_size=10.5),
            spacing=gap,
        )


@validate_call
def draw_page_number(
    width: PosInt = 14,
    height: PosInt = 3,
    *,
    template: str = "{index} / {total}",
    style: Style | None = None,
    auto_setup: bool = True,
) -> None:
    """Draw a standardized slide page number badge using current_slide.

    Args:
        width: Canvas width in coordinate units. Defaults to 14.
        height: Canvas height in coordinate units. Defaults to 3.
        template: Format string with ``{index}`` and ``{total}`` placeholders.
            Defaults to ``"{index} / {total}"``.
        style: Text style for the page counter. Defaults to
            ``Styles.Muted.patch(text_size=65.0)``.
        auto_setup: Whether to call ``clear()`` and
            ``setup(width=width, height=height, alpha=0.0)`` automatically
            before drawing. Defaults to True.

    Raises:
        ValueError: If ``width`` or ``height`` is not positive.
    """
    if width <= 0 or height <= 0:
        msg = "width and height must be > 0."
        raise ValueError(msg)

    if auto_setup:
        clear()
        setup(width=width, height=height, alpha=0.0)
    effective_style = style or Styles.Muted.patch(text_size=65.0)
    label = (
        current_slide.text
        if template == "{index} / {total}"
        else current_slide.format(template)
    )
    text((width / 2.0, height / 2.0), label, style=effective_style)


@validate_call
def draw_section_header(  # noqa: PLR0913
    section_num: PosInt,
    title: str,
    subtitle: str = "",
    topics: Sequence[str | tuple[str, str]] = (),
    total_sections: PosInt = 0,
    *,
    variant: Literal["split", "centered", "banner", "minimal"] = "split",
    section_label: str = "SECTION",
    badge_text: str | None = None,
    show_page_number: bool = True,
    show_decorations: bool = True,
    auto_setup: bool = True,
    left_panel_style: Style | None = None,
    right_panel_style: Style | None = None,
    divider_bar_style: Style | None = None,
    decoration_style: Style | None = None,
    section_label_style: Style | None = None,
    section_num_style: Style | None = None,
    active_dot_style: Style | None = None,
    completed_dot_style: Style | None = None,
    upcoming_dot_style: Style | None = None,
    badge_style: Style | None = None,
    badge_text_style: Style | None = None,
    title_style: Style | None = None,
    subtitle_style: Style | None = None,
    line_style: Style | None = None,
    topic_card_style: Style | None = None,
    topic_text_style: Style | None = None,
    topic_description_style: Style | None = None,
    topic_badge_style: Style | None = None,
    topic_badge_text_style: Style | None = None,
    page_number_style: Style | None = None,
) -> None:
    """Draw a full-bleed 16:9 section header slide (192.0 x 108.0 canvas).

    Args:
        section_num: 1-based section number.
        title: Section title displayed prominently on the slide.
        subtitle: Optional summary line displayed below the title.
        topics: Optional sequence of topic strings or ``(title, description)``
            tuples rendered as preview cards.
        total_sections: Total number of sections in the deck. When greater than
            zero, progress indicator dots and a ``"Part X of Y"`` badge are
            shown automatically. Defaults to 0.
        variant: Section header layout pattern (``"split"``, ``"centered"``,
            ``"banner"``, or ``"minimal"``). Defaults to ``"split"``.
        section_label: Uppercase header label above or beside the section
            number. Defaults to ``"SECTION"``.
        badge_text: Optional custom badge text overriding ``"Part X of Y"``.
        show_page_number: Whether to draw ``current_slide.text`` at the
            bottom-right corner. Defaults to True.
        show_decorations: Whether to draw subtle background geometric circles.
            Defaults to True.
        auto_setup: Whether to call ``clear()`` and ``setup(width=192, height=108)``
            automatically before drawing. Defaults to True.
        left_panel_style: Optional style override for the dark panel or banner.
        right_panel_style: Optional style override for the main neutral canvas.
        divider_bar_style: Optional style override for the accent divider bar.
        decoration_style: Optional style override for decorative background circles.
        section_label_style: Optional style override for the section label text.
        section_num_style: Optional style override for the section number text
            or badge pill.
        active_dot_style: Optional style override for the active progress dot.
        completed_dot_style: Optional style override for completed progress dots.
        upcoming_dot_style: Optional style override for upcoming progress dots.
        badge_style: Optional style override for the part badge background.
        badge_text_style: Optional style override for the part badge text.
        title_style: Optional style override for the main section title.
        subtitle_style: Optional style override for the section subtitle.
        line_style: Optional style override for the horizontal divider line.
        topic_card_style: Optional style override for topic card rectangles.
        topic_text_style: Optional style override for topic card titles.
        topic_description_style: Optional style override for topic card descriptions.
        topic_badge_style: Optional style override for topic card number badges.
        topic_badge_text_style: Optional style override for topic card badge text.
        page_number_style: Optional style override for the bottom-right slide counter.

    Raises:
        ValueError: If ``section_num`` is less than 1.
    """
    if section_num < 1:
        msg = "section_num must be >= 1."
        raise ValueError(msg)

    if auto_setup:
        clear()
        setup(width=192, height=108)

    resolved_badge = (
        badge_text
        if badge_text is not None
        else (
            f"Part {section_num} of {total_sections}"
            if total_sections > 0
            else ""
        )
    )

    cfg = _SectionHeaderConfig(
        section_num=int(section_num),
        title=title,
        subtitle=subtitle,
        norm_topics=_normalize_topics(topics),
        total_sections=total_sections,
        section_label=section_label,
        resolved_badge=resolved_badge,
        show_decorations=show_decorations,
        left_panel_style=left_panel_style
        or Styles.DarkFlat.patch(shape_line_width=0.0, shape_r=0.0),
        right_panel_style=right_panel_style
        or Styles.Neutral.patch(shape_line_width=0.0, shape_r=0.0),
        divider_bar_style=divider_bar_style
        or Styles.PrimaryFlat.patch(shape_line_width=0.0, shape_r=0.0),
        decoration_style=decoration_style,
        section_label_style=section_label_style,
        section_num_style=section_num_style,
        active_dot_style=active_dot_style,
        completed_dot_style=completed_dot_style,
        upcoming_dot_style=upcoming_dot_style,
        badge_style=badge_style,
        badge_text_style=badge_text_style,
        title_style=title_style,
        subtitle_style=subtitle_style,
        line_style=line_style
        or Styles.Neutral.patch(line_color=Colors.Gray3, line_width=1.0),
        topic_card_style=topic_card_style
        or Styles.White.patch(
            shape_line_color=Colors.Gray3,
            shape_line_width=0.9,
        ),
        topic_text_style=topic_text_style
        or Styles.DarkBold.patch(text_size=11.0),
        topic_description_style=topic_description_style
        or Styles.Muted.patch(text_size=9.8),
        topic_badge_style=topic_badge_style,
        topic_badge_text_style=topic_badge_text_style,
    )

    if variant == "split":
        _draw_split_variant(cfg)
    elif variant == "centered":
        _draw_centered_variant(cfg)
    elif variant == "banner":
        _draw_banner_variant(cfg)
    elif variant == "minimal":
        _draw_minimal_variant(cfg)

    if show_page_number:
        p_st = page_number_style or Styles.Muted.patch(text_size=9.5)
        text((182.0, 4.5), current_slide.text, style=p_st)


__all__ = [
    "draw_page_number",
    "draw_section_header",
]
