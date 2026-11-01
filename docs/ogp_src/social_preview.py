# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Primary GitHub Social Preview (1280x640): Source -> Doc Code (.md / .py) -> Output (Site, Doc, Slide)."""

from __future__ import annotations

from drawlib.canvas import save
from drawlib.utils import draw_git_repo_3col_ogp

draw_git_repo_3col_ogp(
    left_title="Source",
    left_sub="App Code & Specs",
    center_title="Doc Code (.md / .py)",
    center_title_size=13.2,
    right_title="Output",
    right_sub="Site, Doc, Slide",
)
save()
