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

        card_style = Style(
            shape_fill_color=(245, 247, 250),
            shape_line_color=(220, 225, 235),
            shape_line_width=1.5,
        )
        rectangle((w / 2.0, h / 2.0), width=w * 0.9, height=h * 0.8, r=4.0, style=card_style)

        text(
            (w / 2.0, h / 2.0 + 3.0),
            "99.99%",
            style=Styles.BlackBold.patch(
                text_size=20.0,
                text_halign="center",
                text_valign="center",
                text_color=(26, 115, 232),
            ),
        )
        text(
            (w / 2.0, h / 2.0 - 4.0),
            content.strip() or "System Availability",
            style=Styles.BlackBold.patch(
                text_size=11.0,
                text_halign="center",
                text_valign="center",
                text_color=(95, 99, 104),
            ),
        )

        save(os.path.abspath(output_file), format="svg")
        clear()
