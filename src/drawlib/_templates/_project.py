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
from typing import Final, Literal

from drawlib._templates._css import get_css
from drawlib._templates._models import ProjectPaths
from drawlib._templates.langs import get_font_replacements, get_language_config, normalize_language

PROJECT_TYPES: Final[dict[str, str]] = {
    "doc": "Single specification, RFC, or multi-chapter technical report compiled to HTML and PDF.",
    "site": "Multi-page documentation website with sidebar navigation and search.",
    "catalog": "Multi-page searchable catalog & reference website with H1/H2 sidebar navigation and semantic badges.",
    "slide": "16:9 presentation slide deck with modular SmartArts and vector diagrams.",
    "images": "Standalone Python illustration scripts compiled into images.",
}

_CANONICAL_TYPE_MAP: Final[dict[str, str]] = {
    "doc": "doc",
    "site": "site",
    "catalog": "catalog",
    "slide": "slide",
    "images": "images",
    "image": "images",
}
_I18N_PROJECT_TYPES: Final[frozenset[str]] = frozenset({"doc", "site", "slide", "catalog"})


def list_project_types() -> dict[str, str]:
    """Return available project types and their descriptions.

    Returns:
        dict[str, str]: Mapping of project type name to description.
    """
    return dict(PROJECT_TYPES)


def _resolve_target_base_and_dir(
    canonical_type: str,
    target: str | None,
    destination: str | Path,
) -> tuple[str, Path]:
    """Resolve (base_name, base_dir) supporting subdirectory target paths like 'docs/mysite'."""
    dest_path = Path(destination)
    if target is not None and target.strip():
        cleaned = target.strip().rstrip("/\\").replace("\\", "/")
        if "/" in cleaned:
            parent_rel, leaf = cleaned.rsplit("/", 1)
            base_dir = (dest_path / parent_rel).resolve()
            base_name = leaf[:-4] if leaf.endswith("_src") else leaf
            return base_name, base_dir
        base_name = cleaned[:-4] if cleaned.endswith("_src") else cleaned
        return base_name, dest_path.resolve()

    default_names = {
        "site": "docs",
        "catalog": "catalog",
        "images": "images",
        "image": "images",
        "slide": "slide",
        "doc": "doc",
    }
    return default_names.get(canonical_type, canonical_type), dest_path.resolve()


def resolve_project_paths(
    project_type: str,
    target: str | None = None,
    destination: str | Path = ".",
) -> ProjectPaths:
    """Resolve project directory names and output paths into a structured ProjectPaths object.

    Args:
        project_type: Project type name ('doc', 'site', 'catalog', 'slide', 'images', 'image').
        target: Custom base name or relative path for the project (e.g. 'spec', 'docs/mysite').
            If None, defaults to canonical type name ('doc', 'docs', 'catalog', 'slide', 'images').
        destination: Base directory path where <target>_src will be created (defaults to current dir).

    Returns:
        ProjectPaths: Data object containing all resolved directory paths and artifact names.
    """
    normalized_type = project_type.strip().lower()
    canonical_type = _CANONICAL_TYPE_MAP.get(normalized_type, normalized_type)
    base_name, base_dir = _resolve_target_base_and_dir(canonical_type, target, destination)

    src_dir_name = f"{base_name}_src"
    src_dir = base_dir / src_dir_name

    out_markdown_dir_name = f"{base_name}_markdown"
    out_images_dir_name = base_name if canonical_type == "images" else f"{base_name}_images"
    out_html_dir_name = f"{base_name}_html"
    out_pdf_name = f"{base_name}.pdf"
    out_docx_name = f"{base_name}.docx"
    out_pptx_name = f"{base_name}.pptx"

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
        out_docx_name=out_docx_name,
        out_pptx_name=out_pptx_name,
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


def _resolve_stylesheet(
    project_type: str,
    style: str,
    lang: str = "en",
) -> str | None:
    """Resolve and validate stylesheet content for web/slide project types."""
    target_map: dict[str, Literal["site", "doc", "slide", "catalog"]] = {
        "site": "site",
        "doc": "doc",
        "slide": "slide",
        "catalog": "catalog",
    }
    target = target_map.get(project_type)
    if target is None:
        return None
    return get_css(name=style, target=target, lang=lang)


def _deploy_stylesheet(
    src_dir: Path,
    css_content: str | None,
    created_files: list[Path],
) -> None:
    """Write resolved style.css into target project directory."""
    if css_content is None:
        return
    style_css_target = src_dir / "style.css"
    style_css_target.write_text(css_content, encoding="utf-8")
    if style_css_target not in created_files:
        created_files.append(style_css_target)


