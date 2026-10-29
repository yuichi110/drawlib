# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Shared Playwright headless Chromium launcher and on-demand installer."""

from __future__ import annotations

import contextlib
import os
import subprocess  # noqa: S404
import sys
import tempfile
import threading
from collections.abc import Callable, Iterator, Sequence
from pathlib import Path
from typing import TYPE_CHECKING, Final

from drawlib._core.l1_core import logger

if TYPE_CHECKING:
    from playwright.sync_api import Browser, Playwright, PlaywrightContextManager

_INSTALL_ARGS: Final[tuple[str, ...]] = ("install", "--only-shell", "chromium")
_DEFAULT_CHROMIUM_ARGS: Final[tuple[str, ...]] = (
    "--font-render-hinting=medium",
    "--enable-font-antialiasing",
)
_INSTALL_THREAD_LOCK = threading.Lock()


def _resolve_lock_file_paths() -> list[Path]:
    """Return candidate per-user lock file paths in priority order."""
    candidates: list[Path] = []
    browsers_path = os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "").strip()
    if browsers_path and browsers_path != "0":
        candidates.append(Path(browsers_path).expanduser() / ".drawlib_browser_install.lock")

    if sys.platform == "win32":
        local_app_data = os.environ.get("LOCALAPPDATA", str(Path.home()))
        candidates.append(Path(local_app_data) / "drawlib" / "playwright_install.lock")
    else:
        xdg_cache = os.environ.get("XDG_CACHE_HOME", str(Path.home() / ".cache"))
        candidates.append(Path(xdg_cache) / "drawlib" / "playwright_install.lock")

    uid_suffix = str(os.getuid()) if hasattr(os, "getuid") else "user"
    candidates.append(Path(tempfile.gettempdir()) / f"drawlib_{uid_suffix}" / "playwright_install.lock")
    return candidates


@contextlib.contextmanager
def _browser_install_lock() -> Iterator[None]:
    """Serialize concurrent headless Chromium downloads across threads and processes."""
    with _INSTALL_THREAD_LOCK:
        lock_handle = None
        for lock_path in _resolve_lock_file_paths():
            try:
                lock_path.parent.mkdir(parents=True, exist_ok=True)
                lock_handle = lock_path.open("a+", encoding="utf-8")
                break
            except OSError:
                continue

        if lock_handle is None:
            yield
            return

        locked = False
        try:
            with contextlib.suppress(ImportError, OSError):
                import fcntl

                fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX)
                locked = True
            yield
        finally:
            if locked:
                with contextlib.suppress(ImportError, OSError):
                    import fcntl

                    fcntl.flock(lock_handle.fileno(), fcntl.LOCK_UN)
            with contextlib.suppress(OSError):
                lock_handle.close()


def _is_missing_browser_executable_error(err: BaseException) -> bool:
    """Return True if Playwright failed because the browser binary is not downloaded yet."""
    err_lower = str(err).lower()
    return (
        "executable doesn't exist" in err_lower
        or "looks like playwright was just installed or updated" in err_lower
    )


def _is_missing_system_deps_error(err: BaseException) -> bool:
    """Return True if Chromium failed due to missing Linux OS shared libraries."""
    err_lower = str(err).lower()
    return any(
        marker in err_lower
        for marker in (
            "host system is missing dependencies",
            "error while loading shared libraries",
            "cannot open shared object file",
            "install-deps",
        )
    )


def _format_missing_playwright_error(context_label: str) -> str:
    """Format an actionable error message when the playwright Python package is missing."""
    return (
        f"\n[{context_label} Error]\n"
        f"{context_label} requires the 'playwright' package.\n\n"
        "Reinstall drawlib or install Playwright:\n"
        "  - For uv users:\n"
        "      uv sync\n"
        "    (or: uv add playwright)\n\n"
        "  - For pip users:\n"
        "      pip install drawlib\n"
        "    (or: pip install playwright)\n"
    )


def _format_missing_system_deps_error(context_label: str, err: BaseException) -> str:
    """Format an actionable error message for CI / minimal Linux containers missing OS libraries."""
    return (
        f"\n[{context_label} Error]\n"
        "Headless Chromium could not start because required OS shared libraries are missing\n"
        "(common in minimal Linux containers and CI pipelines).\n\n"
        "Install the required system dependencies (requires root/sudo privileges):\n"
        "  - For uv users:\n"
        "      uv run playwright install --with-deps chromium\n"
        "    (or OS libraries only: uv run playwright install-deps chromium)\n\n"
        "  - For pip / Docker users:\n"
        "      playwright install --with-deps chromium\n"
        "    (or OS libraries only: playwright install-deps chromium)\n\n"
        f"Details:\n{err}"
    )


