# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Helper script for getting latest drawlib version which includes pre-release."""

import importlib.util
import json
import re
import urllib.request
from typing import List, Tuple

from tools.dcli.common import PROJECT_ROOT

LIB_NAME = "drawlib"
INIT_PATH = str(PROJECT_ROOT / "src" / "drawlib" / "__init__.py")
PYPI_JSON_URL_TEMPLATE = "https://pypi.org/pypi/{package_name}/json"
TEST_PYPI_JSON_URL_TEMPLATE = "https://test.pypi.org/pypi/{package_name}/json"


def get_latest_version(package_name: str, test_pypi: bool = False) -> str:
    """Fetches the latest version of a package from PyPI, including pre-releases."""
    versions = list_versions(package_name, test_pypi=test_pypi)
    if not versions:
        raise ValueError(f"No versions found for package '{package_name}'")
    return versions[0]


def list_versions(package_name: str, test_pypi: bool = False) -> List[str]:
    """Fetches all versions of a package from PyPI, sorted newest to oldest."""
    if test_pypi:
        url = TEST_PYPI_JSON_URL_TEMPLATE.format(package_name=package_name)
    else:
        url = PYPI_JSON_URL_TEMPLATE.format(package_name=package_name)

    try:
        with urllib.request.urlopen(url) as response:  # noqa: S310
            if response.status != 200:
                raise RuntimeError(f"PyPI returned status code: {response.status}")

            data = json.load(response)
            all_versions = data["releases"].keys()
            sorted_versions = sorted(all_versions, key=_parse_version, reverse=True)
            return sorted_versions

    except Exception as e:
        raise RuntimeError(f"Failed to fetch versions for package '{package_name}': {e}") from e


def check_new_version_ok(latest_version: str, new_version: str, allow_jump: bool = False) -> None:
    """Compare PyPI latest version and new_version."""
    if _parse_version(new_version) <= _parse_version(latest_version):
        raise ValueError(f"New version {new_version} must be greater than latest version {latest_version}.")

    latest_parts = tuple(int(part) if part.isdigit() else part for part in latest_version.split("."))
    new_parts = tuple(int(part) if part.isdigit() else part for part in new_version.split("."))

    if latest_parts[0] != new_parts[0]:
        _check_new_major_version_ok(latest_parts, new_parts, latest_version, new_version, allow_jump)

    elif latest_parts[1] != new_parts[1]:
        _check_new_minor_version_ok(latest_parts, new_parts, latest_version, new_version, allow_jump)

    elif latest_parts[2] != new_parts[2]:
        _check_new_patch_version_ok(latest_parts, new_parts, latest_version, new_version, allow_jump)

    else:
        _check_new_prerelease_version_ok(latest_parts, new_parts, latest_version, new_version, allow_jump)


#
# Private of get_latest_version()
#


def _parse_version(version: str) -> Tuple[int, int, int, str]:
    """Parses a version string into a tuple of integers for comparison."""
    parts = version.split(".")
    parts_list = list(int(part) if part.isdigit() else part for part in parts)
    if len(parts_list) == 3:
        # make "1.2.3" is newer rather than "1.2.3.dev1" and "1.2.3.rc1".
        parts_list.append("zzz")
    return tuple(parts_list)  # type: ignore


#
# Private of check_new_version_ok()
#


def _handle_jump(message: str, latest_version: str, new_version: str, allow_jump: bool) -> None:
    if allow_jump:
        return

    raise ValueError(
        f"Version jump detected: {message} (Current latest: {latest_version}, New version: {new_version}). "
        "Use --allow-jump if you want to skip version."
    )


