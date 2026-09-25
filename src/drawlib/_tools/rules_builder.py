# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Rules compiler, cache manager, and on-demand illustration generator for Drawlib."""

from __future__ import annotations

import contextlib
import importlib.resources
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Final, Sequence

from drawlib._core.l1_core import RULES_DIR_PATH
from drawlib._tools.doc_builder import build_markdown

AVAILABLE_TOPICS: Final[tuple[str, ...]] = (
    "overview",
    "overview_min",
    "canvas",
    "shapes",
    "lines",
    "text",
    "colors",
    "fonts",
    "images",
    "math",
    "types",
    "preset_styles",
    "icons",
    "smartarts",
    "charts",
    "diagrams",
    "tools",
    "cli",
    "docs_build",
)

INSTRUCTION_MARKER: Final[str] = "Instructions for AI Agents & Developers"


def _normalize_topic(topic: str) -> str:
    """Normalize topic name and handle historical aliases.

    Args:
        topic: Input topic string.

    Returns:
        str: Canonical topic name.

    Raises:
        ValueError: If topic name is unknown.
    """
    clean = topic.strip().lower()
    if clean in {"doc_build", "docs", "doc"}:
        clean = "docs_build"
    elif clean in {"theme", "themes"}:
        clean = "preset_styles"
    elif clean in {"overview-min", "overview_min", "overviewmin", "min"}:
        clean = "overview_min"
    elif clean in {"color", "colour", "colours"}:
        clean = "colors"
    elif clean in {"font"}:
        clean = "fonts"
    elif clean in {"image", "img"}:
        clean = "images"
    elif clean in {"type", "style", "styles"}:
        clean = "types"
    elif clean in {"tool"}:
        clean = "tools"

    if clean not in AVAILABLE_TOPICS:
        raise ValueError(f"Unknown rule topic '{topic}'. Available topics: {', '.join(AVAILABLE_TOPICS)}")
    return clean


def get_rule_source_path(topic: str) -> Path:
    """Get the filesystem path to a source rule Markdown file in drawlib._rules.

    Args:
        topic: Topic name.

    Returns:
        Path: Filesystem path to the source rule Markdown file.
    """
    canonical = _normalize_topic(topic)
    res = importlib.resources.files("drawlib._rules").joinpath(f"{canonical}.md")
    return Path(str(res))


def get_rule_target_path(topic: str) -> Path:
    """Get the filesystem path to a cached rule Markdown file in _assets/rules.

    Args:
        topic: Topic name.

    Returns:
        Path: Filesystem path to the cached rule Markdown file.
    """
    canonical = _normalize_topic(topic)
    return Path(RULES_DIR_PATH) / f"{canonical}.md"


def is_rule_cached(topic: str) -> bool:
    """Check if the rendered rule and its illustrations are cached and up-to-date.

    Args:
        topic: Topic name.

    Returns:
        bool: True if cached document exists and its mtime is newer than or equal to source.
    """
    canonical = _normalize_topic(topic)
    target_path = get_rule_target_path(canonical)
    if not target_path.is_file():
        return False

    source_path = get_rule_source_path(canonical)
    if not source_path.is_file():
        return True

    return target_path.stat().st_mtime >= source_path.stat().st_mtime


def _rewrite_image_paths_to_runtime(content: str, topic: str) -> str:
    """Rewrite relative rule image links to portable PYTHON_RUNTIME path notation.

    Args:
        content: Markdown content with relative image links.
        topic: Rule topic name (e.g. 'overview', 'shapes').

    Returns:
        str: Markdown content with image links rewritten to PYTHON_RUNTIME/site-packages/...
    """
    prefix = f"PYTHON_RUNTIME/site-packages/drawlib/_assets/rules/{topic}_images/"

    # 1. Standard Markdown image syntax: ![alt](<topic>_images/<file>)
    md_pattern = rf"!\[(.*?)\]\({re.escape(topic)}_images/([^)]+)\)"
    content = re.sub(md_pattern, rf"![\1]({prefix}\2)", content)

    # 2. HTML <img> tags with double quotes: src="<topic>_images/<file>"
    html_pattern_dq = rf'(<img\s+[^>]*?src="){re.escape(topic)}_images/([^"]+)(")'
    content = re.sub(html_pattern_dq, rf"\1{prefix}\2\3", content)

    # 3. HTML <img> tags with single quotes: src='<topic>_images/<file>'
    html_pattern_sq = rf"(<img\s+[^>]*?src='){re.escape(topic)}_images/([^']+)(')"
    content = re.sub(html_pattern_sq, rf"\1{prefix}\2\3", content)

    return content


