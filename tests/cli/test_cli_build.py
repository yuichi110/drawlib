# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

# ruff: noqa: S404, S603

"""Integration tests using subprocess to verify drawlib CLI build command variations."""

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


def test_cli_build_directory_default(tmp_path) -> None:
    """Test CLI directory build (PNG image export + external style.css)."""
    src_dir = tmp_path / "src_docs"
    out_dir = tmp_path / "dist_docs"
    src_dir.mkdir()

    (src_dir / "index.md").write_text(
        """# Main Index

```drawlib
circle((50, 50), radius=20)
```
""",
        encoding="utf-8",
    )

    res = run_drawlib_cli(["build", str(src_dir), "-o", str(out_dir)], cwd=str(tmp_path))

    assert res.returncode == 0
    assert "Successfully compiled document(s)" in res.stdout

    index_html = out_dir / "index.html"
    style_css = out_dir / "style.css"
    index_img = out_dir / "index_images" / "1.png"

    assert index_html.exists()
    assert style_css.exists()
    assert index_img.exists()

    content = index_html.read_text(encoding="utf-8")
    assert '<link rel="stylesheet" href="style.css">' in content
    assert '<img src="index_images/1.png"' in content


def test_cli_build_single_file(tmp_path) -> None:
    """Test CLI single file build."""
    input_md = tmp_path / "sample.md"
    output_html = tmp_path / "sample.html"

    input_md.write_text(
        """# Sample Page

```drawlib
rectangle((50, 50), width=40, height=20)
```
""",
        encoding="utf-8",
    )

    res = run_drawlib_cli(["build", str(input_md), "-o", str(output_html)], cwd=str(tmp_path))

    assert res.returncode == 0
    assert output_html.exists()
    assert (tmp_path / "sample_images" / "1.png").exists()


def test_cli_build_inline_svg(tmp_path) -> None:
    """Test CLI build with --image-format inline_svg."""
    input_md = tmp_path / "sample.md"
    output_html = tmp_path / "sample.html"

    input_md.write_text(
        """# SVG Test

```drawlib
circle((50, 50), radius=10)
```
""",
        encoding="utf-8",
    )

    res = run_drawlib_cli(
        ["build", str(input_md), "-o", str(output_html), "--image-format", "inline_svg"],
        cwd=str(tmp_path),
    )

    assert res.returncode == 0
    content = output_html.read_text(encoding="utf-8")
    assert "<svg" in content
    assert "sample_1.png" not in content


def test_cli_build_css_embed_mode(tmp_path) -> None:
    """Test CLI directory build with --css-mode embed."""
    src_dir = tmp_path / "src_docs"
    out_dir = tmp_path / "dist_docs"
    src_dir.mkdir()

    (src_dir / "index.md").write_text("# Embedded CSS Test", encoding="utf-8")

    res = run_drawlib_cli(
        ["build", str(src_dir), "-o", str(out_dir), "--css-mode", "embed"],
        cwd=str(tmp_path),
    )

    assert res.returncode == 0
    index_html = out_dir / "index.html"
    style_css = out_dir / "style.css"

    assert index_html.exists()
    assert not style_css.exists()
    assert "<style>" in index_html.read_text(encoding="utf-8")


def test_cli_build_overwrite_error(tmp_path) -> None:
    """Test CLI build error when output path equals input source file."""
    input_md = tmp_path / "sample.md"
    input_md.write_text("# Overwrite Test", encoding="utf-8")

    res = run_drawlib_cli(["build", str(input_md), "-o", str(input_md)], cwd=str(tmp_path))

    assert res.returncode != 0
    assert "Refusing to overwrite input source file" in res.stderr
