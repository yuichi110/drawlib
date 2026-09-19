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

        with patch("urllib.request.urlopen") as mock_urlopen:
            download_if_not_exist(str(file_path), "http://dummy/url", md5_hash)
            # urlopen should not be called since file exists and checksum is ok
            mock_urlopen.assert_not_called()

    def test_download_if_not_exist_file_does_not_exist(self, tmp_path: Path):
        """Test download_if_not_exist when file does not exist locally."""
        file_path = tmp_path / "subdir" / "test_file.txt"
        content = b"hello"
        md5_hash = hashlib.md5(content).hexdigest()  # noqa: S324

        # Mock urllib.request.urlopen as a context manager
        mock_response = MagicMock()
        mock_response.read.return_value = content

        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_urlopen.return_value.__enter__.return_value = mock_response

            download_if_not_exist(str(file_path), "http://dummy/url", md5_hash)

            mock_urlopen.assert_called_once_with("http://dummy/url")

        assert file_path.exists()
        assert file_path.read_bytes() == content

    def test_download_if_not_exist_file_exists_but_checksum_mismatch(self, tmp_path: Path):
        """Test download_if_not_exist when file exists but has incorrect checksum."""
        file_path = tmp_path / "test_file.txt"
        file_path.write_bytes(b"world")  # Mismatched initial content

        target_content = b"hello"
        md5_hash = hashlib.md5(target_content).hexdigest()  # noqa: S324

        # Mock urllib.request.urlopen as a context manager
        mock_response = MagicMock()
        mock_response.read.return_value = target_content

        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_urlopen.return_value.__enter__.return_value = mock_response

            download_if_not_exist(str(file_path), "http://dummy/url", md5_hash)

            mock_urlopen.assert_called_once_with("http://dummy/url")

        assert file_path.exists()
        assert file_path.read_bytes() == target_content

    def test_download_if_not_exist_http_error(self, tmp_path: Path):
        """Test download_if_not_exist raises RuntimeError when network download fails."""
        file_path = tmp_path / "test_file.txt"
        md5_hash = "d41d8cd98f00b204e9800998ecf8427e"

        with patch("urllib.request.urlopen", side_effect=Exception("HTTP Error 404")):
            with pytest.raises(RuntimeError, match="File download error happens. HTTP Error 404"):
                download_if_not_exist(str(file_path), "http://dummy/url", md5_hash)

    def test_download_if_not_exist_checksum_mismatch_after_download(self, tmp_path: Path):
        """Test download_if_not_exist raises RuntimeError when checksum mismatches post-download."""
        file_path = tmp_path / "test_file.txt"
        downloaded_content = b"world"
        expected_md5 = hashlib.md5(b"hello").hexdigest()  # noqa: S324  # Checksum expects 'hello'

        mock_response = MagicMock()
        mock_response.read.return_value = downloaded_content

        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_urlopen.return_value.__enter__.return_value = mock_response

            with pytest.raises(RuntimeError, match="File download completed. But checksum has problem. Abort."):
                download_if_not_exist(str(file_path), "http://dummy/url", expected_md5)

    def test_download_if_not_exist_file_missing_after_download(self, tmp_path: Path):
        """Test download_if_not_exist raises RuntimeError if file is missing after download."""
        file_path = tmp_path / "test_file.txt"
        content = b"hello"
        md5_hash = hashlib.md5(content).hexdigest()  # noqa: S324

        mock_response = MagicMock()
        mock_response.read.return_value = content

        original_exists = os.path.exists

        def custom_exists(path: Union[str, os.PathLike[str]]) -> bool:
            if str(path) == str(file_path):
                return False
            return original_exists(path)

        with (
            patch("urllib.request.urlopen") as mock_urlopen,
            patch("os.path.exists", side_effect=custom_exists),
        ):
            mock_urlopen.return_value.__enter__.return_value = mock_response

            with pytest.raises(RuntimeError, match="File download completed. But not saved. Abort."):
                download_if_not_exist(str(file_path), "http://dummy/url", md5_hash)
