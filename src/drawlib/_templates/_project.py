# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Project scaffolding and template expansion engine for Drawlib."""

from __future__ import annotations

import importlib.resources
from importlib.resources.abc import Traversable
from pathlib import Path
from typing import Final, Literal, Optional

from drawlib._templates._css import get_css
from drawlib._templates._models import ProjectPaths
from drawlib._templates.langs import get_font_replacements, normalize_language

PROJECT_TYPES: Final[dict[str, str]] = {
    "doc": "Single specification, RFC, or multi-chapter technical report compiled to HTML and PDF.",
    "site": "Multi-page documentation website with sidebar navigation and search.",
    "slide": "16:9 presentation slide deck with modular SmartArts and vector diagrams.",
    "images": "Standalone Python illustration scripts compiled into images.",
}

_CANONICAL_TYPE_MAP: Final[dict[str, str]] = {
    "doc": "doc",
    "site": "site",
    "slide": "slide",
    "images": "images",
    "image": "images",
}


def list_project_types() -> dict[str, str]:
    """Return available project types and their descriptions.

    Returns:
        dict[str, str]: Mapping of project type name to description.
    """
    return dict(PROJECT_TYPES)


def resolve_project_paths(
    project_type: str,
    target: Optional[str] = None,
    destination: str | Path = ".",
) -> ProjectPaths:
    """Resolve project directory names and output paths into a structured ProjectPaths object.

    Args:
        project_type: Project type name ('doc', 'site', 'slide', 'images', 'image').
        target: Custom base name for the project (e.g. 'spec', 'report', 'docs').
            If None, defaults to canonical type name ('doc', 'docs', 'slide', 'images').
        destination: Base directory path where <target>_src will be created (defaults to current dir).

    Returns:
        ProjectPaths: Data object containing all resolved directory paths and artifact names.
    """
    normalized_type = project_type.strip().lower()
    canonical_type = _CANONICAL_TYPE_MAP.get(normalized_type, normalized_type)

    if target is not None and target.strip():
        base_name = target.strip().rstrip("/\\")
        if base_name.endswith("_src"):
            base_name = base_name[:-4]
    elif canonical_type == "site":
        base_name = "docs"
    elif canonical_type in {"images", "image"}:
        base_name = "images"
    elif canonical_type == "slide":
        base_name = "slide"
    elif canonical_type == "doc":
        base_name = "doc"
    else:
        base_name = canonical_type

    base_dir = Path(destination).resolve()
    src_dir_name = f"{base_name}_src"
    src_dir = base_dir / src_dir_name

    out_markdown_dir_name = f"{base_name}_markdown"
    out_images_dir_name = base_name if canonical_type == "images" else f"{base_name}_images"
    out_html_dir_name = f"{base_name}_html"
    out_pdf_name = f"{base_name}.pdf"

    return ProjectPaths(
        project_type=canonical_type,
        target=base_name,
        base_dir=base_dir,
        src_dir=src_dir,
        src_dir_name=src_dir_name,
        out_markdown_dir_name=out_markdown_dir_name,
        out_images_dir_name=out_images_dir_name,
        out_html_dir_name=out_html_dir_name,
        out_pdf_name=out_pdf_name,
    )


def _validate_slide_style(utils_root: Traversable, style: str) -> None:
    """Validate that the requested slide style has a corresponding utils template.

    Args:
        utils_root: Traversable root for slide utils templates.
        style: Theme style name to validate.

    Raises:
        ValueError: If the style template file does not exist.
    """
    template_path = utils_root.joinpath(f"{style}.py.template")
    if not template_path.is_file():
        available: list[str] = []
        if utils_root.is_dir():
            available = sorted(
                f.name[:-12]
                for f in utils_root.iterdir()
                if f.name.endswith(".py.template")
            )
        raise ValueError(
            f"Unsupported slide style '{style}'. Available styles: {', '.join(available)}"
        )


def _validate_conflicts(src_dir: Path, force: bool) -> None:
    """Validate that target source folder does not conflict with existing files."""
    if force:
        return
    if src_dir.exists():
        raise FileExistsError(
            f"Target source directory '{src_dir}' already exists. Use force=True / --force to overwrite."
        )


def _copy_item_with_substitutions(
    src: Traversable,
    dst: Path,
    replacements: dict[str, str],
    created_files: list[Path],
) -> None:
    """Recursively copy template file or directory with variable substitutions."""
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


def _copy_shared_assets(
    src_dir: Path,
    replacements: dict[str, str],
    created_files: list[Path],
) -> None:
    """Copy shared static assets from project/_assets into target project."""
    shared_assets_root = importlib.resources.files("drawlib._templates").joinpath("project", "_assets")
    if shared_assets_root.is_dir():
        _copy_item_with_substitutions(shared_assets_root, src_dir / "_assets", replacements, created_files)


def _deploy_stylesheet(
    project_type: str,
    src_dir: Path,
    style: Optional[str],
    created_files: list[Path],
    lang: str = "en",
) -> None:
    """Deploy custom or synthesized style.css."""
    if project_type in {"site", "doc", "slide"}:
        target: Literal["site", "doc", "slide"] = (
            "site" if project_type == "site" else ("doc" if project_type == "doc" else "slide")
        )
        css_content = get_css(name=style or "default", target=target, lang=lang)
        style_css_target = src_dir / "style.css"
        style_css_target.write_text(css_content, encoding="utf-8")
        if style_css_target not in created_files:
            created_files.append(style_css_target)


