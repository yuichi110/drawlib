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

from collections.abc import Callable
from typing import Any, Literal, Self

from pydantic import BaseModel, ConfigDict, validate_call

from drawlib._core.l2_types import Coordinate, PosFloat
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas import circle as canvas_circle
from drawlib._core.l4_canvas import line as canvas_line
from drawlib._core.l4_canvas import rectangle as canvas_rectangle
from drawlib._core.l4_canvas import text as canvas_text
from drawlib._core.l4_canvas import transform
from drawlib._smartarts._common import (
    draw_card_title_and_description,
    resolve_card_box_style,
)


class CardListItem(BaseModel):
    """Mutable item model for a single rich card in CardList.

    Attributes:
        text: Primary card title text.
        description: Optional supporting description text (single-line or multi-line).
        badge_text: Optional short badge label (e.g. "1", "L1", "P0").
        icon: Optional icon drawing callable (e.g. from drawlib.icons.phosphor).
        style: Card background rectangle style.
        text_style: Text style for the card title.
        description_style: Optional text style for the card description.
        badge_style: Optional style for the badge background shape.
        badge_text_style: Optional text style for the badge label.
        icon_style: Optional style passed to the icon callable.
        show: Whether to render this card item while preserving list layout geometry.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    text: str
    description: str = ""
    badge_text: str | None = None
    icon: Callable[..., Any] | None = None
    style: Style
    text_style: Style
    description_style: Style | None = None
    badge_style: Style | None = None
    badge_text_style: Style | None = None
    icon_style: Style | None = None
    show: bool = True


class CardList:
    """SmartArt component for rendering icon/badge-equipped feature or step cards."""

    @validate_call
    def __init__(  # noqa: PLR0913
        self,
        *,
        style: Style,
        text_style: Style,
        description_style: Style | None = None,
        badge_shape: Literal["circle", "rounded_rect", "none"] = "rounded_rect",
        badge_style: Style | None = None,
        badge_text_style: Style | None = None,
        icon_style: Style | None = None,
        direction: Literal["vertical", "horizontal"] = "vertical",
        spacing: PosFloat = 2.5,
        show_arrows: bool = False,
        arrow_style: Style | None = None,
    ) -> None:
        """Initialize CardList with explicit default styles.

        Args:
            style: Default background card style.
            text_style: Default text style for primary card titles.
            description_style: Default text style for card descriptions.
            badge_shape: Shape of the leading badge ("circle", "rounded_rect", or "none").
                Defaults to "rounded_rect".
            badge_style: Default style for badge background shapes.
            badge_text_style: Default text style for badge labels.
            icon_style: Default style passed to icon callables.
            direction: Layout direction ("vertical" for top-to-bottom stack, "horizontal" for
                left-to-right sequence). Defaults to "vertical".
            spacing: Gap in canvas units between adjacent cards. Defaults to 2.5.
            show_arrows: Whether to draw connecting arrows ("->") between adjacent visible cards.
                Defaults to False.
            arrow_style: Line style for connecting arrows (required when show_arrows=True).

        Raises:
            ValueError: If show_arrows=True and arrow_style is None.
        """
        if show_arrows and arrow_style is None:
            raise ValueError("'arrow_style' must be provided when show_arrows=True.")

        self._style: Style = style
        self._text_style: Style = text_style
        self._description_style: Style | None = description_style
        self._badge_shape: Literal["circle", "rounded_rect", "none"] = badge_shape
        self._badge_style: Style | None = badge_style
        self._badge_text_style: Style | None = badge_text_style
        self._icon_style: Style | None = icon_style
        self._direction: Literal["vertical", "horizontal"] = direction
        self._spacing: float = float(spacing)
        self._show_arrows: bool = bool(show_arrows)
        self._arrow_style: Style | None = arrow_style
        self._items: list[CardListItem] = []

    @property
    def items(self) -> list[CardListItem]:
        """Return the registered card list items."""
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
    ) -> CardListItem:
        """Add a card item to the list.

        Args:
            text: Primary card title text.
            description: Optional supporting description text. Defaults to "".
            badge_text: Optional short text displayed inside the badge (e.g. "1", "L1").
            icon: Optional icon drawing function (e.g. phosphor.shield_check).
            style: Custom background style for this card. If None, default style is used.
            text_style: Custom text style for this card's title. If None, default text_style is used.
            description_style: Custom text style for this card's description.
                If None, default description_style is used.
            badge_style: Custom background style for this card's badge.
                If None, default badge_style is used.
            badge_text_style: Custom text style for this card's badge text.
                If None, default badge_text_style is used.
            icon_style: Custom style for this card's icon. If None, default icon_style is used.
            show: Whether to render this card item. Defaults to True.

        Returns:
            CardListItem: The created mutable card list item instance.

        Raises:
            ValueError: If required optional styles (description_style, badge_style,
                badge_text_style, icon_style) are missing when their features are used.
        """
        effective_style = style if style is not None else self._style
        effective_text_style = text_style if text_style is not None else self._text_style
        effective_desc_style = description_style if description_style is not None else self._description_style
        effective_badge_style = badge_style if badge_style is not None else self._badge_style
        effective_badge_text_style = badge_text_style if badge_text_style is not None else self._badge_text_style
        effective_icon_style = icon_style if icon_style is not None else self._icon_style

        has_desc = bool(description.strip())
        has_badge_text = bool(badge_text and badge_text.strip())
        has_lead = icon is not None or has_badge_text

        if has_desc and effective_desc_style is None:
            raise ValueError(
                "Neither default 'description_style' nor item 'description_style' was provided "
                f"for description of item '{text}'."
            )
        if self._badge_shape != "none" and has_lead and effective_badge_style is None:
            raise ValueError(
                "Neither default 'badge_style' nor item 'badge_style' was provided "
                f"for badge of item '{text}'."
            )
        if has_badge_text and effective_badge_text_style is None:
            raise ValueError(
                "Neither default 'badge_text_style' nor item 'badge_text_style' was provided "
                f"for badge_text of item '{text}'."
            )
        if icon is not None and effective_icon_style is None:
            raise ValueError(
                "Neither default 'icon_style' nor item 'icon_style' was provided "
                f"for icon of item '{text}'."
            )

        item = CardListItem(
            text=text,
            description=description,
            badge_text=badge_text,
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
                has_any_lead = any(
                    it.icon is not None or bool(it.badge_text and it.badge_text.strip())
                    for it in self._items
                )

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
                        and self._arrow_style is not None
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
                        and self._arrow_style is not None
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

        card_style = resolve_card_box_style(item.style, card_h, max_r=2.2)
        canvas_rectangle(xy=(cx, cy), width=card_w, height=card_h, style=card_style)

        if has_any_lead:
            badge_size = min(card_h * 0.68, card_w * 0.14, 8.2)
            left_pad = max(1.8, min(3.2, card_w * 0.032))
            bx = x_left + left_pad + badge_size / 2.0
            by = cy

            if item.icon is not None or bool(item.badge_text and item.badge_text.strip()):
                self._draw_badge_and_icon(item=item, bx=bx, by=by, badge_size=badge_size)

            text_x = x_left + left_pad + badge_size + max(2.0, card_w * 0.032)
        else:
            text_x = x_left + max(2.2, card_w * 0.04)

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

        has_lead = item.icon is not None or bool(item.badge_text and item.badge_text.strip())
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

        t_style = item.text_style.patch(halign="center", valign="center")
        canvas_text(xy=(cx, title_y), text=item.text, style=t_style)

        if has_desc:
            if item.description_style is None:
                raise ValueError(
                    "Neither default 'description_style' nor item 'description_style' was provided "
                    f"for description of item '{item.text}'."
                )
            d_style = item.description_style.patch(halign="center", valign="center")
            canvas_text(xy=(cx, desc_y), text=item.description, style=d_style)

    def _validate_badge_styles(self, item: CardListItem) -> None:
        """Verify that required badge, icon, and badge_text styles are present on item."""
        if self._badge_shape != "none" and item.badge_style is None:
            raise ValueError(f"badge_style is required for badge of item '{item.text}'.")
        if item.icon is not None and item.icon_style is None:
            raise ValueError(f"icon_style is required for icon of item '{item.text}'.")
        if bool(item.badge_text and item.badge_text.strip()) and item.badge_text_style is None:
            raise ValueError(f"badge_text_style is required for badge_text of item '{item.text}'.")

    def _draw_badge_and_icon(
        self,
        *,
        item: CardListItem,
        bx: float,
        by: float,
        badge_size: float,
    ) -> None:
        """Render the badge shape (circle or rounded_rect) and inner icon/badge_text at (bx, by)."""
        self._validate_badge_styles(item)
        if self._badge_shape != "none" and item.badge_style is not None:
            if self._badge_shape == "circle":
                canvas_circle(xy=(bx, by), radius=badge_size / 2.0, style=item.badge_style)
            else:
                canvas_rectangle(
                    xy=(bx, by),
                    width=badge_size,
                    height=badge_size,
                    style=item.badge_style.patch(shape_r=badge_size * 0.24),
                )

        badge_label = item.badge_text if item.badge_text and item.badge_text.strip() else None
        if item.icon is not None and badge_label is not None:
            if item.icon_style is not None:
                item.icon((bx, by + badge_size * 0.14), width=badge_size * 0.46, style=item.icon_style)
            if item.badge_text_style is not None:
                b_style = item.badge_text_style.patch(halign="center", valign="center")
                canvas_text(xy=(bx, by - badge_size * 0.26), text=badge_label, style=b_style)
        elif item.icon is not None and item.icon_style is not None:
            item.icon((bx, by), width=badge_size * 0.56, style=item.icon_style)
        elif badge_label is not None and item.badge_text_style is not None:
            b_style = item.badge_text_style.patch(halign="center", valign="center")
            canvas_text(xy=(bx, by), text=badge_label, style=b_style)


