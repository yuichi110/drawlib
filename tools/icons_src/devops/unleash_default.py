# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""DevOps icon: unleash (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(63.67, 90.98), (63.67, 36.35), (90.97, 36.35), (90.97, 90.98)], style=Icon.fill_style('#1A4049'))
polygon([(36.33, 63.68), (36.33, 90.98), (9.0, 90.98), (9.0, 9.02), (63.67, 9.02), (63.67, 36.35), (36.33, 36.35)], style=Icon.fill_style('#1A4049'))
polygon([(91.0, 36.32), (63.67, 36.32), (63.67, 9.02), (91.0, 9.02)], style=Icon.fill_style('#817AFE'))
save()
# fmt: on
