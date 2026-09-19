from drawlib.apis import *

config(grid=True, height=60, dpi=200)

CODE = """from drawlib.apis import *

circle(
    xy=(50, 50),
    radius=30,
    style=ShapeStyle(
        lstyle="dashed",
        lcolor=Colors140.BlueViolet,
        lwidth=5,
        fcolor=Colors140.Turquoise,
    ),
)
save()"""


def upper():
    y = 52
    text(
        xy=(20, y),
        text="Drawlib",
        style=TextStyle(size=28, font=FontRoboto.ROBOTO_BOLD),
    )
    icon_phosphor.heart(
        xy=(38, y),
        width=7,
        style=IconStyle(color=Colors140.Pink, style="fill"),
    )
    text(
        xy=(70, y),
        text="Illustration as Code",
        style=TextStyle(size=28, font=FontRoboto.ROBOTO_BOLD),
    )


def middle():
    image_y = 12
    arrow_y = 28
    style = ImageStyle(lwidth=1, valign="bottom")

    sc = dsart.SourceCode(style="default", font=FontSourceCode.ROBOTO_MONO)
    text = dsart.SourceCode.get_text("inside.py")
    sc.draw((25, image_y), width=40, code=text, style=style)

    arrow((50, arrow_y), (60, arrow_y), tail_width=5, head_width=10, head_length=5, head="->")

    image((80, image_y), width=31.5, image="inside.png", style=style)


def lower():
    y = 6
    style = TextStyle(size=20, font=FontRoboto.ROBOTO_REGULAR)
    icon_phosphor.file_py(xy=(15, y), width=5)
    text((28, y), "Python Code", style=style)
    text((55, y), "to", style=style)
    icon_phosphor.file_image(xy=(72, y), width=5)
    text((83, y), "Illustration", style=style)


upper()
middle()
lower()

save()
