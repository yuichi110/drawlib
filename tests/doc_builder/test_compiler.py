# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Integration tests for build_document compiler in doc_builder."""

import os

import pytest

from drawlib._tools.doc_builder import build_document, build_documents


def test_build_document_markdown_to_html(tmp_path) -> None:
    """Test compiling Markdown file to standalone HTML with PNG image export."""
    input_md = tmp_path / "sample.md"
    input_md.write_text(
        """# Architecture

```drawlib
circle((50, 50), radius=20, text="Core Engine")
```
""",
        encoding="utf-8",
    )

    out_html = tmp_path / "sample.html"
    res_path = build_document(input_path=str(input_md), output_path=str(out_html))

    assert os.path.exists(res_path)
    content = out_html.read_text(encoding="utf-8")
    assert "<!DOCTYPE html>" in content
    assert "<h1" in content
    assert '<img src="sample_images/1.png"' in content

    png_file = tmp_path / "sample_images" / "1.png"
    assert png_file.exists()


def test_build_document_inline_svg(tmp_path) -> None:
    """Test compiling Markdown file to standalone HTML with inline SVG."""
    input_md = tmp_path / "sample.md"
    input_md.write_text(
        """# Inline SVG

```drawlib
circle((50, 50), radius=20)
```
""",
        encoding="utf-8",
    )

    out_html = tmp_path / "sample.html"
    build_document(input_path=str(input_md), output_path=str(out_html), image_format="inline_svg")

    content = out_html.read_text(encoding="utf-8")
    assert "<svg" in content


def test_build_document_with_custom_css(tmp_path) -> None:
    """Test compiling with custom CSS injection."""
    input_md = tmp_path / "sample.md"
    input_md.write_text("# Styled Document", encoding="utf-8")

    custom_css = tmp_path / "custom.css"
    custom_css.write_text("body { background-color: #ff0000; }", encoding="utf-8")

    out_html = tmp_path / "sample.html"
    build_document(input_path=str(input_md), output_path=str(out_html), css_path=str(custom_css))

    content = out_html.read_text(encoding="utf-8")
    assert "background-color: #ff0000;" in content


def test_build_document_safety_guard_overwrite(tmp_path) -> None:
    """Test that build_document refuses to overwrite input source file."""
    input_md = tmp_path / "sample.md"
    input_md.write_text("# Test Document", encoding="utf-8")

    with pytest.raises(ValueError, match="Refusing to overwrite"):
        build_document(input_path=str(input_md), output_path=str(input_md), output_format="markdown")


def test_build_document_markdown_format(tmp_path) -> None:
    """Test compiling Markdown to rendered Markdown with embedded SVG."""
    input_md = tmp_path / "sample.md"
    input_md.write_text(
        """# Rendered MD Test

```drawlib
line((0, 0), (100, 100))
```
""",
        encoding="utf-8",
    )

    out_md = tmp_path / "sample.rendered.md"
    res_path = build_document(input_path=str(input_md), output_path=str(out_md), output_format="markdown")

    assert os.path.exists(res_path)
    content = out_md.read_text(encoding="utf-8")
    assert "# Rendered MD Test" in content
    assert "![sample.rendered_1](sample.rendered_images/1.png)" in content
    assert "```drawlib" not in content


def test_build_documents_batch(tmp_path) -> None:
    """Test build_documents batch compilation with target pairs and navigation."""
    doc1 = tmp_path / "page1.md"
    doc1.write_text("# Page One\n\n[Link to Page 2](./page2.md)", encoding="utf-8")

    doc2 = tmp_path / "page2.md"
    doc2.write_text("# Page Two\n\n[Link to Page 1](./page1.md)", encoding="utf-8")

    out1 = tmp_path / "out1.html"
    out2 = tmp_path / "out2.html"

    res_paths = build_documents(targets=[(str(doc1), str(out1)), (str(doc2), str(out2))])
    assert len(res_paths) == 2
    assert os.path.exists(str(out1))
    assert os.path.exists(str(out2))

    c1 = out1.read_text(encoding="utf-8")
    assert "Page One" in c1
    assert 'href="./page2.html"' in c1
    assert "nav-item active" in c1


