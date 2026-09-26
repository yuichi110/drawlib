# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Public illustration block export module for drawlib.tools."""

from __future__ import annotations

from drawlib._builder.doc_builder import export_code_block

export_block = export_code_block

__all__ = [
    "export_block",
    "export_code_block",
]
