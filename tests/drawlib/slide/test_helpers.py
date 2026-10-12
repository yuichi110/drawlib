# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for drawlib.slide stage helpers (draw_page_number, draw_section_header)."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import pytest
from pydantic import ValidationError

from drawlib._slide.base import reset_slide_context, set_slide_context
from drawlib.canvas import clear, save, setup
from drawlib.slide import draw_page_number, draw_section_header
from drawlib.styles import Styles


class TestDrawPageNumber:
    """Test suite for draw_page_number helper."""

    def test_default_page_number(self, tmp_path: Path) -> None:
        """Verify draw_page_number renders default '1 / 1' when outside slide context."""
        out_svg = tmp_path / "page_default.svg"
        draw_page_number()
        save(str(out_svg), format="svg")
        clear()

        svg_text = out_svg.read_text(encoding="utf-8")
        assert "1 / 1" in svg_text

    def test_custom_template_and_style_within_slide_context(self, tmp_path: Path) -> None:
        """Verify draw_page_number formats template using active SlideContext and custom style."""
        out_svg = tmp_path / "page_custom.svg"
        token = set_slide_context(7, 24)
        try:
            draw_page_number(
                width=18,
                height=4,
                template="Page {index} of {total}",
                style=Styles.PrimaryBold.patch(text_size=48.0),
            )
            save(str(out_svg), format="svg")
            clear()
        finally:
            reset_slide_context(token)

        svg_text = out_svg.read_text(encoding="utf-8")
        assert "Page 7 of 24" in svg_text

    def test_auto_setup_false(self, tmp_path: Path) -> None:
        """Verify draw_page_number with auto_setup=False draws onto existing canvas."""
        out_svg = tmp_path / "page_existing_canvas.svg"
        clear()
        setup(width=20, height=5)
        draw_page_number(width=20, height=5, auto_setup=False)
        save(str(out_svg), format="svg")
        clear()

        assert out_svg.is_file()
        assert "1 / 1" in out_svg.read_text(encoding="utf-8")

    def test_invalid_dimensions_raise_validation_error(self) -> None:
        """Verify non-positive dimensions raise ValueError or ValidationError."""
        with pytest.raises(ValueError, match="width and height must be > 0"):
            draw_page_number(width=0, height=3)

        with pytest.raises(ValidationError):
            draw_page_number(width=-1, height=3)


class TestDrawSectionHeader:
    """Test suite for draw_section_header across all 4 variants and options."""

    @pytest.mark.parametrize("variant", ["split", "centered", "banner", "minimal"])
    def test_variants_with_topics_and_progress(
        self,
        tmp_path: Path,
        variant: Literal["split", "centered", "banner", "minimal"],
    ) -> None:
        """Verify all 4 variants render section title, subtitle, topics, and progress dots."""
        out_svg = tmp_path / f"section_{variant}.svg"
        token = set_slide_context(2, 15)
        try:
            draw_section_header(
                2,
                "Architecture & Topology",
                "High-Level Components and Auto-Layout Graphs",
                topics=[
                    "Cloud Architecture Diagrams",
                    ("Sequence & Flow", "Lifelines and decision trees"),
                    "Entity Relationship Models",
                ],
                total_sections=4,
                variant=variant,
            )
            save(str(out_svg), format="svg")
            clear()
        finally:
            reset_slide_context(token)

        svg_text = out_svg.read_text(encoding="utf-8")
        assert "02" in svg_text
        assert "Architecture" in svg_text
        assert "Cloud Architecture Diagrams" in svg_text
        assert "Sequence" in svg_text
        assert "2 / 15" in svg_text

    @pytest.mark.parametrize("variant", ["split", "centered", "banner", "minimal"])
    def test_variants_minimal_args_without_topics(
        self,
        tmp_path: Path,
        variant: Literal["split", "centered", "banner", "minimal"],
    ) -> None:
        """Verify all 4 variants render cleanly when topics and subtitle are omitted."""
        out_svg = tmp_path / f"section_minimal_{variant}.svg"
        draw_section_header(
            1,
            "Introduction",
            variant=variant,
            show_page_number=False,
            show_decorations=False,
        )
        save(str(out_svg), format="svg")
        clear()

        svg_text = out_svg.read_text(encoding="utf-8")
        assert "01" in svg_text
        assert "Introduction" in svg_text
        assert "1 / 1" not in svg_text

    def test_custom_badge_and_style_overrides(self, tmp_path: Path) -> None:
        """Verify custom badge_text, section_label, and Style overrides."""
        out_svg = tmp_path / "section_custom_styles.svg"
        draw_section_header(
            3,
            "Custom Styled Section",
            "Subtitle with custom styles",
            topics=[("Topic A", "Desc A")],
            total_sections=5,
            variant="split",
            section_label="CHAPTER",
            badge_text="Milestone 3",
            auto_setup=True,
            left_panel_style=Styles.PrimaryFlat,
            right_panel_style=Styles.NeutralFlat,
            divider_bar_style=Styles.AccentFlat,
            decoration_style=Styles.WhiteOutlineThin,
            section_label_style=Styles.WhiteBold,
            section_num_style=Styles.WhiteBold,
            active_dot_style=Styles.AccentFlat,
            completed_dot_style=Styles.WhiteFlat,
            upcoming_dot_style=Styles.MutedFlat,
            badge_style=Styles.SecondaryNeutral,
            badge_text_style=Styles.SecondaryBold,
            title_style=Styles.BlackBold,
            subtitle_style=Styles.Muted,
            line_style=Styles.PrimaryOutlineThin,
            topic_card_style=Styles.Neutral,
            topic_text_style=Styles.BlackBold,
            topic_description_style=Styles.Muted,
            topic_badge_style=Styles.AccentFlat,
            topic_badge_text_style=Styles.WhiteBold,
            page_number_style=Styles.Dark,
        )
        save(str(out_svg), format="svg")
        clear()

        svg_text = out_svg.read_text(encoding="utf-8")
        assert "CHAPTER" in svg_text
        assert "Milestone 3" in svg_text
        assert "Custom Styled Section" in svg_text

    def test_validation_errors(self) -> None:
        """Verify invalid section_num, total_sections, or variant raise errors."""
        with pytest.raises(ValueError, match="section_num must be >= 1"):
            draw_section_header(0, "Invalid Section Number")

        with pytest.raises(ValidationError):
            draw_section_header(1, "Negative Total Sections", total_sections=-1)

        with pytest.raises(ValidationError):
            draw_section_header(1, "Invalid Variant", variant="unknown")  # type: ignore
