from drawlib.apis import *

config(width=100, height=60, grid=True)

icon_phosphor.airplane((25, 30), width=20)
icon_phosphor.coffee(
    xy=(75, 30),
    width=20,
    angle=45,
    style=IconStyle(color=Colors.Red, style="fill"),
)

save()
