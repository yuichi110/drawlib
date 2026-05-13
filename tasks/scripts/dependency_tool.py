# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Dependency management tool for drawlib."""

import argparse
import json
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime
from typing import Literal

import tomlkit
from utils import cd_to_project_root

PYPROJECT_TOML_PATH = "pyproject.toml"


@dataclass
class Args:
    """Command line arguments for the dependency tool."""

    command: Literal["list", "releases"]
    package: str | None = None
    format: Literal["text", "json"] = "text"
    year_from: int | None = None
    year_to: int | None = None


@dataclass
class DependencyInfo:
    """Information about a package dependency."""

    name: str
    version_specifier: str


@dataclass
class ReleaseInfo:
    """Information about a package release version."""

    version: str
    timestamps: datetime


def main() -> None:
    """Main function for the dependency management tool."""
    cd_to_project_root()
    parser = get_parser()
    args = get_args(parser)

    if args.command == "list":
        dependencies = get_dependencies()
        list_dependencies(dependencies)
        return

    if args.command == "releases":
        if args.package is None:
            parser.print_help()
            sys.exit(1)
        releases = get_releases(args.package, args.year_from, args.year_to)
        list_releases(releases, args.format)
        return

    parser.print_help()
    sys.exit(1)


def get_parser() -> argparse.ArgumentParser:
    """Create and return the argument parser for the dependency tool."""
    parser = argparse.ArgumentParser(description="Dependency management tool for drawlib")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # 'list' command configuration
    subparsers.add_parser("list", help="List all dependencies in pyproject.toml")

    # 'releases' command configuration
    releases_parser = subparsers.add_parser("releases", help="List available releases for a package")
    releases_parser.add_argument("package", help="Package name to check releases for")
    releases_parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )
    releases_parser.add_argument(
        "--from",
        type=int,
        default=None,
        help="Start year to filter releases (inclusive)",
    )
    releases_parser.add_argument(
        "--to",
        type=int,
        default=None,
        help="End year to filter releases (inclusive)",
    )

    return parser


def get_args(parser: argparse.ArgumentParser) -> Args:
    """Parse and return the command line arguments."""
    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        sys.exit(1)

    return Args(
        command=args.command,
        package=getattr(args, "package", None),
        format=getattr(args, "format", "text"),
        year_from=getattr(args, "from", None),
        year_to=getattr(args, "to", None),
    )


def get_dependencies() -> list[DependencyInfo]:
    """Retrieve the list of dependencies from pyproject.toml."""
    with open(PYPROJECT_TOML_PATH, mode="r", encoding="utf8") as fin:
        doc = tomlkit.parse(fin.read())

    # Extract dependencies from the [project] section.
    # Returns an empty list if the section or key is missing.
    deps_version = doc.get("project", {}).get("dependencies", [])
    deps = []
    for dep in deps_version:
        name = dep.split(">")[0].split("<")[0].split("=")[0].split("!")[0].strip()
        deps.append(DependencyInfo(name=name, version_specifier=dep))
    return deps


def list_dependencies(dependencies: list[DependencyInfo]) -> None:
    """Print a cleaned list of dependency package names."""
    for dep in dependencies:
        print(dep.name)


def get_releases(package_name: str, year_from: int | None, year_to: int | None) -> list[ReleaseInfo]:
    """Fetch release information for a package from PyPI."""
    url = f"https://pypi.org/pypi/{package_name}/json"

    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req) as response:  # noqa: S310
            data = json.load(response)
            versions = []
            for version, release_files in data["releases"].items():
                if not release_files:
                    continue

                # Take the upload time from the first file in the release.
                # PyPI returns a list of files (wheels, source) for each version.
                r = ReleaseInfo(
                    version=version,
                    timestamps=datetime.fromisoformat(release_files[0]["upload_time_iso_8601"].replace("Z", "+00:00")),
                )

                # Filter by year range if specified
                if year_from and r.timestamps.year < year_from:
                    continue
                if year_to and r.timestamps.year > year_to:
                    continue

                versions.append(r)

            # Sort versions by timestamp in descending order
            versions.sort(key=lambda x: x.timestamps, reverse=True)
            return versions

    except urllib.error.HTTPError as e:
        print(f"Error fetching versions for {package_name}: {e}")
        sys.exit(1)

    except json.JSONDecodeError:
        print(f"Error decoding JSON response from PyPI for {package_name}")
        sys.exit(1)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


def list_releases(releases: list[ReleaseInfo], format: str = "text") -> None:
    """Print the list of releases in the specified format."""
    if format == "json":
        print(
            json.dumps(
                [{"version": r.version, "timestamps": r.timestamps.isoformat()} for r in releases],
                indent=2,
            )
        )
    else:
        print("\n".join([r.version for r in releases]))


if __name__ == "__main__":
    main()
