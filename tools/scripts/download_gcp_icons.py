# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Script to download and extract official Google Cloud architecture diagram icons."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import sys
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, NamedTuple

project_root = Path(__file__).parent.parent.parent.resolve()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from tools.scripts.utils import cd_to_project_root  # noqa: E402


class PackageSource(NamedTuple):
    """Configuration for an official Google Cloud icon asset package."""

    name: str
    url: str
    target_subdir: str
    strip_prefix: str


SOURCES: list[PackageSource] = [
    PackageSource(
        name="core_products",
        url="https://services.google.com/fh/files/misc/core-products-icons.zip",
        target_subdir="core_products",
        strip_prefix="Unique Icons/",
    ),
    PackageSource(
        name="category",
        url="https://services.google.com/fh/files/misc/category-icons.zip",
        target_subdir="category",
        strip_prefix="Category Icons/",
    ),
    PackageSource(
        name="legacy",
        url="https://services.google.com/fh/files/misc/google-cloud-legacy-icons.zip",
        target_subdir="legacy",
        strip_prefix="",
    ),
]

DOCUMENTATION_URL = "https://services.google.com/fh/files/misc/google-cloud-product-icons.pdf"


def _download_url(url: str) -> bytes:
    """Download bytes from a given URL using a standard browser user agent.

    Args:
        url: Direct HTTP/HTTPS URL.

    Returns:
        Downloaded raw bytes content.
    """
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; drawlib-asset-fetcher/1.0)"})
    with urllib.request.urlopen(req) as resp:
        return resp.read()


def _compute_sha256(data: bytes) -> str:
    """Compute hex SHA-256 digest of raw bytes.

    Args:
        data: Raw bytes content.

    Returns:
        Hex-encoded SHA-256 string.
    """
    return hashlib.sha256(data).hexdigest()


def download_and_extract_gcp_icons(
    output_dir: Path,
    save_archives: bool = True,
    download_doc: bool = True,
) -> dict[str, Any]:
    """Download all official Google Cloud icon packages and extract cleanly.

    Args:
        output_dir: Path to directory where original assets are saved (e.g. original_assets/gcp).
        save_archives: Whether to store original .zip files in _archives/ folder.
        download_doc: Whether to download official overview PDF guide into docs/.

    Returns:
        Manifest dictionary cataloging downloaded sources and extracted files.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    archives_dir = output_dir / "_archives"
    if save_archives:
        archives_dir.mkdir(parents=True, exist_ok=True)

    manifest_sources: dict[str, dict[str, object]] = {}
    manifest_files: dict[str, list[str]] = {}
    total_files_extracted = 0

    for source in SOURCES:
        print(f"[*] Downloading {source.name} from {source.url} ...")
        zip_bytes = _download_url(source.url)
        sha256_digest = _compute_sha256(zip_bytes)
        size_bytes = len(zip_bytes)
        archive_name = source.url.split("/")[-1]

        if save_archives:
            archive_path = archives_dir / archive_name
            archive_path.write_bytes(zip_bytes)
            print(f"    Saved raw archive: {archive_path}")

        target_dir = output_dir / source.target_subdir
        target_dir.mkdir(parents=True, exist_ok=True)

        extracted_rel_paths: list[str] = []
        with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
            for zip_entry in zf.infolist():
                entry_name = zip_entry.filename
                # Skip directory entries, macOS metadata, hidden files, and Adobe Illustrator files
                if (
                    entry_name.endswith("/")
                    or "__MACOSX" in entry_name
                    or ".DS_Store" in entry_name
                    or entry_name.endswith(".ai")
                ):
                    continue

                rel_name = entry_name
                if source.strip_prefix and rel_name.startswith(source.strip_prefix):
                    rel_name = rel_name[len(source.strip_prefix) :]

                dest_file = target_dir / rel_name
                dest_file.parent.mkdir(parents=True, exist_ok=True)

                file_content = zf.read(entry_name)
                dest_file.write_bytes(file_content)
                dest_file.chmod(0o644)

                extracted_rel_paths.append(str(dest_file.relative_to(output_dir)))

        extracted_rel_paths.sort()
        manifest_files[source.name] = extracted_rel_paths
        count = len(extracted_rel_paths)
        total_files_extracted += count

        manifest_sources[source.name] = {
            "url": source.url,
            "archive_name": archive_name,
            "sha256": sha256_digest,
            "size_bytes": size_bytes,
            "files_count": count,
            "target_dir": source.target_subdir,
        }
        print(f"    Extracted {count} files to {target_dir}")

    if download_doc:
        print(f"[*] Downloading official icon overview guide from {DOCUMENTATION_URL} ...")
        docs_dir = output_dir / "docs"
        docs_dir.mkdir(parents=True, exist_ok=True)
        pdf_bytes = _download_url(DOCUMENTATION_URL)
        pdf_sha256 = _compute_sha256(pdf_bytes)
        pdf_name = DOCUMENTATION_URL.rsplit("/", maxsplit=1)[-1]
        pdf_path = docs_dir / pdf_name
        pdf_path.write_bytes(pdf_bytes)
        print(f"    Saved documentation: {pdf_path}")

        manifest_sources["documentation"] = {
            "url": DOCUMENTATION_URL,
            "file_name": pdf_name,
            "sha256": pdf_sha256,
            "size_bytes": len(pdf_bytes),
            "target_path": f"docs/{pdf_name}",
        }

    now_iso = datetime.now(timezone.utc).isoformat()
    manifest = {
        "format_version": "1.0",
        "provider": "gcp",
        "downloaded_at": now_iso,
        "total_icons": total_files_extracted,
        "sources": manifest_sources,
        "files": manifest_files,
    }

    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[✓] Generated manifest at {manifest_path}")
    print(f"[✓] Successfully acquired {total_files_extracted} original Google Cloud icons!")

    return manifest


def main() -> None:
    """CLI entry point for downloading GCP original icon assets."""
    cd_to_project_root()

    parser = argparse.ArgumentParser(
        description="Download and extract official Google Cloud architecture diagram icons.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("original_assets/gcp"),
        help="Destination directory for original GCP assets (default: original_assets/gcp).",
    )
    parser.add_argument(
        "--no-archives",
        action="store_true",
        help="Do not retain raw .zip archive files in _archives/ subdirectory.",
    )
    parser.add_argument(
        "--no-docs",
        action="store_true",
        help="Do not download official overview guide PDF.",
    )

    args = parser.parse_args()

    download_and_extract_gcp_icons(
        output_dir=args.output_dir,
        save_archives=not args.no_archives,
        download_doc=not args.no_docs,
    )


if __name__ == "__main__":
    main()
