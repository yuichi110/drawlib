from typing import Any
import matplotlib.pyplot as pyplot
import matplotlib.patches as patches


class __Drawer:

    def __init__(self):
        self.width = 0
        self.height = 0
        self.aspect = "equal"
        self.axis = True

        self.fig, self.ax = pyplot.subplots()
        self.shapes = []

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

    def Circle(self, x: float, y: float, radius: float, **kwargs: Any):
        self.shapes.append(patches.Circle((x, y), radius, **kwargs))

    def plot(self):
        self._render()
        pyplot.show()

    def save(self, file: str):
        self._render()
        pyplot.savefig(file)

    def _render(self):
        for shape in self.shapes:
            self.ax.add_patch(shape)
        self.ax.set_xlim(0, self.width)
        self.ax.set_ylim(0, self.height)
        self.ax.set_aspect(self.aspect)
        self.ax.axis("on" if self.axis else "off")


__d = __Drawer()
config = __d.config
plot = __d.plot
save = __d.save
Circle = __d.Circle
