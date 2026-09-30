# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Common help epilog and formatting for drawlib CLI commands."""

from __future__ import annotations

HELP_EPILOG: str = (
    "[bold cyan]AI Instructions:[/bold cyan]\n"
    '  • Run [bold yellow]"drawlib rules show agent-instruction"[/bold yellow] '
    "for AI agent bootstrap and workflow loop.\n"
    '  • Run [bold yellow]"drawlib rules show cli"[/bold yellow] '
    "to inspect full CLI commands, arguments, and options.\n"
    '  • Run [bold yellow]"drawlib rules show overview"[/bold yellow] '
    "for canvas lifecycle and drawing architecture.\n"
    '  • Run [bold yellow]"drawlib rules list"[/bold yellow] '
    "to explore all available drawing guideline topics."
)
