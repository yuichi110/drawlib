from drawlib.apis import *

config(width=100, height=50)

# get style.
green_style = dtheme.textstyles.get("green")
text((15, 25), "Get Style", size=24, style=green_style)

# set style
dtheme.textstyles.set(
    style=TextStyle(color=Colors.White, bgfcolor=Colors.Black, bglwidth=0, size=24),
    name="bgblack",
)
text((40, 25), "Set Style", style="bgblack")

# update(get -> modify -> set) style
s = dtheme.textstyles.get("red")
s.size = 36
s.font = FontSerif.COURIER_REGULAR
dtheme.textstyles.set(s, "red")
text((75, 25), "Update Style", style="red")

save()
