"""``gridcode.ui.grid_view``"""

import functools
import sys
import tkinter

from ..runtime import Color


CANVAS_SIZE = 640


class GridView:
    """``GridView``"""

    def __init__(self, ui, parent, size: int):
        self.size = size

        self.canvas = tkinter.Canvas(parent,
                                     width=CANVAS_SIZE,
                                     height=CANVAS_SIZE,
                                     background="black",
                                     highlightthickness=0)
        self.canvas.pack()

        step = CANVAS_SIZE / size

        self.cell_items = []
        for y in range(size):
            for x in range(size):
                left = x * step
                top = y * step
                cell_item = self.canvas.create_rectangle(left,
                                                         top,
                                                         left + step,
                                                         top + step,
                                                         fill="black",
                                                         outline="black",
                                                         width=3)
                self.canvas.tag_bind(cell_item, "<Button-1>",
                                     lambda event, x=x, y=y: ui.cell_clicked(x, y))
                self.cell_items.append(cell_item)

    def draw(self, colors: list[Color]) -> None:
        """``grid_view.draw(colors)``"""
        for cell_item, color in zip(self.cell_items, colors):
            self.canvas.itemconfig(cell_item, fill=color_to_hex(*color))

    def add_cell_highlight(self, x: int, y: int) -> None:
        """``grid_view.add_cell_highlight(x, y)``"""
        cell_item = self._cell_item(x, y)
        self.canvas.itemconfig(cell_item, outline="red", width=5)
        self.canvas.tag_raise(cell_item)

    def remove_cell_highlight(self, x: int, y: int) -> None:
        """``grid_view.remove_cell_highlight(x, y)``"""
        cell_item = self._cell_item(x, y)
        self.canvas.itemconfig(cell_item, outline="black", width=3)

    def _cell_item(self, x: int, y: int) -> int:
        return self.cell_items[y * self.size + x]


@functools.lru_cache(maxsize=4096)
def color_to_hex(r: float, g: float, b: float, a: float) -> str:
    """``color_to_hex(r, g, b, a)``"""
    r, g, b = r * a, g * a, b * a
    if sys.platform == "darwin":
        r, g, b = _p3_to_srgb(r, g, b)
    return "#%02x%02x%02x" % (round(r * 255), round(g * 255), round(b * 255))


_P3_TO_SRGB = ((1.2249, -0.2247, 0.0000),
              (-0.0420, 1.0419, 0.0000),
              (-0.0197, -0.0786, 1.0979))


def _p3_to_srgb(r: float, g: float, b: float) -> tuple[float, float, float]:
    linear = [_to_linear(value) for value in (r, g, b)]
    converted = [sum(factor * value for factor, value in zip(row, linear))
                 for row in _P3_TO_SRGB]
    return tuple(_to_gamma(min(max(value, 0.0), 1.0)) for value in converted)


def _to_linear(value: float) -> float:
    if value <= 0.04045:
        return value / 12.92
    return ((value + 0.055) / 1.055) ** 2.4


def _to_gamma(value: float) -> float:
    if value <= 0.0031308:
        return value * 12.92
    return 1.055 * value ** (1 / 2.4) - 0.055
