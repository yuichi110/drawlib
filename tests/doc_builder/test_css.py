# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for template, CSS, and drawlib.tools public API facade."""

import os

import pytest

from drawlib.tools import (
    build_html,
    build_image,
    build_markdown,
    build_pdf,
    clear_cache,
    download_cache,
    export_block,
    export_code_block,
    export_css,
    get_css,
    init_project,
    list_cache,
    list_css,
    serve_docs,
    show_block,
    show_code_block,
)


def test_public_tools_facade_exports() -> None:
    """Verify all drawlib.tools public facade functions are callable."""
    assert callable(build_image)
    assert callable(build_markdown)
    assert callable(build_html)
    assert callable(build_pdf)
    assert callable(clear_cache)
    assert callable(list_cache)
    assert callable(download_cache)
    assert callable(list_css)
    assert callable(export_css)
    assert callable(get_css)
    assert callable(serve_docs)
    assert callable(show_code_block)
    assert callable(show_block)
    assert callable(export_code_block)
    assert callable(export_block)
    assert callable(init_project)


def test_list_css() -> None:
    """Test listing built-in HTML and PDF CSS style presets."""
    html_presets = list_css(target="html")
    html_names = [p["name"] for p in html_presets]
    assert "default" in html_names
    assert "default-dark" in html_names
    assert "default-auto" in html_names
    assert "google" in html_names
    assert "google-dark" in html_names
    assert "google-auto" in html_names
    assert "github" in html_names
    assert "minimal" in html_names
    assert "monochrome" in html_names

    pdf_presets = list_css(target="pdf")
    pdf_names = [p["name"] for p in pdf_presets]
    assert "default" in pdf_names
    assert "default-dark" in pdf_names
    assert "default-auto" not in pdf_names
    assert "google" in pdf_names
    assert "google-dark" in pdf_names
    assert "google-auto" not in pdf_names
    assert "github" in pdf_names
    assert "minimal" in pdf_names
    assert "monochrome" in pdf_names


def test_get_and_export_css(tmp_path) -> None:
    """Test get_css and export_css functionality."""
    html_css = get_css("google", target="html")
    assert len(html_css) > 100
    assert "google" in html_css.lower() or "font" in html_css.lower()

    pdf_css = get_css("google", target="pdf")
    assert len(pdf_css) > 100

    # Test export
    out_file = tmp_path / "style.css"
    exported = export_css("google", str(out_file), target="html")
    assert os.path.exists(exported)
    assert out_file.read_text(encoding="utf-8") == html_css

    # Test without force raises FileExistsError
    with pytest.raises(FileExistsError):
        export_css("default", str(out_file), target="html", force=False)

    # Test with force overwrites
    export_css("default", str(out_file), target="html", force=True)
    assert out_file.read_text(encoding="utf-8") != html_css


def test_build_document_custom_template(tmp_path) -> None:
    """Test compiling document with custom template.html and style.css in the directory."""
    tmpl = tmp_path / "template.html"
    tmpl.write_text(
        """<!DOCTYPE html>
<html>
<head><title>{{ title }}</title></head>
<body>
    <header class="custom-header">My Custom Header</header>
    <main>{{ body | safe }}</main>
</body>
</html>""",
        encoding="utf-8",
    )
    style = tmp_path / "style.css"
    style.write_text("body { margin: 0; }", encoding="utf-8")

    input_md = tmp_path / "doc.md"
    input_md.write_text("# Custom Template Page\n\nHello Custom Template!", encoding="utf-8")

    out_html = tmp_path / "doc.html"
    res_path = build_html(input_path=str(input_md), output_path=str(out_html))

    assert os.path.exists(res_path)
    content = out_html.read_text(encoding="utf-8")
    assert '<header class="custom-header">My Custom Header</header>' in content
    assert "Hello Custom Template!" in content
