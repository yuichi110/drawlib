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
import subprocess
import sys
import time
import urllib.request


def test_cli_serve_command(tmp_path) -> None:
    """Test drawlib serve subcommand via subprocess."""
    doc_dir = tmp_path / "docs" / "html"
    doc_dir.mkdir(parents=True)
    (doc_dir / "index.html").write_text("<h1>CLI Serve Integration Test</h1>", encoding="utf-8")

    port = 8995
    cmd = [
        sys.executable,
        "-m",
        "drawlib",
        "serve",
        str(doc_dir),
        "-p",
        str(port),
        "--no-browser",
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
        for _ in range(10):
            try:
                resp = urllib.request.urlopen(url, timeout=3)
                break
            except Exception:
                time.sleep(0.3)
        assert resp is not None, "Failed to connect to CLI serve HTTP server"
        with resp:
            assert resp.status == 200
            body = resp.read().decode("utf-8")
            assert "<h1>CLI Serve Integration Test</h1>" in body
    finally:

        proc.terminate()
        proc.wait(timeout=2)
