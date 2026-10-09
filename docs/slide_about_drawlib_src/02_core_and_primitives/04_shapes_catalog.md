::: block (80, 45) (1760, 110)
# 23 Geometric Primitives (`drawlib.shapes`)
A rich vocabulary of vector shapes—all supporting `style` (including rotation `style.angle`), `text`, and `text_style`.
:::

::: block (80, 165) (1760, 810)
```drawlib file:shapes_catalog.svg
from drawlib.canvas import clear, save, setup
from drawlib.shapes import (
    bubblespeech,
    chevron,
    circle,
    cylinder,
    donuts,
    ellipse,
    face,
    parallelogram,
    polygon,
    rectangle,
    regularpolygon,
    rhombus,
    star,
    trapezoid,
    triangle,
    wedge,
)
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=176, height=81)

cols = [24, 66, 110, 152]
rows = [67, 46, 25, 6]

def draw_cell_label(cx: float, cy: float, label: str) -> None:
    text((cx, cy - 8.2), label, style=Styles.DarkBold.patch(text_size=8.5))

# Row 1 (y = 67)
rectangle((cols[0], rows[0]), width=22, height=11, r=2.5, style=Styles.PrimaryFlat, text="Hero Card", text_style=Styles.WhiteBold.patch(text_size=8.5))
draw_cell_label(cols[0], rows[0], "rectangle(r=2.5)")

circle((cols[1], rows[0]), radius=6.0, style=Styles.Neutral, text="Node", text_style=Styles.DarkBold.patch(text_size=8.5))
draw_cell_label(cols[1], rows[0], "circle()")

ellipse((cols[2], rows[0]), width=22, height=11, style=Styles.PrimaryNeutral, text="Topic", text_style=Styles.DarkBold.patch(text_size=8.5))
draw_cell_label(cols[2], rows[0], "ellipse()")

cylinder((cols[3], rows[0]), width=16, height=12, disks=3, style=Styles.SecondaryNeutral, text="DB", text_style=Styles.DarkBold.patch(text_size=8.5))
draw_cell_label(cols[3], rows[0], "cylinder(disks=3)")

# Row 2 (y = 46)
rhombus((cols[0], rows[1]), width=22, height=12, style=Styles.BlueNeutral, text="Gate?", text_style=Styles.DarkBold.patch(text_size=8.5))
draw_cell_label(cols[0], rows[1], "rhombus()")

trapezoid((cols[1], rows[1]), height=10.5, bottomedge_width=22, topedge_width=13, style=Styles.Neutral, text="Pool", text_style=Styles.DarkBold.patch(text_size=8.5))
draw_cell_label(cols[1], rows[1], "trapezoid()")

parallelogram((cols[2], rows[1]), width=20, height=10.5, corner_angle=68, style=Styles.TealNeutral, text="I/O Stream", text_style=Styles.DarkBold.patch(text_size=8.0))
draw_cell_label(cols[2], rows[1], "parallelogram()")

triangle((cols[3], rows[1]), width=18, height=11, style=Styles.PrimaryNeutral, text="Delta", text_style=Styles.DarkBold.patch(text_size=8.0, xy_shift=(0, -1.5)))
draw_cell_label(cols[3], rows[1], "triangle()")

# Row 3 (y = 25)
regularpolygon((cols[0], rows[2]), num_vertex=6, radius=6.5, style=Styles.PrimaryFlat, text="Pod", text_style=Styles.WhiteBold.patch(text_size=8.5))
draw_cell_label(cols[0], rows[2], "regularpolygon(6)")

star((cols[1], rows[2]), num_vertex=5, radius_ext=6.8, radius_int=3.2, style=Styles.SecondaryNeutral)
draw_cell_label(cols[1], rows[2], "star(5)")

donuts((cols[2], rows[2]), radius=6.2, width=2.4, style=Styles.BlueNeutral, text="75%", text_style=Styles.DarkBold.patch(text_size=7.5))
draw_cell_label(cols[2], rows[2], "donuts()")

wedge((cols[3], rows[2]), radius=6.2, angle_start=0, angle_end=240, width=2.6, style=Styles.PrimaryNeutral)
draw_cell_label(cols[3], rows[2], "wedge()")

# Row 4 (y = 6 -> shape centers at y=9.5, labels at y=1.3)
r3_y = 9.5
chevron((cols[0], r3_y), width=22, height=10, corner_angle=55, style=Styles.SecondaryNeutral, text="Stage 1", text_style=Styles.DarkBold.patch(text_size=8.5))
draw_cell_label(cols[0], r3_y, "chevron()")

bubblespeech(
    xy=(cols[1] - 11, r3_y - 4.5),
    width=22,
    height=9.5,
    tail_edge="left",
    tail_start_ratio=0.25,
    tail_vertex_xy=(cols[1] - 15, r3_y - 2.0),
    tail_end_ratio=0.65,
    style=Styles.Neutral,
    text="Note!",
    text_style=Styles.DarkBold.patch(text_size=8.5),
)
draw_cell_label(cols[1], r3_y, "bubblespeech()")

face((cols[2], r3_y), radius=5.8, mood="smile", style=Styles.PrimaryNeutral)
draw_cell_label(cols[2], r3_y, 'face(mood="smile")')

polygon(
    [(cols[3] - 10, r3_y - 4.5), (cols[3] + 6, r3_y - 4.5), (cols[3] + 11, r3_y), (cols[3] + 6, r3_y + 4.5), (cols[3] - 10, r3_y + 4.5)],
    style=Styles.Neutral,
    text="Custom",
    text_style=Styles.DarkBold.patch(text_size=8.0),
)
draw_cell_label(cols[3], r3_y, "polygon(xys)")

save()
```
:::

::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils
utils.draw_page_number()
```
:::

::: note
- `drawlib.shapes` provides 23 geometric primitives out of the box.
- Here is a 4x4 visual catalog of 16 core shapes: rounded rectangles, circles, ellipses, multi-disk 3D database cylinders, rhombuses, trapezoids, parallelograms, triangles, hexagons (`regularpolygon`), stars, donuts, wedges, chevrons, speech bubbles, expressive user faces, and arbitrary polygons.
:::
