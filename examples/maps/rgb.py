#!/usr/bin/env python3

"""RGB"""

import random

from gridcode import *
from gridcode.data.maps import MapsData


class RGB(Program, data_class=MapsData, size=16, frame_rate=100):

    @staticmethod
    def setup(grid: Grid[MapsData]) -> None:
        for cell in grid.cells.all():
            grid.data.maps.add(cell, {"type": "counts",
                                 "r": 0,
                                 "g": 0,
                                 "b": 0})

            grid.data.maps.add(cell, {"type": "channels",
                                 "red": 0,
                                 "green": 0,
                                 "blue": 0})

    @staticmethod
    def update(grid: Grid[MapsData]) -> None:
        counts = random.choice(list(grid.data.maps.select(matches={"type": "counts"})))

        channel = random.choice(["r", "g", "b"])
        counts[channel] = counts[channel] + 1

        r, g, b = counts.get("r", "g", "b")
        brightest = max(r, g, b) * 1.0

        for channels in grid.data.maps.select(at_cells={counts.cell},
                                               matches={"type": "channels"}):
            channels.set({"red": r / brightest,
                          "green": g / brightest,
                          "blue": b / brightest})

    @staticmethod
    def color_for_cell(grid: Grid[MapsData], cell: Cell) -> Color:
        for channels in grid.data.maps.select(at_cells={cell}, matches={"type": "channels"}):
            return Color(channels["red"], channels["green"], channels["blue"])

        return Color(0, 0, 0)

    @staticmethod
    def on_cell_click(grid: Grid[MapsData], cell: Cell) -> None:
        pass

    @staticmethod
    def on_key_press(grid: Grid[MapsData], key: str) -> None:
        pass


if __name__ == "__main__":
    run(RGB)
