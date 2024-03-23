from drawlib import *

LINESTYLE_SOLID = "solid"
LINESTYLE_DASH = "dash"

if not has_cache_linestyle(LINESTYLE_SOLID):
    set_cache_linestyle(
        LINESTYLE_SOLID,
        LineStyle(
            width=1,
            color="black",
            style="solid",
        ),
    )

if not has_cache_linestyle(LINESTYLE_DASH):
    set_cache_linestyle(
        LINESTYLE_DASH,
        LineStyle(
            width=1,
            color="black",
            style="dashed",
        ),
    )
