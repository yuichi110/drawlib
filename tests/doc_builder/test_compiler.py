# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Integration tests for build_markdown, build_html, build_pdf, and detector in doc_builder."""

import os
from unittest.mock import MagicMock

import pytest

from drawlib._builder.doc_builder import (
    DocType,
    build_document,
    build_documents,
    build_html,
    build_markdown,
    build_pdf,
    detect_document_type,
    exporter_pdf,
)
from drawlib._builder.doc_builder.exporter_pdf import export_html_to_pdf
from drawlib._builder.doc_builder.merger import build_merged_html


def _is_playwright_chromium_available() -> bool:
    try:
        from playwright.sync_api import sync_playwright  # noqa: PLC0415

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            browser.close()
        return True
    except Exception:
        return False


def _setup_template_and_css(directory) -> None:
    template_content = (
        "<!DOCTYPE html>\n"
        "<html>\n"
        "<head>\n"
        "    <title>{{ title }}</title>\n"
        '    {% if css_href %}<link rel="stylesheet" href="{{ css_href }}">{% endif %}\n'
        "    {% if custom_css %}<style>{{ custom_css }}</style>{% endif %}\n"
        "</head>\n"
        "<body>\n"
        "    {% if nav_sections %}\n"
        "        {% for section in nav_sections %}\n"
        "            <div>{{ section.title }}</div>\n"
        "            <ul>\n"
        '            {% for item in section["items"] %}\n'
        '                <li class="nav-item {% if item.active %}active{% endif %}">'
        '<a href="{{ item.url }}" {% if item.is_external %}target="_blank"{% endif %}>{{ item.title }}</a></li>\n'
        "            {% endfor %}\n"
        "            </ul>\n"
        "        {% endfor %}\n"
        "    {% endif %}\n"
        "    {% if nav_items %}\n"
        "        <ul>\n"
        "        {% for item in nav_items %}\n"
        '            <li class="nav-item {% if item.active %}active{% endif %}">'
        '<a href="{{ item.url }}" {% if item.is_external %}target="_blank"{% endif %}>{{ item.title }}</a></li>\n'
        "        {% endfor %}\n"
        "        </ul>\n"
        "    {% endif %}\n"
        "    <main>{{ body }}</main>\n"
        "</body>\n"
        "</html>\n"
    )
    (directory / "template.html").write_text(template_content, encoding="utf-8")
    (directory / "style.css").write_text("body { margin: 0; }", encoding="utf-8")


def test_detect_document_type(tmp_path) -> None:
    """Test auto-detection of the 4 document input types."""
    md_dl = tmp_path / "doc_dl.md"
    md_dl.write_text("# Doc\n```drawlib\ncircle((50,50), 10)\n```\n", encoding="utf-8")
    info1 = detect_document_type(str(md_dl))
    assert info1.doc_type == "markdown_drawlib"
    assert info1.has_drawlib is True

    md_plain = tmp_path / "doc_plain.md"
    md_plain.write_text("# Plain Markdown\nHello", encoding="utf-8")
    info2 = detect_document_type(str(md_plain))
    assert info2.doc_type == "markdown"
    assert info2.has_drawlib is False

    html_dl = tmp_path / "doc_dl.html"
    html_dl.write_text(
        '<h1>HTML</h1>\n<script type="text/drawlib">\ncircle((50,50), 10)\n</script>',
        encoding="utf-8",
    )
    info3 = detect_document_type(str(html_dl))
    assert info3.doc_type == "html_drawlib"
    assert info3.has_drawlib is True

    html_plain = tmp_path / "doc_plain.html"
    html_plain.write_text("<h1>Plain HTML</h1>", encoding="utf-8")
    info4 = detect_document_type(str(html_plain))
    assert info4.doc_type == "html"
    assert info4.has_drawlib is False


