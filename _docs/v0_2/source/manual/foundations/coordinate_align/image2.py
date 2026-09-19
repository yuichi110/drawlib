from drawlib.apis import *

config(width=100, height=100, grid_only=True)

for x, halign in [(15, "left"), (50, "center"), (85, "right")]:
    for y, valign in [(15, "bottom"), (50, "center"), (85, "top")]:
        rectangle(
            xy=(x, y),
            width=15,
            height=15,
            style=ShapeStyle(halign=halign, valign=valign),
            text=f"({halign}, {valign})",
            textstyle=ShapeTextStyle(size=14),
        )
        circle(
            xy=(x, y),
            radius=1,
            style=ShapeStyle(lcolor=Colors.Red, fcolor=Colors.Red),
        )

save()
