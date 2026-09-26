from drawlib.canvas import save, setup
from drawlib.images import image
from drawlib.lines import line
from drawlib.config import styles
from drawlib.shapes import circle
from drawlib.text import text

setup(width=100, height=100, grid=True)
line((10, 10), (90, 90), style=styles.primary)
circle((25, 75), radius=20, style=styles.primary)
image((75, 25), width=30, image="python.png")
text((75, 5), "Hello drawlib!", style=styles.primary)

save()

