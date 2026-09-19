from drawlib.apis import *

dtheme.allstyles.merge(
    dtheme.ThemeStyles(
        linestyle=LineStyle(width=5),
        textstyle=TextStyle(font=FontSansSerif.RALEWAYS_REGULAR, size=28),
    ),
    targets=[""],
)

config(width=100, height=50)
text((50, 15), "Hello Drawlib!")
line((30, 35), (70, 35))
save()
