from drawlib.apis import *

# Define ShapeStyle with name "mystyle"
dtheme.shapestyles.set(
    style=ShapeStyle(
        lstyle="dashed",
        lcolor=Colors140.BlueViolet,
        lwidth=3,
        fcolor=Colors140.Turquoise,
    ),
    name="mystyle",
)

# Define TextStyle with name "mystyle"
dtheme.textstyles.set(
    style=TextStyle(
        color=Colors140.BlueViolet,
        font=FontSansSerif.RALEWAYS_REGULAR,
        size=32,
    ),
    name="mystyle",
)
