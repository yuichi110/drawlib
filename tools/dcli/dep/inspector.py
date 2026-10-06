# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Dependency inspection and release tracking utilities."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import tomlkit

from tools.dcli.common import PROJECT_ROOT

PYPROJECT_TOML_PATH = PROJECT_ROOT / "pyproject.toml"


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


def get_dependencies(pyproject_path: Path = PYPROJECT_TOML_PATH) -> list[DependencyInfo]:
    """Retrieve the list of dependencies from pyproject.toml."""
    content = pyproject_path.read_text(encoding="utf-8")
    doc = tomlkit.parse(content)

    deps_version = doc.get("project", {}).get("dependencies", [])
    deps: list[DependencyInfo] = []
    for dep in deps_version:
        name = dep.split(">")[0].split("<")[0].split("=")[0].split("!")[0].strip()
        deps.append(DependencyInfo(name=name, version_specifier=dep))
    return deps


def get_releases(package_name: str, year_from: int | None = None, year_to: int | None = None) -> list[ReleaseInfo]:
    """Fetch release information for a package from PyPI."""
    url = f"https://pypi.org/pypi/{package_name}/json"
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (compatible; drawlib-dep-tool/1.0)",
        },
    )

    try:
        with urllib.request.urlopen(req) as response:  # noqa: S310
            data = json.load(response)
            versions: list[ReleaseInfo] = []
            for version, release_files in data.get("releases", {}).items():
                if not release_files:
                    continue

                r = ReleaseInfo(
                    version=version,
                    timestamps=datetime.fromisoformat(release_files[0]["upload_time_iso_8601"].replace("Z", "+00:00")),
                )

                if year_from is not None and r.timestamps.year < year_from:
                    continue
                if year_to is not None and r.timestamps.year > year_to:
                    continue

                versions.append(r)

            versions.sort(key=lambda x: x.timestamps, reverse=True)
            return versions

    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Error fetching versions for {package_name}: {e}") from e
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Error decoding JSON response from PyPI for {package_name}") from e
