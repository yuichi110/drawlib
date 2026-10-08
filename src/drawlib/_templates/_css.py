# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""CSS theme synthesizer and asset exporter for Drawlib."""

from __future__ import annotations

import importlib.resources
import os
from typing import Dict, Final, List, Literal, Optional

from drawlib._templates.langs import get_font_replacements

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


def get_slide_readme() -> str:
    """Get the standalone viewer README.md content for compiled HTML slide decks.

    Returns:
        str: Markdown instructions for viewing and controlling the compiled slide deck.
    """
    return _read_template_resource("project", "slide", "output_readme.md")


def get_html_readme() -> str:
    """Get the standalone viewer README.md content for compiled HTML documentation directories.

    Returns:
        str: Markdown instructions for viewing the compiled HTML documentation.
    """
    return _read_template_resource("project", "_shared", "output_html_readme.md")


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
