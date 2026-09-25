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

import sys
from typing import Annotated, Final, Optional

import typer

from drawlib._tools.rules_builder import (
    AVAILABLE_TOPICS,
    build_all_rules,
    build_rule,
    clean_rules_cache,
    get_rule_markdown,
    is_rule_cached,
)

rules_app = typer.Typer(
    name="rules",
    help="Display drawing guidelines, API rules, and code examples for AI coding agents.",
    no_args_is_help=False,
    context_settings={"help_option_names": ["-h", "--help"]},
)

TOPIC_DESCRIPTIONS: Final[dict[str, str]] = {
    "overview": "Canvas lifecycle, coordinate system, core imports, and workflow",
    "cli": "Document compilation, export, preview, and cache CLI commands",
    "docs_build": "Documentation site structure, navbar rules, scaffolding, and build conventions",
    "shapes": "Rectangles, circles, ellipses, wedges, and polygons",
    "lines": "Straight, curved, and chained lines with arrowheads",
    "text": "Text rendering, formatting, alignment, and fonts",
    "icons": "Phosphor, FontAwesome, and GCP cloud architecture icons",
    "preset_styles": "Pre-defined style naming rules and color palette classes",
    "smartarts": "Tables, trees, mindmaps, and structured visual elements",
    "charts": "Bar, line, pie, scatter, radar, area, and Gantt charts",
    "diagrams": "Flowcharts, sequence, state, class, ER, and architecture diagrams",
}


@rules_app.command("show")
def cmd_rules_show(
    topic: Annotated[
        Optional[str],
        typer.Argument(
            help="Rule topic to display. Defaults to 'overview' if omitted.",
        ),
    ] = None,
    rebuild: Annotated[
        bool,
        typer.Option("--rebuild", "-r", help="Force rebuilding rule illustrations even if cache exists."),
    ] = False,
    raw: Annotated[
        bool,
        typer.Option("--raw", help="Output raw source Markdown without building or checking illustration cache."),
    ] = False,
) -> None:
    """Display rules and examples for a specified topic (defaults to overview).

    Args:
        topic: The rule topic name to display (e.g. shapes, lines, text).
        rebuild: Whether to force rebuilding illustrations.
        raw: Whether to bypass cache and output raw Markdown source.
    """
    selected_topic = "overview" if topic is None else topic.strip().lower()

    if selected_topic in {"doc_build", "docs", "doc"}:
        selected_topic = "docs_build"

    if selected_topic in {"theme", "themes"}:
        print(
            "Note: 'themes' has been replaced by 'preset_styles'. Showing 'preset_styles' rules.\n",
            file=sys.stderr,
        )
        selected_topic = "preset_styles"

    if selected_topic not in TOPIC_DESCRIPTIONS:
        print(f"Error: Unknown rule topic '{topic}'.\n", file=sys.stderr)
        print("Available topics:", file=sys.stderr)
        for t, desc in TOPIC_DESCRIPTIONS.items():
            print(f"  - {t:<14}: {desc}", file=sys.stderr)
        raise typer.Exit(code=1)

    try:
        content = get_rule_markdown(selected_topic, rebuild=rebuild, raw=raw)
        sys.stdout.write(content)
        if not content.endswith("\n"):
            sys.stdout.write("\n")
        sys.stdout.flush()
    except Exception as exc:
        print(f"Error: Failed to load rule topic '{selected_topic}': {exc}", file=sys.stderr)
        raise typer.Exit(code=1) from exc


@rules_app.command("build")
def cmd_rules_build(
    topic: Annotated[
        Optional[str],
        typer.Argument(
            help="Specific rule topic to compile (e.g. shapes, overview).",
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
            selected_topic = topic.strip().lower()
            if selected_topic in {"doc_build", "docs", "doc"}:
                selected_topic = "docs_build"
            elif selected_topic in {"theme", "themes"}:
                selected_topic = "preset_styles"

            if selected_topic not in TOPIC_DESCRIPTIONS:
                print(f"Error: Unknown rule topic '{topic}'.", file=sys.stderr)
                raise typer.Exit(code=1)

            build_rule(selected_topic, force=force, quiet=False)
            print(f"Successfully compiled rule topic '{selected_topic}'.")
    except Exception as exc:
        print(f"Error: Failed to build rules: {exc}", file=sys.stderr)
        raise typer.Exit(code=1) from exc


@rules_app.command("clean")
def cmd_rules_clean() -> None:
    """Delete all cached rule documents and generated illustration images in _assets/rules/."""
    try:
        clean_rules_cache()
        print("Successfully cleaned rules illustration cache (_assets/rules/).")
    except Exception as exc:
        print(f"Error: Failed to clean rules cache: {exc}", file=sys.stderr)
        raise typer.Exit(code=1) from exc


@rules_app.command("list")
def cmd_rules_list() -> None:
    """List all available rule topics, their descriptions, and cache status."""
    print("Available Drawlib Rule Topics:\n")
    max_len = max(len(t) for t in TOPIC_DESCRIPTIONS)
    for topic, desc in TOPIC_DESCRIPTIONS.items():
        cached_tag = "[cached]" if is_rule_cached(topic) else ""
        print(f"  - {topic:<{max_len}} : {desc} {cached_tag}".rstrip())
    print("\nRun `drawlib rules show <topic>` to view rules for a specific topic.")
    print("Pass `--rebuild` to regenerate illustrations, or `--raw` to view raw Markdown.")


@rules_app.callback(invoke_without_command=True)
def rules_default_callback(ctx: typer.Context) -> None:
    """Default callback when `drawlib rules` is executed without subcommands."""
    if ctx.invoked_subcommand is None:
        cmd_rules_show(topic=None)
