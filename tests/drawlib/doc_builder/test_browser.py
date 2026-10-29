# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for shared Playwright headless Chromium launcher and auto-installer."""

from __future__ import annotations

import subprocess  # noqa: S404
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from drawlib._builder._common.browser import (
    install_headless_chromium,
    launch_headless_chromium,
)
from drawlib._builder._common.cache_manager import download_cache
from drawlib._builder.doc_builder.exporter_pdf import (
    export_html_file_to_pdf,
    export_html_to_pdf,
)
from tests.drawlib.cli.common import run_drawlib_cli


def test_launch_headless_chromium_already_installed(monkeypatch) -> None:
    """Verify browser launches immediately with zero installer calls when Chromium is already present."""
    mock_install = MagicMock()
    monkeypatch.setattr("drawlib._builder._common.browser.install_headless_chromium", mock_install)

    mock_p = MagicMock()
    mock_browser = MagicMock()
    mock_p.chromium.launch.return_value = mock_browser

    res = launch_headless_chromium(mock_p)
    assert res is mock_browser
    mock_install.assert_not_called()
    mock_p.chromium.launch.assert_called_once_with(
        headless=True,
        args=["--font-render-hinting=medium", "--enable-font-antialiasing"],
    )


def test_launch_headless_chromium_auto_installs_and_retries(monkeypatch) -> None:
    """Verify missing executable triggers on-demand install and retries browser launch."""
    mock_install = MagicMock()
    monkeypatch.setattr("drawlib._builder._common.browser.install_headless_chromium", mock_install)

    mock_p = MagicMock()
    mock_browser = MagicMock()
    mock_p.chromium.launch.side_effect = [
        Exception("BrowserType.launch: Executable doesn't exist at /cache/headless_shell"),
        mock_browser,
    ]

    res = launch_headless_chromium(mock_p, context_label="PDF Export")
    assert res is mock_browser
    mock_install.assert_called_once_with(context_label="PDF Export")
    assert mock_p.chromium.launch.call_count == 2


def test_launch_headless_chromium_auto_install_disabled(monkeypatch) -> None:
    """Verify auto_install=False raises RuntimeError without invoking installer."""
    mock_install = MagicMock()
    monkeypatch.setattr("drawlib._builder._common.browser.install_headless_chromium", mock_install)

    mock_p = MagicMock()
    mock_p.chromium.launch.side_effect = Exception("Executable doesn't exist at /cache/headless_shell")

    with pytest.raises(RuntimeError) as exc_info:
        launch_headless_chromium(mock_p, auto_install=False)

    mock_install.assert_not_called()
    assert "drawlib cache download --browser" in str(exc_info.value)


@pytest.mark.parametrize(
    "sys_err_msg",
    [
        "Host system is missing dependencies to run browsers.",
        "error while loading shared libraries: libnss3.so: cannot open shared object file",
        "Please run: sudo playwright install-deps",
    ],
)
def test_launch_headless_chromium_missing_system_deps_error(monkeypatch, sys_err_msg: str) -> None:
    """Verify missing Linux OS shared libraries emit CI/container instructions without running installer."""
    mock_install = MagicMock()
    monkeypatch.setattr("drawlib._builder._common.browser.install_headless_chromium", mock_install)

    mock_p = MagicMock()
    mock_p.chromium.launch.side_effect = Exception(sys_err_msg)

    with pytest.raises(RuntimeError) as exc_info:
        launch_headless_chromium(mock_p, context_label="PDF Export")

    mock_install.assert_not_called()
    err_msg = str(exc_info.value)
    assert "required OS shared libraries are missing" in err_msg
    assert "playwright install --with-deps chromium" in err_msg
    assert "playwright install-deps chromium" in err_msg


def test_launch_headless_chromium_missing_system_deps_after_auto_install(monkeypatch) -> None:
    """Verify minimal Linux container missing OS libs after first-time download surfaces --with-deps guide."""
    mock_install = MagicMock()
    monkeypatch.setattr("drawlib._builder._common.browser.install_headless_chromium", mock_install)

    mock_p = MagicMock()
    mock_p.chromium.launch.side_effect = [
        Exception("Executable doesn't exist at /root/.cache/ms-playwright/headless_shell"),
        Exception("Host system is missing dependencies to run browsers."),
    ]

    with pytest.raises(RuntimeError) as exc_info:
        launch_headless_chromium(mock_p, context_label="PDF Export")

    mock_install.assert_called_once_with(context_label="PDF Export")
    err_msg = str(exc_info.value)
    assert "required OS shared libraries are missing" in err_msg
    assert "playwright install --with-deps chromium" in err_msg


def test_install_headless_chromium_invokes_bundled_driver(monkeypatch, tmp_path: Path) -> None:
    """Verify install_headless_chromium invokes Playwright's internal driver with --only-shell chromium."""
    fake_node = tmp_path / "node"
    fake_cli = tmp_path / "cli.js"
    fake_node.write_text("#!/bin/sh\n", encoding="utf-8")
    fake_cli.write_text("// cli\n", encoding="utf-8")

    browsers_dir = tmp_path / "pw-browsers"
    monkeypatch.setenv("PLAYWRIGHT_BROWSERS_PATH", str(browsers_dir))
    monkeypatch.setattr(
        "playwright._impl._driver.compute_driver_executable",
        lambda: (str(fake_node), str(fake_cli)),
    )
    monkeypatch.setattr(
        "playwright._impl._driver.get_driver_env",
        lambda: {"PW_LANG_NAME": "python"},
    )

    mock_run = MagicMock(return_value=subprocess.CompletedProcess(args=[], returncode=0, stdout="ok", stderr=""))
    monkeypatch.setattr("drawlib._builder._common.browser.subprocess.run", mock_run)

    install_headless_chromium()

    mock_run.assert_called_once()
    call_args, call_kwargs = mock_run.call_args
    assert call_args[0] == [
        str(fake_node.resolve()),
        str(fake_cli.resolve()),
        "install",
        "--only-shell",
        "chromium",
    ]
    assert call_kwargs["env"] == {"PW_LANG_NAME": "python"}
    assert call_kwargs["check"] is False
    assert (browsers_dir / ".drawlib_browser_install.lock").is_file()


