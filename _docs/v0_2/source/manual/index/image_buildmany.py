from drawlib.apis import *

dtheme.apply_official_theme("essentials")
config(grid=True, height=60)

rect_width = 20
rect_height = 38
dtheme.linestyles.merge(LineStyle(width=0.5), [""])
dtheme.textstyles.merge(TextStyle(size=12, halign="left"))
dtheme.iconstyles.merge(IconStyle(style="thin"))

tscenter16 = TextStyle(halign="center", size=16)
tscenter16r = TextStyle(halign="center", size=16, color=ColorsThemeEssentials.Red)


def left():
    text((15, 54), "Drawlib's\nDocument Source", style=tscenter16)

    rectangle(
        xy=(15, 30),
        width=rect_width,
        height=rect_height,
        r=2,
        style="dashed",
    )

    x = 8
    icon_phosphor.folder((x, 45), width=3)
    text((x + 2.5, 45), "docs")
    line((x, 43), (x, 13))

    line((x, 42), (x + 1, 42))
    icon_phosphor.folder((x + 3, 42), width=3)
    text((x + 5.5, 42), "commons")
    line((x + 3, 40), (x + 3, 35))
    icon_phosphor.file_py((x + 6, 39), width=3, style="red")
    text((x + 8.5, 39), "style.py", style="red")
    line((x + 3, 39), (x + 4, 39))
    icon_phosphor.file_py((x + 6, 36), width=3, style="red")
    text((x + 8.5, 36), "util.py", style="red")
    line((x + 3, 36), (x + 4, 36))

    line((x, 30), (x + 1, 30))
    icon_phosphor.folder((x + 3, 30), width=3)
    text((x + 5.5, 30), "chapter1")
    line((x + 3, 28), (x + 3, 19))
    icon_phosphor.file_md((x + 6, 27), width=3)
    text((x + 8.5, 27), "doc.md")
    line((x + 3, 27), (x + 4, 27))
    icon_phosphor.file_py((x + 6, 24), width=3, style="red")
    text((x + 8.5, 24), "img1.py", style="red")
    line((x + 3, 24), (x + 4, 24))
    icon_phosphor.file_py((x + 6, 21), width=3, style="red")
    text((x + 8.5, 21), "img2.py", style="red")
    line((x + 3, 21), (x + 4, 21))

    line((x, 15), (x + 1, 15))
    icon_phosphor.folder((x + 3, 15), width=3)
    text((x + 5.5, 15), "chapter2")


def center():
    text((50, 54), "Traditional\nDocument Source", style=tscenter16)
    rectangle(
        xy=(50, 30),
        width=rect_width,
        height=rect_height,
        r=2,
        style="dashed",
    )

    x = 43
    icon_phosphor.folder((x, 45), width=3)
    text((x + 2.5, 45), "docs")
    line((x, 43), (x, 13))

    line((x, 30), (x + 1, 30))
    icon_phosphor.folder((x + 3, 30), width=3)
    text((x + 5.5, 30), "chapter1")
    line((x + 3, 28), (x + 3, 19), style=LineStyle(width=0.5))
    icon_phosphor.file_md((x + 6, 27), width=3)
    text((x + 8.5, 27), "doc.md")
    line((x + 3, 27), (x + 4, 27), style=LineStyle(width=0.5))
    icon_phosphor.file_image((x + 6, 24), width=3, style="red")
    text((x + 8.5, 24), "img1.png", style="red")
    line((x + 3, 24), (x + 4, 24), style=LineStyle(width=0.5))
    icon_phosphor.file_image((x + 6, 21), width=3, style="red")
    text((x + 8.5, 21), "img2.png", style="red")
    line((x + 3, 21), (x + 4, 21))

    line((x, 15), (x + 1, 15))
    icon_phosphor.folder((x + 3, 15), width=3)
    text((x + 5.5, 15), "chapter2")


def right():
    text((85, 54), "Output Documents", style=tscenter16)

    rectangle(
        xy=(85, 30),
        width=rect_width,
        height=rect_height,
        r=2,
        style="dashed",
    )

    icon_phosphor.file_pdf((85, 43), width=6)
    icon_phosphor.file_html((85, 35), width=6)
    icon_phosphor.file_ppt((85, 27), width=6)
    icon_phosphor.book_bookmark((85, 19), width=6)
    text((85, 14.5), text="eBook", style=tscenter16)


def bottom():
    rectangle(
        xy=(50, 5),
        width=90,
        height=6,
        r=2,
        style="solid",
    )
    icon_phosphor.github_logo((17, 5), width=5)
    text(
        (53, 5),
        "Illustration and doc text versioning with CI/CD automation",
        style=tscenter16,
    )


left()
arrow(
    (28, 35),
    (37, 35),
    tail_width=3,
    head_width=6,
    head_length=3,
    style="red_flat",
    text="Drawlib",
    textstyle=ShapeTextStyle(
        size=14,
        color=Colors.White,
        font=FontRoboto.ROBOTO_BOLD,
        xy_shift=(-0.5, -0.1),
    ),
)
text((32, 25), "Build\nImages", style=tscenter16r)
center()
arrow(
    (63, 35),
    (72, 35),
    tail_width=3,
    head_width=6,
    head_length=3,
    style="solid",
)
text((67, 25), "Build\nDocs", style=tscenter16)
right()
bottom()
save()
