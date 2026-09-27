# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Geometry type definitions for drawlib."""


# Modern type definitions
Coordinate = tuple[float, float]
Coordinates = list[Coordinate]

Bezier2 = tuple[Coordinate, Coordinate]
Bezier3 = tuple[Coordinate, Coordinate, Coordinate]
PathPoint = Coordinate | Bezier2 | Bezier3
PathPoints = list[PathPoint]
