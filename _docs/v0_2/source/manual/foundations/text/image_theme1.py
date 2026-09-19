from drawlib.apis import *

config(width=100, height=50)
text(xy=(25, 15), text="Hello Drawlib.", style="red")
text(xy=(25, 35), text="Hello Drawlib.", size=12, style="bold")
text(xy=(75, 15), text="Hello Drawlib.", style="blue_light")
text(xy=(75, 35), text="Hello Drawlib.", size=24, style="green_bold")
save()
