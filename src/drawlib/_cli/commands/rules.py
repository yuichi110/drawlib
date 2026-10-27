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
from typing import Annotated, Final

import typer

from drawlib._builder.rules_builder import (
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
    "style-guide": "Diagram design principles, visual hierarchy, 8-color semantic system, and layout best practices",
    "review-guide": "Autonomous 3-stage multimodal review loop, 720pt typography scaling, and quality criteria",
    "anim-guide": "Animation design principles, loop idioms, and component animation patterns across all modules",
    "slide-guide": "Slide deck story arc, Dual-Layer (::: block vs. ::: note) rule, and visual best practices",
    "project-overview": "Project scaffolding (init), choosing among the 4 project archetypes, and cache architecture",
    "project-images": "Standalone Python diagram scripts (images_src/*.py), clear() lifecycle, and batch image build",
    "project-doc": "Linear technical documents, whitepapers, cover/ToC, and A4 vector PDF export (doc_src/)",
    "project-site": "Multi-page documentation websites, navbar.md sidebar rules, and Top Hero layout (docs_src/)",
    "project-slide": "16:9 presentation slide decks, 1920x1080 ::: block/note syntax, and Presenter View (slide_src/)",
    "cli": "Document compilation, export, preview, and cache CLI commands",
    "api": "Comprehensive API index and quick reference cheat sheet for all Drawlib modules",
}