def test_install_headless_chromium_driver_failure_raises_runtime_error(monkeypatch, tmp_path: Path) -> None:
    """Verify non-zero exit from Playwright driver raises actionable RuntimeError."""
    fake_node = tmp_path / "node"
    fake_cli = tmp_path / "cli.js"
    fake_node.write_text("#!/bin/sh\n", encoding="utf-8")
    fake_cli.write_text("// cli\n", encoding="utf-8")

    monkeypatch.setenv("PLAYWRIGHT_BROWSERS_PATH", str(tmp_path / "pw-browsers"))
    monkeypatch.setattr(
        "playwright._impl._driver.compute_driver_executable",
        lambda: (str(fake_node), str(fake_cli)),
    )
    monkeypatch.setattr("playwright._impl._driver.get_driver_env", lambda: {})

    mock_run = MagicMock(
        return_value=subprocess.CompletedProcess(
            args=[],
            returncode=1,
            stdout="",
            stderr="Download failed: ENOTFOUND cdn.playwright.dev",
        )
    )
    monkeypatch.setattr("drawlib._builder._common.browser.subprocess.run", mock_run)

    with pytest.raises(RuntimeError) as exc_info:
        install_headless_chromium(context_label="PDF Export")

    err_msg = str(exc_info.value)
    assert "[PDF Export Error]" in err_msg
    assert "ENOTFOUND cdn.playwright.dev" in err_msg
    assert "drawlib cache download --browser" in err_msg


def test_export_pdf_functions_succeed_after_auto_install(monkeypatch, tmp_path: Path) -> None:
    """Verify both export_html_to_pdf and export_html_file_to_pdf recover via auto-install."""
    mock_install = MagicMock()
    monkeypatch.setattr("drawlib._builder._common.browser.install_headless_chromium", mock_install)

    def _make_mock_browser() -> MagicMock:
        mock_browser = MagicMock()
        mock_page = MagicMock()

        def _fake_pdf(**kwargs) -> None:
            Path(kwargs["path"]).write_bytes(b"%PDF-1.4\n/CreationDate (D:20261029000000+00'00')\n%%EOF")

        mock_page.pdf.side_effect = _fake_pdf
        mock_browser.new_page.return_value = mock_page
        return mock_browser

    mock_playwright = MagicMock()
    mock_p = MagicMock()
    mock_playwright.return_value.__enter__.return_value = mock_p
    mock_p.chromium.launch.side_effect = [
        Exception("Executable doesn't exist"),
        _make_mock_browser(),
        Exception("Executable doesn't exist"),
        _make_mock_browser(),
    ]
    monkeypatch.setattr("playwright.sync_api.sync_playwright", mock_playwright)

    out1 = tmp_path / "mem.pdf"
    export_html_to_pdf("<h1>Hello</h1>", str(out1))
    assert out1.is_file()
    assert b"D:20260101000000+00'00'" in out1.read_bytes()

    html_file = tmp_path / "in.html"
    html_file.write_text("<h1>File</h1>", encoding="utf-8")
    out2 = tmp_path / "file.pdf"
    export_html_file_to_pdf(str(html_file), str(out2))
    assert out2.is_file()
    assert mock_install.call_count == 2


def test_download_cache_browser_routing(monkeypatch) -> None:
    """Verify download_cache routes --browser, category flags, and --all properly."""
    mock_assets = MagicMock()
    mock_fonts = MagicMock()
    mock_icons = MagicMock()
    mock_maps = MagicMock()
    mock_browser = MagicMock()

    monkeypatch.setattr("drawlib._builder._common.cache_manager.download_all_assets", mock_assets)
    monkeypatch.setattr("drawlib._builder._common.cache_manager.download_all_fonts", mock_fonts)
    monkeypatch.setattr("drawlib._builder._common.cache_manager.download_all_icons", mock_icons)
    monkeypatch.setattr("drawlib._builder._common.cache_manager.download_all_maps", mock_maps)
    monkeypatch.setattr("drawlib._builder._common.cache_manager.install_headless_chromium", mock_browser)

    # --browser only
    download_cache(browser=True)
    mock_browser.assert_called_once_with(context_label="Cache Download")
    mock_assets.assert_not_called()
    mock_fonts.assert_not_called()

    mock_browser.reset_mock()

    # --fonts only (should NOT download browser)
    download_cache(fonts=True)
    mock_fonts.assert_called_once()
    mock_browser.assert_not_called()
    mock_assets.assert_not_called()

    mock_fonts.reset_mock()

    # --all (default) downloads both release assets and headless browser
    download_cache(all_assets=True)
    mock_assets.assert_called_once()
    mock_browser.assert_called_once_with(context_label="Cache Download")


def test_cli_cache_download_help_exposes_browser_option(tmp_path: Path) -> None:
    """Verify `drawlib cache download --help` lists the --browser option."""
    res = run_drawlib_cli(["cache", "download", "--help"], cwd=str(tmp_path))
    assert res.returncode == 0
    assert "--browser" in res.stdout
