# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Shared utilities for MS Office (.docx / .pptx) document exporters."""

from __future__ import annotations

import contextlib
import datetime
import hashlib
import os
import tempfile
import zipfile
from typing import Literal

_NATIVE_OFFICE_IMAGE_EXTS: frozenset[str] = frozenset(
    {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tif", ".tiff"}
)

StaticFrameSpec = Literal["first", "last"] | int


def parse_static_frame(
    value: Literal["first", "last"] | int | str,
    *,
    param_name: str = "static_frame",
) -> StaticFrameSpec:
    """Validate and normalize a static frame specification ('first', 'last', or int).

    Args:
        value: Frame selector ('first', 'last', integer index, or integer string).
        param_name: Parameter name used in error messages.

    Returns:
        StaticFrameSpec: Normalized 'first', 'last', or integer frame index.

    Raises:
        ValueError: If value is not 'first', 'last', or a valid integer.
    """
    if isinstance(value, bool):
        raise ValueError(f"{param_name} must be 'first', 'last', or an integer frame index.")
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        cleaned = value.strip().lower()
        if cleaned == "first":
            return "first"
        if cleaned == "last":
            return "last"
        try:
            return int(cleaned)
        except ValueError as e:
            raise ValueError(f"{param_name} must be 'first', 'last', or an integer frame index.") from e
    raise ValueError(f"{param_name} must be 'first', 'last', or an integer frame index.")


def resolve_target_frame_index(n_frames: int, static_frame: StaticFrameSpec) -> int:
    """Resolve a 0-based frame index within [0, max(0, n_frames - 1)].

    Args:
        n_frames: Total number of frames in the image (>= 1).
        static_frame: 'first', 'last', or integer index (supports negative Python-style indexing).

    Returns:
        int: Clamped 0-based frame index.
    """
    if n_frames <= 1:
        return 0
    if isinstance(static_frame, str):
        return (n_frames - 1) if static_frame == "last" else 0
    idx = int(static_frame)
    if idx < 0:
        idx = n_frames + idx
    return max(0, min(n_frames - 1, idx))


def resolve_office_datetime(*, timestamp: bool = False) -> datetime.datetime:
    """Resolve UTC timestamp for OpenXML core_properties metadata.

    Args:
        timestamp: If True, return the current UTC datetime. If False (default),
            return a deterministic datetime (respecting SOURCE_DATE_EPOCH if set).

    Returns:
        datetime.datetime: Timezone-aware UTC datetime object.
    """
    if timestamp:
        return datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)

    source_date_epoch = os.environ.get("SOURCE_DATE_EPOCH")
    if source_date_epoch:
        with contextlib.suppress(ValueError, OverflowError, OSError):
            epoch_val = int(source_date_epoch)
            return datetime.datetime.fromtimestamp(epoch_val, tz=datetime.timezone.utc).replace(microsecond=0)

    return datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)


def normalize_opc_zip_timestamps(file_path: str) -> None:
    """Normalize ZIP entry modification timestamps inside an OpenXML (.docx/.pptx) archive.

    Args:
        file_path: Path to the generated .docx or .pptx file.
    """
    if not os.path.isfile(file_path):
        return

    dt = resolve_office_datetime(timestamp=False)
    year = max(dt.year, 1980)
    zip_dt = (year, dt.month, dt.day, dt.hour, dt.minute, dt.second)

    parent_dir = os.path.dirname(os.path.abspath(file_path)) or "."
    fd, tmp_path = tempfile.mkstemp(suffix=".opc_tmp", dir=parent_dir)
    os.close(fd)
    try:
        with zipfile.ZipFile(file_path, "r") as zin, zipfile.ZipFile(
            tmp_path, "w", compression=zipfile.ZIP_DEFLATED
        ) as zout:
            for item in sorted(zin.infolist(), key=lambda info: info.filename):
                data = zin.read(item.filename)
                new_info = zipfile.ZipInfo(filename=item.filename, date_time=zip_dt)
                new_info.compress_type = zipfile.ZIP_DEFLATED
                new_info.external_attr = 0o644 << 16
                zout.writestr(new_info, data)
        os.replace(tmp_path, file_path)
    except Exception:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise


def ensure_static_office_image(
    image_path: str,
    scratch_dir: str,
    *,
    static_frame: Literal["first", "last"] | int | str = "last",
) -> tuple[str, int, int]:
    """Ensure an image file is a single-frame Office-compatible raster image and return its dimensions.

    Animated images (APNG / Animated WebP / GIF with multiple frames) or formats unsupported
    by python-docx / python-pptx (such as .webp or .apng) are converted into a static PNG
    inside scratch_dir.

    Args:
        image_path: Path to source image file.
        scratch_dir: Temporary directory for converted static PNG files.
        static_frame: Which frame ('first', 'last', or integer index) to extract when animated.

    Returns:
        tuple[str, int, int]: (usable_image_path, pixel_width, pixel_height).
    """
    from PIL import Image  # noqa: PLC0415

    resolved_frame = parse_static_frame(static_frame)
    abs_path = os.path.abspath(image_path)
    ext = os.path.splitext(abs_path)[1].lower()

    with Image.open(abs_path) as img:
        n_frames = int(getattr(img, "n_frames", 1) or 1)
        is_animated = bool(getattr(img, "is_animated", False) and n_frames > 1)
        needs_conversion = is_animated or ext not in _NATIVE_OFFICE_IMAGE_EXTS

        if not needs_conversion:
            return abs_path, int(img.width), int(img.height)

        target_frame = resolve_target_frame_index(n_frames, resolved_frame) if is_animated else 0
        if is_animated and target_frame > 0:
            img.seek(target_frame)

        converted = img.convert("RGBA")
        width, height = int(converted.width), int(converted.height)

        os.makedirs(scratch_dir, exist_ok=True)
        digest = hashlib.sha256(
            f"{abs_path}:{resolved_frame}:{os.path.getsize(abs_path)}".encode("utf-8")
        ).hexdigest()[:12]
        stem = os.path.splitext(os.path.basename(abs_path))[0]
        out_png = os.path.join(scratch_dir, f"{stem}_{digest}.png")
        converted.save(out_png, format="PNG")
        return out_png, width, height
