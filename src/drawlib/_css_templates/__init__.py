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

from drawlib._langs import get_font_replacements

BUILTIN_HTML_CSS_PRESETS: Dict[str, Dict[str, str]] = {
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
        "description": "High-contrast black-and-white style suited for formal web publications.",
    },
}

BUILTIN_PDF_CSS_PRESETS: Dict[str, Dict[str, str]] = {
    "default": {
        "file": "default.css.template",
        "description": "Modern print/PDF typography with line-wrapped code and A4 pagination.",
    },
    "default-dark": {
        "file": "default-dark.css.template",
        "description": "Modern print/PDF dark theme with deep slate & indigo palette.",
    },
    "google": {
        "file": "google.css.template",
        "description": "Google editorial print/PDF theme with line-wrapped code and clean pagination.",
    },
    "google-dark": {
        "file": "google-dark.css.template",
        "description": "Google editorial print/PDF dark theme with Material Dark palette.",
    },
    "github": {
        "file": "github.css.template",
        "description": "GitHub-flavored print/PDF theme with line-wrapped code and bordered tables.",
    },
    "minimal": {
        "file": "minimal.css.template",
        "description": "Minimalist serif print/PDF typography.",
    },
    "monochrome": {
        "file": "monochrome.css.template",
        "description": "High-contrast black-and-white print/PDF theme.",
    },
}

BUILTIN_SLIDE_CSS_PRESETS: Dict[str, Dict[str, str]] = {
    "google": {
        "file": "google.css.template",
        "description": "Google editorial presentation theme with 16:9 stage and Material palette.",
    },
    "default": {
        "file": "default.css.template",
        "description": "Modern developer light presentation theme with Tailwind-inspired colors.",
    },
    "monochrome": {
        "file": "monochrome.css.template",
        "description": "High-contrast black-and-white presentation theme for print and clean projection.",
    },
}

BUILTIN_CSS_PRESETS = BUILTIN_HTML_CSS_PRESETS


def list_css(target: Literal["html", "pdf", "slide"] = "html") -> List[Dict[str, str]]:
    """Return metadata for built-in CSS presets for the specified target ('html', 'pdf', or 'slide').

    Args:
        target (Literal["html", "pdf", "slide"]): Target format ('html', 'pdf', or 'slide'). Defaults to 'html'.

    Returns:
        List[Dict[str, str]]: List of dicts with keys 'name', 'file', and 'description'.
    """
    if target == "pdf":
        registry = BUILTIN_PDF_CSS_PRESETS
    elif target == "slide":
        registry = BUILTIN_SLIDE_CSS_PRESETS
    else:
        registry = BUILTIN_HTML_CSS_PRESETS
    return [{"name": name, "file": meta["file"], "description": meta["description"]} for name, meta in registry.items()]


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


def _read_preset_css(css_dir: str, file_name: str) -> str:
    """Read preset CSS file content from directory, trying template variants."""
    candidates = [file_name, f"{file_name}.template", "default.css.template", "default.css"]
    for cand in candidates:
        preset_file = os.path.join(css_dir, cand)
        if os.path.isfile(preset_file):
            with open(preset_file, "r", encoding="utf-8") as f:
                return f.read()
    return ""


def get_css(
    name: Optional[str] = None,
    target: Literal["html", "pdf", "slide"] = "html",
    lang: str = "en",
) -> str:
    """Get complete theme CSS content string for HTML, PDF, or Slide.

    Args:
        name (Optional[str]): Built-in CSS preset name or path to a custom CSS file.
            If None or empty, returns the default theme CSS content.
        target (Literal["html", "pdf", "slide"]): Target document format
            ('html', 'pdf', or 'slide'). Defaults to 'html'.
        lang (str): Language code or alias (e.g. 'en', 'ja', 'zh-cn', 'th') for typography. Defaults to 'en'.

    Returns:
        str: Complete CSS content string.

    Raises:
        ValueError: If specified CSS preset name is unknown or file cannot be found.
    """
    target_configs: Dict[str, tuple[str, Dict[str, Dict[str, str]]]] = {
        "pdf": ("pdf", BUILTIN_PDF_CSS_PRESETS),
        "slide": ("slide", BUILTIN_SLIDE_CSS_PRESETS),
        "html": ("html", BUILTIN_HTML_CSS_PRESETS),
    }
    subdir, registry = target_configs.get(target, ("html", BUILTIN_HTML_CSS_PRESETS))
    css_dir = os.path.join(os.path.dirname(__file__), subdir)

    if not name:
        raw_css = _read_preset_css(css_dir, "default.css")
    elif os.path.exists(name):
        with open(name, "r", encoding="utf-8") as f:
            raw_css = f.read()
    else:
        normalized = "google" if (target == "pdf" and name == "google-pdf") else name
        file_name = registry.get(normalized, {}).get("file", "")
        raw_css = _read_preset_css(css_dir, file_name) if file_name else ""

    if not raw_css and name and not os.path.exists(name):
        available = ", ".join(sorted(registry.keys()))
        raise ValueError(f"Unknown CSS preset '{name}' for target '{target}'. Available presets: {available}")

    return _apply_css_font_replacements(raw_css, lang=lang)


def get_slide_js() -> str:
    """Get the vanilla JavaScript presentation deck engine script content.

    Returns:
        str: JavaScript code for slide navigation, overview grid, and responsive scaling.
    """
    js_path = os.path.join(os.path.dirname(__file__), "slide", "slide.js")
    with open(js_path, "r", encoding="utf-8") as f:
        return f.read()


def export_css(
    name: str,
    output_path: Optional[str] = None,
    target: Literal["html", "pdf", "slide"] = "html",
    force: bool = False,
    lang: str = "en",
) -> str:
    """Export a built-in CSS preset to a target file.

    Args:
        name (str): Built-in CSS preset name (e.g., 'google', 'default-dark').
        output_path (Optional[str]): Destination file path. If None, auto-resolves to
            'docs_src/style.css' if 'docs_src/style.css' exists, otherwise 'style.css'.
        target (Literal["html", "pdf", "slide"]): Target format ('html', 'pdf', or 'slide'). Defaults to 'html'.
        force (bool): If True, overwrite destination file if it already exists.
        lang (str): Language code or alias (e.g. 'en', 'ja', 'zh-cn', 'th') for typography. Defaults to 'en'.

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


__all__ = [
    "BUILTIN_CSS_PRESETS",
    "BUILTIN_HTML_CSS_PRESETS",
    "BUILTIN_PDF_CSS_PRESETS",
    "BUILTIN_SLIDE_CSS_PRESETS",
    "export_css",
    "get_css",
    "get_slide_js",
    "list_css",
    "list_html_css",
    "list_pdf_css",
    "list_slide_css",
]
