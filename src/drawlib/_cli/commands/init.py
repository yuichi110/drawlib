# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Typer sub-application for `drawlib init` project scaffolding commands."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Annotated

import typer

from drawlib._cli._help import HELP_EPILOG
from drawlib._templates import (
    AgentTriggerMode,
    detect_agent_targets,
    init_agent_instruction,
    init_project,
    list_agent_targets,
    list_project_types,
    resolve_project_paths,
)

_HELP_CTX = {"help_option_names": ["-h", "--help"]}

init_app = typer.Typer(
    name="init",
    help="Scaffold starter drawlib projects and AI coding agent instructions.",
    epilog=HELP_EPILOG,
    no_args_is_help=True,
    context_settings=_HELP_CTX,
)

project_app = typer.Typer(
    name="project",
    help="Scaffold starter drawlib projects (doc, site, slide, images).",
    epilog=HELP_EPILOG,
    no_args_is_help=True,
    context_settings=_HELP_CTX,
)
init_app.add_typer(project_app, name="project")


def _print_init_success(
    project_type: str,
    target: str,
    created: list[Path],
) -> None:
    """Print initialization success message and next steps.

    Args:
        project_type: Initialized project type ('doc', 'site', 'slide', 'images').
        target: Target base name (e.g. 'doc', 'spec', 'docs').
        created: List of created file paths.
    """
    paths = resolve_project_paths(project_type=project_type, target=target)
    cwd = Path(".").resolve()
    try:
        rel_src_dir = paths.src_dir.relative_to(cwd).as_posix()
    except ValueError:
        rel_src_dir = paths.src_dir.as_posix()

    print(f"Initialized '{project_type}' project ('{rel_src_dir}/')\n")
    print("Project files created:")
    for file_path in created:
        try:
            rel = file_path.relative_to(cwd)
            print(f"  - {rel}")
        except ValueError:
            print(f"  - {file_path}")

    print("\nNext steps:")
    print(f"  ./{rel_src_dir}/build.sh")
    if project_type == "doc":
        print(f"  ./{rel_src_dir}/build_docx.sh")
    elif project_type == "slide":
        print(f"  ./{rel_src_dir}/build_pptx.sh")

    if project_type in {"site", "doc", "slide"}:
        print(f"  ./{rel_src_dir}/serve.sh")


def _run_init(
    project_type: str,
    target: str,
    style: str | None = None,
    lang: str = "en",
    force: bool = False,
) -> None:
    """Common runner for project initialization subcommands.

    Args:
        project_type: Project type ('doc', 'site', 'slide', 'images').
        target: Base name for project folder and artifacts.
        style: Style preset theme or custom CSS path.
        lang: Starter template language code.
        force: Overwrite existing files if True.
    """
    try:
        created = init_project(
            project_type=project_type,
            target=target,
            force=force,
            lang=lang,
            style=style,
        )
    except FileExistsError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise typer.Exit(code=1) from exc
    except Exception as exc:
        print(f"Error: Failed to initialize project: {exc}", file=sys.stderr)
        raise typer.Exit(code=1) from exc

    _print_init_success(
        project_type=project_type,
        target=target,
        created=created,
    )


@project_app.command("doc", epilog=HELP_EPILOG)
def cmd_init_doc(
    target: Annotated[
        str,
        typer.Argument(
            help="Base name for the document and source folder (creates '<target>_src/').",
        ),
    ] = "doc",
    style: Annotated[
        str | None,
        typer.Option(
            "-s",
            "--style",
            help="Style preset theme ('default', 'google', 'monochrome', etc.) or custom CSS path.",
        ),
    ] = None,
    lang: Annotated[
        str,
        typer.Option(
            "-l",
            "--lang",
            help="Language code ('en', 'ja', etc.) or comma-separated codes for multi-locale doc ('en,ja').",
        ),
    ] = "en",
    force: Annotated[
        bool,
        typer.Option(
            "-f",
            "--force",
            help="Overwrite existing files in destination directory.",
        ),
    ] = False,
) -> None:
    """Scaffold a linear document project (HTML, PDF, Word, Markdown) in the current directory."""
    _run_init(project_type="doc", target=target, style=style, lang=lang, force=force)


