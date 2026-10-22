# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for drawlib.charts.heatmap (HeatmapChart & HeatmapOverlay)."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from drawlib import canvas
from drawlib.charts.heatmap import HeatmapChart, HeatmapOverlay, OverlayMode
from drawlib.diagrams.class_diagram import ClassDiagram, ClassNode
from drawlib.styles import Styles


class TestHeatmapChartUnit:
    """Unit tests for HeatmapChart container, rows, and cells."""

    def test_initialization_with_styles_list(self) -> None:
        """Test HeatmapChart initialization with a list of Style stops."""
        chart = HeatmapChart(
            styles=[Styles.Neutral, Styles.PrimaryNeutral, Styles.PrimaryFlat],
            x_categories=["Mon", "Tue", "Wed"],
            y_categories=["Morning", "Evening"],
            width=85.0,
            height=50.0,
            title="Activity Matrix",
        )
        assert chart.width == 85.0
        assert chart.height == 50.0
        assert chart.title == "Activity Matrix"
        assert len(chart.styles) == 3
        assert len(chart.color_stops) == 3
        assert chart.get_size() == (85.0, 50.0)

    def test_initialization_with_min_max_style(self) -> None:
        """Test HeatmapChart initialization with min_style and max_style."""
        chart = HeatmapChart(
            min_style=Styles.Neutral,
            max_style=Styles.AccentFlat,
        )
        assert len(chart.styles) == 2

    def test_initialization_requires_two_styles(self) -> None:
        """Test that fewer than 2 styles raises ValueError."""
        with pytest.raises(ValueError, match="requires either 'styles'"):
            HeatmapChart(min_style=Styles.Neutral)

        with pytest.raises(ValueError, match="at least 2 Style objects"):
            HeatmapChart(styles=[Styles.Neutral])

    def test_add_row_and_set_cell(self) -> None:
        """Test adding rows and overriding individual cells by index and category label."""
        chart = HeatmapChart(
            styles=[Styles.Neutral, Styles.PrimaryFlat],
            x_categories=["API", "DB", "Cache"],
        )
        r1 = chart.add_row("Auth", [12.0, 45.0, 5.0])
        r2 = chart.add_row("Billing", [25.0, 88.0, 14.0])

        assert r1.name == "Auth"
        assert r2.values == [25.0, 88.0, 14.0]
        assert chart.y_categories == ["Auth", "Billing"]
        assert len(chart.rows) == 2

        c1 = chart.set_cell("DB", "Billing", 99.5, label="99.5 (Hot)", style=Styles.DangerFlat)
        assert c1.x == 1
        assert c1.y == 1
        assert c1.value == 99.5
        assert c1.label == "99.5 (Hot)"
        assert len(chart.cells) == 1

    def test_set_data_bulk(self) -> None:
        """Test replacing matrix data via set_data()."""
        chart = HeatmapChart(min_style=Styles.Neutral, max_style=Styles.PrimaryFlat)
        chart.set_data(
            [[1.0, 2.0], [3.0, 4.0]],
            x_categories=["C1", "C2"],
            y_categories=["R1", "R2"],
        )
        assert len(chart.rows) == 2
        assert chart.x_categories == ["C1", "C2"]
        assert chart.y_categories == ["R1", "R2"]


class TestHeatmapOverlayUnit:
    """Unit tests for HeatmapOverlay container and spots."""

    def test_overlay_initialization_and_add_spot(self) -> None:
        """Test adding spots via coordinate tuples and ClassNode instances."""
        overlay = HeatmapOverlay(
            styles=[Styles.PrimaryNeutral, Styles.WarningFlat, Styles.DangerFlat],
            default_radius=18.0,
        )
        s1 = overlay.add_spot((30.0, 40.0), value=0.85, label="High Load")
        assert s1.xy == (30.0, 40.0)
        assert s1.value == 0.85
        assert s1.radius == 18.0
        assert s1.label == "High Load"

        # Passing a ClassNode attached to a ClassDiagram
        diag = ClassDiagram(
            node_style=Styles.Neutral,
            edge_style=Styles.Primary,
            edge_text_style=Styles.Primary,
        )
        cls_node = diag.add(ClassNode("PaymentService"), xy=(75.0, 45.0))
        s2 = overlay.add_spot(cls_node, value=0.95, radius=22.0)
        assert s2.xy == (75.0, 45.0)
        assert s2.radius == 22.0
        assert len(overlay.spots) == 2

        bounds = overlay.get_bounds()
        assert bounds[0] < 30.0
        assert bounds[2] > 75.0
        w, h = overlay.get_size()
        assert w > 0.0
        assert h > 0.0


