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
        """Verify default configuration values of Roadmap."""
        rm = Roadmap()
        assert rm._direction == "vertical"
        assert rm._curve_bend == 0.0
        assert rm._card_shape == "rounded_rect"
        assert rm._alternating is False
        assert len(rm.items) == 0

    def test_invalid_init_arguments_raise_error(self) -> None:
        """Verify out-of-range or invalid parameters raise ValueError or ValidationError."""
        with pytest.raises(ValueError, match="curve_bend"):
            Roadmap(curve_bend=0.8)

        with pytest.raises(ValueError, match="curve_bend"):
            Roadmap(curve_bend=-0.8)

        with pytest.raises(ValueError, match="badge_palette"):
            Roadmap(badge_palette=[])

        with pytest.raises(ValidationError):
            Roadmap(direction="diagonal")  # ty: ignore[invalid-argument-type]

        with pytest.raises(ValidationError):
            Roadmap(card_shape="hexagon")  # ty: ignore[invalid-argument-type]

    def test_add_and_mutate_items(self) -> None:
        """Verify adding items, auto badge numbering, description alias, and item mutation."""
        palette = [(220, 38, 38), (16, 185, 129)]
        rm = Roadmap(badge_palette=palette)

        item1 = rm.add("Anomaly Detected", "SYN/UDP flood alert", badge_text="T+0m")
        item2 = rm.add("Auto-Scrubbing", description="BGP Anycast diversion", show=False)
        item3 = rm.add("Origin Stabilized", "Latency restored", card_style=Styles.PrimaryNeutral)

        assert len(rm.items) == 3
        assert isinstance(item1, RoadmapItem)
        assert item1.title == "Anomaly Detected"
        assert item1.subtitle == "SYN/UDP flood alert"
        assert item1.description == "SYN/UDP flood alert"
        assert item1.badge_text == "T+0m"
        assert item1.badge_style.shape_fill_color == (220, 38, 38)

        # Auto-numbered badge_text ("2") when badge_text is omitted
        assert item2.badge_text == "2"
        assert item2.subtitle == "BGP Anycast diversion"
        assert item2.show is False
        assert item2.badge_style.shape_fill_color == (16, 185, 129)

        assert item3.badge_text == "3"
        assert item3.card_style == Styles.PrimaryNeutral
        assert item3.badge_style.shape_fill_color == (220, 38, 38)

        # Mutate returned item
        item1.description = "Updated description"
        item1.show = False
        assert rm.items[0].subtitle == "Updated description"
        assert rm.items[0].show is False


class TestRoadmapRendering:
    """Integration tests verifying canvas rendering across Roadmap layout modes."""

    def test_render_empty_is_noop(self) -> None:
        """Verify drawing an empty Roadmap instance succeeds without errors."""
        canvas.clear()
        rm = Roadmap()
        res = rm.draw(xy=(10.0, 10.0), width=80.0, height=50.0)
        assert res is rm

    def test_render_vertical_straight(self) -> None:
        """Test rendering vertical straight timeline with wide timestamp badges."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "roadmap_v_straight.png"
            canvas.clear()
            canvas.setup(width=120, height=80)

            rm = Roadmap(direction="vertical", curve_bend=0.0, card_shape="rounded_rect")
            rm.add("Anomaly Detected", "SYN/UDP flood alert triggered at Edge POP", badge_text="T+0m")
            rm.add("Auto-Scrubbing Active", "BGP Anycast diversion & Cloud Armor rules", badge_text="T+3m")
            rm.add("Origin Stabilized", "P99 latency restored to <12ms SLA", badge_text="T+15m")

            rm.draw(xy=(8.0, 8.0), width=104.0, height=64.0)
            canvas.save(str(out_file))

            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_vertical_curved_pill(self) -> None:
        """Test rendering vertical curved arc roadmap with pill cards."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "roadmap_v_curved.png"
            canvas.clear()
            canvas.setup(width=120, height=80)

            rm = Roadmap(direction="vertical", curve_bend=0.14, card_shape="pill")
            rm.add("Phase 1: Core Engine", "Pure-Python vector canvas & styles")
            rm.add("Phase 2: High-Level SmartArts", "KpiCards, CardList, Roadmap, GeoMap")
            rm.add("Phase 3: AI Self-Healing Loop", "Grid inspection & automated doc build")

            rm.draw(xy=(8.0, 8.0), width=104.0, height=64.0)
            canvas.save(str(out_file))

            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_horizontal_alternating_and_visibility(self) -> None:
        """Test rendering horizontal alternating roadmap with icons and item.show toggle."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_all = Path(tmpdir) / "roadmap_h_all.png"
            file_hidden = Path(tmpdir) / "roadmap_h_hidden.png"

            rm = Roadmap(direction="horizontal", alternating=True)
            rm.add("Architecture RFC", "Unified Markdown syntax", badge_text="Q1", icon=phosphor.file_text)
            rm.add("SmartArts v2", "KpiCards & CardList", badge_text="Q2", icon=phosphor.squares_four)
            rm.add("Slide Helpers", "16:9 stage components", badge_text="Q3", icon=phosphor.presentation_chart)
            item4 = rm.add("GA Release", "PyPI & Docker cleanroom", badge_text="Q4", icon=phosphor.rocket_launch)

            canvas.clear()
            canvas.setup(width=170, height=60)
            rm.draw(xy=(6.0, 6.0), width=158.0, height=48.0, scale=0.98)
            canvas.save(str(file_all))

            item4.show = False
            canvas.clear()
            canvas.setup(width=170, height=60)
            rm.draw(xy=(6.0, 6.0), width=158.0, height=48.0, scale=0.98)
            canvas.save(str(file_hidden))

            assert file_all.exists()
            assert file_hidden.exists()
            assert file_all.read_bytes() != file_hidden.read_bytes()
