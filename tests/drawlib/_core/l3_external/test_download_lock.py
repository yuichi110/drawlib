# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for cross-thread and cross-process locking in l3_external download."""

from __future__ import annotations

import hashlib
import io
import multiprocessing as mp
import threading
import time
import zipfile
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from drawlib._core.l3_external._download import download_if_not_exist
from drawlib._core.l3_external._package import ReleaseAssetPackage


def _mp_worker_download(args: tuple[str, str, str]) -> int:
    """Child process entrypoint testing cross-process _asset_package_lock serialization."""
    target_file_str, assets_root_str, counter_file_str = args
    target_file = Path(target_file_str)
    counter_file = Path(counter_file_str)

    def _fake_extract() -> None:
        # Record invocation count atomically via append
        with counter_file.open("ab") as cf:
            cf.write(b"1")
        time.sleep(0.08)
        target_file.parent.mkdir(parents=True, exist_ok=True)
        target_file.write_bytes(b"shared-font-payload")

    mock_pkg = MagicMock()
    mock_pkg.name = "font_roboto"
    mock_pkg.download_and_extract.side_effect = _fake_extract

    with (
        patch("drawlib._core.l3_external._download.ASSETS_DIR_PATH", assets_root_str),
        patch("drawlib._core.l3_external._download._find_package_for_file_path", return_value=mock_pkg),
    ):
        download_if_not_exist(target_file_str)
    return 1


class TestAssetDownloadLocking:
    """Tests for concurrent asset download serialization and atomic archive extraction."""

    def test_concurrent_threads_download_only_once(self, tmp_path: Path) -> None:
        """Multiple threads requesting the same missing asset should download/extract once."""
        assets_root = tmp_path / "cached_assets"
        target_file = assets_root / "fonts" / "roboto" / "Roboto-Regular.ttf"
        call_count = 0
        count_lock = threading.Lock()
        barrier = threading.Barrier(6)

        def fake_extract() -> None:
            nonlocal call_count
            with count_lock:
                call_count += 1
            time.sleep(0.05)
            target_file.parent.mkdir(parents=True, exist_ok=True)
            target_file.write_bytes(b"roboto-bytes")

        mock_pkg = MagicMock()
        mock_pkg.name = "font_roboto"
        mock_pkg.download_and_extract.side_effect = fake_extract

        def worker() -> None:
            barrier.wait()
            download_if_not_exist(str(target_file))

        with (
            patch("drawlib._core.l3_external._download.ASSETS_DIR_PATH", str(assets_root)),
            patch("drawlib._core.l3_external._download._find_package_for_file_path", return_value=mock_pkg),
        ):
            with ThreadPoolExecutor(max_workers=6) as pool:
                futures = [pool.submit(worker) for _ in range(6)]
                for fut in futures:
                    fut.result()

        assert call_count == 1
        assert target_file.read_bytes() == b"roboto-bytes"

    def test_concurrent_processes_download_only_once(self, tmp_path: Path) -> None:
        """Multiple spawned processes requesting the same missing asset serialize via file lock."""
        assets_root = tmp_path / "cached_assets_mp"
        target_file = assets_root / "fonts" / "roboto" / "Roboto-Regular.ttf"
        counter_file = tmp_path / "extract_calls.bin"
        counter_file.write_bytes(b"")

        payload = (str(target_file), str(assets_root), str(counter_file))
        ctx = mp.get_context("spawn")
        with ProcessPoolExecutor(max_workers=4, mp_context=ctx) as pool:
            results = list(pool.map(_mp_worker_download, [payload] * 4))

        assert sum(results) == 4
        assert target_file.read_bytes() == b"shared-font-payload"
        assert len(counter_file.read_bytes()) == 1

    def test_atomic_zip_extraction_and_zip_slip_rejection(self, tmp_path: Path) -> None:
        """ReleaseAssetPackage.download_and_extract writes files atomically and rejects path traversal."""
        assets_root = tmp_path / "assets"

        # 1. Valid archive extracts cleanly with no leftover .tmp_* files
        good_buf = io.BytesIO()
        with zipfile.ZipFile(good_buf, "w") as zf:
            zf.writestr("Roboto-Regular.ttf", b"ttf-binary-content")
        good_bytes = good_buf.getvalue()
        good_sha = hashlib.sha256(good_bytes).hexdigest()

        pkg = ReleaseAssetPackage(
            name="font_roboto",
            category="font",
            archive_name="font_roboto.zip",
            archive_sha256=good_sha,
            source_rel_path="fonts/roboto",
            target_rel_path="fonts/roboto",
            files=("Roboto-Regular.ttf",),
        )

        mock_resp = MagicMock()
        mock_resp.__enter__.return_value.read.return_value = good_bytes

        with (
            patch("drawlib._core.l3_external._package.ASSETS_DIR_PATH", str(assets_root)),
            patch("urllib.request.urlopen", return_value=mock_resp),
        ):
            pkg.download_and_extract(force=True)

        extracted = assets_root / "fonts" / "roboto" / "Roboto-Regular.ttf"
        assert extracted.read_bytes() == b"ttf-binary-content"
        leftover_tmps = list((assets_root / "fonts" / "roboto").glob(".tmp_*"))
        assert leftover_tmps == []

        # 2. Malicious Zip Slip path traversal is rejected
        bad_buf = io.BytesIO()
        with zipfile.ZipFile(bad_buf, "w") as zf:
            zf.writestr("../../escaped.txt", b"malicious")
        bad_bytes = bad_buf.getvalue()
        bad_sha = hashlib.sha256(bad_bytes).hexdigest()

        bad_pkg = ReleaseAssetPackage(
            name="font_evil",
            category="font",
            archive_name="font_evil.zip",
            archive_sha256=bad_sha,
            source_rel_path="fonts/evil",
            target_rel_path="fonts/evil",
            files=("escaped.txt",),
        )
        mock_bad_resp = MagicMock()
        mock_bad_resp.__enter__.return_value.read.return_value = bad_bytes

        with (
            patch("drawlib._core.l3_external._package.ASSETS_DIR_PATH", str(assets_root)),
            patch("urllib.request.urlopen", return_value=mock_bad_resp),
            pytest.raises(RuntimeError, match="Unsafe archive member path"),
        ):
            bad_pkg.download_and_extract(force=True)

        assert not (tmp_path / "escaped.txt").exists()