def _inject_agent_instructions(content: str, topic: str) -> str:
    """Inject AI Agent and developer instructions banner directly below the first H1 header.

    Args:
        content: Rendered Markdown content.
        topic: Topic name.

    Returns:
        str: Markdown content with instructions banner injected.
    """
    if INSTRUCTION_MARKER in content:
        return content

    banner = (
        "> [!NOTE]\n"
        "> **Instructions for AI Agents & Developers**:\n"
        f"> This document is compiled from `drawlib` core rules and companion illustrations are located at:\n"
        f"> `PYTHON_RUNTIME/site-packages/drawlib/_assets/rules/{topic}_images/<n>.png`\n"
        ">\n"
        "> (Resolve `PYTHON_RUNTIME` to your active Python / virtualenv environment path to inspect images).\n"
        "> You can inspect any image directly using your file/image viewing tool (`view_file`, etc.) "
        "to visually verify the layout, spatial positioning, coordinate alignment, and styling produced "
        "by the corresponding Python code block above it.\n"
    )

    lines = content.splitlines(keepends=True)
    h1_idx = -1
    for idx, line in enumerate(lines):
        if line.strip().startswith("# "):
            h1_idx = idx
            break

    if h1_idx != -1:
        lines.insert(h1_idx + 1, "\n" + banner + "\n")
        return "".join(lines)

    return banner + "\n" + content


def build_rule(topic: str, force: bool = False, quiet: bool = False) -> str:
    """Compile a single rule topic and its illustrations into _assets/rules/.

    Args:
        topic: Topic name to compile.
        force: If True, recompile even if the cached document is up-to-date.
        quiet: If True, suppress progress messages to sys.stderr.

    Returns:
        str: Full text content of the rendered rule Markdown file.

    Raises:
        ValueError: If topic is unknown.
        OSError: If compilation fails due to filesystem errors.
    """
    canonical = _normalize_topic(topic)
    target_path = get_rule_target_path(canonical)
    source_path = get_rule_source_path(canonical)

    if not force and is_rule_cached(canonical):
        return target_path.read_text(encoding="utf-8")

    if not quiet:
        sys.stderr.write(f"[drawlib] Building illustrations for rule '{canonical}' (on-demand)... ")
        sys.stderr.flush()

    target_path.parent.mkdir(parents=True, exist_ok=True)

    if quiet:
        with open(os.devnull, "w", encoding="utf-8") as devnull, contextlib.redirect_stdout(devnull):
            build_markdown(input_path=str(source_path), output=str(target_path))
    else:
        with contextlib.redirect_stdout(sys.stderr):
            build_markdown(input_path=str(source_path), output=str(target_path))

    rendered_text = target_path.read_text(encoding="utf-8")
    rewritten_text = _rewrite_image_paths_to_runtime(rendered_text, topic=canonical)
    final_text = _inject_agent_instructions(
        content=rewritten_text,
        topic=canonical,
    )
    target_path.write_text(final_text, encoding="utf-8")

    if not quiet:
        sys.stderr.write("Done.\n")
        sys.stderr.flush()

    return final_text


def build_all_rules(force: bool = False, quiet: bool = False) -> list[str]:
    """Compile all available rule topics and illustrations into _assets/rules/.

    Args:
        force: If True, recompile even if up-to-date.
        quiet: If True, suppress progress output.

    Returns:
        list[str]: List of canonical topic names successfully built.
    """
    built: list[str] = []
    for topic in AVAILABLE_TOPICS:
        build_rule(topic, force=force, quiet=quiet)
        built.append(topic)
    return built


def clean_rules_cache() -> None:
    """Delete all cached rule documents and generated illustration images in _assets/rules/."""
    cache_dir = Path(RULES_DIR_PATH)
    if not cache_dir.exists():
        return

    for item in cache_dir.iterdir():
        if item.name in {"__init__.py", ".gitignore"}:
            continue
        if item.is_file():
            item.unlink()
        elif item.is_dir():
            shutil.rmtree(item)


def get_rule_markdown(
    topic: str,
    rebuild: bool = False,
    raw: bool = False,
    quiet: bool = False,
) -> str:
    """Retrieve rule markdown content, building illustrations on demand if needed.

    Args:
        topic: Topic name, e.g. 'shapes', 'overview'.
        rebuild: Force rebuilding illustrations.
        raw: Return raw source Markdown without building or checking cache.
        quiet: Suppress progress messages to stderr.

    Returns:
        str: Rule markdown content.
    """
    canonical = _normalize_topic(topic)
    source_path = get_rule_source_path(canonical)

    if raw:
        return source_path.read_text(encoding="utf-8")

    try:
        return build_rule(canonical, force=rebuild, quiet=quiet)
    except (PermissionError, OSError) as err:
        if not quiet:
            sys.stderr.write(f"[drawlib] Warning: Rules cache unavailable ({err}). Falling back to raw rules.\n")
            sys.stderr.flush()
        return source_path.read_text(encoding="utf-8")
