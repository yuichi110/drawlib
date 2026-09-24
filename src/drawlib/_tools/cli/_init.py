# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Typer command for `drawlib init` project scaffolding."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Annotated, Optional

import typer

from drawlib._tools.project_init import init_project, list_project_types


def _print_types_list(types: dict[str, str]) -> None:
    """Print the formatted list of available project types."""
    print("Available Drawlib Project Types:\n")
    max_len = max(len(t) for t in types)
    for name, desc in types.items():
        print(f"  - {name:<{max_len}} : {desc}")
    print("\nUsage:\n  drawlib init <type> [destination]\n  drawlib init <type> --here")


def _validate_type_or_exit(project_type: Optional[str], types: dict[str, str]) -> str:
    """Validate project type argument or print helpful error and exit.

    Args:
        project_type: Input project type name.
        types: Mapping of valid project type names to descriptions.

    Returns:
        str: Normalized lowercase project type.

    Raises:
        typer.Exit: If project_type is missing or not in types.
    """
    if project_type is None:
        print("Error: Missing project type.\n", file=sys.stderr)
    else:
        selected_type = project_type.strip().lower()
        if selected_type in types:
            return selected_type
        print(f"Error: Unknown project type '{project_type}'.\n", file=sys.stderr)

    print("Available types:", file=sys.stderr)
    for name, desc in types.items():
        print(f"  - {name:<10}: {desc}", file=sys.stderr)
    print("\nRun `drawlib init --list` to view descriptions.", file=sys.stderr)
    raise typer.Exit(code=1)


def _print_init_success(
    selected_type: str,
    dest_str: str,
    created: list[Path],
    dest_path: Path,
) -> None:
    """Print initialization success message and next steps.

    Args:
        selected_type: Initialized project type.
        dest_str: Target destination string.
        created: List of created file paths.
        dest_path: Destination path object.
    """
    resolved_dest = dest_path.resolve()
    rel_display = dest_str if dest_str != "." else "."

    print(f"Initialized '{selected_type}' project in {rel_display}\n")
    print("Project files created:")
    for file_path in created:
        try:
            rel = file_path.relative_to(resolved_dest)
            print(f"  - {rel}")
        except ValueError:
            print(f"  - {file_path}")

    print("\nNext steps:")
    if dest_str != ".":
        print(f"  cd {dest_str}")
    print("  ./docs_build.sh")
    if selected_type == "site":
        print("  drawlib serve docs_html/")


def cmd_init(
    project_type: Annotated[
        Optional[str],
        typer.Argument(
            metavar="TYPE",
            help="Starter project type ('simple', 'site', 'pdf').",
        ),
    ] = None,
    destination: Annotated[
        Optional[str],
        typer.Argument(
            metavar="[DESTINATION]",
            help="Target directory path (defaults to current directory).",
        ),
    ] = None,
    here: Annotated[
        bool,
        typer.Option(
            "--here",
            help="Initialize directly into the current directory.",
        ),
    ] = False,
    list_types: Annotated[
        bool,
        typer.Option(
            "-l",
            "--list",
            help="List all available starter project types and exit.",
        ),
    ] = False,
    force: Annotated[
        bool,
        typer.Option(
            "-f",
            "--force",
            help="Overwrite existing files in destination directory.",
        ),
    ] = False,
) -> None:
    """Scaffold a starter drawlib project with sample illustrations and build script.

    Args:
        project_type: Starter project type ('simple', 'site', 'pdf').
        destination: Target directory path (defaults to current directory).
        here: If True, initialize directly into current directory.
        list_types: If True, list available project types and exit.
        force: If True, overwrite existing files in destination directory.
    """
    types = list_project_types()
    if list_types:
        _print_types_list(types)
        return

    selected_type = _validate_type_or_exit(project_type, types)

    if here and destination is not None and destination != ".":
        print("Error: Cannot specify both [DESTINATION] and --here.", file=sys.stderr)
        raise typer.Exit(code=1)

    dest_str = "." if here else (destination if destination is not None else ".")
    dest_path = Path(dest_str)

    try:
        created = init_project(
            project_type=selected_type,
            destination=dest_path,
            force=force,
            here=here,
        )
    except FileExistsError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise typer.Exit(code=1) from exc
    except Exception as exc:
        print(f"Error: Failed to initialize project: {exc}", file=sys.stderr)
        raise typer.Exit(code=1) from exc

    _print_init_success(selected_type, dest_str, created, dest_path)
