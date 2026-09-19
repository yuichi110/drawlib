from drawlib.apis import *


def draw_versions(x: float, y: float, versions: list[str]):
    width = 6
    height = 5
    corner_angle = 60
    padding = 1

    s1 = ShapeStyle(halign="left", valign="bottom")
    s2 = ShapeStyle(halign="left", valign="bottom", lstyle="dashed", fcolor=Colors.Transparent)
    st1 = ShapeTextStyle(size=12, color=Colors.White, font=FontRoboto.ROBOTO_REGULAR)
    st2 = ShapeTextStyle(size=12, font=FontRoboto.ROBOTO_REGULAR)
    for i, version in enumerate(versions):
        if len(versions) == 5 and i in [0, 1]:
            chevron(
                (x + (width + padding) * i, y),
                width=width,
                height=height,
                corner_angle=corner_angle,
                style=s2,
                text=version,
                textstyle=st2,
            )
        else:
            chevron(
                (x + (width + padding) * i, y),
                width=width,
                height=height,
                corner_angle=corner_angle,
                style=s1,
                text=version,
                textstyle=st1,
            )


config(width=115, height=72)

ts = TextStyle(size=16, font=FontRoboto.ROBOTO_REGULAR)
text((7, 6), "private\nα\nrelease", style=ts)
text((7, 18), "public\nβ\nrelease", style=ts)
text((7, 30), "public\nreleases", style=ts)
text((7, 53), "matured\npublic\nreleases", style=ts)

# v0.1
draw_versions(15, 3, ["0.1.1", "...", "0.1.n"])
line((32, 9), (32, 14), arrowhead="->")

# v0.2
draw_versions(29, 15, ["0.2.1", "...", "0.2.n"])
line((46, 21), (46, 26), arrowhead="->")

text((50, 34), "dev only", style=TextStyle(size=14, font=FontRoboto.ROBOTO_REGULAR))
draw_versions(43, 27, ["0.3.0\ndev1", "...", "0.3.1", "...", "0.3.n"])
line((74, 33), (74, 38), arrowhead="->")
text((74, 39.5), 'keep "0.n.m" till library matures', style=TextStyle(font=FontRoboto.ROBOTO_REGULAR))
line((74, 42), (74, 47), arrowhead="->")

text((78, 55), "dev only", style=TextStyle(size=14, font=FontRoboto.ROBOTO_REGULAR))
draw_versions(71, 48, ["1.0.0\ndev1", "...", "1.0.1", "...", "1.0.n"])
line((102, 54), (102, 59), arrowhead="->")
text((102, 62), "...")

arrow(
    (15, 67),
    (113, 67),
    tail_width=3,
    head_width=7,
    head_length=5,
    head="->",
    style=ShapeStyle(lwidth=0),
    text="Time",
    textstyle=ShapeTextStyle(color=Colors.White, size=14, font=FontRoboto.ROBOTO_REGULAR),
)
save()
