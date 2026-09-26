from drawlib.canvas import save, setup
from drawlib.lines import line, line_curved, lines
from drawlib.config import styles

setup(width=100, height=50, grid=True)
line((10, 25), (40, 25), arrowhead="->", style=styles.primary)
line_curved((60, 10), (90, 40), bend=0.3, style=styles.primary)
lines([(25, 10), (50, 40), (75, 10)], style=styles.primary)

save()

