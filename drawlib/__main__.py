"""write docstring later"""

import os
import sys
from typing import List
from drawlib.advance import run
import drawlib._args as args


def main(paths: List[str]):
    """write docstring later"""

    def get_abspath(path):
        abspath = os.path.abspath(path)
        return os.path.realpath(abspath)

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

    if len(paths) == 0:
        print("no input files and directories")
        print("syntax: drawlib <files or directories> <options>")
        exit(1)

    for path in paths:
        abspath = get_abspath(path)
        run(abspath)


if __name__ == "__main__":
    ...