@project_app.command("site", epilog=HELP_EPILOG)
def cmd_init_site(
    target: Annotated[
        str,
        typer.Argument(
            help="Base name for the documentation site and source folder (creates '<target>_src/').",
        ),
    ] = "docs",
    style: Annotated[
        str | None,
        typer.Option(
            "-s",
            "--style",
            help="Style preset theme ('default', 'google', 'monochrome', etc.) or custom CSS path.",
        ),
    ] = None,
    lang: Annotated[
        str,
        typer.Option(
            "-l",
            "--lang",
            help="Language code ('en', 'ja', etc.) or comma-separated codes for multi-locale site ('en,ja').",
        ),
    ] = "en",
    force: Annotated[
        bool,
        typer.Option(
            "-f",
            "--force",
            help="Overwrite existing files in destination directory.",
        ),
    ] = False,
) -> None:
    """Scaffold a multi-page documentation website with sidebar navigation in current directory."""
    _run_init(project_type="site", target=target, style=style, lang=lang, force=force)


@project_app.command("slide", epilog=HELP_EPILOG)
def cmd_init_slide(
    target: Annotated[
        str,
        typer.Argument(
            help="Base name for the presentation deck and source folder (creates '<target>_src/').",
        ),
    ] = "slide",
    style: Annotated[
        str | None,
        typer.Option(
            "-s",
            "--style",
            help="Slide style theme ('default', 'default-dark', 'google', 'google-dark', 'monochrome').",
        ),
    ] = None,
    lang: Annotated[
        str,
        typer.Option(
            "-l",
            "--lang",
            help="Language code ('en', 'ja', etc.) or comma-separated codes for multi-locale slide ('en,ja').",
        ),
    ] = "en",
    force: Annotated[
        bool,
        typer.Option(
            "-f",
            "--force",
            help="Overwrite existing files in destination directory.",
        ),
    ] = False,
) -> None:
    """Scaffold a 16:9 presentation slide deck (HTML, PDF, PowerPoint) in current directory."""
    _run_init(project_type="slide", target=target, style=style, lang=lang, force=force)


@project_app.command("images", epilog=HELP_EPILOG)
def cmd_init_images(
    target: Annotated[
        str,
        typer.Argument(
            help="Base name for the illustrations repository and source folder (creates '<target>_src/').",
        ),
    ] = "images",
    style: Annotated[
        str | None,
        typer.Option(
            "-s",
            "--style",
            help="Style preset theme ('default', 'google', 'monochrome', etc.) or custom CSS path.",
        ),
    ] = None,
    lang: Annotated[
        str,
        typer.Option(
            "-l",
            "--lang",
            help="Language code for starter templates and font config ('en', 'ja', 'zh-cn', 'ko', etc.).",
        ),
    ] = "en",
    force: Annotated[
        bool,
        typer.Option(
            "-f",
            "--force",
            help="Overwrite existing files in destination directory.",
        ),
    ] = False,
) -> None:
    """Scaffold a standalone Python illustrations project in current directory."""
    _run_init(project_type="images", target=target, style=style, lang=lang, force=force)


@project_app.command("image", hidden=True, epilog=HELP_EPILOG)
def cmd_init_image_alias(
    target: Annotated[
        str,
        typer.Argument(
            help="Singular alias for 'images'.",
        ),
    ] = "images",
    style: Annotated[str | None, typer.Option("-s", "--style")] = None,
    lang: Annotated[str, typer.Option("-l", "--lang")] = "en",
    force: Annotated[bool, typer.Option("-f", "--force")] = False,
) -> None:
    """Singular alias for `drawlib init project images`."""
    _run_init(project_type="images", target=target, style=style, lang=lang, force=force)


