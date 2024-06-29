# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Helper script for getting latest drawlib version which includes pre-release."""

import json
import sys
import urllib.request

from packaging.version import parse


def get_latest_version(package_name):
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
            latest_version = max(all_versions, key=parse)
            return latest_version

    except Exception as e:
        print(f"Failed to fetch the latest version for package {package_name}")
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    latest_version = get_latest_version("drawlib")
    print(latest_version)
