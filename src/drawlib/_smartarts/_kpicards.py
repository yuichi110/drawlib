# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""KpiCards SmartArt implementation module."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, Literal, Self

from pydantic import BaseModel, ConfigDict

from drawlib._core.l1_core import validate_call
from drawlib._core.l2_types import Coordinate, PosFloat, PosInt
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas import line as canvas_line
from drawlib._core.l4_canvas import rectangle as canvas_rectangle
from drawlib._core.l4_canvas import text as canvas_text
from drawlib._core.l4_canvas import transform
from drawlib._smartarts._common import (
    draw_card_title_and_description,
    resolve_card_box_style,
)


class KpiCardItem(BaseModel):
    """Mutable item model for a single KPI card.

    Attributes:
        metric: Primary highlighted metric value or short callout label (e.g. "99.99%", "<50ms").
        text: Primary card title text.
        description: Optional supporting description text.
        style: Card background rectangle style.
        metric_style: Text style for the primary metric value.
        text_style: Text style for the card title.
        description_style: Optional text style for the card description.
        accent_style: Optional style for the card's accent pill or top bar.
        icon: Optional icon drawing callable (e.g. from drawlib.icons.phosphor).
        icon_style: Optional style passed to the icon callable.
        show: Whether to render this card item while preserving grid/stack geometry.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    metric: str
    text: str
    description: str = ""
    style: Style
    metric_style: Style
    text_style: Style
    description_style: Style | None = None
    accent_style: Style | None = None
    icon: Callable[..., Any] | None = None
    icon_style: Style | None = None
    show: bool = True


class KpiCards:
    """SmartArt component for rendering KPI / metric highlight cards in stacks or grids."""

    @validate_call
    def __init__(  # noqa: PLR0913
        self,
        *,
        style: Style,
        metric_style: Style,
        text_style: Style,
        description_style: Style | None = None,
        accent_style: Style | None = None,
        icon_style: Style | None = None,
        accent_position: Literal["left_pill", "top_bar", "none"] = "left_pill",
        metric_layout: Literal["left_column", "top_stack"] = "left_column",
        metric_width_ratio: float = 0.28,
        spacing: PosFloat = 3.0,
    ) -> None:
        """Initialize KpiCards with explicit default styles.

        Args:
            style: Default background card style.
            metric_style: Default text style for the primary metric value.
            text_style: Default text style for the primary card title.
            description_style: Default text style for the supporting description text.
            accent_style: Default style for the card accent indicator ("left_pill" or "top_bar").
            icon_style: Default style passed to icon callables.
            accent_position: Placement of the accent indicator ("left_pill", "top_bar", or "none").
                Defaults to "left_pill".
            metric_layout: Internal card layout mode ("left_column" for side-by-side metric and text,
                or "top_stack" for vertically stacked metric, title, and description).
                Defaults to "left_column".
            metric_width_ratio: Fraction of card width allocated to the left metric column when
                metric_layout="left_column" (must be between 0.1 and 0.7). Defaults to 0.28.
            spacing: Gap in canvas units between adjacent cards. Defaults to 3.0.

        Raises:
            ValueError: If metric_width_ratio is outside [0.1, 0.7].
        """
        if not 0.1 <= metric_width_ratio <= 0.7:
            raise ValueError("metric_width_ratio must be between 0.1 and 0.7.")

        self._style: Style = style
        self._metric_style: Style = metric_style
        self._text_style: Style = text_style
        self._description_style: Style | None = description_style
        self._accent_style: Style | None = accent_style
        self._icon_style: Style | None = icon_style
        self._accent_position: Literal["left_pill", "top_bar", "none"] = accent_position
        self._metric_layout: Literal["left_column", "top_stack"] = metric_layout
        self._metric_width_ratio: float = float(metric_width_ratio)
        self._spacing: float = float(spacing)
        self._items: list[KpiCardItem] = []

    @property
    def items(self) -> list[KpiCardItem]:
        """Return the registered KPI card items."""
        return self._items

    @validate_call
    def add(  # noqa: PLR0913
        self,
        metric: str,
        text: str,
        description: str = "",
        *,
        style: Style | None = None,
        metric_style: Style | None = None,
        text_style: Style | None = None,
        description_style: Style | None = None,
        accent_style: Style | None = None,
        icon: Callable[..., Any] | None = None,
        icon_style: Style | None = None,
        show: bool = True,
    ) -> KpiCardItem:
        """Add a KPI card item.

        Args:
            metric: Highlighted metric string or key value (e.g. "300M+", "99.99%", "<50ms").
            text: Primary card title text.
            description: Optional supporting description text. Defaults to "".
            style: Custom background style for this card. If None, default style is used.
            metric_style: Custom text style for this card's metric value. If None, default metric_style is used.
            text_style: Custom text style for this card's title. If None, default text_style is used.
            description_style: Custom text style for this card's description.
                If None, default description_style is used.
            accent_style: Custom style for this card's accent pill or top bar.
                If None, default accent_style is used.
            icon: Optional icon drawing function (e.g. phosphor.shield_check).
            icon_style: Optional style for the icon. If None, default icon_style is used.
            show: Whether to render this card item. Defaults to True.

        Returns:
            KpiCardItem: The created mutable KPI card item instance.

        Raises:
            ValueError: If required optional styles (description_style, accent_style, icon_style)
                are missing when their corresponding features are used.
        """
        effective_style = style if style is not None else self._style
        effective_metric_style = metric_style if metric_style is not None else self._metric_style
        effective_text_style = text_style if text_style is not None else self._text_style
        effective_desc_style = description_style if description_style is not None else self._description_style
        effective_accent_style = accent_style if accent_style is not None else self._accent_style
        effective_icon_style = icon_style if icon_style is not None else self._icon_style

        if bool(description.strip()) and effective_desc_style is None:
            raise ValueError(
                "Neither default 'description_style' nor item 'description_style' was provided "
                f"for description of item '{text}'."
            )
        if self._accent_position != "none" and effective_accent_style is None:
            raise ValueError(
                "Neither default 'accent_style' nor item 'accent_style' was provided "
                f"when accent_position='{self._accent_position}' for item '{text}'."
            )
        if icon is not None and effective_icon_style is None:
            raise ValueError(
                f"Neither default 'icon_style' nor item 'icon_style' was provided for icon of item '{text}'."
            )

        item = KpiCardItem(
            metric=metric,
            text=text,
            description=description,
            style=effective_style,
            metric_style=effective_metric_style,
            text_style=effective_text_style,
            description_style=effective_desc_style,
            accent_style=effective_accent_style,
            icon=icon,
            icon_style=effective_icon_style,
            show=show,
        )
        self._items.append(item)
        return item

    @validate_call
    def draw(  # noqa: PLR0913
        self,
        xy: Coordinate,
        width: PosFloat = 90.0,
        height: PosFloat = 60.0,
        *,
        columns: PosInt = 1,
        align: Literal["bottom_left", "center"] = "bottom_left",
        scale: PosFloat = 1.0,
    ) -> Self:
        """Draw the KPI cards within the specified bounding box.

        Args:
            xy: Anchor coordinate (x, y) of the overall bounding box.
            width: Total width of the KPI cards grid/stack. Defaults to 90.0.
            height: Total height of the KPI cards grid/stack. Defaults to 60.0.
            columns: Number of grid columns (1 for vertical stack, >=2 for multi-column grid).
                Defaults to 1.
            align: Anchor alignment of `xy` ("bottom_left" or "center").
                Defaults to "bottom_left".
            scale: Proportional scale factor around xy. Defaults to 1.0.

        Returns:
            Self: This KpiCards instance for method chaining.
        """
        num_items = len(self._items)
        if num_items == 0:
            return self

        total_w = float(width)
        total_h = float(height)
        x0 = float(xy[0]) - total_w / 2.0 if align == "center" else float(xy[0])
        y0 = float(xy[1]) - total_h / 2.0 if align == "center" else float(xy[1])
        cols = int(columns)
        rows = (num_items + cols - 1) // cols

        card_w = max(4.0, (total_w - (cols - 1) * self._spacing) / cols)
        card_h = max(4.0, (total_h - (rows - 1) * self._spacing) / rows)

        with transform(origin=xy, scale=scale):
            for i, item in enumerate(self._items):
                if not item.show:
                    continue

                col = i % cols
                row = i // cols
                cx = x0 + col * (card_w + self._spacing) + card_w / 2.0
                cy = y0 + total_h - row * (card_h + self._spacing) - card_h / 2.0

                self._draw_single_card(item=item, cx=cx, cy=cy, card_w=card_w, card_h=card_h)

        return self

    def _draw_single_card(
        self,
        *,
        item: KpiCardItem,
        cx: float,
        cy: float,
        card_w: float,
        card_h: float,
    ) -> None:
        """Render a single KPI card at center (cx, cy) with dimensions (card_w, card_h)."""
        x_left = cx - card_w / 2.0
        y_top = cy + card_h / 2.0

        card_style = resolve_card_box_style(item.style, card_h, max_r=2.5)
        canvas_rectangle(xy=(cx, cy), width=card_w, height=card_h, style=card_style)

        if self._accent_position == "left_pill" and item.accent_style is not None:
            pill_w = max(1.0, min(2.0, card_w * 0.022))
            pill_h = card_h * 0.68
            pill_x = x_left + pill_w * 1.25
            canvas_rectangle(
                xy=(pill_x, cy),
                width=pill_w,
                height=pill_h,
                style=item.accent_style.patch(shape_r=pill_w / 2.0),
            )
        elif self._accent_position == "top_bar" and item.accent_style is not None:
            bar_w = card_w * 0.88
            bar_h = max(0.8, min(1.6, card_h * 0.085))
            bar_y = y_top - bar_h * 0.9
            canvas_rectangle(
                xy=(cx, bar_y),
                width=bar_w,
                height=bar_h,
                style=item.accent_style.patch(shape_r=bar_h / 2.0),
            )

        if self._metric_layout == "left_column":
            self._draw_left_column_layout(item=item, cx=cx, cy=cy, card_w=card_w, card_h=card_h)
        else:
            self._draw_top_stack_layout(item=item, cx=cx, cy=cy, card_w=card_w, card_h=card_h)

    def _draw_left_column_layout(
        self,
        *,
        item: KpiCardItem,
        cx: float,
        cy: float,
        card_w: float,
        card_h: float,
    ) -> None:
        """Render card content in side-by-side left-column metric layout."""
        x_left = cx - card_w / 2.0
        has_any_icon = any(it.icon is not None for it in self._items)
        eff_ratio = max(self._metric_width_ratio, 0.33) if has_any_icon else self._metric_width_ratio
        metric_zone_w = card_w * eff_ratio

        pill_offset = (
            max(1.0, min(2.0, card_w * 0.022)) * 2.2
            if self._accent_position == "left_pill" and item.accent_style is not None
            else card_w * 0.035
        )
        metric_x = x_left + pill_offset + card_w * 0.012

        if item.icon is not None:
            if item.icon_style is None:
                raise ValueError(f"icon_style is required for icon of item '{item.text}'.")
            icon_w = min(card_h * 0.28, metric_zone_w * 0.18, 3.8)
            icon_cx = metric_x + icon_w / 2.0
            item.icon((icon_cx, cy), width=icon_w, style=item.icon_style)
            metric_x = icon_cx + icon_w / 2.0 + card_w * 0.014

        m_style = item.metric_style.patch(halign="left", valign="center")
        canvas_text(xy=(metric_x, cy), text=item.metric, style=m_style)

        # Subtle vertical divider derived from card border color
        div_x = x_left + metric_zone_w
        div_color = item.style.shape_line_color
        if div_color is not None:
            div_width = max(0.6, (item.style.shape_line_width or 1.2) * 0.65)
            canvas_line(
                xy1=(div_x, cy - card_h * 0.32),
                xy2=(div_x, cy + card_h * 0.32),
                style=Style(line_color=div_color, line_width=div_width),
            )

        text_x = div_x + card_w * 0.035
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

    @staticmethod
    def _draw_top_stack_layout(
        *,
        item: KpiCardItem,
        cx: float,
        cy: float,
        card_w: float,
        card_h: float,
    ) -> None:
        """Render card content in vertically stacked metric-above-title layout."""
        has_desc = bool(item.description.strip())

        if has_desc:
            metric_y = cy + card_h * 0.20
            title_y = cy - card_h * 0.08
            desc_y = cy - card_h * 0.30
        else:
            metric_y = cy + card_h * 0.14
            title_y = cy - card_h * 0.20
            desc_y = cy

        metric_cx = cx
        if item.icon is not None:
            if item.icon_style is None:
                raise ValueError(f"icon_style is required for icon of item '{item.text}'.")
            icon_w = min(card_h * 0.28, card_w * 0.18, 4.8)
            icon_cx = cx - card_w * 0.22
            item.icon((icon_cx, metric_y), width=icon_w, style=item.icon_style)
            metric_cx = cx + icon_w * 0.35

        m_style = item.metric_style.patch(halign="center", valign="center")
        t_style = item.text_style.patch(halign="center", valign="center")

        canvas_text(xy=(metric_cx, metric_y), text=item.metric, style=m_style)
        canvas_text(xy=(cx, title_y), text=item.text, style=t_style)

        if has_desc:
            if item.description_style is None:
                raise ValueError(
                    "Neither default 'description_style' nor item 'description_style' was provided "
                    f"for description of item '{item.text}'."
                )
            d_style = item.description_style.patch(halign="center", valign="center")
            canvas_text(xy=(cx, desc_y), text=item.description, style=d_style)


# Singular alias for convenience
KpiCard = KpiCards
