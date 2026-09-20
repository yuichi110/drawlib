# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for bubblespeech smart art."""

from drawlib.canvas import clear, save
from drawlib.colors import Colors
from drawlib.smartarts import dsart
from drawlib.types import Style

OUTPUT_DIR = "../../output_tests/l7_smartarts/bubblespeech/"


class TestBubblespeech:
    """Tests for the bubblespeech drawing function."""

    def test_tail_left(self) -> None:
        """Verify bubblespeech tail rendered on the left edge."""
        clear()
        dsart.bubblespeech(
            xy=(30, 30),
            width=50,
            height=40,
            tail_edge="left",
            tail_start_ratio=0.2,
            tail_vertex_xy=(10, 50),
            tail_end_ratio=0.6,
        )
        save(f"{OUTPUT_DIR}test_tail_left.png")

    def test_tail_top(self) -> None:
        """Verify bubblespeech tail rendered on the top edge."""
        clear()
        dsart.bubblespeech(
            xy=(30, 30),
            width=50,
            height=40,
            tail_edge="top",
            tail_start_ratio=0.2,
            tail_vertex_xy=(50, 90),
            tail_end_ratio=0.6,
        )
        save(f"{OUTPUT_DIR}test_tail_top.png")

    def test_tail_right(self) -> None:
        """Verify bubblespeech tail rendered on the right edge."""
        clear()
        dsart.bubblespeech(
            xy=(30, 30),
            width=50,
            height=40,
            tail_edge="right",
            tail_start_ratio=0.2,
            tail_vertex_xy=(95, 50),
            tail_end_ratio=0.6,
        )
        save(f"{OUTPUT_DIR}test_tail_right.png")

    def test_tail_bottom(self) -> None:
        """Verify bubblespeech tail rendered on the bottom edge."""
        clear()
        dsart.bubblespeech(
            xy=(30, 30),
            width=50,
            height=40,
            tail_edge="bottom",
            tail_start_ratio=0.2,
            tail_vertex_xy=(50, 10),
            tail_end_ratio=0.6,
        )
        save(f"{OUTPUT_DIR}test_tail_bottom.png")

    def test_with_text_and_style(self) -> None:
        """Verify bubblespeech drawing with formatted text and custom Style."""
        clear()
        dsart.bubblespeech(
            xy=(30, 30),
            width=50,
            height=40,
            tail_edge="left",
            tail_start_ratio=0.2,
            tail_vertex_xy=(10, 50),
            tail_end_ratio=0.6,
            text="Hello Drawlib\nHello Python World!!",
            textstyle=Style(text_color=Colors.Red, text_size=28),
        )
        save(f"{OUTPUT_DIR}test_with_text_style.png")
