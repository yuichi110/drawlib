# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for release asset downloading and extraction features."""

import hashlib
import io
import zipfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from drawlib._core.l3_external._download import (
    _find_package_for_file_path,
    download_if_not_exist,
)
from drawlib._release_assets import (
    RELEASE_ASSET_PACKAGES,
    ReleaseAssetPackage,
    download_all_release_assets,
    ensure_asset_available,
    find_package_for_font_path,
    find_package_for_icon_path,
    find_package_for_resource_path,
)


def _make_dummy_zip_bytes(files: dict[str, bytes]) -> tuple[bytes, str]:
    """Create in-memory zip bytes and calculate its SHA-256 hex digest."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        for fname, data in files.items():
            zf.writestr(fname, data)
    raw = buf.getvalue()
    sha = hashlib.sha256(raw).hexdigest()
    return raw, sha


class TestPackageResolution:
    """Test resolution of font and icon packages from resource paths."""

    def test_find_package_for_font_path(self):
        """Verify font resource path mapping."""
        pkg = find_package_for_font_path("roboto/regular.ttf")
        assert pkg is not None
        assert pkg.name == "font_roboto"

        pkg_with_prefix = find_package_for_font_path("fonts/roboto/bold.ttf")
        assert pkg_with_prefix is not None
        assert pkg_with_prefix.name == "font_roboto"

        pkg_cjk = find_package_for_font_path("cjk_japanese_noto_sans/regular.otf")
        assert pkg_cjk is not None
        assert pkg_cjk.name == "font_cjk_japanese_noto_sans"

        assert find_package_for_font_path("non_existent/foo.ttf") is None

    def test_find_package_for_icon_path(self):
        """Verify icon resource path mapping."""
        pkg = find_package_for_icon_path("phosphor/thin.ttf")
        assert pkg is not None
        assert pkg.name == "icon_phosphor"

        pkg_with_prefix = find_package_for_icon_path("fonticons/phosphor/bold.ttf")
        assert pkg_with_prefix is not None
        assert pkg_with_prefix.name == "icon_phosphor"

        assert find_package_for_icon_path("unknown/icon.ttf") is None

    def test_find_package_for_resource_path(self):
        """Verify unified resource path resolution for both fonts and icons."""
        font_pkg = find_package_for_resource_path("fonts/roboto/light.ttf")
        assert font_pkg is not None
        assert font_pkg.name == "font_roboto"

        icon_pkg = find_package_for_resource_path("fonticons/phosphor/regular.ttf")
        assert icon_pkg is not None
        assert icon_pkg.name == "icon_phosphor"

        icon_pkg2 = find_package_for_resource_path("phosphor/fill.ttf")
        assert icon_pkg2 is not None
        assert icon_pkg2.name == "icon_phosphor"

    def test_find_package_for_file_path(self):
        """Verify file path mapping in download module."""
        pkg1 = _find_package_for_file_path("/path/to/drawlib/_assets/fonts/roboto/regular.ttf")
        assert pkg1 is not None
        assert pkg1.name == "font_roboto"

        pkg2 = _find_package_for_file_path("C:\\drawlib\\_assets\\fonticons\\phosphor\\bold.ttf")
        assert pkg2 is not None
        assert pkg2.name == "icon_phosphor"

        assert _find_package_for_file_path("/non_assets_path/arbitrary/file.txt") is None


class TestDownloadAndExtract:
    """Test downloading and extraction lifecycle."""

    def test_is_downloaded(self, tmp_path: Path):
        """Test is_downloaded checks presence of all package files."""
        pkg = RELEASE_ASSET_PACKAGES.font_roboto
        with patch.object(ReleaseAssetPackage, "get_local_dir", return_value=tmp_path):
            assert not pkg.is_downloaded()

            # Create partial files
            for fname in pkg.files[:-1]:
                (tmp_path / fname).write_bytes(b"dummy")
            assert not pkg.is_downloaded()

            # Create all files
            (tmp_path / pkg.files[-1]).write_bytes(b"dummy")
            assert pkg.is_downloaded()

    def test_download_and_extract_success(self, tmp_path: Path):
        """Test successful download, SHA-256 check, and archive extraction."""
        zip_bytes, sha256 = _make_dummy_zip_bytes({"regular.ttf": b"ttf_content", "LICENSE.txt": b"license"})

        test_pkg = ReleaseAssetPackage(
            name=RELEASE_ASSET_PACKAGES.font_roboto.name,
            category="font",
            archive_name="test.zip",
            archive_sha256=sha256,
            source_rel_path="fonts/test",
            target_rel_path="fonts/test",
            files=["regular.ttf", "LICENSE.txt"],
        )

        mock_resp = MagicMock()
        mock_resp.read.return_value = zip_bytes

        with (
            patch.object(ReleaseAssetPackage, "get_local_dir", return_value=tmp_path),
            patch("urllib.request.urlopen") as mock_urlopen,
        ):
            mock_urlopen.return_value.__enter__.return_value = mock_resp
            test_pkg.download_and_extract()

        assert (tmp_path / "regular.ttf").read_bytes() == b"ttf_content"
        assert (tmp_path / "LICENSE.txt").read_bytes() == b"license"

    def test_download_and_extract_hash_mismatch(self, tmp_path: Path):
        """Test that SHA-256 mismatch raises RuntimeError and does not extract files."""
        zip_bytes, _ = _make_dummy_zip_bytes({"regular.ttf": b"content"})

        test_pkg = ReleaseAssetPackage(
            name=RELEASE_ASSET_PACKAGES.font_roboto.name,
            category="font",
            archive_name="test.zip",
            archive_sha256="wrong_hash_00000000000000000000000000000000000000000000000000000000",
            source_rel_path="fonts/test",
            target_rel_path="fonts/test",
            files=["regular.ttf"],
        )

        mock_resp = MagicMock()
        mock_resp.read.return_value = zip_bytes

        with (
            patch.object(ReleaseAssetPackage, "get_local_dir", return_value=tmp_path),
            patch("urllib.request.urlopen") as mock_urlopen,
        ):
            mock_urlopen.return_value.__enter__.return_value = mock_resp
            with pytest.raises(RuntimeError, match="Checksum mismatch for 'test.zip'"):
                test_pkg.download_and_extract()

        assert not (tmp_path / "regular.ttf").exists()

    def test_ensure_asset_available(self, tmp_path: Path):
        """Test ensure_asset_available triggers download if files are missing."""
        with (
            patch.object(ReleaseAssetPackage, "is_downloaded", return_value=False),
            patch.object(ReleaseAssetPackage, "download_and_extract") as mock_dl,
        ):
            ensure_asset_available("fonts/roboto/regular.ttf")
            mock_dl.assert_called_once()

        with (
            patch.object(ReleaseAssetPackage, "is_downloaded", return_value=True),
            patch.object(ReleaseAssetPackage, "download_and_extract") as mock_dl,
        ):
            ensure_asset_available("fonts/roboto/regular.ttf")
            mock_dl.assert_not_called()

    def test_download_if_not_exist_uses_release_package(self, tmp_path: Path):
        """Test download_if_not_exist delegates to package extraction when path matches a release package."""
        target_file = tmp_path / "fonts" / "roboto" / "regular.ttf"

        def fake_extract(**kwargs):
            target_file.parent.mkdir(parents=True, exist_ok=True)
            target_file.write_bytes(b"downloaded")

        with patch.object(ReleaseAssetPackage, "download_and_extract", side_effect=fake_extract) as mock_extract:
            download_if_not_exist(str(target_file), "http://dummy/url", "dummy_md5")
            mock_extract.assert_called_once()

        assert target_file.read_bytes() == b"downloaded"

    def test_download_all_release_assets(self):
        """Test download_all_release_assets iterates over all 47 packages."""
        with patch("drawlib._release_assets.ReleaseAssetPackage.download_and_extract") as mock_dl:
            download_all_release_assets()
            assert mock_dl.call_count == 47
