# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Public CSS preset management module for drawlib.tools."""

from __future__ import annotations

from drawlib._tools.doc_builder import export_css, list_css

list = list_css  # noqa: A001
export = export_css

__all__ = [
    "export",
    "export_css",
    "list",
    "list_css",
]
