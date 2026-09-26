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
import logging
import os
from importlib.resources.abc import Traversable
from pathlib import Path
from typing import Final, Literal, Optional

from drawlib._tools.doc_builder import build_html, build_markdown, build_pdf
from drawlib._tools.doc_builder.exporter_html import get_default_css
from drawlib._tools.image_builder import build_image

logger = logging.getLogger(__name__)

PROJECT_TYPES: Final[dict[str, str]] = {
    "site": "Multi-page documentation website with sidebar navigation.",
    "simple": "Single Markdown document compiled to Markdown and standalone HTML.",
    "pdf": "Multi-chapter report/document compiled into a single PDF with Table of Contents.",
    "image": "Standalone Python illustration scripts compiled into images.",
}


def list_project_types() -> dict[str, str]:
    """Return available project types and their descriptions.

    Returns:
        dict[str, str]: Mapping of project type name to description.
    """
    return dict(PROJECT_TYPES)


def _validate_conflicts(
    src_path: Path,
    expected_outputs: list[Path],
    force: bool,
    here: bool,
    no_build: bool,
) -> None:
    """Validate that neither the source folder nor expected output targets conflict.

    Args:
        src_path: Resolved target source directory path.
        expected_outputs: List of expected build output destinations.
        force: Whether to overwrite existing files.
        here: If True, deploy directly into destination without creating subfolder.
        no_build: If True, initial build outputs will not be generated.

    Raises:
        FileExistsError: If destination contains conflicting files and force is False.
    """
    if force:
        return

    if here:
        critical_items = [
            src_path / "build.sh",
            src_path / "config.py",
            src_path / "README.md",
            src_path / "style.css",
            src_path / "template.html",
        ]
        conflicts = [p for p in critical_items if p.exists()]
        if conflicts:
            conflicts_str = ", ".join(f"'{p.name}'" for p in conflicts)
            raise FileExistsError(
                f"Destination '{src_path}' already contains project files ({conflicts_str}). "
                "Use force=True / --force to overwrite."
            )
        return

    if src_path.exists():
        raise FileExistsError(
            f"Target source directory '{src_path}' already exists. Use force=True / --force to overwrite."
        )

    if not no_build:
        for out_path in expected_outputs:
            if out_path.exists():
                raise FileExistsError(
                    f"Build output destination '{out_path}' already exists. "
                    "Use force=True / --force to overwrite."
                )


def _copy_item_with_substitutions(
    src: Traversable,
    dst: Path,
    replacements: dict[str, str],
    created_files: list[Path],
) -> None:
    """Recursively copy template file or directory with variable substitutions.

    Args:
        src: Source traversable template resource.
        dst: Target destination filesystem path.
        replacements: Placeholder replacements mapping.
        created_files: Mutable list collecting paths of created files.
    """
    if src.is_dir():
        dst.mkdir(parents=True, exist_ok=True)
        for item in src.iterdir():
            if item.name == "__pycache__" or item.name.startswith("."):
                continue
            _copy_item_with_substitutions(item, dst / item.name, replacements, created_files)
        return

    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.suffix in {".sh", ".md", ".txt"}:
        content = src.read_text(encoding="utf-8")
        for key, val in replacements.items():
            content = content.replace(key, val)
        dst.write_text(content, encoding="utf-8")
    else:
        dst.write_bytes(src.read_bytes())

    if dst.name.endswith(".sh"):
        try:
            dst.chmod(dst.stat().st_mode | 0o755)
        except OSError:
            pass
    created_files.append(dst)


def _resolve_project_paths(
    selected_type: str,
    output: Optional[str],
    destination: str | Path,
    here: bool,
) -> tuple[Path, Path, str, str, str, str, list[Path]]:
    """Resolve project directory names and expected output paths."""
    if output is not None and output.strip():
        base_name = output.strip().rstrip("/\\")
        if base_name.endswith("_src"):
            base_name = base_name[:-4]
    elif selected_type == "image":
        base_name = "images"
    elif selected_type == "pdf":
        base_name = "doc"
    else:
        base_name = "docs"

    src_dir_name = f"{base_name}_src"
    parent_dest = Path(destination).resolve()
    src_path = parent_dest if here else parent_dest / src_dir_name

    out_dir_name = base_name
    out_html_dir_name = f"{base_name}_html"
    out_pdf_name = f"{base_name}.pdf"

    expected_outputs: list[Path] = []
    if selected_type in {"site", "simple"}:
        expected_outputs = [parent_dest / out_html_dir_name, parent_dest / out_dir_name]
    elif selected_type == "pdf":
        expected_outputs = [parent_dest / out_pdf_name]
    elif selected_type == "image":
        expected_outputs = [parent_dest / out_dir_name]

    return (
        parent_dest,
        src_path,
        src_dir_name,
        out_dir_name,
        out_html_dir_name,
        out_pdf_name,
        expected_outputs,
    )


def _resolve_template_root(selected_type: str, lang: str = "en") -> Traversable:
    """Resolve importlib resources template root directory."""
    type_key = f"{selected_type}_ja" if lang == "ja" else selected_type
    if selected_type in {"site", "simple", "pdf"}:
        root = importlib.resources.files("drawlib._project_templates.docs_src").joinpath(type_key)
    else:
        root = importlib.resources.files("drawlib._project_templates.images_src").joinpath(type_key)

    if not root.is_dir():
        raise FileNotFoundError(f"Template directory for '{type_key}' not found.")
    return root


