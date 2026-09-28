# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

# ruff: noqa: S404, S603

"""Integration tests for drawlib styles CLI subcommands."""

from pathlib import Path

from tests.cli.common import run_drawlib_cli


def test_cli_styles_list(tmp_path: Path) -> None:
    """Test drawlib styles list command displays preset catalogs."""
    res = run_drawlib_cli(["styles", "list"], cwd=str(tmp_path))
    assert res.returncode == 0
    assert "DefaultStyles" in res.stdout
    assert "MonochromeStyles" in res.stdout
    assert "GoogleStyles" in res.stdout


def test_cli_styles_show_export(tmp_path: Path) -> None:
    """Test drawlib styles show with -o saves image file."""
    out_png = tmp_path / "monochrome_styles.png"
    res = run_drawlib_cli(
        ["styles", "show", "monochrome", "-o", str(out_png)],
        cwd=str(tmp_path),
    )
    assert res.returncode == 0
    assert "Success" in res.stdout
    assert out_png.exists()
    assert out_png.stat().st_size > 1000


def test_cli_styles_show_color_filter(tmp_path: Path) -> None:
    """Test drawlib styles show with color filter option."""
    out_png = tmp_path / "blue_styles.png"
    res = run_drawlib_cli(
        ["styles", "show", "default", "-c", "blue", "-o", str(out_png)],
        cwd=str(tmp_path),
    )
    assert res.returncode == 0
    assert "Success" in res.stdout
    assert out_png.exists()
    assert out_png.stat().st_size > 1000


def test_cli_styles_show_with_grid(tmp_path: Path) -> None:
    """Test drawlib styles show with --grid option."""
    out_png = tmp_path / "monochrome_grid.png"
    res = run_drawlib_cli(
        ["styles", "show", "monochrome", "-o", str(out_png), "--grid"],
        cwd=str(tmp_path),
    )
    assert res.returncode == 0
    assert out_png.exists()


def test_cli_styles_show_invalid_preset(tmp_path: Path) -> None:
    """Test drawlib styles show with unknown preset exits with code 1."""
    res = run_drawlib_cli(
        ["styles", "show", "invalid_styles_preset"],
        cwd=str(tmp_path),
    )
    assert res.returncode != 0
    output = res.stderr + res.stdout
    assert "Unknown style preset" in output


def test_cli_styles_show_invalid_color_filter(tmp_path: Path) -> None:
    """Test drawlib styles show with unmatched color filter exits with code 1."""
    res = run_drawlib_cli(
        ["styles", "show", "default", "-c", "nonexistent_hue_xyz"],
        cwd=str(tmp_path),
    )
    assert res.returncode != 0
    output = res.stderr + res.stdout
    assert "No base colors match filter" in output
