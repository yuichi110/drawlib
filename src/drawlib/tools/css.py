# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Public HTML and PDF CSS preset management module for drawlib.tools."""

from __future__ import annotations

from drawlib._css_templates import (
    export_css,
    get_css,
    list_css,
    list_html_css,
    list_pdf_css,
)

export = export_css
list = list_css  # noqa: A001

__all__ = [
    "export",
    "export_css",
    "get_css",
    "list",
    "list_css",
    "list_html_css",
    "list_pdf_css",
]
