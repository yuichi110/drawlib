from typing import List, Optional, Tuple, Union
from matplotlib.lines import Line2D

from drawlib._model import LineStyle
from drawlib._core.util import get_line_options


def get_line(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    style: Optional[LineStyle] = None,
) -> Line2D:
    options = get_line_options(style)
    return Line2D(
        xdata=[x1, x2],
        ydata=[y1, y2],
        **options,
    )


def get_lines(
    xys: List[Tuple[float, float]],
    style: Optional[LineStyle] = None,
):
    xs = [xy[0] for xy in xys]
    ys = [xy[1] for xy in xys]
    options = get_line_options(style)
    return Line2D(xdata=xs, ydata=ys, **options)


def get_line_bezier(
    x: float,
    y: float,
    bezier_points: List[
        Union[
            Tuple[float, float],
            Tuple[float, float, float, float],
        ]
    ],
    smooth_points: int = 100,
    style: Optional[LineStyle] = None,
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

    options = get_line_options(style)
    return Line2D(xdata=xs, ydata=ys, **options)
