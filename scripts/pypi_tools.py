# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
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
import os
import re
import sys
import urllib.request
from typing import Tuple


def main():
    """A"""
    cd_to_project_root()
    if len(sys.argv) != 2:
        print('Requires only one argument. "--get_latest_version" or "--check_new_version_ok".')
        sys.exit(1)

    command = sys.argv[1]
    if command == "--get_latest_version":
        print(get_latest_version("drawlib"))

    elif command == "--check_new_version_ok":
        latest_version = get_latest_version("drawlib")
        new_version = _get_new_version()
        try:
            check_new_version_ok(latest_version, new_version)
            print("Check success.")
        except Exception as e:
            print(f"Check failed. {e}")
            sys.exit(1)

    else:
        print("Argument not supported.")
        print('Requires only one argument. "--get_latest_version" or "--check_new_version_ok".')
        sys.exit(1)


def cd_to_project_root():
    """Change directory to project root."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    os.chdir("../")


def get_latest_version(package_name: str) -> str:
    """Fetches the latest version of a package from PyPI, including pre-releases.

    Latest rule follows PEP 440 Compliance.
    In Summary,
    1. sort by major.minor.patch
    2. rc release > dev release > normal release

    Args:
        package_name (str): The name of the package for which to fetch the latest version.

    Returns:
        str: The latest version of the package, including pre-releases, if successful.

    """
    url = f"https://pypi.org/pypi/{package_name}/json"

    try:
        with urllib.request.urlopen(url) as response:
            if response.status != 200:
                raise Exception(f"PyPI returns status code: {response.status}")

            data = json.load(response)
            all_versions = data["releases"].keys()
            latest_version = max(all_versions, key=_parse_version)
            return latest_version

    except Exception as e:
        print(f"Failed to fetch the latest version for package {package_name}")
        print(f"Error: {e}")
        sys.exit(1)


def check_new_version_ok(latest_version: str, new_version: str) -> None:
    """Compare PyPI latest version and new_version."""
    latest_parts = tuple(int(part) if part.isdigit() else part for part in latest_version.split("."))
    new_parts = tuple(int(part) if part.isdigit() else part for part in new_version.split("."))

    if latest_parts[0] != new_parts[0]:
        _check_new_major_version_ok(latest_parts, new_parts)

    elif latest_parts[1] != new_parts[1]:
        _check_new_minor_version_ok(latest_parts, new_parts)

    elif latest_parts[2] != new_parts[2]:
        _check_new_patch_version_ok(latest_parts, new_parts)

    else:
        _check_new_prerelease_version_ok(latest_parts, new_parts)


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


def _test_parse_version() -> None:
    """Test parse_version()"""
    versions = [
        "0.2.0.dev1",
        "0.2.0.dev2",
        "0.2.1.rc1",
        "0.2.1.rc2",
        "0.2.1",
        "0.2.2",
        "0.2.2.rc1",
        "0.2.2.rc2",
    ]

    sorted_versions = sorted(versions, key=_parse_version)
    print(sorted_versions)


#
# Private of check_new_version_ok()
#


def _get_new_version() -> str:
    spec = importlib.util.spec_from_file_location("init", "drawlib/__init__.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load module")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module.LIB_VERSION


def _check_new_major_version_ok(latest_parts: Tuple, new_parts: Tuple):
    """A"""
    if (latest_parts[0] + 1) != new_parts[0]:
        raise ValueError("New major version must be current +1.")

    if new_parts[1] != 0:
        raise ValueError("Minor version must be 0 when having new major version.")

    if new_parts[2] != 0:
        raise ValueError("Patch version must be 0 when having new major version.")

    if len(new_parts) == 3:
        raise ValueError("Requires pre-release version when having new major version.")

    patch_version: str = new_parts[3]
    if patch_version not in {"dev1", "rc1"}:
        raise ValueError('Pre-release version must be "dev1" or "rc1" when having new major version.')


def _check_new_minor_version_ok(latest_parts: Tuple, new_parts: Tuple):
    """A"""
    if (latest_parts[1] + 1) != new_parts[1]:
        raise ValueError("New minor version must be current +1.")

    if new_parts[2] != 0:
        raise ValueError("Patch version must be 0 when having new minor version.")

    if len(new_parts) == 3:
        raise ValueError("Requires pre-release version when having new minor version.")

    patch_version: str = new_parts[3]
    if patch_version not in {"dev1", "rc1"}:
        raise ValueError('Pre-release version must be "dev1" or "rc1" when having new minor version.')


def _check_new_patch_version_ok(latest_parts: Tuple, new_parts: Tuple):
    """A"""
    if (latest_parts[2] + 1) != new_parts[2]:
        raise ValueError("New patch version must be current +1.")

    if len(new_parts) == 3:
        # patch version doesn't requires dev1 and rc1
        return

    patch_version: str = new_parts[3]
    if patch_version not in {"dev1", "rc1"}:
        raise ValueError(
            'Pre-release version is not mandatory when having new patch version. But it should be "dev1" or "rc1".'
        )


def _check_new_prerelease_version_ok(latest_parts: Tuple, new_parts: Tuple):  # noqa: C901
    """A"""
    if len(latest_parts) == 3:
        if len(new_parts) == 3:
            raise ValueError("New patch version must be current +1.")

        raise ValueError(
            "New patch release version l.m.n.X can't be released after standard version l.m.n was released.",
        )

    if len(new_parts) == 3:
        # standard release version (l.m.n) can be released after pre-release version (l.m.n.X)
        return

    def get_dev_value(text: str) -> int:
        matches = re.findall(r"dev(\d+)", text)
        values = [int(match) for match in matches]
        if not values:
            return -1
        return values[0]

    def get_rc_value(text: str) -> int:
        matches = re.findall(r"rc(\d+)", text)
        values = [int(match) for match in matches]
        if not values:
            return -1
        return values[0]

    latest_pre: str = latest_parts[3]
    new_pre: str = new_parts[3]
    latest_dev_value = get_dev_value(latest_pre)
    latest_rc_value = get_rc_value(latest_pre)
    new_dev_value = get_dev_value(new_pre)
    new_rc_value = get_rc_value(new_pre)

    if latest_dev_value != -1:
        if (latest_dev_value + 1) == new_dev_value:
            return
        if new_rc_value == 1:
            return

        raise ValueError(f"next pre-release version must be dev{latest_dev_value + 1} or rc1 or standard version.")

    if latest_rc_value != -1:
        if (latest_rc_value + 1) == new_rc_value:
            return

        raise ValueError(f"next pre-release version must be rc{latest_rc_value + 1} or standard version.")

    raise ValueError(f'Something went wrong. Current "{latest_parts}", New "{new_parts}".')


def _test_check_new_version_ok():
    for latest, new in [
        ("0.1.1", "1.0.0.dev1"),
        ("0.1.1", "1.1.0"),
        ("0.1.1", "1.0.1"),
        ("0.1.1", "1.0.0"),
        ("0.1.1", "0.2.0.dev1"),
        ("0.1.1", "0.2.1"),
        ("0.1.1", "0.2.0"),
        ("0.1.1", "0.1.2"),
        ("0.1.1", "0.1.1"),
        ("0.1.1", "0.1.1.rc1"),
        ("0.1.1.dev1", "0.1.1.dev2"),
        ("0.1.1.dev1", "0.1.1.dev3"),
        ("0.1.1.dev1", "0.1.1.rc1"),
        ("0.1.1.dev1", "0.1.1.rc2"),
        ("0.1.1.dev1", "0.1.1"),
        ("0.1.1.rc1", "0.1.1"),
        ("0.1.1.rc1", "0.1.1.rc2"),
        ("0.1.1.rc1", "0.1.1.rc3"),
        ("0.1.1.rc1", "0.1.1.dev1"),
    ]:
        try:
            print(f"Test latest {latest}, new {new}.")
            check_new_version_ok(latest, new)
            print("OK.")
        except Exception as e:
            print(f"NG. {str(e)}")


if __name__ == "__main__":
    main()