@project_app.command("list", epilog=HELP_EPILOG)
def cmd_init_project_list() -> None:
    """List available Drawlib project types."""
    types = list_project_types()
    print("Available Drawlib Project Types:\n")
    max_len = max(len(t) for t in types)
    for name, desc in types.items():
        print(f"  - {name:<{max_len}} : {desc}")
    print("\nUsage: drawlib init project <type> [target] [-l <langs>] [-s <style>]")


def _print_agent_targets_list() -> None:
    """Print supported AI coding agent instruction targets and output paths."""
    targets = list_agent_targets()
    print("Available AI Coding Agent Targets (`drawlib init agent <target>`):\n")
    max_name = max(len(item["name"]) for item in targets)
    max_path = max(len(item["project_path"]) for item in targets)
    for item in targets:
        name = item["name"]
        proj_path = item["project_path"]
        label = item["label"]
        fmt = item["format"]
        print(f"  - {name:<{max_name}} : {proj_path:<{max_path}}  ({label} — {fmt})")
    print(
        f"  - {'all':<{max_name}} : {'(all modular rules/* files)':<{max_path}}  "
        "(antigravity, claude, cursor, copilot, windsurf, cline, roo)"
    )
    print("\nTrigger Modes (--mode / -m):")
    print("  - auto   (default) : On-demand / task-relevant loading to conserve context tokens")
    print("  - always           : Always-on loading for dedicated Drawlib documentation repositories")
    print("\nExamples:")
    print("  drawlib init agent antigravity")
    print("  drawlib init agent antigravity --mode always")
    print("  drawlib init agent claude cursor copilot")
    print("  drawlib init agent --detect")
    print("  drawlib init agent antigravity --global")


def _resolve_cli_agent_targets(
    raw_agents: list[str],
    detect: bool,
    global_scope: bool,
    directory: str,
) -> list[str]:
    """Validate flags and resolve effective agent target list for CLI execution."""
    if global_scope and detect:
        print("Error: --detect cannot be combined with --global (-g).", file=sys.stderr)
        raise typer.Exit(code=1)

    effective: list[str] = []
    if detect:
        effective.extend(detect_agent_targets(destination=directory))
    effective.extend(raw_agents)

    if not effective:
        resolved_dir = Path(directory).expanduser().resolve()
        print(
            f"Error: No existing AI agent configuration directories or files detected in '{resolved_dir}'.\n"
            "Specify an agent explicitly (e.g. `drawlib init agent antigravity`) "
            "or run `drawlib init agent list`.",
            file=sys.stderr,
        )
        raise typer.Exit(code=1)
    return effective


def _print_agent_init_summary(written: list[Path], scope_label: str) -> None:
    """Print initialized AI agent instruction file paths."""
    cwd = Path(".").resolve()
    print(f"Initialized AI agent instruction file(s) ({scope_label}):")
    for path in written:
        try:
            rel = path.relative_to(cwd)
            print(f"  - {rel.as_posix()}")
        except ValueError:
            print(f"  - {path.as_posix()}")


