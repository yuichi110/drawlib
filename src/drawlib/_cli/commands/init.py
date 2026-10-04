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
from typing import Annotated, Optional

import typer

from drawlib._cli._help import HELP_EPILOG
from drawlib._templates import (
    init_project,
    list_project_types,
    resolve_project_paths,
)

_HELP_CTX = {"help_option_names": ["-h", "--help"]}

init_app = typer.Typer(
    name="init",
    help="Scaffold starter drawlib projects with sample illustrations and build scripts.",
    epilog=HELP_EPILOG,
    no_args_is_help=True,
    context_settings=_HELP_CTX,
)


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

    print(f"Initialized '{project_type}' project ('{paths.src_dir_name}/')\n")
    print("Project files created:")
    for file_path in created:
        try:
            rel = file_path.relative_to(cwd)
            print(f"  - {rel}")
        except ValueError:
            print(f"  - {file_path}")

    print("\nNext steps:")
    print(f"  ./{paths.src_dir_name}/build.sh")

    if project_type in {"site", "doc", "slide"}:
        print(f"  ./{paths.src_dir_name}/serve.sh")


def _run_init(
    project_type: str,
    target: str,
    style: Optional[str] = None,
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


@init_app.command("doc", epilog=HELP_EPILOG)
def cmd_init_doc(
    target: Annotated[
        str,
        typer.Argument(
            help="Base name for the document and source folder (creates '<target>_src/').",
        ),
    ] = "doc",
    style: Annotated[
        Optional[str],
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
    """Scaffold a linear document project (HTML, PDF, Markdown) in the current directory."""
    _run_init(project_type="doc", target=target, style=style, lang=lang, force=force)


@init_app.command("site", epilog=HELP_EPILOG)
def cmd_init_site(
    target: Annotated[
        str,
        typer.Argument(
            help="Base name for the documentation site and source folder (creates '<target>_src/').",
        ),
    ] = "docs",
    style: Annotated[
        Optional[str],
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
    """Scaffold a multi-page documentation website with sidebar navigation in current directory."""
    _run_init(project_type="site", target=target, style=style, lang=lang, force=force)


@init_app.command("slide", epilog=HELP_EPILOG)
def cmd_init_slide(
    target: Annotated[
        str,
        typer.Argument(
            help="Base name for the presentation deck and source folder (creates '<target>_src/').",
        ),
    ] = "slide",
    style: Annotated[
        Optional[str],
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
    """Scaffold a 16:9 presentation slide deck (HTML & PDF) in current directory."""
    _run_init(project_type="slide", target=target, style=style, lang=lang, force=force)


@init_app.command("images", epilog=HELP_EPILOG)
def cmd_init_images(
    target: Annotated[
        str,
        typer.Argument(
            help="Base name for the illustrations repository and source folder (creates '<target>_src/').",
        ),
    ] = "images",
    style: Annotated[
        Optional[str],
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


@init_app.command("image", hidden=True, epilog=HELP_EPILOG)
def cmd_init_image_alias(
    target: Annotated[
        str,
        typer.Argument(
            help="Legacy alias for 'images'.",
        ),
    ] = "images",
    style: Annotated[Optional[str], typer.Option("-s", "--style")] = None,
    lang: Annotated[str, typer.Option("-l", "--lang")] = "en",
    force: Annotated[bool, typer.Option("-f", "--force")] = False,
) -> None:
    """Backward compatibility alias for `drawlib init images`."""
    _run_init(project_type="images", target=target, style=style, lang=lang, force=force)


@init_app.command("list", epilog=HELP_EPILOG)
def cmd_init_list() -> None:
    """List available project types and descriptions."""
    types = list_project_types()
    print("Available Drawlib Project Types:\n")
    max_len = max(len(t) for t in types)
    for name, desc in types.items():
        print(f"  - {name:<{max_len}} : {desc}")
    print("\nUsage:\n  drawlib init <type> [target]")