def get_new_version() -> str:
    """Retrieve current library version from src/drawlib/__init__.py."""
    spec = importlib.util.spec_from_file_location("init", INIT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module from {INIT_PATH}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module.LIB_VERSION


_get_new_version = get_new_version


def _check_new_major_version_ok(
    latest_parts: Tuple, new_parts: Tuple, latest_version: str, new_version: str, allow_jump: bool
) -> None:
    """A"""
    if (latest_parts[0] + 1) != new_parts[0]:
        _handle_jump("New major version is not current +1.", latest_version, new_version, allow_jump)

    if new_parts[1] != 0:
        raise ValueError("Minor version must be 0 when having new major version.")

    if new_parts[2] != 0:
        raise ValueError("Patch version must be 0 when having new major version.")

    if len(new_parts) == 3:
        raise ValueError("Requires pre-release version when having new major version.")

    patch_version: str = new_parts[3]
    if patch_version not in {"dev1", "rc1"}:
        raise ValueError('Pre-release version must be "dev1" or "rc1" when having new major version.')


def _check_new_minor_version_ok(
    latest_parts: Tuple, new_parts: Tuple, latest_version: str, new_version: str, allow_jump: bool
) -> None:
    """A"""
    if (latest_parts[1] + 1) != new_parts[1]:
        _handle_jump("New minor version is not current +1.", latest_version, new_version, allow_jump)

    if new_parts[2] != 0:
        raise ValueError("Patch version must be 0 when having new minor version.")

    if len(new_parts) == 3:
        raise ValueError("Requires pre-release version when having new minor version.")

    patch_version: str = new_parts[3]
    if patch_version not in {"dev1", "rc1"}:
        raise ValueError('Pre-release version must be "dev1" or "rc1" when having new minor version.')


def _check_new_patch_version_ok(
    latest_parts: Tuple, new_parts: Tuple, latest_version: str, new_version: str, allow_jump: bool
) -> None:
    """A"""
    if (latest_parts[2] + 1) != new_parts[2]:
        _handle_jump("New patch version is not current +1.", latest_version, new_version, allow_jump)

    if len(new_parts) == 3:
        # patch version doesn't requires dev1 and rc1
        return

    patch_version: str = new_parts[3]
    if patch_version not in {"dev1", "rc1"}:
        raise ValueError(
            'Pre-release version is not mandatory when having new patch version. But it should be "dev1" or "rc1".'
        )


def _get_dev_value(text: str) -> int:
    matches = re.findall(r"dev(\d+)", text)
    values = [int(match) for match in matches]
    if not values:
        return -1
    return values[0]


def _get_rc_value(text: str) -> int:
    matches = re.findall(r"rc(\d+)", text)
    values = [int(match) for match in matches]
    if not values:
        return -1
    return values[0]


def _check_new_prerelease_version_ok(
    latest_parts: Tuple, new_parts: Tuple, latest_version: str, new_version: str, allow_jump: bool
) -> None:
    """Check if the transition from one pre-release version to another is valid."""
    if len(latest_parts) == 3:
        if len(new_parts) == 3:
            _handle_jump("New patch version is not current +1.", latest_version, new_version, allow_jump)
            return

        raise ValueError(
            "New patch release version l.m.n.X can't be released after standard version l.m.n was released.",
        )

    if len(new_parts) == 3:
        # standard release version (l.m.n) can be released after pre-release version (l.m.n.X)
        return

    latest_pre: str = latest_parts[3]
    new_pre: str = new_parts[3]
    latest_dev_value = _get_dev_value(latest_pre)
    latest_rc_value = _get_rc_value(latest_pre)
    new_dev_value = _get_dev_value(new_pre)
    new_rc_value = _get_rc_value(new_pre)

    if latest_dev_value != -1:
        _check_dev_transition(latest_dev_value, new_dev_value, new_rc_value, latest_version, new_version, allow_jump)
    elif latest_rc_value != -1:
        _check_rc_transition(latest_rc_value, new_rc_value, latest_version, new_version, allow_jump)
    else:
        raise ValueError(f'Something went wrong. Current "{latest_parts}", New "{new_parts}".')


def _check_dev_transition(
    latest_dev: int, new_dev: int, new_rc: int, latest_version: str, new_version: str, allow_jump: bool
) -> None:
    if (latest_dev + 1) == new_dev:
        return
    if new_rc == 1:
        return

    _handle_jump(
        f"next pre-release version should be dev{latest_dev + 1} or rc1 or standard version.",
        latest_version,
        new_version,
        allow_jump,
    )


def _check_rc_transition(
    latest_rc: int,
    new_rc: int,
    latest_version: str,
    new_version: str,
    allow_jump: bool,
) -> None:
    if (latest_rc + 1) == new_rc:
        return

    _handle_jump(
        f"next pre-release version should be rc{latest_rc + 1} or standard version.",
        latest_version,
        new_version,
        allow_jump,
    )
