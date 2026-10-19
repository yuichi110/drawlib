# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""AI icon: elevenlabs (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(26.08, 91.0), (43.17, 91.0), (43.17, 9.0), (26.08, 9.0)], style=Icon.fill_style('#18181B'))
polygon([(56.83, 91.0), (73.92, 91.0), (73.92, 9.0), (56.83, 9.0)], style=Icon.fill_style('#18181B'))
save()
# fmt: on
