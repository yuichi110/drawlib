# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Root package."""

import re
import sys
from typing import Final, List

# please update here when you release new version
LIB_VERSION = "0.2.3.dev2"

# please list active main committers (1+ commits per month)
AUTHORS: Final[List[str]] = [
    "Yuichi Ito <yuichi@yuichi.com>",
]

# please change accordingly
LIB_NAME: Final[str] = "drawlib"
DESCRIPTION: Final[str] = "Python drawing library. Illustration as Code."
HOMEPAGE: Final[str] = "https://www.drawlib.com"
REPOSITORY: Final[str] = "https://github.com/yuichi110/drawlib"
README: Final[str] = "pypi.md"

__version__: Final[str] = LIB_VERSION


def _check_version_syntax() -> None:  # noqa: C901
    parts = tuple(int(part) if part.isdigit() else part for part in LIB_VERSION.split("."))

    if not isinstance(parts[0], int):
        raise ValueError(f"Major version must be int. But {LIB_VERSION}")

    if not isinstance(parts[1], int):
        raise ValueError(f"Minor version must be int. But {LIB_VERSION}")

    if not isinstance(parts[0], int):
        raise ValueError(f"Patch version must be int. But {LIB_VERSION}")

    if len(parts) == 3:
        return

    if len(parts) != 4:
        raise ValueError(
            f'Version syntax is "major.minor.patch" or "major.minor.patch.pre-release". But {LIB_VERSION}',
        )

    pre_version = parts[3]
    if not isinstance(pre_version, str):
        raise ValueError(f"Pre-release version can't be int. But {LIB_VERSION}")

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

    if get_dev_value(pre_version) >= 1:
        return

    if get_rc_value(pre_version) >= 1:
        return

    raise ValueError(f"Pre-release version must be dev<n> or rc<n>. But {LIB_VERSION}")


try:
    _check_version_syntax()
except ValueError as e:
    print(f"System Error. Version syntax has problem. {str(e)}")
    print("Please check drawlib.__init__.py")
    print("Abort.")
    sys.exit(1)
