from drawlib.apis import *

xs = [28, 48, 68, 88]
ys = [80, 50, 20]


def draw_header():
    x0 = 10
    y0 = 92

    text((x0, y0), "width \\ type", style="red")
    text((xs[0], y0), "(default)", style="red")
    text((xs[1], y0), "flat", style="red")
    text((xs[2], y0), "solid", style="red")
    text((xs[3], y0), "dashed", style="red")
    text((x0, ys[0]), "light", style="red")
    text((x0, ys[1]), "(default)", style="red")
    text((x0, ys[2]), "bold", style="red")


def draw_content():
    ts16 = dtheme.textstyles.get()
    ts16.size = 16

    for i, style_type in enumerate(["", "flat", "solid", "dashed"]):
        for j, style_width in enumerate(["light", "", "bold"]):
            if style_type == "flat":
                if style_width in ["light", "bold"]:
                    continue

            x = xs[i]
            y = ys[j]
            st = f"_{style_type}" if style_type != "" else ""
            sw = f"_{style_width}" if style_width != "" else ""
            style = f"blue{st}{sw}"

            if style_type in ["", "flat"]:
                circle((x - 4, y), 4, style=style)
                icon_phosphor.heart((x + 4.5, y - 0.5), width=8, style=style)
            else:
                circle((x, y), 4, style=style)

            if style_type != "flat":
                line((x - 7.5, y - 8), (x + 7.5, y - 8), style=style)
            if style_type == "":
                text((x, y - 12), style, style=style)
            else:
                text((x, y - 12), style, style=ts16)


dtheme.allstyles.merge(dtheme.ThemeStyles(textstyle=TextStyle(size=20)))

draw_header()
draw_content()

save()
