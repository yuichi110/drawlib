# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

# ruff: noqa: S404, S603

"""Integration tests using subprocess to verify drawlib CLI build {markdown, html, pdf} subcommands."""

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


def test_cli_build_html_directory_default(tmp_path) -> None:
    """Test CLI build html directory (PNG image export + external style.css)."""
    src_dir = tmp_path / "src_docs"
    out_dir = tmp_path / "dist_docs"
    src_dir.mkdir()

    (src_dir / "index.md").write_text(
        """# Main Index

```drawlib
circle((50, 50), radius=20, style=styles.primary)
```
""",
        encoding="utf-8",
    )
    (src_dir / "navbar.md").write_text("- [Main Index](index.md)\n", encoding="utf-8")

    res = run_drawlib_cli(["build", "html", str(src_dir), "-o", str(out_dir)], cwd=str(tmp_path))

    assert res.returncode == 0
    assert "Successfully compiled HTML" in res.stdout

    index_html = out_dir / "index.html"
    style_css = out_dir / "style.css"
    index_img = out_dir / "index_images" / "1.png"

    assert index_html.exists()
    assert style_css.exists()
    assert index_img.exists()

    content = index_html.read_text(encoding="utf-8")
    assert '<link rel="stylesheet" href="style.css">' in content
    assert '<img src="index_images/1.png"' in content


def test_cli_build_html_single_file(tmp_path) -> None:
    """Test CLI build html single file (external style.css + PNG image)."""
    input_md = tmp_path / "sample.md"
    output_html = tmp_path / "sample.html"

    input_md.write_text(
        """# Sample Page

```drawlib
rectangle((50, 50), width=40, height=20, style=styles.primary)
```
""",
        encoding="utf-8",
    )

    res = run_drawlib_cli(["build", "html", str(input_md), "-o", str(output_html)], cwd=str(tmp_path))

    assert res.returncode == 0
    assert output_html.exists()
    assert (tmp_path / "style.css").exists()
    assert (tmp_path / "sample_images" / "1.png").exists()
    assert '<link rel="stylesheet" href="style.css">' in output_html.read_text(encoding="utf-8")


def test_cli_build_html_webp_format(tmp_path) -> None:
    """Test CLI build html with --image-format webp."""
    input_md = tmp_path / "sample.md"
    output_html = tmp_path / "sample.html"

    input_md.write_text(
        """# WebP Test

```drawlib
circle((50, 50), radius=10, style=styles.primary)
```
""",
        encoding="utf-8",
    )

    res = run_drawlib_cli(
        ["build", "html", str(input_md), "-o", str(output_html), "--image-format", "webp"],
        cwd=str(tmp_path),
    )

    assert res.returncode == 0
    content = output_html.read_text(encoding="utf-8")
    assert "sample_images/1.webp" in content
    assert (tmp_path / "sample_images" / "1.webp").exists()


def test_cli_build_markdown_single_file(tmp_path) -> None:
    """Test CLI build markdown single file."""
    input_md = tmp_path / "doc.md"
    out_md = tmp_path / "rendered.md"
    input_md.write_text(
        """# Markdown Output

```drawlib
circle((50, 50), radius=10, style=styles.primary)
```
""",
        encoding="utf-8",
    )

    res = run_drawlib_cli(["build", "markdown", str(input_md), "-o", str(out_md)], cwd=str(tmp_path))

    assert res.returncode == 0
    assert "Successfully compiled Markdown" in res.stdout
    assert out_md.exists()
    assert (tmp_path / "rendered_images" / "1.png").exists()


def test_cli_build_overwrite_error(tmp_path) -> None:
    """Test CLI build markdown error when output path equals input source file."""
    input_md = tmp_path / "sample.md"
    input_md.write_text("# Overwrite Test", encoding="utf-8")

    res = run_drawlib_cli(["build", "markdown", str(input_md), "-o", str(input_md)], cwd=str(tmp_path))

    assert res.returncode != 0
    assert "Refusing to overwrite input source file" in res.stderr or "Refusing to overwrite" in res.stdout


def test_cli_build_images_alias(tmp_path) -> None:
    """Test CLI build images alias command executes Python script."""
    script = tmp_path / "simple.py"
    script.write_text(
        """from drawlib.canvas import save
from drawlib.preset_styles import get_default_styles
from drawlib.shapes import circle

styles = get_default_styles()
circle((50, 50), radius=10, style=styles.primary)
save()
""",
        encoding="utf-8",
    )

    res = run_drawlib_cli(["build", "images", str(script)], cwd=str(tmp_path))
    assert res.returncode == 0
    assert (tmp_path / "simple.png").exists()


def test_cli_build_images_subdirectories(tmp_path) -> None:
    """Test CLI build images preserves subdirectory structure under output directory."""
    codes_dir = tmp_path / "codes"
    sub_a = codes_dir / "about"
    sub_b = codes_dir / "qs"
    sub_a.mkdir(parents=True)
    sub_b.mkdir(parents=True)

    (sub_a / "img_a.py").write_text(
        """from drawlib.canvas import save
from drawlib.preset_styles import get_default_styles
from drawlib.shapes import circle

styles = get_default_styles()
circle((50, 50), radius=10, style=styles.primary)
save()
""",
        encoding="utf-8",
    )
    (sub_b / "img_b.py").write_text(
        """from drawlib.canvas import save
from drawlib.preset_styles import get_default_styles
from drawlib.shapes import circle

styles = get_default_styles()
circle((30, 30), radius=10, style=styles.primary)
save()
""",
        encoding="utf-8",
    )

    out_images = tmp_path / "images"
    res = run_drawlib_cli(
        ["build", "images", str(codes_dir), "-o", str(out_images)],
        cwd=str(tmp_path),
    )
    assert res.returncode == 0
    assert (out_images / "about" / "img_a.png").exists()
    assert (out_images / "qs" / "img_b.png").exists()


def test_cli_build_images_auto_detect(tmp_path) -> None:
    """Test CLI build images auto-detects codes/ and routes to images/ when given root directory."""
    root_dir = tmp_path / "readme_assets"
    sub_codes = root_dir / "codes" / "feature"
    sub_codes.mkdir(parents=True)

    (sub_codes / "feat.py").write_text(
        """from drawlib.canvas import save
from drawlib.preset_styles import get_default_styles
from drawlib.shapes import circle

styles = get_default_styles()
circle((50, 50), radius=15, style=styles.primary)
save()
""",
        encoding="utf-8",
    )

    res = run_drawlib_cli(
        ["build", "images", str(root_dir)],
        cwd=str(tmp_path),
    )
    assert res.returncode == 0
    assert (root_dir / "images" / "feature" / "feat.png").exists()