def _deploy_shared_templates(
    project_base: Traversable,
    src_dir: Path,
    replacements: dict[str, str],
    created_files: list[Path],
) -> None:
    """Deploy default shared files (_shared/styles.py.template, _shared/utils.py)."""
    shared_root = project_base.joinpath("_shared")
    if not shared_root.is_dir():
        return
    for item in shared_root.iterdir():
        if item.name in {"__pycache__", "output_html_readme.md"} or item.name.startswith("."):
            continue
        _copy_item_with_substitutions(item, src_dir / item.name, replacements, created_files)


def _deploy_type_root_files(
    type_root: Traversable,
    src_dir: Path,
    replacements: dict[str, str],
    created_files: list[Path],
) -> None:
    """Deploy type-specific root files (build scripts, template.html, etc.)."""
    for item in type_root.iterdir():
        if item.name in {"docs", "docs_i18n", "__pycache__", "output_readme.md"} or item.name.startswith("."):
            continue
        _copy_item_with_substitutions(item, src_dir / item.name, replacements, created_files)


def _deploy_localized_docs(
    type_root: Traversable,
    src_dir: Path,
    selected_lang: str,
    replacements: dict[str, str],
    created_files: list[Path],
) -> None:
    """Deploy flat localized scripts and README (<type>/docs/<lang>/) for standalone 'images' projects."""
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


def _parse_init_languages(lang: str, canonical_type: str) -> list[str]:
    """Parse and validate single or comma-separated language codes for project initialization."""
    parts = [part.strip() for part in lang.split(",") if part.strip()]
    if not parts:
        raise ValueError("Language code cannot be empty.")

    normalized: list[str] = []
    for raw_code in parts:
        norm_code = normalize_language(raw_code)
        if norm_code in normalized:
            raise ValueError(f"Duplicate language code '{norm_code}' in --lang '{lang}'.")
        normalized.append(norm_code)

    if len(normalized) > 1 and canonical_type not in _I18N_PROJECT_TYPES:
        raise ValueError(
            f"Multi-language initialization ('{lang}') is supported for 'doc', 'site', 'slide', and 'catalog' "
            f"projects, not '{canonical_type}'."
        )
    return normalized


def _to_archetype_literal(canonical_type: str) -> Literal["images", "doc", "site", "slide", "catalog"]:
    """Narrow canonical project type string to ProjectArchetype literal."""
    mapping: dict[str, Literal["images", "doc", "site", "slide", "catalog"]] = {
        "doc": "doc",
        "site": "site",
        "slide": "slide",
        "catalog": "catalog",
    }
    return mapping.get(canonical_type, "images")


def _deploy_project_manifest(
    src_dir: Path,
    canonical_type: Literal["images", "doc", "site", "slide", "catalog"],
    target_name: str,
    style: str,
    primary_lang: str,
    parsed_langs: list[str],
    created_files: list[Path],
) -> None:
    """Write ``drawlib.toml`` project manifest file for any initialized project archetype."""
    from drawlib._builder._common.manifest import format_project_manifest_toml  # noqa: PLC0415

    project_name = target_name or canonical_type
    manifest_style = "custom" if Path(style).exists() else style
    is_i18n_type = canonical_type in _I18N_PROJECT_TYPES
    labels = (
        {lc: get_language_config(lc).display_name for lc in parsed_langs}
        if is_i18n_type and len(parsed_langs) > 1
        else None
    )
    toml_text = format_project_manifest_toml(
        name=project_name,
        project_type=canonical_type,
        style=manifest_style,
        lang=primary_lang,
        langs=parsed_langs if is_i18n_type else None,
        labels=labels,
    )

    target_path = src_dir / "drawlib.toml"
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(toml_text, encoding="utf-8")
    if target_path not in created_files:
        created_files.append(target_path)


