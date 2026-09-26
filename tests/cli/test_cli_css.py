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
import subprocess
import sys


def run_drawlib_cli(args: list[str], cwd: str) -> subprocess.CompletedProcess[str]:
    """Helper to execute drawlib CLI command via subprocess with current PYTHONPATH."""
    env = os.environ.copy()
    src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src"))
    env["PYTHONPATH"] = src_dir + os.pathsep + env.get("PYTHONPATH", "")

    cmd = [sys.executable, "-m", "drawlib"] + args
    return subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, check=False)


def test_cli_css_list(tmp_path) -> None:
    """Test drawlib css html/pdf list subcommands."""
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


def test_cli_css_export(tmp_path) -> None:
    """Test drawlib css html/pdf export subcommands."""
    out_css = tmp_path / "style.css"
    res_html = run_drawlib_cli(["css", "html", "export", "google", "-o", str(out_css)], cwd=str(tmp_path))
    assert res_html.returncode == 0
    assert "Success" in res_html.stdout
    assert out_css.exists()
    content = out_css.read_text(encoding="utf-8")
    assert len(content) > 100

    # Test failure without --force
    res_fail = run_drawlib_cli(["css", "html", "export", "default", "-o", str(out_css)], cwd=str(tmp_path))
    assert res_fail.returncode != 0
    fail_out = res_fail.stderr + res_fail.stdout
    assert "already" in fail_out and "exists" in fail_out

    # Test success with --force
    res_force = run_drawlib_cli(["css", "html", "export", "default", "-o", str(out_css), "--force"], cwd=str(tmp_path))
    assert res_force.returncode == 0
    assert "Success" in res_force.stdout

    # Test pdf export
    pdf_out = tmp_path / "pdf_style.css"
    res_pdf = run_drawlib_cli(["css", "pdf", "export", "google", "-o", str(pdf_out)], cwd=str(tmp_path))
    assert res_pdf.returncode == 0
    assert "Success" in res_pdf.stdout
    assert pdf_out.exists()

    # Test top-level css export
    top_out = tmp_path / "top_style.css"
    res_top = run_drawlib_cli(["css", "export", "minimal", "-o", str(top_out)], cwd=str(tmp_path))
    assert res_top.returncode == 0
    assert "Success" in res_top.stdout
    assert top_out.exists()


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
    out_html = tmp_path / "sample.html"

    res = run_drawlib_cli(
        ["build", "html", str(input_md), "-o", str(out_html)],
        cwd=str(tmp_path),
    )

    assert res.returncode == 0
    assert out_html.exists()
    assert "<body class='cli-custom'>" in out_html.read_text(encoding="utf-8")


def test_cli_build_html_missing_template_error(tmp_path) -> None:
    """Test that build html fails when template.html is missing."""
    style = tmp_path / "style.css"
    style.write_text("body { margin: 0; }", encoding="utf-8")
    input_md = tmp_path / "sample.md"
    input_md.write_text("# Sample", encoding="utf-8")
    out_html = tmp_path / "sample.html"

    res = run_drawlib_cli(
        ["build", "html", str(input_md), "-o", str(out_html)],
        cwd=str(tmp_path),
    )
    assert res.returncode != 0
    assert 'Missing required "template.html"' in res.stderr
