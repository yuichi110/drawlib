# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for bubblespeech smart art."""

from pathlib import Path

import pytest
from pydantic import ValidationError

from drawlib.canvas import clear, save
from drawlib.smartarts import bubblespeech
from drawlib.styles import Colors, Styles

default_styles = Styles
OUTPUT_DIR = "../../output_tests/l7_smartarts/bubblespeech/"


class TestBubblespeech:
    """Tests for the bubblespeech drawing function."""

    def test_validation_ratio_order(self) -> None:
        """Verify error when tail_start_ratio >= tail_end_ratio."""
        styles = default_styles
        with pytest.raises(ValueError, match="tail_start_ratio must be smaller than tail_end_ratio"):
            bubblespeech(
                xy=(30, 30),
                width=50,
                height=40,
                tail_edge="left",
                tail_start_ratio=0.7,
                tail_vertex_xy=(10, 50),
                tail_end_ratio=0.3,
                style=styles.Primary,
            )

        with pytest.raises(ValueError, match="tail_start_ratio must be smaller than tail_end_ratio"):
            bubblespeech(
                xy=(30, 30),
                width=50,
                height=40,
                tail_edge="left",
                tail_start_ratio=0.5,
                tail_vertex_xy=(10, 50),
                tail_end_ratio=0.5,
                style=styles.Primary,
            )

    def test_validation_ratio_bounds(self) -> None:
        """Verify validation errors when ratio is outside [0.0, 1.0]."""
        styles = default_styles
        with pytest.raises(ValidationError):
            bubblespeech(
                xy=(30, 30),
                width=50,
                height=40,
                tail_edge="left",
                tail_start_ratio=-0.1,  # type: ignore[arg-type]
                tail_vertex_xy=(10, 50),
                tail_end_ratio=0.5,
                style=styles.Primary,
            )

        with pytest.raises(ValidationError):
            bubblespeech(
                xy=(30, 30),
                width=50,
                height=40,
                tail_edge="left",
                tail_start_ratio=0.2,
                tail_vertex_xy=(10, 50),
                tail_end_ratio=1.2,  # type: ignore[arg-type]
                style=styles.Primary,
            )

    def test_tail_left(self) -> None:
        """Verify bubblespeech tail rendered on the left edge."""
        clear()
        styles = default_styles
        bubblespeech(
            xy=(30, 30),
            width=50,
            height=40,
            tail_edge="left",
            tail_start_ratio=0.2,
            tail_vertex_xy=(10, 50),
            tail_end_ratio=0.6,
            style=styles.Primary,
        )
        save(f"{OUTPUT_DIR}test_tail_left.png")

    def test_tail_top(self) -> None:
        """Verify bubblespeech tail rendered on the top edge."""
        clear()
        styles = default_styles
        bubblespeech(
            xy=(30, 30),
            width=50,
            height=40,
            tail_edge="top",
            tail_start_ratio=0.2,
            tail_vertex_xy=(50, 90),
            tail_end_ratio=0.6,
            style=styles.Primary,
        )
        save(f"{OUTPUT_DIR}test_tail_top.png")

    def test_tail_right(self) -> None:
        """Verify bubblespeech tail rendered on the right edge."""
        clear()
        styles = default_styles
        bubblespeech(
            xy=(30, 30),
            width=50,
            height=40,
            tail_edge="right",
            tail_start_ratio=0.2,
            tail_vertex_xy=(95, 50),
            tail_end_ratio=0.6,
            style=styles.Primary,
        )
        save(f"{OUTPUT_DIR}test_tail_right.png")

    def test_tail_bottom(self) -> None:
        """Verify bubblespeech tail rendered on the bottom edge."""
        clear()
        styles = default_styles
        bubblespeech(
            xy=(30, 30),
            width=50,
            height=40,
            tail_edge="bottom",
            tail_start_ratio=0.2,
            tail_vertex_xy=(50, 10),
            tail_end_ratio=0.6,
            style=styles.Primary,
        )
        save(f"{OUTPUT_DIR}test_tail_bottom.png")

    def test_with_text_and_style(self) -> None:
        """Verify bubblespeech drawing with formatted text and custom Style."""
        clear()
        styles = default_styles
        bubblespeech(
            xy=(30, 30),
            width=50,
            height=40,
            tail_edge="left",
            tail_start_ratio=0.2,
            tail_vertex_xy=(10, 50),
            tail_end_ratio=0.6,
            style=styles.Primary,
            text="Hello Drawlib\nHello Python World!!",
            text_style=styles.Primary.patch(text_color=Colors.Red, text_size=28),
        )
        save(f"{OUTPUT_DIR}test_with_text_style.png")
