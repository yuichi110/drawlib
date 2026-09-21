# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Normalize Google Cloud architecture diagram icons into uniform 512x512 transparent PNGs."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image

project_root = Path(__file__).parent.parent.parent.resolve()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from tools.scripts.utils import cd_to_project_root  # noqa: E402

COMMON_ALIASES: dict[str, str] = {
    "gce": "compute_engine",
    "gcs": "cloud_storage",
    "gke": "google_kubernetes_engine",
    "google_kubernetes_engine": "gke",
    "iam": "identity_and_access_management",
    "vpc": "virtual_private_cloud",
    "kms": "key_management_service",
    "functions": "cloud_functions",
}


def sanitize_name(name: str) -> str:
    """Sanitize a raw service or category name into a snake_case identifier.

    Args:
        name: Raw name from folder or archive (e.g. 'Compute Engine', 'AI _ Machine Learning').

    Returns:
        Clean lowercase snake_case string (e.g. 'compute_engine', 'ai_machine_learning').
    """
    cleaned = name.replace("&", "").replace("-", "_").replace(" ", "_")
    cleaned = re.sub(r"[^\w]", "", cleaned)
    cleaned = re.sub(r"_+", "_", cleaned.strip()).strip("_").lower()
    return cleaned


def normalize_single_icon(
    src_path: Path,
    dest_path: Path,
    target_size: int = 512,
    inner_size: int = 460,
) -> tuple[int, int, int, int]:
    """Normalize a single icon image to a transparent target_size x target_size PNG.

    Trims transparent/white outer padding, scales proportionally to fit within inner_size,
    and centers the icon within a square transparent canvas.

    Args:
        src_path: Path to original icon image file.
        dest_path: Destination path for normalized PNG.
        target_size: Dimensions of the square canvas (default 512).
        inner_size: Maximum dimension for the icon artwork (default 460).

    Returns:
        Bounding box tuple (left, upper, right, lower) of artwork in target canvas.

    Raises:
        ValueError: If artwork bounding box is empty after clipping.
    """
    img = Image.open(src_path)

    if img.mode == "RGB":
        rgba = img.convert("RGBA")
        arr = np.array(rgba)
        # Convert near-white background to transparent
        white_mask = (arr[:, :, 0] > 245) & (arr[:, :, 1] > 245) & (arr[:, :, 2] > 245)
        arr[white_mask, 3] = 0
        rgba = Image.fromarray(arr)
    else:
        rgba = img.convert("RGBA")
        # Special fix for legacy data_labeling stray rectangle in top-left
        if "data_labeling" in str(src_path):
            arr = np.array(rgba)
            arr[:30, :180, 3] = 0
            rgba = Image.fromarray(arr)

    bbox = rgba.getbbox()
    if not bbox:
        raise ValueError(f"Empty bounding box for {src_path}")

    cropped = rgba.crop(bbox)
    crop_w, crop_h = cropped.size

    scale = inner_size / max(crop_w, crop_h)
    new_w = max(1, int(round(crop_w * scale)))
    new_h = max(1, int(round(crop_h * scale)))

    resized = cropped.resize((new_w, new_h), Image.Resampling.LANCZOS)

    canvas = Image.new("RGBA", (target_size, target_size), (0, 0, 0, 0))
    offset_x = (target_size - new_w) // 2
    offset_y = (target_size - new_h) // 2
    canvas.paste(resized, (offset_x, offset_y), resized)

    dest_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(dest_path, "PNG", optimize=True)

    result_bbox = canvas.getbbox()
    return result_bbox or (offset_x, offset_y, offset_x + new_w, offset_y + new_h)


def _collect_icon_sources(manifest_data: dict[str, Any], src_dir: Path) -> dict[str, tuple[str, Path]]:
    """Gather mapping of normalized icon names to original source paths.

    Args:
        manifest_data: Loaded manifest JSON data from original assets.
        src_dir: Root directory of original assets.

    Returns:
        Dictionary mapping normalized name to (category, file_path).
    """
    icon_sources: dict[str, tuple[str, Path]] = {}

    # 1. Register Legacy icons
    for rel_path in manifest_data["files"].get("legacy", []):
        if rel_path.endswith(".png"):
            service_name = rel_path.split("/")[1]
            key = sanitize_name(service_name)
            icon_sources[key] = ("legacy", src_dir / rel_path)

    # 2. Register Core Products icons (overrides legacy with modern icons)
    for rel_path in manifest_data["files"].get("core_products", []):
        if rel_path.endswith(".png"):
            service_name = rel_path.split("/")[1]
            key = sanitize_name(service_name)
            icon_sources[key] = ("core_products", src_dir / rel_path)

    # 3. Register Category icons (prefixed with category_)
    for rel_path in manifest_data["files"].get("category", []):
        if rel_path.endswith(".png"):
            category_name = rel_path.split("/")[1]
            key = f"category_{sanitize_name(category_name)}"
            icon_sources[key] = ("category", src_dir / rel_path)

    return icon_sources


