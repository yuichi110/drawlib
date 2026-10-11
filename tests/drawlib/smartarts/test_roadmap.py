# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for drawlib.smartarts (Roadmap)."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest
from pydantic import ValidationError

from drawlib import canvas
from drawlib.icons import phosphor
from drawlib.smartarts import Roadmap, RoadmapItem
from drawlib.styles import Styles


class TestRoadmapUnit:
    """Unit tests for Roadmap configuration, validation, and item mutation."""

    def test_default_initialization(self) -> None:
        """Verify Roadmap explicit style initialization values."""
        rm = Roadmap(
            style=Styles.Neutral,
            text_style=Styles.DarkBold,
            spine_style=Styles.MutedBold,
            badge_style=Styles.SecondaryFlat,
            badge_text_style=Styles.WhiteBold,
        )
        assert rm._direction == "vertical"
        assert rm._curve_bend == 0.0
        assert rm._card_shape == "rounded_rect"
        assert rm._alternating is False
        assert rm._spacing == 2.5
        assert len(rm.items) == 0

    def test_invalid_init_and_add_arguments_raise_error(self) -> None:
        """Verify out-of-range curve_bend, negative spacing, or missing optional styles raise errors."""
        with pytest.raises(ValueError, match="curve_bend"):
            Roadmap(
                style=Styles.Neutral,
                text_style=Styles.DarkBold,
                spine_style=Styles.MutedBold,
                badge_style=Styles.SecondaryFlat,
                badge_text_style=Styles.WhiteBold,
                curve_bend=0.8,
            )

        with pytest.raises(ValueError, match="curve_bend"):
            Roadmap(
                style=Styles.Neutral,
                text_style=Styles.DarkBold,
                spine_style=Styles.MutedBold,
                badge_style=Styles.SecondaryFlat,
                badge_text_style=Styles.WhiteBold,
                curve_bend=-0.6,
            )

        with pytest.raises(ValidationError):
            Roadmap(
                style=Styles.Neutral,
                text_style=Styles.DarkBold,
                spine_style=Styles.MutedBold,
                badge_style=Styles.SecondaryFlat,
                badge_text_style=Styles.WhiteBold,
                spacing=-1.0,
            )

        rm = Roadmap(
            style=Styles.Neutral,
            text_style=Styles.DarkBold,
            spine_style=Styles.MutedBold,
            badge_style=Styles.SecondaryFlat,
            badge_text_style=Styles.WhiteBold,
        )
        with pytest.raises(ValueError, match="description_style"):
            rm.add("Milestone 1", "Needs description_style")

        with pytest.raises(ValueError, match="icon_style"):
            rm.add("Milestone 1", icon=phosphor.flag)

    def test_add_and_mutate_items(self) -> None:
        """Verify adding milestones, default numbering, and mutating RoadmapItem instances."""
        rm = Roadmap(
            style=Styles.Neutral,
            text_style=Styles.DarkBold,
            description_style=Styles.Muted,
            spine_style=Styles.MutedBold,
            badge_style=Styles.SecondaryFlat,
            badge_text_style=Styles.WhiteBold,
        )

        item1 = rm.add("Phase 1", "Initial rollout")
        item2 = rm.add("Phase 2", "Canary testing", badge_text="P2", show=False)
        item3 = rm.add(
            "Phase 3",
            "Global GA",
            style=Styles.PrimaryNeutral,
            badge_style=Styles.PrimaryFlat,
        )

        assert len(rm.items) == 3
        assert isinstance(item1, RoadmapItem)
        assert item1.text == "Phase 1"
        assert item1.description == "Initial rollout"
        assert item1.badge_text == "1"
        assert item1.show is True
        assert item1.badge_style == Styles.SecondaryFlat

        assert item2.badge_text == "P2"
        assert item2.show is False

        assert item3.badge_text == "3"
        assert item3.style == Styles.PrimaryNeutral
        assert item3.badge_style == Styles.PrimaryFlat

        item1.description = "Updated subtitle"
        item1.show = False
        assert rm.items[0].description == "Updated subtitle"
        assert rm.items[0].show is False


