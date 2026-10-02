# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for the download module in l3_external."""

import hashlib
import os
from pathlib import Path
from typing import Union
from unittest.mock import MagicMock, patch

import pytest

from drawlib._core.l3_external._download import download_if_not_exist


class TestDownloadIfNotExist:
    """Test cases for download_if_not_exist function."""

    def test_download_if_not_exist_file_exists_checksum_ok(self, tmp_path: Path):
        """Test download_if_not_exist when file already exists and checksum is correct."""
        file_path = tmp_path / "test_file.txt"
        content = b"hello"
        file_path.write_bytes(content)

        md5_hash = hashlib.md5(content).hexdigest()  # noqa: S324

        with patch("drawlib._core.l3_external._download._find_package_for_file_path") as mock_find:
            download_if_not_exist(str(file_path), "http://dummy/url", md5_hash)
            # Should not look up package since file exists and checksum is ok
            mock_find.assert_not_called()

    def test_download_if_not_exist_unknown_package(self, tmp_path: Path):
        """Test download_if_not_exist raises FileNotFoundError when no package matches."""
        file_path = tmp_path / "unknown_asset.ttf"
        with pytest.raises(FileNotFoundError, match="does not exist locally and no release asset package matches it"):
            download_if_not_exist(str(file_path))

    def test_download_if_not_exist_package_success(self, tmp_path: Path):
        """Test download_if_not_exist downloads and extracts matching package."""
        file_path = tmp_path / "fonts" / "roboto" / "Roboto-Regular.ttf"
        mock_pkg = MagicMock()
        mock_pkg.name = "font_roboto"

        def fake_extract():
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_bytes(b"fontdata")

        mock_pkg.download_and_extract.side_effect = fake_extract

        with patch("drawlib._core.l3_external._download._find_package_for_file_path", return_value=mock_pkg):
            download_if_not_exist(str(file_path))
            mock_pkg.download_and_extract.assert_called_once()

        assert file_path.exists()
        assert file_path.read_bytes() == b"fontdata"

    def test_download_if_not_exist_file_missing_after_download(self, tmp_path: Path):
        """Test download_if_not_exist raises RuntimeError if file is missing after download."""
        file_path = tmp_path / "fonts" / "roboto" / "Roboto-Regular.ttf"
        mock_pkg = MagicMock()
        mock_pkg.name = "font_roboto"
        # does not write the file

        with patch("drawlib._core.l3_external._download._find_package_for_file_path", return_value=mock_pkg):
            with pytest.raises(RuntimeError, match="downloaded, but file .* was not found"):
                download_if_not_exist(str(file_path))
