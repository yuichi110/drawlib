# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""CardList SmartArt implementation module."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Any, Literal, Self

from pydantic import BaseModel, ConfigDict, validate_call

from drawlib import styles as _styles
from drawlib._core.l2_types import ColorRGB, ColorRGBA, Coordinate, PosFloat
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas import circle as canvas_circle
from drawlib._core.l4_canvas import line as canvas_line
from drawlib._core.l4_canvas import rectangle as canvas_rectangle
from drawlib._core.l4_canvas import text as canvas_text
from drawlib._core.l4_canvas import transform

_DEFAULT_BADGE_PALETTE: tuple[ColorRGB | ColorRGBA, ...] = (
    (37, 99, 235),
    (13, 148, 136),
    (124, 58, 237),
    (245, 158, 11),
    (220, 38, 38),
    (16, 185, 129),
)


class CardListItem(BaseModel):
    """Mutable item model for a single rich card in CardList.

    Attributes:
        title: Primary bold card title text.
        description: Optional supporting description text (single-line or multi-line).
        badge_text: Optional short badge label (e.g. "1", "L1", "P0").
        icon: Optional icon drawing callable (e.g. from drawlib.icons.phosphor).
        style: Card background rectangle style.
        title_style: Text style for the card title.
        description_style: Text style for the card description.
        badge_style: Optional style for the badge background shape.
        badge_text_style: Text style for the badge label.
        icon_style: Style passed to the icon callable.
        show: Whether to render this card item while preserving list layout geometry.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    title: str
    description: str = ""
    badge_text: str | None = None
    icon: Callable[..., Any] | None = None
    style: Style
    title_style: Style
    description_style: Style
    badge_style: Style | None = None
    badge_text_style: Style
    icon_style: Style
    show: bool = True


class CardList:
    """SmartArt component for rendering icon/badge-equipped feature or step cards."""

    @validate_call
    def __init__(  # noqa: PLR0913
        self,
        *,
        style: Style | None = None,
        title_style: Style | None = None,
        description_style: Style | None = None,
        badge_shape: Literal["circle", "rounded_rect", "none"] = "rounded_rect",
        badge_style: Style | None = None,
        badge_text_style: Style | None = None,
        badge_palette: Sequence[ColorRGB | ColorRGBA] | None = None,
        icon_style: Style | None = None,
        direction: Literal["vertical", "horizontal"] = "vertical",
        spacing: float = 2.5,
        show_arrows: bool = False,
        arrow_style: Style | None = None,
    ) -> None:
        """Initialize CardList.

        Args:
            style: Default background card style. Defaults to Styles.Neutral with rounded corners.
            title_style: Default text style for card titles. Defaults to Styles.DarkBold.
            description_style: Default text style for card descriptions. Defaults to muted Dark text.
            badge_shape: Shape of the leading badge ("circle", "rounded_rect", or "none").
                Defaults to "rounded_rect".
            badge_style: Optional uniform style for badge backgrounds. If None, cycles through
                badge_palette automatically.
            badge_text_style: Default text style for badge labels. Defaults to Styles.WhiteBold.
            badge_palette: Sequence of RGB/RGBA color tuples cycled per card when badge_style is None.
            icon_style: Default style for icons. Defaults to Styles.White when badge_shape != "none",
                or accent-colored style when badge_shape == "none".
            direction: Layout direction ("vertical" for top-to-bottom stack, "horizontal" for
                left-to-right sequence). Defaults to "vertical".
            spacing: Gap in canvas units between adjacent cards (must be >= 0.0). Defaults to 2.5.
            show_arrows: Whether to draw connecting arrows ("->") between adjacent visible cards.
                Defaults to False.
            arrow_style: Optional line style for connecting arrows. Defaults to Styles.PrimaryBold.

        Raises:
            ValueError: If spacing < 0.0 or badge_palette is empty when provided.
        """
        if spacing < 0.0:
            raise ValueError("spacing must be >= 0.0.")
        if badge_palette is not None and len(badge_palette) == 0:
            raise ValueError("badge_palette must not be empty when provided.")

        default_card_style = _styles.Styles.Neutral
        if default_card_style.shape_r is None:
            default_card_style = default_card_style.patch(shape_r=2.2)

        default_halign: Literal["left", "center"] = "left" if direction == "vertical" else "center"

        self._style: Style = style if style is not None else default_card_style
        self._title_style: Style = (
            title_style
            if title_style is not None
            else _styles.Styles.DarkBold.patch(
                text_size=10.2,
                text_color=(15, 23, 42),
                halign=default_halign,
                valign="center",
            )
        )
        self._description_style: Style = (
            description_style
            if description_style is not None
            else _styles.Styles.Dark.patch(
                text_size=8.5,
                text_color=(100, 116, 139),
                halign=default_halign,
                valign="center",
            )
        )
        self._badge_shape: Literal["circle", "rounded_rect", "none"] = badge_shape
        self._badge_style: Style | None = badge_style
        self._badge_text_style: Style = (
            badge_text_style
            if badge_text_style is not None
            else _styles.Styles.WhiteBold.patch(text_size=9.5, halign="center", valign="center")
        )
        self._badge_palette: tuple[ColorRGB | ColorRGBA, ...] = (
            tuple(badge_palette) if badge_palette is not None else _DEFAULT_BADGE_PALETTE
        )
        self._icon_style: Style | None = icon_style
        self._direction: Literal["vertical", "horizontal"] = direction
        self._spacing: float = float(spacing)
        self._show_arrows: bool = bool(show_arrows)
        self._arrow_style: Style = (
            arrow_style if arrow_style is not None else _styles.Styles.PrimaryBold.patch(line_width=1.8)
        )
        self._items: list[CardListItem] = []

    @property
    def items(self) -> list[CardListItem]:
        """Return the registered card list items."""
        return self._items

    @validate_call
    def add(  # noqa: PLR0913
        self,
        title: str,
        description: str = "",
        *,
        badge_text: str | None = None,
        icon: Callable[..., Any] | None = None,
        style: Style | None = None,
        title_style: Style | None = None,
        description_style: Style | None = None,
        badge_style: Style | None = None,
        badge_text_style: Style | None = None,
        icon_style: Style | None = None,
        show: bool = True,
    ) -> CardListItem:
        """Add a card item to the list.

        Args:
            title: Primary bold card title text.
            description: Optional supporting description text. Defaults to "".
            badge_text: Optional short text displayed inside the badge (e.g. "1", "L1").
            icon: Optional icon drawing function (e.g. phosphor.shield_check).
            style: Custom background style for this card.
            title_style: Custom text style for this card's title.
            description_style: Custom text style for this card's description.
            badge_style: Custom background style for this card's badge.
            badge_text_style: Custom text style for this card's badge text.
            icon_style: Custom style for this card's icon.
            show: Whether to render this card item. Defaults to True.

        Returns:
            CardListItem: The created mutable card list item instance.
        """
        idx = len(self._items)
        palette_color = self._badge_palette[idx % len(self._badge_palette)]

        if badge_style is not None:
            resolved_badge_style = badge_style
        elif self._badge_style is not None:
            resolved_badge_style = self._badge_style
        else:
            resolved_badge_style = Style(
                shape_fill_color=palette_color,
                shape_line_color=palette_color,
                shape_line_width=0.0,
            )

        badge_color = resolved_badge_style.shape_fill_color or palette_color

        if icon_style is not None:
            resolved_icon_style = icon_style
        elif self._icon_style is not None:
            resolved_icon_style = self._icon_style
        elif self._badge_shape != "none":
            resolved_icon_style = _styles.Styles.White
        else:
            resolved_icon_style = _styles.Styles.Primary.patch(icon_color=badge_color)

        if badge_text_style is not None:
            resolved_badge_text_style = badge_text_style
        elif self._badge_shape == "none":
            resolved_badge_text_style = _styles.Styles.PrimaryBold.patch(
                text_size=10.5,
                text_color=badge_color,
                halign="center",
                valign="center",
            )
        else:
            resolved_badge_text_style = self._badge_text_style

        item = CardListItem(
            title=title,
            description=description,
            badge_text=badge_text,
            icon=icon,
            style=style if style is not None else self._style,
            title_style=title_style if title_style is not None else self._title_style,
            description_style=description_style if description_style is not None else self._description_style,
            badge_style=resolved_badge_style,
            badge_text_style=resolved_badge_text_style,
            icon_style=resolved_icon_style,
            show=show,
        )
        self._items.append(item)
        return item

    @validate_call
    def draw(
        self,
        xy: Coordinate,
        width: PosFloat = 90.0,
        height: PosFloat = 50.0,
        *,
        scale: PosFloat = 1.0,
    ) -> Self:
        """Draw the card list within the specified bounding box.

        Args:
            xy: Bottom-left coordinate (x, y) of the overall bounding box.
            width: Total width of the card list. Defaults to 90.0.
            height: Total height of the card list. Defaults to 50.0.
            scale: Proportional scale factor around xy. Defaults to 1.0.

        Returns:
            Self: This CardList instance for method chaining.
        """
        num_items = len(self._items)
        if num_items == 0:
            return self

        x0, y0 = float(xy[0]), float(xy[1])
        total_w = float(width)
        total_h = float(height)

        eff_spacing = max(self._spacing, 4.2) if self._show_arrows else self._spacing

        with transform(origin=xy, scale=scale):
            if self._direction == "vertical":
                card_w = total_w
                card_h = max(4.0, (total_h - (num_items - 1) * eff_spacing) / num_items)
                has_any_lead = any(it.icon is not None or it.badge_text is not None for it in self._items)

                for i, item in enumerate(self._items):
                    cx = x0 + card_w / 2.0
                    cy = y0 + total_h - i * (card_h + eff_spacing) - card_h / 2.0

                    if item.show:
                        self._draw_vertical_card(
                            item=item,
                            cx=cx,
                            cy=cy,
                            card_w=card_w,
                            card_h=card_h,
                            has_any_lead=has_any_lead,
                        )

                    if (
                        self._show_arrows
                        and i < num_items - 1
                        and item.show
                        and self._items[i + 1].show
                    ):
                        y_bot = cy - card_h / 2.0
                        y_next_top = y_bot - eff_spacing
                        pad = min(0.7, eff_spacing * 0.16)
                        canvas_line(
                            xy1=(cx, y_bot - pad),
                            xy2=(cx, y_next_top + pad),
                            arrow_head="->",
                            style=self._arrow_style,
                        )
            else:
                card_w = max(4.0, (total_w - (num_items - 1) * eff_spacing) / num_items)
                card_h = total_h

                for i, item in enumerate(self._items):
                    cx = x0 + i * (card_w + eff_spacing) + card_w / 2.0
                    cy = y0 + card_h / 2.0

                    if item.show:
                        self._draw_horizontal_card(
                            item=item,
                            cx=cx,
                            cy=cy,
                            card_w=card_w,
                            card_h=card_h,
                        )

                    if (
                        self._show_arrows
                        and i < num_items - 1
                        and item.show
                        and self._items[i + 1].show
                    ):
                        x_right = cx + card_w / 2.0
                        x_next_left = x_right + eff_spacing
                        pad = min(0.7, eff_spacing * 0.16)
                        canvas_line(
                            xy1=(x_right + pad, cy),
                            xy2=(x_next_left - pad, cy),
                            arrow_head="->",
                            style=self._arrow_style,
                        )

        return self

    def _draw_vertical_card(  # noqa: PLR0913
        self,
        *,
        item: CardListItem,
        cx: float,
        cy: float,
        card_w: float,
        card_h: float,
        has_any_lead: bool,
    ) -> None:
        """Render a single vertical-mode card at center (cx, cy)."""
        x_left = cx - card_w / 2.0

        card_style = item.style
        if card_style.shape_r is None:
            card_style = card_style.patch(shape_r=min(2.2, card_h * 0.18))
        canvas_rectangle(xy=(cx, cy), width=card_w, height=card_h, style=card_style)

        if has_any_lead:
            badge_size = min(card_h * 0.68, card_w * 0.14, 8.2)
            left_pad = max(1.8, min(3.2, card_w * 0.032))
            bx = x_left + left_pad + badge_size / 2.0
            by = cy

            if item.icon is not None or item.badge_text is not None:
                self._draw_badge_and_icon(item=item, bx=bx, by=by, badge_size=badge_size)

            text_x = x_left + left_pad + badge_size + max(2.0, card_w * 0.032)
        else:
            text_x = x_left + max(2.2, card_w * 0.04)

        has_desc = bool(item.description.strip())
        t_style = item.title_style.patch(halign="left", valign="center")

        if has_desc:
            is_multiline = "\n" in item.description.strip()
            title_y = cy + card_h * (0.23 if is_multiline else 0.18)
            desc_y = cy - card_h * (0.14 if is_multiline else 0.18)
            d_style = item.description_style.patch(halign="left", valign="center")
            canvas_text(xy=(text_x, title_y), text=item.title, style=t_style)
            canvas_text(xy=(text_x, desc_y), text=item.description, style=d_style)
        else:
            canvas_text(xy=(text_x, cy), text=item.title, style=t_style)

    def _draw_horizontal_card(
        self,
        *,
        item: CardListItem,
        cx: float,
        cy: float,
        card_w: float,
        card_h: float,
    ) -> None:
        """Render a single horizontal-mode card at center (cx, cy)."""
        card_style = item.style
        if card_style.shape_r is None:
            card_style = card_style.patch(shape_r=min(2.2, card_w * 0.1))
        canvas_rectangle(xy=(cx, cy), width=card_w, height=card_h, style=card_style)

        has_lead = item.icon is not None or item.badge_text is not None
        has_desc = bool(item.description.strip())

        if has_lead:
            badge_size = min(card_h * 0.30, card_w * 0.38, 8.2)
            by = cy + card_h * (0.25 if has_desc else 0.18)
            self._draw_badge_and_icon(item=item, bx=cx, by=by, badge_size=badge_size)
            title_y = cy - card_h * (0.03 if has_desc else 0.22)
            desc_y = cy - card_h * 0.27
        else:
            title_y = cy + card_h * (0.16 if has_desc else 0.0)
            desc_y = cy - card_h * 0.16

        t_style = item.title_style.patch(halign="center", valign="center")
        canvas_text(xy=(cx, title_y), text=item.title, style=t_style)

        if has_desc:
            d_style = item.description_style.patch(halign="center", valign="center")
            canvas_text(xy=(cx, desc_y), text=item.description, style=d_style)

    def _draw_badge_and_icon(
        self,
        *,
        item: CardListItem,
        bx: float,
        by: float,
        badge_size: float,
    ) -> None:
        """Render the badge shape (circle or rounded_rect) and inner icon/badge_text at (bx, by)."""
        if self._badge_shape == "circle" and item.badge_style is not None:
            canvas_circle(xy=(bx, by), radius=badge_size / 2.0, style=item.badge_style)
        elif self._badge_shape == "rounded_rect" and item.badge_style is not None:
            canvas_rectangle(
                xy=(bx, by),
                width=badge_size,
                height=badge_size,
                style=item.badge_style.patch(shape_r=badge_size * 0.24),
            )

        has_icon = item.icon is not None
        has_badge_text = bool(item.badge_text and item.badge_text.strip())

        if has_icon and has_badge_text and item.icon is not None and item.badge_text is not None:
            icon_w = badge_size * 0.46
            item.icon((bx, by + badge_size * 0.14), width=icon_w, style=item.icon_style)
            b_size = min(item.badge_text_style.text_size or 7.5, 7.6)
            b_style = item.badge_text_style.patch(text_size=b_size, halign="center", valign="center")
            canvas_text(xy=(bx, by - badge_size * 0.26), text=item.badge_text, style=b_style)
        elif has_icon and item.icon is not None:
            icon_w = badge_size * 0.56
            item.icon((bx, by), width=icon_w, style=item.icon_style)
        elif has_badge_text and item.badge_text is not None:
            b_style = item.badge_text_style.patch(halign="center", valign="center")
            canvas_text(xy=(bx, by), text=item.badge_text, style=b_style)
