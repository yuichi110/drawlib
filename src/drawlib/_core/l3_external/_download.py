# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Download assets implementations."""

from __future__ import annotations

import contextlib
import hashlib
import os
import re
import sys
import tempfile
import threading
import time
from collections.abc import Generator
from pathlib import Path
from typing import IO, Final

from drawlib._core.l1_core import logger
from drawlib._core.l1_core._const import ASSETS_DIR_PATH
from drawlib._core.l3_external._package import ReleaseAssetPackage

_THREAD_MAP_LOCK = threading.Lock()
_PACKAGE_THREAD_LOCKS: dict[str, threading.Lock] = {}
_WIN_LOCK_TIMEOUT_SEC: Final[float] = 300.0
_WIN_LOCK_POLL_SEC: Final[float] = 0.05


def _get_package_thread_lock(pkg_name: str) -> threading.Lock:
    """Return a per-package in-process threading lock."""
    with _THREAD_MAP_LOCK:
        lock = _PACKAGE_THREAD_LOCKS.get(pkg_name)
        if lock is None:
            lock = threading.Lock()
            _PACKAGE_THREAD_LOCKS[pkg_name] = lock
        return lock


def _resolve_asset_lock_paths(pkg_name: str) -> list[Path]:
    """Return candidate lock file paths for serializing concurrent downloads of `pkg_name`."""
    safe_name = re.sub(r"[^a-zA-Z0-9_.-]", "_", os.path.basename(pkg_name)) or "asset"
    lock_filename = f"{safe_name}.lock"
    candidates: list[Path] = [Path(ASSETS_DIR_PATH) / ".locks" / lock_filename]

    if sys.platform == "win32":
        local_app_data = os.environ.get("LOCALAPPDATA", str(Path.home()))
        candidates.append(Path(local_app_data) / "drawlib" / "locks" / lock_filename)
    else:
        xdg_cache = os.environ.get("XDG_CACHE_HOME", str(Path.home() / ".cache"))
        candidates.append(Path(xdg_cache) / "drawlib" / "locks" / lock_filename)

    uid_suffix = str(os.getuid()) if hasattr(os, "getuid") else "user"
    candidates.append(Path(tempfile.gettempdir()) / f"drawlib_{uid_suffix}" / "locks" / lock_filename)
    return candidates


def _acquire_os_file_lock(lock_handle: IO[bytes]) -> str | None:
    """Acquire an exclusive cross-process lock on POSIX (fcntl) or Windows (msvcrt)."""
    if sys.platform == "win32":
        with contextlib.suppress(ImportError, OSError):
            import msvcrt  # noqa: PLC0415

            locking_fn = getattr(msvcrt, "locking", None)
            lk_nblck = getattr(msvcrt, "LK_NBLCK", 2)
            if locking_fn is None:
                return None

            lock_handle.seek(0, os.SEEK_END)
            if lock_handle.tell() == 0:
                lock_handle.write(b"0")
                lock_handle.flush()

            deadline = time.monotonic() + _WIN_LOCK_TIMEOUT_SEC
            while True:
                try:
                    lock_handle.seek(0)
                    locking_fn(lock_handle.fileno(), lk_nblck, 1)
                    return "msvcrt"
                except OSError:
                    if time.monotonic() >= deadline:
                        return None
                    time.sleep(_WIN_LOCK_POLL_SEC)
        return None

    with contextlib.suppress(ImportError, OSError):
        import fcntl  # noqa: PLC0415

        fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX)
        return "fcntl"
    return None


def _release_os_file_lock(lock_handle: IO[bytes], backend: str | None) -> None:
    """Release an exclusive cross-process file lock acquired by `_acquire_os_file_lock`."""
    if backend == "msvcrt":
        with contextlib.suppress(ImportError, OSError):
            import msvcrt  # noqa: PLC0415

            locking_fn = getattr(msvcrt, "locking", None)
            lk_unlck = getattr(msvcrt, "LK_UNLCK", 0)
            if locking_fn is not None:
                lock_handle.seek(0)
                locking_fn(lock_handle.fileno(), lk_unlck, 1)
    elif backend == "fcntl":
        with contextlib.suppress(ImportError, OSError):
            import fcntl  # noqa: PLC0415

            fcntl.flock(lock_handle.fileno(), fcntl.LOCK_UN)


