# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""ChevronProcess SmartArt implementation module."""

from __future__ import annotations

import math

from pydantic import validate_call

from drawlib._core.l2_types import Angle90, Coordinate, PosFloat
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas import chevron as canvas_chevron
from drawlib._core.l4_canvas import polygon as canvas_polygon
from drawlib._core.l4_canvas import text as canvas_text


class _ChevronItem:
    """Internal container for a single step in ChevronProcess."""

    def __init__(
        self,
        text: str,
        style: Style,
        text_style: Style,
        description_style: Style,
        description: str = "",
    ) -> None:
        self.text = text
        self.style = style
        self.text_style = text_style
        self.description_style = description_style
        self.description = description


class ChevronProcess:
    """SmartArt component for sequential chevron (arrowhead block) process diagrams."""

    @validate_call
    def __init__(
        self,
        *,
        style: Style,
        text_style: Style,
        description_style: Style,
        corner_angle: Angle90 = 60.0,
        spacing: PosFloat = 1.5,
        flat_left_end: bool = False,
    ) -> None:
        """Initialize ChevronProcess.

        Args:
            style: Default style for the chevron block shapes.
            text_style: Default style for the primary step title texts.
            description_style: Default style for the secondary description texts.
            corner_angle: Angle of the arrowhead point in degrees (between 10.0 and 80.0). Defaults to 60.0.
            spacing: Horizontal gap between consecutive chevrons. Defaults to 1.5.
            flat_left_end: Whether the first chevron has a flat vertical left edge instead of an indent.
                Defaults to False.
        """
        self._style = style
        self._text_style = text_style
        self._description_style = description_style
        self._corner_angle = float(corner_angle)
        self._spacing = float(spacing)
        self._flat_left_end = bool(flat_left_end)
        self._items: list[_ChevronItem] = []

    @property
    def items(self) -> list[_ChevronItem]:
        """Return the registered chevron items."""
        return self._items

    @validate_call
    def append(
        self,
        text: str,
        *,
        description: str = "",
        style: Style | None = None,
        text_style: Style | None = None,
        description_style: Style | None = None,
    ) -> None:
        """Append a step to the chevron process.

        Args:
            text: Primary step title text.
            description: Optional supporting description text displayed below the title.
            style: Custom Style for this chevron block. If None, default style is used.
            text_style: Custom Style for the title text. If None, default text_style is used.
            description_style: Custom Style for the description text. If None, default description_style is used.
        """
        self.insert(
            len(self._items),
            text=text,
            description=description,
            style=style,
            text_style=text_style,
            description_style=description_style,
        )

    @validate_call
    def extend(
        self,
        texts: list[str],
        *,
        descriptions: list[str] | None = None,
        styles: list[Style] | Style | None = None,
        text_styles: list[Style] | Style | None = None,
        description_styles: list[Style] | Style | None = None,
    ) -> None:
        """Extend the process with multiple step titles and optional descriptions/styles.

        Args:
            texts: List of step title texts.
            descriptions: Optional list of corresponding descriptions.
            styles: Optional Style applied to all steps or a list of Styles matching texts length.
            text_styles: Optional Style applied to all step titles or a list of Styles.
            description_styles: Optional Style applied to all descriptions or a list of Styles.

        Raises:
            ValueError: If a provided style list length does not match texts length.
        """
        n = len(texts)

        def _resolve_list(val: list[Style] | Style | None, name: str) -> list[Style | None]:
            if val is None:
                return [None] * n
            if isinstance(val, Style):
                return [val] * n
            if len(val) != n:
                raise ValueError(f"Length of '{name}' ({len(val)}) must match length of 'texts' ({n}).")
            return list(val)

        style_list = _resolve_list(styles, "styles")
        text_style_list = _resolve_list(text_styles, "text_styles")
        desc_style_list = _resolve_list(description_styles, "description_styles")

        for i, text in enumerate(texts):
            desc = descriptions[i] if descriptions and i < len(descriptions) else ""
            self.append(
                text=text,
                description=desc,
                style=style_list[i],
                text_style=text_style_list[i],
                description_style=desc_style_list[i],
            )

    @validate_call
    def insert(
        self,
        index: int,
        text: str,
        *,
        description: str = "",
        style: Style | None = None,
        text_style: Style | None = None,
        description_style: Style | None = None,
    ) -> None:
        """Insert a step at the specified index.

        Args:
            index: Position index to insert the step.
            text: Primary step title text.
            description: Optional supporting description text.
            style: Custom Style for this chevron block. If None, default style is used.
            text_style: Custom Style for the title text. If None, default text_style is used.
            description_style: Custom Style for the description text. If None, default description_style is used.
        """
        effective_style = style if style is not None else self._style
        effective_text_style = text_style if text_style is not None else self._text_style
        effective_desc_style = description_style if description_style is not None else self._description_style

        item = _ChevronItem(
            text=text,
            style=effective_style,
            text_style=effective_text_style,
            description_style=effective_desc_style,
            description=description,
        )
        self._items.insert(index, item)

    @validate_call
    def draw(
        self,
        xy: Coordinate,
        width: PosFloat = 90.0,
        height: PosFloat = 12.0,
        item_width: PosFloat | None = None,
    ) -> None:
        """Draw the chevron process diagram at the specified location.

        Args:
            xy: Bottom-left coordinate (x, y) of the starting bounding box.
            width: Overall width allocated for the entire process. Used when item_width is None.
            height: Height of each chevron block.
            item_width: Optional explicit width per chevron block. If None, calculated evenly from width.
        """
        num_items = len(self._items)
        if num_items == 0:
            return

        x0, y0 = xy
        h = float(height)
        cy = y0 + h / 2.0
        angle_rad = math.radians(self._corner_angle)
        x_indent = (h / 2.0) / math.tan(angle_rad)

        # Calculate item_width if not explicitly given
        if item_width is not None:
            w_item = float(item_width)
        else:
            total_gaps = (num_items - 1) * self._spacing
            # Total width = N * w_item + (N - 1) * spacing + x_indent
            available_w = float(width) - total_gaps - x_indent
            w_item = max(2.0, available_w / num_items)

        total_w = w_item + x_indent

        if not self._flat_left_end:
            # All items are standard chevrons centered at cx_i
            cx_0 = x0 + total_w / 2.0
            for i, item in enumerate(self._items):
                cx = cx_0 + i * (w_item + self._spacing)
                canvas_chevron(
                    xy=(cx, cy),
                    width=w_item,
                    height=h,
                    corner_angle=self._corner_angle,
                    style=item.style,
                )
                self._draw_item_texts(item, cx, cy, h)
        else:
            # First item is a flat-backed pentagon, subsequent items are chevrons
            for i, item in enumerate(self._items):
                if i == 0:
                    points = [
                        (x0, y0),
                        (x0, y0 + h),
                        (x0 + w_item, y0 + h),
                        (x0 + w_item + x_indent, cy),
                        (x0 + w_item, y0),
                    ]
                    canvas_polygon(xys=points, style=item.style)
                    cx = x0 + (w_item + x_indent * 0.35) / 2.0
                else:
                    # Align indentation with the previous chevron's tip + spacing
                    cx = x0 + (1.5 + (i - 1)) * w_item + i * self._spacing + 0.5 * x_indent
                    canvas_chevron(
                        xy=(cx, cy),
                        width=w_item,
                        height=h,
                        corner_angle=self._corner_angle,
                        style=item.style,
                    )
                self._draw_item_texts(item, cx, cy, h)

    @staticmethod
    def _draw_item_texts(
        item: _ChevronItem,
        cx: float,
        cy: float,
        h: float,
    ) -> None:
        """Render primary title and optional description text within the chevron."""
        has_desc = bool(item.description.strip())

        t_style = item.text_style
        if t_style.text_halign is None or t_style.text_valign is None:
            t_style = t_style.patch(
                text_halign=t_style.text_halign or "center",
                text_valign=t_style.text_valign or "center",
            )

        if has_desc:
            title_y = cy + h * 0.16
            desc_y = cy - h * 0.18

            d_style = item.description_style
            if d_style.text_halign is None or d_style.text_valign is None:
                d_style = d_style.patch(
                    text_halign=d_style.text_halign or "center",
                    text_valign=d_style.text_valign or "center",
                )

            canvas_text(xy=(cx, title_y), text=item.text, style=t_style)
            canvas_text(xy=(cx, desc_y), text=item.description, style=d_style)
        else:
            canvas_text(xy=(cx, cy), text=item.text, style=t_style)
