# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unified builder and synthesizer for Drawlib project templates and CSS themes."""

from __future__ import annotations

import importlib.resources
import os
from importlib.resources.abc import Traversable
from pathlib import Path
from typing import Dict, Final, List, Literal, Optional

from drawlib._templates.langs import get_font_replacements, normalize_language

PROJECT_TYPES: Final[dict[str, str]] = {
    "site": "Multi-page documentation website with sidebar navigation and search.",
    "doc": "Single specification, RFC, or multi-chapter technical report compiled to HTML and PDF.",
    "slide": "16:9 presentation slide deck with modular SmartArts and vector diagrams.",
    "image": "Standalone Python illustration scripts compiled into images.",
}

BUILTIN_THEMES: Final[Dict[str, Dict[str, str]]] = {
    "default": {
        "file": "default.css.template",
        "description": "Modern developer light theme inspired by VitePress & Tailwind CSS.",
    },
    "default-dark": {
        "file": "default-dark.css.template",
        "description": "Modern developer dark theme with deep slate & indigo palette.",
    },
    "default-auto": {
        "file": "default-auto.css.template",
        "description": "Modern developer responsive theme switching between light and dark.",
    },
    "google": {
        "file": "google.css.template",
        "description": "Clean editorial Google Blog (The Keyword) & Material Design light style.",
    },
    "google-dark": {
        "file": "google-dark.css.template",
        "description": "Google editorial dark theme with Material Dark palette.",
    },
    "google-auto": {
        "file": "google-auto.css.template",
        "description": "Google editorial responsive theme switching between light and dark.",
    },
    "github": {
        "file": "github.css.template",
        "description": "GitHub-flavored Markdown style with familiar code block and table formatting.",
    },
    "minimal": {
        "file": "minimal.css.template",
        "description": "Lightweight, distraction-free minimalist typography.",
    },
    "monochrome": {
        "file": "monochrome.css.template",
        "description": "High-contrast black-and-white style suited for formal publications.",
    },
}

BUILTIN_HTML_CSS_PRESETS = BUILTIN_THEMES
BUILTIN_CSS_PRESETS = BUILTIN_THEMES
BUILTIN_PDF_CSS_PRESETS: Final[Dict[str, Dict[str, str]]] = {
    k: v for k, v in BUILTIN_THEMES.items() if not k.endswith("-auto")
}
BUILTIN_SLIDE_CSS_PRESETS: Final[Dict[str, Dict[str, str]]] = {
    k: v for k, v in BUILTIN_THEMES.items() if k in {"default", "default-dark", "google", "google-dark", "monochrome"}
}


def list_project_types() -> dict[str, str]:
    """Return available project types and their descriptions.

    Returns:
        dict[str, str]: Mapping of project type name to description.
    """
    return dict(PROJECT_TYPES)


def list_css(
    target: Literal["html", "pdf", "slide", "site", "doc"] = "html",
) -> List[Dict[str, str]]:
    """Return metadata for built-in CSS presets for the specified target.

    Args:
        target: Target format ('html', 'pdf', 'slide', 'site', 'doc'). Defaults to 'html'.

    Returns:
        List[Dict[str, str]]: List of dicts with keys 'name', 'file', and 'description'.
    """
    if target == "pdf":
        names = [k for k in BUILTIN_THEMES if not k.endswith("-auto")]
    elif target == "slide":
        names = ["default", "default-dark", "google", "google-dark", "monochrome"]
    else:
        names = list(BUILTIN_THEMES.keys())

    return [
        {"name": name, "file": BUILTIN_THEMES[name]["file"], "description": BUILTIN_THEMES[name]["description"]}
        for name in names
    ]


def list_html_css() -> List[Dict[str, str]]:
    """Return metadata for built-in HTML CSS presets."""
    return list_css(target="html")


def list_pdf_css() -> List[Dict[str, str]]:
    """Return metadata for built-in PDF CSS presets."""
    return list_css(target="pdf")


def list_slide_css() -> List[Dict[str, str]]:
    """Return metadata for built-in slide CSS presets."""
    return list_css(target="slide")


def _apply_css_font_replacements(css_text: str, lang: str = "en") -> str:
    """Apply font family replacements to CSS placeholders."""
    replacements = get_font_replacements(lang)
    for key in ("__RTD_FONT_FAMILY__", "__RTD_MONO_FONT_FAMILY__"):
        if key in replacements:
            css_text = css_text.replace(key, replacements[key])
    return css_text


