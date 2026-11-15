# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for tools/dcli/docs."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from typer.testing import CliRunner

from tools.dcli.docs import app
from tools.dcli.docs.banner import detect_portal_id, inject_portal_banners
from tools.dcli.docs.builder import ALL_TARGETS, TARGET_MAP

runner = CliRunner()


def test_docs_cli_help() -> None:
    """Test dcli docs --help."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "build" in result.output
    assert "serve" in result.output


def test_target_definitions() -> None:
    """Test that all targets are properly mapped."""
    assert "site" in TARGET_MAP
    assert "docs" in TARGET_MAP
    assert "doc" in TARGET_MAP
    assert "api" in TARGET_MAP
    assert "architecture" in TARGET_MAP
    assert "reports" in TARGET_MAP
    assert "report" in TARGET_MAP
    assert "readme" in TARGET_MAP
    assert "logo" in TARGET_MAP
    assert "ogp" in TARGET_MAP
    assert "quickstart" in TARGET_MAP
    assert "about-drawlib" in TARGET_MAP
    assert "slide" in TARGET_MAP
    assert "jupyter" in TARGET_MAP
    assert "dogfooding" not in TARGET_MAP
    assert "slide-ddos" not in TARGET_MAP
    assert len(ALL_TARGETS) == 10


def test_docs_build_unknown_target() -> None:
    """Test building an unknown target reports error."""
    result = runner.invoke(app, ["build", "nonexistent_target"])
    assert result.exit_code == 1
    assert "Unknown target" in result.output


def test_docs_build_invocation() -> None:
    """Test build command invokes build_docs correctly."""
    with patch("tools.dcli.docs.cli.build_docs") as mock_build:
        result = runner.invoke(app, ["build", "architecture", "--no-clean"])
        assert result.exit_code == 0
        mock_build.assert_called_once_with(target_name="architecture", build_all=False, clean=False)


def test_docs_build_all_invocation() -> None:
    """Test build --all invokes build_docs correctly."""
    with patch("tools.dcli.docs.cli.build_docs") as mock_build:
        result = runner.invoke(app, ["build", "--all"])
        assert result.exit_code == 0
        mock_build.assert_called_once_with(target_name=None, build_all=True, clean=True)


def test_docs_serve_nonexistent_directory(tmp_path: Path) -> None:
    """Test serve reports error if target directory does not exist."""
    result = runner.invoke(app, ["serve", "nonexistent_dir"])
    assert result.exit_code == 1
    assert "does not exist" in result.output


def test_docs_serve_lab_option(tmp_path: Path) -> None:
    """Test serve --lab invokes JupyterLab via uvx."""
    target_dir = tmp_path / "jupyter_out"
    target_dir.mkdir(parents=True)
    with patch("tools.dcli.docs.cli.run_command") as mock_run:
        result = runner.invoke(app, ["serve", str(target_dir), "--lab", "--no-browser", "-p", "8888"])
        assert result.exit_code == 0
        mock_run.assert_called_once()
        cmd = mock_run.call_args.args[0]
        assert cmd[0] == "uvx"
        assert "jupyterlab" in cmd
        assert "--no-browser" in cmd
        assert "--port=8888" in cmd


def test_detect_portal_id() -> None:
    """Test portal identification from relative path parts."""
    assert detect_portal_id(("index.html",)) == "user_guide"
    assert detect_portal_id(("en", "index.html")) == "user_guide"
    assert detect_portal_id(("api", "en", "index.html")) == "api"
    assert detect_portal_id(("architecture", "en", "index.html")) == "architecture"
    assert detect_portal_id(("quickstart", "ja", "index.html")) == "quickstart"
    assert detect_portal_id(("about-drawlib", "en", "index.html")) == "about-drawlib"
    assert detect_portal_id(("jupyter", "en", "index.html")) == "jupyter"
    assert detect_portal_id(("reports", "pni-full-audit", "index.html")) == "pni501"


def test_inject_portal_banners_idempotent(tmp_path: Path) -> None:
    """Test idempotent banner injection across HTML, CSS, and slide.js files."""
    docs_root = tmp_path / "docs"
    (docs_root / "en").mkdir(parents=True)
    (docs_root / "quickstart" / "ja").mkdir(parents=True)
    (docs_root / "about-drawlib" / "en").mkdir(parents=True)

    # Create sample HTMLs, 404.html, meta-refresh redirect, deliverables, CSS, and slide.js
    (docs_root / "404.html").write_text("<html><body><h1>404</h1></body></html>", encoding="utf-8")
    (docs_root / "about-drawlib" / "index.html").write_text(
        '<html><head><meta http-equiv="refresh" content="0; url=en/index.html"></head><body></body></html>',
        encoding="utf-8",
    )
    (docs_root / "en" / "index.html").write_text(
        '<html lang="en"><body><div class="doc-layout">Hello</div></body></html>',
        encoding="utf-8",
    )
    (docs_root / "quickstart" / "quickstart_ja.pdf").write_bytes(b"%PDF")
    (docs_root / "quickstart" / "quickstart_ja.docx").write_bytes(b"PK")
    (docs_root / "quickstart" / "ja" / "index.html").write_text(
        '<html lang="ja"><body class="doc-body"><main>Quickstart JA</main></body></html>',
        encoding="utf-8",
    )
    (docs_root / "en" / "style.css").write_text("body { margin: 0; }\n", encoding="utf-8")
    (docs_root / "about-drawlib" / "slide.js").write_text(
        "  function updateScale() {\n"
        "    const windowWidth = window.innerWidth;\n"
        "    const windowHeight = window.innerHeight;\n"
        "  }\n"
        "  window.addEventListener('resize', updateScale);\n",
        encoding="utf-8",
    )

    html_count, css_count = inject_portal_banners(docs_root)
    assert html_count == 2
    assert css_count == 1
    assert "demo-banner" not in (docs_root / "404.html").read_text(encoding="utf-8")
    assert "demo-banner" not in (docs_root / "about-drawlib" / "index.html").read_text(encoding="utf-8")

    en_html = (docs_root / "en" / "index.html").read_text(encoding="utf-8")
    assert "<strong>User Guide</strong>" in en_html
    assert 'href="../api/index.html"' in en_html

    qs_ja_html = (docs_root / "quickstart" / "ja" / "index.html").read_text(encoding="utf-8")
    assert "<strong>Quickstart</strong>" in qs_ja_html
    assert 'href="../../ja/index.html"' in qs_ja_html
    assert 'href="../../quickstart/quickstart_ja.pdf">PDF</a>' in qs_ja_html
    assert 'href="../../quickstart/quickstart_ja.docx">DOCX</a>' in qs_ja_html

    slide_js = (docs_root / "about-drawlib" / "slide.js").read_text(encoding="utf-8")
    assert "document.querySelector('.demo-banner')" in slide_js
    assert "fullscreenchange" in slide_js

    # Second run must be 100% idempotent
    inject_portal_banners(docs_root)
    assert (docs_root / "en" / "index.html").read_text(encoding="utf-8") == en_html
    assert (docs_root / "quickstart" / "ja" / "index.html").read_text(encoding="utf-8") == qs_ja_html
    assert (docs_root / "about-drawlib" / "slide.js").read_text(encoding="utf-8") == slide_js

