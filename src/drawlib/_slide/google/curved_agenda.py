# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Curved Agenda SmartArt component with Google branding and Native SVG output."""

from __future__ import annotations

import os
import re
from typing import ClassVar

from drawlib._slide.base import BoundingBox, SmartArtComponent
from drawlib._slide.resolver import register_smartart
from drawlib.canvas import clear, save, setup
from drawlib.lines import line_bezier1
from drawlib.shapes import circle, rectangle
from drawlib.styles import Style, Styles
from drawlib.text import text

_GOOGLE_PALETTE = [
    (26, 115, 232),  # Blue (#1a73e8)
    (234, 67, 53),  # Red (#ea4335)
    (24, 128, 56),  # Green (#188038)
    (234, 67, 53),  # Red (#ea4335)
    (251, 188, 4),  # Yellow (#fbbc04)
]


@register_smartart
class CurvedAgenda(SmartArtComponent):
    """Google-style curved roadmap/agenda SmartArt component.

    Draws a curved arc with numbered circle badges and pill containers entirely in
    Drawlib, emitting native SVG `<text>` elements for browser searchability.
    """

    name: ClassVar[str] = "curved_agenda"

    def render(
        self,
        box: BoundingBox,
        content: str,
        output_file: str,
        **kwargs: object,
    ) -> None:
        """Render the curved agenda into an SVG file within the given bounding box.

        Args:
            box: Target bounding box on the 1920x1080 slide stage.
            content: Markdown content containing numbered or bulleted agenda items.
            output_file: Target path to save the generated SVG file.
            **kwargs: Optional configuration parameters:
                accent_bar (bool): Whether to draw the left blue accent bar (default: True).
                colors (list[tuple[int, int, int]]): Custom color sequence for badges.
        """
        items = self._parse_items(content)
        if not items:
            return

        w = box.width / 10.0 if box.width > 200 else box.width
        h = box.height / 10.0 if box.height > 200 else box.height

        clear()
        setup(width=int(round(w)), height=int(round(h)))

        accent_bar = bool(kwargs.get("accent_bar", True))
        if accent_bar:
            bar_color = (26, 115, 232)
            bar_style = Style(shape_fill_color=bar_color, shape_line_color=bar_color, shape_line_width=0.0)
            rectangle((1.0, h / 2.0), width=1.5, height=h * 0.9, style=bar_style)

        # Smooth curved arc line
        p_start = (w * 0.18, h * 0.88)
        p_end = (w * 0.17, h * 0.12)
        p_ctrl = (w * 0.28, h * 0.50)

        arc_style = Style(line_color=(205, 210, 218), line_width=3.5)
        line_bezier1(p_start, p_end, p_ctrl, style=arc_style)

        palette = _GOOGLE_PALETTE
        custom_colors = kwargs.get("colors")
        if isinstance(custom_colors, list) and custom_colors:
            palette = custom_colors

        n = len(items)
        for i, (title_str, sub_str) in enumerate(items):
            t = i / (n - 1) if n > 1 else 0.5
            xi = (1 - t) ** 2 * p_start[0] + 2 * (1 - t) * t * p_ctrl[0] + t**2 * p_end[0]
            yi = (1 - t) ** 2 * p_start[1] + 2 * (1 - t) * t * p_ctrl[1] + t**2 * p_end[1]

            color = palette[i % len(palette)]
            r_badge = min(3.8, h / (n * 3.2))
            badge_style = Style(shape_fill_color=color, shape_line_color=color, shape_line_width=0.0)
            circle((xi, yi), radius=r_badge, style=badge_style, text=str(i + 1), text_style=Styles.WhiteBold)

            # Pill container
            x_pill_start = xi + r_badge + 2.5
            w_pill = min(w - x_pill_start - 3.0, 75.0)
            h_pill = max(6.5, min(r_badge * 2.3, 9.0))
            x_pill_center = x_pill_start + w_pill / 2.0
            pill_style = Style(
                shape_fill_color=(255, 255, 255),
                shape_line_color=(220, 224, 230),
                shape_line_width=1.0,
            )
            rectangle((x_pill_center, yi), width=w_pill, height=h_pill, r=h_pill / 2.0, style=pill_style)

            # Text labels
            x_text = x_pill_start + 4.0
            if sub_str:
                text(
                    (x_text, yi + 1.2),
                    title_str,
                    style=Styles.BlackBold.patch(
                        text_size=12.0,
                        text_halign="left",
                        text_valign="center",
                        text_color=(32, 33, 36),
                    ),
                )
                text(
                    (x_text, yi - 1.4),
                    sub_str,
                    style=Styles.WhiteBold.patch(
                        text_size=9.0,
                        text_halign="left",
                        text_valign="center",
                        text_color=(105, 110, 118),
                    ),
                )
            else:
                text(
                    (x_text, yi),
                    title_str,
                    style=Styles.BlackBold.patch(
                        text_size=12.5,
                        text_halign="left",
                        text_valign="center",
                        text_color=(32, 33, 36),
                    ),
                )

        save(os.path.abspath(output_file), format="svg")
        clear()

    @staticmethod
    def _parse_items(content: str) -> list[tuple[str, str]]:
        """Parse raw markdown content into (title, subtitle) tuples.

        Args:
            content: Raw markdown text with items.

        Returns:
            list[tuple[str, str]]: List of parsed (title, subtitle) tuples.
        """
        results: list[tuple[str, str]] = []
        for raw_line in content.splitlines():
            line_str = raw_line.strip()
            if not line_str:
                continue

            # Strip leading numbers (e.g. "1. ") or bullets ("- ", "* ")
            cleaned = re.sub(r"^(\d+[\.\)]\s*|[-*+]\s+)", "", line_str).strip()
            if not cleaned:
                continue

            # Check for delimiters: Title (Subtitle), Title | Subtitle, Title / Subtitle
            if "(" in cleaned and cleaned.endswith(")"):
                r_idx = cleaned.rfind("(")
                title = cleaned[:r_idx].strip()
                subtitle = cleaned[r_idx + 1 : -1].strip()
            elif "|" in cleaned:
                parts = cleaned.split("|", 1)
                title = parts[0].strip()
                subtitle = parts[1].strip()
            elif "/" in cleaned:
                parts = cleaned.split("/", 1)
                title = parts[0].strip()
                subtitle = parts[1].strip()
            else:
                title = cleaned
                subtitle = ""

            results.append((title, subtitle))
        return results
