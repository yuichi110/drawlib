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

import importlib.resources
import sys
from typing import Annotated, Final, Optional

import typer

rules_app = typer.Typer(
    name="rules",
    help="Display drawing guidelines, API rules, and code examples for AI coding agents.",
    no_args_is_help=False,
    context_settings={"help_option_names": ["-h", "--help"]},
)

TOPIC_DESCRIPTIONS: Final[dict[str, str]] = {
    "overview": "Canvas lifecycle, coordinate system, core imports, and workflow",
    "cli": "Document compilation, export, preview, and cache CLI commands",
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
) -> None:
    """Display rules and examples for a specified topic (defaults to overview).

    Args:
        topic: The rule topic name to display (e.g. shapes, lines, text).
    """
    selected_topic = "overview" if topic is None else topic.strip().lower()

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
        rule_resource = importlib.resources.files("drawlib._rules").joinpath(f"{selected_topic}.md")
        content = rule_resource.read_text(encoding="utf-8")
        sys.stdout.write(content)
        if not content.endswith("\n"):
            sys.stdout.write("\n")
        sys.stdout.flush()
    except Exception as exc:
        print(f"Error: Failed to load rule topic '{selected_topic}': {exc}", file=sys.stderr)
        raise typer.Exit(code=1) from exc


@rules_app.command("list")
def cmd_rules_list() -> None:
    """List all available rule topics and their descriptions."""
    print("Available Drawlib Rule Topics:\n")
    max_len = max(len(t) for t in TOPIC_DESCRIPTIONS)
    for topic, desc in TOPIC_DESCRIPTIONS.items():
        print(f"  - {topic:<{max_len}} : {desc}")
    print("\nRun `drawlib rules show <topic>` to view rules for a specific topic.")


@rules_app.callback(invoke_without_command=True)
def rules_default_callback(ctx: typer.Context) -> None:
    """Default callback when `drawlib rules` is executed without subcommands."""
    if ctx.invoked_subcommand is None:
        cmd_rules_show("overview")
