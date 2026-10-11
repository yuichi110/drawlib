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
        """Verify KpiCard alias and explicit style configuration values."""
        assert KpiCard is KpiCards

        kpi = KpiCards(
            style=Styles.Neutral,
            metric_style=Styles.PrimaryBold,
            text_style=Styles.DarkBold,
            description_style=Styles.Muted,
            accent_style=Styles.PrimaryFlat,
        )
        assert kpi._accent_position == "left_pill"
        assert kpi._metric_layout == "left_column"
        assert kpi._metric_width_ratio == 0.28
        assert kpi._spacing == 3.0
        assert len(kpi.items) == 0

    def test_invalid_init_and_add_arguments_raise_error(self) -> None:
        """Verify out-of-range or missing required optional styles raise errors."""
        with pytest.raises(ValueError, match="metric_width_ratio"):
            KpiCards(
                style=Styles.Neutral,
                metric_style=Styles.PrimaryBold,
                text_style=Styles.DarkBold,
                metric_width_ratio=0.05,
            )

        with pytest.raises(ValueError, match="metric_width_ratio"):
            KpiCards(
                style=Styles.Neutral,
                metric_style=Styles.PrimaryBold,
                text_style=Styles.DarkBold,
                metric_width_ratio=0.85,
            )

        with pytest.raises(ValidationError):
            KpiCards(
                style=Styles.Neutral,
                metric_style=Styles.PrimaryBold,
                text_style=Styles.DarkBold,
                spacing=-1.0,
            )

        with pytest.raises(ValidationError):
            KpiCards(
                style=Styles.Neutral,
                metric_style=Styles.PrimaryBold,
                text_style=Styles.DarkBold,
                accent_position="invalid",  # ty: ignore[invalid-argument-type]
            )

        # Missing description_style when description is provided
        kpi_no_desc = KpiCards(
            style=Styles.Neutral,
            metric_style=Styles.PrimaryBold,
            text_style=Styles.DarkBold,
            accent_style=Styles.PrimaryFlat,
        )
        with pytest.raises(ValueError, match="description_style"):
            kpi_no_desc.add("99.9%", "Uptime", "Needs description_style")

        # Missing accent_style when accent_position != 'none'
        kpi_no_accent = KpiCards(
            style=Styles.Neutral,
            metric_style=Styles.PrimaryBold,
            text_style=Styles.DarkBold,
            accent_position="left_pill",
        )
        with pytest.raises(ValueError, match="accent_style"):
            kpi_no_accent.add("99.9%", "Uptime")

        # Missing icon_style when icon is provided
        with pytest.raises(ValueError, match="icon_style"):
            kpi_no_desc.add("99.9%", "Uptime", icon=phosphor.shield_check)

    def test_add_and_mutate_items(self) -> None:
        """Verify adding items, per-item style overrides, and mutating returned KpiCardItem instances."""
        kpi = KpiCards(
            style=Styles.Neutral,
            metric_style=Styles.PrimaryBold,
            text_style=Styles.DarkBold,
            description_style=Styles.Muted,
            accent_style=Styles.SecondaryFlat,
        )

        item1 = kpi.add("99.99%", "High Availability", "Multi-region active-active")
        item2 = kpi.add("< 15ms", "Edge Latency", "Global Anycast POPs", show=False)
        item3 = kpi.add(
            "Zero-Dep",
            "Lightweight Core",
            style=Styles.PrimaryNeutral,
            accent_style=Styles.PrimaryFlat,
        )

        assert len(kpi.items) == 3
        assert isinstance(item1, KpiCardItem)
        assert item1.metric == "99.99%"
        assert item1.text == "High Availability"
        assert item1.description == "Multi-region active-active"
        assert item1.show is True
        assert item1.accent_style == Styles.SecondaryFlat

        assert item2.show is False
        assert item3.style == Styles.PrimaryNeutral
        assert item3.accent_style == Styles.PrimaryFlat

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
        kpi = KpiCards(
            style=Styles.Neutral,
            metric_style=Styles.PrimaryBold,
            text_style=Styles.DarkBold,
        )
        res = kpi.draw(xy=(10.0, 10.0), width=80.0, height=50.0)
        assert res is kpi

    def test_render_vertical_left_column(self) -> None:
        """Test rendering vertical stack with left_column layout and icons."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "kpi_vertical.png"
            canvas.clear()
            canvas.setup(width=120, height=80)

            kpi = KpiCards(
                style=Styles.Neutral,
                metric_style=Styles.PrimaryBold.patch(text_size=13.0),
                text_style=Styles.DarkBold.patch(text_size=10.5),
                description_style=Styles.Muted.patch(text_size=9.5),
                accent_style=Styles.PrimaryFlat,
                icon_style=Styles.Primary,
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
                style=Styles.Neutral,
                metric_style=Styles.PrimaryBold.patch(text_size=13.0),
                text_style=Styles.DarkBold.patch(text_size=10.5),
                description_style=Styles.Muted.patch(text_size=9.5),
                accent_style=Styles.SecondaryFlat,
                icon_style=Styles.Primary,
                accent_position="top_bar",
                metric_layout="top_stack",
                spacing=3.0,
            )
            kpi.add("300M+", "Peak RPS", "Botnet flood volume", icon=phosphor.lightning)
            kpi.add("$6,750", "Hourly Cost", "L7 EDoS billing spike")
            kpi.add(
                "4.2 sec",
                "Auto Mitigation",
                "BGP Flowspec trigger",
                style=Styles.PrimaryNeutral,
                accent_style=Styles.PrimaryFlat,
            )
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
