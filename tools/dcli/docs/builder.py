# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Build engine for compiling documentation, slides, and project illustrations."""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from tools.dcli.common import PROJECT_ROOT, console, err_console


@dataclass(frozen=True)
class BuildTarget:
    """Definition of a documentation build target."""

    name: str
    src_dir: str
    script_rel_path: str
    description: str
    clean_paths: tuple[str, ...]


ALL_TARGETS: tuple[BuildTarget, ...] = (
    BuildTarget(
        name="site",
        src_dir="docs/docs_src",
        script_rel_path="docs/docs_src/build.sh",
        description="Documentation Site (docs/docs_markdown & docs/docs_html)",
        clean_paths=("docs/docs_markdown", "docs/docs_html", "docs/docs_images"),
    ),
    BuildTarget(
        name="quickstart",
        src_dir="docs/quickstart_src",
        script_rel_path="docs/quickstart_src/build.sh",
        description="Quickstart Document & PDF",
        clean_paths=(
            "docs/quickstart_markdown",
            "docs/quickstart_html",
            "docs/quickstart.pdf",
            "docs/quickstart_images",
        ),
    ),
    BuildTarget(
        name="readme",
        src_dir="docs/readme_src",
        script_rel_path="docs/readme_src/build.sh",
        description="README Asset Images",
        clean_paths=("docs/readme_images",),
    ),
    BuildTarget(
        name="dogfooding",
        src_dir="docs/drawlib-dogfooding_src",
        script_rel_path="docs/drawlib-dogfooding_src/build.sh",
        description="Dogfooding Document (JP)",
        clean_paths=(
            "docs/drawlib-dogfooding_markdown",
            "docs/drawlib-dogfooding_html",
            "docs/drawlib-dogfooding.pdf",
            "docs/drawlib-dogfooding_images",
        ),
    ),
    BuildTarget(
        name="dogfooding-en",
        src_dir="docs/drawlib-dogfooding-en_src",
        script_rel_path="docs/drawlib-dogfooding-en_src/build.sh",
        description="Dogfooding Document (EN)",
        clean_paths=(
            "docs/drawlib-dogfooding-en_markdown",
            "docs/drawlib-dogfooding-en_html",
            "docs/drawlib-dogfooding-en.pdf",
            "docs/drawlib-dogfooding-en_images",
        ),
    ),
    BuildTarget(
        name="slide",
        src_dir="docs/slide_about_drawlib_src",
        script_rel_path="docs/slide_about_drawlib_src/build.sh",
        description="16:9 Presentation Slide Deck (About Drawlib)",
        clean_paths=(
            "docs/slide_about_drawlib_html",
            "docs/slide_about_drawlib.pdf",
            "docs/slide_about_drawlib_images",
        ),
    ),
)

TARGET_MAP: dict[str, BuildTarget] = {
    target.name: target for target in ALL_TARGETS
}
# Convenience aliases
TARGET_MAP["docs"] = TARGET_MAP["site"]
TARGET_MAP["doc"] = TARGET_MAP["site"]
TARGET_MAP["slide_about_drawlib"] = TARGET_MAP["slide"]
TARGET_MAP["slide-about-drawlib"] = TARGET_MAP["slide"]


def clean_target_artifacts(targets: Sequence[BuildTarget]) -> None:
    """Remove build output directories and files for specified targets.

    Args:
        targets: Sequence of build targets to clean.
    """
    for target in targets:
        for clean_rel in target.clean_paths:
            path = PROJECT_ROOT / clean_rel
            if path.is_dir():
                shutil.rmtree(path)
            elif path.is_file():
                path.unlink()


def run_target_build(target: BuildTarget) -> None:
    """Execute the build script for a specific documentation target.

    Args:
        target: The BuildTarget to compile.
    """
    script_path = PROJECT_ROOT / target.script_rel_path
    if not script_path.exists():
        console.print(f"[yellow]Target source script '{target.script_rel_path}' not found, skipping.[/yellow]")
        return

    console.print(f"[bold cyan]=== Building {target.description} ({target.script_rel_path}) ===[/bold cyan]")
    result = subprocess.run(["bash", str(script_path)], cwd=str(PROJECT_ROOT))
    if result.returncode != 0:
        err_console.print(f"[bold red]Build failed for {target.name} with return code {result.returncode}[/bold red]")
        raise RuntimeError(f"Build failed for {target.name}")


def build_docs(
    target_name: str | None = None,
    build_all: bool = False,
    clean: bool = True,
) -> None:
    """Build specified documentation targets or all targets.

    Args:
        target_name: Specific target name ('site', 'quickstart', 'readme', 'dogfooding', 'dogfooding-en', 'slide').
        build_all: If True, build all available targets in sequence.
        clean: If True, remove previous build artifacts before building.
    """
    if build_all or target_name in ("all", "*"):
        targets_to_build: list[BuildTarget] = [t for t in ALL_TARGETS if (PROJECT_ROOT / t.src_dir).exists()]
    elif target_name:
        if target_name not in TARGET_MAP:
            valid_names = ", ".join(sorted(TARGET_MAP.keys()) + ["all"])
            raise ValueError(f"Unknown target '{target_name}'. Valid targets: {valid_names}")
        targets_to_build = [TARGET_MAP[target_name]]
    else:
        # Default: build main documentation site (docs_src)
        targets_to_build = [TARGET_MAP["site"]]

    if clean:
        console.print("[dim]Cleaning target artifacts...[/dim]")
        clean_target_artifacts(targets_to_build)

    for target in targets_to_build:
        run_target_build(target)
        console.print()

    console.print("[bold green]All builds completed successfully![/bold green]")
