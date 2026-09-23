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

from drawlib.tools.build import build_html, build_image, build_markdown, build_pdf
from drawlib.tools.cache import clear_cache, download_cache, list_cache
from drawlib.tools.css import export_css, list_css
from drawlib.tools.export import export_code_block
from drawlib.tools.serve import serve_docs
from drawlib.tools.show import show_code_block
from drawlib.tools.template import export_default_template, export_template, list_templates, validate_template


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
    assert callable(list_templates)
    assert callable(export_template)
    assert callable(validate_template)
    assert callable(serve_docs)
    assert callable(show_code_block)
    assert callable(export_code_block)


def test_list_and_export_templates(tmp_path) -> None:
    """Test listing and exporting built-in Jinja2 templates."""
    templates = list_templates()
    names = [t["name"] for t in templates]
    assert "sidebar" in names
    assert "simple" in names

    out_file = tmp_path / "custom_template.html.j2"
    result_path = export_default_template(str(out_file))

    assert os.path.exists(result_path)
    assert out_file.exists()
    content = out_file.read_text(encoding="utf-8")
    assert "{{ body | safe }}" in content or "{{ body }}" in content

    simple_file = tmp_path / "simple_template.html.j2"
    export_template(name="simple", output=str(simple_file))
    assert simple_file.exists()


def test_list_and_export_css(tmp_path) -> None:
    """Test listing and exporting built-in CSS style presets."""
    presets = list_css()
    names = [p["name"] for p in presets]
    assert "default" in names
    assert "google" in names
    assert "github" in names
    assert "minimal" in names
    assert "monochrome" in names

    out_css = tmp_path / "github_theme.css"
    res = export_css(name="github", output=str(out_css))
    assert os.path.exists(res)
    assert out_css.exists()
    assert len(out_css.read_text(encoding="utf-8")) > 0


def test_validate_template_valid(tmp_path) -> None:
    """Test validating a valid template with required body placeholder."""
    tmpl = tmp_path / "valid.html.j2"
    tmpl.write_text("<html><body>{{ body | safe }}</body></html>", encoding="utf-8")

    is_valid, msgs = validate_template(str(tmpl))
    assert is_valid is True
    assert any("is valid" in m for m in msgs)


def test_validate_template_missing_body(tmp_path) -> None:
    """Test validating a template missing the required body placeholder."""
    tmpl = tmp_path / "invalid_body.html.j2"
    tmpl.write_text("<html><body>{{ title }}</body></html>", encoding="utf-8")

    is_valid, msgs = validate_template(str(tmpl))
    assert is_valid is False
    assert any("missing mandatory placeholder 'body'" in m for m in msgs)


def test_validate_template_syntax_error(tmp_path) -> None:
    """Test validating a template with Jinja syntax errors."""
    tmpl = tmp_path / "bad_syntax.html.j2"
    tmpl.write_text("<html><body>{% if true %}{{ body }}{% endfor %}</body></html>", encoding="utf-8")

    is_valid, msgs = validate_template(str(tmpl))
    assert is_valid is False
    assert any("Syntax Error" in m for m in msgs)


def test_build_document_custom_template(tmp_path) -> None:
    """Test compiling document with a custom Jinja2 template."""
    custom_tmpl = tmp_path / "custom.html.j2"
    custom_tmpl.write_text(
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

    input_md = tmp_path / "doc.md"
    input_md.write_text("# Custom Template Page\n\nHello Custom Template!", encoding="utf-8")

    out_html = tmp_path / "doc.html"
    res_path = build_html(input_path=str(input_md), output_path=str(out_html), template_path=str(custom_tmpl))

    assert os.path.exists(res_path)
    content = out_html.read_text(encoding="utf-8")
    assert '<header class="custom-header">My Custom Header</header>' in content
    assert "Hello Custom Template!" in content