def test_build_html_markdown_with_external_css(tmp_path) -> None:
    """Test compiling Markdown file to HTML with PNG image export and external style.css."""
    _setup_template_and_css(tmp_path)
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
    res_path = build_html(input_path=str(input_md), output_path=str(out_html))

    assert os.path.exists(res_path)
    content = out_html.read_text(encoding="utf-8")
    assert "<!DOCTYPE html>" in content
    assert "<h1" in content
    assert '<img src="sample_images/1.png"' in content
    assert '<link rel="stylesheet" href="style.css">' in content

    png_file = tmp_path / "sample_images" / "1.png"
    style_css = tmp_path / "style.css"
    assert png_file.exists()
    assert style_css.exists()


def test_build_html_webp_format(tmp_path) -> None:
    """Test compiling Markdown file to HTML with WebP image format."""
    _setup_template_and_css(tmp_path)
    input_md = tmp_path / "sample.md"
    input_md.write_text(
        """# WebP Test

```drawlib
circle((50, 50), radius=20)
```
""",
        encoding="utf-8",
    )

    out_html = tmp_path / "sample.html"
    build_html(input_path=str(input_md), output_path=str(out_html), image_format="webp")

    content = out_html.read_text(encoding="utf-8")
    assert '<img src="sample_images/1.webp"' in content
    assert (tmp_path / "sample_images" / "1.webp").exists()


def test_build_html_from_html_drawlib(tmp_path) -> None:
    """Test compiling HTML file containing <script type='text/drawlib'>."""
    _setup_template_and_css(tmp_path)
    input_html = tmp_path / "source.html"
    input_html.write_text(
        """<!DOCTYPE html>
<html>
<head><title>HTML Drawlib</title></head>
<body>
<h1>Diagram inside HTML</h1>
<script type="text/drawlib" file="my_fig.png">
circle((50, 50), radius=15)
</script>
</body>
</html>
""",
        encoding="utf-8",
    )
    out_html = tmp_path / "compiled.html"
    build_html(input_path=str(input_html), output_path=str(out_html))

    content = out_html.read_text(encoding="utf-8")
    assert '<img src="compiled_images/my_fig.png"' in content
    assert (tmp_path / "compiled_images" / "my_fig.png").exists()


def test_build_document_with_custom_css(tmp_path) -> None:
    """Test compiling with custom CSS written to external style.css."""
    _setup_template_and_css(tmp_path)
    (tmp_path / "style.css").write_text("body { background-color: #ff0000; }", encoding="utf-8")

    input_md = tmp_path / "sample.md"
    input_md.write_text("# Styled Document", encoding="utf-8")

    out_html = tmp_path / "sample.html"
    build_html(input_path=str(input_md), output_path=str(out_html))

    style_css = tmp_path / "style.css"
    assert style_css.exists()
    assert "background-color: #ff0000;" in style_css.read_text(encoding="utf-8")


def test_build_document_safety_guard_overwrite(tmp_path) -> None:
    """Test that build_markdown refuses to overwrite input source file."""
    input_md = tmp_path / "sample.md"
    input_md.write_text("# Test Document", encoding="utf-8")

    with pytest.raises(ValueError, match="Refusing to overwrite"):
        build_markdown(input_path=str(input_md), output_path=str(input_md))


def test_build_markdown_format(tmp_path) -> None:
    """Test compiling Markdown to rendered Markdown with external PNG."""
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
    res_path = build_markdown(input_path=str(input_md), output_path=str(out_md))

    assert os.path.exists(res_path)
    content = out_md.read_text(encoding="utf-8")
    assert "# Rendered MD Test" in content
    assert "![sample.rendered_1](sample.rendered_images/1.png)" in content
    assert "```drawlib" not in content


def test_build_documents_batch(tmp_path) -> None:
    """Test build_documents batch compilation with target pairs and navigation."""
    _setup_template_and_css(tmp_path)
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
    assert (tmp_path / "style.css").exists()

    c1 = out1.read_text(encoding="utf-8")
    assert "Page One" in c1
    assert 'href="./page2.html"' in c1
    assert "nav-item active" in c1


