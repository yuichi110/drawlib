# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Shared utilities and validations for document compilers."""

from __future__ import annotations

import os
import re
import shutil
import sys
from typing import Optional, Set

EXCLUDED_ASSET_NAMES: set[str] = {
    "build.sh",
    "styles.py",
    "utils.py",
    "style.css",
    "template.html.j2",
    "template.html",
}
EXCLUDED_ASSET_EXTENSIONS: tuple[str, ...] = (".py", ".sh", ".j2", ".template")


def require_directory(path: str, caller_name: str) -> str:
    """Validate that path exists and is a directory.

    Args:
        path (str): Input path to validate.
        caller_name (str): Name of calling function for error reporting.

    Returns:
        str: Normalized absolute directory path.

    Raises:
        ValueError: If path does not exist or is a file rather than a directory.
    """
    abs_path = os.path.abspath(path)
    if not os.path.exists(abs_path):
        raise ValueError(f'Input path "{abs_path}" does not exist.')
    if not os.path.isdir(abs_path):
        raise ValueError(
            f'{caller_name} requires a directory as input. Received file: "{abs_path}". '
            "Single-file builds are not supported; use 'drawlib show' for quick preview "
            "or organize your file into a documentation directory."
        )
    return abs_path


def resolve_template_and_css(search_dir: str) -> tuple[str, str]:
    """Resolve required template.html and style.css in the target directory.

    Args:
        search_dir (str): Directory where project assets reside.

    Returns:
        tuple[str, str]: Absolute paths to (template.html, style.css).

    Raises:
        ValueError: If template.html or style.css does not exist.
    """
    template_cand = os.path.join(search_dir, "template.html")
    if not os.path.isfile(template_cand):
        raise ValueError(
            f'Missing required "template.html" in "{search_dir}". '
            'Please run "drawlib init" to initialize your project, or provide "template.html".'
        )

    css_cand = os.path.join(search_dir, "style.css")
    if not os.path.isfile(css_cand):
        raise ValueError(
            f'Missing required "style.css" in "{search_dir}". '
            'Please run "drawlib init" to initialize your project, or provide "style.css".'
        )

    return template_cand, css_cand


def validate_markdown_images(src_abs: str, content: str) -> None:
    """Check for missing local static images referenced via ![alt](path) in markdown."""
    src_dir = os.path.dirname(src_abs)
    pattern = re.compile(r"!\[(.*?)\]\((.*?)\)")
    for match in pattern.finditer(content):
        img_ref = match.group(2).strip()
        if not img_ref or img_ref.startswith(("http://", "https://", "data:", "#")):
            continue
        clean_ref = img_ref.split("#")[0].split("?")[0]
        resolved_path = os.path.abspath(os.path.join(src_dir, clean_ref))
        if not os.path.exists(resolved_path):
            sys.stderr.write(f"WARNING: Image '{img_ref}' referenced in '{src_abs}' does not exist.\n")


def extract_title(md_content: str, filename: str) -> str:
    """Extract title from first H1 header in Markdown content or fallback to filename."""
    for line in md_content.splitlines():
        line_str = line.strip()
        if line_str.startswith("# "):
            return line_str[2:].strip()
    base = os.path.splitext(filename)[0]
    return base.replace("_", " ").replace("-", " ").title()


def extract_html_body(html_text: str) -> str:
    """Extract inner content of <body>...</body> if present, otherwise return html_text."""
    match = re.search(r"<body\b[^>]*>(.*?)</body>", html_text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return html_text.strip()


def copy_directory_assets(
    input_dir_abs: str,
    out_dir_abs: str,
    excluded_files: Optional[Set[str]] = None,
) -> None:
    """Recursively copy static asset files from input directory to output directory.

    Skips markdown files, html documents, hidden files, and project template/script files.

    Args:
        input_dir_abs (str): Absolute source directory path.
        out_dir_abs (str): Absolute destination directory path.
        excluded_files (Optional[Set[str]]): Specific absolute file paths to skip.
    """
    if input_dir_abs == out_dir_abs:
        return

    excluded = excluded_files or set()

    for root, dirnames, files in os.walk(input_dir_abs):
        # Exclude output dir if inside input dir
        dirnames[:] = [
            d
            for d in dirnames
            if not (
                os.path.abspath(os.path.join(root, d)) == out_dir_abs
                or os.path.abspath(os.path.join(root, d)).startswith(out_dir_abs + os.sep)
            )
        ]
        for fname in sorted(files):
            if fname.startswith("."):
                continue
            src_abs = os.path.join(root, fname)
            if src_abs in excluded:
                continue
            if fname.lower() in EXCLUDED_ASSET_NAMES or fname.endswith(EXCLUDED_ASSET_EXTENSIONS):
                continue
            if fname.lower().endswith((".md", ".markdown", ".html", ".htm")):
                continue

            rel_path = os.path.relpath(src_abs, input_dir_abs)
            dest_abs = os.path.join(out_dir_abs, rel_path)
            os.makedirs(os.path.dirname(dest_abs), exist_ok=True)
            shutil.copy2(src_abs, dest_abs)
