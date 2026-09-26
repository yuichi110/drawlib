# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.
"""Markdown exporter for writing rendered Markdown files with embedded images."""

import os


def write_rendered_markdown(rendered_markdown: str, output_path: str) -> None:
    """Write rendered Markdown text to the specified output file path.

    Args:
        rendered_markdown (str): Processed Markdown string.
        output_path (str): Target output file path.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered_markdown)