def _run_init_agent(
    ctx: typer.Context,
    agents: list[str] | None,
    mode: str,
    global_scope: bool,
    detect: bool,
    list_targets: bool,
    directory: str,
    output: str | None,
    force: bool,
) -> None:
    """Execute `drawlib init agent` CLI workflow."""
    raw_agents = list(agents) if agents else []
    if list_targets or (len(raw_agents) == 1 and raw_agents[0].strip().lower() == "list"):
        _print_agent_targets_list()
        return

    if not raw_agents and not detect:
        print(ctx.get_help())
        print("\nRun `drawlib init agent list` to see all supported AI agent targets and output paths.")
        raise typer.Exit(code=0)

    normalized_mode = mode.strip().lower()
    if normalized_mode not in {"auto", "always"}:
        print(f"Error: Invalid mode '{mode}'. Must be 'auto' or 'always'.", file=sys.stderr)
        raise typer.Exit(code=1)
    typed_mode: AgentTriggerMode = "always" if normalized_mode == "always" else "auto"

    effective_agents = _resolve_cli_agent_targets(
        raw_agents=raw_agents,
        detect=detect,
        global_scope=global_scope,
        directory=directory,
    )

    try:
        written = init_agent_instruction(
            agent=effective_agents,
            destination=directory,
            mode=typed_mode,
            global_scope=global_scope,
            output_path=output,
            force=force,
        )
    except (FileExistsError, IsADirectoryError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise typer.Exit(code=1) from exc
    except Exception as exc:
        print(f"Error: Failed to initialize AI agent instructions: {exc}", file=sys.stderr)
        raise typer.Exit(code=1) from exc

    scope_label = "global" if global_scope else f"mode: {typed_mode}"
    _print_agent_init_summary(written=written, scope_label=scope_label)


@init_app.command("agent", epilog=HELP_EPILOG)
def cmd_init_agent(
    ctx: typer.Context,
    agents: Annotated[
        list[str] | None,
        typer.Argument(
            help=(
                "AI agent target(s): 'antigravity', 'claude', 'cursor', 'copilot', "
                "'windsurf', 'cline', 'roo', 'codex', 'gemini', 'all', or 'list'."
            ),
        ),
    ] = None,
    mode: Annotated[
        str,
        typer.Option(
            "-m",
            "--mode",
            help="Trigger mode for frontmatter-capable agents: 'auto' (on-demand) or 'always' (always-on).",
        ),
    ] = "auto",
    global_scope: Annotated[
        bool,
        typer.Option(
            "-g",
            "--global",
            help="Write instruction file(s) to user home global configuration directory.",
        ),
    ] = False,
    detect: Annotated[
        bool,
        typer.Option(
            "--detect",
            help="Auto-detect existing AI agent directories/files in workspace and initialize them.",
        ),
    ] = False,
    list_targets: Annotated[
        bool,
        typer.Option(
            "--list",
            help="List supported AI coding agent targets, output paths, and formats.",
        ),
    ] = False,
    directory: Annotated[
        str,
        typer.Option(
            "-d",
            "--dir",
            help="Target project workspace root directory.",
        ),
    ] = ".",
    output: Annotated[
        str | None,
        typer.Option(
            "-o",
            "--output",
            help="Explicit destination file path (valid only when a single agent is specified).",
        ),
    ] = None,
    force: Annotated[
        bool,
        typer.Option(
            "-f",
            "--force",
            help="Overwrite existing rule file(s) or update existing Drawlib marker blocks.",
        ),
    ] = False,
) -> None:
    """Generate per-agent Drawlib instruction files (.agents/rules/, .claude/rules/, .cursor/rules/, etc.)."""
    _run_init_agent(
        ctx=ctx,
        agents=agents,
        mode=mode,
        global_scope=global_scope,
        detect=detect,
        list_targets=list_targets,
        directory=directory,
        output=output,
        force=force,
    )


@init_app.command("agents", hidden=True, epilog=HELP_EPILOG)
def cmd_init_agents_alias(
    ctx: typer.Context,
    agents: Annotated[list[str] | None, typer.Argument()] = None,
    mode: Annotated[str, typer.Option("-m", "--mode")] = "auto",
    global_scope: Annotated[bool, typer.Option("-g", "--global")] = False,
    detect: Annotated[bool, typer.Option("--detect")] = False,
    list_targets: Annotated[bool, typer.Option("--list")] = False,
    directory: Annotated[str, typer.Option("-d", "--dir")] = ".",
    output: Annotated[str | None, typer.Option("-o", "--output")] = None,
    force: Annotated[bool, typer.Option("-f", "--force")] = False,
) -> None:
    """Plural alias for `drawlib init agent`."""
    _run_init_agent(
        ctx=ctx,
        agents=agents,
        mode=mode,
        global_scope=global_scope,
        detect=detect,
        list_targets=list_targets,
        directory=directory,
        output=output,
        force=force,
    )