def _read_template_resource(*subpath: str) -> str:
    """Read UTF-8 text from a resource path inside drawlib._templates."""
    res = importlib.resources.files("drawlib._templates")
    for segment in subpath:
        res = res.joinpath(segment)
    return res.read_text(encoding="utf-8")


def get_css(
    name: Optional[str] = None,
    target: Literal["html", "pdf", "slide", "site", "doc"] = "html",
    lang: str = "en",
) -> str:
    """Get complete synthesized theme CSS content string.

    Composes Layer 1 (Theme tokens) + Layer 2 (Components) + Layer 3 (Target layout)
    into a self-contained, standalone stylesheet.

    Args:
        name: Built-in theme name or path to a custom CSS file. Defaults to 'default'.
        target: Target document format ('html', 'site', 'doc', 'pdf', 'slide'). Defaults to 'html'.
        lang: Language code or alias (e.g. 'en', 'ja') for font replacements. Defaults to 'en'.

    Returns:
        str: Synthesized CSS content string.

    Raises:
        ValueError: If theme name is unknown.
    """
    if name and os.path.exists(name):
        with open(name, "r", encoding="utf-8") as f:
            raw_css = f.read()
        return _apply_css_font_replacements(raw_css, lang=lang)

    theme_name = (name or "default").strip().lower()
    if theme_name == "google-pdf":
        theme_name = "google"

    if theme_name not in BUILTIN_THEMES:
        available_presets = ", ".join(sorted(p["name"] for p in list_css(target=target)))
        raise ValueError(
            f"Unknown CSS preset '{name}' for target '{target}'. Available presets: {available_presets}"
        )

    theme_file = BUILTIN_THEMES[theme_name]["file"]
    theme_content = _read_template_resource("css", "themes", theme_file)

    parts: list[str] = [theme_content]

    if target in {"html", "site", "doc", "pdf"}:
        parts.append(_read_template_resource("css", "components", "code.css"))
        parts.append(_read_template_resource("css", "components", "markdown.css"))

    if target in {"html", "site"}:
        parts.append(_read_template_resource("css", "targets", "site.css"))
    elif target == "doc":
        parts.append(_read_template_resource("css", "targets", "doc.css"))
    elif target == "pdf":
        parts.append(_read_template_resource("css", "targets", "pdf.css"))
    elif target == "slide":
        parts.append(_read_template_resource("css", "components", "code.css"))
        parts.append(_read_template_resource("css", "targets", "slide.css"))

    combined = "\n\n".join(parts)
    return _apply_css_font_replacements(combined, lang=lang)


def get_slide_js() -> str:
    """Get the vanilla JavaScript presentation deck engine script content.

    Returns:
        str: JavaScript code for slide navigation, overview grid, and responsive scaling.
    """
    return _read_template_resource("project", "slide", "slide.js")


def export_css(
    name: str,
    output_path: Optional[str] = None,
    target: Literal["html", "pdf", "slide", "site", "doc"] = "html",
    force: bool = False,
    lang: str = "en",
) -> str:
    """Export a synthesized CSS theme to a target file.

    Args:
        name: Built-in CSS preset name (e.g., 'google', 'default-dark').
        output_path: Destination file path. If None, auto-resolves to 'style.css'.
        target: Target format ('html', 'pdf', 'slide', 'site', 'doc'). Defaults to 'html'.
        force: If True, overwrite destination file if it already exists.
        lang: Language code or alias for typography. Defaults to 'en'.

    Returns:
        str: Absolute path of exported CSS file.

    Raises:
        ValueError: If preset name is unknown.
        FileExistsError: If destination file exists and force is False.
    """
    content = get_css(name=name, target=target, lang=lang)

    if output_path is None:
        cand_docs_src = os.path.join("docs_src", "style.css")
        if os.path.exists(cand_docs_src):
            resolved_dest = os.path.abspath(cand_docs_src)
        else:
            resolved_dest = os.path.abspath("style.css")
    else:
        resolved_dest = os.path.abspath(output_path)

    if os.path.exists(resolved_dest) and not force:
        raise FileExistsError(f"Destination file '{resolved_dest}' already exists. Use --force to overwrite.")

    os.makedirs(os.path.dirname(resolved_dest), exist_ok=True)
    with open(resolved_dest, "w", encoding="utf-8") as f:
        f.write(content)

    return resolved_dest


