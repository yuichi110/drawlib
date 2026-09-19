from drawlib.apis import *

dtheme.textstyles.merge(
    TextStyle(font=FontSansSerif.RALEWAYS_REGULAR, size=28),
)
dtheme.textstyles.merge(
    TextStyle(font=FontSansSerif.RALEWAYS_LIGHT, size=28),
    targets=["light"],
)
dtheme.textstyles.merge(
    TextStyle(font=FontSansSerif.RALEWAYS_BOLD, size=28),
    targets=["bold"],
)

config(width=100, height=50)
text((50, 15), "Hello Drawlib!")
text((50, 25), "Hello Drawlib!", style="light")
text((50, 35), "Hello Drawlib!", style="bold")
save()
