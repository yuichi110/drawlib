from drawlib.canvas import save, setup
from drawlib.images import image
from drawlib.lines import line
from drawlib.shapes import circle
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=200, height=100, color=Colors.canvas)
line((10, 10), (90, 90), style=Styles.Primary)
circle((25, 75), radius=20, style=Styles.Primary)
image((75, 25), width=30, image="python.png")
text((75, 5), "Hello drawlib!", style=Styles.Primary)

save()