def init_project(
    project_type: str,
    destination: str | Path = ".",
    output: Optional[str] = None,
    force: bool = False,
    here: bool = False,
    no_build: bool = False,
    lang: Literal["en", "ja"] | str = "en",
    css: Optional[str] = None,
) -> list[Path]:
    """Scaffold a starter drawlib project and optionally run initial compilation.

    Args:
        project_type: Project type ('site', 'simple', 'pdf', 'image').
        destination: Parent destination directory path (defaults to current directory).
        output: Custom artifact/project name (defaults to 'docs' or 'images').
        force: If True, overwrite existing files and directories.
        here: If True, deploy directly into destination without creating <name>_src subfolder.
        no_build: If True, skip executing initial build after scaffolding.
        lang: Language for starter templates ('en' or 'ja'). Defaults to 'en'.
        css: CSS preset theme ('default', 'google', 'github', etc.) or custom CSS file path.

    Returns:
        list[Path]: List of created project file paths.

    Raises:
        ValueError: If project_type, lang, or css is invalid.
        FileExistsError: If destination directory or output targets conflict and force is False.
        FileNotFoundError: If template resources for the project type cannot be found.
    """
    selected_type = project_type.strip().lower()
    if selected_type not in PROJECT_TYPES:
        types_str = ", ".join(PROJECT_TYPES.keys())
        raise ValueError(f"Unknown project type '{project_type}'. Available types: {types_str}")

    selected_lang = lang.strip().lower()
    if selected_lang not in {"en", "ja"}:
        raise ValueError(f"Unsupported language '{lang}'. Supported languages: 'en', 'ja'")

    (
        parent_dest,
        src_path,
        src_dir_name,
        out_dir_name,
        out_html_dir_name,
        out_pdf_name,
        expected_outputs,
    ) = _resolve_project_paths(selected_type, output, destination, here)

    _validate_conflicts(
        src_path=src_path,
        expected_outputs=expected_outputs,
        force=force,
        here=here,
        no_build=no_build,
    )

    template_root = _resolve_template_root(selected_type, lang=selected_lang)

    replacements = {
        "__SRC_DIR__": "." if here else src_dir_name,
        "__OUT_DIR__": out_dir_name,
        "__OUT_HTML_DIR__": out_html_dir_name,
        "__OUT_PDF__": out_pdf_name,
    }

    created_files: list[Path] = []
    for item in template_root.iterdir():
        if item.name == "__pycache__" or item.name.startswith("."):
            continue
        _copy_item_with_substitutions(item, src_path / item.name, replacements, created_files)

    if selected_type in {"site", "simple"}:
        css_theme = css or "default"
        css_content = get_default_css(custom_css_path=css_theme, target="html")
        style_css_target = src_path / "style.css"
        style_css_target.write_text(css_content, encoding="utf-8")
        if style_css_target not in created_files:
            created_files.append(style_css_target)
    elif selected_type == "pdf":
        css_theme = css or "default"
        css_content = get_default_css(custom_css_path=css_theme, target="pdf")
        style_css_target = src_path / "style.css"
        style_css_target.write_text(css_content, encoding="utf-8")
        if style_css_target not in created_files:
            created_files.append(style_css_target)

    if not no_build:
        _run_initial_build(
            project_type=selected_type,
            src_path=src_path,
            parent_dest=parent_dest,
            out_dir_name=out_dir_name,
            out_html_dir_name=out_html_dir_name,
            out_pdf_name=out_pdf_name,
        )

    return sorted(created_files)


def _run_initial_build(
    project_type: str,
    src_path: Path,
    parent_dest: Path,
    out_dir_name: str,
    out_html_dir_name: str,
    out_pdf_name: str,
) -> None:
    """Execute initial compilation for the scaffolded project.

    Args:
        project_type: Project type ('site', 'simple', 'pdf', 'image').
        src_path: Target source directory.
        parent_dest: Destination parent directory.
        out_dir_name: Base output directory name.
        out_html_dir_name: HTML output directory name.
        out_pdf_name: PDF output file name.
    """
    orig_cwd = os.getcwd()
    try:
        os.chdir(str(parent_dest))
        src_str = str(src_path.resolve())

        if project_type == "site":
            build_markdown(input_path=src_str, output=out_dir_name, no_cache=True)
            build_html(input_path=src_str, output=out_html_dir_name, no_cache=True)
        elif project_type == "simple":
            doc_file = os.path.join(src_str, "doc.md")
            if os.path.isfile(doc_file):
                build_markdown(input_path=doc_file, output=os.path.join(out_dir_name, "doc.md"), no_cache=True)
                build_html(input_path=doc_file, output=os.path.join(out_html_dir_name, "doc.html"), no_cache=True)
            else:
                build_markdown(input_path=src_str, output=out_dir_name, no_cache=True)
                build_html(input_path=src_str, output=out_html_dir_name, no_cache=True)
        elif project_type == "pdf":
            try:
                build_pdf(inputs=src_str, output=out_pdf_name, generate_index=True, no_cache=True)
            except Exception as exc:
                logger.warning(f"Initial PDF build skipped (PDF engine issue): {exc}")
        elif project_type == "image":
            build_image(inputs=src_str, output=out_dir_name, no_cache=True)
    finally:
        os.chdir(orig_cwd)
