# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""File path type definitions for drawlib."""

from __future__ import annotations

import os
from typing import Annotated, Any

from pydantic import BeforeValidator

from drawlib._core.l1_core import get_script_relative_path


def resolve_file_path(v: Any) -> Any:  # noqa: ANN401
    """Normalize user-provided path to absolute path resolved relative to caller script.

    If an absolute path is provided, it is returned unchanged.
    If a relative path is provided, it is resolved relative to the user's caller script directory.
    Non-string and non-PathLike objects are returned unchanged so that Pydantic Unions
    (such as FilePath | Image.Image | Dimage) can fall through to other union variants.

    Args:
        v: File path string or PathLike object.

    Returns:
        Any: Absolute path string if input was a path, otherwise the original input.

    Raises:
        ValueError: If input is an empty string.
        FileNotFoundError: If the calling script cannot be detected when resolving a relative path.
    """
    if isinstance(v, os.PathLike):
        v = os.fspath(v)

    if not isinstance(v, str):
        return v

    path_str = v.strip()
    if not path_str:
        raise ValueError("File path cannot be empty.")

    return get_script_relative_path(path_str)


FilePath = Annotated[str, BeforeValidator(resolve_file_path)]
TypeFilePath = FilePath
