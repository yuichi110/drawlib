# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Typer sub-application for `drawlib rules` commands."""

from __future__ import annotations

import os
import sys
from typing import Annotated, Final, Optional

import typer

from drawlib._builder.rules_builder import (
    AVAILABLE_TOPICS,
    build_all_rules,
    build_rule,
    clear_rules_cache,
    get_rule_markdown,
    is_rule_cached,
)
from drawlib._cli._help import HELP_EPILOG

rules_app = typer.Typer(
    name="rules",
    help="Display drawing guidelines, API rules, and code examples for AI coding agents.",
    epilog=HELP_EPILOG,
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)

GENERAL_TOPICS: Final[dict[str, str]] = {
    "agent-instruction": "AI agent bootstrap instructions, workflow loop, and capabilities",
    "overview": "Canvas lifecycle, coordinate system, core imports, and workflow",
    "style-guide": "Diagram design principles, visual hierarchy, 60-30-10 color rules, and layout best practices",
    "project": "Project scaffolding (init), directory structure (docs_src), navbar rules, and build workflows",
    "cli": "Document compilation, export, preview, and cache CLI commands",
}

LIBRARY_TOPICS: Final[dict[str, str]] = {
    "lib-canvas": "Canvas configuration, coordinate space, clear/save lifecycle, and background",
    "lib-shapes": "Rectangles, circles, ellipses, wedges, and polygons",
    "lib-lines": "Straight, curved, and chained lines with arrowheads",
    "lib-text": "Text rendering, formatting, alignment, and fonts",
    "lib-colors": "Color models, RGB/RGBA tuples, hex conversion, and palette classes",
    "lib-styles": "Styles and utils architecture, active preset styles, colors palette, and dynamic custom scripts",
    "lib-preset-styles": "Pre-defined style naming rules and color palette classes",
    "lib-fonts": "Font configuration, system/file fonts, CJK/multilingual typography, and cache",
    "lib-images": "Embedding bitmap and vector images, scaling, rotation, and Dimage",
    "lib-icons": "Phosphor, FontAwesome, and GCP cloud architecture icons",
    "lib-math": "Geometry helpers, coordinate calculations, angles, distance, and bounding box",
    "lib-types": "Type models, Style class, base classes, and Drawlib type conventions",
    "lib-smartarts": "Tables, trees, mindmaps, and structured visual elements",
    "lib-charts": "Bar, line, pie, scatter, radar, area, and Gantt charts",
    "lib-diagrams": "Flowcharts, sequence, state, class, ER, and architecture diagrams",
    "lib-tools": "Python developer API for document building, diagram export, and cache management",
}

TOPIC_DESCRIPTIONS: Final[dict[str, str]] = {
    **GENERAL_TOPICS,
    **LIBRARY_TOPICS,
}


@rules_app.command("show", epilog=HELP_EPILOG)
def cmd_rules_show(
    topic: Annotated[
        str,
        typer.Argument(
            help="Rule topic to display (e.g. overview, lib-shapes, cli).",
        ),
    ],
    rebuild: Annotated[
        bool,
        typer.Option("--rebuild", "-r", help="Force rebuilding rule illustrations even if cache exists."),
    ] = False,
    raw: Annotated[
        bool,
        typer.Option("--raw", help="Output raw source Markdown without building or checking illustration cache."),
    ] = False,
) -> None:
    """Display rules and examples for a specified topic.

    Args:
        topic: The rule topic name to display (e.g. lib-shapes, lib-lines, overview).
        rebuild: Whether to force rebuilding illustrations.
        raw: Whether to bypass cache and output raw Markdown source.
    """
    selected_topic = topic.strip().lower().replace("_", "-")

    if selected_topic not in TOPIC_DESCRIPTIONS:
        print(f"Error: Unknown rule topic '{topic}'.\n", file=sys.stderr)
        print("Available topics:", file=sys.stderr)
        for t, desc in TOPIC_DESCRIPTIONS.items():
            print(f"  - {t:<18}: {desc}", file=sys.stderr)
        raise typer.Exit(code=1)

    try:
        content = get_rule_markdown(selected_topic, rebuild=rebuild, raw=raw)
    except Exception as exc:
        print(f"Error: Failed to load rule topic '{selected_topic}': {exc}", file=sys.stderr)
        raise typer.Exit(code=1) from exc

    try:
        sys.stdout.write(content)
        if not content.endswith("\n"):
            sys.stdout.write("\n")
        sys.stdout.flush()
    except BrokenPipeError:
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
        return


@rules_app.command("build", epilog=HELP_EPILOG)
def cmd_rules_build(
    topic: Annotated[
        Optional[str],
        typer.Argument(
            help="Specific rule topic to compile (e.g. lib-shapes, overview).",
        ),
    ] = None,
    all_topics: Annotated[
        bool,
        typer.Option("--all", "-a", help="Compile illustrations for all available rule topics."),
    ] = False,
    force: Annotated[
        bool,
        typer.Option("--force", "-f", help="Force recompile even if cached documents are up-to-date."),
    ] = False,
) -> None:
    """Pre-build rule documents and illustrations into _assets/rules/.

    Args:
        topic: Topic name to compile.
        all_topics: If True, compile all topics.
        force: If True, force recompile.
    """
    if not topic and not all_topics:
        print("Error: Specify a topic name or pass --all to build all topics.", file=sys.stderr)
        raise typer.Exit(code=1)

    try:
        if all_topics or topic == "all":
            built = build_all_rules(force=force, quiet=False)
            print(f"Successfully compiled {len(built)} rule topic(s).")
        elif topic:
            selected_topic = topic.strip().lower().replace("_", "-")
            if selected_topic not in TOPIC_DESCRIPTIONS:
                print(f"Error: Unknown rule topic '{topic}'.", file=sys.stderr)
                raise typer.Exit(code=1)

            build_rule(selected_topic, force=force, quiet=False)
            print(f"Successfully compiled rule topic '{selected_topic}'.")
    except Exception as exc:
        print(f"Error: Failed to build rules: {exc}", file=sys.stderr)
        raise typer.Exit(code=1) from exc


@rules_app.command("clear", epilog=HELP_EPILOG)
def cmd_rules_clear() -> None:
    """Delete all cached rule documents and generated illustration images in _assets/rules/."""
    try:
        clear_rules_cache()
        print("Successfully cleared rules illustration cache (_assets/rules/).")
    except Exception as exc:
        print(f"Error: Failed to clear rules cache: {exc}", file=sys.stderr)
        raise typer.Exit(code=1) from exc


@rules_app.command("list", epilog=HELP_EPILOG)
def cmd_rules_list() -> None:
    """List all available rule topics, their descriptions, and cache status."""
    print("Available Drawlib Rule Topics:\n")
    max_len = max(len(t) for t in TOPIC_DESCRIPTIONS)

    print("General Guidelines:")
    for topic, desc in GENERAL_TOPICS.items():
        cached_tag = "[cached]" if is_rule_cached(topic) else ""
        print(f"  - {topic:<{max_len}} : {desc} {cached_tag}".rstrip())

    print("\nLibrary Modules (drawlib.*):")
    for topic, desc in LIBRARY_TOPICS.items():
        cached_tag = "[cached]" if is_rule_cached(topic) else ""
        print(f"  - {topic:<{max_len}} : {desc} {cached_tag}".rstrip())

    print("\nRun `drawlib rules show <topic>` to view rules for a specific topic.")
    print("Pass `--rebuild` to regenerate illustrations, or `--raw` to view raw Markdown.")
