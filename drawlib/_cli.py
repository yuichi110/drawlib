"""Manage CLI option when drawlib command is used"""

from typing import Optional, List
import argparse
import sys
import drawlib._const as const
import drawlib.settings as settings
from drawlib._logging import logger


class DrawlibArgParser:
    def __init__(self):

        parser = argparse.ArgumentParser(
            description='Ilustration as code by python',
        )
        parser.add_argument(
            'file_or_directory',
            nargs='...',
            help='Target python file or directory which contains python codes',
        )
        parser.add_argument(
            '-v',
            '--version',
            action='store_true',
            help='Show version',
        )
        parser.add_argument(
            '--quiet',
            action='store_true',
            help='Enable quiet logging. show only error messages',
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Enable verbose logging.',
        )
        parser.add_argument(
            '--developer',
            action='store_true',
            help='Enable verbose logging. Disable error handling for library users.',
        )
        self._parser = parser
        self._positional_args: Optional[List[str]] = None
        self._name_args: Optional[argparse.Namespace] = None

    def parse(self):
        self._name_args, _ = self._parser.parse_known_args()
        args = self._parser.parse_args()
        self._positional_args = args.file_or_directory

    def get_positional_args(self):
        if self._name_args is None:
            logger.critical(
                "DrawlibArgParser must be parsed before getting optional args"
            )
            sys.exit(1)
        return self._positional_args

    def apply_options(self):
        if self._name_args is None:
            logger.critical(
                "DrawlibArgParser must be parsed before apply options"
            )
            sys.exit(1)

        if self._name_args.version:
            logger.critical(const.VERSION)
            sys.exit(0)

        if self._name_args.quiet and (
            self._name_args.verbose or self._name_args.developer
        ):
            raise ValueError(
                "option --quiet can't use with option --debug and --devdebug"
            )

        if self._name_args.quiet:
            settings.set_logging_mode("quiet")

        if self._name_args.verbose:
            settings.set_logging_mode("verbose")

        if self._name_args.developer:
            settings.set_logging_mode("developer")
