"""write docstring later"""

import os
import sys
from drawlib.advance import run
from drawlib._logging import logger
from drawlib._cli import DrawlibArgParser


def main() -> None:
    """write docstring later"""

    argparser = DrawlibArgParser()
    argparser.parse()
    argparser.apply_options()
    paths = argparser.get_positional_args()

    if len(paths) == 0:
        logger.critical("no input files and directories")
        logger.critical('check options with "drawlib --help"')
        sys.exit(1)

    for path in paths:
        if not os.path.isfile(path) and not os.path.isdir(path):
            msg = f'ignore arg "{path}" since it is not a file/dir path'
            logger.warning(msg)
            continue

        abspath = os.path.abspath(path)
        realpath = os.path.realpath(abspath)
        logger.info(realpath)
        run(realpath)


if __name__ == "__main__":
    main()
