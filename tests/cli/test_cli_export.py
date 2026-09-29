# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

# ruff: noqa: S404, S603

"""Integration tests using subprocess to verify drawlib CLI show -o option (consolidated export)."""

from pathlib import Path

from tests.cli.common import run_drawlib_cli


def test_cli_show_by_index_with_output(tmp_path: Path) -> None:
    """Test exporting a specific block by index to a designated output file using show -o."""
    md_file = tmp_path / "doc.md"
    md_file.write_text(
        """# Sample Document

```drawlib
from drawlib.canvas import setup
from drawlib.styles import Styles
from drawlib.shapes import circle
setup(width=100, height=100)
circle((50, 50), radius=20, style=Styles.primary)
```
""",
        encoding="utf-8",
    )

    out_file = tmp_path / "custom_output.png"
    res = run_drawlib_cli(["show", str(md_file), "1", "-o", str(out_file)], cwd=str(tmp_path))
    assert res.returncode == 0
    assert "Successfully exported block #1 to:" in res.stdout
    assert out_file.exists()
    assert out_file.stat().st_size > 0


def test_cli_show_with_styles_and_output(tmp_path: Path) -> None:
    """Test show -o command executing code block with a custom styles script."""
    styles_file = tmp_path / "my_styles.py"
    styles_file.write_text(
        """from drawlib.preset_styles import MonochromeStyles
Styles = MonochromeStyles
""",
        encoding="utf-8",
    )

    md_file = tmp_path / "doc.md"
    md_file.write_text(
        """# Styled Document

```drawlib
from drawlib.canvas import setup
from drawlib.styles import Styles
from drawlib.shapes import circle
assert getattr(Styles, '__name__', Styles.__class__.__name__) in ("StylesMonochrome", "MonochromeStyles")
setup(width=100, height=100)
circle((50, 50), radius=20, style=Styles.Primary)
```
""",
        encoding="utf-8",
    )

    out_file = tmp_path / "styled_output.png"
    res = run_drawlib_cli(
        ["show", str(md_file), "1", "-o", str(out_file), "--styles", str(styles_file)],
        cwd=str(tmp_path),
    )
    assert res.returncode == 0
    assert out_file.exists()


def test_cli_show_with_utils_and_output(tmp_path: Path) -> None:
    """Test show -o command executing code block with a custom utils script."""
    utils_file = tmp_path / "my_utils.py"
    utils_file.write_text(
        """def get_radius() -> float:
    return 25.0
""",
        encoding="utf-8",
    )

    md_file = tmp_path / "doc.md"
    md_file.write_text(
        """# Utils Document

```drawlib
from drawlib.canvas import setup
from drawlib.styles import Styles
from drawlib.utils import get_radius
from drawlib.shapes import circle
setup(width=100, height=100)
circle((50, 50), radius=get_radius(), style=Styles.primary)
```
""",
        encoding="utf-8",
    )

    out_file = tmp_path / "utils_output.png"
    res = run_drawlib_cli(
        ["show", str(md_file), "1", "-o", str(out_file), "--utils", str(utils_file)],
        cwd=str(tmp_path),
    )
    assert res.returncode == 0
    assert out_file.exists()


def test_cli_show_with_grid_and_output(tmp_path: Path) -> None:
    """Test exporting code block with coordinate grid overlay using show -o."""
    md_file = tmp_path / "doc.md"
    md_file.write_text(
        """# Sample Document

```drawlib
from drawlib.canvas import setup
from drawlib.styles import Styles
from drawlib.shapes import circle
setup(width=100, height=100)
circle((50, 50), radius=20, style=Styles.primary)
```
""",
        encoding="utf-8",
    )

    out_file = tmp_path / "grid_output.png"
    res = run_drawlib_cli(["show", str(md_file), "1", "-o", str(out_file), "--grid"], cwd=str(tmp_path))
    assert res.returncode == 0
    assert out_file.exists()
    assert out_file.stat().st_size > 0


def test_cli_show_python_script_with_output(tmp_path: Path) -> None:
    """Test show -o command directly exporting a Python script to image."""
    script_file = tmp_path / "draw_standalone.py"
    script_file.write_text(
        """from drawlib.canvas import setup
from drawlib.styles import Styles
from drawlib.shapes import circle

setup(width=100, height=100)
circle((50, 50), radius=20, style=Styles.primary)
""",
        encoding="utf-8",
    )

    out_file = tmp_path / "standalone_out.png"
    res = run_drawlib_cli(["show", str(script_file), "-o", str(out_file)], cwd=str(tmp_path))
    assert res.returncode == 0
    assert out_file.exists()


def test_cli_export_command_removed(tmp_path: Path) -> None:
    """Verify that the top-level export command has been removed in favor of show -o."""
    res = run_drawlib_cli(["export"], cwd=str(tmp_path))
    assert res.returncode != 0
    assert "No such command 'export'" in res.stderr or "No such command 'export'" in res.stdout
