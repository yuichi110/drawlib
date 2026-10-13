# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Roadmap SmartArt implementation module."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, Literal, Self

from pydantic import BaseModel, ConfigDict, validate_call

from drawlib._core.l2_types import Coordinate, PosFloat
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas import circle as canvas_circle
from drawlib._core.l4_canvas import line as canvas_line
from drawlib._core.l4_canvas import line_bezier1 as canvas_line_bezier1
from drawlib._core.l4_canvas import rectangle as canvas_rectangle
from drawlib._core.l4_canvas import transform
from drawlib._smartarts._common import draw_card_title_and_description


class RoadmapItem(BaseModel):
    """Mutable item model for a single milestone or phase node in Roadmap.

    Attributes:
        text: Primary milestone or phase title text.
        description: Optional supporting description or subtitle text.
        badge_text: Short label displayed on the spine badge (e.g. "1", "Q1", "T+0m").
        icon: Optional icon drawing callable displayed inside the milestone card.
        style: Style for the milestone card container.
        text_style: Text style for the milestone title.
        description_style: Optional text style for the milestone description.
        badge_style: Style for the milestone badge on the spine.
        badge_text_style: Text style for the badge label.
        icon_style: Optional style passed to the icon callable.
        show: Whether to render this milestone item while preserving timeline geometry.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    text: str
    description: str = ""
    badge_text: str | None = None
    icon: Callable[..., Any] | None = None
    style: Style
    text_style: Style
    description_style: Style | None = None
    badge_style: Style
    badge_text_style: Style
    icon_style: Style | None = None
    show: bool = True


class Roadmap:
    """SmartArt component for rendering linear timelines, curved agendas, and milestone roadmaps."""

    @validate_call
    def __init__(  # noqa: PLR0913
        self,
        *,
        style: Style,
        text_style: Style,
        spine_style: Style,
        badge_style: Style,
        badge_text_style: Style,
        description_style: Style | None = None,
        icon_style: Style | None = None,
        direction: Literal["vertical", "horizontal"] = "vertical",
        curve_bend: float = 0.0,
        card_shape: Literal["pill", "rounded_rect"] = "rounded_rect",
        alternating: bool = False,
        spacing: PosFloat = 2.5,
    ) -> None:
        """Initialize Roadmap with explicit default styles.

        Args:
            style: Default style for milestone card containers.
            text_style: Default text style for milestone titles.
            spine_style: Line style for the timeline/roadmap spine.
            badge_style: Default style for spine milestone badges.
            badge_text_style: Default text style for spine badge labels.
            description_style: Default text style for milestone descriptions/subtitles.
            icon_style: Default style passed to milestone card icons.
            direction: Spine orientation ("vertical" for top-to-bottom timeline/agenda,
                "horizontal" for left-to-right milestone roadmap). Defaults to "vertical".
            curve_bend: Quadratic Bezier bend ratio for vertical roadmaps (between -0.5 and 0.5;
                0.0 renders a straight spine with an arrowhead). Defaults to 0.0.
            card_shape: Shape of milestone cards ("rounded_rect" or "pill"). Defaults to "rounded_rect".
            alternating: Whether horizontal roadmap cards alternate above and below the spine.
                Defaults to False.
            spacing: Gap in canvas units between adjacent milestone cards. Defaults to 2.5.

        Raises:
            ValueError: If curve_bend is outside [-0.5, 0.5].
        """
        if not -0.5 <= curve_bend <= 0.5:
            raise ValueError("curve_bend must be between -0.5 and 0.5.")

        self._style: Style = style
        self._text_style: Style = text_style
        self._spine_style: Style = spine_style
        self._badge_style: Style = badge_style
        self._badge_text_style: Style = badge_text_style
        self._description_style: Style | None = description_style
        self._icon_style: Style | None = icon_style
        self._direction: Literal["vertical", "horizontal"] = direction
        self._curve_bend: float = float(curve_bend)
        self._card_shape: Literal["pill", "rounded_rect"] = card_shape
        self._alternating: bool = bool(alternating)
        self._spacing: float = float(spacing)
        self._items: list[RoadmapItem] = []

    @property
    def items(self) -> list[RoadmapItem]:
        """Return the registered roadmap milestone items."""
        return self._items

    @validate_call
    def add(  # noqa: PLR0913
        self,
        text: str,
        description: str = "",
        *,
        badge_text: str | None = None,
        icon: Callable[..., Any] | None = None,
        style: Style | None = None,
        text_style: Style | None = None,
        description_style: Style | None = None,
        badge_style: Style | None = None,
        badge_text_style: Style | None = None,
        icon_style: Style | None = None,
        show: bool = True,
    ) -> RoadmapItem:
        """Add a milestone or phase item to the roadmap.

        Args:
            text: Primary milestone or phase title text.
            description: Supporting description or subtitle text. Defaults to "".
            badge_text: Optional short label on the spine badge (defaults to "1", "2", ... if None).
            icon: Optional icon drawing function displayed inside the milestone card.
            style: Custom style for this milestone's card container. If None, default style is used.
            text_style: Custom text style for this milestone's title. If None, default text_style is used.
            description_style: Custom text style for this milestone's description.
                If None, default description_style is used.
            badge_style: Custom style for this milestone's spine badge. If None, default badge_style is used.
            badge_text_style: Custom text style for this milestone's badge label.
                If None, default badge_text_style is used.
            icon_style: Custom style for this milestone's icon. If None, default icon_style is used.
            show: Whether to render this milestone item. Defaults to True.

        Returns:
            RoadmapItem: The created mutable roadmap item instance.

        Raises:
            ValueError: If description or icon is provided without a corresponding style.
        """
        idx = len(self._items)
        effective_style = style if style is not None else self._style
        effective_text_style = text_style if text_style is not None else self._text_style
        effective_desc_style = description_style if description_style is not None else self._description_style
        effective_badge_style = badge_style if badge_style is not None else self._badge_style
        effective_badge_text_style = badge_text_style if badge_text_style is not None else self._badge_text_style
        effective_icon_style = icon_style if icon_style is not None else self._icon_style

        if bool(description.strip()) and effective_desc_style is None:
            raise ValueError(
                "Neither default 'description_style' nor item 'description_style' was provided "
                f"for description of item '{text}'."
            )
        if icon is not None and effective_icon_style is None:
            raise ValueError(
                f"Neither default 'icon_style' nor item 'icon_style' was provided for icon of item '{text}'."
            )

        resolved_badge_text = badge_text if badge_text is not None else str(idx + 1)

        item = RoadmapItem(
            text=text,
            description=description,
            badge_text=resolved_badge_text,
            icon=icon,
            style=effective_style,
            text_style=effective_text_style,
            description_style=effective_desc_style,
            badge_style=effective_badge_style,
            badge_text_style=effective_badge_text_style,
            icon_style=effective_icon_style,
            show=show,
        )
        self._items.append(item)
        return item

    @validate_call
    def draw(
        self,
        xy: Coordinate,
        width: PosFloat = 100.0,
        height: PosFloat = 60.0,
        *,
        align: Literal["bottom_left", "center"] = "bottom_left",
        scale: PosFloat = 1.0,
    ) -> Self:
        """Draw the roadmap within the specified bounding box.

        Args:
            xy: Anchor coordinate (x, y) of the overall bounding box.
            width: Total width of the roadmap. Defaults to 100.0.
            height: Total height of the roadmap. Defaults to 60.0.
            align: Anchor alignment of `xy` ("bottom_left" or "center").
                Defaults to "bottom_left".
            scale: Proportional scale factor around xy. Defaults to 1.0.

        Returns:
            Self: This Roadmap instance for method chaining.
        """
        if not self._items:
            return self

        total_w = float(width)
        total_h = float(height)
        x0 = float(xy[0]) - total_w / 2.0 if align == "center" else float(xy[0])
        y0 = float(xy[1]) - total_h / 2.0 if align == "center" else float(xy[1])

        with transform(origin=xy, scale=scale):
            if self._direction == "vertical":
                if abs(self._curve_bend) < 1e-6:
                    self._draw_vertical_straight(x0=x0, y0=y0, total_w=total_w, total_h=total_h)
                else:
                    self._draw_vertical_curved(x0=x0, y0=y0, total_w=total_w, total_h=total_h)
            else:
                self._draw_horizontal(x0=x0, y0=y0, total_w=total_w, total_h=total_h)

        return self

    def _draw_vertical_straight(
        self,
        *,
        x0: float,
        y0: float,
        total_w: float,
        total_h: float,
    ) -> None:
        """Render vertical straight spine timeline with milestone badges and cards."""
        num_items = len(self._items)
        max_badge_len = max((len(it.badge_text or "") for it in self._items), default=1)
        is_wide_badge = max_badge_len >= 3

        avail_h = total_h - 6.0 - max(0, num_items - 1) * self._spacing
        card_h = min(13.0, max(5.5, avail_h / max(num_items, 1)))
        badge_h = min(6.0, card_h * 0.56)
        badge_w = max(badge_h, min(13.0, total_w * 0.14)) if is_wide_badge else badge_h

        spine_x = x0 + badge_w / 2.0 + 1.5
        y_spine_top = y0 + total_h - 1.5
        y_spine_bot = y0 + 1.5

        canvas_line(
            xy1=(spine_x, y_spine_top),
            xy2=(spine_x, y_spine_bot),
            arrow_head="->",
            style=self._spine_style,
        )

        y_first = y0 + total_h - card_h / 2.0 - 2.5
        y_last = y0 + card_h / 2.0 + 4.5
        step_y = (y_first - y_last) / (num_items - 1) if num_items > 1 else 0.0

        card_left = spine_x + badge_w / 2.0 + max(2.6, total_w * 0.032)
        card_w = max(8.0, (x0 + total_w - 1.0) - card_left)
        cx_card = card_left + card_w / 2.0

        for i, item in enumerate(self._items):
            if not item.show:
                continue

            yi = y_first - i * step_y if num_items > 1 else y0 + total_h / 2.0
            canvas_line(
                xy1=(spine_x, yi),
                xy2=(card_left, yi),
                style=self._spine_style,
            )

            if is_wide_badge:
                canvas_rectangle(
                    xy=(spine_x, yi),
                    width=badge_w,
                    height=badge_h,
                    style=item.badge_style.patch(shape_r=badge_h / 2.0),
                    text=item.badge_text or "",
                    text_style=item.badge_text_style.patch(halign="center", valign="center"),
                )
            else:
                canvas_circle(
                    xy=(spine_x, yi),
                    radius=badge_h / 2.0,
                    style=item.badge_style,
                    text=item.badge_text or "",
                    text_style=item.badge_text_style.patch(halign="center", valign="center"),
                )

            self._draw_card_box_and_content(
                item=item,
                cx=cx_card,
                cy=yi,
                card_w=card_w,
                card_h=card_h,
            )

    def _draw_vertical_curved(
        self,
        *,
        x0: float,
        y0: float,
        total_w: float,
        total_h: float,
    ) -> None:
        """Render vertical quadratic Bezier curved arc roadmap."""
        num_items = len(self._items)
        p_start = (x0 + total_w * 0.09, y0 + total_h * 0.90)
        p_end = (x0 + total_w * 0.08, y0 + total_h * 0.10)
        p_ctrl = (x0 + total_w * (0.09 + self._curve_bend), y0 + total_h * 0.50)

        canvas_line_bezier1(
            xy1=p_start,
            xy2=p_end,
            cp=p_ctrl,
            style=self._spine_style,
        )

        avail_h = total_h * 0.84 - max(0, num_items - 1) * self._spacing
        card_h = min(12.0, max(5.5, avail_h / max(num_items, 1)))
        r_badge = min(3.4, card_h * 0.34)

        for i, item in enumerate(self._items):
            if not item.show:
                continue

            t = i / (num_items - 1) if num_items > 1 else 0.5
            xi = (1.0 - t) ** 2 * p_start[0] + 2.0 * (1.0 - t) * t * p_ctrl[0] + t**2 * p_end[0]
            yi = (1.0 - t) ** 2 * p_start[1] + 2.0 * (1.0 - t) * t * p_ctrl[1] + t**2 * p_end[1]

            canvas_circle(
                xy=(xi, yi),
                radius=r_badge,
                style=item.badge_style,
                text=item.badge_text or "",
                text_style=item.badge_text_style.patch(halign="center", valign="center"),
            )

            card_left = xi + r_badge + max(2.0, total_w * 0.025)
            card_w = max(8.0, (x0 + total_w - 1.0) - card_left)
            cx_card = card_left + card_w / 2.0

            self._draw_card_box_and_content(
                item=item,
                cx=cx_card,
                cy=yi,
                card_w=card_w,
                card_h=card_h,
            )

    def _draw_horizontal(
        self,
        *,
        x0: float,
        y0: float,
        total_w: float,
        total_h: float,
    ) -> None:
        """Render horizontal milestone roadmap with optional alternating top/bottom cards."""
        num_items = len(self._items)

        if self._alternating:
            y_spine = y0 + total_h * 0.50
            card_h = min(13.0, total_h * 0.31)
            r_badge = min(3.2, total_h * 0.085)
            stem_gap = max(2.0, total_h * 0.065)
            cy_top = y_spine + r_badge + stem_gap + card_h / 2.0
            cy_bot = y_spine - r_badge - stem_gap - card_h / 2.0
        else:
            y_spine = y0 + max(5.0, total_h * 0.22)
            r_badge = min(3.2, total_h * 0.09)
            card_h = min(16.0, total_h * 0.52)
            stem_gap = max(2.2, total_h * 0.08)
            cy_top = y_spine + r_badge + stem_gap + card_h / 2.0
            cy_bot = cy_top

        canvas_line(
            xy1=(x0 + 1.5, y_spine),
            xy2=(x0 + total_w - 1.5, y_spine),
            arrow_head="->",
            style=self._spine_style,
        )

        base_w = max(8.0, (total_w - 6.0 - (num_items - 1) * self._spacing) / num_items)
        if self._alternating and num_items >= 3:
            max_alt_w = (2.0 * (total_w - 5.0) - self._spacing * (num_items - 1)) / (num_items + 1)
            card_w = max(8.0, min(base_w * 1.24, max_alt_w))
        else:
            card_w = base_w

        x_first = x0 + card_w / 2.0 + 1.5
        x_last = x0 + total_w - card_w / 2.0 - 3.5
        step_x = (x_last - x_first) / (num_items - 1) if num_items > 1 else 0.0

        for i, item in enumerate(self._items):
            if not item.show:
                continue

            xi = x_first + i * step_x if num_items > 1 else x0 + total_w / 2.0
            is_top = True if not self._alternating else (i % 2 == 0)
            cy_card = cy_top if is_top else cy_bot
            y_stem_end = cy_card - card_h / 2.0 if is_top else cy_card + card_h / 2.0

            canvas_line(
                xy1=(xi, y_spine),
                xy2=(xi, y_stem_end),
                style=self._spine_style,
            )

            canvas_circle(
                xy=(xi, y_spine),
                radius=r_badge,
                style=item.badge_style,
                text=item.badge_text or "",
                text_style=item.badge_text_style.patch(halign="center", valign="center"),
            )

            self._draw_card_box_and_content(
                item=item,
                cx=xi,
                cy=cy_card,
                card_w=card_w,
                card_h=card_h,
            )

    def _draw_card_box_and_content(
        self,
        *,
        item: RoadmapItem,
        cx: float,
        cy: float,
        card_w: float,
        card_h: float,
    ) -> None:
        """Render a milestone card box and its optional icon, title, and description."""
        if self._card_shape == "pill":
            c_style = item.style.patch(shape_r=card_h / 2.0)
        elif item.style.shape_r is None:
            c_style = item.style.patch(shape_r=min(2.2, card_h * 0.18))
        else:
            c_style = item.style
        canvas_rectangle(xy=(cx, cy), width=card_w, height=card_h, style=c_style)

        x_left = cx - card_w / 2.0
        pad_x = card_h * 0.38 if self._card_shape == "pill" else max(2.2, card_w * 0.05)
        text_x = x_left + pad_x

        if item.icon is not None:
            if item.icon_style is None:
                raise ValueError(f"icon_style is required for icon of item '{item.text}'.")
            icon_w = min(card_h * 0.36, card_w * 0.14, 4.2)
            icon_cx = text_x + icon_w / 2.0
            item.icon((icon_cx, cy), width=icon_w, style=item.icon_style)
            text_x = icon_cx + icon_w / 2.0 + max(1.6, card_w * 0.03)

        draw_card_title_and_description(
            text_x=text_x,
            cy=cy,
            card_h=card_h,
            text=item.text,
            description=item.description,
            text_style=item.text_style,
            description_style=item.description_style,
            halign="left",
        )
