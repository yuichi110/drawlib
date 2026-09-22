# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for drawlib.charts (GanttChart)."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from drawlib import canvas
from drawlib._charts.gantt_chart._renderer import _resolve_point_time, _resolve_time
from drawlib._core.l3_styles import Style
from drawlib.charts import (
    GanttChart,
    GanttDependency,
    GanttMarker,
    GanttMilestone,
    GanttSection,
    GanttTask,
)


class TestGanttItems:
    """Unit tests for GanttChart item models."""

    def test_task_initialization(self) -> None:
        """Test default and clamped attributes of GanttTask."""
        t1 = GanttTask("Task A", start="Apr", end="May", progress=0.6)
        assert t1.name == "Task A"
        assert t1.start == "Apr"
        assert t1.end == "May"
        assert t1.progress == 0.6
        assert t1.color is None
        assert t1.style is None
        assert t1.show_progress_text is True

        t2 = GanttTask("Task B", start=0.0, end=2.0, progress=1.5)
        assert t2.progress == 1.0  # Clamped

        t3 = GanttTask("Task C", start=0.0, end=1.0, progress=-0.5)
        assert t3.progress == 0.0  # Clamped

    def test_section_initialization(self) -> None:
        """Test attributes of GanttSection."""
        s = GanttSection("Phase 1: Planning")
        assert s.name == "Phase 1: Planning"
        assert s.style is None

    def test_milestone_initialization(self) -> None:
        """Test attributes of GanttMilestone."""
        m = GanttMilestone("Launch", at="Jun", color=(255, 200, 0))
        assert m.name == "Launch"
        assert m.at == "Jun"
        assert m.color == (255, 200, 0)

    def test_marker_and_dependency(self) -> None:
        """Test attributes of GanttMarker and GanttDependency."""
        t1 = GanttTask("T1", "W1", "W2")
        t2 = GanttTask("T2", "W2", "W3")
        dep = GanttDependency(from_task=t1, to_task=t2, color=(100, 100, 100))
        assert dep.from_task is t1
        assert dep.to_task is t2
        assert dep.color == (100, 100, 100)

        marker = GanttMarker(at="W2", label="Today")
        assert marker.at == "W2"
        assert marker.label == "Today"


class TestGanttChartConstruction:
    """Unit tests for GanttChart container and sizing."""

    def test_empty_columns_validation(self) -> None:
        """Test that empty columns list raises ValueError."""
        with pytest.raises(ValueError, match="at least 1 column"):
            GanttChart(columns=[])

    def test_add_items(self) -> None:
        """Test registering various items in GanttChart."""
        chart = GanttChart(columns=["Jan", "Feb", "Mar"])
        sec = chart.add_section("Planning")
        t1 = chart.add_task("Spec", start="Jan", end="Feb")
        m1 = chart.add_milestone("Alpha", at="Mar")
        mark = chart.add_marker(at="Feb", label="Now")
        dep = chart.add_dependency(t1, t1)

        assert len(chart.items) == 3
        assert chart.items[0] is sec
        assert chart.items[1] is t1
        assert chart.items[2] is m1
        assert len(chart.markers) == 1
        assert chart.markers[0] is mark
        assert len(chart.dependencies) == 1
        assert chart.dependencies[0] is dep

    def test_get_size_auto_and_custom(self) -> None:
        """Test dimension calculation."""
        c1 = GanttChart(columns=["Q1", "Q2"], width=100.0, row_height=5.0, header_height=6.0)
        c1.add_task("T1", "Q1", "Q2")
        c1.add_task("T2", "Q2", "Q2")
        w1, h1 = c1.get_size()
        assert w1 == 100.0
        assert h1 == 6.0 + 2 * 5.0 + 6.0

        c2 = GanttChart(columns=["Q1"], width=80.0, height=45.0)
        assert c2.get_size() == (80.0, 45.0)


