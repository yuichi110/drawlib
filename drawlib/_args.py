import argparse
import sys
import logging
import drawlib._const as const

__parser = argparse.ArgumentParser(
    description='Ilustration as code by python',
)
__parser.add_argument(
    '-v',
    '--version',
    action='store_true',
    help='Show version',
)
__parser.add_argument(
    '--quiet',
    action='store_true',
    help='Enable quiet mode. show only error messages',
)
__parser.add_argument(
    '--debug',
    action='store_true',
    help='Enable debug mode. Verbose logging and stacktrace at error.',
)
__parser.add_argument(
    '--devdebug',
    action='store_true',
    help='Enable liberary developer debug mode. Verbose logging and raw error.',
)

__args = __parser.parse_args()

if __args.version:
    print(const.VERSION)
    sys.exit(0)

if __args.quiet and (__args.debug or __args.devdebug):
    raise ValueError(
        "option --quiet can't use with option --debug and --devdebug"
    )

if __args.quiet:
    log_level = logging.CRITICAL

if __args.debug:
    log_level = logging.DEBUG

if __args.devdebug:
    log_level = logging.DEBUG
    is_devdebug_mode = True
