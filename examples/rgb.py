#!/usr/bin/env python3

"""RGB"""

import random

from gridcode import *


class RGB(Program, size=16, frame_rate=100):

    @staticmethod
    def setup(grid: Grid) -> None:
        for cell in grid.cells.all():
            grid.maps.add(cell, {"type": "counts",
                                 "r": 0,
                                 "g": 0,
                                 "b": 0})

            grid.maps.add(cell, {"type": "channels",
                                 "red": 0,
                                 "green": 0,
                                 "blue": 0})

    @staticmethod
    def update(grid: Grid) -> None:
        counts = random.choice(list(grid.maps.get(data={"type": "counts"})))

        channel = random.choice(["r", "g", "b"])
        counts[channel] = counts[channel] + 1

        r = counts["r"]
        g = counts["g"]
        b = counts["b"]
        brightest = max(r, g, b) * 1.0

        for channels in grid.maps.get(at_cells={counts.cell}, data={"type": "channels"}):
            channels.set({"red": r / brightest,
                          "green": g / brightest,
                          "blue": b / brightest})

    @staticmethod
    def color_for_cell(cell: Cell, grid: Grid) -> Color:
        for channels in grid.maps.get(at_cells={cell}, data={"type": "channels"}):
            return Color(channels["red"], channels["green"], channels["blue"])

        return Color(0, 0, 0)

    @staticmethod
    def on_cell_click(cell: Cell, grid: Grid) -> None:
        pass

    @staticmethod
    def on_key_press(key: str, grid: Grid) -> None:
        pass


if __name__ == "__main__":
    run(RGB)
