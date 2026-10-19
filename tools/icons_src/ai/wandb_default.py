# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""AI icon: wandb (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import circle
from drawlib.utils import Icon

Icon.setup()
_st = Icon.fill_style("#FCBC32")

# Left column (top to bottom)
circle((17.53, 85.60), radius=5.33, style=_st)
circle((17.49, 64.47), radius=8.47, style=_st)
circle((17.44, 43.36), radius=5.33, style=_st)
circle((17.49, 22.22), radius=8.47, style=_st)

# Middle column (top to bottom)
circle((50.03, 77.68), radius=5.25, style=_st)
circle((50.08, 56.65), radius=5.33, style=_st)
circle((50.08, 35.47), radius=8.49, style=_st)
circle((50.08, 14.40), radius=5.33, style=_st)

# Right column (top to bottom)
circle((82.62, 85.60), radius=5.33, style=_st)
circle((82.57, 64.44), radius=8.43, style=_st)
circle((82.62, 43.25), radius=5.33, style=_st)
circle((82.62, 22.18), radius=5.33, style=_st)

save()
