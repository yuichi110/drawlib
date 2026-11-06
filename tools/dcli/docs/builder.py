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
from collections.abc import Sequence
from dataclasses import dataclass

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
        name="logo",
        src_dir="docs_src/logo",
        script_rel_path="docs_src/logo/build.sh",
        description="Drawlib Brand Logo & Favicon Assets (docs/logo/)",
        clean_paths=("docs/logo",),
    ),
    BuildTarget(
        name="ogp",
        src_dir="docs_src/ogp",
        script_rel_path="docs_src/ogp/build.sh",
        description="GitHub Social Preview & OGP Banner Images (docs/ogp_images/)",
        clean_paths=("docs/ogp_images",),
    ),
    BuildTarget(
        name="readme",
        src_dir="docs_src/readme",
        script_rel_path="docs_src/readme/build.sh",
        description="README Asset Images (docs/readme_images/)",
        clean_paths=("docs/readme_images",),
    ),
    BuildTarget(
        name="site",
        src_dir="docs_src/site",
        script_rel_path="docs_src/site/build.sh",
        description="Official Documentation Site (docs/)",
        clean_paths=(
            "docs/en",
            "docs/ja",
            "docs/images",
            "docs/_assets",
            "docs/pypi_images",
            "docs/index.html",
            "docs/404.html",
            "docs/robots.txt",
            "docs/sitemap.xml",
            "docs/llms.txt",
            "docs/.nojekyll",
            "docs/CNAME",
            "docs/README.md",
        ),
    ),
    BuildTarget(
        name="architecture",
        src_dir="docs_src/architecture",
        script_rel_path="docs_src/architecture/build.sh",
        description="Software Architecture Specification Site (docs/architecture/)",
        clean_paths=("docs/architecture",),
    ),
    BuildTarget(
        name="api",
        src_dir="docs_src/api",
        script_rel_path="docs_src/api/build.sh",
        description="Official API & CLI Reference Site (docs/api/)",
        clean_paths=("docs/api",),
    ),
    BuildTarget(
        name="reports",
        src_dir="reports/full_audit_src",
        script_rel_path="reports/full_audit_src/build.sh",
        description="PNI501 Full Audit Report (docs/reports/pni-full-audit/)",
        clean_paths=("docs/reports/pni-full-audit",),
    ),
)

TARGET_MAP: dict[str, BuildTarget] = {target.name: target for target in ALL_TARGETS}
# Convenience aliases
TARGET_MAP["docs"] = TARGET_MAP["site"]
TARGET_MAP["doc"] = TARGET_MAP["site"]
TARGET_MAP["report"] = TARGET_MAP["reports"]


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
    result = subprocess.run(["bash", str(script_path)], cwd=str(PROJECT_ROOT), check=False)
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
        target_name: Specific target name ('site', 'api', 'architecture', 'readme', 'logo', 'ogp', or 'all').
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
