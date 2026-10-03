# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Chevron Process SmartArt component for slides with Native SVG output."""

from __future__ import annotations

import os
import re
from typing import ClassVar

from drawlib._slide.base import BoundingBox, SmartArtComponent
from drawlib._slide.resolver import register_smartart
from drawlib._smartarts._chevronprocess import ChevronProcess as CoreChevronProcess
from drawlib.canvas import clear, save, setup
from drawlib.styles import Style, Styles


@register_smartart
class ChevronProcess(SmartArtComponent):
    """Horizontal chevron process pipeline SmartArt component.

    Draws a sequence of interlocking chevron blocks representing stages, phases,
    or workflow pipelines, emitted as native SVG with searchable `<text>` elements.
    """

    name: ClassVar[str] = "chevron_process"

    def render(
        self,
        box: BoundingBox,
        content: str,
        output_file: str,
        **kwargs: object,
    ) -> None:
        """Render the chevron process into an SVG file within the given bounding box.

        Args:
            box: Target bounding box on the 1920x1080 slide stage.
            content: Markdown content with sequential process steps.
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

        palette = [
            Styles.PrimaryFlat,
            Styles.SecondaryFlat,
            Styles.AccentFlat,
            Styles.LightFlat,
        ]

        title_style = Styles.WhiteBold.patch(
            text_size=12.0,
            text_halign="center",
            text_valign="center",
        )
        desc_style = Styles.WhiteBold.patch(
            text_size=9.0,
            text_halign="center",
            text_valign="center",
            text_color=(240, 243, 246),
        )

        cp = CoreChevronProcess(
            style=Styles.PrimaryFlat,
            text_style=title_style,
            description_style=desc_style,
            flat_left_end=True,
            spacing=1.2,
        )

        for i, (title, desc) in enumerate(items):
            block_style = palette[i % len(palette)]
            cp.append(
                text=title,
                description=desc,
                style=block_style,
                text_style=title_style,
                description_style=desc_style,
            )

        margin_x = w * 0.05
        draw_w = w * 0.90
        draw_h = min(h * 0.35, 18.0)
        y0 = (h - draw_h) / 2.0

        cp.draw((margin_x, y0), width=draw_w, height=draw_h)

        save(os.path.abspath(output_file), format="svg")
        clear()

    @staticmethod
    def _parse_items(content: str) -> list[tuple[str, str]]:
        """Parse raw markdown lines into (title, description) tuples.

        Args:
            content: Raw markdown text.

        Returns:
            list[tuple[str, str]]: List of parsed (title, description) tuples.
        """
        results: list[tuple[str, str]] = []
        for raw_line in content.splitlines():
            line_str = raw_line.strip()
            if not line_str:
                continue

            cleaned = re.sub(r"^(\d+[\.\)]\s*|[-*+]\s+)", "", line_str).strip()
            if not cleaned:
                continue

            if "(" in cleaned and cleaned.endswith(")"):
                r_idx = cleaned.rfind("(")
                title = cleaned[:r_idx].strip()
                desc = cleaned[r_idx + 1 : -1].strip()
            elif "|" in cleaned:
                parts = cleaned.split("|", 1)
                title = parts[0].strip()
                desc = parts[1].strip()
            elif "/" in cleaned:
                parts = cleaned.split("/", 1)
                title = parts[0].strip()
                desc = parts[1].strip()
            else:
                title = cleaned
                desc = ""

            results.append((title, desc))
        return results
