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

from drawlib._builder.project_init import init_project, list_project_types


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


def _resolve_base_name(output: Optional[str], selected_type: str) -> str:
    """Resolve base project/artifact name without _src suffix."""
    if output and output.strip():
        name = output.strip().rstrip("/\\")
        return name[:-4] if name.endswith("_src") else name
    return "images" if selected_type == "image" else "docs"


def _print_build_summary(selected_type: str, out_dir: str, out_html: str, out_pdf: str) -> None:
    """Print completed initial build artifacts."""
    print("\nInitial build completed:")
    if selected_type in {"site", "simple"}:
        print(f"  - Markdown: {out_dir}/")
        print(f"  - HTML:     {out_html}/")
    elif selected_type == "pdf":
        print(f"  - PDF report: {out_pdf}")
    elif selected_type == "image":
        print(f"  - Images: {out_dir}/")


def _print_init_success(
    selected_type: str,
    dest_str: str,
    created: list[Path],
    dest_path: Path,
    output: Optional[str] = None,
    here: bool = False,
    no_build: bool = False,
) -> None:
    """Print initialization success message and next steps.

    Args:
        selected_type: Initialized project type.
        dest_str: Target destination string.
        created: List of created file paths.
        dest_path: Destination path object.
        output: Custom output name or None.
        here: If True, deployed directly into destination.
        no_build: If True, initial build was skipped.
    """
    resolved_dest = dest_path.resolve()
    rel_display = dest_str if dest_str != "." else "."

    base_name = _resolve_base_name(output, selected_type)
    src_dir = "." if here else f"{base_name}_src"
    out_dir = base_name
    out_html = f"{base_name}_html"
    out_pdf = f"{base_name}.pdf"

    print(f"Initialized '{selected_type}' project in {rel_display}\n")
    print("Project files created:")
    for file_path in created:
        try:
            rel = file_path.relative_to(resolved_dest)
            print(f"  - {rel}")
        except ValueError:
            print(f"  - {file_path}")

    if not no_build:
        _print_build_summary(selected_type, out_dir, out_html, out_pdf)

    print("\nNext steps:")
    if dest_str != ".":
        print(f"  cd {dest_str}")

    if selected_type == "site" and not no_build:
        print(f"  drawlib serve {out_html}/")

    if here:
        print("  ./build.sh")
    else:
        print(f"  ./{src_dir}/build.sh")


def cmd_init(
    project_type: Annotated[
        Optional[str],
        typer.Argument(
            metavar="TYPE",
            help="Starter project type ('site', 'simple', 'pdf', 'image').",
        ),
    ] = None,
    destination: Annotated[
        Optional[str],
        typer.Argument(
            metavar="[DESTINATION]",
            help="Target directory path (defaults to current directory).",
        ),
    ] = None,
    output: Annotated[
        Optional[str],
        typer.Option(
            "-o",
            "--output",
            help="Output project/artifact name (source folder will be <name>_src).",
        ),
    ] = None,
    here: Annotated[
        bool,
        typer.Option(
            "--here",
            help="Initialize directly into the current directory.",
        ),
    ] = False,
    no_build: Annotated[
        bool,
        typer.Option(
            "--no-build",
            help="Skip running the initial build after scaffolding.",
        ),
    ] = False,
    lang: Annotated[
        str,
        typer.Option(
            "--lang",
            help="Language for starter templates and font config ('en' or 'ja').",
        ),
    ] = "en",
    css: Annotated[
        Optional[str],
        typer.Option(
            "--css",
            help="CSS preset theme ('default', 'google', 'github', 'minimal', 'monochrome', etc.) or file path.",
        ),
    ] = None,
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
            help="Overwrite existing files and output directories.",
        ),
    ] = False,
) -> None:
    """Scaffold a starter drawlib project with sample illustrations and build script.

    Args:
        project_type: Starter project type ('site', 'simple', 'pdf', 'image').
        destination: Target directory path (defaults to current directory).
        output: Output project/artifact name.
        here: If True, initialize directly into current directory.
        no_build: If True, skip running initial build.
        lang: Starter template language ('en' or 'ja').
        css: CSS theme preset name or custom stylesheet file path.
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
            output=output,
            force=force,
            here=here,
            no_build=no_build,
            lang=lang,
            css=css,
        )
    except FileExistsError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise typer.Exit(code=1) from exc
    except Exception as exc:
        print(f"Error: Failed to initialize project: {exc}", file=sys.stderr)
        raise typer.Exit(code=1) from exc

    _print_init_success(
        selected_type=selected_type,
        dest_str=dest_str,
        created=created,
        dest_path=dest_path,
        output=output,
        here=here,
        no_build=no_build,
    )
