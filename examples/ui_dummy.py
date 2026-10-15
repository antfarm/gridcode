#!/usr/bin/env python3

"""Empty"""

import random

from gridcode import *


class UIDummy(Program, size=32, frame_rate=8):

    @staticmethod
    def setup(grid: Grid) -> None:
        pass

    @staticmethod
    def update(grid: Grid) -> None:
        pass

    @staticmethod
    def color_for_cell(grid: Grid, cell: Cell) -> Color:
        n = 2
        r = random.randint(0, n) / n
        g = random.randint(0, n) / n
        b = random.randint(0, n) / n
        return Color(r, g, b)

    @staticmethod
    def on_key_press(grid: Grid, key: str) -> None:
        pass

    @staticmethod
    def on_cell_click(grid: Grid, cell: Cell) -> None:
        pass


if __name__ == "__main__":
    run(UIDummy)
