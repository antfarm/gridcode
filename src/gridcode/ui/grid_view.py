"""``gridcode.ui.grid_view``"""

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
            self.canvas.itemconfig(cell_item, fill=color.to_rgb_hex())

    def add_cell_highlight(self, x: int, y: int) -> None:
        """``grid_view.add_cell_highlight(x, y)``"""
        cell_item = self.cell_item(x, y)
        self.canvas.itemconfig(cell_item, outline="red", width=5)
        self.canvas.tag_raise(cell_item)

    def remove_cell_highlight(self, x: int, y: int) -> None:
        """``grid_view.remove_cell_highlight(x, y)``"""
        cell_item = self.cell_item(x, y)
        self.canvas.itemconfig(cell_item, outline="black", width=3)

    def cell_item(self, x: int, y: int) -> int:
        return self.cell_items[y * self.size + x]
