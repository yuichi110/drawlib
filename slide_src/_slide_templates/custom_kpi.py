# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Example project-local custom SmartArt component."""

from __future__ import annotations

import os
from typing import ClassVar

from drawlib._slide.base import BoundingBox, SmartArtComponent
from drawlib.canvas import clear, save, setup
from drawlib.shapes import rectangle
from drawlib.styles import Style, Styles
from drawlib.text import text


class CustomKpi(SmartArtComponent):
    """Custom project-specific KPI summary cards."""

    name: ClassVar[str] = "custom_kpi"

    def render(
        self,
        box: BoundingBox,
        content: str,
        output_file: str,
        **kwargs: object,
    ) -> None:
        """Render KPI metrics into an SVG file within the bounding box."""
        w = box.width / 10.0 if box.width > 200 else box.width
        h = box.height / 10.0 if box.height > 200 else box.height

        clear()
        setup(width=int(round(w)), height=int(round(h)))

        lines = [line.strip() for line in content.strip().splitlines() if line.strip()]
        if not lines:
            lines = ["99.99% | System Availability | Tier-1 SLA Guaranteed"]

        n = len(lines)
        accent_colors = [
            (26, 115, 232),   # Google Blue
            (52, 168, 83),    # Google Green
            (234, 67, 53),    # Google Red
            (251, 188, 4),    # Google Yellow
        ]

        card_h = min(22.0, (h - 10.0) / max(n, 1))
        gap = (h - 10.0 - (card_h * n)) / max(n + 1, 1)

        for i, line in enumerate(lines):
            parts = [p.strip() for p in line.split("|")]
            metric = parts[0] if len(parts) > 0 else "N/A"
            label = parts[1] if len(parts) > 1 else ""
            subtext = parts[2] if len(parts) > 2 else ""

            cy = h - 5.0 - gap - (i * (card_h + gap)) - (card_h / 2.0)
            cx = w / 2.0
            card_w = w * 0.92

            # Background card
            card_style = Style(
                shape_fill_color=(248, 249, 250),
                shape_line_color=(220, 225, 235),
                shape_line_width=1.0,
            )
            rectangle((cx, cy), width=card_w, height=card_h, r=3.0, style=card_style)

            # Left accent pill
            accent = accent_colors[i % len(accent_colors)]
            pill_style = Styles.WhiteFlat.patch(
                shape_fill_color=accent,
                shape_line_color=accent,
                shape_line_width=0.0,
            )
            pill_x = cx - (card_w / 2.0) + 1.5
            rectangle((pill_x, cy), width=2.0, height=card_h * 0.7, r=1.0, style=pill_style)

            # Metric number
            text(
                (cx - (card_w / 2.0) + 8.0, cy),
                metric,
                style=Styles.BlackBold.patch(
                    text_size=16.0,
                    text_halign="left",
                    text_valign="center",
                    text_color=accent,
                ),
            )

            # Label
            if label:
                text(
                    (cx - (card_w / 2.0) + 40.0, cy + 3.0),
                    label,
                    style=Styles.BlackBold.patch(
                        text_size=11.0,
                        text_halign="left",
                        text_valign="center",
                        text_color=(32, 33, 36),
                    ),
                )

            # Subtext
            if subtext:
                text(
                    (cx - (card_w / 2.0) + 40.0, cy - 3.5),
                    subtext,
                    style=Styles.BlackBold.patch(
                        text_size=8.5,
                        text_halign="left",
                        text_valign="center",
                        text_color=(95, 99, 104),
                    ),
                )

        save(os.path.abspath(output_file), format="svg")
        clear()
