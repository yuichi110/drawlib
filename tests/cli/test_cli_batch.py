# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

# ruff: noqa: S404, S603

"""Integration tests using subprocess to verify drawlib CLI batch command."""

import os
import subprocess
import sys


def run_drawlib_cli(args: list[str], cwd: str) -> subprocess.CompletedProcess[str]:
    """Helper to execute drawlib CLI command via subprocess with current PYTHONPATH.

    Args:
        args (list[str]): Command line arguments for drawlib.
        cwd (str): Working directory for subprocess.

    Returns:
        subprocess.CompletedProcess[str]: Result of subprocess execution.
    """
    env = os.environ.copy()
    src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src"))
    env["PYTHONPATH"] = src_dir + os.pathsep + env.get("PYTHONPATH", "")

    cmd = [sys.executable, "-m", "drawlib"] + args
    return subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, check=False)


def test_cli_batch_single_file(tmp_path) -> None:
    """Test batch command executing a single Python file."""
    script = tmp_path / "test_img.py"
    script.write_text(
        """from drawlib.canvas import config, save
from drawlib.shapes import circle

config(width=100, height=100)
circle((50, 50), radius=20)
save()
""",
        encoding="utf-8",
    )

    res = run_drawlib_cli(["batch", str(script)], cwd=str(tmp_path))
    assert res.returncode == 0
    assert "Successfully executed batch drawing" in res.stdout
    assert (tmp_path / "test_img.png").exists()


def test_cli_batch_directory_package(tmp_path) -> None:
    """Test batch command executing a directory structured as a Python package."""
    pkg_dir = tmp_path / "pkg"
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text("", encoding="utf-8")
    (pkg_dir / "img1.py").write_text(
        """from drawlib.canvas import config, save
from drawlib.shapes import circle

config(width=100, height=100)
circle((25, 25), radius=10)
save()
""",
        encoding="utf-8",
    )
    (pkg_dir / "img2.py").write_text(
        """from drawlib.canvas import config, save
from drawlib.shapes import circle

config(width=100, height=100)
circle((75, 75), radius=10)
save()
""",
        encoding="utf-8",
    )

    res = run_drawlib_cli(["batch", str(pkg_dir)], cwd=str(tmp_path))
    assert res.returncode == 0
    assert (pkg_dir / "img1.png").exists()
    assert (pkg_dir / "img2.png").exists()


def test_cli_batch_directory_standalone(tmp_path) -> None:
    """Test batch command executing a directory without __init__.py."""
    dir_path = tmp_path / "standalone"
    dir_path.mkdir()
    (dir_path / "stand1.py").write_text(
        """from drawlib.canvas import config, save
from drawlib.shapes import circle

config(width=100, height=100)
circle((50, 50), radius=15)
save()
""",
        encoding="utf-8",
    )

    res = run_drawlib_cli(["batch", str(dir_path)], cwd=str(tmp_path))
    assert res.returncode == 0
    assert (dir_path / "stand1.png").exists()


def test_cli_batch_with_output_dir(tmp_path) -> None:
    """Test batch command with -o/--output-dir redirecting saved images."""
    scripts_dir = tmp_path / "scripts"
    out_dir = tmp_path / "output_images"
    scripts_dir.mkdir()
    out_dir.mkdir()

    (scripts_dir / "img_out.py").write_text(
        """from drawlib.canvas import config, save
from drawlib.shapes import circle

config(width=100, height=100)
circle((50, 50), radius=20)
save()
""",
        encoding="utf-8",
    )

    res = run_drawlib_cli(["batch", str(scripts_dir), "-o", str(out_dir)], cwd=str(tmp_path))
    assert res.returncode == 0
    assert (out_dir / "img_out.png").exists()
    assert not (scripts_dir / "img_out.png").exists()


def test_cli_batch_with_config(tmp_path) -> None:
    """Test batch command with --config script applied before drawing."""
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()
    cfg_file = tmp_path / "custom_config.py"
    cfg_file.write_text(
        """from drawlib.canvas import config
config(width=200, height=100)
""",
        encoding="utf-8",
    )

    (scripts_dir / "img_cfg.py").write_text(
        """from drawlib.canvas import save
from drawlib.shapes import circle

circle((100, 50), radius=20)
save()
""",
        encoding="utf-8",
    )

    res = run_drawlib_cli(
        ["batch", str(scripts_dir), "--config", str(cfg_file)],
        cwd=str(tmp_path),
    )
    assert res.returncode == 0
    assert (scripts_dir / "img_cfg.png").exists()


def test_cli_batch_single_file_with_grid(tmp_path) -> None:
    """Test batch command executing a single Python file with --grid option."""
    script = tmp_path / "test_batch_grid.py"
    script.write_text(
        """from drawlib.canvas import config, save
from drawlib.shapes import circle

config(width=100, height=100)
circle((50, 50), radius=20)
save()
""",
        encoding="utf-8",
    )

    res = run_drawlib_cli(["batch", str(script), "--grid"], cwd=str(tmp_path))
    assert res.returncode == 0
    assert "Successfully executed batch drawing" in res.stdout
    assert (tmp_path / "test_batch_grid.png").exists()
    assert (tmp_path / "test_batch_grid_grid.png").exists()


def test_cli_batch_single_file_with_grid_short(tmp_path) -> None:
    """Test batch command executing a single Python file with -g shorthand."""
    script = tmp_path / "test_batch_g.py"
    script.write_text(
        """from drawlib.canvas import config, save
from drawlib.shapes import circle

config(width=100, height=100)
circle((50, 50), radius=20)
save()
""",
        encoding="utf-8",
    )

    res = run_drawlib_cli(["batch", str(script), "-g"], cwd=str(tmp_path))
    assert res.returncode == 0
    assert "Successfully executed batch drawing" in res.stdout
    assert (tmp_path / "test_batch_g.png").exists()
    assert (tmp_path / "test_batch_g_grid.png").exists()


def test_cli_batch_directory_with_grid(tmp_path) -> None:
    """Test batch command executing a directory with --grid option."""
    pkg_dir = tmp_path / "pkg_grid"
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text("", encoding="utf-8")
    (pkg_dir / "img1.py").write_text(
        """from drawlib.canvas import config, save
from drawlib.shapes import circle

config(width=100, height=100)
circle((25, 25), radius=10)
save()
""",
        encoding="utf-8",
    )

    res = run_drawlib_cli(["batch", str(pkg_dir), "--grid"], cwd=str(tmp_path))
    assert res.returncode == 0
    assert (pkg_dir / "img1.png").exists()
    assert (pkg_dir / "img1_grid.png").exists()


def test_cli_legacy_with_grid(tmp_path) -> None:
    """Test legacy command execution with --grid option."""
    script = tmp_path / "test_legacy_grid.py"
    script.write_text(
        """from drawlib.canvas import config, save
from drawlib.shapes import circle

config(width=100, height=100)
circle((50, 50), radius=20)
save()
""",
        encoding="utf-8",
    )

    res = run_drawlib_cli([str(script), "--grid"], cwd=str(tmp_path))
    assert res.returncode == 0
    assert (tmp_path / "test_legacy_grid.png").exists()
    assert (tmp_path / "test_legacy_grid_grid.png").exists()