LIBRARY_TOPICS: Final[dict[str, str]] = {
    # Core Modules
    "lib-canvas": "Canvas configuration, coordinate space, clear/save lifecycle, and background",
    "lib-anim": "Animation configuration, formats (APNG, Animated WebP), and multi-step diagram flows",
    "lib-lines": "Straight, curved, bezier, arc, and chained lines with arrowheads",
    "lib-text": "Text rendering, formatting, alignment, and fonts",
    "lib-preset-colors": "Color models, RGB/RGBA tuples, hex conversion, and palette classes",
    "lib-styles": "Styles and utils architecture, active preset styles, colors palette, and dynamic custom scripts",
    "lib-preset-styles": "Pre-defined style naming rules and color palette classes",
    "lib-fonts": "Font configuration, system/file fonts, CJK/multilingual typography, and cache",
    "lib-images": "Embedding raster images, Dimage filters/transformations, and get_dimage_from_code",
    "lib-math": "Geometry helpers, coordinate calculations, angles, distance, and path interpolation",
    "lib-types": "Type models, Style class, base classes, and Drawlib type conventions",
    "lib-tools": "Python developer API for document building, diagram export, and cache management",
    "lib-slide": "Python API for presentation slides (current_slide, SlideContext, BoundingBox, build_slide)",
    # Shapes (drawlib.shapes)
    "lib-shapes-overview": "Overview of 43 geometric shapes, center-anchor geometry, and sub-topic routing",
    "lib-shapes-basic": "Basic curved shapes (circle, ellipse, wedge, fan, arc, cylinder)",
    "lib-shapes-polygon": "Planar polygons (rectangle, parallelogram, rhombus, trapezoid, triangle, star)",
    "lib-shapes-arrow": "Arrow shapes (arrow, arrow_arc, arrow_polyline, chevron)",
    "lib-shapes-badge": "Badge, shield, tag, ribbon, seal, medal, banner, bookmark, and callout shapes",
    "lib-shapes-container": "3D and container shapes (cylinder, cube, document, funnel, cloud, brace)",
    "lib-shapes-symbol": "Symbolic primitives (gear, cross, checkmark, lightning, heart, cloud, puzzle, lock, key)",
    # Icons (drawlib.icons)
    "lib-icons-overview": "Overview of 34 icon suites, font_icon, center-anchor sizing, and asset caching",
    "lib-icons-phosphor": "Phosphor vector font icons (thin, light, regular, bold, fill) and custom font_icon",
    "lib-icons-gcp": "Google Cloud Platform (GCP) official architecture icons",
    "lib-icons-aws": "Amazon Web Services (AWS) official architecture icons",
    "lib-icons-azure": "Microsoft Azure official architecture icons",
    "lib-icons-ai": "AI & Machine Learning domain and original brand icons",
    "lib-icons-business": "Business & Finance domain and original brand icons",
    "lib-icons-client": "Client Devices, Browsers & OS domain and original brand icons",
    "lib-icons-cloud": "Cloud Platforms & SaaS domain and original brand icons",
    "lib-icons-cnative": "Cloud Native & Kubernetes (CNCF) domain and original brand icons",
    "lib-icons-code": "Programming Languages & Frameworks domain and original brand icons",
    "lib-icons-data": "Databases, Analytics & Messaging domain and original brand icons",
    "lib-icons-devops": "DevOps, CI/CD & Observability domain and original brand icons",
    "lib-icons-facility": "Facilities, Buildings & IoT domain and original brand icons",
    "lib-icons-itservice": "IT Service Management & Operations domain and original brand icons",
    "lib-icons-network": "Networking, DNS & Telecom domain and original brand icons",
    "lib-icons-security": "Cybersecurity, IAM & Compliance domain and original brand icons",
    "lib-icons-server": "Servers, Compute & Hardware domain and original brand icons",
    "lib-icons-social": "Social Media & Communication domain and original brand icons",
    "lib-icons-workspace": "Workspace, Collaboration & Productivity domain and original brand icons",
    # SmartArts (drawlib.smartarts)
    "lib-smartarts-overview": "Overview of 18 SmartArt components, coordinate anchor rules, and sub-topic routing",
    "lib-smartarts-table": "Table component with headers, cell styling, merging, and flexible column/row sizing",
    "lib-smartarts-tree": "TreeNode hierarchical directory and taxonomy tree component",
    "lib-smartarts-mindmap": "MindMapNode 4-directional radial brainstorming and concept map component",
    "lib-smartarts-box-list": "BoxList linear horizontal/vertical box sequence component",
    "lib-smartarts-bullet-points": "BulletPoints structured multi-level typography list component",
    "lib-smartarts-chevron-process": "ChevronProcess sequential pipeline and stage flow component",
    "lib-smartarts-cycle": "Cycle circular lifecycle and feedback loop component",
    "lib-smartarts-grid-layout": "GridLayout multi-column/row matrix and card grid component",
    "lib-smartarts-pyramid": "Pyramid layered hierarchy and funnel structure component",
    "lib-smartarts-source-code": "SourceCode syntax-highlighted code block and terminal window component",
    "lib-smartarts-geomap": "GeoMap world, regional, and country vector map visualization component",
    "lib-smartarts-kpi-cards": "KpiCards executive metric and KPI dashboard card grid component",
    "lib-smartarts-card-list": "CardList icon/badge feature card list and grid component",
    "lib-smartarts-roadmap": "Roadmap chronological milestone and phase timeline component",
    "lib-smartarts-panel": "Panel titled container frame with get_content_box layout helper",
    "lib-smartarts-calendar": "MonthCalendar, WeekCalendar, and DayCalendar schedule and timetable components",
    # Charts (drawlib.charts)
    "lib-charts-overview": "Overview of 9 chart types, Axis configuration, legends, and animation draw_ratio",
    "lib-charts-bar": "BarChart grouped/stacked vertical and horizontal bar charts",
    "lib-charts-line": "LineChart multi-series trend lines with point markers",
    "lib-charts-area": "AreaChart standard and stacked filled area charts",
    "lib-charts-pie": "PieChart pie and donut proportional charts",
    "lib-charts-radar": "RadarChart spider/web multi-axis comparison charts",
    "lib-charts-scatter": "ScatterChart 2D coordinate points and bubble series charts",
    "lib-charts-gantt": "GanttChart project schedule, sections, tasks, milestones, and markers",
    "lib-charts-heatmap": "HeatmapChart 2D matrix density grids and HeatmapOverlay spatial thermal overlays",
    # Diagrams (drawlib.diagrams)
    "lib-diagrams-overview": "Overview of 6 diagram engines, local coordinates, routing, and sub-topic routing",
    "lib-diagrams-architecture": "ArchitectureDiagram cloud/system topology with Node, NodeGroup, Edge, and icons",
    "lib-diagrams-flow": "FlowDiagram workflows, decision trees, and swimlanes (Process, Decision, Lane)",
    "lib-diagrams-sequence": "SequenceDiagram participant lifelines, sync/async messages, notes, and blocks",
    "lib-diagrams-state": "StateDiagram UML state machines (State, Initial, Final, Choice, ForkJoin, StateNote)",
    "lib-diagrams-class": "ClassDiagram OOP UML class models (ClassNode, Attribute, Method, Relationship, Visibility)",
    "lib-diagrams-er": "ERDiagram database schemas (Entity, Column, PK/FK badges, Cardinality relationships)",
    # Graph Layout Solvers (drawlib.graph)
    "lib-graph-overview": "Overview of pure coordinate graph layout solvers (get_layout, NodeLayout, to_code)",
    "lib-graph-architecture": "ArchitectureGraph clustered multi-tier cloud topology layout solver",
    "lib-graph-layer": "LayerGraph Sugiyama hierarchical DAG layout solver",
    "lib-graph-tree": "TreeGraph Reingold-Tilford tidy tree layout solver",
    "lib-graph-radial": "RadialGraph concentric ring and star topology layout solver",
    "lib-graph-grid": "GridGraph uniform row/column matrix and snake flow layout solver",
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
        str | None,
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