class TestHeatmapRendering:
    """Integration tests verifying canvas rendering of HeatmapChart and HeatmapOverlay."""

    def test_render_matrix_heatmap_with_colorbar_and_legend(self) -> None:
        """Test rendering standard 2D matrix HeatmapChart with colorbar and legend."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "heatmap_matrix.png"
            canvas.clear()
            canvas.setup(width=120, height=85)

            chart = HeatmapChart(
                styles=[Styles.Neutral, Styles.PrimaryNeutral, Styles.PrimaryFlat, Styles.AccentFlat],
                x_categories=["00:00", "04:00", "08:00", "12:00", "16:00", "20:00"],
                axis_line_style=Styles.Primary,
                axis_text_style=Styles.Muted.patch(text_size=9.5),
                value_text_style=Styles.BlackBold.patch(text_size=9.0),
                background_style=Styles.Neutral,
                width=85.0,
                height=52.0,
                title="API Error Rate (%) by Day & Hour",
                title_style=Styles.BlackBold.patch(text_size=13.0),
                value_format="{:.1f}%",
            )
            chart.add_row("Mon", [0.2, 0.1, 1.4, 3.8, 2.9, 0.8])
            chart.add_row("Tue", [0.3, 0.2, 1.8, 4.5, 3.1, 0.9])
            chart.add_row("Wed", [0.1, 0.2, 2.2, 6.4, 4.8, 1.2])
            chart.add_row("Thu", [0.4, 0.3, 1.5, 3.2, 2.4, 0.7])
            chart.add_row("Fri", [0.5, 0.2, 2.9, 8.5, 5.2, 1.9])

            chart.draw(xy=(8.0, 22.0))
            chart.draw_colorbar(
                xy=(25.0, 10.0),
                text_style=Styles.Muted.patch(text_size=9.0),
                length=50.0,
                orientation="horizontal",
                label="Error Rate (%)",
            )
            chart.draw_legend(
                xy=(98.0, 65.0),
                text_style=Styles.Muted.patch(text_size=9.0),
                orientation="vertical",
                num_steps=4,
            )

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_overlay_on_class_diagram_smooth_and_contour(self) -> None:
        """Test rendering HeatmapOverlay (smooth and contour modes) on top of a ClassDiagram."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_smooth = Path(tmpdir) / "class_heatmap_smooth.png"
            out_contour = Path(tmpdir) / "class_heatmap_contour.png"

            modes: list[tuple[OverlayMode, Path]] = [
                ("smooth", out_smooth),
                ("contour", out_contour),
            ]
            for mode, out_file in modes:
                canvas.clear()
                canvas.setup(width=130, height=85)

                diagram = ClassDiagram(
                    node_style=Styles.Neutral,
                    header_style=Styles.PrimaryNeutral,
                    edge_style=Styles.Primary,
                    edge_text_style=Styles.Muted.patch(text_size=9.5),
                    title="Domain Model Complexity & Bug Hotspot Overlay",
                    title_style=Styles.BlackBold.patch(text_size=13.0),
                )
                order_cls = diagram.add(
                    ClassNode("OrderController", width=30.0).add_method("create_order", "req", "Response"),
                    xy=(25.0, 42.0),
                )
                god_cls = diagram.add(
                    ClassNode("LegacyOrderProcessor", width=34.0)
                    .add_attribute("state_flags", "dict")
                    .add_method("process_all", "order", "bool")
                    .add_method("reconcile_ledger", "tx", "void"),
                    xy=(70.0, 42.0),
                )
                repo_cls = diagram.add(
                    ClassNode("OrderRepository", width=28.0).add_method("save", "entity", "void"),
                    xy=(112.0, 42.0),
                )
                diagram.connect(order_cls, god_cls, "dependency", directed=True)
                diagram.connect(god_cls, repo_cls, "association", directed=True)
                diagram.draw(xy=(0.0, 0.0))

                overlay = HeatmapOverlay(
                    styles=[Styles.PrimaryNeutral, Styles.WarningFlat, Styles.DangerFlat],
                    mode=mode,
                    max_alpha=0.55,
                )
                overlay.add_spot(god_cls, value=0.95, radius=22.0, label="Hotspot: 28 Bugs")
                overlay.add_spot(order_cls, value=0.45, radius=16.0)
                overlay.add_spot(repo_cls, value=0.20, radius=14.0)
                overlay.draw(xy=(0.0, 0.0))
                overlay.draw_colorbar(
                    xy=(45.0, 8.0),
                    text_style=Styles.Muted.patch(text_size=9.0),
                    length=40.0,
                    label="Risk Score",
                )

                canvas.save(str(out_file))
                assert out_file.exists()
                assert out_file.stat().st_size > 0

    def test_heatmap_lifecycle_and_partial_rendering(self) -> None:
        """Test show, draw_ratio, draw_direction, top x_labels, and bottom y_origin."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "heatmap_lifecycle.png"
            canvas.clear()
            canvas.setup(width=100, height=75)

            chart = HeatmapChart(
                min_style=Styles.Neutral,
                max_style=Styles.PrimaryFlat,
                x_categories=["Q1", "Q2", "Q3", "Q4"],
                x_label_position="top",
                y_origin="bottom",
                axis_text_style=Styles.Muted.patch(text_size=9.5),
            )
            chart.add_row("Region A", [10.0, 20.0, 30.0, 40.0], draw_ratio=0.6, draw_direction="left_to_right")
            chart.add_row("Region B", [15.0, None, 35.0, 45.0], draw_ratio=0.5, draw_direction="bottom_to_top")
            chart.add_row("Hidden", [50.0, 60.0, 70.0, 80.0], show=False)

            chart.draw(xy=(50.0, 37.5), width=75.0, height=48.0, align="center", scale=0.9)
            assert chart.get_size() == (80.0, 55.0)

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0
