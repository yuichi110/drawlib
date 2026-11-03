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
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from drawlib._builder._common.manifest import ProjectManifest

EXCLUDED_ASSET_NAMES: set[str] = {
    "build.sh",
    "serve.sh",
    "styles.py",
    "utils.py",
    "style.css",
    "template.html.j2",
    "template.html",
    "drawlib.toml",
}
EXCLUDED_ASSET_EXTENSIONS: tuple[str, ...] = (".py", ".pyc", ".sh", ".j2", ".template")


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
    """Resolve required template.html and style.css in search_dir or parent drawlib.toml project root.

    Args:
        search_dir (str): Directory where project assets reside.

    Returns:
        tuple[str, str]: Absolute paths to (template.html, style.css).

    Raises:
        ValueError: If template.html or style.css does not exist.
    """
    candidate_dirs = [search_dir]
    parent_dir = os.path.dirname(os.path.abspath(search_dir))
    if parent_dir and parent_dir != os.path.abspath(search_dir):
        if os.path.isfile(os.path.join(parent_dir, "drawlib.toml")):
            candidate_dirs.append(parent_dir)

    template_cand: str | None = None
    for d in candidate_dirs:
        cand = os.path.join(d, "template.html")
        if os.path.isfile(cand):
            template_cand = cand
            break
    if template_cand is None:
        raise ValueError(
            f'Missing required "template.html" in "{search_dir}". '
            'Please run "drawlib init project <doc|site>" to initialize your project, '
            'or provide "template.html".'
        )

    css_cand: str | None = None
    for d in candidate_dirs:
        cand = os.path.join(d, "style.css")
        if os.path.isfile(cand):
            css_cand = cand
            break
    if css_cand is None:
        raise ValueError(
            f'Missing required "style.css" in "{search_dir}". '
            'Please run "drawlib init project <doc|site>" to initialize your project, '
            'or provide "style.css".'
        )

    return template_cand, css_cand


_FORBIDDEN_LINK_PREFIXES: tuple[str, ...] = (
    "file://",
    "file:/",
    "/usr/",
    "/home/",
    "/users/",
    "/root/",
    "/private/",
    "/tmp/",  # noqa: S108
    "/var/",
    "/opt/",
)


def _mask_code_blocks(text: str) -> str:
    """Mask code block contents with spaces while preserving line numbers and line breaks."""

    def repl(m: re.Match[str]) -> str:
        return re.sub(r"[^\n]", " ", m.group(0))

    masked = re.sub(r"(?s)(`{3,}|~{3,}).*?\1", repl, text)
    return re.sub(r"`[^`\n]+`", lambda m: " " * len(m.group(0)), masked)


def validate_markdown_links(src_abs: str, content: str) -> None:
    """Validate that Markdown content does not contain forbidden absolute paths or file:// URLs.

    Args:
        src_abs (str): Absolute path to the source Markdown file.
        content (str): Raw Markdown text content.

    Raises:
        ValueError: If forbidden file:// URLs or local filesystem absolute paths are found.
    """
    masked = _mask_code_blocks(content)
    md_pattern = re.compile(r"!?\[(.*?)\]\((.*?)\)")
    html_pattern = re.compile(r"""<(?:a|img)\b[^>]*?\b(?:href|src)=["']([^"']+)["']""", re.IGNORECASE)

    violations: list[tuple[int, str]] = []
    for line_num, line in enumerate(masked.splitlines(), start=1):
        for m in md_pattern.finditer(line):
            raw_target = m.group(2).strip()
            if not raw_target:
                continue
            clean_target = raw_target.split()[0].strip("<>\"'")
            if clean_target.lower().startswith(_FORBIDDEN_LINK_PREFIXES) or re.match(r"^[A-Za-z]:[\\/]", clean_target):
                violations.append((line_num, clean_target))

        for m in html_pattern.finditer(line):
            raw_target = m.group(1).strip()
            if not raw_target:
                continue
            clean_target = raw_target.split()[0].strip("<>\"'")
            if clean_target.lower().startswith(_FORBIDDEN_LINK_PREFIXES) or re.match(r"^[A-Za-z]:[\\/]", clean_target):
                violations.append((line_num, clean_target))

    if violations:
        lines_summary = "\n".join(f"  • Line {ln}: (target: '{tgt}')" for ln, tgt in violations)
        raise ValueError(
            f'Forbidden absolute path or file:// URL detected in "{src_abs}":\n'
            f"{lines_summary}\n"
            "Documentation links must be relative paths (e.g. '../path.md') "
            "and must not reference local filesystem paths."
        )


