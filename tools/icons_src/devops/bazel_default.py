# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""DevOps icon: bazel (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(29.5, 91.0), (50.0, 70.5), (29.5, 50.0), (9.0, 70.5)], style=Icon.fill_style('#76D275'))
polygon([(9.0, 70.5), (9.0, 50.0), (29.5, 29.5), (29.5, 50.0)], style=Icon.fill_style('#43A047'))
polygon([(70.5, 91.0), (91.0, 70.5), (70.5, 50.0), (50.0, 70.5)], style=Icon.fill_style('#76D275'))
polygon([(91.0, 70.5), (91.0, 50.0), (70.5, 29.5), (70.5, 50.0)], style=Icon.fill_style('#43A047'))
polygon([(50.0, 70.5), (70.5, 50.0), (50.0, 29.5), (29.5, 50.0)], style=Icon.fill_style('#43A047'))
polygon([(50.0, 29.5), (50.0, 9.0), (29.5, 29.5), (29.5, 50.0)], style=Icon.fill_style('#00701A'))
polygon([(50.0, 29.5), (70.5, 50.0), (70.5, 29.5), (50.0, 9.0)], style=Icon.fill_style('#004300'))
save()
# fmt: on
