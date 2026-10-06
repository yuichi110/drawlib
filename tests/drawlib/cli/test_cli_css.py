# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

# ruff: noqa: S404, S603

"""Integration tests using subprocess to verify drawlib css and cache CLI subcommands."""

import os

from tests.drawlib.cli.common import run_drawlib_cli


def test_cli_css_list(tmp_path) -> None:
    """Test drawlib css list and target-filtered list subcommands."""
    # Test unified list (both HTML & PDF)
    res_all = run_drawlib_cli(["css", "list"], cwd=str(tmp_path))
    assert res_all.returncode == 0
    assert "default" in res_all.stdout
    assert "google" in res_all.stdout
    assert "HTML" in res_all.stdout
    assert "PDF" in res_all.stdout

    # Test html filtered list
    res_html_list = run_drawlib_cli(["css", "list", "html"], cwd=str(tmp_path))
    assert res_html_list.returncode == 0
    assert "default" in res_html_list.stdout
    assert "default-dark" in res_html_list.stdout
    assert "default-auto" in res_html_list.stdout
    assert "google" in res_html_list.stdout
    assert "google-dark" in res_html_list.stdout
    assert "google-auto" in res_html_list.stdout

    # Test pdf filtered list
    res_pdf_list = run_drawlib_cli(["css", "list", "pdf"], cwd=str(tmp_path))
    assert res_pdf_list.returncode == 0
    assert "default" in res_pdf_list.stdout
    assert "default-dark" in res_pdf_list.stdout
    assert "default-auto" not in res_pdf_list.stdout
    assert "google" in res_pdf_list.stdout
    assert "google-dark" in res_pdf_list.stdout
    assert "google-auto" not in res_pdf_list.stdout


def test_cli_css_show(tmp_path) -> None:
    """Test drawlib css show terminal display and export subcommands."""
    # Test terminal output without -o
    res_term = run_drawlib_cli(["css", "show", "html", "google"], cwd=str(tmp_path))
    assert res_term.returncode == 0
    assert ":root" in res_term.stdout or "color" in res_term.stdout

    # Test convenience syntax defaulting to html
    res_term_default = run_drawlib_cli(["css", "show", "google"], cwd=str(tmp_path))
    assert res_term_default.returncode == 0
    assert ":root" in res_term_default.stdout or "color" in res_term_default.stdout

    # Test export with -o
    out_css = tmp_path / "style.css"
    res_html = run_drawlib_cli(["css", "show", "html", "google", "-o", str(out_css)], cwd=str(tmp_path))
    assert res_html.returncode == 0
    assert "Success" in res_html.stdout
    assert out_css.exists()
    content = out_css.read_text(encoding="utf-8")
    assert len(content) > 100

    # Test failure without --force
    res_fail = run_drawlib_cli(["css", "show", "html", "default", "-o", str(out_css)], cwd=str(tmp_path))
    assert res_fail.returncode != 0
    fail_out = res_fail.stderr + res_fail.stdout
    assert "already" in fail_out and "exists" in fail_out

    # Test success with --force
    res_force = run_drawlib_cli(["css", "show", "html", "default", "-o", str(out_css), "--force"], cwd=str(tmp_path))
    assert res_force.returncode == 0
    assert "Success" in res_force.stdout

    # Test pdf export
    pdf_out = tmp_path / "pdf_style.css"
    res_pdf = run_drawlib_cli(["css", "show", "pdf", "google", "-o", str(pdf_out)], cwd=str(tmp_path))
    assert res_pdf.returncode == 0
    assert "Success" in res_pdf.stdout
    assert pdf_out.exists()

    # Test convenience export with default target
    top_out = tmp_path / "top_style.css"
    res_top = run_drawlib_cli(["css", "show", "minimal", "-o", str(top_out)], cwd=str(tmp_path))
    assert res_top.returncode == 0
    assert "Success" in res_top.stdout
    assert top_out.exists()

    # Test with -l / --lang option
    res_lang = run_drawlib_cli(["css", "show", "google", "--lang", "th"], cwd=str(tmp_path))
    assert res_lang.returncode == 0
    assert "Noto Sans Thai" in res_lang.stdout

    lang_out = tmp_path / "thai.css"
    res_export_lang = run_drawlib_cli(["css", "show", "google", "-l", "th", "-o", str(lang_out)], cwd=str(tmp_path))
    assert res_export_lang.returncode == 0
    assert lang_out.exists()
    assert "Noto Sans Thai" in lang_out.read_text(encoding="utf-8")


def test_cli_cache_list(tmp_path) -> None:
    """Test drawlib cache list subcommand."""
    res = run_drawlib_cli(["cache", "list"], cwd=str(tmp_path))
    assert res.returncode == 0
    assert "Package" in res.stdout or "font" in res.stdout


def test_cli_build_html_with_custom_template(tmp_path) -> None:
    """Test drawlib build html uses template.html and style.css in directory."""
    tmpl = tmp_path / "template.html"
    tmpl.write_text("<html><body class='cli-custom'>{{ body | safe }}</body></html>", encoding="utf-8")
    style = tmp_path / "style.css"
    style.write_text("body { margin: 0; }", encoding="utf-8")

    input_md = tmp_path / "sample.md"
    input_md.write_text("# CLI Custom Template Test", encoding="utf-8")
    out_dir = tmp_path / "out"

    res = run_drawlib_cli(
        ["build", "html", str(tmp_path), "-o", str(out_dir)],
        cwd=str(tmp_path),
    )

    assert res.returncode == 0
    out_html = out_dir / "sample.html"
    assert out_html.exists()
    assert "<body class='cli-custom'>" in out_html.read_text(encoding="utf-8")


def test_cli_build_html_missing_template_error(tmp_path) -> None:
    """Test that build html fails when template.html is missing."""
    style = tmp_path / "style.css"
    style.write_text("body { margin: 0; }", encoding="utf-8")
    input_md = tmp_path / "sample.md"
    input_md.write_text("# Sample", encoding="utf-8")
    out_dir = tmp_path / "out"

    res = run_drawlib_cli(
        ["build", "html", str(tmp_path), "-o", str(out_dir)],
        cwd=str(tmp_path),
    )
    assert res.returncode != 0
    assert 'Missing required "template.html"' in res.stderr
