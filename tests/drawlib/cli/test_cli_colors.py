# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

# ruff: noqa: S404, S603

"""Integration tests for drawlib colors CLI subcommands."""

from pathlib import Path

from tests.drawlib.cli.common import run_drawlib_cli


def test_cli_colors_list(tmp_path: Path) -> None:
    """Test drawlib colors list command displays preset catalogs."""
    res = run_drawlib_cli(["colors", "list"], cwd=str(tmp_path))
    assert res.returncode == 0
    assert "CssColors" in res.stdout
    assert "DefaultColors" in res.stdout
    assert "GoogleColors" in res.stdout
    assert "MonochromeColors" in res.stdout


def test_cli_colors_show_export(tmp_path: Path) -> None:
    """Test drawlib colors show with -o saves image file."""
    out_png = tmp_path / "monochrome.png"
    res = run_drawlib_cli(
        ["colors", "show", "monochrome", "-o", str(out_png)],
        cwd=str(tmp_path),
    )
    assert res.returncode == 0
    assert "Success" in res.stdout
    assert out_png.exists()
    assert out_png.stat().st_size > 1000


def test_cli_colors_show_sort_modes(tmp_path: Path) -> None:
    """Test drawlib colors show with different sort modes and verify -s is rejected."""
    for mode in ["hsv", "name", "raw"]:
        out_png = tmp_path / f"default_{mode}.png"
        res = run_drawlib_cli(
            ["colors", "show", "default", "-o", str(out_png), "--sort", mode],
            cwd=str(tmp_path),
        )
        assert res.returncode == 0
        assert out_png.exists()
        assert out_png.stat().st_size > 1000

    # Verify shorthand -s is rejected
    res_err = run_drawlib_cli(
        ["colors", "show", "default", "-s", "name"],
        cwd=str(tmp_path),
    )
    assert res_err.returncode != 0


def test_cli_colors_show_with_grid(tmp_path: Path) -> None:
    """Test drawlib colors show with --grid option."""
    out_png = tmp_path / "css_grid.png"
    res = run_drawlib_cli(
        ["colors", "show", "css", "-o", str(out_png), "--grid"],
        cwd=str(tmp_path),
    )
    assert res.returncode == 0
    assert out_png.exists()


def test_cli_colors_show_invalid_preset(tmp_path: Path) -> None:
    """Test drawlib colors show with unknown preset exits with code 1."""
    res = run_drawlib_cli(
        ["colors", "show", "invalid_palette_name"],
        cwd=str(tmp_path),
    )
    assert res.returncode != 0
    output = res.stderr + res.stdout
    assert "Unknown color preset" in output


def test_cli_colors_show_no_cache(tmp_path: Path) -> None:
    """Test drawlib colors show with --no-cache bypasses image cache."""
    out_png = tmp_path / "monochrome_no_cache.png"
    res = run_drawlib_cli(
        ["colors", "show", "monochrome", "-o", str(out_png), "--no-cache"],
        cwd=str(tmp_path),
    )
    assert res.returncode == 0
    assert "Success" in res.stdout
    assert out_png.exists()
    assert out_png.stat().st_size > 1000
