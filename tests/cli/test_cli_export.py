# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

# ruff: noqa: S404, S603

"""Integration tests using subprocess to verify drawlib CLI export command and show -o option."""

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


def test_cli_export_list(tmp_path: Path) -> None:
    """Test export command listing available code blocks when target is omitted."""
    md_file = tmp_path / "doc.md"
    md_file.write_text(
        """# Sample Document

```drawlib 400px center caption:"First Image"
from drawlib.canvas import setup
from drawlib.config import styles
from drawlib.shapes import circle
setup(width=100, height=100)
circle((50, 50), radius=20, style=styles.primary)
```

```drawlib 500px file:custom.png
from drawlib.canvas import setup
from drawlib.config import styles
from drawlib.shapes import rectangle
setup(width=100, height=100)
rectangle((50, 50), width=40, height=30, style=styles.primary)
```
""",
        encoding="utf-8",
    )

    res = run_drawlib_cli(["export", str(md_file)], cwd=str(tmp_path))
    assert res.returncode == 0
    assert "Available drawlib code blocks in" in res.stdout
    assert "doc_images/1.png" in res.stdout
    assert "doc_images/custom.png" in res.stdout


def test_cli_export_by_index_with_output(tmp_path: Path) -> None:
    """Test exporting a specific block by index to a designated output file."""
    md_file = tmp_path / "doc.md"
    md_file.write_text(
        """# Sample Document

```drawlib
from drawlib.canvas import setup
from drawlib.config import styles
from drawlib.shapes import circle
setup(width=100, height=100)
circle((50, 50), radius=20, style=styles.primary)
```
""",
        encoding="utf-8",
    )

    out_file = tmp_path / "custom_output.png"
    res = run_drawlib_cli(["export", str(md_file), "1", "-o", str(out_file)], cwd=str(tmp_path))
    assert res.returncode == 0
    assert "Successfully exported block #1 to:" in res.stdout
    assert out_file.exists()
    assert out_file.stat().st_size > 0


def test_cli_export_with_config(tmp_path: Path) -> None:
    """Test export command executing code block with a Python config/setup script."""
    config_file = tmp_path / "my_config.py"
    config_file.write_text(
        """# Config script setting a global variable or environment
import os
os.environ["DRAWLIB_TEST_CONFIG_FLAG"] = "applied"
""",
        encoding="utf-8",
    )

    md_file = tmp_path / "doc.md"
    md_file.write_text(
        """# Configured Document

```drawlib
import os
from drawlib.canvas import setup
from drawlib.config import styles
from drawlib.shapes import circle
assert os.environ.get("DRAWLIB_TEST_CONFIG_FLAG") == "applied"
setup(width=100, height=100)
circle((50, 50), radius=20, style=styles.primary)
```
""",
        encoding="utf-8",
    )

    out_file = tmp_path / "configured_output.png"
    res = run_drawlib_cli(
        ["export", str(md_file), "1", "-o", str(out_file), "--config", str(config_file)],
        cwd=str(tmp_path),
    )
    assert res.returncode == 0
    assert out_file.exists()


def test_cli_export_with_grid(tmp_path: Path) -> None:
    """Test exporting code block with coordinate grid overlay."""
    md_file = tmp_path / "doc.md"
    md_file.write_text(
        """# Sample Document

```drawlib
from drawlib.canvas import setup
from drawlib.config import styles
from drawlib.shapes import circle
setup(width=100, height=100)
circle((50, 50), radius=20, style=styles.primary)
```
""",
        encoding="utf-8",
    )

    out_file = tmp_path / "grid_output.png"
    res = run_drawlib_cli(["export", str(md_file), "1", "-o", str(out_file), "--grid"], cwd=str(tmp_path))
    assert res.returncode == 0
    assert out_file.exists()
    assert out_file.stat().st_size > 0


def test_cli_export_python_script(tmp_path: Path) -> None:
    """Test export command directly executing a Python script."""
    script_file = tmp_path / "draw_standalone.py"
    script_file.write_text(
        """from drawlib.canvas import setup
from drawlib.preset_styles import default_styles
from drawlib.shapes import circle

styles = default_styles
setup(width=100, height=100)
circle((50, 50), radius=20, style=styles.primary)
""",
        encoding="utf-8",
    )

    out_file = tmp_path / "standalone_out.png"
    res = run_drawlib_cli(["export", str(script_file), "-o", str(out_file)], cwd=str(tmp_path))
    assert res.returncode == 0
    assert out_file.exists()


def test_cli_show_with_output_option(tmp_path: Path) -> None:
    """Test drawlib show command saving to file path using -o option without GUI display."""
    md_file = tmp_path / "doc.md"
    md_file.write_text(
        """# Sample Document

```drawlib
from drawlib.canvas import setup
from drawlib.config import styles
from drawlib.shapes import circle
setup(width=100, height=100)
circle((50, 50), radius=20, style=styles.primary)
```
""",
        encoding="utf-8",
    )

    out_file = tmp_path / "show_out.png"
    res = run_drawlib_cli(["show", str(md_file), "1", "-o", str(out_file)], cwd=str(tmp_path))
    assert res.returncode == 0
    assert out_file.exists()
    assert out_file.stat().st_size > 0
