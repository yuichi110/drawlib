# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Entry point of drawlib command."""

from drawlib.v0_2.private.command import call


def main() -> None:
    """Call latest drawlib command"""
    call()


if __name__ == "__main__":
    main()
