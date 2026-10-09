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
    "style-guide": "Diagram design principles, visual hierarchy, 6-color semantic system, and layout best practices",
    "review-guide": "Autonomous 3-stage multimodal review loop, 720pt typography scaling, and quality criteria",
    "anim-guide": "Animation design principles, loop idioms, and component animation patterns across all modules",
    "project-overview": "Project scaffolding (init), choosing among the 4 project archetypes, and cache architecture",
    "project-images": "Standalone Python diagram scripts (images_src/*.py), clear() lifecycle, and batch image build",
    "project-doc": "Linear technical documents, whitepapers, cover/ToC, and A4 vector PDF export (doc_src/)",
    "project-site": "Multi-page documentation websites, navbar.md sidebar rules, and Top Hero layout (docs_src/)",
    "project-slide": "16:9 presentation slide decks, 1920x1080 ::: block/note syntax, and Presenter View (slide_src/)",
    "cli": "Document compilation, export, preview, and cache CLI commands",
    "api": "Comprehensive API index and quick reference cheat sheet for all Drawlib modules",
}

LIBRARY_TOPICS: Final[dict[str, str]] = {
    "lib-canvas": "Canvas configuration, coordinate space, clear/save lifecycle, and background",
    "lib-anim": "Animation configuration, formats (APNG, Animated WebP), and multi-step diagram flows",
    "lib-shapes": "Rectangles, circles, ellipses, wedges, and polygons",
    "lib-lines": "Straight, curved, and chained lines with arrowheads",
    "lib-text": "Text rendering, formatting, alignment, and fonts",
    "lib-preset-colors": "Color models, RGB/RGBA tuples, hex conversion, and palette classes",
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
    "lib-graph": "Declarative graph layout solvers (Architecture, Layer, Tree, Radial, Grid) and code export",
    "lib-tools": "Python developer API for document building, diagram export, and cache management",
    "lib-slide": "Python API for presentation slides (current_slide, SlideContext, BoundingBox, build_slide)",
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
            print(f"  - {t:<20}: {desc}", file=sys.stderr)
        print("\nRun `drawlib rules list` to inspect cache status of all topics.", file=sys.stderr)
        raise typer.Exit(code=1)

    try:
        content = get_rule_markdown(selected_topic, rebuild=rebuild, raw=raw)
        print(content)
    except Exception as exc:
        print(f"Error: Failed to display rule topic '{selected_topic}': {exc}", file=sys.stderr)
        raise typer.Exit(code=1) from exc


@rules_app.command("build", epilog=HELP_EPILOG)
def cmd_rules_build(
    topic: Annotated[
        Optional[str],
        typer.Argument(
            help="Specific topic to build, or 'all' to build all topics.",
        ),
    ] = None,
    force: Annotated[
        bool,
        typer.Option("--force", "-f", help="Rebuild and re-cache illustrations even if they already exist."),
    ] = False,
) -> None:
    """Pre-build and cache illustrations for one or all rule topics.

    Args:
        topic: Topic name or 'all' (default 'all' if omitted).
        force: Force rebuild even if already cached.
    """
    target = (topic or "all").strip().lower().replace("_", "-")

    try:
        if target == "all":
            built = build_all_rules(force=force, quiet=False)
            print(f"\nDone: {len(built)} rule topics ready.")
        elif target in TOPIC_DESCRIPTIONS:
            build_rule(target, force=force, quiet=False)
            print(f"Successfully compiled rule topic '{target}'.")
        else:
            print(f"Error: Unknown rule topic '{topic}'.\n", file=sys.stderr)
            print("Run `drawlib rules list` to inspect available topics.", file=sys.stderr)
            raise typer.Exit(code=1)
    except Exception as exc:
        print(f"Error: Failed to build rules: {exc}", file=sys.stderr)
        raise typer.Exit(code=1) from exc


@rules_app.command("clear", epilog=HELP_EPILOG)
def cmd_rules_clear() -> None:
    """Clear the cached rules illustrations directory (~/.drawlib/cache/rules/)."""
    try:
        clear_rules_cache()
        print("Successfully cleared rule illustrations cache.")
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