def test_build_document_directory_recursive(tmp_path) -> None:
    """Test recursive directory build system with subdirectories and navbar.md navigation."""
    src_dir = tmp_path / "src_docs"
    out_dir = tmp_path / "dist_docs"
    src_dir.mkdir()
    _setup_template_and_css(src_dir)
    sub_dir = src_dir / "guide"
    sub_dir.mkdir()

    (src_dir / "index.md").write_text("# Home Page\n\n[Guide](./guide/canvas.md)", encoding="utf-8")
    (src_dir / "navbar.md").write_text(
        "# Navigation\n\n- [Home](index.md)\n\n## Guides\n- [Canvas Guide](guide/canvas.md)\n",
        encoding="utf-8",
    )
    (sub_dir / "canvas.md").write_text("# Canvas Guide\n\n[Home](../index.md)", encoding="utf-8")

    res_dir = build_html(input_path=str(src_dir), output_path=str(out_dir))

    assert res_dir == str(out_dir)
    index_html = out_dir / "index.html"
    canvas_html = out_dir / "guide" / "canvas.html"

    assert index_html.exists()
    assert canvas_html.exists()
    assert (out_dir / "style.css").exists()
    assert not (out_dir / "navbar.html").exists()

    c_index = index_html.read_text(encoding="utf-8")
    assert 'href="guide/canvas.html"' in c_index or 'href="./guide/canvas.html"' in c_index
    assert '<link rel="stylesheet" href="style.css">' in c_index
    assert "Guides" in c_index

    c_canvas = canvas_html.read_text(encoding="utf-8")
    assert 'href="../index.html"' in c_canvas
    assert '<link rel="stylesheet" href="../style.css">' in c_canvas
    assert "nav-item active" in c_canvas


def test_build_document_static_assets_copy(tmp_path) -> None:
    """Test copying non-drawlib static assets (images, css) to output directory."""
    src_dir = tmp_path / "src_docs"
    out_dir = tmp_path / "dist_docs"
    src_dir.mkdir()
    _setup_template_and_css(src_dir)

    img_dir = src_dir / "images"
    img_dir.mkdir()
    (img_dir / "logo.png").write_bytes(b"dummy_png_bytes")
    (src_dir / "index.md").write_text("# Title\n\n![Logo](./images/logo.png)", encoding="utf-8")
    (src_dir / "navbar.md").write_text("- [Title](index.md)\n", encoding="utf-8")

    build_html(input_path=str(src_dir), output_path=str(out_dir))

    copied_img = out_dir / "images" / "logo.png"
    assert copied_img.exists()
    assert copied_img.read_bytes() == b"dummy_png_bytes"


def test_build_pdf_multi_document_merge(tmp_path) -> None:
    """Test build_pdf merges multiple inputs into a single PDF and embeds images."""
    if not _is_playwright_chromium_available():
        pytest.skip("Playwright or headless Chromium browser not available for PDF export test.")

    _setup_template_and_css(tmp_path)
    doc1 = tmp_path / "01_intro.md"
    doc1.write_text(
        """# Introduction

```drawlib
circle((50, 50), radius=15)
```
""",
        encoding="utf-8",
    )
    doc2 = tmp_path / "02_details.md"
    doc2.write_text("# Details\n\nDetailed architecture.", encoding="utf-8")

    out_pdf = tmp_path / "manual.pdf"
    res = build_pdf(
        inputs=[str(doc1), str(doc2)],
        output_path=str(out_pdf),
        toc=True,
        page_break=True,
        title="System Manual",
    )

    assert res == str(out_pdf)
    assert out_pdf.exists()
    assert out_pdf.stat().st_size > 0


