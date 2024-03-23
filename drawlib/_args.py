"""write docstring later"""

import sys
import drawlib._const as const

if "-v" in sys.argv or "--version" in sys.argv:
    print(const.VERSION)
    sys.exit(0)

if "-h" in sys.argv or "--help" in sys.argv:
    print("python drawlib. illustration as code.")
    print("options")
    print("  -h:         show help")
    print("  --help:     show help")
    print("  -v:         show version")
    print("  --version:  show version")
    print("  --debug:    show stacktrace(verbose error message)")
    print("  --devdebug: show native error message")
    sys.exit(0)
