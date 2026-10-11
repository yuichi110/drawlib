# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for drawlib.smartarts (KpiCards / KpiCard)."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest
from pydantic import ValidationError

from drawlib import canvas
from drawlib.icons import phosphor
from drawlib.smartarts import KpiCard, KpiCardItem, KpiCards
from drawlib.styles import Styles


class TestKpiCardsUnit:
    """Unit tests for KpiCards configuration, validation, and item mutation."""

    def test_alias_and_default_initialization(self) -> None:
        """Verify KpiCard alias and default configuration values."""
        assert KpiCard is KpiCards

        kpi = KpiCards()
        assert kpi._accent_position == "left_pill"
        assert kpi._metric_layout == "left_column"
        assert kpi._metric_width_ratio == 0.28
        assert kpi._spacing == 3.0
        assert len(kpi.items) == 0

    def test_invalid_init_arguments_raise_error(self) -> None:
        """Verify out-of-range parameters raise ValueError or ValidationError."""
        with pytest.raises(ValueError, match="metric_width_ratio"):
            KpiCards(metric_width_ratio=0.05)

        with pytest.raises(ValueError, match="metric_width_ratio"):
            KpiCards(metric_width_ratio=0.85)

        with pytest.raises(ValueError, match="spacing"):
            KpiCards(spacing=-1.0)

        with pytest.raises(ValueError, match="accent_palette"):
            KpiCards(accent_palette=[])

        with pytest.raises(ValidationError):
            KpiCards(accent_position="invalid")  # ty: ignore[invalid-argument-type]

        with pytest.raises(ValidationError):
            KpiCards(metric_layout="invalid")  # ty: ignore[invalid-argument-type]

    def test_add_and_mutate_items(self) -> None:
        """Verify adding items, palette cycling, and mutating returned KpiCardItem instances."""
        palette = [(200, 10, 20), (10, 180, 90)]
        kpi = KpiCards(accent_palette=palette)

        item1 = kpi.add("99.99%", "High Availability", "Multi-region active-active")
        item2 = kpi.add("< 15ms", "Edge Latency", "Global Anycast POPs", show=False)
        item3 = kpi.add("Zero-Dep", "Lightweight Core", style=Styles.PrimaryNeutral)

        assert len(kpi.items) == 3
        assert isinstance(item1, KpiCardItem)
        assert item1.metric == "99.99%"
        assert item1.title == "High Availability"
        assert item1.description == "Multi-region active-active"
        assert item1.show is True
        assert item1.accent_style is not None
        assert item1.accent_style.shape_fill_color == (200, 10, 20)
        assert item1.metric_style.text_color == (200, 10, 20)

        # Second item uses second palette color; third item wraps around to first
        assert item2.show is False
        assert item2.accent_style is not None
        assert item2.accent_style.shape_fill_color == (10, 180, 90)
        assert item3.accent_style is not None
        assert item3.accent_style.shape_fill_color == (200, 10, 20)
        assert item3.style == Styles.PrimaryNeutral

        # Mutate returned item
        item1.metric = "99.999%"
        item1.show = False
        assert kpi.items[0].metric == "99.999%"
        assert kpi.items[0].show is False


class TestKpiCardsRendering:
    """Integration tests verifying canvas rendering across KpiCards layout modes."""

    def test_render_empty_is_noop(self) -> None:
        """Verify drawing an empty KpiCards instance succeeds without errors."""
        canvas.clear()
        kpi = KpiCards()
        res = kpi.draw(xy=(10.0, 10.0), width=80.0, height=50.0)
        assert res is kpi

    def test_render_vertical_left_column(self) -> None:
        """Test rendering vertical stack with left_column layout and icons."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "kpi_vertical.png"
            canvas.clear()
            canvas.setup(width=120, height=80)

            kpi = KpiCards(
                accent_position="left_pill",
                metric_layout="left_column",
                spacing=3.0,
            )
            kpi.add(
                "99.99%",
                "High Availability SLA",
                "Multi-region active-active failover",
                icon=phosphor.shield_check,
            )
            kpi.add(
                "< 12ms",
                "Edge P99 Latency",
                "Global CDN & Anycast routing",
            )
            kpi.add(
                "Zero-Dep",
                "Pure Python Core",
            )

            kpi.draw(xy=(10.0, 10.0), width=100.0, height=60.0, columns=1)
            canvas.save(str(out_file))

            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_grid_top_stack_and_visibility(self) -> None:
        """Test rendering 2x2 grid with top_stack layout, top_bar accent, and item.show toggle."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_all = Path(tmpdir) / "kpi_grid_all.png"
            file_hidden = Path(tmpdir) / "kpi_grid_hidden.png"

            kpi = KpiCards(
                accent_position="top_bar",
                metric_layout="top_stack",
                spacing=3.0,
            )
            kpi.add("300M+", "Peak RPS", "Botnet flood volume", icon=phosphor.lightning)
            kpi.add("$6,750", "Hourly Cost", "L7 EDoS billing spike")
            kpi.add("4.2 sec", "Auto Mitigation", "BGP Flowspec trigger")
            item4 = kpi.add("100%", "Traffic Scrubbed")

            canvas.clear()
            canvas.setup(width=120, height=80)
            kpi.draw(xy=(10.0, 10.0), width=100.0, height=60.0, columns=2, scale=0.95)
            canvas.save(str(file_all))

            item4.show = False
            canvas.clear()
            canvas.setup(width=120, height=80)
            kpi.draw(xy=(10.0, 10.0), width=100.0, height=60.0, columns=2, scale=0.95)
            canvas.save(str(file_hidden))

            assert file_all.exists()
            assert file_hidden.exists()
            assert file_all.read_bytes() != file_hidden.read_bytes()