def test_build_pdf_deterministic_timestamp(tmp_path) -> None:
    """Test build_pdf normalizes timestamps by default to produce deterministic byte-identical PDFs."""
    if not _is_playwright_chromium_available():
        pytest.skip("Playwright or headless Chromium browser not available for PDF export test.")

    _setup_template_and_css(tmp_path)
    doc = tmp_path / "doc.md"
    doc.write_text("# Chapter 1\n\nContent for deterministic test.", encoding="utf-8")

    out_pdf1 = tmp_path / "out1.pdf"
    out_pdf2 = tmp_path / "out2.pdf"

    build_pdf(inputs=[str(doc)], output_path=str(out_pdf1), timestamp=False)
    build_pdf(inputs=[str(doc)], output_path=str(out_pdf2), timestamp=False)

    bytes1 = out_pdf1.read_bytes()
    bytes2 = out_pdf2.read_bytes()

    assert bytes1 == bytes2
    assert b"D:20260101000000+00'00'" in bytes1


def test_build_pdf_with_timestamp(tmp_path) -> None:
    """Test build_pdf with timestamp=True preserves the current timestamp in metadata."""
    if not _is_playwright_chromium_available():
        pytest.skip("Playwright or headless Chromium browser not available for PDF export test.")

    _setup_template_and_css(tmp_path)
    doc = tmp_path / "doc.md"
    doc.write_text("# Chapter 1\n\nContent for timestamp test.", encoding="utf-8")

    out_pdf = tmp_path / "out_ts.pdf"
    build_pdf(inputs=[str(doc)], output_path=str(out_pdf), timestamp=True)

    data = out_pdf.read_bytes()
    assert b"/CreationDate (D:" in data
    # Should not be normalized to default fixed date
    assert b"D:20260101000000+00'00'" not in data


def test_export_html_to_pdf_missing_playwright(monkeypatch, tmp_path) -> None:
    """Test friendly error message is raised when playwright package is not installed."""
    orig_import = __import__

    def mock_import(name, *args, **kwargs):
        if "playwright" in name:
            raise ImportError(f"No module named '{name}'")
        return orig_import(name, *args, **kwargs)

    monkeypatch.setattr("builtins.__import__", mock_import)

    out_pdf = tmp_path / "out.pdf"
    with pytest.raises(RuntimeError) as exc_info:
        export_html_to_pdf("<h1>Test</h1>", str(out_pdf))

    err_msg = str(exc_info.value)
    assert "PDF export requires the 'playwright' package" in err_msg
    assert 'uv add "drawlib[pdf]"' in err_msg
    assert 'pip install "drawlib[pdf]"' in err_msg
    assert "uv run playwright install chromium" in err_msg
    assert "playwright install chromium" in err_msg


def test_export_html_to_pdf_missing_chromium(monkeypatch, tmp_path) -> None:
    """Test friendly error message is raised when Chromium browser is not downloaded."""
    mock_playwright = MagicMock()
    mock_p = MagicMock()
    mock_playwright.return_value.__enter__.return_value = mock_p
    mock_p.chromium.launch.side_effect = Exception(
        "Executable doesn't exist at /path/to/chromium. Run playwright install"
    )

    monkeypatch.setattr("playwright.sync_api.sync_playwright", mock_playwright)

    out_pdf = tmp_path / "out.pdf"
    with pytest.raises(RuntimeError) as exc_info:
        export_html_to_pdf("<h1>Test</h1>", str(out_pdf))

    err_msg = str(exc_info.value)
    assert "Playwright is installed, but the headless Chromium browser is missing." in err_msg
    assert "uv run playwright install chromium" in err_msg
    assert "playwright install chromium" in err_msg


def test_build_document_missing_image_warning(tmp_path, capsys) -> None:
    """Test warning is emitted when local static image referenced in Markdown is missing."""
    _setup_template_and_css(tmp_path)
    doc = tmp_path / "missing_img.md"
    doc.write_text("# Doc\n\n![Nonexistent](missing_test_image.png)\n", encoding="utf-8")
    out = tmp_path / "out.html"

    build_document(input_path=str(doc), output_path=str(out))
    captured = capsys.readouterr()
    assert "WARNING: Image 'missing_test_image.png'" in captured.err


