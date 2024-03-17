from typing import Final, Union, Optional, List, Tuple, Dict, Any, Literal
import matplotlib.font_manager
import matplotlib.pyplot as pyplot
import matplotlib.patches as patches
import matplotlib.offsetbox as offsetbox
import PIL.Image
import numpy


matplotlib.font_manager.FontProperties()


class FontStyle:

    def __init__(
        self,
        family: Optional[str] = None,
        file: Optional[str] = None,
        size: Union[float, str, None] = None,
        style: Optional[Literal["normal", "italic", "oblique"]] = None,
        variant: Optional[Literal["normal", "small-caps"]] = None,
        weight: Union[int, str, None] = None,
        stretch: Union[int, str, None] = None,
        math_fontfamily: Optional[str] = None,
    ):
        self.family = family
        self.file = file
        self.size = size
        self.style = style
        self.variant = variant
        self.weight = weight
        self.stretch = stretch
        self.math_fontfamily = math_fontfamily


class LineStyle:

    def __init__(self, width, color, style, alpha):
        self.width = width
        self.color = color
        self.style = style
        self.alpha = alpha


class ShapeStyle:

    def __init__(self, lwidth, lcolor, lstyle, lalpha, fcolor, falpha):
        self.lwidth = lwidth
        self.lcolor = lcolor
        self.lstyle = lstyle
        self.lalpha = lalpha
        self.fcolor = fcolor
        self.falpha = falpha


