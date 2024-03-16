from typing import Any, Final, Union, List, Tuple
import matplotlib.pyplot as pyplot
import matplotlib.patches as patches


class __Drawer:
    DEFAULT_CONFIG_WIDTH: Final[float] = -1.0
    DEFAULT_CONFIG_HEIGHT: Final[float] = -1.0
    DEFUALT_CONFIG_ASPECT: Final[str] = "equal"
    DEFAULT_CONFIG_AXIS: Final[bool] = False
    DEFAULT_CONFIG_LOGLEVEL: Final[str] = "info"

    class Text:
        def __init__(self, x: float, y: float, s: str):
            self.x = x
            self.y = y
            self.s = s

    class Line:
        def __init__(self, xs: List[float], ys: List[float]):
            self.xs = xs
            self.ys = ys

    def __init__(self):
        self.width = self.DEFAULT_CONFIG_WIDTH
        self.height = self.DEFAULT_CONFIG_HEIGHT
        self.aspect = self.DEFUALT_CONFIG_ASPECT
        self.axis = self.DEFAULT_CONFIG_AXIS
        self.loglevel = self.DEFAULT_CONFIG_LOGLEVEL

        self._logger = None
        self._shapes: List[Union[patches.Patch, self.Text, self.Line]] = []

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
        pyplot.savefig(file)

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

    def circle(self, x: float, y: float, radius: float, **kwargs: Any):
        self._shapes.append(patches.Circle((x, y), radius, **kwargs))

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

    def text(self, x: float, y: float, s: str):
        self._shapes.append(self.Text(x, y, s))

    def image(self): ...

    def line(self, x1: float, y1: float, x2: float, y2: float):
        xs = [x1, x2]
        ys = [y1, y2]
        self._shapes.append(self.Line(xs, ys))

    def lines(self, xys: List[Tuple[float, float]]):
        xs = [xy[0] for xy in xys]
        ys = [xy[1] for xy in xys]
        self._shapes.append(self.Line(xs, ys))

    def line_bezier(
        self,
        bezier_points: List[
            Union[
                Tuple[float, float],
                Tuple[float, float, float, float],
                Tuple[float, float, float, float, float, float],
            ],
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

        xs = []
        ys = []
        for i, p in enumerate(bezier_points):
            length = len(p)
            if i == 0:
                if length == 4:
                    xs.extend([p[0], p[2]])
                    ys.extend([p[1], p[3]])
                elif length == 6:
                    bx, by = quadratic_bezier(p[0], p[1], p[2], p[3], p[4], p[5])
                    xs.extend(bx)
                    ys.extend(by)
                else:
                    raise ValueError()
                continue
            if length == 2:
                xs.append(p[0])
                ys.append(p[1])
            elif length == 4:
                bx, by = quadratic_bezier(xs[-1], ys[-1], p[0], p[1], p[2], p[3])
                xs.extend(bx[1:])
                ys.extend(by[1:])
            else:
                raise ValueError(f"index {i}")

        self._shapes.append(self.Line(xs, ys))


__d = __Drawer()
# basics
clear = __d.clear
config = __d.config
plot = __d.plot
save = __d.save

# shapes
circle = __d.circle
text = __d.text
line = __d.line
lines = __d.lines
line_bezier = __d.line_bezier
