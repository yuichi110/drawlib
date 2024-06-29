# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Root package."""

from typing import Final, List

# please update here when you release new version
LIB_VERSION = "0.1.33.dev2"

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
