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
from drawlib._core.l3_colors import ColorUtil
from drawlib._core.l3_fonts import Font
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
        description: str = "",
        textstyle: Style | None = None,
        description_style: Style | None = None,
    ) -> None:
        self.text = text
        self.style = style
        self.description = description
        self.textstyle = textstyle
        self.description_style = description_style


class ChevronProcess:
    """SmartArt component for sequential chevron (arrowhead block) process diagrams."""

    @validate_call
    def __init__(
        self,
        *,
        corner_angle: Angle90 = 60.0,
        spacing: PosFloat = 1.5,
        flat_left_end: bool = False,
        default_textstyle: Style | None = None,
        default_description_style: Style | None = None,
    ) -> None:
        """Initialize ChevronProcess.

        Args:
            corner_angle: Angle of the arrowhead point in degrees (between 10.0 and 80.0). Defaults to 60.0.
            spacing: Horizontal gap between consecutive chevrons. Defaults to 1.5.
            flat_left_end: Whether the first chevron has a flat vertical left edge instead of an indent.
                Defaults to False.
            default_textstyle: Default style for primary step text (titles).
            default_description_style: Default style for secondary description text.
        """
        self._corner_angle = float(corner_angle)
        self._spacing = float(spacing)
        self._flat_left_end = bool(flat_left_end)
        self._default_textstyle = default_textstyle
        self._default_description_style = default_description_style
        self._items: list[_ChevronItem] = []

    @property
    def items(self) -> list[_ChevronItem]:
        """Return the registered chevron items."""
        return self._items

    @validate_call
    def append(
        self,
        text: str,
        style: Style,
        description: str = "",
        textstyle: Style | None = None,
        description_style: Style | None = None,
    ) -> None:
        """Append a step to the chevron process.

        Args:
            text: Primary step title text.
            style: Mandatory Style for this chevron block.
            description: Optional supporting description text displayed below the title.
            textstyle: Custom Style for the title text.
            description_style: Custom Style for the description text.
        """
        self.insert(
            len(self._items),
            text=text,
            style=style,
            description=description,
            textstyle=textstyle,
            description_style=description_style,
        )

    @validate_call
    def extend(
        self,
        texts: list[str],
        styles: list[Style] | Style,
        descriptions: list[str] | None = None,
    ) -> None:
        """Extend the process with multiple step titles and styles.

        Args:
            texts: List of step title texts.
            styles: A single Style applied to all steps or a list of Styles matching texts length.
            descriptions: Optional list of corresponding descriptions.
        """
        if isinstance(styles, Style):
            style_list = [styles] * len(texts)
        elif len(styles) != len(texts):
            raise ValueError(
                f"Length of 'styles' ({len(styles)}) must match length of 'texts' ({len(texts)})."
            )
        else:
            style_list = list(styles)

        for i, text in enumerate(texts):
            desc = descriptions[i] if descriptions and i < len(descriptions) else ""
            self.append(text=text, style=style_list[i], description=desc)

    @validate_call
    def insert(
        self,
        index: int,
        text: str,
        style: Style,
        description: str = "",
        textstyle: Style | None = None,
        description_style: Style | None = None,
    ) -> None:
        """Insert a step at the specified index.

        Args:
            index: Position index to insert the step.
            text: Primary step title text.
            style: Mandatory Style for this chevron block.
            description: Optional supporting description text.
            textstyle: Custom Style for the title text.
            description_style: Custom Style for the description text.
        """
        if textstyle is None and self._default_textstyle is None:
            raise ValueError(f"Neither 'default_textstyle' nor 'textstyle' was provided for item '{text}'.")

        if bool(description.strip()) and description_style is None and self._default_description_style is None:
            raise ValueError(
                "Neither 'default_description_style' nor 'description_style' was provided "
                f"for description of item '{text}'."
            )

        item = _ChevronItem(
            text=text,
            style=style,
            description=description,
            textstyle=textstyle,
            description_style=description_style,
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
                c_style = item.style
                canvas_chevron(
                    xy=(cx, cy),
                    width=w_item,
                    height=h,
                    corner_angle=self._corner_angle,
                    style=c_style,
                )
                self._draw_item_texts(item, c_style, cx, cy, h)
        else:
            # First item is a flat-backed pentagon, subsequent items are chevrons
            for i, item in enumerate(self._items):
                c_style = item.style
                if i == 0:
                    points = [
                        (x0, y0),
                        (x0, y0 + h),
                        (x0 + w_item, y0 + h),
                        (x0 + w_item + x_indent, cy),
                        (x0 + w_item, y0),
                    ]
                    canvas_polygon(xys=points, style=c_style)
                    cx = x0 + (w_item + x_indent * 0.35) / 2.0
                else:
                    # Align indentation with the previous chevron's tip + spacing
                    cx = x0 + (1.5 + (i - 1)) * w_item + i * self._spacing + 0.5 * x_indent
                    canvas_chevron(
                        xy=(cx, cy),
                        width=w_item,
                        height=h,
                        corner_angle=self._corner_angle,
                        style=c_style,
                    )
                self._draw_item_texts(item, c_style, cx, cy, h)

    def _draw_item_texts(
        self,
        item: _ChevronItem,
        c_style: Style,
        cx: float,
        cy: float,
        h: float,
    ) -> None:
        """Render primary title and optional description text within the chevron."""
        has_desc = bool(item.description.strip())

        fill_color = c_style.shape_fill_color
        fill_alpha = c_style.shape_fill_alpha
        def_title_col = ColorUtil.get_contrast_text_color(fill_color, fill_alpha)
        def_desc_col = ColorUtil.get_contrast_text_color(
            fill_color,
            fill_alpha,
            dark_color=(80, 80, 80, 1.0),
            light_color=(255, 255, 255, 0.9),
        )

        if has_desc:
            title_y = cy + h * 0.16
            desc_y = cy - h * 0.18

            t_style = (
                item.textstyle
                or self._default_textstyle
                or Style(
                    text_size=10.0,
                    text_font=Font.SANSSERIF_BOLD,
                    text_color=def_title_col,
                    text_halign="center",
                    text_valign="center",
                )
            )
            d_style = (
                item.description_style
                or self._default_description_style
                or Style(
                    text_size=8.0,
                    text_font=Font.SANSSERIF_REGULAR,
                    text_color=def_desc_col,
                    text_halign="center",
                    text_valign="center",
                )
            )
            canvas_text(xy=(cx, title_y), text=item.text, style=t_style)
            canvas_text(xy=(cx, desc_y), text=item.description, style=d_style)
        else:
            t_style = (
                item.textstyle
                or self._default_textstyle
                or Style(
                    text_size=10.5,
                    text_font=Font.SANSSERIF_BOLD,
                    text_color=def_title_col,
                    text_halign="center",
                    text_valign="center",
                )
            )
            canvas_text(xy=(cx, cy), text=item.text, style=t_style)
