# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Timeline SmartArt component with Native SVG vector output."""

from __future__ import annotations

import os
import re
from typing import ClassVar

from drawlib._slide.base import BoundingBox, SmartArtComponent
from drawlib._slide.resolver import register_smartart
from drawlib.canvas import clear, save, setup
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.styles import Style, Styles
from drawlib.text import text


@register_smartart
class Timeline(SmartArtComponent):
    """Vertical milestone timeline SmartArt component.

    Draws a vertical milestone spine with interactive dates, titles, and descriptions,
    emitted as native SVG with searchable `<text>` elements.
    """

    name: ClassVar[str] = "timeline"

    def render(
        self,
        box: BoundingBox,
        content: str,
        output_file: str,
        **kwargs: object,
    ) -> None:
        """Render the timeline into an SVG file within the given bounding box.

        Args:
            box: Target bounding box on the 1920x1080 slide stage.
            content: Markdown content with milestone lines.
            output_file: Target path to save the generated SVG file.
            **kwargs: Optional configuration parameters.
        """
        items = self._parse_items(content)
        if not items:
            return

        w = box.width / 10.0 if box.width > 200 else box.width
        h = box.height / 10.0 if box.height > 200 else box.height

        clear()
        setup(width=int(round(w)), height=int(round(h)))

        n = len(items)
        x_spine = w * 0.18

        # Draw vertical spine line
        y_top = h * 0.88
        y_bottom = h * 0.12
        spine_style = Style(line_color=(205, 210, 218), line_width=3.0)
        line((x_spine, y_top), (x_spine, y_bottom), style=spine_style)

        for i, (date_tag, title, desc) in enumerate(items):
            t = i / (n - 1) if n > 1 else 0.5
            yi = y_top - t * (y_top - y_bottom)

            # Node circle on spine
            r_dot = 2.8
            dot_style = Style(
                shape_fill_color=(26, 115, 232),
                shape_line_color=(255, 255, 255),
                shape_line_width=1.5,
            )
            circle((x_spine, yi), radius=r_dot, style=dot_style)

            # Date tag (left side of spine)
            if date_tag:
                w_tag = min(x_spine - 3.0, 16.0)
                h_tag = 5.0
                tag_style = Style(
                    shape_fill_color=(240, 244, 250),
                    shape_line_color=(210, 220, 235),
                    shape_line_width=1.0,
                )
                rectangle((x_spine - 2.5 - w_tag / 2.0, yi), width=w_tag, height=h_tag, r=1.5, style=tag_style)
                text(
                    (x_spine - 2.5 - w_tag / 2.0, yi),
                    date_tag,
                    style=Styles.BlackBold.patch(
                        text_size=9.0,
                        text_halign="center",
                        text_valign="center",
                        text_color=(26, 115, 232),
                    ),
                )

            # Title & Description card (right side of spine)
            x_card_start = x_spine + 4.0
            w_card = max(20.0, w - x_card_start - 3.0)
            h_card = max(7.0, min((y_top - y_bottom) / n * 0.75, 12.0))
            card_style = Style(
                shape_fill_color=(255, 255, 255),
                shape_line_color=(225, 230, 238),
                shape_line_width=1.0,
            )
            rectangle(
                (x_card_start + w_card / 2.0, yi),
                width=w_card,
                height=h_card,
                r=2.0,
                style=card_style,
            )

            x_text = x_card_start + 3.0
            if desc:
                text(
                    (x_text, yi + 1.2),
                    title,
                    style=Styles.BlackBold.patch(
                        text_size=11.5,
                        text_halign="left",
                        text_valign="center",
                        text_color=(32, 33, 36),
                    ),
                )
                text(
                    (x_text, yi - 1.4),
                    desc,
                    style=Styles.WhiteBold.patch(
                        text_size=8.5,
                        text_halign="left",
                        text_valign="center",
                        text_color=(95, 99, 104),
                    ),
                )
            else:
                text(
                    (x_text, yi),
                    title,
                    style=Styles.BlackBold.patch(
                        text_size=12.0,
                        text_halign="left",
                        text_valign="center",
                        text_color=(32, 33, 36),
                    ),
                )

        save(os.path.abspath(output_file), format="svg")
        clear()

    @staticmethod
    def _parse_items(content: str) -> list[tuple[str, str, str]]:
        """Parse content into (date_tag, title, description) tuples.

        Args:
            content: Raw markdown text.

        Returns:
            list[tuple[str, str, str]]: List of (date_tag, title, description) tuples.
        """
        results: list[tuple[str, str, str]] = []
        for raw_line in content.splitlines():
            line_str = raw_line.strip()
            if not line_str:
                continue

            cleaned = re.sub(r"^(\d+[\.\)]\s*|[-*+]\s+)", "", line_str).strip()
            if not cleaned:
                continue

            if "|" in cleaned:
                parts = [p.strip() for p in cleaned.split("|")]
                if len(parts) >= 3:
                    results.append((parts[0], parts[1], parts[2]))
                elif len(parts) == 2:
                    results.append((parts[0], parts[1], ""))
                else:
                    results.append(("", parts[0], ""))
            elif ":" in cleaned:
                parts = [p.strip() for p in cleaned.split(":", 1)]
                results.append((parts[0], parts[1], ""))
            else:
                results.append(("", cleaned, ""))
        return results
