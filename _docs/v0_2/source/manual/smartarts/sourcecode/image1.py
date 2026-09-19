from drawlib.apis import *

CODE = """
from drawlib.apis import *

config(width=100, height=100)
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
save()
""".strip()

config(width=100, height=50)

sc1 = dsart.SourceCode(
    language="python",
    style="default",
)
sc1.draw((25, 25), width=40, code=CODE)

sc2 = dsart.SourceCode(
    style="monokai",
    font=FontSourceCode.ROBOTO_MONO,
    show_linenum=True,
    linenum_textcolor=Colors140.Black,
    linenum_bgcolor=Colors140.LightGray,
)
sc2.draw((75, 25), width=40, code=CODE, style=ImageStyle(lwidth=2, lcolor=Colors.Red))

save()
