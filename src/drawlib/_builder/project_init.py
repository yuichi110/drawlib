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
from typing import Final, Optional

from drawlib._css_templates import get_css
from drawlib._langs import get_font_replacements, normalize_language

PROJECT_TYPES: Final[dict[str, str]] = {
    "site": "Multi-page documentation website with sidebar navigation.",
    "simple": "Single Markdown document compiled to Markdown and standalone HTML.",
    "pdf": "Multi-chapter report/document compiled into a single PDF with Table of Contents.",
    "slide": "HTML presentation slide deck with modular SmartArts and vector diagrams.",
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
    force: bool,
    here: bool,
) -> None:
    """Validate that target source folder or destination files do not conflict.

    Args:
        src_path: Resolved target source directory path.
        force: Whether to overwrite existing files.
        here: If True, deploy directly into destination without creating subfolder.

    Raises:
        FileExistsError: If destination contains conflicting files and force is False.
    """
    if force:
        return

    if here:
        critical_items = [
            src_path / "build.sh",
            src_path / "serve.sh",
            src_path / "styles.py",
            src_path / "utils.py",
            src_path / "README.md",
            src_path / "style.css",
            src_path / "slide.css",
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
    if dst.name.endswith(".template"):
        dst = dst.with_name(dst.name[:-9])

    if dst.suffix in {".sh", ".md", ".txt", ".html", ".css", ".py"}:
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
    if dst not in created_files:
        created_files.append(dst)


def _resolve_project_paths(
    selected_type: str,
    output: Optional[str],
    destination: str | Path,
    here: bool,
) -> tuple[Path, Path, str, str, str, str]:
    """Resolve project directory names and output paths."""
    if output is not None and output.strip():
        base_name = output.strip().rstrip("/\\")
        if base_name.endswith("_src"):
            base_name = base_name[:-4]
    elif selected_type == "image":
        base_name = "images"
    elif selected_type == "pdf":
        base_name = "doc"
    elif selected_type == "slide":
        base_name = "slide"
    else:
        base_name = "docs"

    src_dir_name = f"{base_name}_src"
    parent_dest = Path(destination).resolve()
    src_path = parent_dest if here else parent_dest / src_dir_name

    out_dir_name = base_name
    out_html_dir_name = f"{base_name}_html"
    out_pdf_name = f"{base_name}.pdf"

    return (
        parent_dest,
        src_path,
        src_dir_name,
        out_dir_name,
        out_html_dir_name,
        out_pdf_name,
    )


def _copy_shared_assets(
    src_path: Path,
    replacements: dict[str, str],
    created_files: list[Path],
) -> None:
    """Copy shared static assets from _project_templates/_assets into target project."""
    shared_assets_root = importlib.resources.files("drawlib._project_templates").joinpath("_assets")
    if shared_assets_root.is_dir():
        _copy_item_with_substitutions(shared_assets_root, src_path / "_assets", replacements, created_files)


def _deploy_stylesheet(
    selected_type: str,
    src_path: Path,
    style: Optional[str],
    created_files: list[Path],
    lang: str = "en",
) -> None:
    """Deploy custom or default style.css or slide.css for document/slide projects."""
    if selected_type in {"site", "simple", "pdf"}:
        target = "pdf" if selected_type == "pdf" else "html"
        css_content = get_css(name=style or "default", target=target, lang=lang)
        style_css_target = src_path / "style.css"
        style_css_target.write_text(css_content, encoding="utf-8")
        if style_css_target not in created_files:
            created_files.append(style_css_target)
    elif selected_type == "slide":
        css_content = get_css(name=style or "default", target="slide", lang=lang)
        slide_css_target = src_path / "slide.css"
        slide_css_target.write_text(css_content, encoding="utf-8")
        if slide_css_target not in created_files:
            created_files.append(slide_css_target)


def _deploy_shared_templates(
    templates_base: Traversable,
    src_path: Path,
    replacements: dict[str, str],
    created_files: list[Path],
) -> None:
    """Deploy default shared files (_shared/styles.py.template, _shared/utils.py).

    Args:
        templates_base: Base traversable of project templates.
        src_path: Target source directory.
        replacements: Placeholder substitution dictionary.
        created_files: Mutable list collecting created file paths.
    """
    shared_root = templates_base.joinpath("_shared")
    if not shared_root.is_dir():
        return
    for item in shared_root.iterdir():
        if item.name == "__pycache__" or item.name.startswith("."):
            continue
        _copy_item_with_substitutions(item, src_path / item.name, replacements, created_files)


def _deploy_type_root_files(
    type_root: Traversable,
    src_path: Path,
    replacements: dict[str, str],
    created_files: list[Path],
) -> None:
    """Deploy type-specific root files (build.sh, template.html, or overrides).

    Args:
        type_root: Traversable root of the selected project type.
        src_path: Target source directory.
        replacements: Placeholder substitution dictionary.
        created_files: Mutable list collecting created file paths.
    """
    for item in type_root.iterdir():
        if item.name in {"docs", "__pycache__"} or item.name.startswith("."):
            continue
        _copy_item_with_substitutions(item, src_path / item.name, replacements, created_files)


def _deploy_localized_docs(
    type_root: Traversable,
    src_path: Path,
    selected_lang: str,
    replacements: dict[str, str],
    created_files: list[Path],
) -> None:
    """Deploy localized documents and samples (<type>/docs/<lang>/, fallback to 'en').

    Args:
        type_root: Traversable root of the selected project type.
        src_path: Target source directory.
        selected_lang: Normalized language code.
        replacements: Placeholder substitution dictionary.
        created_files: Mutable list collecting created file paths.
    """
    docs_root = type_root.joinpath("docs")
    if not docs_root.is_dir():
        return

    lang_docs = docs_root.joinpath(selected_lang)
    if not lang_docs.is_dir():
        lang_docs = docs_root.joinpath("en")
    if not lang_docs.is_dir():
        return

    for item in lang_docs.iterdir():
        if item.name == "__pycache__" or item.name.startswith("."):
            continue
        _copy_item_with_substitutions(item, src_path / item.name, replacements, created_files)


def init_project(
    project_type: str,
    destination: str | Path = ".",
    output: Optional[str] = None,
    force: bool = False,
    here: bool = False,
    lang: str = "en",
    style: Optional[str] = None,
) -> list[Path]:
    """Scaffold a starter drawlib project.

    Args:
        project_type: Project type ('site', 'simple', 'pdf', 'image').
        destination: Parent destination directory path (defaults to current directory).
        output: Base project/artifact name (e.g. 'rbac' creates 'rbac_src' and targets 'rbac.pdf').
        force: If True, overwrite existing files and directories.
        here: If True, deploy directly into destination without creating <name>_src subfolder.
        lang: Language for starter templates ('en', 'ja', 'zh-cn', 'ko', etc.). Defaults to 'en'.
        style: Style preset theme ('default', 'google', 'monochrome', etc.) or custom CSS file path.

    Returns:
        list[Path]: List of created project file paths.

    Raises:
        ValueError: If project_type, lang, or style is invalid.
        FileExistsError: If destination directory contains conflicting files and force is False.
        FileNotFoundError: If template resources for the project type cannot be found.
    """
    selected_type = project_type.strip().lower()
    if selected_type not in PROJECT_TYPES:
        types_str = ", ".join(PROJECT_TYPES.keys())
        raise ValueError(f"Unknown project type '{project_type}'. Available types: {types_str}")

    selected_lang = normalize_language(lang)
    resolved_style = (style or "default").strip()

    (
        _parent_dest,
        src_path,
        src_dir_name,
        out_dir_name,
        out_html_dir_name,
        out_pdf_name,
    ) = _resolve_project_paths(selected_type, output, destination, here)

    _validate_conflicts(
        src_path=src_path,
        force=force,
        here=here,
    )

    templates_base = importlib.resources.files("drawlib._project_templates")
    type_root = templates_base.joinpath(selected_type)
    if not type_root.is_dir():
        raise FileNotFoundError(f"Template directory for '{selected_type}' not found.")

    replacements = {
        "__SRC_DIR__": "." if here else src_dir_name,
        "__OUT_DIR__": out_dir_name,
        "__OUT_HTML_DIR__": out_html_dir_name,
        "__OUT_PDF__": out_pdf_name,
        **get_font_replacements(selected_lang, style_theme=resolved_style),
    }

    created_files: list[Path] = []
    _deploy_shared_templates(templates_base, src_path, replacements, created_files)
    _deploy_type_root_files(type_root, src_path, replacements, created_files)
    _deploy_localized_docs(type_root, src_path, selected_lang, replacements, created_files)
    _copy_shared_assets(src_path, replacements, created_files)
    _deploy_stylesheet(selected_type, src_path, resolved_style, created_files, lang=selected_lang)

    return sorted(created_files)