class __Drawer:
    DEFAULT_WIDTH: Final[float] = 100
    DEFAULT_HEIGHT: Final[float] = 100
    DEFUALT_ASPECT: Final[str] = "equal"
    DEFAULT_AXIS: Final[bool] = False
    DEFAULT_LOGLEVEL: Final[str] = "info"
    SYSTEM_FONTS = ["serif", "sanserif"]

    class Title:
        def __init__(
            self,
            s: str,
            x: Optional[float] = None,
            y: Optional[float] = None,
        ):
            self.s = s
            self.x = x
            self.y = y

    class Text:
        def __init__(
            self,
            x: float,
            y: float,
            s: str,
            options: Dict[str, Any],
        ):
            self.x = x
            self.y = y
            self.s = s
            self.options = options

    class Line:
        def __init__(
            self,
            xs: List[float],
            ys: List[float],
        ):
            self.xs = xs
            self.ys = ys

    def __init__(self):
        self.width = self.DEFAULT_WIDTH
        self.height = self.DEFAULT_HEIGHT
        self.aspect = self.DEFUALT_ASPECT
        self.axis = self.DEFAULT_AXIS
        self.loglevel = self.DEFAULT_LOGLEVEL

        self.title_: Optional[self.Title] = None
        self._logger = None
        self._shapes: List[
            Union[
                patches.Patch,
                self.Text,
                self.Line,
                offsetbox.AnnotationBbox,
            ]
        ] = []
        self._image_cache: dict[Union[str, PIL.Image.Image], numpy.array] = {}

    ##############
    ### basics ###
    ##############

    def clear(self):
        self.__init__()

    def config(
        self,
        width: int | None = None,
        height: int | None = None,
        aspect: str | None = None,
        axis: bool | None = None,
    ) -> None:
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height
        if aspect is not None:
            self.aspect = aspect
        if axis is not None:
            self.axis = axis

    def plot(self):
        self._render()
        pyplot.show()

    def save(self, file: str):
        self._render()
        pyplot.savefig(file, bbox_inches="tight", pad_inches=0)

    def _render(self):
        fig = pyplot.figure()
        ax = fig.add_subplot(1, 1, 1)

        # configure
        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)
        ax.set_aspect(self.aspect)
        ax.axis("on" if self.axis else "off")

        # draw
        for shape in self._shapes:
            if isinstance(shape, patches.Patch):
                ax.add_patch(shape)
            elif isinstance(shape, self.Text):
                ax.text(shape.x, shape.y, shape.s)
            elif isinstance(shape, self.Line):
                ax.plot(shape.xs, shape.ys)
            elif isinstance(shape, offsetbox.AnnotationBbox):
                ax.add_artist(shape)

        if self.title_ is not None:
            t = self.title_
            d = {}
            if t.x:
                d["x"] = t.x
            if t.y:
                d["y"] = t.y
            ax.set_title(t.s, **d)

        fig.tight_layout()

    ####################################
    ### wrapper of matplotlib.patchs ###
    ####################################

    def arc(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        angle: float = 0,
    ):
        self._shapes.append(patches.Arc((x, y), width, height, angle))

    def arrow(self): ...

    def arrow_fancy(self): ...

    def circle(self, x: float, y: float, radius: float):
        self._shapes.append(patches.Circle((x, y), radius))

    def ellipse(self): ...

    def polygon(self): ...

    def polygon_circle(self): ...

    def polygon_regular(self): ...

    def rectangle(self): ...

    def rectangle_fancy(self): ...

    def wedge(self): ...

    ################
    ### original ###
    ################

    def title(
        self,
        s: str,
        x: Optional[float] = None,
        y: Optional[float] = None,
        style: Optional[FontStyle] = None,
    ):
        self.title_ = self.Title(s, x, y)

    def text(
        self,
        x: float,
        y: float,
        s: str,
        style: Optional[FontStyle] = None,
    ):
        options = {}
        if style is not None:
            options["fontproperties"] = style

        self._shapes.append(self.Text(x, y, s, options))

    def text_vertical(self, x: float, y: float, s: str): ...

    def image(
        self,
        x: float,
        y: float,
        file: Optional[str] = None,
        pilimg: Optional[PIL.Image.Image] = None,
        zoom=1,
    ):
        if file is None and pilimg is None:
            raise ValueError()
        if file and pilimg:
            raise ValueError()

        if file:
            if file not in self._image_cache:
                im = pyplot.imread(file)
                self._image_cache[file] = im
            else:
                im = self._image_cache[file]
        else:
            key = str(pilimg)
            if key not in self._image_cache:
                im = numpy.array(pilimg)
                self._image_cache[key] = im
            im = self._image_cache[key]

        imagebox = offsetbox.OffsetImage(im, zoom=zoom)
        ab = offsetbox.AnnotationBbox(imagebox, (x, y), frameon=False)
        self._shapes.append(ab)

    def line(self, x1: float, y1: float, x2: float, y2: float):
        self._shapes.append(self.Line([x1, x2], [y1, y2]))

    def lines(self, xys: List[Tuple[float, float]]):
        xs = [xy[0] for xy in xys]
        ys = [xy[1] for xy in xys]
        self._shapes.append(self.Line(xs, ys))

    def line_bezier(
        self,
        x: float,
        y: float,
        bezier_points: List[
            Union[
                Tuple[float, float],
                Tuple[float, float, float, float],
            ]
        ],
        smooth_points: int = 100,
    ):
        def quadratic_bezier(x0, y0, x1, y1, x2, y2):
            points = []
            for i in range(smooth_points):
                t = i / (smooth_points - 1)
                x = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * x1 + t**2 * x2
                y = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * y1 + t**2 * y2
                points.append((x, y))
            return zip(*points)

        xs = [x]
        ys = [y]
        for p in bezier_points:
            if len(p) == 2:
                xs.append(p[0])
                ys.append(p[1])
            elif len(p) == 4:
                bx, by = quadratic_bezier(xs[-1], ys[-1], p[0], p[1], p[2], p[3])
                xs.extend(bx[1:])
                ys.extend(by[1:])
            else:
                raise ValueError()

        self._shapes.append(self.Line(xs, ys))


################
### external ###
################

__d = __Drawer()
# basics
clear = __d.clear
config = __d.config
plot = __d.plot
save = __d.save

# patched shapes
circle = __d.circle

# original shapes
title = __d.title
text = __d.text
image = __d.image
line = __d.line
lines = __d.lines
line_bezier = __d.line_bezier
