# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Radar chart (spider web) components."""

from drawlib._charts.radar_chart._chart import RadarChart
from drawlib._charts.radar_chart._series import RadarSeries

# Alias for typo tolerance
RaderChart = RadarChart

__all__ = [
    "RadarChart",
    "RadarSeries",
    "RaderChart",
]