def validate_markdown_images(src_abs: str, content: str) -> None:
    """Check for missing local static images referenced via ![alt](path) in markdown."""
    src_dir = os.path.dirname(src_abs)
    masked = _mask_code_blocks(content)
    pattern = re.compile(r"!\[(.*?)\]\((.*?)\)")
    for match in pattern.finditer(masked):
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
    excluded_files: set[str] | None = None,
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
        # Exclude hidden dirs, __pycache__, and output dir if inside input dir
        dirnames[:] = [
            d
            for d in dirnames
            if not d.startswith(".")
            and d != "__pycache__"
            and not (
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


def resolve_multi_locale_dest(
    default_base_dir: str,
    default_stem: str,
    output_file: str | None,
    lang: str,
    ext: str,
) -> str:
    """Resolve ``<stem>_<lang><ext>`` output path for multi-locale PDF/DOCX builds.

    Args:
        default_base_dir: Default directory when ``output_file`` is omitted.
        default_stem: Base project stem (e.g. ``'drawlib-dogfooding'``).
        output_file: Optional CLI ``-o`` file or directory path.
        lang: Canonical language code (e.g. ``'en'``, ``'ja'``).
        ext: Target extension with leading dot (e.g. ``'.pdf'`` or ``'.docx'``).

    Returns:
        str: Resolved absolute path ending in ``_<lang><ext>``.
    """
    if output_file:
        if os.path.isdir(output_file) or output_file.endswith(os.sep) or output_file.endswith("/"):
            return os.path.abspath(os.path.join(output_file, f"{default_stem}_{lang}{ext}"))
        out_abs = os.path.abspath(output_file)
        stem_prefix, out_ext = os.path.splitext(out_abs)
        if out_ext.lower() == ext.lower():
            return f"{stem_prefix}_{lang}{out_ext}"
        return f"{out_abs}_{lang}{ext}"
    return os.path.abspath(os.path.join(default_base_dir, f"{default_stem}_{lang}{ext}"))


def resolve_doc_locale_and_root(path_abs: str) -> tuple[str, ProjectManifest | None, str]:
    """Resolve ``(lang, manifest, project_root_abs)`` for a single file or single-locale directory."""
    from drawlib._builder._common.manifest import find_project_manifest

    search_dir = path_abs if os.path.isdir(path_abs) else os.path.dirname(path_abs)
    found = find_project_manifest(path_abs, max_up=2)
    if found is None:
        return "en", None, search_dir

    proj_root, manifest = found
    if manifest.i18n is not None:
        rel = os.path.relpath(path_abs, proj_root)
        first_part = rel.split(os.sep)[0]
        if first_part in manifest.i18n.langs:
            return first_part, manifest, proj_root
        return manifest.i18n.default_lang, manifest, proj_root

    return manifest.effective_lang, manifest, proj_root


def write_root_redirect_html(
    out_dir_abs: str,
    default_lang: str,
    target_rel: str = "index.html",
    title: str = "Redirecting...",
    *,
    canonical_url: str | None = None,
    extra_head_html: str = "",
) -> str:
    """Write a root ``index.html`` redirecting to ``<default_lang>/<target_rel>`` with query/hash preserved.

    Args:
        out_dir_abs: Root output HTML directory.
        default_lang: Default canonical language directory name (e.g. ``'en'``).
        target_rel: Target HTML filename inside ``<default_lang>/``.
        title: HTML page title.
        canonical_url: Optional absolute canonical URL override (defaults to relative ``<default_lang>/<target_rel>``).
        extra_head_html: Optional pre-escaped ``<meta>``/``<link>`` lines to insert inside ``<head>``.

    Returns:
        str: Absolute path to the written ``index.html``.
    """
    import html as html_lib  # noqa: PLC0415
    import json  # noqa: PLC0415

    target_url = f"{default_lang}/{target_rel}"
    esc_url = html_lib.escape(target_url, quote=True)
    esc_canonical = html_lib.escape(canonical_url if canonical_url else target_url, quote=True)
    esc_title = html_lib.escape(title)
    js_url_literal = json.dumps(target_url)
    extra_block = f"{extra_head_html}\n" if extra_head_html else ""
    content = (
        "<!DOCTYPE html>\n"
        f'<html lang="{html_lib.escape(default_lang, quote=True)}">\n'
        "<head>\n"
        '  <meta charset="UTF-8">\n'
        f'  <meta http-equiv="refresh" content="0; url={esc_url}">\n'
        f'  <link rel="canonical" href="{esc_canonical}">\n'
        f"  <title>{esc_title}</title>\n"
        f"{extra_block}"
        "  <script>\n"
        f"    window.location.replace({js_url_literal} + window.location.search + window.location.hash);\n"
        "  </script>\n"
        "</head>\n"
        "<body>\n"
        f'  <p>Redirecting to <a href="{esc_url}">{esc_url}</a>...</p>\n'
        "</body>\n"
        "</html>\n"
    )
    os.makedirs(out_dir_abs, exist_ok=True)
    dest_abs = os.path.join(out_dir_abs, "index.html")
    with open(dest_abs, "w", encoding="utf-8") as f:
        f.write(content)
    return dest_abs