def test_build_html_duplicate_document_outputs_error(tmp_path) -> None:
    """Test pre-check raises ValueError when two source files map to the same HTML output file."""
    src_dir = tmp_path / "src_dup"
    out_dir = tmp_path / "out_dup"
    src_dir.mkdir()
    _setup_template_and_css(src_dir)
    (src_dir / "index.md").write_text("# Home\n", encoding="utf-8")
    (src_dir / "topic.md").write_text("# Topic MD\n", encoding="utf-8")
    (src_dir / "topic.html").write_text("<h1>Topic HTML</h1>\n", encoding="utf-8")
    (src_dir / "navbar.md").write_text("- [Home](index.md)\n- [Topic](topic.md)\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Duplicate output file detected") as exc_info:
        build_html(input_path=str(src_dir), output_path=str(out_dir))
    assert "/topic.md" in str(exc_info.value)
    assert "/topic.html" in str(exc_info.value)


def test_build_html_directory_missing_index_error(tmp_path) -> None:
    """Test directory build fails when index.md is missing at root."""
    src_dir = tmp_path / "src_no_index"
    out_dir = tmp_path / "out_no_index"
    src_dir.mkdir()
    _setup_template_and_css(src_dir)
    (src_dir / "navbar.md").write_text("- [Topic](topic.md)\n", encoding="utf-8")
    (src_dir / "topic.md").write_text("# Topic\n", encoding="utf-8")

    with pytest.raises(ValueError, match='Directory build requires "index.md" at the root'):
        build_html(input_path=str(src_dir), output_path=str(out_dir))


def test_build_html_directory_missing_navbar_error(tmp_path) -> None:
    """Test directory build fails when navbar.md is missing at root."""
    src_dir = tmp_path / "src_no_navbar"
    out_dir = tmp_path / "out_no_navbar"
    src_dir.mkdir()
    _setup_template_and_css(src_dir)
    (src_dir / "index.md").write_text("# Home\n", encoding="utf-8")

    with pytest.raises(ValueError, match='Directory build requires "navbar.md" at the root'):
        build_html(input_path=str(src_dir), output_path=str(out_dir))


def test_build_html_navbar_broken_link_error(tmp_path) -> None:
    """Test directory build fails with detailed message when navbar.md links to nonexistent file."""
    src_dir = tmp_path / "src_broken_nav"
    out_dir = tmp_path / "out_broken_nav"
    src_dir.mkdir()
    _setup_template_and_css(src_dir)
    (src_dir / "index.md").write_text("# Home\n", encoding="utf-8")
    (src_dir / "navbar.md").write_text(
        "# Navigation\n\n- [Home](index.md)\n- [Ghost Page](nonexistent.md)\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Target file 'nonexistent.md' does not exist"):
        build_html(input_path=str(src_dir), output_path=str(out_dir))


def test_build_html_navbar_external_and_anchor_links(tmp_path) -> None:
    """Test directory build properly handles external URLs and anchor links in navbar.md."""
    src_dir = tmp_path / "src_nav_ext"
    out_dir = tmp_path / "out_nav_ext"
    src_dir.mkdir()
    _setup_template_and_css(src_dir)
    (src_dir / "index.md").write_text("# Home\n", encoding="utf-8")
    (src_dir / "guide.md").write_text("# Guide\n", encoding="utf-8")
    (src_dir / "navbar.md").write_text(
        "# Navigation\n\n"
        "- [Home](index.md)\n"
        "- [Guide Section](guide.md#sec1)\n"
        "## External\n"
        "- [GitHub](https://github.com/example/repo)\n",
        encoding="utf-8",
    )

    res_dir = build_html(input_path=str(src_dir), output_path=str(out_dir))
    assert res_dir == str(out_dir)
    index_html = (out_dir / "index.html").read_text(encoding="utf-8")
    assert 'href="https://github.com/example/repo"' in index_html
    assert 'target="_blank"' in index_html
    assert 'href="guide.html#sec1"' in index_html


