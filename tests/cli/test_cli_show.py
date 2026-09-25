# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

# ruff: noqa: S404, S603

"""Integration tests using subprocess to verify drawlib CLI show command."""

import os
import subprocess
import sys
from pathlib import Path


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
    env["DRAWLIB_SHOW_NO_DISPLAY"] = "1"

    cmd = [sys.executable, "-m", "drawlib"] + args
    return subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, check=False)


def test_cli_show_python_script_default(tmp_path: Path) -> None:
    """Test show command executing a Python script without grid overlay."""
    script = tmp_path / "drawing.py"
    script.write_text(
        """from drawlib.canvas import config, save
from drawlib.preset_styles import get_default_styles
from drawlib.shapes import circle

styles = get_default_styles()
config(width=100, height=100)
circle((50, 50), radius=20, style=styles.primary)
save()
""",
        encoding="utf-8",
    )

    res = run_drawlib_cli(["show", str(script)], cwd=str(tmp_path))
    assert res.returncode == 0
    assert "Executing Python script" in res.stdout
    assert "with grid overlay..." not in res.stdout
    assert "Rendered successfully to temp file:" in res.stdout
    assert "_grid.png" not in res.stdout


def test_cli_show_python_script_with_grid_long(tmp_path: Path) -> None:
    """Test show command executing a Python script with --grid flag."""
    script = tmp_path / "drawing_grid.py"
    script.write_text(
        """from drawlib.canvas import config, save
from drawlib.preset_styles import get_default_styles
from drawlib.shapes import rectangle

styles = get_default_styles()
config(width=100, height=100)
rectangle((50, 50), width=40, height=30, style=styles.primary)
save()
""",
        encoding="utf-8",
    )

    res = run_drawlib_cli(["show", str(script), "--grid"], cwd=str(tmp_path))
    assert res.returncode == 0
    assert "Executing Python script" in res.stdout
    assert "with grid overlay..." in res.stdout
    assert "Rendered successfully to temp file:" in res.stdout
    assert "_grid.png" in res.stdout


def test_cli_show_python_script_with_grid_short(tmp_path: Path) -> None:
    """Test show command executing a Python script with -g flag."""
    script = tmp_path / "drawing_grid_short.py"
    script.write_text(
        """from drawlib.canvas import config, save
from drawlib.preset_styles import get_default_styles
from drawlib.shapes import rectangle

styles = get_default_styles()
config(width=100, height=100)
rectangle((50, 50), width=40, height=30, style=styles.primary)
save()
""",
        encoding="utf-8",
    )

    res = run_drawlib_cli(["show", str(script), "-g"], cwd=str(tmp_path))
    assert res.returncode == 0
    assert "Executing Python script" in res.stdout
    assert "with grid overlay..." in res.stdout
    assert "Rendered successfully to temp file:" in res.stdout
    assert "_grid.png" in res.stdout


def test_cli_show_markdown_list_blocks(tmp_path: Path) -> None:
    """Test show command listing code blocks from a Markdown file."""
    doc = tmp_path / "doc.md"
    doc.write_text(
        """# Sample Document

```drawlib file:first.png
circle((30, 30), radius=10, style=styles.primary)
```

```drawlib file:second.png
rectangle((50, 50), width=20, height=20, style=styles.primary)
```
""",
        encoding="utf-8",
    )

    res = run_drawlib_cli(["show", str(doc)], cwd=str(tmp_path))
    assert res.returncode == 0
    assert "Available drawlib code blocks" in res.stdout
    assert "first.png" in res.stdout
    assert "second.png" in res.stdout


def test_cli_show_markdown_block_by_index(tmp_path: Path) -> None:
    """Test show command executing a specific Markdown block by index without grid."""
    doc = tmp_path / "doc_block.md"
    doc.write_text(
        """# Doc

```drawlib
circle((50, 50), radius=20, style=styles.primary)
```
""",
        encoding="utf-8",
    )

    res = run_drawlib_cli(["show", str(doc), "1"], cwd=str(tmp_path))
    assert res.returncode == 0
    assert "Executing block #1" in res.stdout
    assert "with grid overlay..." not in res.stdout
    assert "Rendered successfully to temp file:" in res.stdout
    assert "_grid.png" not in res.stdout


def test_cli_show_markdown_block_with_grid(tmp_path: Path) -> None:
    """Test show command executing a Markdown block with --grid flag."""
    doc = tmp_path / "doc_grid.md"
    doc.write_text(
        """# Doc

```drawlib
circle((50, 50), radius=20, style=styles.primary)
```
""",
        encoding="utf-8",
    )

    res = run_drawlib_cli(["show", str(doc), "1", "--grid"], cwd=str(tmp_path))
    assert res.returncode == 0
    assert "Executing block #1" in res.stdout
    assert "with grid overlay..." in res.stdout
    assert "Rendered successfully to temp file:" in res.stdout
    assert "_grid.png" in res.stdout


def test_cli_show_nonexistent_file(tmp_path: Path) -> None:
    """Test show command when target file does not exist."""
    res = run_drawlib_cli(["show", str(tmp_path / "missing.py")], cwd=str(tmp_path))
    assert res.returncode != 0
    assert "does not exist" in res.stderr or "does not exist" in res.stdout


def test_cli_show_invalid_block_target(tmp_path: Path) -> None:
    """Test show command when target block index does not exist in Markdown."""
    doc = tmp_path / "doc_empty.md"
    doc.write_text("# No blocks here", encoding="utf-8")

    res = run_drawlib_cli(["show", str(doc), "1"], cwd=str(tmp_path))
    assert res.returncode == 0
    assert "No drawlib code blocks found" in res.stdout
