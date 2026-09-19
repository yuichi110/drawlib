import drawlib.apis

import docs.commons.style


def draw_3circles(x: float, y: float, radius: float, margin: float) -> None:
    x_shift = 2 * radius + margin
    drawlib.apis.circle((x - x_shift, y), radius)
    drawlib.apis.circle((x, y), radius)
    drawlib.apis.circle((x + x_shift, y), radius)


def draw_3rectangle(x: float, y: float, width: float, height: float, margin: float) -> None:
    x_shift = width + margin
    drawlib.apis.rectangle((x - x_shift, y), width, height, style="flat")
    drawlib.apis.rectangle((x, y), width, height, style="flat")
    drawlib.apis.rectangle((x + x_shift, y), width, height, style="flat")


def draw_logo(x: float = 15, y: float = 5):
    drawlib.apis.text(
        (x, y),
        text="Drawlib",
        style=drawlib.apis.TextStyle(
            color=drawlib.apis.Colors140.BlueViolet,
            size=24,
            font=drawlib.apis.FontFile("avenger/regular.ttf"),
        ),
    )