def _deploy_i18n_locales(
    type_root: Traversable,
    src_dir: Path,
    langs: list[str],
    replacements: dict[str, str],
    created_files: list[Path],
) -> None:
    """Deploy starter document trees under <src_dir>/<lang>/ for each locale."""
    docs_root = type_root.joinpath("docs")
    docs_i18n_root = type_root.joinpath("docs_i18n")
    en_docs = docs_root.joinpath("en")

    primary_lang = langs[0] if langs else "en"
    primary_docs = docs_root.joinpath(primary_lang) if docs_root.is_dir() else None
    readme_cand = primary_docs.joinpath("README.md") if primary_docs is not None and primary_docs.is_dir() else None
    if readme_cand is None or not readme_cand.is_file():
        readme_cand = en_docs.joinpath("README.md") if en_docs.is_dir() else None
    if readme_cand is not None and readme_cand.is_file():
        _copy_item_with_substitutions(readme_cand, src_dir / "README.md", replacements, created_files)

    is_multi = len(langs) > 1
    for lc in langs:
        if is_multi:
            cand = docs_i18n_root.joinpath(lc) if docs_i18n_root.is_dir() else None
        else:
            cand = docs_root.joinpath(lc) if docs_root.is_dir() else None
        source_tree = cand if (cand is not None and cand.is_dir()) else en_docs
        if not source_tree.is_dir():
            continue
        locale_dst = src_dir / lc
        locale_dst.mkdir(parents=True, exist_ok=True)
        for item in source_tree.iterdir():
            if item.name in {"__pycache__", "README.md"} or item.name.startswith("."):
                continue
            _copy_item_with_substitutions(item, locale_dst / item.name, replacements, created_files)


def init_project(
    project_type: str,
    destination: str | Path = ".",
    target: str | None = None,
    output: str | None = None,
    force: bool = False,
    lang: str = "en",
    style: str | None = None,
    here: bool = False,
) -> list[Path]:
    """Scaffold a starter Drawlib project in the target destination directory.

    Args:
        project_type: Project type ('doc', 'site', 'catalog', 'slide', 'images', 'image').
        destination: Base directory path where <target>_src is created (defaults to current dir).
        target: Custom base name for the project (e.g. 'spec', 'report', 'docs', 'catalog', 'api').
        output: Legacy alias for target (e.g. 'rbac' creates 'rbac_src/').
        force: If True, overwrite existing files and directories.
        lang: Language code ('en', 'ja', etc.) or comma-separated codes for 'doc'/'site'/'catalog'/'slide' ('en,ja').
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
    parsed_langs = _parse_init_languages(lang, canonical_type)
    primary_lang = parsed_langs[0]
    resolved_style = (style or "default").strip()
    effective_target = target if target is not None else output

    paths = resolve_project_paths(
        project_type=canonical_type,
        target=effective_target,
        destination=destination,
    )

    project_base = importlib.resources.files("drawlib._templates").joinpath("project")
    type_root = project_base.joinpath(canonical_type)
    if not type_root.is_dir() and canonical_type == "images":
        type_root = project_base.joinpath("image")
    if not type_root.is_dir():
        raise FileNotFoundError(f"Template directory for '{canonical_type}' not found.")

    css_content = _resolve_stylesheet(canonical_type, resolved_style, lang=primary_lang)
    _validate_conflicts(src_dir=paths.src_dir, force=force)

    replacements = {
        "__TARGET__": paths.target,
        "__DEFAULT_LANG__": primary_lang,
        "__SRC_DIR__": paths.src_dir_name,
        "__OUT_DIR__": paths.out_markdown_dir_name,
        "__OUT_MARKDOWN_DIR__": paths.out_markdown_dir_name,
        "__OUT_IMAGES_DIR__": paths.out_images_dir_name,
        "__OUT_HTML_DIR__": paths.out_html_dir_name,
        "__OUT_PDF__": paths.out_pdf_name,
        "__OUT_DOCX__": paths.out_docx_name,
        "__OUT_PPTX__": paths.out_pptx_name,
        **get_font_replacements(primary_lang, style_theme=resolved_style),
    }

    created_files: list[Path] = []
    _deploy_shared_templates(project_base, paths.src_dir, replacements, created_files)
    _deploy_type_root_files(type_root, paths.src_dir, replacements, created_files)
    archetype_lit = _to_archetype_literal(canonical_type)
    _deploy_project_manifest(
        src_dir=paths.src_dir,
        canonical_type=archetype_lit,
        target_name=paths.target,
        style=resolved_style,
        primary_lang=primary_lang,
        parsed_langs=parsed_langs,
        created_files=created_files,
    )
    if canonical_type in _I18N_PROJECT_TYPES:
        _deploy_i18n_locales(type_root, paths.src_dir, parsed_langs, replacements, created_files)
    else:
        _deploy_localized_docs(type_root, paths.src_dir, primary_lang, replacements, created_files)
    _copy_shared_assets(paths.src_dir, replacements, created_files)
    _deploy_stylesheet(paths.src_dir, css_content, created_files)

    return sorted(created_files)
