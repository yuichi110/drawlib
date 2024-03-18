from typing import Final, Union, Optional, List, Tuple, Dict, Any, Literal
import matplotlib.font_manager
import matplotlib.artist
import matplotlib.lines
import matplotlib.text
import matplotlib.pyplot as pyplot
import matplotlib.patches as patches
import matplotlib.offsetbox as offsetbox
import PIL.Image
import numpy
import warnings
import inspect
import os
import math


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

    def __init__(
        self,
        width: Optional[float] = None,
        color: Union[float, str, Tuple[float, float, float], None] = None,
        style: Optional[Literal["solid", "dashed", "dotted", "dashdot"]] = None,
        alpha: Optional[float] = None,
    ):
        self.width = width
        self.color = color
        self.style = style
        self.alpha = alpha


class ShapeStyle:

    def __init__(
        self,
        color: Union[float, str, Tuple[float, float, float], None] = None,
        lwidth: Optional[float] = 0.1,
        lcolor: Union[float, str, Tuple[float, float, float], None] = None,
        lstyle: Optional[Literal["solid", "dashed", "dotted", "dashdot"]] = None,
        fcolor: Union[float, str, Tuple[float, float, float], None] = None,
        alpha: Optional[float] = None,
    ):
        self.color = color
        self.lwidth = lwidth
        self.lcolor = lcolor
        self.lstyle = lstyle
        self.fcolor = fcolor
        self.alpha = alpha


