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

from drawlib._builder.doc_builder.processor import DrawlibBlockProcessor
from drawlib._core.l1_core import RULES_DIR_PATH

AVAILABLE_TOPICS: Final[tuple[str, ...]] = (
    "agent-instruction",
    "overview",
    "style-guide",
    "project",
    "cli",
    "api",
    "lib-canvas",
    "lib-anim",
    "lib-shapes",
    "lib-lines",
    "lib-text",
    "lib-preset-colors",
    "lib-styles",
    "lib-preset-styles",
    "lib-fonts",
    "lib-images",
    "lib-icons",
    "lib-math",
    "lib-types",
    "lib-smartarts",
    "lib-charts",
    "lib-diagrams",
    "lib-graph",
    "lib-tools",
    "lib-slide",
)


def _normalize_topic(topic: str) -> str:
    """Normalize topic name.

    Args:
        topic: Input topic string.

    Returns:
        str: Canonical topic name.

    Raises:
        ValueError: If topic name is unknown.
    """
    clean = topic.strip().lower().replace("_", "-")

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
    file_name = canonical.replace("-", "_") + ".md"
    res = importlib.resources.files("drawlib._rules").joinpath(file_name)
    return Path(str(res))


def get_rules_dir() -> Path:
    """Get the filesystem path to the rules cache directory.

    Respects the DRAWLIB_RULES_DIR environment variable if specified.

    Returns:
        Path: Filesystem path to the rules cache directory.
    """
    env_dir = os.environ.get("DRAWLIB_RULES_DIR")
    if env_dir:
        return Path(env_dir)
    return Path(RULES_DIR_PATH)


def get_rule_target_path(topic: str) -> Path:
    """Get the filesystem path to a cached rule Markdown file.

    Args:
        topic: Topic name.

    Returns:
        Path: Filesystem path to the cached rule Markdown file.
    """
    canonical = _normalize_topic(topic)
    file_name = canonical.replace("-", "_") + ".md"
    return get_rules_dir() / file_name


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
        topic: Rule topic name (e.g. 'overview', 'lib-shapes').

    Returns:
        str: Markdown content with image links rewritten to PYTHON_RUNTIME/site-packages/...
    """
    file_stem = topic.replace("-", "_")
    prefix = f"PYTHON_RUNTIME/site-packages/drawlib/_assets/rules/{file_stem}_images/"

    # 1. Standard Markdown image syntax: ![alt](<file_stem>_images/<file>)
    md_pattern = rf"!\[(.*?)\]\({re.escape(file_stem)}_images/([^)]+)\)"
    content = re.sub(md_pattern, rf"![\1]({prefix}\2)", content)

    # 2. HTML <img> tags with double quotes: src="<file_stem>_images/<file>"
    html_pattern_dq = rf'(<img\s+[^>]*?src="){re.escape(file_stem)}_images/([^"]+)(")'
    content = re.sub(html_pattern_dq, rf"\1{prefix}\2\3", content)

    # 3. HTML <img> tags with single quotes: src='<file_stem>_images/<file>'
    html_pattern_sq = rf"(<img\s+[^>]*?src='){re.escape(file_stem)}_images/([^']+)(')"
    content = re.sub(html_pattern_sq, rf"\1{prefix}\2\3", content)

    return content


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
    processor = DrawlibBlockProcessor(require_file=False)
    source_content = source_path.read_text(encoding="utf-8")

    if quiet:
        with open(os.devnull, "w", encoding="utf-8") as devnull, contextlib.redirect_stdout(devnull):
            rendered_text = processor.process_markdown(
                source_content,
                doc_base_name=canonical,
                output_dir=str(target_path.parent),
                use_markdown_syntax=True,
                source_filename=str(source_path),
            )
    else:
        with contextlib.redirect_stdout(sys.stderr):
            rendered_text = processor.process_markdown(
                source_content,
                doc_base_name=canonical,
                output_dir=str(target_path.parent),
                use_markdown_syntax=True,
                source_filename=str(source_path),
            )

    rewritten_text = _rewrite_image_paths_to_runtime(rendered_text, topic=canonical)
    target_path.write_text(rewritten_text, encoding="utf-8")

    if not quiet:
        sys.stderr.write("Done.\n")
        sys.stderr.flush()

    return rewritten_text


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


def clear_rules_cache() -> None:
    """Delete all cached rule documents and generated illustration images."""
    cache_dir = get_rules_dir()
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
