# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Common infrastructure and utilities for drawlib builders."""

from __future__ import annotations

from drawlib._builder._common.cache import (
    BuildImageCache,
    CliImageCache,
    hash_file,
    hash_text,
)
from drawlib._builder._common.cache_manager import (
    clear_cache,
    clear_image_cache,
    download_cache,
    list_cache,
)
from drawlib._builder._common.progress import (
    BAR_WIDTH,
    FileBuildProgress,
    format_duplicate_output_error,
    format_progress_line,
)
from drawlib._builder._common.styles_loader import (
    load_styles,
    load_styles_and_utils,
    load_utils,
    resolve_styles_and_utils,
)

__all__ = [
    "BAR_WIDTH",
    "BuildImageCache",
    "CliImageCache",
    "FileBuildProgress",
    "clear_cache",
    "clear_image_cache",
    "download_cache",
    "format_duplicate_output_error",
    "format_progress_line",
    "hash_file",
    "hash_text",
    "list_cache",
    "load_styles",
    "load_styles_and_utils",
    "load_utils",
    "resolve_styles_and_utils",
]
