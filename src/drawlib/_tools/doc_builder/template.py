# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Template and CSS preset listing, export, and validation utilities for drawlib doc_builder."""

from __future__ import annotations

import os
import shutil
from typing import Dict, List, Literal, Tuple

import jinja2
import jinja2.meta

BUILTIN_HTML_TEMPLATES: Dict[str, Dict[str, str]] = {
    "sidebar": {
        "file": "sidebar.html.j2",
        "description": "Multi-page documentation layout with collapsible left sidebar navigation.",
    },
    "simple": {
        "file": "simple.html.j2",
        "description": "Standalone single-column document layout without sidebar.",
    },
}

BUILTIN_PDF_TEMPLATES: Dict[str, Dict[str, str]] = {
    "default": {
        "file": "default.html.j2",
        "description": "Standard single-column print/PDF layout with clean page margins.",
    },
    "book": {
        "file": "book.html.j2",
        "description": "Book and technical report PDF layout with article wrapper.",
    },
}

BUILTIN_TEMPLATES = BUILTIN_HTML_TEMPLATES

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
    "google": {
        "file": "google.css",
        "description": "Google editorial print/PDF theme with line-wrapped code and clean pagination.",
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


def list_templates(target: Literal["html", "pdf"] = "html") -> List[Dict[str, str]]:
    """Return metadata for built-in Jinja2 templates for the specified target ('html' or 'pdf').

    Args:
        target (Literal["html", "pdf"]): Target format ('html' or 'pdf'). Defaults to 'html'.

    Returns:
        List[Dict[str, str]]: List of dicts with keys 'name', 'file', and 'description'.
    """
    registry = BUILTIN_PDF_TEMPLATES if target == "pdf" else BUILTIN_HTML_TEMPLATES
    return [
        {"name": name, "file": meta["file"], "description": meta["description"]}
        for name, meta in registry.items()
    ]


def list_html_templates() -> List[Dict[str, str]]:
    """Return metadata for built-in HTML templates."""
    return list_templates(target="html")


def list_pdf_templates() -> List[Dict[str, str]]:
    """Return metadata for built-in PDF templates."""
    return list_templates(target="pdf")


def export_template(
    name: str = "sidebar",
    output: str = "template.html.j2",
    target: Literal["html", "pdf"] = "html",
) -> str:
    """Export a built-in HTML or PDF template to a target file path.

    Args:
        name (str): Name of built-in template preset.
        output (str): Destination file path. Defaults to 'template.html.j2'.
        target (Literal["html", "pdf"]): Target format ('html' or 'pdf'). Defaults to 'html'.

    Returns:
        str: Absolute file path of the exported template.

    Raises:
        ValueError: If template name is unknown.
        FileNotFoundError: If built-in template file is missing.
    """
    if target == "pdf":
        normalized = "default" if name in {"simple", "standalone"} else name
        registry = BUILTIN_PDF_TEMPLATES
        templates_dir = os.path.join(os.path.dirname(__file__), "pdf_templates")
    else:
        normalized = "simple" if name == "standalone" else name
        registry = BUILTIN_HTML_TEMPLATES
        templates_dir = os.path.join(os.path.dirname(__file__), "html_templates")

    if normalized not in registry:
        available = ", ".join(registry.keys())
        raise ValueError(f"Unknown {target.upper()} template preset '{name}'. Available presets: {available}")

    filename = registry[normalized]["file"]
    src_path = os.path.join(templates_dir, filename)

    if not os.path.exists(src_path):
        raise FileNotFoundError(f"Built-in template not found at '{src_path}'.")

    dest_abs = os.path.abspath(output)
    os.makedirs(os.path.dirname(dest_abs), exist_ok=True)
    shutil.copy2(src_path, dest_abs)
    return dest_abs


def export_html_template(name: str = "sidebar", output: str = "template.html.j2") -> str:
    """Export a built-in HTML template ('sidebar' or 'simple')."""
    return export_template(name=name, output=output, target="html")


def export_pdf_template(name: str = "default", output: str = "pdf_template.html.j2") -> str:
    """Export a built-in PDF template ('default' or 'book')."""
    return export_template(name=name, output=output, target="pdf")


def export_default_template(output_path: str = "template.html.j2", template_name: str = "sidebar") -> str:
    """Export built-in HTML template (alias for export_template for backward compatibility)."""
    return export_template(name=template_name, output=output_path, target="html")


def validate_template(
    template_path: str,
    target: Literal["html", "pdf"] = "html",
) -> Tuple[bool, List[str]]:
    """Validate Jinja2 syntax and required variable placeholders in a custom template file.

    Args:
        template_path (str): File path to Jinja2 template.
        target (Literal["html", "pdf"]): Target format ('html' or 'pdf'). Defaults to 'html'.

    Returns:
        Tuple[bool, List[str]]: (is_valid, messages_list).
    """
    path_abs = os.path.abspath(template_path)
    if not os.path.exists(path_abs):
        return False, [f"Template file '{path_abs}' does not exist."]

    try:
        with open(path_abs, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return False, [f"Failed to read template file: {e}"]

    env = jinja2.Environment()
    try:
        parsed_ast = env.parse(content)
    except jinja2.exceptions.TemplateSyntaxError as e:
        return False, [f"Jinja2 Syntax Error at line {e.lineno}: {e.message}"]
    except Exception as e:
        return False, [f"Template Parsing Error: {e}"]

    referenced_vars = jinja2.meta.find_undeclared_variables(parsed_ast)
    messages: List[str] = []

    if "body" not in referenced_vars:
        msg = "Error: Template is missing mandatory placeholder 'body' (e.g. {{ body }} or {{ body | safe }})."
        messages.append(msg)
        return False, messages

    messages.append(f"Template '{os.path.basename(template_path)}' is valid.")

    missing_recommended: List[str] = []
    if "title" not in referenced_vars:
        missing_recommended.append("title")
    if target == "html" and "nav_items" not in referenced_vars:
        missing_recommended.append("nav_items")
    if "css_href" not in referenced_vars and "custom_css" not in referenced_vars:
        missing_recommended.append("css_href / custom_css")

    if missing_recommended:
        joined = ", ".join(missing_recommended)
        messages.append(f"Note: Template does not reference recommended variables: {joined}.")

    return True, messages


def list_css(target: Literal["html", "pdf"] = "html") -> List[Dict[str, str]]:
    """Return metadata for built-in CSS presets for the specified target ('html' or 'pdf').

    Args:
        target (Literal["html", "pdf"]): Target format ('html' or 'pdf'). Defaults to 'html'.

    Returns:
        List[Dict[str, str]]: List of dicts with keys 'name', 'file', and 'description'.
    """
    registry = BUILTIN_PDF_CSS_PRESETS if target == "pdf" else BUILTIN_HTML_CSS_PRESETS
    return [
        {"name": name, "file": meta["file"], "description": meta["description"]}
        for name, meta in registry.items()
    ]


def list_html_css() -> List[Dict[str, str]]:
    """Return metadata for built-in HTML CSS presets."""
    return list_css(target="html")


def list_pdf_css() -> List[Dict[str, str]]:
    """Return metadata for built-in PDF CSS presets."""
    return list_css(target="pdf")


def export_css(
    name: str = "default",
    output: str = "style.css",
    target: Literal["html", "pdf"] = "html",
) -> str:
    """Export a built-in CSS preset for HTML or PDF to a target file path.

    Args:
        name (str): Name of built-in CSS preset. Defaults to 'default'.
        output (str): Destination file path. Defaults to 'style.css'.
        target (Literal["html", "pdf"]): Target format ('html' or 'pdf'). Defaults to 'html'.

    Returns:
        str: Absolute file path of the exported CSS file.

    Raises:
        ValueError: If CSS preset name is unknown.
        FileNotFoundError: If built-in CSS file is missing.
    """
    if target == "pdf":
        if name in {"default-dark", "default-auto"}:
            normalized = "default"
        elif name in {"google-pdf", "google-dark", "google-auto"}:
            normalized = "google"
        else:
            normalized = name
        registry = BUILTIN_PDF_CSS_PRESETS
        styles_dir = os.path.join(os.path.dirname(__file__), "pdf_css")
    else:
        normalized = name
        registry = BUILTIN_HTML_CSS_PRESETS
        styles_dir = os.path.join(os.path.dirname(__file__), "html_css")

    if normalized not in registry:
        available = ", ".join(registry.keys())
        raise ValueError(f"Unknown {target.upper()} CSS preset '{name}'. Available presets: {available}")

    filename = registry[normalized]["file"]
    src_path = os.path.join(styles_dir, filename)

    if not os.path.exists(src_path):
        raise FileNotFoundError(f"Built-in CSS file not found at '{src_path}'.")

    dest_abs = os.path.abspath(output)
    os.makedirs(os.path.dirname(dest_abs), exist_ok=True)
    shutil.copy2(src_path, dest_abs)
    return dest_abs


def export_html_css(name: str = "default", output: str = "style.css") -> str:
    """Export a built-in HTML CSS preset."""
    return export_css(name=name, output=output, target="html")


def export_pdf_css(name: str = "default", output: str = "pdf_style.css") -> str:
    """Export a built-in PDF CSS preset."""
    return export_css(name=name, output=output, target="pdf")
