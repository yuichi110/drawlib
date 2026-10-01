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
from pathlib import Path

from tests.cli.common import run_drawlib_cli


def test_cli_show_python_script_default(tmp_path: Path) -> None:
    """Test show command executing a Python script without grid overlay."""
    script = tmp_path / "drawing.py"
    script.write_text(
        """from drawlib.canvas import save, setup
from drawlib.styles import Styles as default_styles
from drawlib.shapes import circle

styles = default_styles
setup(width=100, height=100)
circle((50, 50), radius=20, style=styles.Primary)
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
        """from drawlib.canvas import save, setup
from drawlib.styles import Styles as default_styles
from drawlib.shapes import rectangle

styles = default_styles
setup(width=100, height=100)
rectangle((50, 50), width=40, height=30, style=styles.Primary)
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
        """from drawlib.canvas import save, setup
from drawlib.styles import Styles as default_styles
from drawlib.shapes import rectangle

styles = default_styles
setup(width=100, height=100)
rectangle((50, 50), width=40, height=30, style=styles.Primary)
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
circle((30, 30), radius=10, style=styles.Primary)
```

```drawlib file:second.png
rectangle((50, 50), width=20, height=20, style=styles.Primary)
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
from drawlib.shapes import circle
from drawlib.styles import Styles
circle((50, 50), radius=20, style=Styles.Primary)
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
from drawlib.shapes import circle
from drawlib.styles import Styles
circle((50, 50), radius=20, style=Styles.Primary)
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


def test_cli_show_python_script_no_cache(tmp_path: Path) -> None:
    """Test show command executing a Python script with --no-cache flag."""
    script = tmp_path / "drawing_nocache.py"
    script.write_text(
        """from drawlib.canvas import save, setup
from drawlib.styles import Styles as default_styles
from drawlib.shapes import circle

styles = default_styles
setup(width=100, height=100)
circle((50, 50), radius=20, style=styles.Primary)
save()
""",
        encoding="utf-8",
    )
    out_png = tmp_path / "out_nocache.png"

    res = run_drawlib_cli(["show", str(script), "-o", str(out_png), "--no-cache"], cwd=str(tmp_path))
    assert res.returncode == 0
    assert out_png.exists()


def test_cli_show_markdown_block_no_cache(tmp_path: Path) -> None:
    """Test show command executing a Markdown block with --no-cache flag."""
    doc = tmp_path / "doc_nocache.md"
    doc.write_text(
        """# Doc

```drawlib
from drawlib.shapes import circle
from drawlib.styles import Styles
circle((50, 50), radius=20, style=Styles.Primary)
```
""",
        encoding="utf-8",
    )
    out_png = tmp_path / "out_block_nocache.png"

    res = run_drawlib_cli(["show", str(doc), "1", "-o", str(out_png), "--no-cache"], cwd=str(tmp_path))
    assert res.returncode == 0
    assert out_png.exists()
