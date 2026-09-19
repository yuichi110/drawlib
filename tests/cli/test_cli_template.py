# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

# ruff: noqa: S404, S603

"""Integration tests using subprocess to verify drawlib template CLI subcommands."""

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


def test_cli_template_export(tmp_path) -> None:
    """Test drawlib template export subcommand."""
    out_file = tmp_path / "exported.html.j2"
    res = run_drawlib_cli(["template", "export", str(out_file)], cwd=str(tmp_path))

    assert res.returncode == 0
    assert "Successfully exported default template" in res.stdout
    assert out_file.exists()


def test_cli_template_validate(tmp_path) -> None:
    """Test drawlib template validate subcommand."""
    tmpl = tmp_path / "valid.html.j2"
    tmpl.write_text("<html><body>{{ body | safe }}</body></html>", encoding="utf-8")

    res = run_drawlib_cli(["template", "validate", str(tmpl)], cwd=str(tmp_path))

    assert res.returncode == 0
    assert "is valid" in res.stdout


def test_cli_build_with_custom_template(tmp_path) -> None:
    """Test drawlib build --template subcommand."""
    tmpl = tmp_path / "custom.html.j2"
    tmpl.write_text("<html><body class='cli-custom'>{{ body | safe }}</body></html>", encoding="utf-8")

    input_md = tmp_path / "sample.md"
    input_md.write_text("# CLI Custom Template Test", encoding="utf-8")
    out_html = tmp_path / "sample.html"

    res = run_drawlib_cli(["build", str(input_md), "-o", str(out_html), "-t", str(tmpl)], cwd=str(tmp_path))

    assert res.returncode == 0
    assert out_html.exists()
    assert "<body class='cli-custom'>" in out_html.read_text(encoding="utf-8")
