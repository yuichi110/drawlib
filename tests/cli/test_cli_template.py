# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

# ruff: noqa: S404, S603

"""Integration tests using subprocess to verify drawlib template, css, and cache CLI subcommands."""

import os
import subprocess
import sys


def run_drawlib_cli(args: list[str], cwd: str) -> subprocess.CompletedProcess[str]:
    """Helper to execute drawlib CLI command via subprocess with current PYTHONPATH."""
    env = os.environ.copy()
    src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src"))
    env["PYTHONPATH"] = src_dir + os.pathsep + env.get("PYTHONPATH", "")

    cmd = [sys.executable, "-m", "drawlib"] + args
    return subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, check=False)


def test_cli_template_list_and_export(tmp_path) -> None:
    """Test drawlib template html/pdf list and export subcommands."""
    res_html_list = run_drawlib_cli(["template", "html", "list"], cwd=str(tmp_path))
    assert res_html_list.returncode == 0
    assert "sidebar" in res_html_list.stdout
    assert "simple" in res_html_list.stdout

    res_pdf_list = run_drawlib_cli(["template", "pdf", "list"], cwd=str(tmp_path))
    assert res_pdf_list.returncode == 0
    assert "default" in res_pdf_list.stdout
    assert "book" in res_pdf_list.stdout

    out_file = tmp_path / "exported.html.j2"
    res = run_drawlib_cli(["template", "html", "export", str(out_file)], cwd=str(tmp_path))
    assert res.returncode == 0
    assert "Successfully exported HTML template" in res.stdout
    assert out_file.exists()

    out_pdf_file = tmp_path / "exported_pdf.html.j2"
    res_pdf = run_drawlib_cli(["template", "pdf", "export", "book", "-o", str(out_pdf_file)], cwd=str(tmp_path))
    assert res_pdf.returncode == 0
    assert "Successfully exported PDF template" in res_pdf.stdout
    assert out_pdf_file.exists()


def test_cli_css_list_and_export(tmp_path) -> None:
    """Test drawlib css html/pdf list and export subcommands."""
    res_html_list = run_drawlib_cli(["css", "html", "list"], cwd=str(tmp_path))
    assert res_html_list.returncode == 0
    assert "default" in res_html_list.stdout
    assert "default-dark" in res_html_list.stdout
    assert "default-auto" in res_html_list.stdout
    assert "google" in res_html_list.stdout
    assert "google-dark" in res_html_list.stdout
    assert "google-auto" in res_html_list.stdout

    res_pdf_list = run_drawlib_cli(["css", "pdf", "list"], cwd=str(tmp_path))
    assert res_pdf_list.returncode == 0
    assert "default" in res_pdf_list.stdout
    assert "default-dark" in res_pdf_list.stdout
    assert "default-auto" not in res_pdf_list.stdout
    assert "google" in res_pdf_list.stdout
    assert "google-dark" in res_pdf_list.stdout
    assert "google-auto" not in res_pdf_list.stdout

    out_css = tmp_path / "exported.css"
    res = run_drawlib_cli(["css", "html", "export", str(out_css), "-n", "github"], cwd=str(tmp_path))
    assert res.returncode == 0
    assert "Successfully exported HTML CSS" in res.stdout
    assert out_css.exists()

    out_pdf_css = tmp_path / "exported_pdf.css"
    res_pdf = run_drawlib_cli(["css", "pdf", "export", str(out_pdf_css), "-n", "google"], cwd=str(tmp_path))
    assert res_pdf.returncode == 0
    assert "Successfully exported PDF CSS" in res_pdf.stdout
    assert out_pdf_css.exists()

    # Reject auto preset in PDF export CLI
    res_err = run_drawlib_cli(
        ["css", "pdf", "export", str(tmp_path / "err.css"), "-n", "default-auto"],
        cwd=str(tmp_path),
    )
    assert res_err.returncode != 0


def test_cli_cache_list(tmp_path) -> None:
    """Test drawlib cache list subcommand."""
    res = run_drawlib_cli(["cache", "list"], cwd=str(tmp_path))
    assert res.returncode == 0
    assert "Package" in res.stdout or "font" in res.stdout


def test_cli_template_validate(tmp_path) -> None:
    """Test drawlib template html/pdf validate subcommands."""
    tmpl = tmp_path / "valid.html.j2"
    tmpl.write_text("<html><body>{{ body | safe }}</body></html>", encoding="utf-8")

    res_html = run_drawlib_cli(["template", "html", "validate", str(tmpl)], cwd=str(tmp_path))
    assert res_html.returncode == 0
    assert "is valid" in res_html.stdout

    res_pdf = run_drawlib_cli(["template", "pdf", "validate", str(tmpl)], cwd=str(tmp_path))
    assert res_pdf.returncode == 0
    assert "is valid" in res_pdf.stdout


def test_cli_build_html_with_custom_template(tmp_path) -> None:
    """Test drawlib build html --template subcommand."""
    tmpl = tmp_path / "custom.html.j2"
    tmpl.write_text("<html><body class='cli-custom'>{{ body | safe }}</body></html>", encoding="utf-8")

    input_md = tmp_path / "sample.md"
    input_md.write_text("# CLI Custom Template Test", encoding="utf-8")
    out_html = tmp_path / "sample.html"

    res = run_drawlib_cli(
        ["build", "html", str(input_md), "-o", str(out_html), "-t", str(tmpl)],
        cwd=str(tmp_path),
    )

    assert res.returncode == 0
    assert out_html.exists()
    assert "<body class='cli-custom'>" in out_html.read_text(encoding="utf-8")