def _validate_conflicts(
    src_path: Path,
    force: bool,
    here: bool,
) -> None:
    """Validate that target source folder or destination files do not conflict."""
    if force:
        return

    if here:
        critical_items = [
            src_path / "build.sh",
            src_path / "build_html.sh",
            src_path / "build_pdf.sh",
            src_path / "build_markdown.sh",
            src_path / "build_image.sh",
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
    elif selected_type == "doc":
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
    """Copy shared static assets from project/_assets into target project."""
    shared_assets_root = importlib.resources.files("drawlib._templates").joinpath("project", "_assets")
    if shared_assets_root.is_dir():
        _copy_item_with_substitutions(shared_assets_root, src_path / "_assets", replacements, created_files)


def _deploy_stylesheet(
    selected_type: str,
    src_path: Path,
    style: Optional[str],
    created_files: list[Path],
    lang: str = "en",
) -> None:
    """Deploy custom or synthesized style.css or slide.css."""
    if selected_type in {"site", "doc"}:
        target: Literal["site", "doc"] = "site" if selected_type == "site" else "doc"
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
    project_base: Traversable,
    src_path: Path,
    replacements: dict[str, str],
    created_files: list[Path],
    selected_type: str = "",
) -> None:
    """Deploy default shared files (_shared/styles.py.template, _shared/utils.py)."""
    shared_root = project_base.joinpath("_shared")
    if not shared_root.is_dir():
        return
    for item in shared_root.iterdir():
        if item.name == "__pycache__" or item.name.startswith("."):
            continue
        if selected_type == "slide" and item.name == "utils.py":
            continue
        _copy_item_with_substitutions(item, src_path / item.name, replacements, created_files)


def _deploy_slide_utils(
    project_base: Traversable,
    src_path: Path,
    style: str,
    replacements: dict[str, str],
    created_files: list[Path],
) -> None:
    """Deploy style-specific utils.py for slide projects."""
    utils_root = project_base.joinpath("slide", "utils")
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
    _copy_item_with_substitutions(template_path, src_path / "utils.py", replacements, created_files)


def _deploy_type_root_files(
    type_root: Traversable,
    src_path: Path,
    replacements: dict[str, str],
    created_files: list[Path],
) -> None:
    """Deploy type-specific root files (build scripts, template.html, etc.)."""
    for item in type_root.iterdir():
        if item.name in {"docs", "utils", "__pycache__"} or item.name.startswith("."):
            continue
        _copy_item_with_substitutions(item, src_path / item.name, replacements, created_files)


def _deploy_localized_docs(
    type_root: Traversable,
    src_path: Path,
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
    """Scaffold a starter Drawlib project.

    Args:
        project_type: Project type ('site', 'doc', 'slide', 'image').
        destination: Parent destination directory path (defaults to current directory).
        output: Base project/artifact name (e.g. 'report' creates 'report_src').
        force: If True, overwrite existing files and directories.
        here: If True, deploy directly into destination without creating <name>_src subfolder.
        lang: Language for starter templates ('en', 'ja', etc.). Defaults to 'en'.
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

    project_base = importlib.resources.files("drawlib._templates").joinpath("project")
    type_root = project_base.joinpath(selected_type)
    if not type_root.is_dir():
        raise FileNotFoundError(f"Template directory for '{selected_type}' not found.")

    if selected_type == "slide":
        utils_root = project_base.joinpath("slide", "utils")
        template_path = utils_root.joinpath(f"{resolved_style}.py.template")
        if not template_path.is_file():
            available = (
                sorted(
                    f.name[:-12]
                    for f in utils_root.iterdir()
                    if f.name.endswith(".py.template")
                )
                if utils_root.is_dir()
                else []
            )
            raise ValueError(
                f"Unsupported slide style '{resolved_style}'. Available styles: {', '.join(available)}"
            )

    _validate_conflicts(
        src_path=src_path,
        force=force,
        here=here,
    )

    replacements = {
        "__SRC_DIR__": "." if here else src_dir_name,
        "__OUT_DIR__": out_dir_name,
        "__OUT_HTML_DIR__": out_html_dir_name,
        "__OUT_PDF__": out_pdf_name,
        **get_font_replacements(selected_lang, style_theme=resolved_style),
    }

    created_files: list[Path] = []
    _deploy_shared_templates(
        project_base, src_path, replacements, created_files, selected_type=selected_type
    )
    if selected_type == "slide":
        _deploy_slide_utils(project_base, src_path, resolved_style, replacements, created_files)
    _deploy_type_root_files(type_root, src_path, replacements, created_files)
    _deploy_localized_docs(type_root, src_path, selected_lang, replacements, created_files)
    _copy_shared_assets(src_path, replacements, created_files)
    _deploy_stylesheet(selected_type, src_path, resolved_style, created_files, lang=selected_lang)

    return sorted(created_files)
