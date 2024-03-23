"""write docstring later"""

import sys
from typing import List
from drawlib import *


def main(paths: List[str]):
    """write docstring later"""

    for path in paths:
        ...


if __name__ == "__main__":
    paths = []
    for arg in sys.argv:
        if arg in [
            # args for calling drawlib
            "python",
            "-m",
            "drawlib",
            # options
            "-v",
            "--version",
            "--debug",
            "--devdebug",
        ]:
            continue
        paths.append(arg)

    if len(paths):
        print("no input files and directories")
        print("syntax: drawlib <files or directories> <options>")
        exit(1)

    main(paths)