def _deploy_shared_templates(
    project_base: Traversable,
    src_dir: Path,
    replacements: dict[str, str],
    created_files: list[Path],
    project_type: str = "",
) -> None:
    """Deploy default shared files (_shared/styles.py.template, _shared/utils.py)."""
    shared_root = project_base.joinpath("_shared")
    if not shared_root.is_dir():
        return
    for item in shared_root.iterdir():
        if item.name in {"__pycache__", "output_html_readme.md"} or item.name.startswith("."):
            continue
        if project_type == "slide" and item.name == "utils.py":
            continue
        _copy_item_with_substitutions(item, src_dir / item.name, replacements, created_files)


def _deploy_slide_utils(
    utils_root: Traversable,
    src_dir: Path,
    style: str,
    replacements: dict[str, str],
    created_files: list[Path],
) -> None:
    """Deploy style-specific utils.py for slide projects."""
    _validate_slide_style(utils_root, style)
    template_path = utils_root.joinpath(f"{style}.py.template")
    _copy_item_with_substitutions(template_path, src_dir / "utils.py", replacements, created_files)


def _deploy_type_root_files(
    type_root: Traversable,
    src_dir: Path,
    replacements: dict[str, str],
    created_files: list[Path],
) -> None:
    """Deploy type-specific root files (build scripts, template.html, etc.)."""
    for item in type_root.iterdir():
        if item.name in {"docs", "utils", "__pycache__", "output_readme.md"} or item.name.startswith("."):
            continue
        _copy_item_with_substitutions(item, src_dir / item.name, replacements, created_files)


def _deploy_localized_docs(
    type_root: Traversable,
    src_dir: Path,
    selected_lang: str,
    replacements: dict[str, str],
    created_files: list[Path],
) -> None:
    """Deploy localized documents and samples (<type>/docs/<lang>/)."""
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
        _copy_item_with_substitutions(item, src_dir / item.name, replacements, created_files)


def init_project(
    project_type: str,
    destination: str | Path = ".",
    target: Optional[str] = None,
    output: Optional[str] = None,
    force: bool = False,
    lang: str = "en",
    style: Optional[str] = None,
    here: bool = False,
) -> list[Path]:
    """Scaffold a starter Drawlib project in the target destination directory.

    Args:
        project_type: Project type ('doc', 'site', 'slide', 'images', 'image').
        destination: Base directory path where <target>_src is created (defaults to current dir).
        target: Custom base name for the project (e.g. 'spec', 'report', 'docs').
        output: Legacy alias for target (e.g. 'rbac' creates 'rbac_src/').
        force: If True, overwrite existing files and directories.
        lang: Language for starter templates ('en', 'ja', etc.). Defaults to 'en'.
        style: Style preset theme ('default', 'google', 'monochrome', etc.) or custom CSS file path.
        here: Deprecated legacy option. Ignored when target_src is always created.

    Returns:
        list[Path]: List of created project file paths.

    Raises:
        ValueError: If project_type, lang, or style is invalid.
        FileExistsError: If destination directory contains conflicting files and force is False.
        FileNotFoundError: If template resources for the project type cannot be found.
    """
    raw_type = project_type.strip().lower()
    if raw_type not in _CANONICAL_TYPE_MAP:
        types_str = ", ".join(PROJECT_TYPES.keys())
        raise ValueError(f"Unknown project type '{project_type}'. Available types: {types_str}")

    canonical_type = _CANONICAL_TYPE_MAP[raw_type]
    selected_lang = normalize_language(lang)
    resolved_style = (style or "default").strip()
    effective_target = target if target is not None else output

    paths = resolve_project_paths(
        project_type=canonical_type,
        target=effective_target,
        destination=destination,
    )

    project_base = importlib.resources.files("drawlib._templates").joinpath("project")

    # Handle image vs images directory fallback
    type_dir_name = canonical_type
    type_root = project_base.joinpath(type_dir_name)
    if not type_root.is_dir() and canonical_type == "images":
        type_dir_name = "image"
        type_root = project_base.joinpath(type_dir_name)

    if not type_root.is_dir():
        raise FileNotFoundError(f"Template directory for '{canonical_type}' not found.")

    utils_root = project_base.joinpath("slide", "utils")
    if canonical_type == "slide":
        _validate_slide_style(utils_root, resolved_style)

    _validate_conflicts(src_dir=paths.src_dir, force=force)

    replacements = {
        "__SRC_DIR__": paths.src_dir_name,
        "__OUT_DIR__": paths.out_markdown_dir_name,
        "__OUT_MARKDOWN_DIR__": paths.out_markdown_dir_name,
        "__OUT_IMAGES_DIR__": paths.out_images_dir_name,
        "__OUT_HTML_DIR__": paths.out_html_dir_name,
        "__OUT_PDF__": paths.out_pdf_name,
        **get_font_replacements(selected_lang, style_theme=resolved_style),
    }

    created_files: list[Path] = []
    _deploy_shared_templates(
        project_base, paths.src_dir, replacements, created_files, project_type=canonical_type
    )
    if canonical_type == "slide":
        _deploy_slide_utils(utils_root, paths.src_dir, resolved_style, replacements, created_files)
    _deploy_type_root_files(type_root, paths.src_dir, replacements, created_files)
    _deploy_localized_docs(type_root, paths.src_dir, selected_lang, replacements, created_files)
    _copy_shared_assets(paths.src_dir, replacements, created_files)
    _deploy_stylesheet(canonical_type, paths.src_dir, resolved_style, created_files, lang=selected_lang)

    return sorted(created_files)