@contextlib.contextmanager
def _asset_package_lock(pkg_name: str) -> Generator[None, None, None]:
    """Serialize concurrent downloads and extractions of `pkg_name` across threads and processes."""
    with _get_package_thread_lock(pkg_name):
        lock_handle: IO[bytes] | None = None
        for lock_path in _resolve_asset_lock_paths(pkg_name):
            try:
                lock_path.parent.mkdir(parents=True, exist_ok=True)
                lock_handle = lock_path.open("a+b")
                break
            except OSError:
                continue

        if lock_handle is None:
            yield
            return

        backend: str | None = None
        try:
            backend = _acquire_os_file_lock(lock_handle)
            yield
        finally:
            _release_os_file_lock(lock_handle, backend)
            with contextlib.suppress(OSError):
                lock_handle.close()


def _find_package_for_file_path(file_path: str) -> ReleaseAssetPackage | None:
    """Identify matching ReleaseAssetPackage for a local file path if applicable.

    Args:
        file_path: File path to inspect.

    Returns:
        ReleaseAssetPackage | None: Matching package if matched, otherwise None.
    """
    from drawlib._release_assets import find_package_for_resource_path  # noqa: PLC0415

    normalized = file_path.replace("\\", "/").strip("/")
    if "/fonts/" in normalized:
        sub = "fonts/" + normalized.split("/fonts/", 1)[1]
        return find_package_for_resource_path(sub)
    if "/fonticons/" in normalized:
        sub = "fonticons/" + normalized.split("/fonticons/", 1)[1]
        return find_package_for_resource_path(sub)
    if "/icons/" in normalized:
        sub = "icons/" + normalized.split("/icons/", 1)[1]
        return find_package_for_resource_path(sub)
    if "/maps/" in normalized:
        sub = "maps/" + normalized.split("/maps/", 1)[1]
        return find_package_for_resource_path(sub)
    if (
        normalized.startswith("fonts/")
        or normalized.startswith("fonticons/")
        or normalized.startswith("icons/")
        or normalized.startswith("maps/")
    ):
        return find_package_for_resource_path(normalized)
    return None


def download_if_not_exist(
    file_path: str,
    md5_hash: str = "",
) -> None:
    """Download asset package if the asset file does not exist locally.

    Args:
        file_path (str): Local file path where the asset should exist.
        md5_hash (str): Optional expected MD5 checksum of the file.

    Raises:
        FileNotFoundError: If the asset package cannot be found for the given path.
        RuntimeError: If downloading or extracting the package fails.
    """

    def is_file_exist() -> bool:
        return os.path.exists(file_path)

    def is_checksum_correct() -> bool:
        if not md5_hash:
            return True
        md5_hash2 = hashlib.md5(usedforsecurity=False)
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                md5_hash2.update(chunk)
        return md5_hash2.hexdigest().lower() == md5_hash.strip().lower()

    # Fast path: if file exists and checksum is correct, nothing to do
    if is_file_exist() and is_checksum_correct():
        return

    # Check if this asset belongs to a defined ReleaseAssetPackage
    pkg = _find_package_for_file_path(file_path)
    if pkg is None:
        raise FileNotFoundError(
            f"Asset file '{file_path}' does not exist locally and no release asset package matches it."
        )

    with _asset_package_lock(pkg.name):
        if is_file_exist() and is_checksum_correct():
            return

        logger.info('Downloading release asset package "%s" from GitHub Releases...', pkg.name)
        pkg.download_and_extract()

        if not is_file_exist():
            raise RuntimeError(f"Asset package '{pkg.name}' downloaded, but file '{file_path}' was not found.")
        logger.info('Asset package "%s" downloaded and extracted successfully.', pkg.name)
