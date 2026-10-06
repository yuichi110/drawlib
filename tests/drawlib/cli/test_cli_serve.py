# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

# ruff: noqa: S404, S603, S310

"""Integration tests using subprocess to verify drawlib CLI serve command."""

import os
import socket
import subprocess
import sys
import time
import urllib.request

from tests.drawlib.cli.common import run_drawlib_cli


def test_cli_serve_command(tmp_path) -> None:
    """Test drawlib serve subcommand via subprocess."""
    doc_dir = tmp_path / "docs" / "html"
    doc_dir.mkdir(parents=True)
    (doc_dir / "index.html").write_text("<h1>CLI Serve Integration Test</h1>", encoding="utf-8")

    with socket.socket() as s:
        s.bind(("", 0))
        port = s.getsockname()[1]

    cmd = [
        sys.executable,
        "-m",
        "drawlib",
        "serve",
        str(doc_dir),
        "-p",
        str(port),
        "--no-browser",
        "--skip-check",
    ]
    env = os.environ.copy()
    src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src"))
    env["PYTHONPATH"] = src_dir + os.pathsep + env.get("PYTHONPATH", "")

    proc = subprocess.Popen(
        cmd,
        cwd=str(tmp_path),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    try:
        url = f"http://localhost:{port}/index.html"
        resp = None
        for _ in range(150):
            try:
                resp = urllib.request.urlopen(url, timeout=3)
                break
            except Exception:
                time.sleep(0.1)
        if resp is None:
            _, err = proc.communicate(timeout=2)
            raise AssertionError(f"Failed to connect to CLI serve HTTP server on port {port}. Stderr: {err}")
        with resp:
            assert resp.status == 200
            body = resp.read().decode("utf-8")
            assert "<h1>CLI Serve Integration Test</h1>" in body
    finally:
        proc.terminate()
        proc.wait(timeout=2)


def test_cli_serve_missing_directory_fails() -> None:
    """Test that `drawlib serve` without directory argument fails with non-zero exit code."""
    res = run_drawlib_cli(["serve"])
    assert res.exit_code != 0
    output = res.stdout + res.stderr
    assert "Missing argument" in output or "DIRECTORY" in output


def test_cli_serve_invalid_directory_fails() -> None:
    """Test that `drawlib serve <nonexistent>` fails with exit code 1."""
    res = run_drawlib_cli(["serve", "/path/that/does/not/exist/drawlib_preview"])
    assert res.exit_code == 1
    output = res.stdout + res.stderr
    assert "does not exist" in output


def test_cli_serve_check_flag(tmp_path) -> None:
    """Test `drawlib serve <directory> --check` validates links and exits without starting server."""
    doc_dir = tmp_path / "html"
    doc_dir.mkdir()
    (doc_dir / "index.html").write_text("<h1>Valid Docs</h1>", encoding="utf-8")

    res = run_drawlib_cli(["serve", str(doc_dir), "--check"])
    assert res.exit_code == 0
    assert "Verified 1 HTML file(s)" in (res.stdout + res.stderr)
