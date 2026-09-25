# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for GCP icons drawing."""

import pytest

from drawlib._icons.png_icons import gcp as gcp_internal
from drawlib._icons.png_icons.gcp._base import GCP_PROVIDER
from drawlib.canvas import clear, save
from drawlib.colors import Colors
from drawlib.icons import gcp
from drawlib.types import Style

OUTPUT_DIR = "../../output_tests/l6_icons/icon_gcp/"


class TestCanvasGcp:
    """Tests for GCP icons drawing support."""

    def test_gcp_icon_basic_drawing(self) -> None:
        """Verify basic GCP icon drawing."""
        clear()
        gcp.compute_engine(xy=(50, 50), width=20, style=Style())
        save(f"{OUTPUT_DIR}test_basic.png")

    def test_gcp_icon_angle(self) -> None:
        """Verify GCP icon drawing combined with a rotation angle."""
        clear()
        gcp.compute_engine(
            xy=(50, 50),
            width=20,
            angle=45,
            style=Style(),
        )
        save(f"{OUTPUT_DIR}test_angle45.png")

    def test_gcp_icon_styles(self) -> None:
        """Verify GCP icon drawing with style options (alpha, fill tint, border)."""
        clear()
        # Transparent alpha
        gcp.compute_engine(
            xy=(25, 25),
            width=20,
            style=Style(image_alpha=0.4),
        )
        # Silhouette fill color
        gcp.compute_engine(
            xy=(75, 75),
            width=20,
            style=Style(image_tint_color=Colors.Red),
        )
        # Border
        gcp.gke(
            xy=(25, 75),
            width=20,
            style=Style(image_border_color=Colors.Blue, image_border_width=2),
        )
        save(f"{OUTPUT_DIR}test_styles.png")

    def test_gcp_aliases(self) -> None:
        """Verify common short GCP alias functions."""
        clear()
        gcp.gce(xy=(25, 50), width=15, style=Style())
        gcp.gke(xy=(50, 50), width=15, style=Style())
        gcp.gcs(xy=(75, 50), width=15, style=Style())
        save(f"{OUTPUT_DIR}test_aliases.png")

    def test_gcp_flat_import(self) -> None:
        """Verify GCP icon drawing via drawlib.icons.gcp import."""
        clear()
        gcp.compute_engine(xy=(50, 50), width=25, style=Style())
        save(f"{OUTPUT_DIR}test_flat_import.png")
        assert gcp.compute_engine == gcp_internal.compute_engine

    def test_gcp_nonexistent_icon_error(self) -> None:
        """Verify FileNotFoundError when requesting an invalid icon file."""
        with pytest.raises(FileNotFoundError):
            GCP_PROVIDER.get_icon_path("non_existent_icon_xyz")
