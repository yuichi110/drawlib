# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Math and geometry calculations for drawlib core."""

from drawlib._core.l3_math._geometry import (
    get_angle,
    get_center_and_size,
    get_distance,
    get_point_on_ellipse,
    get_rotated_path_points,
    get_rotated_points,
    minus_2points,
    plus_2points,
    rotate_point,
)
from drawlib._core.l3_math._routing import (
    RoutingType,
    Side,
    compute_orthogonal_path,
)

__all__ = [
    "RoutingType",
    "Side",
    "compute_orthogonal_path",
    "get_angle",
    "get_center_and_size",
    "get_distance",
    "get_point_on_ellipse",
    "get_rotated_path_points",
    "get_rotated_points",
    "minus_2points",
    "plus_2points",
    "rotate_point",
]