def test_build_html_duplicate_block_image_outputs_error(tmp_path) -> None:
    """Test pre-check raises ValueError when two drawlib blocks write to the same image file."""
    _setup_template_and_css(tmp_path)
    doc = tmp_path / "guide.md"
    doc.write_text(
        "# Guide\n```drawlib file:same.png\ncircle((50, 50), 10)\n```\n"
        "```drawlib file:same.png\ncircle((50, 50), 20)\n```\n",
        encoding="utf-8",
    )
    out = tmp_path / "guide.html"

    with pytest.raises(ValueError, match="Duplicate output file detected") as exc_info:
        build_html(input_path=str(doc), output_path=str(out))
    assert "block #1" in str(exc_info.value)
    assert "block #2" in str(exc_info.value)


def test_build_merged_html_filename_order_and_generate_index(tmp_path) -> None:
    """Test directory files merge strictly in filename order and index is placed between 1st and 2nd files."""
    pdf_src = tmp_path / "pdf_src"
    pdf_src.mkdir()
    _setup_template_and_css(pdf_src)
    (pdf_src / "02-install.md").write_text("# 2. Installation\n", encoding="utf-8")
    (pdf_src / "00-cover.md").write_text("# Drawlib Cover\n", encoding="utf-8")
    (pdf_src / "01-about.md").write_text("# 1. About Drawlib\n", encoding="utf-8")

    html, files = build_merged_html([str(pdf_src)], generate_index=True)
    assert [os.path.basename(f) for f in files] == [
        "00-cover.md",
        "01-about.md",
        "02-install.md",
    ]
    pos_cover = html.index('id="chapter-1-00-cover"')
    pos_toc = html.index('<nav class="pdf-toc"')
    pos_about = html.index('id="chapter-2-01-about"')
    pos_install = html.index('id="chapter-3-02-install"')
    assert pos_cover < pos_toc < pos_about < pos_install
    toc_section = html[pos_toc:pos_about]
    assert "Drawlib Cover" not in toc_section
    assert 'href="#chapter-1-00-cover"' not in toc_section
    assert "1. About Drawlib" in toc_section
    assert "2. Installation" in toc_section
    assert "page-break-before: always" in toc_section
    assert "page-break-after: always" in toc_section


def test_build_html_missing_template_error(tmp_path) -> None:
    """Test build_html raises ValueError when template.html is missing."""
    doc = tmp_path / "doc.md"
    doc.write_text("# Hello\n", encoding="utf-8")
    (tmp_path / "style.css").write_text("body {}", encoding="utf-8")
    out = tmp_path / "doc.html"
    with pytest.raises(ValueError, match='Missing required "template.html"'):
        build_html(input_path=str(doc), output_path=str(out))


def test_build_html_missing_style_error(tmp_path) -> None:
    """Test build_html raises ValueError when style.css is missing."""
    doc = tmp_path / "doc.md"
    doc.write_text("# Hello\n", encoding="utf-8")
    (tmp_path / "template.html").write_text("<html><body>{{ body }}</body></html>", encoding="utf-8")
    out = tmp_path / "doc.html"
    with pytest.raises(ValueError, match='Missing required "style.css"'):
        build_html(input_path=str(doc), output_path=str(out))


def test_build_pdf_missing_template_error(tmp_path) -> None:
    """Test build_pdf raises ValueError when template.html is missing."""
    doc = tmp_path / "doc.md"
    doc.write_text("# Hello\n", encoding="utf-8")
    (tmp_path / "style.css").write_text("body {}", encoding="utf-8")
    out = tmp_path / "doc.pdf"
    with pytest.raises(ValueError, match='Missing required "template.html"'):
        build_pdf(inputs=[str(doc)], output_path=str(out))


def test_build_pdf_missing_style_error(tmp_path) -> None:
    """Test build_pdf raises ValueError when style.css is missing."""
    doc = tmp_path / "doc.md"
    doc.write_text("# Hello\n", encoding="utf-8")
    (tmp_path / "template.html").write_text("<html><body>{{ body }}</body></html>", encoding="utf-8")
    out = tmp_path / "doc.pdf"
    with pytest.raises(ValueError, match='Missing required "style.css"'):
        build_pdf(inputs=[str(doc)], output_path=str(out))
