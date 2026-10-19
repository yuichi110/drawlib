# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Business icon: sendgrid (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(91.0, 91.0), (91.0, 36.33), (63.67, 36.33), (63.67, 9.0), (9.0, 9.0), (9.0, 36.33), (9.0, 63.67), (36.33, 63.67), (36.33, 91.0)], style=Icon.fill_style('#9DD6E3'))
polygon([(9.0, 9.0), (36.33, 9.0), (36.33, 36.33), (9.0, 36.33)], style=Icon.fill_style('#3F72AB'))
polygon([(63.67, 36.33), (91.0, 36.33), (91.0, 63.67), (63.67, 63.67)], style=Icon.fill_style('#00A9D1'))
polygon([(36.33, 63.67), (63.67, 63.67), (63.67, 91.0), (36.33, 91.0)], style=Icon.fill_style('#00A9D1'))
polygon([(36.33, 36.33), (63.67, 36.33), (63.67, 63.67), (36.33, 63.67)], style=Icon.fill_style('#2191C4'))
polygon([(63.67, 63.67), (91.0, 63.67), (91.0, 91.0), (63.67, 91.0)], style=Icon.fill_style('#3F72AB'))
save()
# fmt: on
