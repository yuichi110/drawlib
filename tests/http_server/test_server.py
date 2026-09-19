# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for http_server module."""

import threading
import time
import urllib.request

import pytest

from drawlib._tools.http_server.server import run_server


def test_run_server_invalid_directory() -> None:
    """Test that run_server raises ValueError if target directory does not exist."""
    with pytest.raises(ValueError, match="does not exist"):
        run_server(directory="/path/that/does/not/exist/drawlib_test", port=9999, open_browser=False)


def test_run_server_serves_files(tmp_path) -> None:
    """Test that run_server serves files correctly over HTTP."""
    (tmp_path / "index.html").write_text("<h1>Server Test Page</h1>", encoding="utf-8")

    port = 8877
    server_thread = threading.Thread(
        target=run_server,
        kwargs={"directory": str(tmp_path), "port": port, "open_browser": False},
        daemon=True,
    )
    server_thread.start()
    time.sleep(0.4)

    url = f"http://localhost:{port}/index.html"
    with urllib.request.urlopen(url) as response:
        assert response.status == 200
        content = response.read().decode("utf-8")
        assert "<h1>Server Test Page</h1>" in content
