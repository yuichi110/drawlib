from drawlib.canvas import config, save
from drawlib.preset_styles import get_styles
from drawlib.shapes import rectangle, star

config(width=100, height=50, grid=True)
ps = get_styles()

star((25, 25), num_vertex=5, radius_ext=20, radius_int=7.5, style=ps.primary)
rectangle((75, 25), width=30, height=20, r=3, angle=45, style=ps.primary)

save()

