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
import urllib.error
import urllib.request

import pytest

from drawlib._http_server import scan_broken_links, serve_docs


def test_serve_docs_invalid_directory() -> None:
    """Test that serve_docs raises ValueError if target directory does not exist."""
    with pytest.raises(ValueError, match="does not exist"):
        serve_docs(directory="/path/that/does/not/exist/drawlib_test", port=9999, open_browser=False)


def test_serve_docs_path_is_file(tmp_path) -> None:
    """Test that serve_docs raises ValueError if target path is a file, not a directory."""
    file_path = tmp_path / "test.html"
    file_path.write_text("<h1>Hello</h1>", encoding="utf-8")
    with pytest.raises(ValueError, match="is a file, not a directory"):
        serve_docs(directory=str(file_path), port=9999, open_browser=False)


def test_serve_docs_serves_files(tmp_path) -> None:
    """Test that serve_docs serves files correctly over HTTP."""
    (tmp_path / "index.html").write_text("<h1>Server Test Page</h1>", encoding="utf-8")

    port = 8877
    server_thread = threading.Thread(
        target=serve_docs,
        kwargs={"directory": str(tmp_path), "port": port, "open_browser": False},
        daemon=True,
    )
    server_thread.start()

    url = f"http://127.0.0.1:{port}/index.html"
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    last_err: Exception | None = None
    for _ in range(30):
        try:
            with opener.open(url, timeout=2.0) as response:
                assert response.status == 200
                content = response.read().decode("utf-8")
                assert "<h1>Server Test Page</h1>" in content
                last_err = None
                break
        except urllib.error.URLError as e:
            last_err = e
            time.sleep(0.2)
    if last_err is not None:
        raise last_err


def test_scan_broken_links(tmp_path) -> None:
    """Test scan_broken_links identifies broken local links and ignores valid/external ones."""
    # Create directory structure with valid and broken references
    (tmp_path / "valid.png").write_bytes(b"png")
    (tmp_path / "style.css").write_text("body {}", encoding="utf-8")
    (tmp_path / "other.html").write_text("<p>Hello</p>", encoding="utf-8")

    index_html = tmp_path / "index.html"
    index_html.write_text(
        """<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="style.css">
    <link rel="stylesheet" href="missing.css">
</head>
<body>
    <a href="other.html">Valid</a>
    <a href="nonexistent.html">Broken</a>
    <a href="https://example.com">External</a>
    <a href="#section">Fragment</a>
    <img src="valid.png" alt="Valid Image">
    <img src="broken.png" alt="Broken Image">
</body>
</html>""",
        encoding="utf-8",
    )

    total_files, total_links, broken = scan_broken_links(str(tmp_path))
    assert total_files == 2
    assert total_links == 6  # style.css, missing.css, other.html, nonexistent.html, valid.png, broken.png
    assert len(broken) == 3  # missing.css, nonexistent.html, broken.png
    broken_targets = {target for _, _, target in broken}
    assert "nonexistent.html" in broken_targets
    assert "broken.png" in broken_targets
    assert "missing.css" in broken_targets


def test_serve_docs_check_only_success(tmp_path, capsys) -> None:
    """Test serve_docs with check_only=True and no broken links exits cleanly."""
    (tmp_path / "index.html").write_text("<html><body>Hello</body></html>", encoding="utf-8")

    with pytest.raises(SystemExit) as exc_info:
        serve_docs(directory=str(tmp_path), open_browser=False, check_only=True)

    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert "[Link Check] Verified 1 HTML file(s)" in captured.out


def test_serve_docs_check_only_broken_links(tmp_path, capsys) -> None:
    """Test serve_docs with check_only=True and broken links exits with code 1."""
    (tmp_path / "index.html").write_text('<a href="missing.html">Broken</a>', encoding="utf-8")

    with pytest.raises(SystemExit) as exc_info:
        serve_docs(directory=str(tmp_path), open_browser=False, check_only=True)

    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "Found 1 broken link(s)" in captured.err