def _format_missing_browser_error(context_label: str, detail: str = "") -> str:
    """Format an actionable error message when headless Chromium cannot be downloaded."""
    extra = f"\nDetails:\n{detail}\n" if detail else ""
    return (
        f"\n[{context_label} Error]\n"
        "Headless Chromium browser is not installed and could not be downloaded automatically.\n\n"
        "To pre-download headless Chromium manually, run:\n"
        "  - Via drawlib CLI:\n"
        "      uv run drawlib cache download --browser\n"
        "    (or: drawlib cache download --browser)\n\n"
        "  - Via Playwright CLI:\n"
        "      uv run playwright install --only-shell chromium\n"
        "    (or: playwright install --only-shell chromium)\n"
        f"{extra}"
    )


def import_sync_playwright(
    context_label: str = "PDF Export",
) -> Callable[[], PlaywrightContextManager]:
    """Lazily import and return `playwright.sync_api.sync_playwright`.

    Args:
        context_label (str): Human-readable feature name for error messages.

    Returns:
        Callable[[], PlaywrightContextManager]: Playwright sync context manager factory.

    Raises:
        RuntimeError: If the `playwright` package is not installed.
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as err:
        raise RuntimeError(_format_missing_playwright_error(context_label)) from err
    return sync_playwright


def install_headless_chromium(context_label: str = "Browser Setup") -> None:
    """Download Playwright's lightweight `chromium-headless-shell` via its bundled driver.

    Args:
        context_label (str): Human-readable feature name for error messages.

    Raises:
        RuntimeError: If Playwright is missing, driver binaries are invalid, or download fails.
    """
    try:
        from playwright._impl._driver import (  # noqa: PLC2701
            compute_driver_executable,
            get_driver_env,
        )
    except ImportError as err:
        raise RuntimeError(_format_missing_playwright_error(context_label)) from err

    driver_executable, driver_cli = compute_driver_executable()
    exec_path = Path(driver_executable).resolve()
    cli_path = Path(driver_cli).resolve()
    if not exec_path.is_file() or not cli_path.is_file():
        detail = f"Playwright driver executable not found ({exec_path}, {cli_path})."
        raise RuntimeError(_format_missing_browser_error(context_label, detail=detail))

    with _browser_install_lock():
        logger.info("Downloading headless Chromium browser (first-time setup)...")
        proc = subprocess.run(  # noqa: S603
            [str(exec_path), str(cli_path), *_INSTALL_ARGS],
            env=get_driver_env(),
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode != 0:
            output = (proc.stderr or proc.stdout or "").strip()
            detail = output or f"Playwright driver exited with status code {proc.returncode}."
            raise RuntimeError(_format_missing_browser_error(context_label, detail=detail))
        logger.info("Headless Chromium browser is ready.")


def launch_headless_chromium(
    playwright: Playwright,
    *,
    args: Sequence[str] | None = None,
    auto_install: bool = True,
    context_label: str = "PDF Export",
) -> Browser:
    """Launch headless Chromium, automatically downloading `chromium-headless-shell` on first use.

    Args:
        playwright (Playwright): Active Playwright instance from `sync_playwright()`.
        args (Sequence[str] | None): Chromium launch flags. Uses font-hinting defaults when None.
        auto_install (bool): Automatically download `chromium-headless-shell` if missing.
        context_label (str): Human-readable feature name for error messages.

    Returns:
        Browser: Launched headless Chromium browser instance.

    Raises:
        RuntimeError: If browser launch or on-demand installation fails.
    """
    launch_args = list(args) if args is not None else list(_DEFAULT_CHROMIUM_ARGS)
    try:
        return playwright.chromium.launch(headless=True, args=launch_args)
    except Exception as err:
        if _is_missing_system_deps_error(err):
            raise RuntimeError(_format_missing_system_deps_error(context_label, err)) from err
        if not _is_missing_browser_executable_error(err):
            raise RuntimeError(f"Failed to launch Chromium browser: {err}") from err
        if not auto_install:
            raise RuntimeError(_format_missing_browser_error(context_label, detail=str(err))) from err

        install_headless_chromium(context_label=context_label)

    try:
        return playwright.chromium.launch(headless=True, args=launch_args)
    except Exception as retry_err:
        if _is_missing_system_deps_error(retry_err):
            raise RuntimeError(_format_missing_system_deps_error(context_label, retry_err)) from retry_err
        if _is_missing_browser_executable_error(retry_err):
            raise RuntimeError(
                _format_missing_browser_error(context_label, detail=str(retry_err))
            ) from retry_err
        raise RuntimeError(f"Failed to launch Chromium browser: {retry_err}") from retry_err
