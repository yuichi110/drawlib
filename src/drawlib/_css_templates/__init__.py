# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Built-in CSS presets, loader, and exporter for HTML and PDF documentation."""

from __future__ import annotations

import os
from typing import Dict, List, Literal, Optional

BUILTIN_HTML_CSS_PRESETS: Dict[str, Dict[str, str]] = {
    "default": {
        "file": "default.css",
        "description": "Modern developer light theme inspired by VitePress & Tailwind CSS.",
    },
    "default-dark": {
        "file": "default-dark.css",
        "description": "Modern developer dark theme with deep slate & indigo palette.",
    },
    "default-auto": {
        "file": "default-auto.css",
        "description": "Modern developer responsive theme switching between light and dark.",
    },
    "google": {
        "file": "google.css",
        "description": "Clean editorial Google Blog (The Keyword) & Material Design light style.",
    },
    "google-dark": {
        "file": "google-dark.css",
        "description": "Google editorial dark theme with Material Dark palette.",
    },
    "google-auto": {
        "file": "google-auto.css",
        "description": "Google editorial responsive theme switching between light and dark.",
    },
    "github": {
        "file": "github.css",
        "description": "GitHub-flavored Markdown style with familiar code block and table formatting.",
    },
    "minimal": {
        "file": "minimal.css",
        "description": "Lightweight, distraction-free minimalist typography.",
    },
    "monochrome": {
        "file": "monochrome.css",
        "description": "High-contrast black-and-white style suited for formal web publications.",
    },
}

BUILTIN_PDF_CSS_PRESETS: Dict[str, Dict[str, str]] = {
    "default": {
        "file": "default.css",
        "description": "Modern print/PDF typography with line-wrapped code and A4 pagination.",
    },
    "default-dark": {
        "file": "default-dark.css",
        "description": "Modern print/PDF dark theme with deep slate & indigo palette.",
    },
    "google": {
        "file": "google.css",
        "description": "Google editorial print/PDF theme with line-wrapped code and clean pagination.",
    },
    "google-dark": {
        "file": "google-dark.css",
        "description": "Google editorial print/PDF dark theme with Material Dark palette.",
    },
    "github": {
        "file": "github.css",
        "description": "GitHub-flavored print/PDF theme with line-wrapped code and bordered tables.",
    },
    "minimal": {
        "file": "minimal.css",
        "description": "Minimalist serif print/PDF typography.",
    },
    "monochrome": {
        "file": "monochrome.css",
        "description": "High-contrast black-and-white print/PDF theme.",
    },
}

BUILTIN_CSS_PRESETS = BUILTIN_HTML_CSS_PRESETS


def list_css(target: Literal["html", "pdf"] = "html") -> List[Dict[str, str]]:
    """Return metadata for built-in CSS presets for the specified target ('html' or 'pdf').

    Args:
        target (Literal["html", "pdf"]): Target format ('html' or 'pdf'). Defaults to 'html'.

    Returns:
        List[Dict[str, str]]: List of dicts with keys 'name', 'file', and 'description'.
    """
    registry = BUILTIN_PDF_CSS_PRESETS if target == "pdf" else BUILTIN_HTML_CSS_PRESETS
    return [{"name": name, "file": meta["file"], "description": meta["description"]} for name, meta in registry.items()]


def list_html_css() -> List[Dict[str, str]]:
    """Return metadata for built-in HTML CSS presets."""
    return list_css(target="html")


def list_pdf_css() -> List[Dict[str, str]]:
    """Return metadata for built-in PDF CSS presets."""
    return list_css(target="pdf")


def get_css(
    name: Optional[str] = None,
    target: Literal["html", "pdf"] = "html",
) -> str:
    """Get complete theme CSS content string for HTML or PDF.

    Args:
        name (Optional[str]): Built-in CSS preset name or path to a custom CSS file.
            If None or empty, returns the default theme CSS content.
        target (Literal["html", "pdf"]): Target document format ('html' or 'pdf'). Defaults to 'html'.

    Returns:
        str: Complete CSS content string.

    Raises:
        ValueError: If specified CSS preset name is unknown or file cannot be found.
    """
    subdir = "pdf" if target == "pdf" else "html"
    css_dir = os.path.join(os.path.dirname(__file__), subdir)
    registry = BUILTIN_PDF_CSS_PRESETS if target == "pdf" else BUILTIN_HTML_CSS_PRESETS

    if not name:
        default_file = os.path.join(css_dir, "default.css")
        if os.path.exists(default_file):
            with open(default_file, "r", encoding="utf-8") as f:
                return f.read()
        return ""

    if os.path.exists(name):
        with open(name, "r", encoding="utf-8") as f:
            return f.read()

    normalized = "google" if (target == "pdf" and name == "google-pdf") else name
    if normalized in registry:
        preset_file = os.path.join(css_dir, registry[normalized]["file"])
        if os.path.exists(preset_file):
            with open(preset_file, "r", encoding="utf-8") as f:
                return f.read()

    available = ", ".join(sorted(registry.keys()))
    raise ValueError(f"Unknown CSS preset '{name}' for target '{target}'. Available presets: {available}")


def export_css(
    name: str,
    output_path: Optional[str] = None,
    target: Literal["html", "pdf"] = "html",
    force: bool = False,
) -> str:
    """Export a built-in CSS preset to a target file.

    Args:
        name (str): Built-in CSS preset name (e.g., 'google', 'default-dark').
        output_path (Optional[str]): Destination file path. If None, auto-resolves to
            'docs_src/style.css' if 'docs_src/style.css' exists, otherwise 'style.css'.
        target (Literal["html", "pdf"]): Target format ('html' or 'pdf'). Defaults to 'html'.
        force (bool): If True, overwrite destination file if it already exists.

    Returns:
        str: Absolute path of exported CSS file.

    Raises:
        ValueError: If preset name is unknown.
        FileExistsError: If destination file exists and force is False.
    """
    content = get_css(name=name, target=target)

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


__all__ = [
    "BUILTIN_CSS_PRESETS",
    "BUILTIN_HTML_CSS_PRESETS",
    "BUILTIN_PDF_CSS_PRESETS",
    "export_css",
    "get_css",
    "list_css",
    "list_html_css",
    "list_pdf_css",
]
