# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Data models for Drawlib template and project initialization."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProjectPaths:
    """Resolved file system paths and directory names for a scaffolded project.

    Attributes:
        project_type: Canonical project type ('doc', 'site', 'slide', 'images').
        target: Base name for the project and artifacts (e.g. 'doc', 'spec', 'docs').
        base_dir: Base directory where <target>_src is created.
        src_dir: Full resolved path to the source folder (<base_dir>/<target>_src).
        src_dir_name: Source folder name ('<target>_src').
        out_markdown_dir_name: Target markdown export directory name.
        out_images_dir_name: Target images export directory name.
        out_html_dir_name: Target HTML export directory name.
        out_pdf_name: Target PDF export filename.
    """

    project_type: str
    target: str
    base_dir: Path
    src_dir: Path
    src_dir_name: str
    out_markdown_dir_name: str
    out_images_dir_name: str
    out_html_dir_name: str
    out_pdf_name: str
