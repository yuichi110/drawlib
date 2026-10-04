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
import sys

import pytest

from tests.cli.common import run_drawlib_cli


def _is_playwright_available() -> bool:
    try:
        from playwright.sync_api import sync_playwright  # noqa: PLC0415

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            browser.close()
        return True
    except Exception:
        return False


def test_cli_build_html_directory_default(tmp_path) -> None:
    """Test CLI build html directory (PNG image export + external style.css)."""
    src_dir = tmp_path / "src_docs"
    out_dir = tmp_path / "dist_docs"
    src_dir.mkdir()

    (src_dir / "template.html").write_text(
        '<!DOCTYPE html><html><head>{% if css_href %}<link rel="stylesheet" href="{{ css_href }}">'
        "{% endif %}</head><body>{{ body }}</body></html>",
        encoding="utf-8",
    )
    (src_dir / "style.css").write_text("body { margin: 0; }", encoding="utf-8")
    (src_dir / "index.md").write_text(
        """# Main Index

```drawlib file:circle.png
from drawlib.styles import Styles
from drawlib.shapes import circle
circle((50, 50), radius=20, style=Styles.Primary)
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
    index_img = out_dir / "index_images" / "circle.png"

    assert index_html.exists()
    assert style_css.exists()
    assert index_img.exists()

    content = index_html.read_text(encoding="utf-8")
    assert '<link rel="stylesheet" href="style.css">' in content
    assert '<img src="index_images/circle.png"' in content


def test_cli_build_html_single_file_rejected(tmp_path) -> None:
    """Test CLI build html rejects single file with descriptive error."""
    input_md = tmp_path / "sample.md"
    input_md.write_text("# Sample Page\n", encoding="utf-8")
    output_html = tmp_path / "sample.html"

    res = run_drawlib_cli(["build", "html", str(input_md), "-o", str(output_html)], cwd=str(tmp_path))

    assert res.returncode != 0
    assert "requires a directory as input" in res.stderr or "requires a directory as input" in res.stdout


def test_cli_build_html_webp_format(tmp_path) -> None:
    """Test CLI build html with -f webp."""
    src_dir = tmp_path / "src_webp"
    out_dir = tmp_path / "out_webp"
    src_dir.mkdir()

    (src_dir / "template.html").write_text(
        '<!DOCTYPE html><html><head>{% if css_href %}<link rel="stylesheet" href="{{ css_href }}">'
        "{% endif %}</head><body>{{ body }}</body></html>",
        encoding="utf-8",
    )
    (src_dir / "style.css").write_text("body { margin: 0; }", encoding="utf-8")
    (src_dir / "index.md").write_text(
        """# WebP Test

```drawlib file:circle.webp
from drawlib.styles import Styles
from drawlib.shapes import circle
circle((50, 50), radius=10, style=Styles.Primary)
```
""",
        encoding="utf-8",
    )
    (src_dir / "navbar.md").write_text("- [WebP Test](index.md)\n", encoding="utf-8")

    res = run_drawlib_cli(
        ["build", "html", str(src_dir), "-o", str(out_dir), "-f", "webp"],
        cwd=str(tmp_path),
    )

    assert res.returncode == 0
    content = (out_dir / "index.html").read_text(encoding="utf-8")
    assert "index_images/circle.webp" in content
    assert (out_dir / "index_images" / "circle.webp").exists()

    # Verify deprecated --image-format is rejected
    res_err = run_drawlib_cli(
        ["build", "html", str(src_dir), "-o", str(out_dir), "--image-format", "webp"],
        cwd=str(tmp_path),
    )
    assert res_err.returncode != 0


def test_cli_build_markdown_directory(tmp_path) -> None:
    """Test CLI build markdown directory."""
    src_dir = tmp_path / "src_md"
    out_dir = tmp_path / "out_md"
    src_dir.mkdir()

    (src_dir / "doc.md").write_text(
        """# Markdown Output

```drawlib file:circle.png
from drawlib.styles import Styles
from drawlib.shapes import circle
circle((50, 50), radius=10, style=Styles.Primary)
```
""",
        encoding="utf-8",
    )

    res = run_drawlib_cli(["build", "markdown", str(src_dir), "-o", str(out_dir)], cwd=str(tmp_path))

    assert res.returncode == 0
    assert "Successfully compiled Markdown" in res.stdout
    assert (out_dir / "doc.md").exists()
    assert (out_dir / "doc_images" / "circle.png").exists()


def test_cli_build_single_file_rejected(tmp_path) -> None:
    """Test CLI build markdown rejects single file input."""
    input_md = tmp_path / "sample.md"
    input_md.write_text("# Single File Test", encoding="utf-8")

    res = run_drawlib_cli(["build", "markdown", str(input_md)], cwd=str(tmp_path))

    assert res.returncode != 0
    assert "requires a directory as input" in res.stderr or "requires a directory as input" in res.stdout


def test_cli_build_image_single_file(tmp_path) -> None:
    """Test CLI build image command executes Python script."""
    script = tmp_path / "simple.py"
    script.write_text(
        """from drawlib.canvas import save
from drawlib.styles import Styles as default_styles
from drawlib.shapes import circle

styles = default_styles
circle((50, 50), radius=10, style=styles.Primary)
save()
""",
        encoding="utf-8",
    )

    res = run_drawlib_cli(["build", "image", str(script)], cwd=str(tmp_path))
    assert res.returncode == 0
    assert (tmp_path / "simple.png").exists()


def test_cli_build_images_removed_error(tmp_path) -> None:
    """Test CLI build images alias is rejected after being removed."""
    script = tmp_path / "simple.py"
    script.write_text(
        """from drawlib.canvas import save
save()
""",
        encoding="utf-8",
    )

    res = run_drawlib_cli(["build", "images", str(script)], cwd=str(tmp_path))
    assert res.returncode != 0


def test_cli_build_image_subdirectories(tmp_path) -> None:
    """Test CLI build image preserves subdirectory structure under output directory."""
    codes_dir = tmp_path / "codes"
    sub_a = codes_dir / "about"
    sub_b = codes_dir / "qs"
    sub_a.mkdir(parents=True)
    sub_b.mkdir(parents=True)

    (sub_a / "img_a.py").write_text(
        """from drawlib.canvas import save
from drawlib.styles import Styles as default_styles
from drawlib.shapes import circle

styles = default_styles
circle((50, 50), radius=10, style=styles.Primary)
save()
""",
        encoding="utf-8",
    )
    (sub_b / "img_b.py").write_text(
        """from drawlib.canvas import save
from drawlib.styles import Styles as default_styles
from drawlib.shapes import circle

styles = default_styles
circle((30, 30), radius=10, style=styles.Primary)
save()
""",
        encoding="utf-8",
    )

    out_images = tmp_path / "images"
    res = run_drawlib_cli(
        ["build", "image", str(codes_dir), "-o", str(out_images)],
        cwd=str(tmp_path),
    )
    assert res.returncode == 0
    assert (out_images / "about" / "img_a.png").exists()
    assert (out_images / "qs" / "img_b.png").exists()


def test_cli_build_image_auto_detect(tmp_path) -> None:
    """Test CLI build image auto-detects codes/ and routes to images/ when given root directory."""
    root_dir = tmp_path / "readme_assets"
    sub_codes = root_dir / "codes" / "feature"
    sub_codes.mkdir(parents=True)

    (sub_codes / "feat.py").write_text(
        """from drawlib.canvas import save
from drawlib.styles import Styles as default_styles
from drawlib.shapes import circle

styles = default_styles
circle((50, 50), radius=15, style=styles.Primary)
save()
""",
        encoding="utf-8",
    )

    res = run_drawlib_cli(
        ["build", "image", str(root_dir)],
        cwd=str(tmp_path),
    )
    assert res.returncode == 0
    assert (root_dir / "images" / "feature" / "feat.png").exists()


def test_cli_build_pdf_deterministic(tmp_path) -> None:
    """Test CLI build pdf produces deterministic identical bytes without --timestamp."""
    if not _is_playwright_available():
        pytest.skip("Playwright or headless Chromium not available")

    doc_dir = tmp_path / "doc_src"
    doc_dir.mkdir()
    (doc_dir / "template.html").write_text("<!DOCTYPE html><html><body>{{ body }}</body></html>", encoding="utf-8")
    (doc_dir / "style.css").write_text("body { margin: 0; }", encoding="utf-8")
    (doc_dir / "00_intro.md").write_text("# Title\n\nContent for PDF.", encoding="utf-8")

    out_pdf1 = tmp_path / "doc1.pdf"
    out_pdf2 = tmp_path / "doc2.pdf"

    res1 = run_drawlib_cli(["build", "pdf", str(doc_dir), "-o", str(out_pdf1)], cwd=str(tmp_path))
    assert res1.returncode == 0
    res2 = run_drawlib_cli(["build", "pdf", str(doc_dir), "-o", str(out_pdf2)], cwd=str(tmp_path))
    assert res2.returncode == 0

    assert out_pdf1.read_bytes() == out_pdf2.read_bytes()
    assert b"D:20260101000000+00'00'" in out_pdf1.read_bytes()


def test_cli_build_pdf_timestamp_flag(tmp_path) -> None:
    """Test CLI build pdf preserves timestamp when --timestamp is provided."""
    if not _is_playwright_available():
        pytest.skip("Playwright or headless Chromium not available")

    doc_dir = tmp_path / "doc_src"
    doc_dir.mkdir()
    (doc_dir / "template.html").write_text("<!DOCTYPE html><html><body>{{ body }}</body></html>", encoding="utf-8")
    (doc_dir / "style.css").write_text("body { margin: 0; }", encoding="utf-8")
    (doc_dir / "00_intro.md").write_text("# Title\n\nContent for PDF.", encoding="utf-8")

    out_pdf = tmp_path / "doc_ts.pdf"
    res = run_drawlib_cli(["build", "pdf", str(doc_dir), "-o", str(out_pdf), "--timestamp"], cwd=str(tmp_path))
    assert res.returncode == 0

    data = out_pdf.read_bytes()
    assert b"/CreationDate (D:" in data
    assert b"D:20260101000000+00'00'" not in data


def test_cli_build_multiple_inputs_rejected(tmp_path) -> None:
    """Test that all build commands reject multiple input arguments."""
    file1 = tmp_path / "a.py"
    file2 = tmp_path / "b.py"
    file1.touch()
    file2.touch()

    # image
    res_img = run_drawlib_cli(["build", "image", str(file1), str(file2)], cwd=str(tmp_path))
    assert res_img.returncode != 0

    # markdown
    res_md = run_drawlib_cli(["build", "markdown", str(file1), str(file2)], cwd=str(tmp_path))
    assert res_md.returncode != 0

    # html
    res_html = run_drawlib_cli(["build", "html", str(file1), str(file2)], cwd=str(tmp_path))
    assert res_html.returncode != 0

    # pdf
    res_pdf = run_drawlib_cli(["build", "pdf", str(file1), str(file2)], cwd=str(tmp_path))
    assert res_pdf.returncode != 0


def test_cli_build_pdf_single_markdown_file(tmp_path) -> None:
    """Test CLI build pdf compiles a single standalone markdown file into PDF."""
    if not _is_playwright_available():
        pytest.skip("Playwright or headless Chromium not available")

    md_file = tmp_path / "spec.md"
    md_file.write_text("# Specification\n\nThis is a single-file technical spec.", encoding="utf-8")
    out_pdf = tmp_path / "spec.pdf"

    res = run_drawlib_cli(["build", "pdf", str(md_file), "-o", str(out_pdf)], cwd=str(tmp_path))
    assert res.returncode == 0
    assert "Successfully compiled PDF" in res.stdout
    assert out_pdf.exists()
    assert out_pdf.stat().st_size > 0


def test_cli_build_pdf_slide_project(tmp_path) -> None:
    """Test CLI build pdf compiles a slide project into presentation PDF."""
    if not _is_playwright_available():
        pytest.skip("Playwright or headless Chromium not available")

    slide_dir = tmp_path / "slide_src"
    slide_dir.mkdir()
    (slide_dir / "slide.css").write_text("@media print { @page { size: 16in 9in; } }", encoding="utf-8")
    (slide_dir / "01_title.md").write_text("# Slide Title\n\nPresentation slide content.", encoding="utf-8")

    out_pdf = tmp_path / "presentation.pdf"
    res = run_drawlib_cli(["build", "pdf", str(slide_dir), "-o", str(out_pdf)], cwd=str(tmp_path))
    assert res.returncode == 0
    assert "Successfully compiled PDF" in res.stdout
    assert out_pdf.exists()
    assert out_pdf.stat().st_size > 0


def test_cli_build_image_from_markdown(tmp_path) -> None:
    """Test CLI build image extracts and renders drawlib blocks from Markdown files."""
    doc_dir = tmp_path / "doc_src"
    doc_dir.mkdir()
    (doc_dir / "chapter.md").write_text(
        """# Chapter 1

Here is an architectural diagram:

```drawlib file:arch.png
from drawlib.shapes import rectangle
from drawlib.styles import Styles
rectangle((50, 50), width=40, height=20, style=Styles.Primary)
```
""",
        encoding="utf-8",
    )

    out_images = tmp_path / "images"
    res = run_drawlib_cli(["build", "image", str(doc_dir), "-o", str(out_images)], cwd=str(tmp_path))
    assert res.returncode == 0
    assert "Successfully executed image build" in res.stdout
    assert (out_images / "chapter_images" / "arch.png").exists()
    assert (out_images / "chapter_images" / "arch.png").stat().st_size > 0
