# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Subcommands package for drawlib CLI."""

from __future__ import annotations

from drawlib._cli.commands.build import build_app
from drawlib._cli.commands.cache import cache_app
from drawlib._cli.commands.colors import colors_app
from drawlib._cli.commands.css import css_app
from drawlib._cli.commands.init import init_app
from drawlib._cli.commands.rules import cmd_rules_show, rules_app
from drawlib._cli.commands.serve import cmd_serve
from drawlib._cli.commands.show import cmd_show
from drawlib._cli.commands.styles import styles_app

__all__ = [
    "build_app",
    "cache_app",
    "cmd_rules_show",
    "cmd_serve",
    "cmd_show",
    "colors_app",
    "css_app",
    "init_app",
    "rules_app",
    "styles_app",
]
