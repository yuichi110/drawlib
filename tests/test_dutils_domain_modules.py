# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for public domain utilities in drawlib.math, drawlib.colors, and drawlib.canvas."""

from drawlib._builder.doc_builder.exporter_html import get_default_css
from drawlib.canvas import initialize
from drawlib.colors import Colors, from_grayscale, from_hex, with_alpha
from drawlib.doc_builder import (
    build,
    build_document,
    build_documents,
)
from drawlib.math import get_angle, get_center_and_size, get_distance


class TestDomainUtilities:
    """Test suite for public domain utilities."""

    def test_colors_utilities(self) -> None:
        """Verify colors.from_hex, colors.from_grayscale, and colors.with_alpha."""
        assert from_hex("#FF0000") == (255, 0, 0, 1.0)
        assert abs(from_hex("00FF0080")[3] - 0.5) < 0.01
        assert from_grayscale(0.5, alpha=0.8) == (127, 127, 127, 0.8)
        assert with_alpha(Colors.Red, 0.5) == (255, 0, 0, 0.5)

    def test_math_utilities(self) -> None:
        """Verify math.get_distance, math.get_angle, and math.get_center_and_size."""
        assert get_distance((0, 0), (3, 4)) == 5.0
        assert get_angle((0, 0), (1, 0)) == 0.0
        center, size = get_center_and_size([(0, 0), (10, 20)])
        assert center == (5.0, 10.0)
        assert size == (10.0, 20.0)

    def test_canvas_initialize(self) -> None:
        """Verify canvas.initialize executes clean environment setup without errors."""
        initialize()

    def test_doc_builder_exports(self) -> None:
        """Verify drawlib.doc_builder exports public build functions."""
        assert callable(build)
        assert callable(build_document)
        assert callable(build_documents)

    def test_css_presets(self) -> None:
        """Verify get_default_css loads built-in CSS presets correctly."""
        for preset in ["default", "github", "monochrome", "minimal"]:
            css = get_default_css(preset)
            assert len(css) > 100, f"Preset {preset} should return non-empty CSS content"
