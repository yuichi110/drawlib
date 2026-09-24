# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Project scaffolding implementation for drawlib init command."""

from __future__ import annotations

import importlib.resources
from importlib.resources.abc import Traversable
from pathlib import Path
from typing import Final

PROJECT_TYPES: Final[dict[str, str]] = {
    "simple": "Single Markdown document compiled to Markdown and standalone HTML.",
    "site": "Multi-page documentation website with sidebar navigation.",
    "pdf": "Multi-chapter report/document compiled into a single PDF with Table of Contents.",
}


def list_project_types() -> dict[str, str]:
    """Return available project types and their descriptions.

    Returns:
        dict[str, str]: Mapping of project type name to description.
    """
    return dict(PROJECT_TYPES)


def _validate_destination(dest_path: Path, force: bool, here: bool = False) -> None:
    """Validate destination directory before scaffolding.

    Args:
        dest_path: Resolved target path.
        force: Whether to overwrite existing files.
        here: If True, allow non-empty directory but check for conflicting drawlib files.

    Raises:
        FileExistsError: If destination contains conflicting files and force is False.
    """
    if not dest_path.exists():
        return

    if here:
        if (dest_path / "docs_src").exists() and not force:
            raise FileExistsError(
                f"Directory '{dest_path / 'docs_src'}' already exists. Use force=True to overwrite."
            )
        return

    existing_items = [p for p in dest_path.iterdir() if p.name != ".git"]
    if existing_items and not force:
        raise FileExistsError(
            f"Destination directory '{dest_path}' is not empty. Use force=True to overwrite."
        )


def _copy_item(src: Traversable, dst: Path, created_files: list[Path]) -> None:
    """Recursively copy template file or directory.

    Args:
        src: Source traversable template resource.
        dst: Target destination filesystem path.
        created_files: Mutable list collecting paths of created files.
    """
    if src.is_dir():
        dst.mkdir(parents=True, exist_ok=True)
        for item in src.iterdir():
            if item.name == "__pycache__" or item.name.startswith("."):
                continue
            _copy_item(item, dst / item.name, created_files)
        return

    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(src.read_bytes())
    if dst.name.endswith(".sh"):
        try:
            dst.chmod(dst.stat().st_mode | 0o755)
        except OSError:
            pass
    created_files.append(dst)


def init_project(
    project_type: str,
    destination: str | Path = ".",
    force: bool = False,
    here: bool = False,
) -> list[Path]:
    """Scaffold a starter drawlib project into the destination directory.

    Args:
        project_type: Project type ('simple', 'site', 'pdf').
        destination: Destination directory path (defaults to current directory).
        force: If True, overwrite existing files in destination directory.
        here: If True, deploy directly into current directory without checking for other project files.

    Returns:
        list[Path]: List of created project file paths.

    Raises:
        ValueError: If project_type is not a recognized type.
        FileExistsError: If destination directory contains conflicting files and force is False.
        FileNotFoundError: If template resources for the project type cannot be found.
    """
    selected_type = project_type.strip().lower()
    if selected_type not in PROJECT_TYPES:
        types_str = ", ".join(PROJECT_TYPES.keys())
        raise ValueError(f"Unknown project type '{project_type}'. Available types: {types_str}")

    target = Path(".") if here else Path(destination)
    dest_path = target.resolve()
    _validate_destination(dest_path, force=force, here=here)

    template_root = importlib.resources.files("drawlib._project_templates").joinpath(selected_type)
    if not template_root.is_dir():
        raise FileNotFoundError(f"Template directory for '{selected_type}' not found.")

    created_files: list[Path] = []
    for item in template_root.iterdir():
        if item.name == "__pycache__" or item.name.startswith("."):
            continue
        _copy_item(item, dest_path / item.name, created_files)

    return sorted(created_files)