class TestRoadmapRendering:
    """Integration tests verifying canvas rendering across Roadmap modes."""

    def test_render_empty_is_noop(self) -> None:
        """Verify drawing an empty Roadmap instance succeeds without errors."""
        canvas.clear()
        rm = Roadmap(
            style=Styles.Neutral,
            text_style=Styles.DarkBold,
            spine_style=Styles.MutedBold,
            badge_style=Styles.SecondaryFlat,
            badge_text_style=Styles.WhiteBold,
        )
        res = rm.draw(xy=(10.0, 10.0), width=80.0, height=50.0)
        assert res is rm

    def test_render_vertical_straight_with_wide_badges(self) -> None:
        """Test rendering vertical straight spine timeline with wide pill badges and icons."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "roadmap_v_straight.png"
            canvas.clear()
            canvas.setup(width=120, height=80)

            rm = Roadmap(
                style=Styles.Neutral,
                text_style=Styles.DarkBold.patch(text_size=10.2),
                description_style=Styles.Muted.patch(text_size=9.5),
                spine_style=Styles.MutedBold,
                badge_style=Styles.SecondaryFlat,
                badge_text_style=Styles.WhiteBold.patch(text_size=9.5),
                icon_style=Styles.Secondary,
                direction="vertical",
                curve_bend=0.0,
                card_shape="rounded_rect",
            )
            rm.add(
                "Alert Triggered",
                "SYN flood hits 300M pps",
                badge_text="T+0m",
                icon=phosphor.warning,
                badge_style=Styles.PrimaryFlat,
                icon_style=Styles.Primary,
            )
            rm.add("BGP Flowspec", "Traffic diverted to scrubbing", badge_text="T+2m", icon=phosphor.shield_check)
            rm.add("SLA Restored", "Origin P99 latency normal", badge_text="T+5m")

            rm.draw(xy=(10.0, 10.0), width=100.0, height=60.0)
            canvas.save(str(out_file))

            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_vertical_curved_pill_agenda(self) -> None:
        """Test rendering vertical curved Bezier spine with pill cards."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "roadmap_v_curved.png"
            canvas.clear()
            canvas.setup(width=120, height=80)

            rm = Roadmap(
                style=Styles.Neutral,
                text_style=Styles.DarkBold.patch(text_size=10.2),
                description_style=Styles.Muted.patch(text_size=9.5),
                spine_style=Styles.MutedBold,
                badge_style=Styles.PrimaryFlat,
                badge_text_style=Styles.WhiteBold.patch(text_size=9.5),
                icon_style=Styles.Primary,
                direction="vertical",
                curve_bend=0.22,
                card_shape="pill",
            )
            rm.add("01. Core Engine", "Vector canvas & themes", badge_text="01", icon=phosphor.cube)
            rm.add("02. AI Agent CLI", "Headless build & grid review", badge_text="02", icon=phosphor.robot)
            rm.add("03. Cloud & GeoMap", "GCP icons & 215 maps", badge_text="03", icon=phosphor.globe_hemisphere_east)

            rm.draw(xy=(10.0, 10.0), width=100.0, height=60.0, scale=0.95)
            canvas.save(str(out_file))

            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_horizontal_alternating_and_visibility(self) -> None:
        """Test rendering horizontal alternating roadmap and toggling item.show."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_all = Path(tmpdir) / "roadmap_h_all.png"
            file_hidden = Path(tmpdir) / "roadmap_h_hidden.png"

            rm = Roadmap(
                style=Styles.Neutral,
                text_style=Styles.DarkBold.patch(text_size=10.2),
                description_style=Styles.Muted.patch(text_size=9.5),
                spine_style=Styles.MutedBold,
                badge_style=Styles.SecondaryFlat,
                badge_text_style=Styles.WhiteBold.patch(text_size=9.5),
                icon_style=Styles.Secondary,
                direction="horizontal",
                alternating=True,
            )
            rm.add("Phase 1", "Scaffold project", badge_text="Q1", icon=phosphor.folder_open)
            rm.add("Phase 2", "Author diagrams", badge_text="Q2", icon=phosphor.code)
            rm.add(
                "Phase 3",
                "Visual review",
                badge_text="Q3",
                icon=phosphor.eye,
                style=Styles.PrimaryNeutral,
                badge_style=Styles.PrimaryFlat,
                icon_style=Styles.Primary,
            )
            item4 = rm.add("Phase 4", "Publish HTML & PDF", badge_text="Q4", icon=phosphor.rocket_launch)

            canvas.clear()
            canvas.setup(width=140, height=70)
            rm.draw(xy=(10.0, 10.0), width=120.0, height=50.0)
            canvas.save(str(file_all))

            item4.show = False
            canvas.clear()
            canvas.setup(width=140, height=70)
            rm.draw(xy=(10.0, 10.0), width=120.0, height=50.0)
            canvas.save(str(file_hidden))

            assert file_all.exists()
            assert file_hidden.exists()
            assert file_all.read_bytes() != file_hidden.read_bytes()
