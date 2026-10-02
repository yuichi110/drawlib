# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""External Python styles and utils loader for doc_builder and drawing blocks."""

from __future__ import annotations

from drawlib._builder._common.styles_loader import (
    load_styles,
    load_styles_and_utils,
    load_utils,
    resolve_styles_and_utils,
)

__all__ = [
    "load_styles",
    "load_styles_and_utils",
    "load_utils",
    "resolve_styles_and_utils",
]