def test_build_document_directory_recursive(tmp_path) -> None:
    """Test recursive directory build system with subdirectories and link rewriting."""
    src_dir = tmp_path / "src_docs"
    out_dir = tmp_path / "dist_docs"
    src_dir.mkdir()
    sub_dir = src_dir / "guide"
    sub_dir.mkdir()

    (src_dir / "index.md").write_text("# Home Page\n\n[Guide](./guide/canvas.md)", encoding="utf-8")
    (sub_dir / "canvas.md").write_text("# Canvas Guide\n\n[Home](../index.md)", encoding="utf-8")

    res_dir = build_document(input_path=str(src_dir), output_path=str(out_dir))

    assert res_dir == str(out_dir)
    index_html = out_dir / "index.html"
    canvas_html = out_dir / "guide" / "canvas.html"

    assert index_html.exists()
    assert canvas_html.exists()

    c_index = index_html.read_text(encoding="utf-8")
    assert 'href="./guide/canvas.html"' in c_index
    assert 'href="guide/canvas.html"' in c_index or 'href="./guide/canvas.html"' in c_index

    c_canvas = canvas_html.read_text(encoding="utf-8")
    assert 'href="../index.html"' in c_canvas


def test_build_document_static_assets_copy(tmp_path) -> None:
    """Test copying non-drawlib static assets (images, css) to output directory."""
    src_dir = tmp_path / "src_docs"
    out_dir = tmp_path / "dist_docs"
    src_dir.mkdir()

    img_dir = src_dir / "images"
    img_dir.mkdir()
    (img_dir / "logo.png").write_bytes(b"dummy_png_bytes")
    (src_dir / "index.md").write_text("# Title\n\n![Logo](./images/logo.png)", encoding="utf-8")

    build_document(input_path=str(src_dir), output_path=str(out_dir))

    copied_img = out_dir / "images" / "logo.png"
    assert copied_img.exists()
    assert copied_img.read_bytes() == b"dummy_png_bytes"


def test_build_document_css_modes(tmp_path) -> None:
    """Test css_mode embed and external modes for CSS generation."""
    src_dir = tmp_path / "src_docs"
    out_dir_ext = tmp_path / "out_external"
    out_dir_emb = tmp_path / "out_embed"
    src_dir.mkdir()
    (src_dir / "index.md").write_text("# CSS Test", encoding="utf-8")

    # Test auto/external mode for directory build
    build_document(input_path=str(src_dir), output_path=str(out_dir_ext), css_mode="external")
    style_css = out_dir_ext / "style.css"
    index_ext = out_dir_ext / "index.html"

    assert style_css.exists()
    assert '<link rel="stylesheet" href="style.css">' in index_ext.read_text(encoding="utf-8")

    # Test embed mode for directory build
    build_document(input_path=str(src_dir), output_path=str(out_dir_emb), css_mode="embed")
    index_emb = out_dir_emb / "index.html"
    assert "<style>" in index_emb.read_text(encoding="utf-8")
    assert not (out_dir_emb / "style.css").exists()


def test_build_document_pdf_embedded_images(tmp_path) -> None:
    """Test PDF compilation embeds images directly in PDF and creates zero external PNG files."""
    src_dir = tmp_path / "src_docs"
    out_dir = tmp_path / "dist_pdf"
    src_dir.mkdir()

    (src_dir / "index.md").write_text(
        """# PDF Embedded Test

```drawlib
circle((50, 50), radius=15)
```
""",
        encoding="utf-8",
    )

    build_document(input_path=str(src_dir), output_path=str(out_dir), output_format="pdf")

    pdf_file = out_dir / "index.pdf"
    assert pdf_file.exists()
    assert pdf_file.stat().st_size > 0

    # Ensure no external PNG images or style.css exist in output directory
    png_files = list(out_dir.glob("*.png"))
    assert len(png_files) == 0
    assert not (out_dir / "style.css").exists()


def test_build_document_missing_image_warning(tmp_path, capsys) -> None:
    """Test warning is emitted when local static image referenced in Markdown is missing."""
    doc = tmp_path / "missing_img.md"
    doc.write_text("# Doc\n\n![Nonexistent](missing_test_image.png)\n", encoding="utf-8")
    out = tmp_path / "out.html"

    build_document(input_path=str(doc), output_path=str(out))
    captured = capsys.readouterr()
    assert "WARNING: Image 'missing_test_image.png'" in captured.err
