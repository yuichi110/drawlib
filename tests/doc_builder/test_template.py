# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for template export, validation, and custom HTML template rendering."""

import os

from drawlib._tools.doc_builder import build_document, export_default_template, validate_template


def test_export_default_template(tmp_path) -> None:
    """Test exporting default template to a file."""
    out_file = tmp_path / "custom_template.html.j2"
    result_path = export_default_template(str(out_file))

    assert os.path.exists(result_path)
    assert out_file.exists()
    content = out_file.read_text(encoding="utf-8")
    assert "{{ body | safe }}" in content or "{{ body }}" in content


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
    res_path = build_document(input_path=str(input_md), output_path=str(out_html), template_path=str(custom_tmpl))

    assert os.path.exists(res_path)
    content = out_html.read_text(encoding="utf-8")
    assert '<header class="custom-header">My Custom Header</header>' in content
    assert "Hello Custom Template!" in content
