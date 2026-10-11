# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Panel SmartArt implementation module."""

from __future__ import annotations

from collections.abc import Callable  # noqa: TC003
from typing import Any, Literal, Self

from pydantic import validate_call

from drawlib._core.l2_types import Coordinate, PosFloat
from drawlib._core.l3_colors import BaseColors
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas import circle as canvas_circle
from drawlib._core.l4_canvas import line as canvas_line
from drawlib._core.l4_canvas import rectangle as canvas_rectangle
from drawlib._core.l4_canvas import text as canvas_text
from drawlib._core.l4_canvas import transform
from drawlib._smartarts._common import resolve_card_box_style


def _estimate_text_units(s: str) -> float:
    """Estimate visual character width units accounting for wide CJK glyphs."""
    return sum(1.85 if ord(ch) > 127 else 1.0 for ch in s)


class Panel:
    """SmartArt component for rendering titled container panels with header bands."""

    @validate_call
    def __init__(  # noqa: PLR0913
        self,
        text: str,
        description: str = "",
        *,
        style: Style,
        header_style: Style,
        text_style: Style,
        description_style: Style | None = None,
        icon: Callable[..., Any] | None = None,
        icon_style: Style | None = None,
        dot_styles: tuple[Style, Style, Style] | Style | None = None,
        header_variant: Literal["filled", "underline", "floating", "window"] = "filled",
        header_height: PosFloat = 8.0,
        header_align: Literal["left", "center"] = "left",
        show: bool = True,
    ) -> None:
        """Initialize Panel with explicit styles for all displayed elements.

        Args:
            text: Primary panel header title text.
            description: Optional supporting subtitle or tag displayed on the right side
                of the header. Defaults to "".
            style: Outer panel body background and border style.
            header_style: Style for the header band ("filled", "window"), divider line
                ("underline"), or floating pill badge ("floating").
            text_style: Text style for the primary header title (`text`).
            description_style: Text style for `description` (required when `description`
                is non-empty).
            icon: Optional icon drawing callable displayed in the header.
            icon_style: Style passed to `icon` (required when `icon` is provided).
            dot_styles: Single `Style` or 3-tuple of `Style` instances for the three window
                control dots (required when `header_variant="window"`).
            header_variant: Visual layout mode of the panel header ("filled", "underline",
                "floating", or "window"). Defaults to "filled".
            header_height: Height of the header band or floating pill in canvas units.
                Defaults to 8.0.
            header_align: Horizontal alignment of the primary header title ("left" or "center")
                for "filled", "underline", and "window" variants. Defaults to "left".
            show: Whether to render this panel when `draw()` is called. Defaults to True.

        Raises:
            ValueError: If a displayed element (`description`, `icon`, or window dots) is
                configured without its corresponding `Style`.
        """
        self.text: str = text
        self.description: str = description
        self.style: Style = style
        self.header_style: Style = header_style
        self.text_style: Style = text_style
        self.description_style: Style | None = description_style
        self.icon: Callable[..., Any] | None = icon
        self.icon_style: Style | None = icon_style
        self.dot_styles: tuple[Style, Style, Style] | Style | None = dot_styles
        self.header_variant: Literal["filled", "underline", "floating", "window"] = header_variant
        self.header_height: float = float(header_height)
        self.header_align: Literal["left", "center"] = header_align
        self.show: bool = show

        self._validate_styles()

    def _validate_styles(self) -> None:
        """Verify that every displayed element has an explicit Style configured."""
        if self.style is None or self.header_style is None or self.text_style is None:
            raise ValueError("'style', 'header_style', and 'text_style' are required for Panel.")
        if bool(self.description and self.description.strip()) and self.description_style is None:
            raise ValueError(
                f"'description_style' must be provided when 'description' is non-empty for panel '{self.text}'."
            )
        if self.icon is not None and self.icon_style is None:
            raise ValueError(
                f"'icon_style' must be provided when 'icon' is specified for panel '{self.text}'."
            )
        if self.header_variant == "window" and self.dot_styles is None:
            raise ValueError(
                f"'dot_styles' must be provided when header_variant='window' for panel '{self.text}'."
            )

    @validate_call
    def get_content_box(  # noqa: PLR0913
        self,
        xy: Coordinate,
        width: PosFloat = 100.0,
        height: PosFloat = 60.0,
        *,
        padding: PosFloat | tuple[PosFloat, PosFloat] = (4.0, 3.0),
        align: Literal["bottom_left", "center"] = "bottom_left",
        content_align: Literal["bottom_left", "center"] | None = None,
        scale: PosFloat = 1.0,
    ) -> tuple[tuple[float, float], float, float]:
        """Calculate the inner drawable bounding box `(inner_xy, inner_width, inner_height)`.

        Args:
            xy: Anchor coordinate (x, y) of the outer panel (`"bottom_left"` or `"center"`).
            width: Total width of the outer panel. Defaults to 100.0.
            height: Total height of the outer panel. Defaults to 60.0.
            padding: Inner horizontal and vertical padding as a single float or `(pad_x, pad_y)`
                tuple. Defaults to `(4.0, 3.0)`.
            align: Anchor alignment of input `xy` ("bottom_left" or "center").
                Defaults to "bottom_left".
            content_align: Anchor alignment of returned `inner_xy` ("bottom_left" or "center").
                When None, defaults to `align`.
            scale: Proportional scale factor around `xy`. Defaults to 1.0.

        Returns:
            tuple[tuple[float, float], float, float]: A tuple `(inner_xy, inner_width, inner_height)`
            representing the anchor coordinate, width, and height of the inner content area.
        """
        w = float(width) * float(scale)
        h = float(height) * float(scale)
        x0 = float(xy[0]) - w / 2.0 if align == "center" else float(xy[0])
        y0 = float(xy[1]) - h / 2.0 if align == "center" else float(xy[1])
        h_height = min(self.header_height * float(scale), h * 0.45)

        if isinstance(padding, tuple):
            pad_x = float(padding[0]) * float(scale)
            pad_y = float(padding[1]) * float(scale)
        else:
            pad_x = float(padding) * float(scale)
            pad_y = float(padding) * float(scale)

        content_x0 = x0 + pad_x
        content_y0 = y0 + pad_y
        content_w = max(1.0, w - pad_x * 2.0)
        content_h = max(1.0, h - h_height - pad_y * 2.0)
        target_align = content_align if content_align is not None else align
        if target_align == "center":
            return (content_x0 + content_w / 2.0, content_y0 + content_h / 2.0), content_w, content_h
        return (content_x0, content_y0), content_w, content_h

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
        """Render the panel container at coordinate `xy`.

        Args:
            xy: Anchor coordinate (x, y) of the panel bounding box.
            width: Total width of the panel. Defaults to 100.0.
            height: Total height of the panel. Defaults to 60.0.
            align: Anchor alignment of `xy` ("bottom_left" or "center").
                Defaults to "bottom_left".
            scale: Proportional scale factor around `xy`. Defaults to 1.0.

        Returns:
            Self: This Panel instance for method chaining.
        """
        self._validate_styles()
        if not self.show:
            return self

        total_w = float(width)
        total_h = float(height)
        x0 = float(xy[0]) - total_w / 2.0 if align == "center" else float(xy[0])
        y0 = float(xy[1]) - total_h / 2.0 if align == "center" else float(xy[1])
        h_height = min(self.header_height, total_h * 0.45)
        body_style = resolve_card_box_style(self.style, total_h, max_r=2.5)
        raw_r = body_style.shape_r
        r: float = (
            float(raw_r[0])
            if isinstance(raw_r, tuple)
            else float(raw_r if raw_r is not None else 2.5)
        )

        with transform(origin=xy, scale=scale):
            if self.header_variant == "filled":
                self._draw_filled(
                    x0=x0, y0=y0, total_w=total_w, total_h=total_h, h_height=h_height, r=r, body_style=body_style
                )
            elif self.header_variant == "underline":
                self._draw_underline(
                    x0=x0, y0=y0, total_w=total_w, total_h=total_h, h_height=h_height, body_style=body_style
                )
            elif self.header_variant == "floating":
                self._draw_floating(
                    x0=x0, y0=y0, total_w=total_w, total_h=total_h, h_height=h_height, body_style=body_style
                )
            elif self.header_variant == "window":
                self._draw_window(
                    x0=x0, y0=y0, total_w=total_w, total_h=total_h, h_height=h_height, r=r, body_style=body_style
                )

        return self

    def _draw_filled(  # noqa: PLR0913
        self,
        *,
        x0: float,
        y0: float,
        total_w: float,
        total_h: float,
        h_height: float,
        r: float,
        body_style: Style,
    ) -> None:
        """Render 'filled' header band variant (rounded top corners, flat bottom join)."""
        cx = x0 + total_w / 2.0
        cy = y0 + total_h / 2.0
        h_cy = y0 + total_h - h_height / 2.0
        div_y = y0 + total_h - h_height

        canvas_rectangle(xy=(cx, cy), width=total_w, height=total_h, style=body_style)
        fill_only = self.header_style.patch(shape_r=(0.0, r, r, 0.0), shape_line_width=0)
        canvas_rectangle(xy=(cx, h_cy), width=total_w, height=h_height, style=fill_only)

        if self.header_style.shape_line_color is not None and self.header_style.shape_line_width:
            self._redraw_frame_border(
                x0=x0,
                cx=cx,
                cy=cy,
                total_w=total_w,
                total_h=total_h,
                div_y=div_y,
                r=r,
                line_color=self.header_style.shape_line_color,
                line_width=self.header_style.shape_line_width,
            )

        self._draw_header_labels(x0=x0, h_cy=h_cy, total_w=total_w, left_offset=4.0)

    def _draw_underline(  # noqa: PLR0913
        self,
        *,
        x0: float,
        y0: float,
        total_w: float,
        total_h: float,
        h_height: float,
        body_style: Style,
    ) -> None:
        """Render 'underline' header variant with a horizontal divider line."""
        cx = x0 + total_w / 2.0
        cy = y0 + total_h / 2.0
        h_cy = y0 + total_h - h_height / 2.0
        div_y = y0 + total_h - h_height
        pad_x = min(4.0, total_w * 0.06)

        canvas_rectangle(xy=(cx, cy), width=total_w, height=total_h, style=body_style)

        line_col = (
            self.header_style.line_color
            or self.header_style.shape_line_color
            or self.header_style.shape_fill_color
        )
        line_w = self.header_style.line_width or self.header_style.shape_line_width or 1.4
        line_st = self.header_style.line_style or self.header_style.shape_line_style or "solid"
        div_style = Style(line_color=line_col, line_width=line_w, line_style=line_st)
        canvas_line(xy1=(x0 + pad_x, div_y), xy2=(x0 + total_w - pad_x, div_y), style=div_style)

        self._draw_header_labels(x0=x0, h_cy=h_cy, total_w=total_w, left_offset=pad_x)

    def _draw_floating(  # noqa: PLR0913
        self,
        *,
        x0: float,
        y0: float,
        total_w: float,
        total_h: float,
        h_height: float,
        body_style: Style,
    ) -> None:
        """Render 'floating' pill badge variant straddling the top border."""
        cx = x0 + total_w / 2.0
        pill_h = h_height
        body_h = total_h - pill_h * 0.45
        body_cy = y0 + body_h / 2.0

        canvas_rectangle(xy=(cx, body_cy), width=total_w, height=body_h, style=body_style)

        raw_sz = self.text_style.text_size
        font_sz: float = float(raw_sz) if isinstance(raw_sz, (int, float)) else 11.0
        char_w = font_sz * 0.142
        pill_w = min(
            total_w - 8.0,
            max(24.0, _estimate_text_units(self.text) * char_w + (10.5 if self.icon else 6.5)),
        )
        pill_cx = cx if self.header_align == "center" else x0 + 4.5 + pill_w / 2.0
        pill_cy = y0 + body_h
        pill_style = self.header_style.patch(shape_r=pill_h / 2.0)
        canvas_rectangle(xy=(pill_cx, pill_cy), width=pill_w, height=pill_h, style=pill_style)

        tx = pill_cx - pill_w / 2.0 + 3.2
        if self.icon is not None and self.icon_style is not None:
            icon_w = min(pill_h * 0.50, 3.6)
            self.icon((tx + icon_w / 2.0, pill_cy), width=icon_w, style=self.icon_style)
            tx += icon_w + 1.8

        canvas_text(
            xy=(tx, pill_cy),
            text=self.text,
            style=self.text_style.patch(halign="left", valign="center"),
        )
        if bool(self.description and self.description.strip()) and self.description_style is not None:
            canvas_text(
                xy=(x0 + total_w - 4.0, pill_cy - pill_h * 0.72),
                text=self.description,
                style=self.description_style.patch(halign="right", valign="center"),
            )

    def _draw_window(  # noqa: PLR0913
        self,
        *,
        x0: float,
        y0: float,
        total_w: float,
        total_h: float,
        h_height: float,
        r: float,
        body_style: Style,
    ) -> None:
        """Render 'window' header variant with 3 left control dots."""
        cx = x0 + total_w / 2.0
        cy = y0 + total_h / 2.0
        h_cy = y0 + total_h - h_height / 2.0
        div_y = y0 + total_h - h_height

        canvas_rectangle(xy=(cx, cy), width=total_w, height=total_h, style=body_style)
        fill_only = self.header_style.patch(shape_r=(0.0, r, r, 0.0), shape_line_width=0)
        canvas_rectangle(xy=(cx, h_cy), width=total_w, height=h_height, style=fill_only)

        border_col = body_style.shape_line_color or self.header_style.shape_line_color
        border_w = body_style.shape_line_width or self.header_style.shape_line_width or 1.0
        if border_col is not None:
            self._redraw_frame_border(
                x0=x0,
                cx=cx,
                cy=cy,
                total_w=total_w,
                total_h=total_h,
                div_y=div_y,
                r=r,
                line_color=border_col,
                line_width=border_w,
            )

        dot_r = min(1.05, h_height * 0.13)
        dots = (
            self.dot_styles
            if isinstance(self.dot_styles, tuple)
            else (self.dot_styles, self.dot_styles, self.dot_styles)
        )
        for idx, d_style in enumerate(dots):
            if d_style is not None:
                canvas_circle(
                    xy=(x0 + 4.2 + idx * (dot_r * 2.8), h_cy),
                    radius=dot_r,
                    style=d_style,
                )

        left_offset = 4.2 + 3 * (dot_r * 2.8) + 1.5
        self._draw_header_labels(x0=x0, h_cy=h_cy, total_w=total_w, left_offset=left_offset)

    def _redraw_frame_border(  # noqa: PLR0913
        self,
        *,
        x0: float,
        cx: float,
        cy: float,
        total_w: float,
        total_h: float,
        div_y: float,
        r: float,
        line_color: Any,  # noqa: ANN401
        line_width: float,
    ) -> None:
        """Draw the horizontal header separator and outer rounded border cleanly."""
        canvas_line(
            xy1=(x0, div_y),
            xy2=(x0 + total_w, div_y),
            style=Style(line_color=line_color, line_width=line_width),
        )
        canvas_rectangle(
            xy=(cx, cy),
            width=total_w,
            height=total_h,
            style=Style(
                shape_fill_color=BaseColors.Transparent,
                shape_line_color=line_color,
                shape_line_width=line_width,
                shape_r=r,
            ),
        )

    def _draw_header_labels(
        self,
        *,
        x0: float,
        h_cy: float,
        total_w: float,
        left_offset: float,
    ) -> None:
        """Draw the header icon, title (`text`), and optional right `description`."""
        tx = x0 + left_offset
        if self.icon is not None and self.icon_style is not None:
            icon_w = min(3.8, self.header_height * 0.48)
            if self.header_align == "center":
                self.icon((tx + icon_w / 2.0, h_cy), width=icon_w, style=self.icon_style)
            else:
                self.icon((tx + icon_w / 2.0, h_cy), width=icon_w, style=self.icon_style)
                tx += icon_w + 2.0

        if self.header_align == "center":
            canvas_text(
                xy=(x0 + total_w / 2.0, h_cy),
                text=self.text,
                style=self.text_style.patch(halign="center", valign="center"),
            )
        else:
            canvas_text(
                xy=(tx, h_cy),
                text=self.text,
                style=self.text_style.patch(halign="left", valign="center"),
            )

        if bool(self.description and self.description.strip()) and self.description_style is not None:
            canvas_text(
                xy=(x0 + total_w - 4.0, h_cy),
                text=self.description,
                style=self.description_style.patch(halign="right", valign="center"),
            )
