# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: vertex_ai."""

from drawlib.canvas import save
from drawlib.shapes import circle
from drawlib.utils import Gcp, Icon

Icon.setup()

chev_w = 7.8
Icon.draw_capsule((12.0, 32.0), (50.0, 8.0), width_units=chev_w, color=Gcp.YELLOW)
Icon.draw_capsule((88.0, 32.0), (50.0, 8.0), width_units=chev_w, color=Gcp.YELLOW)

col_w = 7.6
dot_r = 3.8

# Column 1 (x=22, GCP_RED)
circle((22.0, 90.0), radius=dot_r, style=Icon.fill_style(Gcp.RED))
Icon.draw_capsule((22.0, 54.0), (22.0, 76.0), width_units=col_w, color=Gcp.RED)
circle((22.0, 41.0), radius=dot_r, style=Icon.fill_style(Gcp.RED))

# Column 2 (x=36, GCP_YELLOW)
Icon.draw_capsule((36.0, 59.0), (36.0, 82.0), width_units=col_w, color=Gcp.YELLOW)
circle((36.0, 46.0), radius=dot_r, style=Icon.fill_style(Gcp.YELLOW))
circle((36.0, 33.0), radius=dot_r, style=Icon.fill_style(Gcp.YELLOW))

# Column 3 (x=50, GCP_GREEN)
circle((50.0, 66.0), radius=dot_r, style=Icon.fill_style(Gcp.GREEN))
circle((50.0, 53.0), radius=dot_r, style=Icon.fill_style(Gcp.GREEN))
Icon.draw_capsule((50.0, 23.0), (50.0, 40.0), width_units=col_w, color=Gcp.GREEN)

# Column 4 (x=64, GCP_YELLOW)
Icon.draw_capsule((64.0, 59.0), (64.0, 82.0), width_units=col_w, color=Gcp.YELLOW)
circle((64.0, 46.0), radius=dot_r, style=Icon.fill_style(Gcp.YELLOW))
circle((64.0, 33.0), radius=dot_r, style=Icon.fill_style(Gcp.YELLOW))

# Column 5 (x=78, GCP_BLUE)
circle((78.0, 90.0), radius=dot_r, style=Icon.fill_style(Gcp.BLUE))
circle((78.0, 76.0), radius=dot_r, style=Icon.fill_style(Gcp.BLUE))
Icon.draw_capsule((78.0, 41.0), (78.0, 63.0), width_units=col_w, color=Gcp.BLUE)

save()