class TextBoxStyle:
    BOXSTYLE_SQUARE = "square"

    def __init__(
        self,
        boxstyle: Literal[
            "square",
            "circle",
            "ellipse",
            "larrow",
            "rarrow",
            "darrow",
            "round",
            "round4",
            "sawtooth",
            "roundtooth",
        ],
        lwidth: Optional[float] = 0.1,
        lcolor: Union[float, str, Tuple[float, float, float], None] = None,
        lstyle: Optional[Literal["solid", "dashed", "dotted", "dashdot"]] = None,
        fcolor: Union[float, str, Tuple[float, float, float], None] = None,
        alpha: Optional[float] = None,
        pad: Optional[float] = 0.3,
        rounding_size: Optional[float] = None,
        tooth_size: Optional[float] = None,
    ):
        self.boxstyle = boxstyle
        self.lwidth = lwidth
        self.lcolor = lcolor
        self.lstyle = lstyle
        self.fcolor = fcolor
        self.alpha = alpha
        self.pad = pad
        self.rounding_size = rounding_size
        self.tooth_size = tooth_size


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
            text: str,
            x: Optional[float] = None,
            y: Optional[float] = None,
            fontproperties: Optional[matplotlib.font_manager.FontProperties] = None,
        ):
            self.text = text
            self.x = x
            self.y = y
            self.fontproperties = fontproperties

    def __init__(self):
        self.width = self.DEFAULT_WIDTH
        self.height = self.DEFAULT_HEIGHT
        self.aspect = self.DEFUALT_ASPECT
        self.axis = self.DEFAULT_AXIS
        self.loglevel = self.DEFAULT_LOGLEVEL

        self._title: Optional[self.Title] = None
        self._logger = None
        self._artists: List[matplotlib.artist.Artist] = []
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

    def save(self, file: Optional[str] = None):
        if file is None:
            # get caller module info
            caller_frame = inspect.stack()[1]
            caller_module = inspect.getmodule(caller_frame[0])
            caller_module_file = caller_module.__file__
            caller_module_name = caller_module.__name__

            # create save file path
            parent_dir = os.path.dirname(os.path.abspath(caller_module_file))
            file_name = caller_module_name.split(".")[-1]
            file = f"{os.path.join(parent_dir, file_name)}.png"

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

        # draw artist (patches, line, text)
        for artist in self._artists:
            ax.add_artist(artist)

        # draw title
        if self._title is not None:
            options = {
                key: value
                for key, value in vars(self._title).items()
                if value is not None
            }
            ax.set_title(self._title.text, **options)

        # magic for making good margin
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
        self._artists.append(patches.Arc((x, y), width, height, angle))

    def arrow(self): ...

    def arrow_fancy(self): ...

    def circle(
        self,
        x: float,
        y: float,
        radius: float,
        angle: Optional[float] = None,
        text: Optional[str] = None,
        font: Optional[FontStyle] = None,
    ):
        # draw shape
        shape = patches.Circle((x, y), radius, color="red")
        self._artists.append(shape)

        # draw text
        if text:
            self._artists.append(self._get_shape_text(x, y, text, angle, font))

    def ellipse(self): ...

    def polygon(self): ...

    def polygon_circle(self): ...

    def polygon_regular(self): ...

    def rectangle(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        angle: Optional[float] = None,
        text: Optional[str] = None,
        font: Optional[FontStyle] = None,
    ):
        if angle is None:
            angle = 0

        # shape
        shape = patches.Rectangle(
            (x, y),
            width,
            height,
            angle=angle,
            rotation_point="center",
            color="red",
        )
        self._artists.append(shape)

        # draw text
        if text:
            center_x = x + width / 2
            center_y = y + height / 2
            t = self._get_shape_text(center_x, center_y, text, angle, font)
            self._artists.append(t)

    def rectangle_rounded(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        rtype: Optional[Literal["round", "round4", "sawtooth", "roundtooth"]] = None,
        pad: Optional[float] = None,
        text: Optional[str] = None,
        font: Optional[FontStyle] = None,
    ):
        if rtype is None:
            rtype = "round"
        if pad is None:
            pad = 0.3
        boxstyle = f"{rtype},pad={pad}"

        # shape
        shape = patches.FancyBboxPatch(
            (x + pad, y + pad),
            width - pad * 2,
            height - pad * 2,
            boxstyle=boxstyle,
            color="red",
        )
        self._artists.append(shape)

        # draw text
        if text:
            center_x = x + width / 2
            center_y = y + height / 2
            t = self._get_shape_text(center_x, center_y, text, font=font)
            self._artists.append(t)

    def wedge(self): ...

    def _get_shape_text(
        self,
        x: float,
        y: float,
        text: str,
        angle: Optional[float] = None,
        font: Optional[FontStyle] = None,
    ) -> matplotlib.text.Text:
        return matplotlib.text.Text(
            x,
            y,
            text,
            rotation=angle,
            rotation_mode="anchor",
            horizontalalignment="center",
            verticalalignment="center",
            fontproperties=self._get_font_properties(font),
        )

    ################
    ### original ###
    ################

    def title(
        self,
        text: str,
        x: Optional[float] = None,
        y: Optional[float] = None,
        style: Optional[FontStyle] = None,
    ):
        fp = self._get_font_properties(style)
        self._title = self.Title(text, x, y, fp)

    def text(
        self,
        x: float,
        y: float,
        text_: str,
        font: Optional[FontStyle] = None,
        box: Optional[TextBoxStyle] = None,
    ):
        fp = self._get_font_properties(font)
        bx = self._get_bbox_dict(box)
        t = matplotlib.text.Text(x, y, text_, fontproperties=fp, bbox=bx)
        self._artists.append(t)

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
        self._artists.append(ab)

    def line(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        style: Optional[LineStyle] = None,
    ):
        options = self._get_line_options(style)
        line = matplotlib.lines.Line2D(
            xdata=[x1, x2],
            ydata=[y1, y2],
            **options,
        )
        self._artists.append(line)

    def lines(
        self,
        xys: List[Tuple[float, float]],
        style: Optional[LineStyle] = None,
    ):
        xs = [xy[0] for xy in xys]
        ys = [xy[1] for xy in xys]
        options = self._get_line_options(style)
        line = matplotlib.lines.Line2D(xdata=xs, ydata=ys, **options)
        self._artists.append(line)

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

        options = self._get_line_options(style)
        line = matplotlib.lines.Line2D(xdata=xs, ydata=ys, **options)
        self._artists.append(line)

    ############
    ### util ###
    ############

    def _get_font_properties(
        self,
        style: Optional[FontStyle],
    ) -> Optional[matplotlib.font_manager.FontProperties]:
        if style is None:
            return None

        return matplotlib.font_manager.FontProperties(
            family=style.family,
            style=style.style,
            variant=style.variant,
            weight=style.weight,
            stretch=style.stretch,
            size=style.size,
            fname=style.file,
            math_fontfamily=style.math_fontfamily,
        )

    def _get_line_options(self, style: Optional[LineStyle] = None) -> Dict[str, Any]:
        if style is None:
            return {}

        return {
            "linewidth": style.width,
            "linestyle": style.style,
            "color": style.color,
            "alpha": style.alpha,
        }

    def _get_shape_options(self, style: Optional[ShapeStyle] = None) -> Dict[str, Any]:
        if style is None:
            return {}

        options = {
            "facecolor": style.fcolor if style.fcolor is not None else style.color,
            "edgecolor": style.lcolor if style.lcolor is not None else style.color,
            "linestyle": style.lstyle,
            "linewidth": style.lwidth,
            "alpha": style.alpha,
        }
        return {key: value for key, value in options.items() if value is not None}

    def _get_bbox_dict(self, style: Optional[TextBoxStyle] = None) -> Dict[str, Any]:
        if style is None:
            return {}

        return {}


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
rectangle = __d.rectangle
rectangle_rounded = __d.rectangle_rounded

# original shapes
title = __d.title
text = __d.text
image = __d.image
line = __d.line
lines = __d.lines
line_bezier = __d.line_bezier


def get_angle(x1: float, y1: float, x2: float, y2: float) -> float:
    dx = x2 - x1
    dy = y2 - y1
    angle_rad = math.atan2(dy, dx)
    angle_deg = math.degrees(angle_rad)
    return (angle_deg + 360) % 360


def warning_suppress(module: Optional[str] = None):
    if module is None:
        warnings.filterwarnings("ignore")
    else:
        warnings.filterwarnings("ignore", module=module)