def _create_icon_aliases(dest_dir: Path, normalized_files_meta: dict[str, Any]) -> int:
    """Create convenience aliases for commonly abbreviated service names.

    Args:
        dest_dir: Target directory containing normalized PNGs.
        normalized_files_meta: Metadata dictionary to update with alias entries.

    Returns:
        Number of aliases created.
    """
    alias_count = 0
    print("[*] Creating convenience aliases ...")
    for alias_name, target_name in COMMON_ALIASES.items():
        target_png = dest_dir / f"{target_name}.png"
        alias_png = dest_dir / f"{alias_name}.png"
        if target_png.exists():
            shutil.copy2(target_png, alias_png)
            file_bytes = alias_png.read_bytes()
            sha256 = hashlib.sha256(file_bytes).hexdigest()
            normalized_files_meta[f"{alias_name}.png"] = {
                "source_category": "alias",
                "alias_to": f"{target_name}.png",
                "size_bytes": len(file_bytes),
                "sha256": sha256,
            }
            alias_count += 1
    return alias_count


def normalize_all_gcp_icons(
    src_dir: Path,
    dest_dir: Path,
    target_size: int = 512,
    inner_size: int = 460,
    create_aliases: bool = True,
) -> dict[str, Any]:
    """Normalize all GCP icons from original_assets/gcp into a flat release directory.

    Args:
        src_dir: Source directory containing original assets (e.g. original_assets/gcp).
        dest_dir: Target directory for normalized flat icons (e.g. release_assets/v0.3/icons/gcp).
        target_size: Final square canvas size (default: 512).
        inner_size: Inner content area size (default: 460).
        create_aliases: Whether to create convenience alias files (e.g. gce.png -> compute_engine.png).

    Returns:
        Manifest dictionary cataloging all normalized icons.
    """
    manifest_file = src_dir / "manifest.json"
    if not manifest_file.exists():
        raise FileNotFoundError(f"Original assets manifest not found at {manifest_file}. Run download first.")

    manifest_data = json.loads(manifest_file.read_text(encoding="utf-8"))
    icon_sources = _collect_icon_sources(manifest_data, src_dir)

    dest_dir.mkdir(parents=True, exist_ok=True)
    normalized_files_meta: dict[str, Any] = {}
    total_count = len(icon_sources)
    print(f"[*] Starting normalization of {total_count} Google Cloud icons into {dest_dir} ...")

    for idx, (name, (src_category, file_path)) in enumerate(sorted(icon_sources.items()), 1):
        target_file = dest_dir / f"{name}.png"
        bbox = normalize_single_icon(
            src_path=file_path,
            dest_path=target_file,
            target_size=target_size,
            inner_size=inner_size,
        )

        file_bytes = target_file.read_bytes()
        sha256 = hashlib.sha256(file_bytes).hexdigest()

        normalized_files_meta[f"{name}.png"] = {
            "source_category": src_category,
            "source_file": str(file_path.relative_to(src_dir)),
            "size_bytes": len(file_bytes),
            "sha256": sha256,
            "bbox": bbox,
        }

    alias_count = _create_icon_aliases(dest_dir, normalized_files_meta) if create_aliases else 0

    manifest = {
        "format_version": "1.0",
        "provider": "gcp",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "canvas_size": [target_size, target_size],
        "inner_size": [inner_size, inner_size],
        "total_primary_icons": total_count,
        "total_aliases": alias_count,
        "total_files": len(normalized_files_meta),
        "files": normalized_files_meta,
    }

    manifest_path = dest_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"[✓] Successfully normalized {total_count} primary icons + {alias_count} aliases!")
    print(f"[✓] Output written to {dest_dir} (Manifest: {manifest_path.name})")

    return manifest


def main() -> None:
    """CLI entry point for normalizing GCP icon assets."""
    cd_to_project_root()

    parser = argparse.ArgumentParser(
        description="Normalize Google Cloud architecture diagram icons into uniform 512x512 transparent PNGs.",
    )
    parser.add_argument(
        "--src-dir",
        type=Path,
        default=Path("original_assets/gcp"),
        help="Source directory containing original GCP assets (default: original_assets/gcp).",
    )
    parser.add_argument(
        "--dest-dir",
        type=Path,
        default=Path("release_assets/v0.3/icons/gcp"),
        help="Destination directory for normalized flat icons (default: release_assets/v0.3/icons/gcp).",
    )
    parser.add_argument(
        "--size",
        type=int,
        default=512,
        help="Canvas width/height (default: 512).",
    )
    parser.add_argument(
        "--inner-size",
        type=int,
        default=460,
        help="Target inner bounding size for artwork (default: 460).",
    )
    parser.add_argument(
        "--no-aliases",
        action="store_true",
        help="Do not create common acronym alias files (e.g. gce.png, gke.png).",
    )

    args = parser.parse_args()

    normalize_all_gcp_icons(
        src_dir=args.src_dir,
        dest_dir=args.dest_dir,
        target_size=args.size,
        inner_size=args.inner_size,
        create_aliases=not args.no_aliases,
    )


if __name__ == "__main__":
    main()