class TestGanttTimeResolution:
    """Unit tests for translating time specifications into numeric coordinates."""

    def test_resolve_time_string(self) -> None:
        """Test string column resolution for start and end."""
        chart = GanttChart(columns=["Sprint 1", "Sprint 2", "Sprint 3"])
        # Start at Sprint 1 is 0.0
        assert _resolve_time(chart, "Sprint 1", is_end=False) == 0.0
        # End at Sprint 1 is 1.0 (covers the whole sprint)
        assert _resolve_time(chart, "Sprint 1", is_end=True) == 1.0
        # End at Sprint 2 is 2.0
        assert _resolve_time(chart, "Sprint 2", is_end=True) == 2.0

    def test_resolve_time_float(self) -> None:
        """Test numerical float time resolution."""
        chart = GanttChart(columns=["Sprint 1", "Sprint 2"])
        assert _resolve_time(chart, 1.5, is_end=False) == 1.5
        assert _resolve_time(chart, 2.3, is_end=True) == 2.3

    def test_resolve_point_time(self) -> None:
        """Test point event (milestone/marker) resolution."""
        chart = GanttChart(columns=["Jan", "Feb", "Mar"])
        # Midpoint of Jan (index 0) is 0.5
        assert _resolve_point_time(chart, "Jan") == 0.5
        # Midpoint of Feb (index 1) is 1.5
        assert _resolve_point_time(chart, "Feb") == 1.5
        # Float is preserved
        assert _resolve_point_time(chart, 1.8) == 1.8

    def test_invalid_column_error(self) -> None:
        """Test error raised when invalid column is specified."""
        chart = GanttChart(columns=["Jan", "Feb"])
        with pytest.raises(ValueError, match="not found in GanttChart columns"):
            _resolve_time(chart, "Unknown")


class TestGanttChartRendering:
    """Integration tests verifying full rendering pipeline on canvas."""

    def test_render_full_gantt_chart(self) -> None:
        """Test rendering complete roadmap with sections, tasks, progress, milestone, marker, and dependencies."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "gantt_full.png"
            canvas.initialize()

            chart = GanttChart(
                columns=["Apr", "May", "Jun", "Jul", "Aug"],
                width=90.0,
                height=55.0,
                title="Engineering Roadmap (2026)",
                header_height=6.0,
            )

            chart.add_section("Planning & Architecture")
            t1 = chart.add_task("Requirements Spec", start="Apr", end=0.75, progress=1.0)
            t2 = chart.add_task("System Architecture", start=1.25, end=1.9, progress=0.7)

            chart.add_section("Implementation & QA")
            t3 = chart.add_task("Frontend UI", start=2.25, end=3.75, progress=0.4)
            chart.add_task("Backend Services", start=2.1, end=3.6, progress=0.5)
            chart.add_task("Integration & QA", start=3.85, end="Aug", progress=0.0)

            chart.add_milestone("Alpha Release", at="Jul")
            chart.add_dependency(t1, t2)
            chart.add_dependency(t2, t3)
            chart.add_marker(at=1.5, label="Current (Mid-May)")

            chart.draw(xy=(5.0, 20.0))

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_custom_styles(self) -> None:
        """Test rendering GanttChart with custom task style and colors."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "gantt_custom.png"
            canvas.initialize()

            chart = GanttChart(
                columns=["W1", "W2", "W3", "W4"],
                width=80.0,
                height=40.0,
                show_zebra=False,
                bar_radius=1.5,
            )
            c_style = Style(line_width=1.5)
            chart.add_task("Design", start="W1", end="W2", color=(100, 180, 240), style=c_style)
            chart.add_task("Build", start="W2", end="W4", progress=0.5, color=(40, 200, 120))
            chart.draw(xy=(10.0, 10.0))

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0

    def test_render_empty_chart(self) -> None:
        """Test rendering GanttChart with no items."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "gantt_empty.png"
            canvas.initialize()

            chart = GanttChart(columns=["S1", "S2"])
            chart.draw(xy=(10.0, 10.0))

            canvas.save(str(out_file))
            assert out_file.exists()
            assert out_file.stat().st_size > 0
