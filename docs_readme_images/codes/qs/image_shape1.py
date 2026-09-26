from drawlib.canvas import save, setup
from drawlib.config import styles
from drawlib.shapes import rectangle, star

setup(width=100, height=50, grid=True)
star((25, 25), num_vertex=5, radius_ext=20, radius_int=7.5, style=styles.primary)
rectangle((75, 25), width=30, height=20, r=3, angle=45, style=styles.primary)

save()

